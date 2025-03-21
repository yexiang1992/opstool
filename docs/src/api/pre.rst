Preprocessing
===============

Fiber Section Mesh
--------------------

.. toctree::
   :maxdepth: 1

   pre.section.rst


Tcl to Python
---------------

.. autosummary::
   :toctree: _autosummary
   :template: custom-function-template.rst
   :recursive:
   
   opstool.pre.tcl2py

Remove void nodes
---------------------

.. autosummary::
   :toctree: _autosummary
   :template: custom-function-template.rst
   :recursive:
   
   opstool.pre.remove_void_nodes

Loads Transform and Processing
--------------------------------
.. autosummary::
   :toctree: _autosummary
   :template: custom-function-template.rst
   :recursive:
   
   opstool.pre.apply_load_distribution
   opstool.pre.gen_grav_load
   opstool.pre.transform_beam_uniform_load
   opstool.pre.transform_beam_point_load
   opstool.pre.transform_surface_uniform_load


Model Mass 
-----------

.. autosummary::
   :toctree: _autosummary
   :template: custom-class-template.rst
   :recursive:
   
   opstool.pre.ModelMass

Gmsh to OpenSeesPy
--------------------

.. autosummary::
   :toctree: _autosummary
   :template: custom-class-template.rst
   :recursive:
   
   opstool.pre.Gmsh2OPS

Unit System
-------------

.. autosummary::
   :toctree: _autosummary
   :template: custom-class-template.rst
   :recursive:
   
   opstool.pre.UnitSystem

Model Data
----------------

.. autosummary::
   :toctree: _autosummary
   :template: custom-function-template.rst
   :recursive:
   
   opstool.pre.get_node_coord
   opstool.pre.get_node_mass