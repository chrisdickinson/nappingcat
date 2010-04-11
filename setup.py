#!/usr/bin/python
from setuptools import setup, find_packages
import os

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
        'console_scripts': [
            'nappingcat-serve = nappingcat.serve:ServeApp.run',
            ],
        },

    zip_safe=False,
    install_requires=[
        # setuptools 0.6a9 will have a non-executeable post-update
        # hook, this will make gitosis-admin settings not update
        # (fixed in 0.6c5, maybe earlier)
        'setuptools>=0.6c5',
        ],
    )


