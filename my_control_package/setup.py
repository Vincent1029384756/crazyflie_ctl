from setuptools import setup
import os
from glob import glob

package_name = 'my_control_package'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='your_name',
    maintainer_email='your_email@example.com',
    description='Crazyflie control package',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'dip_detect = my_control_package.dip_detect:main',
            'path_follower = my_control_package.path_follower:main',
        ],
    },
)
