from nappingcat.exceptions import NappingCatRejected

class KittyGitRepoExists(NappingCatRejected):
    def __init__(self, which):
        super(KittyGitRepoExists, self).__init__("""
            There's already a repo in %s. Whoops!
        """.strip() % which)

class KittyGitUnauthorized(NappingCatRejected):
    pass

class KittyGitBadParameter(NappingCatRejected):
    pass
