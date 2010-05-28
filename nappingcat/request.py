from nappingcat import auth

class Request(object):
    def __init__(self, user, command, settings, streams):
        self.user = user
        self.command = command
        self.settings = settings
        self.stdin, self.stdout, self.stderr = streams
        self.auth_backend = auth.get_auth_backend_from_settings(settings)
