from setuptools import find_packages, setup

setup(
    name="oura_api",
    version="0.1.0",
    packages=find_packages(
        where=".",
        include=["oura_api"],
    ),
)
