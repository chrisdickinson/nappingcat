from nappingcat import config
from nappingcat.app import App
from nappingcat.patterns import patterns, include
from nappingcat.util import import_module
from nappingcat.request import Request
from nappingcat.exceptions import NappingCatBadConfig
import sys

class ServeApp(App):
    def main(self, user, original_command):
        settings = config.build_settings()        
        if not settings.has_section(config.SECTION_NAME):
            raise NappingCatBadConfig("""
                Your nappingcat.conf file does not include a %s section!
            """.strip() % config.SECTION_NAME)

        kitty_config = dict(settings.items(config.SECTION_NAME))
        if kitty_config.get('paths', None) is not None:
            sys.path[0:0] = [i for i in kitty_config['paths'].split('\n') if i]        

        router_module_name = kitty_config.get('router')
        cmdpatterns = include(router_module_name)

        target, match = cmdpatterns.match(original_command)
        request = Request(
            user=user, 
            command=original_command, 
            settings=settings
        )
        return target(request, **match.groupdict())


