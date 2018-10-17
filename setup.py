from setuptools import setup

setup(
    name='kish',
    version='0.1',
    author='Philip W Fowler',
    packages=['kish'],
    package_data={'kish': ['../config/H37Rv.gbk']},
    install_requires=[
        "biopython >= 1.70",
        "gemucator>=1.0.0"
    ],
    scripts=["bin/kish-run.py"],
    license='MIT',
    long_description=open('README.md').read(),
)
