from nappingcat.patterns import patterns

cmdpatterns = patterns('felix.handlers', 
    (r'add-user (?P<username>[\w\.\-]+)', 'add_user'),
    (r'add-key-to-user (?P<username>[\w\.\-]+)', 'add_key_to_user'),
    (r'add-permission (?P<username>[\w\.\-]+) \'(?P<permission>.*)\'', 'add_permission'),
    (r'remove-permission (?P<username>[\w\.\-]+) \'(?P<permission>.*)\'', 'remove_permission'),
)
