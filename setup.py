import os

from setuptools import setup, find_packages

setup(
    name='mnp',
    version='1.0.0',
    author='Heryandi',
    author_email='heryandi@gmail.com',
    packages=find_packages(exclude='test'),
    scripts=[],
    url='https://github.com/heryandi/mnp',
    license='MIT',
    description='Wrapper tools to manage Mininet package',
    long_description=open('README.rst').read(),
    install_requires=[
        "pip",
        "distribute",
    ],
    entry_points={'console_scripts': [
        'mnp = mnp:main',
    ]}
)
