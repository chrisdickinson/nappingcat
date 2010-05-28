from unittest import TestCase
from nappingcat.response import Response 
from nappingcat.request import Request
from nappingcat.exceptions import NappingCatException
from nappingcat.contrib.git import handlers
from nappingcat.contrib.git import operations
from nappingcat.contrib.git import utils 
from nappingcat.contrib.git.exceptions import KittyGitUnauthorized, KittyGitBadParameter
from tests.gittests.test_utils import fake_settings 
import random
import os
import shutil
import sys
import subprocess
import mox

class TestFork(TestCase):
    def setUp(self):
        self.test_dir = os.path.expanduser('~/.kittygittests')

    def tearDown(self):
        if os.path.isdir(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_unauthorized(self):
        settings_str = """
[kittyconfig]
auth = tests.gittests.test_utils.NoAuth
[kittygit]
        """.strip()

        test_settings = fake_settings(settings_str)
        with open('/dev/null', 'rw') as stream:
            request = Request('random-user-%d' % random.randint(0, 100), 'kitty-git fork', test_settings, (stream, stream, stream))
            self.assertRaises(KittyGitUnauthorized, handlers.fork_repo, request, 'user-dne/random%d' % random.randint(0,100))

    def test_operation_successful(self):
        test_dir = self.test_dir
        settings_str = """
[kittyconfig]
auth = tests.gittests.test_utils.AllAuth
[kittygit]
repo_dir = %s 
        """.strip() % test_dir
        test_settings = fake_settings(settings_str)

        repo_name = 'something-%d' % random.randint(0, 100)
        full_repo_name = 'random-user-%d/%s' % (random.randint(0, 100), repo_name)

        directory = '%s/%s.git' % (test_dir, full_repo_name)
        with open('/dev/null', 'w') as output:
            operations.create_repository('git', output, output, output, directory)

        other_user = 'random-user-%d' % random.randint(0, 100)
        with open('/dev/null', 'w') as out_stream:
            with open('/dev/null', 'w') as err_stream:
                streams = (sys.stdin, out_stream, err_stream)
                request = Request(other_user, 'kitty-git fork', test_settings, streams)
                expected_dir = os.path.expanduser('%s/%s/%s.git' % (test_dir, other_user, repo_name))
                result = handlers.fork_repo(request, full_repo_name)

        self.assertTrue(isinstance(result, Response))
        self.assertTrue(repo_name in result.content['message'])
        self.assertTrue(os.path.isdir(directory))
        self.assertTrue(os.path.isdir(expected_dir))

    def test_operation_failed(self):
        test_dir = self.test_dir
        settings_str = """
[kittyconfig]
auth = tests.gittests.test_utils.AllAuth
[kittygit]
repo_dir = %s 
        """.strip() % test_dir
        test_settings = fake_settings(settings_str)

        repo_name = 'something-%d' % random.randint(0, 100)
        full_repo_name = 'random-user-%d/%s' % (random.randint(0, 100), repo_name)
        directory = '%s/%s.git' % (test_dir, full_repo_name)
        other_user = 'random-user-%d' % random.randint(0, 100)
        with open('/dev/null', 'w') as out_stream:
            with open('/dev/null', 'w') as err_stream:
                streams = (sys.stdin, out_stream, err_stream)
                request = Request(other_user, 'kitty-git fork', test_settings, streams)
                expected_dir = os.path.expanduser('%s/%s/%s.git' % (test_dir, other_user, repo_name))

                self.assertRaises(NappingCatException, handlers.fork_repo, request, full_repo_name)
                self.assertFalse(os.path.isdir(directory))
                self.assertFalse(os.path.isdir(expected_dir))

class TestCreateRepo(TestCase):
    def setUp(self):
        self.test_dir = os.path.expanduser('~/.kittygittests')
        self.mox = mox.Mox()

    def tearDown(self):
        self.mox.UnsetStubs()
        if os.path.isdir(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_no_permission(self):
        settings_str = """
[kittyconfig]
auth = tests.gittests.test_utils.NoAuth
[kittygit]
        """.strip()
        test_settings = fake_settings(settings_str)
        with open('/dev/null', 'w') as out_stream:
            with open('/dev/null', 'w') as err_stream:
                streams = (sys.stdin, out_stream, err_stream)
                request = Request('random-user-%d' % random.randint(0, 100), "kitty-git create-repo 'repo'", test_settings, streams)
                self.assertRaises(KittyGitUnauthorized, handlers.create_repo, request, 'repo-%d' % random.randint(0,10))


    def test_success(self):
        settings_str = """
[kittyconfig]
auth = tests.gittests.test_utils.AllAuth
[kittygit]
repo_dir = %s 
        """.strip() % self.test_dir
        test_settings = fake_settings(settings_str)

        user = 'user-%d' % random.randint(0, 100)
        repo_name = 'repo-%d' % random.randint(0, 100)
        repo = '%s/%s.git' % (user, repo_name)
        with open('/dev/null', 'w') as out_stream:
            with open('/dev/null', 'w') as err_stream:
                streams = (sys.stdin, out_stream, err_stream)
                request = Request(user, "kitty-git create-repo 'repo'", test_settings, streams)
                settings = handlers.get_settings(request)
                full_repo_dir = utils.get_full_repo_dir(settings, user, repo_name) 

                result = handlers.create_repo(request, repo_name)
        self.assertTrue(user in result.content['message'])
        self.assertTrue(repo_name in result.content['message'])
        self.assertTrue(os.path.isdir(full_repo_dir))


    def test_success_with_template_dir(self):
        settings_str = """
[kittyconfig]
auth = tests.gittests.test_utils.AllAuth
[kittygit]
repo_dir = %s 
        """.strip() % self.test_dir
        test_settings = fake_settings(settings_str)

        user = 'user-%d' % random.randint(0, 100)
        repo_name = 'repo-%d' % random.randint(0, 100)
        repo = '%s/%s.git' % (user, repo_name)
        with open('/dev/null', 'w') as out_stream:
            with open('/dev/null', 'w') as err_stream:
                streams = (sys.stdin, out_stream, err_stream)
                request = Request(user, "kitty-git create-repo 'repo'", test_settings, streams)
                settings = handlers.get_settings(request)
                full_repo_dir = utils.get_full_repo_dir(settings, user, repo_name) 

                result = handlers.create_repo(request, repo_name, os.path.join(os.getcwd(), 'tests/support'))
        self.assertTrue(user in result.content['message'])
        self.assertTrue(repo_name in result.content['message'])
        self.assertTrue(os.path.isdir(full_repo_dir))
        self.assertTrue(os.path.isfile('tests/support/hooks/post-commit'))
        import time; time.sleep(1)      # pass the time for a bit for things to 
                                        # flush to disk
        self.assertTrue(os.path.isfile('%s/hooks/post-commit' % full_repo_dir))

    def test_fail(self):
        settings_str = """
[kittyconfig]
auth = tests.gittests.test_utils.AllAuth
[kittygit]
repo_dir = %s 
        """.strip() % self.test_dir
        test_settings = fake_settings(settings_str)

        user = 'user-%d' % random.randint(0, 100)
        repo_name = 'repo-%d' % random.randint(0, 100)
        repo = '%s/%s.git' % (user, repo_name)
        streams = (sys.stdin, sys.stdout, sys.stderr)
        request = Request(user, "kitty-git create-repo 'repo'", test_settings, streams)
        settings = handlers.get_settings(request)
        full_repo_dir = utils.get_full_repo_dir(settings, user, repo_name) 

        self.mox.StubOutWithMock(subprocess, 'call')
        subprocess.call(
            args=['git','--git-dir=.', 'init', '--bare'],
            cwd=full_repo_dir,
            stdout=sys.stderr,
            close_fds=True
        ).AndReturn(random.randint(1,100))   

        self.assertRaises(NappingCatException, handlers.create_repo, request, repo_name) 

class TestHandleGit(TestCase):
    def setUp(self):
        self.test_dir = os.path.expanduser('~/.kittygittests')
        self.mox = mox.Mox()

    def tearDown(self):
        self.mox.UnsetStubs()
        if os.path.isdir(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_no_permission(self):
        settings_str = """
[kittyconfig]
auth = tests.gittests.test_utils.NoAuth
[kittygit]
        """.strip()
        test_settings = fake_settings(settings_str)

        repo = 'blah/%d.git' % random.randint(0, 100)
        variants = (
            ("git-upload-pack '%s'", "-upload-pack "),
            ("git upload-pack '%s'", " upload-pack "),
            ("git-receive-pack '%s'", "-receive-pack "),
            ("git receive-pack '%s'", " receive-pack "),
        )

        streams = (sys.stdin, sys.stdout, sys.stderr)
        for cmd, action in variants:
            request = Request('random-user-%d' % random.randint(0, 100), cmd % repo, test_settings, streams)
            self.assertRaises(KittyGitUnauthorized, handlers.handle_git, request, action) 

    def test_bad_repo_raises_bad_parameter(self):
        settings_str = """
[kittyconfig]
auth = tests.gittests.test_utils.AllAuth
[kittygit]
repo_dir = %s 
        """.strip() % self.test_dir
        test_settings = fake_settings(settings_str)
        repo = 'blah/%d.git' % random.randint(0, 100)
        variants = (
            ("git-upload-pack '%s'", "-upload-pack "),
            ("git upload-pack '%s'", " upload-pack "),
            ("git-receive-pack '%s'", "-receive-pack "),
            ("git receive-pack '%s'", " receive-pack "),
        )

        streams = (sys.stdin, sys.stdout, sys.stderr)
        for cmd, action in variants:
            request = Request('random-user-%d' % random.randint(0, 100), cmd % repo, test_settings, streams)
            self.assertRaises(KittyGitBadParameter, handlers.handle_git, request, action) 

    def test_successful(self):
        settings_str = """
[kittyconfig]
auth = tests.gittests.test_utils.AllAuth
[kittygit]
repo_dir = %s 
        """.strip() % self.test_dir
        test_settings = fake_settings(settings_str)
        user = 'random-user-%d' % random.randint(0, 100)
        repo_name = str(random.randint(0,100))
        repo = '%s/%s.git' % (user, repo_name)
        variants = (
            ("git-upload-pack '%s'", "-upload-pack "),
            ("git upload-pack '%s'", " upload-pack "),
            ("git-receive-pack '%s'", "-receive-pack "),
            ("git receive-pack '%s'", " receive-pack "),
        )

        streams = (sys.stdin, sys.stdout, sys.stderr)
        for cmd, action in variants:
            request = Request(user, cmd % repo, test_settings, streams)
            path = utils.get_full_repo_dir(handlers.get_settings(request), user, repo_name)
            with open('/dev/null', 'w') as output:
                operations.create_repository('git', output, output, output, path, bare=True)
            self.mox.StubOutWithMock(subprocess, 'call')
            subprocess.call(
                args=['git', 'shell', '-c', ' '.join(['git%s'%action.strip(), "'%s'"%path])],
                cwd=path,
                stdout=sys.stdout,
                stderr=sys.stderr,
                stdin=sys.stdin,
            ).AndReturn(0)
            self.mox.ReplayAll()
            result = handlers.handle_git(request, action)

            self.assertTrue(isinstance(result, Response))
            self.assertTrue(user in str(result))
            self.assertTrue(repo_name in str(result))
            self.mox.UnsetStubs()
            shutil.rmtree(path)

    def test_unsuccessful(self):
        settings_str = """
[kittyconfig]
auth = tests.gittests.test_utils.AllAuth
[kittygit]
repo_dir = %s 
        """.strip() % self.test_dir
        test_settings = fake_settings(settings_str)
        user = 'random-user-%d' % random.randint(0, 100)
        repo_name = str(random.randint(0,100))
        repo = '%s/%s.git' % (user, repo_name)
        variants = (
            ("git-upload-pack '%s'", "-upload-pack "),
            ("git upload-pack '%s'", " upload-pack "),
            ("git-receive-pack '%s'", "-receive-pack "),
            ("git receive-pack '%s'", " receive-pack "),
        )

        streams = (sys.stdin, sys.stdout, sys.stderr)
        for cmd, action in variants:
            request = Request(user, cmd % repo, test_settings, streams)
            path = utils.get_full_repo_dir(handlers.get_settings(request), user, repo_name)
            with open('/dev/null', 'w') as output:
                operations.create_repository('git', output, output, output, path, bare=True)
            self.mox.StubOutWithMock(subprocess, 'call')
            subprocess.call(
                args=['git', 'shell', '-c', ' '.join(['git%s'%action.strip(), "'%s'"%path])],
                cwd=path,
                stdout=sys.stdout,
                stderr=sys.stderr,
                stdin=sys.stdin,
            ).AndReturn(random.randint(1,100))
            self.mox.ReplayAll()
            self.assertRaises(NappingCatException, handlers.handle_git, request, action)
            self.mox.UnsetStubs()
            shutil.rmtree(path)
