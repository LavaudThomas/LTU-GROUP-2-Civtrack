from enum import Enum

class IncidentStatus(Enum):
    SUBMITTED = "Submitted"
    UNDER_REVIEW = "Under Review"
    APPROVED = "Approved"
    REJECTED = "Rejected"
    RESOLVED = "Issue Resolved"