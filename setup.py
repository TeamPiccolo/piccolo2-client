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

    # metadata for upload to PyPI
    author = "Magnus Hagdorn, Alasdair MacArthur, Iain Robinson",
    description = "Part of the piccolo2 system. This package provides the client libraries",
    license = "GPL",
    url = "https://bitbucket.org/uoepiccolo/piccolo2-client",
)
