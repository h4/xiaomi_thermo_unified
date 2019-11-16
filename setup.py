from setuptools import find_packages, setup

VERSION = '0.0.1'

setup(
    name='xiaomi_thermo_unified',
    version=VERSION,
    packages=find_packages(exclude=("tests",)),
    url='https://github.com/h4/xiaomi_thermo_unified',
    license='MIT',
    author='h4',
    classifiers=[
        'Programming Language :: Python :: 3.7',
    ],
    install_requires=['bluepy==1.3.0'],
    author_email='mikhail.baranov@gmail.com',
    description='Unified Python client for Xiaomi BLE Thermometers',
    long_description_content_type='text/x-rst',
    long_description='Library to read data from Xiaomi BLE Temperature and Humidity Sensor (LCD Round, '
                     'E-Inc version with Clock,'
                     'ClearGrass Round E-Inc)',
)
