from setuptools import setup, find_packages
from pathlib import Path


# get current directory
current_directory = Path(__file__).resolve().parent


def get_long_description():
    """
    get long description from README.rst file
    """
    with current_directory.joinpath("README.rst").open() as f:
        return f.read()


setup(
    name="dltreader",
    version="0.0.1",
    description="DLT reader for AUTOSAR Diagnostic, Log and Trace Protocol.",
    long_description=get_long_description(),
    url="https://github.com/keans/dlt",
    author="Ansgar Kellner",
    author_email="keans@gmx.de",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.6",
    keywords="dlt",
    packages=find_packages(
        exclude=["contrib", "docs", "tests"]
    ),
    install_requires=[],
    extra_require={
        "docs": ["mkdocs"],
    }
)
