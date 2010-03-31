from nappingcat.auth import AuthBackend

class SleazyAuth(AuthBackend):
    def get_permission(*args,**kwargs):
        return True

    def has_permission(*args,**kwargs):
        return True
    def add_permission(*args,**kwargs):
        return True

    def remove_permission(*args,**kwargs):
        return True

    
