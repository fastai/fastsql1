from setuptools import setup, find_packages
import os

owner,name = 'jph00','fastsql'
exec(open(os.path.join(name, 'version.py')).read())
readme = open('README.md').read()

setup(description='A bit of extra usability for sqlalchemy',
      author='Jeremy Howard', author_email='info@fast.ai', license='Apache 2.0',
      url='http://github.com/'+owner+'/'+name,
      python_requires  = '>=3.6', install_requires = ['sqlalchemy', 'pandas'],
      long_description = readme, long_description_content_type = 'text/markdown',
      name=name, version=__version__, packages=find_packages(), zip_safe=False)

