from datetime import datetime

class Timestamp:
    def __init__(self):
        now = datetime.now()

        self.year = now.year
        self.month = now.month
        self.day = now.day
        self.hour = now.hour
        self.minute = now.minute

    def format(self):
        return f"{self.year}-{self.month:02d}-{self.day:02d} {self.hour:02d}:{self.minute:02d}"