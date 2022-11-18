from setuptools import setup
import py2exe

setup(
    name='std_doc',
    version='1.0',
    console=['std_doc/docstring_writer.py'],
    url='https://github.com/tigsinthetrees/std_doc',
    license='MIT',
    author='Tigs Edmonds',
    author_email='tedmonds@protonmail.com',
    description='Utility for automatically creating the framework for documenting python modules'
)
