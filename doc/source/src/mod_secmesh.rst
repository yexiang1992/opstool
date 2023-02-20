⚡Fiber Section Mesh Generation⚡
==================================

The module :mod:`opstool.preprocessing` provides a series of classes and functions for fiber section mesh generation, 
based on ``shapely`` and ``sectionproperties``.
The pacakge ``sectionproperties`` utilizes finite element methods to calculate the geometric properties of sections, 
including single-material section and composite section.

Module :py:mod:`~opstool.preprocessing` provides two main classes :py:class:`~opstool.preprocessing.SecMesh` and :py:class:`~opstool.preprocessing.Rebars`, and some functions, including :py:func:`~opstool.preprocessing.offset`, :py:func:`~opstool.preprocessing.add_circle`, :py:func:`~opstool.preprocessing.add_polygon` and :py:func:`~opstool.preprocessing.add_material`, to help create fiber cross-section.

.. toctree::
   :maxdepth: 3
   :caption: Contents:

   notebooks/mod_secmesh.ipynb