from unittest import TestCase
from nappingcat import app
from nappingcat.exceptions import NappingCatException, NappingCatUnhandled
import StringIO
import os
import random
import sys
import fudge

class TestOfApp(TestCase):
    # TODO: refactor these three methods into a common super-class
    def setUp(self):
        fudge.clear_expectations()
        self.patched_apis = []
        self.original_os_environ = os.environ
        self.original_sys_argv = sys.argv

    def tearDown(self):
        fudge.verify()
        for patched in self.patched_apis:
            patched.restore()
        os.environ = self.original_os_environ
        sys.argv = self.original_sys_argv

    def patch(self, *args, **kwargs):
        self.patched_apis.append(fudge.patch_object(*args, **kwargs))

    def test_calls_main_on_provided_instance(self):
        random_user = 'user-%d' % random.randint(100, 200)
        sys.argv = ['_ignored', random_user]
        random_ssh_command = 'execute %d' % random.randint(100, 200)
        os.environ['SSH_ORIGINAL_COMMAND'] = random_ssh_command

        fake_instance = fudge.Fake()
        fake_instance.expects('main').with_args(
            user=random_user,
            original_command=random_ssh_command
        )
        fake_instance.logger = fudge.Fake().provides('good')
        fudge.clear_calls()

        app.App.run(instance=fake_instance)

    def test_main_raises_unhandled(self):
        self.assertRaises(NappingCatUnhandled, app.App().main)

    def test_run_calls_good_on_sucess(self):
        random_test = 'rand-%d' % random.randint(1,100)

        fake_instance = fudge.Fake()
        fake_instance.provides('main').returns(random_test)
        fake_instance.logger = fudge.Fake()
        fake_instance.logger.expects('good').with_args(random_test)
        fudge.clear_calls()

        # TODO: document what these are? [command, user]?
        sys.argv = [random.randint(1,100), random.randint(1,100)]

        app.App.run(instance=fake_instance)

    def test_run_calls_bad_on_failure(self):
        random_test = 'rand-%d' % random.randint(1,100)

        fake_instance = fudge.Fake()
        fake_instance.provides('main').raises(NappingCatException(random_test))
        fake_instance.logger = fudge.Fake()
        fake_instance.logger.expects('bad').with_args(random_test)
        fudge.clear_calls()

        # TODO: document what these are? [command, user]?
        sys.argv = [random.randint(1,100), random.randint(1,100)]

        app.App.run(instance=fake_instance)

    def test_run_delegates_to_app_instance_main(self):
        random_test = 'rand-%d' % random.randint(1,100)

        # TODO: document what these are? [command, user]?
        # TODO: move duplication into helper method with intent revealing name
        sys.argv = [random.randint(1,100), random.randint(1,100)]

        fake_main = fudge.Fake('app.App.main', expect_call=True)
        self.patch(app.App, 'main', fake_main)

        # make sure this stays quiet
        fake_good = fudge.Fake('app.logs.ColorLogger.good', expect_call=True)
        self.patch(app.logs.ColorLogger, 'good', fake_good)

        fudge.clear_calls()

        app.App.run()

    def test_run_passed_original_command_and_user_from_argv(self):
        random_ssh_cmd = "rand-%d" % random.randint(1,100)
        random_user = 'user-%d' % random.randint(1,100)

        # TODO: this should be something that can be passed into the app
        #       rather than requiring a patch of the os.environ global
        os.environ['SSH_ORIGINAL_COMMAND'] = random_ssh_cmd
        sys.argv = ['anything', random_user]

        fake_main = fudge.Fake(
            'app.App.main',
            expect_call=True
        ).with_args(
            user=random_user,
            original_command=random_ssh_cmd
        )
        self.patch(app.App, 'main', fake_main)
        fudge.clear_calls()

        original_logger = app.App.logger
        app.App.logger = fudge.Fake().provides('good')
        app.App.run()

        app.App.logger = original_logger
