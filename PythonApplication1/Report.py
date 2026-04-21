from incident_status import IncidentStatus
from Comment import Comment
from Timestamp import Timestamp

class Report:
    def __init__(self, reportID, incidentType, description, location, time):
        self._reportID = reportID
        self._incidentType = incidentType
        self._description = description
        self._location = location
        self._imagePaths = []      # string[0..*]
        self._status = IncidentStatus.SUBMITTED
        self._time = time
        self._comments = []        # Comment[0..*]

    def addComment(self, comment):
        self._comments.append(comment)

    def updateStatus(self, status):
        self._status = status

    def attachImages(self, images):
        self._imagePaths.extend(images)