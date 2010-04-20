from unittest import TestCase
from nappingcat import app, exceptions
from nappingcat.exceptions import NappingCatException, NappingCatUnhandled
import StringIO
import os
import random
import sys

class TestOfApp(TestCase):
    # TODO: refactor these three methods into a common super-class
    def setUp(self):
        self.original_os_environ = os.environ
        self.original_sys_argv = sys.argv

        # minimum required for tests to run
        sys.argv = ["foo", "foobar-user"]

    def tearDown(self):
        os.environ = self.original_os_environ
        sys.argv = self.original_sys_argv

