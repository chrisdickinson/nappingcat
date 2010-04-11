from unittest import TestCase
from nappingcat import app
from nappingcat.exceptions import NappingCatException, NappingCatUnhandled
import StringIO
import random
import sys
import fudge

class TestOfApp(TestCase):
    # TODO: refactor these three methods into a common super-class
    def setUp(self):
        fudge.clear_expectations()
        self.patched_apis = []

    def tearDown(self):
        fudge.verify()
        for patched in self.patched_apis:
            patched.restore()

    def patch(self, *args, **kwargs):
        self.patched_apis.append(fudge.patch_object(*args, **kwargs))

    def test_main_raises_unhandled(self):
        self.assertRaises(NappingCatUnhandled, app.App().main)

    def test_run_calls_good_on_sucess(self):
        random_test = 'rand-%d' % random.randint(1,100)

        fake_good = fudge.Fake('app.logs.ColorLogger.good', expect_call=True).with_args(random_test)
        self.patch(app.logs.ColorLogger, 'good', fake_good)
        fudge.clear_calls()

        class SubApp(app.App):
            def main(*args, **kwargs):
                return random_test

        # TODO: document what these are? [command, user]?
        sys.argv = [random.randint(1,100), random.randint(1,100)]
        SubApp.run()

    def test_run_calls_bad_on_failure(self):
        random_test = 'rand-%d' % random.randint(1,100)

        fake_bad = fudge.Fake('app.logs.ColorLogger.bad', expect_call=True).with_args(random_test)
        self.patch(app.logs.ColorLogger, 'bad', fake_bad)

        class SubApp(app.App):
            def main(*args, **kwargs):
                raise NappingCatException(random_test)

        # TODO: document what these are? [command, user]?
        sys.argv = [random.randint(1,100), random.randint(1,100)]
        SubApp.run()

    def test_run_delegates_to_app_instance_main(self):
        random_test = 'rand-%d' % random.randint(1,100)
        triggers = {}
        class SubApp(app.App):
            def main(*args, **kwargs):
                triggers['passed_to_main'] = True
        sys.argv = [random.randint(1,100), random.randint(1,100)]
        SubApp.run()
        self.assertTrue(triggers['passed_to_main'])

    def test_run_passed_original_command_and_user_from_argv(self):
        import os
        random_ssh_cmd = "rand-%d" % random.randint(1,100)
        random_user = 'user-%d' % random.randint(1,100)
        os.environ['SSH_ORIGINAL_COMMAND'] = random_ssh_cmd
        sys.argv = ['anything', random_user]

        class SubApp(app.App):
            def main(*args, **kwargs):
                self.assertEqual(kwargs['user'], random_user)
                self.assertEqual(kwargs['original_command'], random_ssh_cmd)
        SubApp.run()
