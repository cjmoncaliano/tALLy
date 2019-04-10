from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, name, id, role, upass, email, active=True):
        self.name = name
        self.password = upass
        self.id = id
        self.active = active
        self.role = role
        self.email = email

    def is_active(self):
        # Here you should write whatever the code is
        # that checks the database if your user is active
        return self.active

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True