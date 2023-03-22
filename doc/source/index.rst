.. opstool documentation master file, created by
   sphinx-quickstart on Fri Dec  2 02:37:37 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to opstool's documentation!
===================================

``opstool`` is a useful toolbox package aims to *modelling*, *visualization*, *post-processing*, etc., for `openseespy <https://openseespydoc.readthedocs.io/en/latest/>`_. 
The package is still under development.

To use, install `opstool` from 
`opstool-PyPI <https://pypi.org/project/opstool/>`_:

.. code-block:: console

   pip install --upgrade opstool

Python 3.9 is required for windows.
It is recommended that you use `Anaconda <https://www.anaconda.com/>`_ to avoid library version incompatibilities.

.. toctree::
   :maxdepth: 5
   :caption: Installation

   src/installation
   CHANGELOG

.. toctree::
   :maxdepth: 5
   :caption: Visualization

   src/mod_vis

.. toctree::
   :maxdepth: 5
   :caption: Fiber Section Mesh

   src/mod_secmesh

.. toctree::
   :maxdepth: 5
   :caption: Pre-processing

   src/tcl2py

.. toctree::
   :maxdepth: 5
   :caption: Analysis

   src/smart_analysis

.. toctree::
   :maxdepth: 5
   :caption: Demos

   src/demos

.. toctree::
   :maxdepth: 5
   :caption: API Reference

   src/opstool

