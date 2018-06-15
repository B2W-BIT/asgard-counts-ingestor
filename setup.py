from setuptools import setup, find_packages  # Always prefer setuptools over distutils
from codecs import open  # To use a consistent encoding
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='asgard-counts-ingestor',
    version='0.1.0',
    description="Coletor de estatísticas de logs das aplicações",
    long_description="Coletor de estatísticas de logs das aplicações",
    url='https://github.com/B2W-BIT/asgard-counts-ingestor',
    # Author details
    author='Dalton Barreto',
    author_email='daltonmatos@gmail.com',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ],
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires = [
        "async-worker>=0.1.0-rc3",
        "simple-json-logger==0.2.3",
    ],
    entry_points={},
)
