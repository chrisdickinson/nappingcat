from nappingcat.auth import AuthBackend
import os
try:
    import json as simplejson
except ImportError:
    import simplejson


SECTION_NAME = 'jsonauth'
class JSONAuthBackend(AuthBackend):
    def __init__(self, *args, **kwargs):
        super(JSONAuthBackend, self).__init__(*args, **kwargs)
        settings_dict = dict(self.settings.items(SECTION_NAME))
        filename = os.path.expanduser(settings_dict.get('file', '~/nappingcat_auth.json'))
        try:
            with open(filename, 'r') as input:
                self.users = simplejson.loads(input.read())
        except (IOError, ValueError) as e:
            self.users = {}
            with open(filename, 'w') as fallback:
                fallback.write(simplejson.dumps({}))

    def finish(self, pubkey_handler):
        super(JSONAuthBackend, self).finish(pubkey_handler)
        if self.require_update:
            settings_dict = dict(self.settings.items(SECTION_NAME))
            filename = os.path.expanduser(settings_dict.get('file', '~/nappingcat_auth.json'))
            with open(filename, 'w') as output:
                output.write(simplejson.dumps(self.users))
