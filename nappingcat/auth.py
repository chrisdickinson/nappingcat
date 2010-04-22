from nappingcat.util import import_module
from nappingcat import config
import StringIO
class AuthBackend(object):
    def __init__(self, settings):
        self.settings = settings

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

    def flush(self, request, target):
        users = self.get_users()
        io = StringIO.StringIO()
        format = 'command="nappingcat-serve %s",no-port-forwarding,no-X11-forwarding,no-pty,no-agent-forwarding %s\n'
        [[io.write(format % (user, key)) for key in self.get_keys(user) if key.strip()] for user in users]
        io.seek(0)
        target.write(io.read())

def get_auth_backend_from_settings(settings):
    settings_dict = dict(settings.items(config.SECTION_NAME))
    module, target = settings_dict['auth'].rsplit('.',1)
    module = import_module(module)
    target = getattr(module,target)
    return target(settings)

def has_permission(request, username, permission):
    backend = get_auth_backend_from_settings(request.settings)
    return backend.has_permission(username, permission)

def add_permission(request, username, permission):
    backend = get_auth_backend_from_settings(request.settings)
    return backend.add_permission(username, permission)

def remove_permission(request, username, permission):
    backend = get_auth_backend_from_settings(request.settings)
    return backend.remove_permission(username, permission)

def add_user(request, username):
    backend = get_auth_backend_from_settings(request.settings)
    return backend.add_user(username)

def add_key_to_user(request, username, key, flush=True, target=None):
    backend = get_auth_backend_from_settings(request.settings)
    result = backend.add_key_to_user(username, key)
    if flush:
        backend.flush(request, target)
    return result
