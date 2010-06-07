from nappingcat.patterns import patterns

cmdpatterns = patterns('nappingcat.contrib.git.handlers',
    (r'^kitty-git fork \'(?P<repo>[\w\.\-\\\/]+).git\'', 'fork_repo'),
    (r'^kitty-git create-repo \'(?P<repo_name>[\w\/\\\-\.]+)\'( --template=\'(?P<template_dir>.*)\')?', 'create_repo'),
    (r'^kitty-git delete-repo \'(?P<repo_name>[\w\/\\\-\.]+)\'', 'delete_repo'),
    (r'^kitty-git list (?P<username>[\w\\\-\.]+)', 'list_repos'),
    (r'^git(?P<action>[\-a-zA-Z_0-9\s]+)', 'handle_git'),
)
