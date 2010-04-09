from unittest import TestCase
from nappingcat import app
from nappingcat.exceptions import NappingCatException, NappingCatUnhandled
import StringIO
import random
import sys

class TestOfApp(TestCase):
    def test_main_raises_unhandled(self):
        self.assertRaises(NappingCatUnhandled, app.App().main)

    def test_run_outputs_green_on_success(self):
        stream = StringIO.StringIO()
        random_test = 'rand-%d' % random.randint(1,100)
        class SubApp(app.App):
            def output(self, color, what, to_stream=None):
                super(SubApp, self).output(color, what, stream) 
            def main(*args, **kwargs):
                return random_test
        sys.argv = [random.randint(1,100), random.randint(1,100)]
        SubApp.run()
        stream.seek(0)
        results = stream.read()
        self.assertTrue(random_test in results)
        self.assertTrue(str(app.COLOR_GREEN) in results)

    def test_run_outputs_red_on_failure(self):
        stream = StringIO.StringIO()
        random_test = 'rand-%d' % random.randint(1,100)
        class SubApp(app.App):
            def output(self, color, what, to_stream=None):
                super(SubApp, self).output(color, what, stream) 
            def main(*args, **kwargs):
                raise NappingCatException(random_test)
        sys.argv = [random.randint(1,100), random.randint(1,100)]
        SubApp.run()
        stream.seek(0)
        results = stream.read()
        self.assertTrue(random_test in results)
        self.assertTrue(str(app.COLOR_RED) in results)

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
