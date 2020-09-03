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
with open(os.path.join(_here, 'ModeNotebookAssets', 'version.py')) as f:
    exec(f.read(), version)

def list_subpackages(package_name):
    yield package_name

    root = os.path.dirname(os.path.realpath(__file__))

    parent_directory = os.path.join(root, *package_name.split('.'))

    for dir in os.listdir(parent_directory):
        path = os.path.join(parent_directory, dir)
        if os.path.isdir(path) and os.path.exists(os.path.join(path, '__init__.py')):
            for i in list_subpackages(package_name + '.' + dir):
                yield i

setup(
    name='ModeNotebookAssets',
    version=version['__version__'],
    description=('Convenience Classes for working with Notebooks in ModeAnalytics'),
    long_description=long_description,
    author='',
    author_email='',
    url='https://github.com/Shopify/mode-notebook-assets',
    license='MPL-2.0',
    packages=['ModeNotebookAssets', 'ModeNotebookAssets.bignum'],
    # packages=list(list_subpackages('ModeNotebookAssets')),
    # package_dir={'bignum': 'ModeNotebookAssets', 'ModeNotebookAssets': 'ModeNotebookAssets'},
    # packages=find_packages(include=["ModeNotebookAssets", "ModeNotebookAssets.bignum", "ModeNotebookAssets.table"]),
    # package_dir={'ModeNotebookAssets': 'ModeNotebookAssets', 'bignum': 'bignum', 'table': 'table'},
#   no dependencies in this example
#   install_requires=[
#       'dependency==1.2.3',
#   ],
#   no scripts in this example
#   scripts=['bin/a-script'],
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        # 'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6'],
    )
