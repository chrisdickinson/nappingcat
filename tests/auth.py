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
