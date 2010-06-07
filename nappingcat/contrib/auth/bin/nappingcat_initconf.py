import os

DEFAULT_CONF = """
[kittyconfig]
routers =
        nappingcat.contrib.auth.patterns
        nappingcat.contrib.git.patterns
        nappingcat.contrib.discoverable.patterns
auth = nappingcat.contrib.auth.backends.jsonauth.JSONAuthBackend
[kittygit]
git = %s 
repo_dir = ~/repos
[jsonauth]
file = ~/auth.json
""".strip()

def which(program):
    is_executable = lambda path : os.path.exists(path) and os.access(path, os.X_OK)
    for path in os.environ['PATH'].split(os.pathsep):
        executable_path = os.path.join(path, program)
        if is_executable(executable_path):
            return executable_path
    return None

def main(username=None):
    username = username if username is not None else os.getlogin()
    output_to = os.path.expanduser('~%s/nappingcat.conf' % username)
    git_executable = which('git')
    if git_executable is None:
        print "\033[0;31mYou don't have `git` installed on path. This'll make kittygit fairly useless.\033[0m\n" % output_to
    if not os.path.isfile(output_to):
        try:
            with open(output_to, 'w') as output:
                output.write(DEFAULT_CONF % git_executable)
            print "\033[0;32mGenerated a default configuration file at %s.\033[0m\n" % output_to
        except (OSError, IOError) as e:
            print "\033[0;31mYou don't have permission to write to %s. Try running the command with `sudo`.\033[0m\n" % output_to
    else:
        print "\033[0;31m%s already exists.\033[0m\n" % output_to

