from unittest import TestCase
from nappingcat.contrib.git import utils
import socket
import random
import mox
import os
class TestGetFullRepoDir(TestCase):
    def test_safe_default(self):
        settings = {}
        user = 'user-%d' % random.randint(1,100) 
        repo = 'repo-%d' % random.randint(1,100) 
        results = utils.get_full_repo_dir(settings, user, repo)
        self.assertEqual(os.path.expanduser('~/repos/%s/%s.git' % (user, repo)), results)

    def test_takes_user_dir(self):
        random_dir = 'rand%d' % random.randint(1,100)
        settings = {
            'repo_dir':random_dir
        }
        user = 'user-%d' % random.randint(1,100) 
        repo = 'repo-%d' % random.randint(1,100) 
        results = utils.get_full_repo_dir(settings, user, repo)
        self.assertEqual('%s/%s/%s.git' % (random_dir, user, repo), results)

class TestGetCloneBaseURL(TestCase):
    def test_use_defaults(self):
        settings = {
            'user':'user-%d' % random.randint(1,100),
            'host':'host-%d' % random.randint(1,100),
        }
        results = utils.get_clone_base_url(settings)
        self.assertEqual('%s@%s' % (settings['user'], settings['host']), results)

    def test_use_hostname(self):
        settings = {
            'user':'user-%d' % random.randint(1,100),
        }

        results = utils.get_clone_base_url(settings)
        self.assertEqual('%s@%s.local' % (settings['user'], socket.gethostname()), results)

    def test_uses_getlogin(self):
        settings = {
            'host':'host-%d' % random.randint(1,100),
        }
        _mox = mox.Mox()
        _mox.StubOutWithMock(os, 'getlogin')
        random_user = 'rand-%d' % random.randint(1,100)
        os.getlogin().AndReturn(random_user)
        _mox.ReplayAll()
        results = utils.get_clone_base_url(settings)
        self.assertEqual('%s@%s' % (random_user, settings['host']), results)
        _mox.UnsetStubs()

    def test_getlogin_fails(self):
        settings = {
            'host':'host-%d' % random.randint(1,100),
        }
        _mox = mox.Mox()
        _mox.StubOutWithMock(os, 'getlogin')
        random_user = 'rand-%d' % random.randint(1,100)
        os.getlogin().AndRaise(OSError)
        _mox.ReplayAll()
        results = utils.get_clone_base_url(settings)
        self.assertEqual('%s@%s' % (utils.DEFAULT_USER_NAME, settings['host']), results)
        _mox.UnsetStubs()
