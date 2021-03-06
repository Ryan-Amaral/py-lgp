from setuptools import setup

setup(
    name='py-lgp',
    version='0.3',
    packages=['lgp'],
    install_requires=['numba','numpy'],
    license='MIT',
    description='Python implementation of Linear Genetic Programming.',
    long_description=open('README.md').read(),
    author='Ryan Amaral',
    author_email='ryan_amaral@live.com',
    url='https://github.com/Ryan-Amaral/py-lgp')
