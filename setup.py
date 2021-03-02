# coding: utf8

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='GRADitude',
    version='0.1.1',
    packages=['graditudelib'],
    author='Silvia Di Giorgio, Konrad U. Förstner',
    author1_email='digiorgio@zbmed.de',
    author2_email='foerstner@zbmed.de',
    description='A tool for the analysis of GRAD-seq data',
    url='https://github.com/foerstner-lab/GRADitude.git',
    install_requires=[
        "matplotlib == 3.1.1",
        "scipy == 1.3.1",
        "bokeh == 1.3.4",
        "Jinja2 == 2.10.3",
        "numpy == 1.17.2",
        "umap-learn == 0.3.10",
        "pytest == 5.2.1",
        "holoviews == 1.14.1",
        "pandas == 0.25.1",
        "networkx == 2.3",
        "seaborn == 0.9.0",
        "scikit-learn == 0.21.3"
    ],
    scripts=['bin/graditude'],
    license='ISC License (ISCL)',
    classifiers=[
        'License :: OSI Approved :: ISC License (ISCL)',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
    ]
)
