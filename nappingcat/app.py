import os
import sys
from nappingcat.exceptions import NappingCatUnhandled, NappingCatException

class App(object):
    def __init__(self, *args, **kwargs):
        super(App, self).__init__(*args, **kwargs)

    @classmethod
    def run(cls, *args, **kwargs):
        user = sys.argv[1]
        original_command = os.environ.get('SSH_ORIGINAL_COMMAND') 
        try:
            results = cls().main(user=user, original_command=original_command)
            print >>sys.stderr, "\033[0;32m%s\033[0m" % results
        except NappingCatException, e:
            print >>sys.stderr, "\033[1;31m%s\033[0m" % e 

    def main(self, *args, **kwargs):
        raise NappingCatUnhandled("""
            You woke up the kitten!
        """.strip())
