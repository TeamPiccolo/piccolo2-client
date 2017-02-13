# Copyright 2014-2016 The Piccolo Team
#
# This file is part of piccolo2-client.
#
# piccolo2-client is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# piccolo2-client is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with piccolo2-client.  If not, see <http://www.gnu.org/licenses/>.

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
    entry_points={
        'console_scripts': [
            'piccolo2-record = piccolo2.precord:main',
        ],
    },

    # metadata for upload to PyPI
    author = "Magnus Hagdorn, Alasdair MacArthur, Iain Robinson",
    description = "Part of the piccolo2 system. This package provides the client libraries",
    license = "GPL",
    url = "https://bitbucket.org/uoepiccolo/piccolo2-client",
)
