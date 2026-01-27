# coding: utf8

from setuptools import setup

setup(
    name='GRADitude',
    version='1.1.0',
    packages=['graditudelib'],
    author='Silvia Di Giorgio, Konrad U. Förstner',
    author1_email='silviadg87@gmail.com',
    author2_email='foerstner@zbmed.de',
    description='A tool for the analysis of GRAD-seq data',
    url='https://github.com/foerstner-lab/GRADitude.git',
    install_requires=[
        "matplotlib>=3.3,<4",
        "scipy>=1.8,<2",
        "bokeh>=2.4.3,<4",
        "Jinja2>=3.1.4,<4",
        "numpy>=1.22,<3",
        "umap-learn>=0.5,<1",
        "holoviews>=1.15,<2",
        "pandas>=1.5,<3",
        "networkx>=2.8,<4",
        "seaborn>=0.12,<1",
        "scikit-learn>=1.2,<2",
    ],
    extras_require={
        "dev": [
            "pytest>=7,<9",
        ]
    },
    scripts=['bin/graditude'],
    license='ISC License (ISCL)',
    classifiers=[
        'License :: OSI Approved :: ISC License (ISCL)',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
    ]
)
