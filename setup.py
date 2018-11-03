from setuptools import setup, find_packages

setup(
    name='latextools',
    version='0.1',
    packages=find_packages(),
    url='https://github.com/joshua-laughner/Latextools',
    license='',
    author='Joshua Laughner',
    author_email='jllacct119@gmail.com',
    description='Various tools to automate certain tasks with Latex documents',
    entry_points={
        'console_scripts': ['latextools=latextools.ltools_main:main']
    }
)
