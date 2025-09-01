class UserModel:
    def __init__(self, username="", password=""):
        self.username = username
        self.password = password

    def is_valid(self):
        return bool(self.username and self.password)
