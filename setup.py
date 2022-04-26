# -*- coding: utf-8 -*-


"""setup.py: setuptools control."""

import re
from setuptools import setup

# https://coderwall.com/p/qawuyq/use-markdown-readme-s-in-python-modules
import os


def long_desc():
    # if os.path.exists('README.md'):
    #     long_descr = open('README.md').read()
    # else: 
    #     long_descr = 'Add a fallback short description here'

    with open("README.md", "rb") as f:
        long_descr = f.read().decode("utf-8")

    return long_descr


long_description = long_desc()

version = re.search(
    r'^__version__\s*=\s*"(.*)"',
    open('simple_curses/version.py').read(),
    re.M
).group(1)

setup(
    name="simple_curses",
    packages=["simple_curses", "simple_curses/widgets"],
    version=version,
    description="A python script implementing a framework for simple cli apps using curses. Personal tool only.",
    long_description=long_description,

    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Intended Audience :: System Administrators',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities'],

    keywords='TUI front end for simple cli programs',

    test_suite="tests.*",

    author="Robert Blackwell",
    author_email="rob@whiteacorn.com",
    url="http://github.com/robertoblackwell/simple_curses.git",
    license='MIT',
    zip_safe=False
)
