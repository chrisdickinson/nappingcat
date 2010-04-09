import os
import sys
from nappingcat.exceptions import NappingCatUnhandled, NappingCatException

COLOR_RED = 31
COLOR_GREEN = 32

class App(object):
    def output(self, color, what, to_stream=sys.stderr):
        output = "\033[0;%dm%s\033[0m" % (color, what)
        print >>to_stream, output 

    @classmethod
    def run(cls, *args, **kwargs):
        user = sys.argv[1]
        original_command = os.environ.get('SSH_ORIGINAL_COMMAND') 
        try:
            instance = cls()
            results = instance.main(user=user, original_command=original_command)
            instance.output(COLOR_GREEN, results)
        except NappingCatException, e:
            instance.output(COLOR_RED, str(e))

    def main(self, *args, **kwargs):
        raise NappingCatUnhandled("""
            You woke up the kitten!
        """.strip())
