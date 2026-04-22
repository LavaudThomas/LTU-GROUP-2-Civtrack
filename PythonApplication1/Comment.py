class Comment:
    def __init__(self, commentID, reportID, text, time):
        self._commentID = commentID
        self._reportID = reportID
        self._text = text
        self._time = time

    # -------------------------
    # DELETE LOGIC (REAL VERSION)
    # -------------------------
    def deleteComment(self, supabase):
        supabase.table("comments").delete().eq("id", self._commentID).execute()

    # -------------------------
    # CONVERT TO DATABASE FORMAT
    # -------------------------
    def to_dict(self):
        return {
            "report_id": self._reportID,
            "text": self._text,
            "timestamp": self._time
        }

    # -------------------------
    # GETTERS (optional but useful)
    # -------------------------
    def getText(self):
        return self._text

    def getReportID(self):
        return self._reportID

    def getTime(self):
        return self._time