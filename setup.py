# coding: utf8

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='GRADitude',
    version='0.0.1',
    packages=['graditudelib'],
    author='Silvia Di Giorgio, Konrad U. Förstner',
    author_email='silvia.digiorgio@uni-wuerzburg.de',
    description='',
    url='https://github.com/konrad/...',
    install_requires=[
        "matplotlib == 2.0.2",
        "pandas == 0.20.1",
        "numpy == 1.11.3",
        "scipy == 0.19.0"
    ],
    scripts=['bin/GRADitude'],
    license='ISC License (ISCL)',
    classifiers=[
        'License :: OSI Approved :: ISC License (ISCL)',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
    ]
)
