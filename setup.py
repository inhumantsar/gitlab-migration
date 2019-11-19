#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

with open('requirements.txt') as reqs_file:
    requirements = reqs_file.readlines()

with open('requirements_dev.txt') as devreqs_file:
    devreqs = devreqs_file.readlines()
    test_requirements = setup_requirements = devreqs

setup(
    author="Shaun Martin",
    author_email='shaun@samsite.ca',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="This project migrates every project in one GitLab instance to another using the API.",
    entry_points={
        'console_scripts': [
            'glm=gitlab_migration.cli:cli',
            'gitlab_migration=gitlab_migration.cli:cli',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='gitlab_migration',
    name='gitlab_migration',
    packages=find_packages(include=['gitlab_migration']),
    setup_requires=setup_requirements + requirements,
    test_suite='test',
    tests_require=test_requirements,
    url='https://github.com/inhumantsar/gitlab_migration',
    version='0.1.0',
    zip_safe=False,
)
