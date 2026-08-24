from setuptools import setup, find_packages

setup(
    name='NetAutomate',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'netmiko',
        'napalm',
        'paramiko',
        'jinja2',
        'pyyaml',
        'rich',
        'click',
        'textfsm',
        'nornir',
        'nornir-netmiko'
    ],
    entry_points={
        'console_scripts': [
            'netautomate=src.cli:cli',
        ],
    },
)
