#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'andyguo'

from setuptools import setup, find_packages

setup(
    name='dayu_timecode',
    version='0.2',
    description=(
        'timecode lib for human. support SMPTE non-drop frame and drop frames and many other timecode formats.'
    ),
    long_description=open('README.rst').read(),
    author='Andy Guo',
    author_email='technology@phenom-films.com',
    maintainer='Andy Guo',
    maintainer_email='andyguo@phenom-films.com',
    license='MIT',
    packages=find_packages(),
    platforms=['dayu_timecode'],
    url='https://github.com/phenom-films/dayu_timecode',
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
)
