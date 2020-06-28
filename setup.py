# coding: utf8

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='GRADitude',
    version='0.1.0',
    packages=['graditudelib'],
    author='Silvia Di Giorgio, Konrad U. Förstner',
    author1_email='silvia.digiorgio@uni-wuerzburg.de',
    author2_email='konrad.foerstner@uni-wuerzburg.de',
    description='A tool for the analysis of GRAD-seq data',
    url='https://github.com/konrad/GRADitude',
    install_requires=[
        "matplotlib == 2.0.2",
        "pandas == 0.20.1",
        "numpy == 1.11.3",
        "scipy == 0.19.0",
        "scikit-learn == 0.18.1"
        "bokeh == 0.12.6", 'scikit-learn', 'bokeh'
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
