from unittest import TestCase
from nappingcat import request
import random

class TestOfRequest(TestCase):
    def test_init(self):
        random_user = random.randint(1,100)
        random_command = random.randint(1,100)
        random_settings = random.randint(1,100)
        req = request.Request(random_user, random_command, random_settings) 
        self.assertEqual(req.user, random_user)
        self.assertEqual(req.command, random_command)
        self.assertEqual(req.settings, random_settings)
