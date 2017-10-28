import os

from setuptools import setup
import distutils.command.sdist

import setuptools.command.sdist

# Patch setuptools' sdist behaviour with distutils' sdist behaviour
setuptools.command.sdist.sdist.run = distutils.command.sdist.sdist.run

version_info = {}
cwd=os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(cwd, "dxlelasticsearchservice", "_version.py")) as f:
    exec(f.read(), version_info)

dist = setup(
    # Package name:
    name="dxlelasticsearchservice",

    # Version number:
    version=version_info["__version__"],

    # Requirements
    install_requires=[
        "dxlbootstrap>=0.1.3",
        "dxlclient",
        "elasticsearch>=5.0.0,<6.0.0"
    ],

    # Package author details:
    author="",

    # License
    license="",

    # Keywords
    keywords=[],

    # Packages
    packages=[
        "dxlelasticsearchservice",
        "dxlelasticsearchservice._config",
        "dxlelasticsearchservice._config.sample",
        "dxlelasticsearchservice._config.app"],

    package_data={
        "dxlelasticsearchservice._config.sample" : ['*'],
        "dxlelasticsearchservice._config.app" : ['*']},

    # Details
    url="",

    description="",

    long_description=open('README').read(),

    classifiers=[
        "Programming Language :: Python"
    ],
)
