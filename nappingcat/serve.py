from nappingcat import config
from nappingcat.app import App
from nappingcat.patterns import patterns, include, CommandPatterns
from nappingcat.util import import_module, import_class_from_module
from nappingcat.request import Request
from nappingcat.exceptions import NappingCatBadArguments
import sys

class ServeApp(App):
    def create_request(self, cmdpatterns):
        try:
            user = self.environ.get('argv', [None])[0]
        except IndexError:
            raise NappingCatBadArguments("nappingcat-serve needs a user to run properly.") 
        return Request(
            user=self.environ.get('argv', [None])[0],
            command=self.environ.get('SSH_ORIGINAL_COMMAND', None),
            settings=self.global_settings,
            streams=(self.stdin, self.stdout, self.stderr),
            root_patterns=cmdpatterns,
        )

    def setup_environ(self):
        super(ServeApp, self).setup_environ()
        router_module_names = self.nappingcat_settings.get('routers')
        router_module_names = "" if not router_module_names else router_module_names
        self.routers = [(r'^', include(i)) for i in router_module_names.split('\n') if i]
        pubkey_handler_name = self.nappingcat_settings.get('public_key_handler', 'nappingcat.pubkey_handlers.AuthorizedKeysFile')

        self.public_key_handler = import_class_from_module(pubkey_handler_name)()
 
    def main(self):
        cmdpatterns = CommandPatterns('', self.routers)
        request = self.create_request(cmdpatterns)
        target, match = cmdpatterns.match(request.command)
        result = target(request, **match.groupdict())
        request.auth_backend.finish(self.public_key_handler)
        return result

