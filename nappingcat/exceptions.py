class NappingCatException(Exception):
    pass

class NappingCatUnhandled(NappingCatException):
    pass

class NappingCatBadConfig(NappingCatException):
    pass

class NappingCatRejected(NappingCatException):
    pass
