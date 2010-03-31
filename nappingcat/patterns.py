from nappingcat.util import import_module 
from nappingcat.exceptions import NappingCatUnhandled
import re

class CommandPatterns(object):
    def __init__(self, path, map):
        self.path, self.map = path, map
        if self.path:
            self.module = import_module(self.path)

    def match(self, command):
        for regex, target in self.map:
            match = re.search(regex, command)
            if match:
                new_cmd = command.replace(command[match.start():match.end()], '')
                results = None
                if isinstance(target, CommandPatterns):
                    try:
                        results = target.match(new_cmd)
                    except NappingCatUnhandled:
                        pass
                elif isinstance(target, str):
                    results = getattr(self.module, target), match
                elif hasattr(target, '__call__'):
                    results = target, match

                if results is not None:
                    return results
        raise NappingCatUnhandled("This cat doesn't understand %s." % command)

def include(path):
    router_module = import_module(path)
    cmdpatterns = getattr(router_module, 'cmdpatterns')
    return cmdpatterns

def patterns(path, *args):
    return CommandPatterns(path, args) 
