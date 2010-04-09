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
        self.request = request.Request(user='random%d'%random.randint(1,100), command="random%d"%random.randint(1,100), settings=config)

    def test_has_permission_delegates_to_backend(self):
        permission = random.randint(1,100)
        self.assertEqual(auth.has_permission(self.request, permission), "triggered has_permission") 

    def test_add_permission_delegates_to_backend(self):
        permission = random.randint(1,100)
        self.assertEqual(auth.add_permission(self.request, permission), "triggered add_permission") 

    def test_remove_permission_delegates_to_backend(self):
        permission = random.randint(1,100)
        self.assertEqual(auth.remove_permission(self.request, permission), "triggered remove_permission") 
