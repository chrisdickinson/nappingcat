from nappingcat.exceptions import NappingCatRejected
from nappingcat.response import Success 
from nappingcat.decorators import discoverable
import sys
import os

PERMISSION_SEP = '::'

@discoverable({'username':'string'},"""
add_user <username>
 
    create a new user.
""".strip())
def add_user(request, username):
    auth = request.auth_backend
    if auth.has_permission(request.user, ('auth', 'adduser')):
        auth.add_user(username)
        return Success({'message':"Added user '%s'" % username})
    raise NappingCatRejected("You don't have permission to add a user.")

@discoverable({'username':'string', 'key':'stdin'},"""
add_key_to_user <username>
 
    add a key (read from stdin) to an existing user.
""".strip())
def add_key_to_user(request, username):
    auth = request.auth_backend
    if auth.has_permission(request.user, ('auth', 'modifyuser')):
        key = request.stdin.read()
        settings = dict(request.settings.items('kittyconfig'))
        auth.add_key_to_user(username, key) 
        return Success({'message':"You added the key '%s...' to the user '%s'" % (key[0:30], username)})
    raise NappingCatRejected("You don't have permission to modify users.")

@discoverable({'username':'string', 'permission':('tuple', PERMISSION_SEP)}, """
add_permission <username> '<permission list>'

    add a permission to an existing user.
    permission tuples should be provided as a series of strings; e.g.,

        {EXECUTABLE} add_permission <username> kittygit read <reponame>
        {EXECUTABLE} add_permission <username> auth modifyuser

""".strip())
def add_permission(request, username, permission):
    auth = request.auth_backend
    permission_tuple = permission.split(PERMISSION_SEP)
    # if you've got global rights to modifying users,
    # OR if you've already got the existing permission
    # you can pay it forward.
    if auth.has_permission(request.user, ('auth', 'modifyuser')) or auth.has_permission(request.user, permission_tuple):
        auth.add_permission(username, permission_tuple)
        return Success({'message':"You granted '%s' the permission '%s'" % (username, permission)})
    raise NappingCatRejected("You really don't have the right to do that. Sorry.")


@discoverable({'username':'string', 'permission':('tuple', PERMISSION_SEP)}, """
remove_permission <username> '<permission list>'

    remove a permission from an existing user
""".strip())
def remove_permission(request, username, permission):
    auth = request.auth_backend
    permission_tuple = permission.split(PERMISSION_SEP)
    user_owned_permission = request.user in permission_tuple[1:]
    # if the username is in the permission AND the user actually has
    # the permission, they can remove it from who they like.
    if auth.has_permission(request.user, ('auth', 'modifyuser')) or (user_owned_permission and auth.has_permission(request.settings, request.user, permission_tuple)):
        auth.remove_permission(username, permission_tuple)
        return Success({'message':"You removed the permission '%s' from '%s'." % (permission, username)})
    raise NappingCatRejected("You really don't have the right to do that. Sorry.")
