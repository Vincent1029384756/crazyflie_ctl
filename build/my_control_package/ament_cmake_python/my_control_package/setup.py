from setuptools import find_packages
from setuptools import setup

setup(
    name='my_control_package',
    version='0.1.0',
    packages=find_packages(
        include=('my_control_package', 'my_control_package.*')),
)
