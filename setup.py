#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst', encoding='utf-8') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst', encoding='utf-8') as history_file:
    history = history_file.read()

requirements = [ ]

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="chuiba",
    author_email='chuibachuibachuiba@163.com',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Bilibili alarmclock",
    entry_points={
        'console_scripts': [
            'garb_alarm_clock=garb_alarm_clock:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='garb_alarm_clock',
    name='garb_alarm_clock',
    packages=find_packages(include=['garb_alarm_clock', 'garb_alarm_clock.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/chuiba/garb_alarm_clock',
    version='0.2.1',
    zip_safe=False,
)
