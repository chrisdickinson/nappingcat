from unittest import TestCase
from nappingcat import app, exceptions
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
        self.original_os_environ = os.environ
        self.original_sys_argv = sys.argv

        # minimum required for tests to run
        sys.argv = ["foo", "foobar-user"]

    def tearDown(self):
        fudge.verify()
        os.environ = self.original_os_environ
        sys.argv = self.original_sys_argv

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

        fake_instance = fudge.Fake()
        fake_instance.expects('main')
        # make sure this stays quiet
        fake_instance.logger = fudge.Fake().provides('good')
        fudge.clear_calls()

        app.App.run(instance=fake_instance)

    def test_run_passed_original_command_and_user_from_argv(self):
        random_ssh_cmd = "rand-%d" % random.randint(1,100)
        random_user = 'user-%d' % random.randint(1,100)

        # TODO: this should be something that can be passed into the app
        #       rather than requiring a patch of the os.environ global
        os.environ['SSH_ORIGINAL_COMMAND'] = random_ssh_cmd
        sys.argv = ['anything', random_user]

        fake_instance = fudge.Fake()
        fake_instance.expects('main').with_args(
            user=random_user,
            original_command=random_ssh_cmd
        )
        fake_instance.logger = fudge.Fake().provides('good')
        fudge.clear_calls()

        app.App.run(instance=fake_instance)

    def test_calling_run_without_an_instance_causes_it_to_instantiate_itself(self):
        class TestableSubApp(app.App):
            logger = fudge.Fake().provides('good')
            pass

        fake = fudge.Fake('TestableSubApp.main', expect_call=True).returns('foobar')
        patched_api = fudge.patch_object(TestableSubApp, 'main', fake)

        fudge.clear_calls()

        TestableSubApp.run()

    def test_runs_with_empty_sys_argv(self):
        sys.argv = []

        fake_instance = fudge.Fake()
        fake_instance.provides('main')
        fake_instance.logger = fudge.Fake().provides('good')
        fudge.clear_calls()

        try:
            app.App.run(instance=fake_instance)
        except exceptions.NoUserException:
            pass
