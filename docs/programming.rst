***********
Programming
***********

The Piccolo has an application programming interface (API).

The API uses `CherryPy <http://www.cherrypy.org/>`_.

=============
Spectrometers
=============

Spectrometers have a name that is based on their serial numbers.

========
Channels
========

The Piccolo is a dual-field-of-view spectrometer system and therefore has two (or possibly more) light inputs. These are referred to as *channels* and in most configurations there are two channels defined:

* upwelling
* downwelling

Channel names may be case sensitive.

==========
Dispatcher
==========

The dispatcher is a Python object (class name ``PiccoloDispatcher``) that receives instructions from the laptop or other sources and passes them on the instruments. There can only be one dispatcher running at any one time. It is possible to run the dispatcher in a background thread.

A class diagram for ``PiccoloDispatcher`` is shown below. As ``PiccoloDispatcher`` is designed to be run in the background as a separate thread, it inherits from Python's built-in ``Thread`` class from the ``threading`` module.

.. image:: images/class-diagrams/PiccoloDispatcher.png

The dispatcher by itself does not handle any hardware. Instead a number of *components* must be registered with it before they can be used. In principle any components can be registered with the dispatcher. Below is an example of the:

#. An upwelling shutter
#. A downwelling shutter
#. An Ocean Optics USB2000+ spectrometer
#. The Piccolo Component
#. The Controller

==========
Controller
==========

The controller contains:

#. The data directory
#. shutters
#. spectrometers

The interface to the data directory is provided by an object of class ``PiccoloDataDir``.

The controller receives instructions and puts them into a queue.

A subclass of ``PiccoloController`` is ``PiccoloControllerCherryPy`` which provides an interface for Remote Procedure Calls (RPC) written in Javascript Object Notation (JSON). This provides a web-like API for the Piccolo.

=========
Scheduler
=========

In logging applications it is required to acquire data at defined times. The scheduler provides an object to do this. Items (jobs) can be added to the scheduler with a specified start time.

===================
Starting the server
===================

Starting *Piccolo Server* goes through the following setup steps:

#. Reads the *server configuration file*.
#. Sets up a log file.
#. Creates the *data directory*.
#. Initializes (but doesn't start) the dispatcher.
#. Reads the *instrument configuration file*.
#. Initializes the shutters.
#. Registers the shutters with the dispatcher.
#. Finds and initializes all (USB-connected) spectrometers, then registers them with the dispatcher.
#. Sets up the *Piccolo Component* and registers it with the dispatcher.
#. Initializes the controller and registers it with the dispatcher.
#. Starts the dispatcher.
#. Starts the *CherryPy* server with the conroller.
