from nappingcat import auth

class Request(object):
    def __init__(self, user, command, settings, streams, root_patterns):
        self.user = user
        self.command = command
        self.settings = settings
        self.stdin, self.stdout, self.stderr = streams
        self.root_patterns = root_patterns 
        self.auth_backend = auth.get_auth_backend_from_settings(settings)
