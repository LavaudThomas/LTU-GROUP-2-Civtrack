from User import User
from incident_status import IncidentStatus


class Admin(User):
    def __init__(self, userID, username, email, password, adminID):
        super().__init__(userID, username, email, password, isAdmin=True)
        self._adminID = adminID

    # -------------------------
    # REVIEW (view only)
    # -------------------------
    def reviewReport(self, report):
        print(f"Reviewing report: {report.getIncidentType()} at {report.getLocation()}")

    # -------------------------
    # APPROVE REPORT
    # -------------------------
    def approveReport(self, supabase, report_id):
        supabase.table("reports").update({
            "status": IncidentStatus.APPROVED.value
        }).eq("id", report_id).execute()

    # -------------------------
    # REJECT REPORT (now DELETE handled in Flask, but kept for flexibility)
    # -------------------------
    def rejectReport(self, supabase, report_id):
        supabase.table("reports").delete().eq("id", report_id).execute()

    # -------------------------
    # UPDATE STATUS (GENERIC)
    # -------------------------
    def updateReportStatus(self, supabase, report_id, status):
        supabase.table("reports").update({
            "status": status.value if hasattr(status, "value") else status
        }).eq("id", report_id).execute()

    # -------------------------
    # GET PENDING REPORTS (FIXED)
    # -------------------------
    def getPendingReports(self, supabase):
        response = supabase.table("reports").select("*").execute()

        return [
            r for r in response.data
            if r["status"] in [
                IncidentStatus.SUBMITTED.value,
                IncidentStatus.UNDER_REVIEW.value
            ]
        ]

    # -------------------------
    # DELETE COMMENT (OPTIONAL FEATURE)
    # -------------------------
    def deleteComment(self, supabase, comment_id):
        supabase.table("comments").delete().eq("id", comment_id).execute()