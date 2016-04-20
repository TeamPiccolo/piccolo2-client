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

Select ``Change User Password`` and enter a new password. The default password is `raspberry`, but this may be insecure if the Raspberry Pi is connected to a network.

Select ``Boot Options`` and then ``Console Autologin``.

Select any other custom configuration required.

Select ``Finish``. When asked ``Would you like to reboot now?``` answer ``Yes``.

=============================
Check packages are up to date
=============================

Type::

  sudo apt-get update

Enter the password when prompted.

=================
Install Mercurial
=================

This step is optional.

*Mercurial* is a source code management tool. It is useful to developers of the Piccolo software to quickly upload and download source code from Bitbucket.

To install Mercurial type::

 sudo apt-get install mercurial

============================
Install Piccolo common files
============================

*Piccolo Common* contains on the specification of the *Pico* file format used by the Piccolo.

Copy the `piccolo-common` files onto the Raspberry Pi and type::

 cd piccolo-common
 sudo python setup.py install

The files are installed in ``/usr/local/lib/python2.7/dist-packages/piccolo2_common-0.1-py2.7.egg``.

======================
Install Piccolo Server
======================

The *psutil* Python module is required by Piccolo Server for monitoring. Type::

  sudo apt-get install python-psutil

(**Note**: *psutil* cannot be installed on Ubuntu with *pip*. It reports that a file called *Python.h* is missing.)

Type::

 cd piccolo-server
 sudo python setup.py install

This will use the Raspberry Pi's internet connection to download and install a number of Python modules.

*CherryPy* is a small web framework for Python. It allows the Piccolo software to use an application programming interface based on popular and standard protocols designed for the world-wide web.

*ConfigObj* is a Python module for reading configuration files, more often known as *ini* files on Windows systems. It is required by the Piccolo software to read the *server configuration file*.

Some other modules installed include:

* docutils
* lockfile
* pbr
* python-daemon

==================
Run Piccolo server
==================

There are a number of different ways to start *Piccolo server*. If *Piccolo server* is not already started, it can run from a terminal by typing::

  python pserver.py

This should produce the error message::

  no such configuration file

===========================
Create a configuraiton file
===========================

The default configuration file can be found in this location::

  /home/pi/piccolo2-server/pdata/piccolo.config

The shutter channels upwelling and downwelling must be defined. (Channel names should be case insensitive, so upwelling and Upwelling refer to the same channel.)

=========================================
Add *Piccolo Server* to the *Python path*
=========================================

This step should be unnecessary, unless Python cannot find modules. Type::

  export PYTHONPATH=/home/pi/piccolo/piccolo_server

==============
Piccolo Server
==============

Once the configuration file is in place, Piccolo server can be started. The Piccolo server script can only be run from the ``piccolo2-server`` directory::

  cd /home/pi/piccolo2-server

Then type::

  python piccolo2/piccolo-server.py

If ``piccolo2-server.py`` is run from the wrong directory it will be unable to find the configuration file.

A number of messages should appear, including::

  Serving on http://localhost:8080
  Bus STARTED

This final message indicates that *Piccolo Server* is running, and that the address to which commands should be sent is (the default)::

  http://localhost:8080
