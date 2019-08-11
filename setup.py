#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009 Akoha. Written by Simon Law <sfllaw@sfllaw.ca>
# 
# This software is licensed under the same terms and conditions as
# Python itself. See the file LICENSE.txt for more details.

from setuptools import setup

LONG_DESCRIPTION = """cygwinreg3 is a direct Cygwin port of Python's winreg.

This is because _winreg or winreg modules don't exist in the Cygwin
Python port.  But often, it is useful to have Python programs running
in Cygwin read and write to the Windows registry.
"""

setup(name='cygwinreg3',
      version='1.0',
      packages=['cygwinreg3'],
      description='Windows registry access for the Cygwin toolkit',
      long_description=LONG_DESCRIPTION,
      author='Simon Law',
      author_email='sfllaw@sfllaw.ca',
      maintainer='Steve Forget',
      url='http://bitbucket.org/sfllaw/cygwinreg3/',
      license='Python Software Foundation License',
      platforms=['Cygwin'],
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
      )



