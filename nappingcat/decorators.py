class DiscoverableEndpoint(object):
    def __init__(self, params, help_text, func):
        self.params, self.help_text, self.func = params, help_text, func

    def get_regex(self, patterns):
        item = patterns.find_func(self)
        return item[0] 

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

def discoverable(params, help_text):
    def inner(func):
        return DiscoverableEndpoint(params, help_text, func)
    return inner 
