from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='sqlparser',
    version='0.1',
    description='fancy sql parser connected to many engines',
    packages=find_packages(exclude=['spa', 'docs']),
    entry_points={
        'console_scripts': ['sqlparser=sqlparser.__main__:main'],
    },
    install_requires=requirements,
)
