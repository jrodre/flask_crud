from setuptools import setup, find_packages

setup(
    name='flask_crud',
    version='0.0.0.1',
    packages=['flask_crud'],
    # packages=find_packages(),
    description='Administra vistas con un enfoque diferente en flask.',
    long_description=open('README.md', encoding="utf-8").read(),
    # long_description=open('README.md').read(),
    author='Tu nombre',
    author_email='jodriz@example.com',
    url='https://github.com/jrodre/flask_crud.git',
    install_requires=[
    "Flask"
    ],
)
