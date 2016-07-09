#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'python_dateutil>=2.5.3',
    'requests>=2.10.0'
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='seqlog',
    version='0.1.0',
    description="SeqLog enables logging from Python to Seq.",
    long_description=readme + '\n\n' + history,
    author="Adam Friedman",
    author_email='tintoy@tintoy.io',
    url='https://github.com/tintoy/seqlog',
    packages=[
        'seqlog',
    ],
    package_dir={'seqlog':
                 'seqlog'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='seqlog',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
