import os
import sys
import subprocess
from nappingcat.contrib.git.exceptions import KittyGitRepoExists, KittyGitUnauthorized, KittyGitBadParameter
from nappingcat.exceptions import NappingCatException
def fork_repository(git, stdin, stdout, stderr, from_directory, to_directory):
    from_directory = os.path.abspath(from_directory)
    to_directory = os.path.abspath(to_directory)

    if not os.path.isdir(from_directory):
        raise NappingCatException("'%s' is not a valid repository." % from_directory)

    if os.path.isdir(to_directory):
        raise KittyGitRepoExists(to_directory)
    os.makedirs(to_directory)
    args = [
        git, '--git-dir=.', 'clone', '--mirror', from_directory, './'
    ]
    return 0 == subprocess.call(
        args=args,
        cwd=to_directory,
        stdin=stdin,
        stdout=stdout,
        stderr=stderr,
        close_fds=True,
    )

def create_repository(git, stdin, stdout, stderr, directory, template_dir=None, bare=True):
    if os.path.isdir(directory):
        raise KittyGitRepoExists(directory)
    args = [git, '--git-dir=.', 'init', '--bare']
    if not bare:
        args = [git, 'init']
    if template_dir:
        if not os.path.isdir(template_dir):
            raise KittyGitBadParameter("""
                The template directory '%s' is invalid.
            """.strip() % (template_dir))
        args.append('--template=%s'%os.path.abspath(template_dir))
    os.makedirs(directory)
    return 0 == subprocess.call(
        args=args,
        cwd=directory,
        stdin=stdin,
        stdout=stdout,
        stderr=stderr,
        close_fds=True,
    )

def git_shell(git, stdin, stdout, stderr, action, directory):
    if not os.path.isdir(directory):
        raise KittyGitBadParameter("%s is not a valid repository." % directory)
    command = 'git%s' % action.strip()
    arg = "'%s'" % directory
    args = [git, 'shell', '-c', ' '.join([command, arg])]
    return 0 == subprocess.call(
        args=args,
        cwd=directory,
        stdin=stdin,
        stdout=stdout,
        stderr=stderr
    )

 
