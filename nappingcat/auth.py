from nappingcat.util import import_module
from nappingcat import config

class AuthBackend(object):
    def __init__(self, settings):
        self.settings = settings

    def has_permission(self, user, permission):
        pass

    def add_permission(self, user, permission):
        pass

    def remove_permission(self, user, permission):
        pass

def get_auth_backend_from_settings(settings):
    settings_dict = dict(settings.items(config.SECTION_NAME))
    module, target = settings_dict['auth'].rsplit('.',1)
    module = import_module(module)
    target = getattr(module,target)
    return target(settings)

def has_permission(request, permission):
    backend = get_auth_backend_from_settings(request.settings)
    return backend.has_permission(request.user, permission)

def add_permission(request, permission):
    backend = get_auth_backend_from_settings(request.settings)
    return backend.add_permission(request.user, permission)

def remove_permission(request, permission):
    backend = get_auth_backend_from_settings(request.settings)
    return backend.remove_permission(request.user, permission)
