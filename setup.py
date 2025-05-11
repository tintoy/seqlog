#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

def normalize_line_endings(text: str):
    return text.replace('\r\n', '\n').replace('\r', '\n')

with open('README.rst') as readme_file:
    readme = readme_file.read()
    readme = normalize_line_endings(readme)

with open('HISTORY.rst') as history_file:
    history = history_file.read()
    history = normalize_line_endings(history)

requirements = [
    'python_dateutil>=2.5.3',
    'requests>=2.10.0',
    'PyYAML>=3.11',
]

test_requirements = [
    'pip>=8.1.2',
    'bumpversion>=0.5.3',
    'wheel>=0.29.0',
    'watchdog>=0.8.3',
    'flake8>=2.6.0',
    'tox>=2.3.1',
    'coverage>=4.1',
    'Sphinx>=1.4.4',
    'cryptography==42.0.4',
    'PyYAML>=3.11',
    'pytest>=2.9.2',
    'httmock>=1.2.5'
]

setup(
    name='seqlog',
    version='0.4.1',
    description="SeqLog enables logging from Python to Seq.",
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/x-rst',
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
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    test_suite='tests',
    tests_require=test_requirements
)

