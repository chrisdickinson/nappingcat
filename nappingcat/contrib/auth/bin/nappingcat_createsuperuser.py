import optparse
import sys
from nappingcat.config import build_settings
from nappingcat.auth import get_auth_backend_from_settings

def main(name=None, key=None):
    name = sys.argv[1] if name is None else name
    key = stdin.read() if key is None else key
    settings = build_settings()
    auth = get_auth_backend_from_settings(settings)
    auth.add_user(name)
    auth.add_key_to_user(name, key)
    auth.add_permission(
        ('auth', 'adduser'),
    )
    auth.add_permission(
        ('auth', 'modifyuser'),
    )
    print "\033[0;32m%s\033[0m\n" % """
    You just created a super great super user!
    """.strip() 
