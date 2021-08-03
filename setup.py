import setuptools
from pathlib import Path
from setuptools import find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = [line.strip() for line in open('requirements.txt')]
scripts = [str(f) for f in Path('./bin').glob('*.py')]

setuptools.setup(
    name="Mirri utils",  # Replace with your own username
    version=0.1,
    author="P.Ziarsolo",
    author_email="pziarsolo@gmail.com",
    description="A small library to help dealing with MIRRI data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pziarsolo/mirri_utils",
    packages=find_packages(),
    package_data={"mirri": ['data/ontobiotopes.csv']},
    # package_dir={"mirri.entities": "mirri.entities"
    #              "mirri.io.parsers": "mirri.io.parsers",
    #              "mirri.io.writers": "mirri.io.writers",
    #              'mirri.validation': 'mirri.vallidation'},
    install_requires=requirements,
    scripts=scripts,
    license="GNU General Public License v3.0",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
