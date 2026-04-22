from flask import Flask, render_template, request

# Supabase connection
from supabase_client import supabase

# Your OOP classes (kept for structure + future features)
from User import User
from Report import Report
from Admin import Admin
from Comment import Comment
from incident_status import IncidentStatus
from Timestamp import Timestamp

app = Flask(__name__)


# -------------------------
# HOME PAGE
# -------------------------
@app.route("/")
def home():
    return render_template("index.html")


# -------------------------
# CREATE USER
# -------------------------
@app.route("/create_user", methods=["POST"])
def create_user():
    user = User(
        0,
        request.form["username"],
        request.form["email"],
        request.form["password"]
    )

    supabase.table("users").insert(user.to_dict()).execute()

    return "User created successfully"


# -------------------------
# SUBMIT REPORT
# -------------------------
@app.route("/submit_report", methods=["POST"])
def submit_report():
    username = request.form["username"]

    report = Report(
        0,
        request.form["incident"],
        request.form["description"],
        request.form["location"],
        None
    )

    supabase.table("reports").insert(
        report.to_dict(username)
    ).execute()

    return "Report submitted successfully"


# -------------------------
# VIEW REPORTS
# -------------------------
@app.route("/reports")
def view_reports():
    response = supabase.table("reports").select("*").execute()
    reports = response.data

    if not reports:
        return "No reports yet"

    output = ""
    for r in reports:
        output += f"""
        <b>Incident:</b> {r['incident']}<br>
        <b>Location:</b> {r['location']}<br>
        <b>Status:</b> {r['status']}<br>
        <hr>
        """

    return output


# -------------------------
# RUN APP
# -------------------------
if __name__ == "__main__":
    print("CivicTrack running...")
    app.run(debug=True)