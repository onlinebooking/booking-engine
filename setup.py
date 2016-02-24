from distutils.core import setup
from setuptools import find_packages

setup(
    name='booking_engine',
    version='0.1',
    packages=find_packages(),
    license='MIT',
    long_description="Booking engine",
    tests_require=['nose>=1.3.7', 'coverage>=4.0.3'],
    install_requires=['toolz>=0.7.4'],
)
