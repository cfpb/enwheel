#!/usr/bin/env python

import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()


setup(
    name='enwheel',
    author='CFPB',
    version_format='{tag}.dev{commitcount}+{gitsha}',
    author_email='tech@cfpb.gov',
    packages=find_packages(),
    description=u'get wheels, generate repo',
    license='Public Domain, CC0',
    classifiers=[
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
    ],
    long_description=README,
    install_requires=['docopt==0.6.2'],
    setup_requires=['setuptools-git-version'],
    zip_safe=False,
    entry_points = {
            'console_scripts': ['enwheel=enwheel.cli:main'],
    }
)
