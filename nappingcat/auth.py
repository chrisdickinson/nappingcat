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

def get_auth_backend_from_settings(settings):
    settings_dict = dict(settings.items(config.SECTION_NAME))
    module, target = settings_dict['auth'].rsplit('.',1)
    module = import_module(module)
    target = getattr(module,target)
    return target(settings)
