from __future__ import annotations

import setuptools


def read_multiline_as_list(file_path: str) -> list[str]:
    with open(file_path) as fh:
        contents = fh.read().split("\n")
        if contents[-1] == "":
            contents.pop()
        return contents


with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = read_multiline_as_list("requirements.txt")
# requirements_dev = read_multiline_as_list("requirements-dev.txt")

setuptools.setup(
    name="persistent-cache",
    version="0.1",
    author="TeiaLabs",
    author_email="nei@teialabs.com",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TeiaLabs/persistent-cache/",
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    # classifiers=classifiers,
    keywords="",
    entry_points={},
    python_requires=">=3.8, <=3.10",
    install_requires=requirements,
    extras_require={
        # "dev": requirements_dev,
    },
)
