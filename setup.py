from setuptools import setup, find_packages


setup(
    name='namestudio',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        "requests==2.22.0",
    ],
    setup_requires=[
        "pytest-runner",
    ],
    tests_require=[
        "pytest==5.3.4",
    ],
)
