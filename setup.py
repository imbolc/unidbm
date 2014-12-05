#!/usr/bin/env python
import os
import sys
import doctest
from codecs import open

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import unidbm as module

name = module.__name__
readme = module.__doc__.strip()

with open('README.md', 'w', 'utf-8') as f:
    f.write(readme)
if doctest.testfile('README.md',
                    optionflags=doctest.REPORT_ONLY_FIRST_FAILURE).failed:
    sys.exit(1)

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit(0)

setup(
    name=module.__name__,
    version=module.__version__,
    description=readme.splitlines()[0],
    long_description=readme,
    author='Imbolc',
    author_email='imbolc@imbolc.name',
    url='https://github.com/imbolc/%s' % name,
    packages=[
        'unidbm',
        'unidbm.backends',
        'unidbm.middlewares',
    ],
    install_requires=[],
    license='ISC',
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',

        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4'
    ),
)
