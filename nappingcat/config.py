import os
from ConfigParser import ConfigParser
SECTION_NAME = 'kittyconfig' 

def build_settings():
    config = ConfigParser()
    config.read([os.path.expanduser('~/nappingcat.conf'), '/etc/nappingcat.conf'])
    return config
