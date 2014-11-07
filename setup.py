#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


ROOT = os.path.dirname(os.path.abspath(__file__))
README_PATH = os.path.join(ROOT, 'README')

try:
    with open(README_PATH, 'rb') as fp:
        long_desc = fp.read()
except:
    long_desc = ''

install_requires = [
    'six',
    'transaction',
    'sqlalchemy',
    'zope.interface',
    'zope.sqlalchemy',
    ]

test_require = [
    'tox',
    'nose',
    'mock',
    'coverage',
    'testfixtures',
    ] + install_requires


class Tox(TestCommand):
    user_options = [('tox-args=', 'a', "Arguments to pass to tox")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import tox
        import shlex
        errno = tox.cmdline(args=shlex.split(self.tox_args))
        sys.exit(errno)

DESCRIPTION = 'Sqlalchemy utilities'


setup(
    name='azoth',
    version='0.1.0',
    url='https://github.com/TakesxiSximada/azoth',
    download_url='https://github.com/TakesxiSximada/azoth',
    license='BSD',
    author='TakesxiSximada',
    author_email='takesxi.sximada@gmail.com',
    description=DESCRIPTION,
    long_description=long_desc,
    zip_safe=False,
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Web Environment :: Mozilla',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Natural Language :: Esperanto',
        'Natural Language :: Japanese',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        ],
    platforms='any',
    include_package_data=True,
    install_requires=install_requires,
    test_require=test_require,
    packages=find_packages(),
    cmdclass={'test': Tox},
    )
