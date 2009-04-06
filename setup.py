#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009 Akoha. Written by Simon Law <sfllaw@sfllaw.ca>
# 
# This software is licensed under the same terms and conditions as
# Python itself. See the file LICENSE.txt for more details.

from distutils.core import setup, Command
from distutils.spawn import spawn
import sys

class test(Command):
    description = "run tests"

    user_options = []

    def initialize_options(self):
        self.tests = None

    def finalize_options(self):
        if self.tests is None:
            self.tests=['test_cygwinreg']

    def run(self):
        for test in self.tests:
            spawn([sys.executable, '-m', test], search_path=False)

setup(name='cygwinreg',
      version='1.0',
      description='Windows registry access for Cygwin',
      author='Simon Law',
      author_email='sfllaw@sfllaw.ca',
      url='http://sfllaw.ca/~sfllaw/programs/cygwinreg',
      py_modules=['cygwinreg.constants', 'cygwinreg.w32api'],
      cmdclass={'test': test},
      )



