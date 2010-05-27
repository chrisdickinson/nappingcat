import os
import socket
DEFAULT_USER_NAME = '<nappingcat-user>'

def get_full_repo_dir(settings, user, repo):
    return os.path.expanduser(
        '/'.join([settings.get('repo_dir', '~/repos'), user, repo+'.git'])
    )

def get_clone_base_url(settings):
    login, hostname = settings.get('user', None), settings.get('host', socket.gethostname()+'.local')
    try:
        login = os.getlogin() if login is None else login
    except OSError:
        login = DEFAULT_USER_NAME
    return '%s@%s' % (login, hostname)
