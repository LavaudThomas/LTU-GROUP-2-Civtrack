class User:
    def __init__(self, userID, username, email, password, isAdmin=False, isGuest=False):
        self._userID = userID
        self._username = username
        self._email = email
        self._password = password
        self._isAdmin = isAdmin
        self._isGuest = isGuest
        self._loggedIn = False

    # Public methods
    def login(self, password):
        if password == self._password:
            self._loggedIn = True
            print("Login successful")
        else:
            print("Incorrect password")

    def logout(self):
        self._loggedIn = False
        print("Logged out")

    def updatePassword(self, newPassword):
        self._password = newPassword
        print("Password updated")

    def submitReport(self, report):
       print(f"{self._username} submitted a report: {report._incidentType}")



