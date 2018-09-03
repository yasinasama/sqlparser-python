# -*- coding: utf-8 -*-

from setuptools import setup


packages = ['sqlparser']

requires = ['ply']

setup(
    name = "sqlparser-python",
    version = "0.1",
    author = "yasinasama",
    author_email = "yasinasama01@gmail.com",
    description = "SQL parser with python.",
    license = "MIT",
    keywords = "SQL parser",
    install_requires = requires,
    packages=packages
)