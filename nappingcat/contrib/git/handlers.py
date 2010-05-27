from nappingcat import auth
from nappingcat.exceptions import NappingCatRejected, NappingCatException
from nappingcat.contrib.git.exceptions import KittyGitUnauthorized
from nappingcat.contrib.git.utils import get_full_repo_dir, get_clone_base_url
from nappingcat.contrib.git import operations
import socket
import os
import subprocess
import sys

def get_settings(request):
    return dict(request.settings.items('kittygit'))

def fork_repo(request, repo):
    settings = get_settings(request)

    username, repo_name = repo.split('/', 1)
    if auth.has_permission(request.settings, request.user, ('kittygit', 'read', '%s/%s' % (username, repo_name))):

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
            auth.add_permission(request.settings, request.user, ('kittygit', 'write', '%s/%s' % (request.user, repo_name)))
            auth.add_permission(request.settings, request.user, ('kittygit', 'read', '%s/%s' % (request.user, repo_name)))
            auth.add_permission(request.settings, username, ('kittygit', 'read', '%s/%s' % (request.user, repo_name)))
            clone_base = get_clone_base_url(settings)
            return "Repository '%s' successfully forked.\nClone it at '%s:%s/%s.git'" % (repo, clone_base, request.user, repo_name)
        else:
            raise NappingCatException('Fork failed.')
    else:
        raise KittyGitUnauthorized("You don't have permission to read %s.git. Sorry!" % repo)

def create_repo(request, repo_name, template_dir=None):
    settings = get_settings(request)
    if auth.has_permission(request.settings, request.user, ('kittygit','create')):
        auth.add_permission(request.settings, request.user, ('kittygit','write','%s/%s' % (request.user, repo_name)))
        auth.add_permission(request.settings, request.user, ('kittygit', 'read', '%s/%s' % (request.user, repo_name)))

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
            return """
                Successfully created a new repository. Clone it at %s:%s.git
            """.strip() % (clone_base, '/'.join([request.user, repo_name]))
        else:
            raise NappingCatException('Create repo failed.') 
    raise KittyGitUnauthorized('You don\'t have permission to create a repo.')

def handle_git(request, action, permission_prefix='kittygit'):
    settings = get_settings(request)
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
    if auth.has_permission(request.settings, request.user, (permission_prefix, perm, parsed_repo)):
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
            return "Successfully %s repo '%s'" % (verb, parsed_repo)
        raise NappingCatException('git%s failed.' % action.strip())
    else:
        raise KittyGitUnauthorized("You don't have permission to %s repo '%s'" % (perm, parsed_repo))
