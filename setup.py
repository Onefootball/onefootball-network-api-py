"""OneFootball Network API client package."""
import pathlib

from setuptools import find_packages, setup


def _read(fname: str) -> str:
    with open(pathlib.Path(fname)) as fh:
        data = fh.read()
    return data


base_packages = ["rich>=5.1.0", "pydantic==1.6.1", "requests==2.24.0", "lxml==4.5.2"]

dev_packages = [
    "jupyterlab>=0.35.4",
    "pytest>=4.0.2",
    "black>=19.3b0",
    "flake8>=3.6.0",
    "flake8-annotations==2.1.0",
    "flake8-bandit==2.1.2",
    "flake8-bugbear==20.1.4",
    "flake8-docstrings==1.5.0",
    "darglint==1.4.0",
    "pre-commit>=2.2.0",
    "mkdocs>=1.1",
    "mkdocs-material==4.6.3",
    "mkdocstrings>=0.11.0",
]

docs_packages = [
    "mkdocs",
    "mkdocs-material==4.6.3",
    "mkdocs-material-extensions==1.0b2",
    "mkdocs-git-revision-date-localized-plugin==0.5.0",
    "mkdocstrings",
]

setup(
    name="onefootball_network",
    version="0.1.0",
    packages=find_packages(exclude=["data", "docs", "notebooks"]),
    long_description=_read("readme.md"),
    install_requires=base_packages,
    extras_require={"dev": dev_packages, "docs": docs_packages},
)
