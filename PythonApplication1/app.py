from flask import Flask, render_template, request, redirect, session
import os
import uuid
from werkzeug.utils import secure_filename

from supabase_client import supabase
from User import User
from Admin import Admin
from Report import Report
from Comment import Comment
from incident_status import IncidentStatus
from Timestamp import Timestamp

app = Flask(__name__)
app.secret_key = "civtrack_secret"

# -------------------------
# IMAGE UPLOAD CONFIG
# -------------------------
app.config["UPLOAD_FOLDER"] = "static/uploads"

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

admin = Admin(1, "admin", "admin@email.com", "password", 1)

# -------------------------
# ADMIN HELPER
# -------------------------
def admin_required(func):
    def wrapper(*args, **kwargs):
        if not session.get("user"):
            return redirect("/")

        if session.get("isadmin") is not True:
            return "Access Denied (Admin only)", 403

        return func(*args, **kwargs)

    wrapper.__name__ = func.__name__
    return wrapper


# -------------------------
# HOME
# -------------------------
@app.route("/")
def home():
    return render_template("index.html")


# -------------------------
# LOGIN
# -------------------------
@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    user = supabase.table("users") \
        .select("*") \
        .eq("username", username) \
        .eq("password", password) \
        .execute()

    if not user.data:
        return render_template("index.html", error="Invalid login")

    db_user = user.data[0]

    session["user"] = username

    raw_admin = db_user.get("isadmin", False)
    session["isadmin"] = str(raw_admin).strip().lower() in ["true", "1", "yes"]

    return redirect("/")


# -------------------------
# LOGOUT
# -------------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# -------------------------
# CREATE USER
# -------------------------
@app.route("/create_user", methods=["POST"])
def create_user():
    username = request.form.get("username")

    existing = supabase.table("users") \
        .select("*") \
        .eq("username", username) \
        .execute()

    if existing.data:
        return render_template("index.html", error="Username already exists")

    user = User(
        0,
        username,
        request.form.get("email"),
        request.form.get("password")
    )

    supabase.table("users").insert(user.to_dict()).execute()

    return render_template("user_created.html")


# -------------------------
# SUBMIT REPORT
# -------------------------
@app.route("/submit_report", methods=["POST"])
def submit_report():
    if not session.get("user"):
        return redirect("/")

    username = session["user"]

    image = request.files.get("image")
    filename = None

    if image and image.filename:
        ext = image.filename.rsplit(".", 1)[-1].lower()
        filename = f"{uuid.uuid4().hex}.{ext}"
        image.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

    report = Report(
        0,
        request.form.get("incident"),
        request.form.get("description"),
        request.form.get("location")
    )

    data = report.to_dict(username)
    data["image_url"] = filename

    supabase.table("reports").insert(data).execute()

    return render_template("thank_you.html")


# -------------------------
# PUBLIC REPORT FEED
# -------------------------
@app.route("/reports")
def view_reports():
    search = request.args.get("search")

    reports = supabase.table("reports") \
        .select("*") \
        .order("id", desc=True) \
        .execute().data or []

    comments = supabase.table("comments").select("*").execute().data or []

    for r in reports:
        r["comments"] = [
            c for c in comments if c.get("report_id") == r.get("id")
        ]

    reports = [
        r for r in reports
        if r.get("status") in [
            IncidentStatus.APPROVED.value,
            IncidentStatus.RESOLVED.value
        ]
    ]

    if search:
        search = search[:50].lower()
        reports = [
            r for r in reports
            if search in (r.get("incident", "").lower())
            or search in (r.get("description", "").lower())
            or search in (r.get("location", "").lower())
        ]

    return render_template("reports.html", reports=reports, search=search)


# -------------------------
# REPORT DETAIL PAGE
# -------------------------
@app.route("/report/<int:report_id>")
def report_detail(report_id):
    report_data = supabase.table("reports") \
        .select("*") \
        .eq("id", report_id) \
        .execute().data

    if not report_data:
        return "Report not found", 404

    report = report_data[0]

    comments = supabase.table("comments") \
        .select("*") \
        .eq("report_id", report_id) \
        .execute().data or []

    return render_template("report_detail.html", report=report, comments=comments)


# -------------------------
# ADD COMMENT
# -------------------------
@app.route("/add_comment", methods=["POST"])
def add_comment():
    comment = Comment(
        0,
        request.form.get("report_id"),
        request.form.get("text"),
        Timestamp().format()
    )

    supabase.table("comments").insert(comment.to_dict()).execute()

    return redirect("/reports")


# -------------------------
# ADMIN DASHBOARD
# -------------------------
@app.route("/admin")
@admin_required
def admin_dashboard():
    reports = supabase.table("reports") \
        .select("*") \
        .order("id", desc=True) \
        .execute().data or []

    admin_reports = [
        r for r in reports
        if r.get("status") not in [
            IncidentStatus.RESOLVED.value,
            IncidentStatus.REJECTED.value
        ]
    ]

    return render_template("admin.html", reports=admin_reports)


# -------------------------
# STATUS FLOW
# -------------------------
@app.route("/review/<int:report_id>")
@admin_required
def mark_under_review(report_id):
    supabase.table("reports").update({
        "status": IncidentStatus.UNDER_REVIEW.value
    }).eq("id", report_id).execute()

    return redirect("/admin")


@app.route("/approve/<int:report_id>")
@admin_required
def approve_report(report_id):
    admin.approveReport(supabase, report_id)
    return redirect("/admin")


@app.route("/reject/<int:report_id>")
@admin_required
def reject_report(report_id):
    supabase.table("reports").delete().eq("id", report_id).execute()
    return redirect("/admin")


@app.route("/resolve/<int:report_id>")
@admin_required
def resolve_report(report_id):
    supabase.table("reports").update({
        "status": IncidentStatus.RESOLVED.value
    }).eq("id", report_id).execute()

    return redirect("/admin")


# -------------------------
# STATS
# -------------------------
@app.route("/stats")
def stats():
    reports = supabase.table("reports").select("*").execute().data or []

    return render_template(
        "stats.html",
        total=len(reports),
        submitted=len([r for r in reports if r.get("status") == IncidentStatus.SUBMITTED.value]),
        review=len([r for r in reports if r.get("status") == IncidentStatus.UNDER_REVIEW.value]),
        approved=len([r for r in reports if r.get("status") == IncidentStatus.APPROVED.value]),
        resolved=len([r for r in reports if r.get("status") == IncidentStatus.RESOLVED.value])
    )


# -------------------------
# RUN
# -------------------------
if __name__ == "__main__":
    print("CivTrack running...")
    app.run(debug=True)