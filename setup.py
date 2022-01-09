#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009 Akoha. Written by Simon Law <sfllaw@sfllaw.ca>
# Copyright (C) 2021 Steve Forget
#
# This software is licensed under the same terms and conditions as
# Python itself. See the file LICENSE.txt for more details.

from setuptools import setup, Command
from distutils.spawn import spawn
import sys


class test(Command):
    description = "run tests"

    user_options = []

    def initialize_options(self):
        self.tests = None

    def finalize_options(self):
        if self.tests is None:
            self.tests = ['test.test_cygwinreg3']

    def run(self):
        for test in self.tests:
            spawn([sys.executable, '-m', test], search_path=False)


LONG_DESCRIPTION = """cygwinreg3 is a direct Cygwin port of Python's winreg.

This is because _winreg or winreg modules don't exist in the Cygwin
Python port.  But often, it is useful to have Python programs running
in Cygwin read and write to the Windows registry.
"""

setup(name='cygwinreg3',
      version='1.2',
      packages=['cygwinreg3'],
      description='Windows registry access for the Cygwin toolkit',
      long_description=LONG_DESCRIPTION,
      author='Simon Law',
      author_email='sfllaw@sfllaw.ca',
      maintainer='Steve Forget',
      url='https://github.com/VonJagdstrumel/cygwinreg3/',
      license='Python Software Foundation License',
      platforms=['Cygwin'],
      python_requires='>=3.6',
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Win32 (MS Windows)',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Python Software Foundation License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Other',
        'Programming Language :: Python',
        'Topic :: Software Development',
        ],
      cmdclass={'test': test},
      )
