class UserAlreadyBanned(Exception):

    def __str__(self):
        return "User already banned"
