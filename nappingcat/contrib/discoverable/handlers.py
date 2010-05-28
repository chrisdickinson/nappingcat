from nappingcat.exceptions import NappingCatRejected
from nappingcat.response import Success 
from nappingcat.decorators import discoverable, DiscoverableEndpoint
from nappingcat.patterns import CommandPatterns

import sys
import os

@discoverable({},"""
discover
 
    send back a list of all discoverable end points, their regexen, args, and help text.
""".strip())
def discover(request):
    root_patterns = request.root_patterns
    output = {}

    def recurse(pattern, base_regex):
        for regex, target in pattern.map:
            if isinstance(target, DiscoverableEndpoint):
                target_info = target.to_dict()
                target_info.update({
                    'regex':base_regex+regex,
                })
                output[target_info['name']] = target_info 
            elif isinstance(target, CommandPatterns):
                recurse(target, base_regex + regex)

    recurse(root_patterns)
    return Success({
        'message':'Successfully ran discover.',
        'endpoints':output,
    })
