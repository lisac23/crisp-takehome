from setuptools import setup, find_packages

setup(
    name='process_csv',
    version='0.1.0',
    author='Lisa Cloutier',
    author_email='lisacloutier77@gmail.com',
    packages=find_packages(),
    license='LICENSE.txt',
    description='A package for CSV transformation.',
    long_description=open('README.md').read()
)