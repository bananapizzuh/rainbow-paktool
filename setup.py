from setuptools import setup, find_packages

setup(
    name='paklib',
    version='1.0.0',
    description='PAK Compiler and Decompiler Library',
    author='bananapizzuh',
    license='MIT',
    packages=find_packages(exclude=['paklib.cli']),
    install_requires=[
        'rich-click',
    ],
    entry_points='''
        [console_scripts]
        pak-cli=paklib.cli:cli
    ''',
)
