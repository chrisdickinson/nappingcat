import os
import sys
from nappingcat.exceptions import NappingCatUnhandled

class App(object):
    def __init__(self, *args, **kwargs):
        super(App, self).__init__(*args, **kwargs)

    @classmethod
    def run(cls, *args, **kwargs):
        user = sys.argv[1]
        original_command = os.environ.get('SSH_ORIGINAL_COMMAND') 
        return cls().main(user=user, original_command=original_command)

    def main(self, *args, **kwargs):
        raise NappingCatUnhandled("""
            You woke up the kitten!
        """.strip())
