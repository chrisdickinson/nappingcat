#!/usr/bin/python
from setuptools import setup, find_packages
import os
import glob

def get_entry_points():
    entry_points = [
        'nappingcat-serve = nappingcat.serve:ServeApp.run',
    ] 
    for f in glob.glob("nappingcat/contrib/*/bin/*.py"):
        module_name = f[:-3].replace('/', '.')
        command_name = module_name.rsplit('.', 1)[-1]
        entry_points.append("%s = %s:main" % (command_name, module_name))
    return entry_points

setup(
    name = "nappingcat",
    version = "0.3",
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
    url = "http://github.com/downloads/chrisdickinson/nappingcat/nappingcat-0.3.tar.gz",

    entry_points = {
        'console_scripts': get_entry_points(),
        },

    zip_safe=False,
    install_requires=[
        'setuptools>=0.6c5',
        'importlib>=1.0.2',
        ],
    )


