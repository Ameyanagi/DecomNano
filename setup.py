#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = [
    "Click>=7.0",
    "wolframclient",
    "pandas",
    "numpy",
    "toml",
    "tqdm",
]

test_requirements = [
    "pytest>=3",
]

setup(
    author="Ryuichi Shimogawa",
    author_email="ryuichi.shimogawa@stonybrook.edu",
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    description="Heterogeneity analysis of bimetallic nanoparticles using coordination numbers obtained from XAS analysis.",
    entry_points={
        "console_scripts": [
            "decomnano=decomnano.cli:main",
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="decomnano",
    name="decomnano",
    packages=find_packages(include=["decomnano", "decomnano.*"]),
    package_data={"": ["*.wl"]},
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/Ameyanagi/decomnano",
    version="0.1.0",
    zip_safe=False,
)
