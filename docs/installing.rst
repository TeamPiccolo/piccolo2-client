**********
Installing
**********

The Piccolo includes a Raspberry Pi which runs *Piccolo Server*. This software controls the Piccolo's hardware (spectrometers, shutters, ...), handles the recording of data, and provides an application programming interface that can be used to control the Piccolo. The Piccolo is usually remotely-controlled from a laptop via a network or radio link.

The Piccolo software is installed on the memory card of the Raspberry Pi that is included with the Piccolo. These instructions are therefore not required for a new instrument. The procedure described here can be used to install the software on a new memory card.

========
Raspbian
========

The Raspberry Pi is a miniature computer which runs an operating system, *Raspbian*, which is a variant of Linux.

*Raspbian* can be obtained from the `downloads page <https://www.raspberrypi.org/downloads>`_ at the `Raspberry Pi Foundation <https://www.raspberrypi.org/>`_. At the time of writing, the latest version is *Raspbian Jessie*, released on 18th March 2016. (*Raspbian Jessie Lite* has not been tested with the Piccolo.)

Download the zip (or Torrent) file and follow `their instructions <https://www.raspberrypi.org/documentation/installation/installing-images/README.md>`_ instructions to image it onto a memory (SD) card.

==============
Python version
==============

The Piccolo software is written for Python 2.7.

==================
Network connection
==================

To install the required software the Raspberry Pi must be connected to the Internet so that it can download software and updates. There are some `notes on Bitbucket <https://bitbucket.org/itrobinson/piccolo/wiki/Setting%20up%20a%20wired%20%28Ethernet%29%20connection%20to%20the%20Piccolo>`_ about how to set up the network connection.

To test the network connection, type::

  ping www.google.com

==========================
Run the configuration tool
==========================

This step is optional, but recommended.

Use the `Raspberry Pi configuration tool <https://www.raspberrypi.org/documentation/configuration/raspi-config.md>`_ to perform these actions:

* Expand the filesystem
* Change the user password
* Disable boot to desktop

Select ``Expand Filesystem``.

Select ``Change User Password`` and enter a new password. The default password is ``raspberry``, but this may be insecure if the Raspberry Pi is connected to a network.

Select ``Boot Options`` and then ``Console Autologin``.

Select any other custom configuration required.

Select ``Finish``. When asked ``Would you like to reboot now?``` answer ``Yes``.

=============================
Check packages are up to date
=============================

The ``apt-get`` tool allows software to be installed onto the Raspberry Pi directly from its internet connection. To do this it maintains a local package list which needs occasionally to be updated. Type::

  sudo apt-get update

Enter the password when prompted. (If the The Raspberry Pi password was not changed in the previous step, it will still be ``raspberry``.)

=================
Install Mercurial
=================

This step is optional.

*Mercurial* is a source code management tool. It is useful to developers of the Piccolo software to quickly upload and download source code from `Bitbucket <http://bitbucket.org/>`_, the web site which holds the development version of the software.

To install Mercurial type::

 sudo apt-get install mercurial

If asked ``Do you want to continue? [Y/n]`` answer ``Y`` for yes.

============================
Install Piccolo common files
============================

*Piccolo Common* contains the specification of the *Pico* file format used by the Piccolo.

Copy the ``piccolo2-common`` files onto the Raspberry Pi and type::

 cd piccolo2-common
 sudo python setup.py install

The files are installed in ``/usr/local/lib/python2.7/dist-packages/piccolo2_common-0.1-py2.7.egg``.

==============
Install psutil
==============

The *psutil* Python module is required by Piccolo Server for monitoring. Type::

  sudo apt-get install python-psutil

This module must be installed with ``apt-get``.

=================
Install configobj
=================

*ConfigObj* is a Python module for reading configuration files, more often known as *ini* files on Windows systems. It is required by the Piccolo software to read the *server configuration file*. To install it type::

  sudo apt-get install python-configobj

=================
Install pyjsonrpc
=================

Type::

  sudo pip install python-jsonrpc

To test the installation::

  python
  import pyjsonrpc
  quit()

======================
Install Piccolo Server
======================

Copy the ``piccolo-server`` files onto the Raspberry Pi.

Type::

  cd piccolo-server
  sudo python setup.py install

This will use the Raspberry Pi's internet connection to download and install a number of Python modules.

If the following error mesage occurs::

  warning: no previously-included files matching '*' found under directory 'docs/_build'
  psutil/_psutil_linux.c:12:20: fatal error: Python.h: No such file or directory
  #include <Python.h>
                     ^
  compilation terminated.
  error: Setup script exited with error: command 'arm-linux-gnueabihf-gcc' failed with exit status 1

then go back to the previous step and ensure that ``psutil`` is installed.

As well as installing *Piccolo Server* a number of Python modules are downloaded form the internet and installed on the Raspberry Pi. These modules are used by *Piccolo Server*.

*CherryPy* is a small web framework for Python. It allows the Piccolo software to use an application programming interface based on popular and standard protocols designed for the world-wide web.

*docutils* is text processing system used that is commonly used to help with the preparation of documentation for Python modules.

*lockfile* handles file locking.

*pbr* is part of a tool for setting up and install Python modules.

*python-daemon* is used to create services which run in the background.

Most of the files are installed in the directory ``/usr/local/lib/python2.7/dist-packages/``.

==================
Run Piccolo server
==================

Before starting Piccolo server it is important to be in the correct directory so that it can find the configuration file. Type::

  cd /home/pi/piccolo2-server
  python piccolo2/pserver.py

Attempting to run ``pserver.py`` from any other directory will produce an error message::

  RuntimeError: no such configuration file /home/pi/Piccolo/piccolo2-server/piccolo2/pdata/piccolo.config

A number of messages should appear, including::

  Serving on http://localhost:8080
  Bus STARTED

This final message indicates that *Piccolo Server* is running, and that the address to which commands should be sent is (the default)::

  http://localhost:8080
