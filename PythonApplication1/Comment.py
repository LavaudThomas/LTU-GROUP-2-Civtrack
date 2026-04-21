class Comment:
    def __init__(self, commentID, reportID, text, time):
        self._commentID = commentID
        self._reportID = reportID
        self._text = text
        self._time = time

    def deleteComment(self):
        print("Comment deleted")
