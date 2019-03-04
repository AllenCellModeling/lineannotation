#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['kivy']

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

setup(
    author="Jamie Sherman",
    author_email='jamies@alleninstitute.org',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: Allen Institute Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="A tool for annotating myofibrile bundles to then use the path and background image to get the "
                "distribution of Sarcomere Lengths",
    entry_points={
        'console_scripts': [
            'line_annot=sarcomereannotation.bin.line_annot:main'
        ],
    },
    install_requires=requirements,
    license="Allen Institute Software License",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='sarcomereannotation',
    name='sarcomereannotation',
    packages=find_packages(include=['sarcomereannotation']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/AllenCellModeling/sarcomereannotation',
    version='0.1.0',
    zip_safe=False,
)
