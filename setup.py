from setuptools import setup, find_packages
import os
import sys

_here = os.path.abspath(os.path.dirname(__file__))

if sys.version_info[0] < 3:
    with open(os.path.join(_here, 'README.rst')) as f:
        long_description = f.read()
else:
    with open(os.path.join(_here, 'README.rst'), encoding='utf-8') as f:
        long_description = f.read()

version = {}
with open(os.path.join(_here, 'mode_notebook_assets', 'version.py')) as f:
    exec(f.read(), version)

setup(
    name='mode_notebook_assets',
    version=version['__version__'],
    description=('Convenience Classes for working with Notebooks in ModeAnalytics'),
    long_description=long_description,
    author='',
    author_email='',
    url='https://github.com/Shopify/mode-notebook-assets',
    license='MPL-2.0',
    packages=['mode_notebook_assets'],
#   install_requires=[
#       'dependency==1.2.3',
#   ],
#   scripts=['bin/a-script'],
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.6'
        ],
    )
