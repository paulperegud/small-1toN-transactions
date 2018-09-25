from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='percentage_trees',
    version='0.0.1',
    description='Small 1toN transactions examples',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/',
    author='PePER',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3'
    ],
    keywords='contracts ethereum development solidity percentage_trees',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=[
        'ethereum==2.3.0',
        'rlp==0.6.0',
        'py-solc-simple==0.0.10'
    ]
)
