import optparse
import sys
from nappingcat.config import build_settings, SECTION_NAME
from nappingcat.auth import get_auth_backend_from_settings
from nappingcat.util import import_class_from_module

def main(name=None, key=None):
    name = sys.argv[1] if name is None else name
    key = sys.stdin.read() if key is None else key
    settings = build_settings()
    auth = get_auth_backend_from_settings(settings)
    pubkey_handler = dict(settings.items(SECTION_NAME)).get('public_key_handler', 'nappingcat.pubkey_handlers.AuthorizedKeysFile')
    pubkey_handler = import_class_from_module(pubkey_handler)()

    auth.add_user(name)
    auth.add_key_to_user(name, key)
    auth.add_permission(
        name,
        ('auth', 'adduser'),
    )
    auth.add_permission(
        name,
        ('auth', 'modifyuser'),
    )
    auth.finish(pubkey_handler)
    print "\033[0;32m%s\033[0m\n" % """
    You just created a super great super user!
    """.strip() 
