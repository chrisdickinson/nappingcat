import os
import sys
from nappingcat.exceptions import NappingCatUnhandled, NappingCatException
from nappingcat import logs

class App(object):
    logger = logs.ColorLogger()
    def __init__(self, logger=None):
        if logger:
            self.logger = logger

    @classmethod
    def run(cls, instance=None, *args, **kwargs):
        user = sys.argv[1]
        original_command = os.environ.get('SSH_ORIGINAL_COMMAND') 
        try:
            if not instance:
                instance = cls()
            results = instance.main(user=user, original_command=original_command)
            instance.logger.good(results)
        except NappingCatException, e:
            instance.logger.bad(str(e))

    def main(self, *args, **kwargs):
        raise NappingCatUnhandled("""
            You woke up the kitten!
        """.strip())
