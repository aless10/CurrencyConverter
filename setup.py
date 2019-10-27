#!/usr/bin/env python
# flake8: noqa
import os

from setuptools import setup, find_packages
from pkg_resources import parse_requirements

req_file = os.path.join(os.path.dirname(__file__), "requirements.txt")

with open(req_file, 'r') as inst_reqs:
    install_requires = [str(req) for req in parse_requirements(inst_reqs)]

packages = find_packages(include=['convert_app', 'convert_app.*'])

setup(
    name='convert_app',
    version='1.0.0.dev',
    author='Alessio Izzo',
    author_email='alessio.izzo86@gmail.com',
    description='An online currency converter',
    long_description=__doc__,
    packages=packages,
    install_requires=install_requires,
    include_package_data=True,
    classifiers=[
        'Development Status :: 1 - Beta',
        'Programming Language :: Python',
        'Environment :: Web Environment',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: System :: Software Distribution',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
