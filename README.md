napping cat
===========

installation
------------
    # on the remote:
    sudo pip install nappingcat
    useradd -m -U -s/bin/bash -r git
    sudo su git
    nappingcat_initconf
    cat id_rsa.pub > nappingcat_createsuperuser admin

    # on your local machine
    sudo pip install -e git+git://github.com/chrisdickinson/thundercat#egg=thundercat
    thundercat addremote <nickname> <git@remoteurl.com>
    thundercat add_permission admin kittygit create

    # now if you cd into a git repo...
    thundercat create_repo somerepo
    # it will create the repo on the remote server, and
    # ask if you want to add a remote.

for a while now i've been using gitosis -- it's really nice! but really, i had no idea how it worked.
so over the last week i've been picking it apart, and i found that really, it's exposing a limited API
around git using the `~/.ssh/authorized_keys` file to automatically funnel all incoming commands through
`gitosis-serve`, which then checks to see if everything looks kosher before sending things back through
git. *this is pretty cool!* it'd be great if it had a little more functionality, though. nothing crazy --
no branch level permissions or anything -- just a bit more of the sugar from github proper. like being
able to create repositories without having to edit a flat file, or being able to fork existing repositories.

i realized that i really just wanted a way to write an extensible API for a single-user ssh system. it
still seems weird, worded like that, but bare with me.

this is the result, at the moment -- it's not done! it's experimental! `nappingcat` works on the same
principle as gitosis, minus some core functionality at the moment. every ssh command coming through the
user it's configured under will be passed through a command router that looks a lot like something
you'd see in a django app.

for example, from [kittygit](http://github.com/chrisdickinson/kittygit)(the app I wrote as a proof-of-concept):

    from nappingcat.patterns import patterns

    cmdpatterns = patterns('kittygit.handlers',
        (r'^kitty-git fork \'(?P<repo>\w+).git\'', 'fork_repo'),
        (r'^kitty-git create-repo \'(?P<repo_name>[\w\\\.]+)\'', 'create_repo'),
        (r'^git(?P<action>[\-a-zA-Z_0-9\s]+)', 'handle_git'),
    )

any ssh command that comes through will pass through those regexen until it finds a match, and then
it'll delegate out to that function (that looks like the following:)

    def handle_git(request, action):
        # do things
        pass

now, they're not required to return anything -- i'm leaning towards having whatever is returned passed back out
through sys.stderr -- but you can see that a request object is passed in, and it contains the following:

    request.user            # a string for the received username
    request.settings        # a configparser instance of the settings file
    request.command         # the original command intercepted
    request.std{in,out,err} # the std streams
    request.auth_backend    # a copy of the auth backend for the session

the settings are loaded from `~/nappingcat.conf`. An example looks like the following:

    [kittyconfig]
    router = kittygit.patterns
    auth = nappingcat.contrib.sleazy_auth.SleazyAuth
    paths =
        /Users/chris/projects/nappingcat
        /Users/chris/projects/kittygit

the router parameter defines a python module from which a variable named `cmdpatterns` can be imported. it looks like
the above!

the auth parameter defines a module to use for authentication. Right now it only has one backend -- 'sleazy_auth', which
just says "yes" to everything. this is a big *TODO*.

note that you can nest cmdpatterns like in django:

    from nappingcat.patterns import patterns, include
    cmdpatterns = patterns('',
                    (r'^', include('kittygit.patterns')),
    )

so you can build up api's out of separate apps.

again, it's very very very beta.

LICENSING
------------------
In an effort to appease all and sundry, I'm offering up this software in three license flavors --
CDDL, GPLv3, or BSD. Choose your poison.


