from nappingcat.exceptions import NappingCatUnhandled, NappingCatException
from nappingcat import exceptions, logs, config
from nappingcat.util import import_module, import_class_from_module
import os
import sys

class App(object):
    def __init__(self, environ=None, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr):
        if environ is None:
            environ = {}
            environ.update(os.environ)
            environ['argv'] = sys.argv[1:]
        self.environ = environ
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr

    def setup_environ(self):
        settings = config.build_settings()        
        if not settings.has_section(config.SECTION_NAME):
            raise exceptions.NappingCatBadConfig("""
                Your nappingcat.conf file does not include a %s section!
            """.strip() % config.SECTION_NAME)

        kitty_config = dict(settings.items(config.SECTION_NAME))
        if kitty_config.get('paths', None) is not None:
            sys.path[0:0] = [i for i in kitty_config['paths'].split('\n') if i]


        logger_class = import_class_from_module(kitty_config['logger']) if 'logger' in kitty_config else logs.ColorLogger
        self.global_settings = settings
        self.nappingcat_settings = kitty_config
        self.logger = logger_class(self.stderr)

    @classmethod
    def run(cls, *args, **kwargs):
        instance = cls()
        instance.setup_environ()
        try:
            results = instance.main()
            instance.logger.good(results)
        except NappingCatException, e:
            instance.logger.bad(str(e))

    def main(self, *args, **kwargs):
        raise NappingCatUnhandled("""
            You woke up the kitten!
        """.strip())
