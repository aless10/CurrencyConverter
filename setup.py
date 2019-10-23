#!/usr/bin/env python
# flake8: noqa

from setuptools import setup, find_packages
from pkg_resources import parse_requirements


with open("requirements.txt", 'r') as inst_reqs:
    install_requires = [str(req) for req in parse_requirements(inst_reqs)]

packages = find_packages(include=['convert_app', 'convert_app.*'])

setup(
    name='convert_app',
    version='0.2.0',
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
