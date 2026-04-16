from User import User
class Admin(User):
    def __init__(self, userID, username, email, password, adminID):
        super().__init__(userID, username, email, password, isAdmin=True)
        self._adminID = adminID
        self._pendingReports = []   # report[0..*] → list

    # Public methods
    def reviewReport(self, report):
        print(f"Reviewing report: {report.title}")

    def approveReport(self, report):
        report.status = "Approved"
        print(f"Report '{report.title}' approved")

    def rejectReport(self, report):
        report.status = "Rejected"
        print(f"Report '{report.title}' rejected")

    def updateReportStatus(self, report, status):
        report.status = status
        print(f"Report '{report.title}' updated to {status}")

    def deleteComment(self, comment):
        print("Comment deleted")