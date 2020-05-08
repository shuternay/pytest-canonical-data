#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='pytest-canonical-data',
    version='0.1.0',
    author='Sergey Kiselev',
    author_email='kiselev.sg@gmail.com',
    maintainer='Sergey Kiselev',
    maintainer_email='kiselev.sg@gmail.com',
    license='MIT',
    url='https://github.com/shuternay/pytest-canonical-data',
    description='A plugin which allows to compare results with canonical results, based on previous runs',
    long_description=read('README.rst'),
    packages=['pytest_canonical_data'],
    python_requires='>=3.5',
    install_requires=['pytest>=3.5.0'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points={
        'pytest11': [
            'canonical_data = pytest_canonical_data.plugin',
        ],
    },
)
