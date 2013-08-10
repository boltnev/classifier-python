# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

# 
# with open('README.rst') as f:
#     readme = f.read()
# 
# with open('LICENSE') as f:
#     license = f.read()

setup(
    name='indexer',
    version='0.0.1',
    description='Indexer',
    long_description=readme,
    author='Ilya Boltnev',
    author_email='ilya@boltnev.com',
    url='https://github.com/boltnev'
    packages=find_packages(exclude=('test'))
)
