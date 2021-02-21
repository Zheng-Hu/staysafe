"""
EECS495 Winter 2021 Group StaySafe
StaySafe python package configuration.
Qinjuan Xie <qinjuanx@umich.edu>

Adapted from
Insta485 python package configuration.
Andrew DeOrio <awdeorio@umich.edu>
"""

from setuptools import setup

setup(
    name='staysafe',
    version='0.1.0',
    packages=['staysafe'],
    include_package_data=True,
    install_requires=[
        'arrow',
        'bs4',
        'Flask',
        'html5validator',
        'pycodestyle',
        'pydocstyle',
        'pylint',
        'pytest',
        'pytest-mock',
        'requests',
    ],
    python_requires='>=3.6',
)
