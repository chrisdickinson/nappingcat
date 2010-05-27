from nappingcat.patterns import patterns

cmdpatterns = patterns('nappingcat.contrib.git.handlers',
    (r'^kitty-git fork \'(?P<repo>[\w\/]+).git\'', 'fork_repo'),
    (r'^kitty-git create-repo \'(?P<repo_name>[\w\\\.]+)\'( --template=\'(?P<template_dir>.*)\')?', 'create_repo'),
    #(r'^kitty-git add-read \'(?P<repo_name>[\w\\\.]+)\' \'(?P<username>[\w\.\-]+)\'', 'add_read'),
    #(r'^kitty-git remove-read \'(?P<repo_name>[\w\\\.]+)\' \'(?P<username>[\w\.\-]+)\'', 'add_read'),
    (r'^git(?P<action>[\-a-zA-Z_0-9\s]+)', 'handle_git'),
)
