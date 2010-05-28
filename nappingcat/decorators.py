class DiscoverableEndpoint(object):
    def __init__(self, name, params, help_text, func):
        self.name = name
        self.params, self.help_text, self.func = params, help_text, func

    def to_dict(self):
        return {
            'name':self.name,
            'params':self.params,
            'help_text':self.help_text,
        }

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

def discoverable(params, help_text):
    def inner(func):
        return DiscoverableEndpoint(func.__name__, params, help_text, func)
    return inner 
