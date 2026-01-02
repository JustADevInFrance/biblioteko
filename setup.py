from setuptools import setup, find_packages

setup(
    name="app",
    version="0.1",
    package_dir={"": "src"},
    packages=find_packages("src"),
    install_requires=[
        "pyramid",
        "pyramid_chameleon",
        "sqlalchemy",
        "waitress",
        "passlib",
    ],
)
