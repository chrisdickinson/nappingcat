from unittest import TestCase
from nappingcat.contrib.auth import handlers
from nappingcat import request
from nappingcat.exceptions import NappingCatRejected
from nappingcat import auth
import ConfigParser
import StringIO
import random
import os

class SimpleAuth(auth.AuthBackend):
    user_dict = {}
    def has_permission(self, username, permission):
        return bool(SimpleAuth.user_dict.get(username, {}).get(handlers.PERMISSION_SEP.join(permission), False)) 

    def add_permission(self, username, permission):
        SimpleAuth.user_dict.get(username, {})[handlers.PERMISSION_SEP.join(permission)] = True

    def remove_permission(self, username, permission):
        del SimpleAuth.user_dict.get(username, {})[handlers.PERMISSION_SEP.join(permission)]

    def add_user(self, username):
        SimpleAuth.user_dict[username] = SimpleAuth.user_dict[username] if SimpleAuth.user_dict.get(username, None) is not None else {'keys':[]}

    def add_key_to_user(self, username, key):
        SimpleAuth.user_dict[username]['keys'].append(key)

    def get_keys(self, username):
        return SimpleAuth.user_dict[username]['keys']

    def get_users(self):
        return SimpleAuth.user_dict.keys()

class TestContribAuthHandlers(TestCase):
    def setUp(self):
        settings_str = """                                                                                                               
[kittyconfig]                                                                                                                            
auth=tests.contribauth.SimpleAuth
authorized_keys=.test_authorized_keys
        """.strip()                                                                                                                      
        config = ConfigParser.ConfigParser()                                                                                             
        config.readfp(StringIO.StringIO(settings_str)) 

        self.random_key = "ssh-rsa BALSHFASHDFAKSDFLKASJDFKLASDJFLKASDJFKLSDJ%dASLKDJFAKSLDJF%d" % (random.randint(1,100), random.randint(1,100))
        self.stdout = StringIO.StringIO()
        self.stdin = StringIO.StringIO(self.random_key)
        self.stderr = StringIO.StringIO()
        self.user = 'rand-%d' % random.randint(1,100)
        self.command = 'random-cmd-%d' % random.randint(1,100)
        self.settings = config 
        self.request = request.Request(
            user=self.user,
            command=self.command,
            settings=self.settings,
            streams=(self.stdin, self.stdout, self.stderr),
        )

    def tearDown(self):
        SimpleAuth.user_dict = {}
        if os.path.isfile('.test_authorized_keys'):
            os.unlink('.test_authorized_keys')

    def test_add_user_adds_a_user(self):
        auth.add_user(self.request, self.user)
        auth.add_permission(self.request, self.user, ('auth', 'adduser'))
        random_user = 'new-user-%d' % random.randint(1,100)
        handlers.add_user(self.request, random_user)
        self.assertTrue(random_user in SimpleAuth.user_dict)

    def test_unauth_add_user(self):
        random_user = 'new-user-%d' % random.randint(1,100)
        self.assertRaises(NappingCatRejected, handlers.add_user, self.request, random_user)

    def test_add_key_to_user_affects_authorized_keys(self):
        auth.add_user(self.request, self.user)
        auth.add_permission(self.request, self.user, ('auth', 'modifyuser'))
        random_user = 'new-user-%d' % random.randint(1,100)
        auth.add_user(self.request, random_user)
        handlers.add_key_to_user(self.request, random_user)

        self.assertTrue(self.random_key in SimpleAuth.user_dict[random_user]['keys'])

        with open('.test_authorized_keys', 'r') as authorized_keys:
            output = authorized_keys.read()

        self.assertTrue(self.random_key in output)
        self.assertTrue(random_user in output)
        self.assertTrue('nappingcat-serve' in output)

    def test_unauth_add_key_to_user(self):
        auth.add_user(self.request, self.user)
        random_user = 'new-user-%d' % random.randint(1,100)
        auth.add_user(self.request, random_user)
        self.assertRaises(NappingCatRejected, handlers.add_key_to_user, self.request, random_user)

    def test_add_permission_actually_adds_permission(self):
        auth.add_user(self.request, self.user)
        auth.add_permission(self.request, self.user, ('auth', 'modifyuser'))
        random_user = 'new-user-%d' % random.randint(1,100)
        auth.add_user(self.request, random_user)
        random_perm = (str(random.randint(1,100)), str(random.randint(1,100))) * random.randint(1,10)
        handlers.add_permission(self.request, random_user, handlers.PERMISSION_SEP.join(random_perm))
        self.assertTrue(auth.has_permission(self.request, random_user, random_perm))

    def test_unauth_add_permission(self):
        auth.add_user(self.request, self.user)
        random_user = 'new-user-%d' % random.randint(1,100)
        auth.add_user(self.request, random_user)
        random_perm = (str(random.randint(1,100)), str(random.randint(1,100))) * random.randint(1,10)
        self.assertRaises(NappingCatRejected, handlers.add_permission, self.request, random_user, handlers.PERMISSION_SEP.join(random_perm))

    def test_remove_permission_actually_removes_permission(self):
        auth.add_user(self.request, self.user)
        auth.add_permission(self.request, self.user, ('auth', 'modifyuser'))
        random_user = 'new-user-%d' % random.randint(1,100)
        auth.add_user(self.request, random_user)
        random_perm = (str(random.randint(1,100)), str(random.randint(1,100))) * random.randint(1,10)
        handlers.add_permission(self.request, random_user, handlers.PERMISSION_SEP.join(random_perm))
        self.assertTrue(auth.has_permission(self.request, random_user, random_perm))
        handlers.remove_permission(self.request, random_user, handlers.PERMISSION_SEP.join(random_perm))
        self.assertFalse(auth.has_permission(self.request, random_user, random_perm))

    def test_unauth_remove_permission(self):
        auth.add_user(self.request, self.user)
        auth.add_permission(self.request, self.user, ('auth', 'modifyuser'))
        random_user = 'new-user-%d' % random.randint(1,100)
        auth.add_user(self.request, random_user)
        random_perm = (str(random.randint(1,100)), str(random.randint(1,100))) * random.randint(1,10)
        handlers.add_permission(self.request, random_user, handlers.PERMISSION_SEP.join(random_perm))
        self.assertTrue(auth.has_permission(self.request, random_user, random_perm))
        auth.remove_permission(self.request, self.user, ('auth', 'modifyuser'))
        self.assertRaises(NappingCatRejected, handlers.remove_permission, self.request, random_user, handlers.PERMISSION_SEP.join(random_perm))
