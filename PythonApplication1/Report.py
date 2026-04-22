from incident_status import IncidentStatus
from Timestamp import Timestamp


class Report:
    def __init__(self, reportID, incidentType, description, location, time=None):
        self._reportID = reportID
        self._incidentType = incidentType
        self._description = description
        self._location = location

        # If no time is passed, generate automatically
        self._time = time if time else Timestamp().format()

        # Default state
        self._status = IncidentStatus.SUBMITTED

        # Optional features (future-proof)
        self._imagePaths = []
        self._comments = []

    # -------------------------
    # STATUS MANAGEMENT
    # -------------------------
    def updateStatus(self, new_status):
        """
        Updates report status using IncidentStatus enum
        """
        self._status = new_status

    def approve(self):
        self._status = IncidentStatus.APPROVED

    def reject(self):
        self._status = IncidentStatus.REJECTED

    def submit(self):
        self._status = IncidentStatus.SUBMITTED

    # -------------------------
    # COMMENTS
    # -------------------------
    def addComment(self, comment):
        self._comments.append(comment)

    def getComments(self):
        return self._comments

    # -------------------------
    # IMAGES
    # -------------------------
    def attachImages(self, images):
        """
        images: list of file paths or URLs
        """
        if len(self._imagePaths) + len(images) <= 7:
            self._imagePaths.extend(images)

    def getImages(self):
        return self._imagePaths

    # -------------------------
    # GETTERS
    # -------------------------
    def getStatus(self):
        return self._status

    def getIncidentType(self):
        return self._incidentType

    def getLocation(self):
        return self._location

    def getTime(self):
        return self._time

    # -------------------------
    # DATABASE CONVERSION
    # -------------------------
    def to_dict(self, username):
        return {
            "username": username,
            "incident": self._incidentType,
            "description": self._description,
            "location": self._location,
            "status": self._status.value,
            "timestamp": self._time
        }