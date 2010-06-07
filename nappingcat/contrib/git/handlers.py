from nappingcat.exceptions import NappingCatRejected, NappingCatException
from nappingcat.contrib.git.exceptions import KittyGitUnauthorized
from nappingcat.contrib.git.utils import get_full_repo_dir, get_clone_base_url
from nappingcat.contrib.git import operations
from nappingcat.response import Success, TextResponse 
from nappingcat.decorators import discoverable
import socket
import os
import subprocess
import sys
import glob
import shutil

def get_settings(request):
    return dict(request.settings.items('kittygit'))

@discoverable({'repo_name':'string'},"""
delete_repo <repo_name>
""".strip())
def delete_repo(request, repo_name):
    if request.auth_backend.has_permission(request.user, ('kittygit', 'write', repo_name)):
        full_directory = os.path.expanduser(os.path.join(dict(request.settings.items('kittygit'))['repo_dir'], repo_name + '.git'))
        if os.path.isdir(full_directory):
            try:
                shutil.rmtree(full_directory)
                return Success({
                    'message':"Successfully deleted repository '%s'" % repo_name
                })
            except OSError:
                raise NappingCatRejected("Could not remove that path.")
    raise KittyGitUnauthorized("You don't have permission to remove '%s'" % repo_name)

@discoverable({'username':'string'},"""
list_repos
""".strip())
def list_repos(request, username):
    path = os.path.expanduser(os.path.join(dict(request.settings.items('kittygit'))['repo_dir'], username)) 
    output = []
    for file in glob.glob('%s/*.git' % path):
        repo = file.rsplit('/', 1)[-1][:-4]
        full_repo_name = '%s/%s' % (username, repo)
        if request.auth_backend.has_permission(request.user, ('kittygit', 'read', full_repo_name)):
            output.append(full_repo_name)
    return Success({
        'message':"You have access to the following repositories:\n\t%s" % "\n\t".join(output)
    })

@discoverable({'repo':'string'},"""
fork_repo <repo_name>

    fork another user's repository to which you have read access.
    repository is given in the form <username>/<repo_name>.

""".strip())
def fork_repo(request, repo):
    settings = get_settings(request)
    auth = request.auth_backend
    username, repo_name = repo.split('/', 1)
    if auth.has_permission(request.user, ('kittygit', 'read', '%s/%s' % (username, repo_name))):

        to_repo_dir = get_full_repo_dir(settings, request.user, repo_name)
        from_repo_dir = get_full_repo_dir(settings, username, repo_name)
        success = operations.fork_repository(
            settings.get('git', 'git'),
            request.stdin,
            request.stdout,
            request.stderr,
            from_repo_dir,
            to_repo_dir
        )
        if success:
            auth.add_permission(request.user, ('kittygit', 'write', '%s/%s' % (request.user, repo_name)))
            auth.add_permission(request.user, ('kittygit', 'read', '%s/%s' % (request.user, repo_name)))
            auth.add_permission(username, ('kittygit', 'read', '%s/%s' % (request.user, repo_name)))
            clone_base = get_clone_base_url(settings)
            return Success({'message':"Repository '%s' successfully forked.\nClone it at '%s:%s/%s.git'" % (repo, clone_base, request.user, repo_name)})
        else:
            raise NappingCatException('Fork failed.')
    else:
        raise KittyGitUnauthorized("You don't have permission to read %s.git. Sorry!" % repo)

@discoverable({'repo_name':'string'},"""
create_repo <repo_name>

    create a new repository.

""".strip())
def create_repo(request, repo_name, template_dir=None):
    auth = request.auth_backend
    settings = get_settings(request)
    if auth.has_permission(request.user, ('kittygit','create')):
        auth.add_permission(request.user, ('kittygit','write','%s/%s' % (request.user, repo_name)))
        auth.add_permission(request.user, ('kittygit', 'read', '%s/%s' % (request.user, repo_name)))

        full_repo_dir = get_full_repo_dir(settings, request.user, repo_name)
        success = operations.create_repository(
            settings.get('git', 'git'),
            request.stdin,
            request.stdout,
            request.stderr,
            full_repo_dir,
            template_dir
        )
        if success:
            clone_base = get_clone_base_url(settings)
            clone_path = '/'.join([request.user, repo_name]) + '.git'
            return Success({
                'message':"""
                    Successfully created a new repository. Clone it at %s:%s
                """.strip() % (clone_base, clone_path),
                'clone_path':clone_path
            })
        else:
            raise NappingCatException('Create repo failed.') 
    raise KittyGitUnauthorized('You don\'t have permission to create a repo.')

def handle_git(request, action, permission_prefix='kittygit'):
    settings = get_settings(request)
    auth = request.auth_backend
    command, subcommand, repo = None, None, None
    if action in (' receive-pack ', ' upload-pack '):
        command, subcommand, repo = request.command.split(' ', 2)
    else:
        command, repo = request.command.split(' ', 1)

    modes = {
        ' receive-pack ':'write',
        '-receive-pack ':'write',
        ' upload-pack ':'read',
        '-upload-pack ':'read',
    }
    perm = modes[action]

    parsed_repo = repo[1:-1][:-4]       # remove quotes and .git extension
    repo_name = parsed_repo.split('/', 1)[1]
    if auth.has_permission(request.user, (permission_prefix, perm, parsed_repo)):
        directory = get_full_repo_dir(settings, request.user, repo_name) 
        success = operations.git_shell(
            settings.get('git', 'git'), 
            request.stdin, 
            request.stdout, 
            request.stderr, 
            action, 
            directory
        ) 
        if success:
            verb = {
                'write':'wrote to',
                'read':'read from',
            }[perm]
            return Success("Successfully %s repo '%s'" % (verb, parsed_repo), TextResponse)
        raise NappingCatException('git%s failed.' % action.strip())
    else:
        raise KittyGitUnauthorized("You don't have permission to %s repo '%s'" % (perm, parsed_repo))
