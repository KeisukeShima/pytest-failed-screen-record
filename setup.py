#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='pytest-failed-screen-record',
    version='0.1.0',
    author='Keisuke Shima',
    author_email='19993104+KeisukeShima@users.noreply.github.com',
    maintainer='Keisuke Shima',
    maintainer_email='19993104+KeisukeShima@users.noreply.github.com',
    license='MIT',
    url='https://github.com/KeisukeShima/pytest-failed-screen-record',
    description='Create a video of the screen when pytest fails',
    long_description=read('README.rst'),
    py_modules=['pytest_failed_screen_record'],
    python_requires='>=3.8',
    install_requires=['pytest>=7.1.2'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points={
        'pytest11': [
            'failed_screen_record = pytest_failed_screen_record',
        ],
    },
)
