from User import User
from Admin import Admin
from Report import Report
from Comment import Comment
from incident_status import IncidentStatus
from Timestamp import Timestamp

def main():
    users = []
    reports = []

    username = input("Enter username: ")
    email = input("Enter email: ")
    password = input("Enter password: ")

    user = User(1, username, email, password)
    users.append(user)

    title = input("Enter report type: ")
    desc = input("Enter description: ")
    loc = input("Enter location: ")

    time = Timestamp(4, 21, 2026, 15, 30)
    report = Report(1, title, desc, loc, time)

    user.submitReport(report)
    reports.append(report)

    print("Report submitted successfully!")

# THIS RUNS YOUR PROGRAM
if __name__ == "__main__":
    main()