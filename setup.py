"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""
from setuptools import setup, find_packages

setup(
    description='Flask Management Blueprint',
    install_requires=['aiofiles', 'flask', 'websockets', 'async_timeout', 'aiohttp'],
    long_description=open('README.md').read().strip(),
    name='flask_management_blueprint',
    packages=find_packages(exclude=['tests']),
    py_modules=['flask_management_blueprint'],
    url='https://github.com/stone-payments/flask-management-blueprint',
    version='0.2.0',
)
