from unittest import TestCase
from nappingcat import auth
from nappingcat import request
import ConfigParser
import StringIO
import random

class StubbedAuthTest(auth.AuthBackend):
    pass

class TriggeredAuthTest(auth.AuthBackend):
    def __getattribute__(self, what):
        return lambda *args, **kwargs : "triggered %s" % what 

class TestOfGetAuthBackendFromSettings(TestCase):
    def test_loads_auth_from_settings(self):
        settings_str = """
[kittyconfig]
auth=tests.auth.StubbedAuthTest
        """.strip()
        config = ConfigParser.ConfigParser()
        config.readfp(StringIO.StringIO(settings_str))
        results = auth.get_auth_backend_from_settings(config)
        self.assertTrue(isinstance(results, StubbedAuthTest))
        self.assertTrue(isinstance(results.settings, ConfigParser.ConfigParser))

class TestPermissionDelegation(TestCase):
    def setUp(self):
        settings_str = """
[kittyconfig]
auth=tests.auth.TriggeredAuthTest
        """.strip()
        config = ConfigParser.ConfigParser()
        config.readfp(StringIO.StringIO(settings_str))

        streams = (StringIO.StringIO(), StringIO.StringIO(), StringIO.StringIO())
        self.request = request.Request(user='random%d'%random.randint(1,100), command="random%d"%random.randint(1,100), settings=config, streams=streams)

    def test_has_permission_delegates_to_backend(self):
        permission = random.randint(1,100)
        self.assertEqual(auth.has_permission(self.request.settings, self.request.user, permission), "triggered has_permission") 

    def test_add_permission_delegates_to_backend(self):
        permission = random.randint(1,100)
        self.assertEqual(auth.add_permission(self.request.settings, self.request.user, permission), "triggered add_permission") 

    def test_remove_permission_delegates_to_backend(self):
        permission = random.randint(1,100)
        self.assertEqual(auth.remove_permission(self.request.settings, self.request.user, permission), "triggered remove_permission")

    def test_add_user_delegates_to_backend(self):
        self.assertEqual(auth.add_user(self.request.settings, self.request.user), "triggered add_user")

    def test_add_key_to_user_delegates_to_backend(self):
        username = str(random.randint(1,100))
        key = str(random.randint(1,100))
        self.assertEqual(auth.add_key_to_user(self.request.settings, username, key), "triggered add_key_to_user")
