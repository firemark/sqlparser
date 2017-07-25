from setuptools import setup, find_packages

setup(
    name='sqlparser',
    version='0.1',
    description='fancy sql parser connected to many engines',
    packages=find_packages(exclude=['spa', 'docs']),
    requirements=[
        'rply>=0.7.5',
        'SQLAlchemy>=1.1.11',
        'pymongo>=3.4.0',
    ]
)
