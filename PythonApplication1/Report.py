from incident_status import IncidentStatus

class Report:
    def __init__(self, reportID, incidentType, description, location, time):
        self._reportID = reportID
        self._incidentType = incidentType
        self._description = description
        self._location = location
        self._time = time

        self._status = IncidentStatus.SUBMITTED
        self._imagePaths = []
        self._comments = []

    # -------------------------
    # STATUS
    # -------------------------
    def updateStatus(self, status):
        self._status = status

    # -------------------------
    # COMMENTS (kept for requirement)
    # -------------------------
    def addComment(self, comment):
        self._comments.append(comment)

    # -------------------------
    # IMAGES (kept for requirement)
    # -------------------------
    def attachImages(self, images):
        self._imagePaths.extend(images)

    # -------------------------
    # CONVERT TO DATABASE FORMAT
    # -------------------------
    def to_dict(self, username):
        return {
            "username": username,
            "incident": self._incidentType,
            "description": self._description,
            "location": self._location,
            "status": self._status.value
        }