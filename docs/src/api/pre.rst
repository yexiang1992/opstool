Preprocessing
===============

Tcl to Python
---------------

.. autofunction:: opstool.pre.tcl2py

Remove void nodes
---------------------

.. autofunction:: opstool.pre.remove_void_nodes

Generate gravity load
--------------------------

.. autofunction:: opstool.pre.gen_grav_load

Transform beam uniform and point load from global to local coordinate system
-------------------------------------------------------------------------------

.. autofunction:: opstool.pre.transform_beam_uniform_load

.. autofunction:: opstool.pre.transform_beam_point_load

Transform surface uniform load from local to global coordinate system
-----------------------------------------------------------------------

.. autofunction:: opstool.pre.transform_surface_uniform_load

Model Mass 
-----------

.. autoclass:: opstool.pre.ModelMass
   :members:
   :inherited-members:

Gmsh to OpenSeesPy
--------------------

.. autoclass:: opstool.pre.Gmsh2OPS
   :members:
   :inherited-members:

Unit System
-------------

.. autoclass:: opstool.pre.UnitSystem
   :members:
   :inherited-members: