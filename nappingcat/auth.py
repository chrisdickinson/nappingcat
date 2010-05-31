from nappingcat.util import import_module
from nappingcat import config

class AuthBackend(object):
    def __init__(self, settings):
        self.users = {}
        self.settings = settings
        self.require_update = False

    def has_permission(self, user, permission):
        full_query = (user,) + tuple(permission)
        result = self.users
        for i in full_query:
            result = result.get(i, {})
        return bool(result)

    def add_permission(self, user, permission):
        self.require_update = True
        full_query = (user,) + tuple(permission)
        result = self.users
        for i in full_query[:-1]:
            level = result.get(i, None)
            if level is None:
                result[i] = {}
            result = result[i]
        result[full_query[-1]] = True

    def remove_permission(self, user, permission):
        self.require_update = True
        full_query = (user,) + tuple(permission)
        result = self.users
        for i in full_query[:-1]:
            level = result.get(i, None)
            if level is None:
                result[i] = {}
            result = result[i]
        del result[full_query[-1]]

    def add_user(self, username):
        self.require_update = True
        self.users[username] = {'keys':[]}

    def add_key_to_user(self, user, key):
        self.require_update = True
        self.users[user]['keys'].append(key)

    def get_keys(self, username):
        return self.users[username]['keys']

    def finish(self, pubkey_handler):
        if self.require_update:
            pubkey_handler.flush_keys(self)

    def get_users(self):
        return self.users.keys()

def get_auth_backend_from_settings(settings):
    settings_dict = dict(settings.items(config.SECTION_NAME))
    module, target = settings_dict['auth'].rsplit('.',1)
    module = import_module(module)
    target = getattr(module,target)
    return target(settings)
