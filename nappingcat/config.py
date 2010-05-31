import os
import sys
from ConfigParser import ConfigParser
SECTION_NAME = 'kittyconfig' 

def build_settings():
    config = ConfigParser()
    config.read([os.path.expanduser('~/nappingcat.conf'), '/etc/nappingcat.conf'])
    return config

def setup_environ(settings):
    kitty_config = dict(settings.items(SECTION_NAME))
    if kitty_config.get('paths', None) is not None:
        sys.path[0:0] = [i for i in kitty_config['paths'].split('\n') if i]
    return kitty_config
