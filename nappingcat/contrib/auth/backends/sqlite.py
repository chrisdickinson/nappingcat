from nappingcat import auth

class AuthBackend(auth.AuthBackend):
    def __init__(self, *args, **kwargs):
        super(AuthBackend, self).__init__(*args, **kwargs)

    def has_permission(self, user, permission):
        pass

    def add_permission(self, user, permission):
        pass

    def remove_permission(self, user, permission):
        pass

    def add_user(self, username):
        pass

    def add_key_to_user(self, user, key):
        pass

    def get_keys(self, username):
        pass

    def get_users(self):
        pass

