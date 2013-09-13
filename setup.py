import os

from setuptools import setup, find_packages

setup(
    name="mnp",
    version="1.0.0",
    author="Heryandi",
    author_email="heryandi@gmail.com",
    packages=find_packages(exclude="test"),
    scripts=[],
    url="https://github.com/heryandi/mnp",
    license="MIT",
    description="Tools to manage Mininet package",
    long_description=open("README.rst").read(),
    install_requires=[
        "pip",
        "requests",
        "setuptools",
    ],
    entry_points={"console_scripts": [
        "mnp = mnp:main",
    ]},
    classifiers=[
        "Mininet :: Tool",
    ],
    keywords="command-line commandline mininet package packaging tool"
)
