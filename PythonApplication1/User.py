class User:
    def __init__(self, userID, username, email, password, isAdmin=False, isGuest=False):
        self._userID = userID
        self._username = username
        self._email = email
        self._password = password
        self._isAdmin = isAdmin
        self._isGuest = isGuest

        self._loggedIn = False

    # -------------------------
    # AUTH STATE (for logic only)
    # -------------------------
    def login(self, password):
        if password == self._password:
            self._loggedIn = True
            return True
        return False

    def logout(self):
        self._loggedIn = False

    def updatePassword(self, newPassword):
        self._password = newPassword

    # -------------------------
    # CONVERT FOR DATABASE
    # -------------------------
    def to_dict(self):
        return {
            "username": self._username,
            "email": self._email,
            "password": self._password,
            "isAdmin": self._isAdmin,
            "isGuest": self._isGuest
        }