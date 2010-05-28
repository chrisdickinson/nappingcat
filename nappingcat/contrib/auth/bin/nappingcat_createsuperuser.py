import optparse
import sys
from nappingcat.config import build_settings
from nappingcat.auth import get_auth_backend_from_settings

def main():
    name = sys.argv[1]
    key = sys.stdin.read()
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
