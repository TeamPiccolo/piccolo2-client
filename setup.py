from setuptools import setup, find_packages

setup(
    name = "piccolo2-client",
    version = "0.1",
    namespace_packages = ['piccolo2'],
    packages = find_packages(),
    install_requires = [
        "piccolo2-common",
        "python-jsonrpc"
    ],
)
