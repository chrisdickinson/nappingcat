class NappingCatException(Exception):
    pass

class NoUserException(NappingCatException):
    pass

class NappingCatUnhandled(NappingCatException):
    pass

class NappingCatBadConfig(NappingCatException):
    pass

class NappingCatBadPatterns(NappingCatBadConfig):
    pass

class NappingCatRejected(NappingCatException):
    pass
