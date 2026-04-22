class User:
    def __init__(self, userID, username, email, password, isAdmin=False, isGuest=False):
        self._userID = userID
        self._username = username
        self._email = email
        self._password = password

        # normalize booleans (important for Supabase consistency)
        self._isAdmin = bool(isAdmin)
        self._isGuest = bool(isGuest)

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
    # GETTERS (IMPORTANT FOR CLEAN USE)
    # -------------------------
    def isAdmin(self):
        return self._isAdmin

    def isGuest(self):
        return self._isGuest

    def isLoggedIn(self):
        return self._loggedIn

    # -------------------------
    # CONVERT FOR DATABASE
    # -------------------------
    def to_dict(self):
        return {
            "username": self._username,
            "email": self._email,
            "password": self._password,
            "isadmin": self._isAdmin,
            "isguest": self._isGuest
        }