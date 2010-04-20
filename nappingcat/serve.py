from nappingcat import config
from nappingcat.app import App
from nappingcat.patterns import patterns, include, CommandPatterns
from nappingcat.util import import_module
from nappingcat.request import Request
from nappingcat.exceptions import NappingCatBadArguments
import sys

class ServeApp(App):
    def create_request(self):
        try:
            user = self.environ.get('argv', [None])[0]
        except IndexError:
            raise NappingCatBadArguments("nappingcat-serve needs a user to run properly.") 
        return Request(
            user=self.environ.get('argv', [None])[0],
            command=self.environ.get('SSH_ORIGINAL_COMMAND', None),
            settings=self.global_settings,
            streams=(self.stdin, self.stdout, self.stderr)
        )

    def setup_environ(self):
        super(ServeApp, self).setup_environ()
        router_module_names = self.nappingcat_settings.get('routers')
        router_module_names = "" if not router_module_names else router_module_names
        self.routers = [(r'^', include(i)) for i in router_module_names.split('\n') if i]

    def main(self):
        request = self.create_request()
        cmdpatterns = CommandPatterns('', self.routers)
        target, match = cmdpatterns.match(request.command)
        return target(request, **match.groupdict())

