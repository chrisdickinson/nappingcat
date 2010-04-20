class Request(object):
    def __init__(self, user, command, settings, streams):
        self.user = user
        self.command = command
        self.settings = settings
        self.stdin, self.stdout, self.stderr = streams
