from nappingcat.auth import AuthBackend
import ConfigParser
import StringIO

def auth_backend_factory(default_permission):
    class Auth(AuthBackend):
        def has_permission(self, user, permission):
            return default_permission
        def add_permission(self, user, permission):
            return default_permission
        def remove_permission(self, user, permission):
            return default_permission
    return Auth

NoAuth = auth_backend_factory(default_permission=False)
AllAuth = auth_backend_factory(default_permission=True)

def fake_settings(string):
    config = ConfigParser.ConfigParser()
    config.readfp(StringIO.StringIO(string)) 
    return config
