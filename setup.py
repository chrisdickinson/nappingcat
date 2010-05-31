#!/usr/bin/python
from setuptools import setup, find_packages
import os
import glob
from importlib import import_module

def get_entry_points():
    entry_points = [
        'nappingcat-serve = nappingcat.serve:ServeApp.run',
    ] 
    for f in glob.glob("nappingcat/contrib/*/bin/*.py"):
        module_name = f[:-3].replace('/', '.')
        try:
            module = import_module(module_name)
            main = getattr(module, 'main')
            command_name = module_name.rsplit('.', 1)[-1]
            entry_points.append("%s = %s:main" % (command_name, module_name))
        except (AttributeError, ImportError) as e:
            pass
    return entry_points

setup(
    name = "nappingcat",
    version = "0.1",
    packages = find_packages(),

    author = "Chris Dickinson",
    author_email = "chris.dickinson@domain51.com",
    description = "python framework for single-user SSH apis",
    long_description = """
A django-inspired framework for routing single-user SSH calls.

Useful for implementing software like gitosis.
""".strip(),
    license = "BSD / GPLv3 / CDDL",
    keywords = "framework restrict commands ssh",
    url = "http://github.com/chrisdickinson/nappingcat/",

    entry_points = {
        'console_scripts': get_entry_points(),
        },

    zip_safe=False,
    install_requires=[
        # setuptools 0.6a9 will have a non-executeable post-update
        # hook, this will make gitosis-admin settings not update
        # (fixed in 0.6c5, maybe earlier)
        'setuptools>=0.6c5',
        ],
    )


