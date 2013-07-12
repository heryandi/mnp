import os

from setuptools import setup, find_packages

scripts = [os.path.join('bin', filename) for filename in os.listdir('bin')]

setup(
    name='mnp',
    version='1.0.0',
    author='Heryandi',
    author_email='heryandi@gmail.com',
    packages=find_packages(exclude='test'),
    scripts=scripts,
    url='https://github.com/heryandi/mnp',
    license='MIT',
    description='Wrapper tools to manage Mininet package',
    long_description=open('README.txt').read(),
    install_requires=[
        "pip",
        "distribute",
    ],
    entry_points={'console_scripts': [
        'mnp = mnp:main',
    ]}
)
