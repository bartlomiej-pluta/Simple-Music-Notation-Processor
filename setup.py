import os

from setuptools import setup, find_packages


def file(file):
    return open(os.path.join(os.path.dirname(__file__), file)).read()

setup(
    name='SMNP',
    version=file('smnp/meta/__version__.txt'),
    packages=find_packages(),
    description=file('smnp/meta/__description__.txt'),
    author='Bartlomiej P. Pluta',
    url='https://gitlab.com/bartlomiej.pluta/smnp',
    install_requires=[
        "cffi>=1.12.3",
        "cycler>=0.10.0",
        "kiwisolver>=1.1.0",
        "matplotlib>=3.1.1",
        "numpy>=1.17.2",
        "pycparser>=2.19",
        "pyparsing>=2.4.2",
        "python-dateutil>=2.8.0",
        "six>=1.12.0",
        "sounddevice>=0.3.13",
        "soundfile>=0.10.2"
    ],
    entry_points={
        'console_scripts': ['smnp=smnp.main:main']
    },
    package_data={
        'smnp.library.code': ['main.mus'],
        'smnp.meta': ['__version__.txt', '__description__.txt']
    }
)