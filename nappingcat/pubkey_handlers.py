import os
import StringIO

class AuthorizedKeysFile(object):
    def __init__(self, key_file='~/.ssh/authorized_keys'):
        self.key_file = os.path.expanduser(key_file)

    def flush_keys(self, auth):
        io = StringIO.StringIO()
        SSH_TEMPLATE = 'command="nappingcat-serve %s",no-port-forwarding,no-X11-forwarding,no-pty,no-agent-forwarding %s\n'
        for user in auth.get_users():
            for key in auth.get_keys(user):
                io.write(SSH_TEMPLATE % (user, key))
        io.seek(0)
        with open(self.key_file, 'w') as keys_file:
            keys_file.write(io.read())

