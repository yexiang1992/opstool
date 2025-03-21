Fiber Section Mesh
===================

Section mesh class
--------------------
This is a main class for creating fiber section triangular mesh.

.. autosummary::
   :toctree: _autosummary
   :template: custom-class-template.rst
   :recursive:

    opstool.pre.section.FiberSecMesh
    opstool.pre.section.SecMesh


Utility functions for creating geometry and materials
-------------------------------------------------------

.. autosummary::
   :toctree: _autosummary
   :template: custom-function-template.rst
   :recursive:

    opstool.pre.section.create_material
    opstool.pre.section.create_polygon_patch
    opstool.pre.section.create_circle_patch
    opstool.pre.section.create_patch_from_dxf
    opstool.pre.section.create_polygon_points
    opstool.pre.section.create_circle_points
    opstool.pre.section.offset
    opstool.pre.section.line_offset
    opstool.pre.section.poly_offset
    opstool.pre.section.set_patch_material
    opstool.pre.section.vis_fiber_sec_real


Wrapper for OpenSeesPy section commands
-------------------------------------------
The following commands wrap the fiber section-related commands in ``OpenSeesPy``. 
These commands retain the same functionality as the original commands but additionally save 
the user-provided input data for purposes such as visualization.

.. autosummary::
   :toctree: _autosummary
   :recursive:

    opstool.pre.section.section
    opstool.pre.section.fiber
    opstool.pre.section.patch
    opstool.pre.section.layer
    opstool.pre.section.plot_fiber_sec_cmds

Example
++++++++

.. jupyter-execute::

    import numpy as np
    import openseespy.opensees as ops
    import opstool as opst

    ops.wipe()
    ops.model("basic", "-ndm", 3, "-ndf", 6)
    ops.uniaxialMaterial("Elastic", 1, 1000)

The following commands, like those in 
`OpenSeesPy <https://openseespydoc.readthedocs.io/en/latest/src/fibersection.html>`_,
create objects in the domain.

.. jupyter-execute::

    sectag = 1
    opst.pre.section.section("Fiber", sectag, "-GJ", 1.0e6)
    opst.pre.section.patch("circ", 1, 40, 1, 0, 0, 1.9, 2, 0, 360, color="blue", opacity=0.75)
    opst.pre.section.patch("circ", 1, 40, 5, 0, 0, 1, 1.9, 0, 360, color="green", opacity=0.35)
    opst.pre.section.layer("circ", 1, 40, np.pi * 0.016**2, 0, 0, 1.9 - 0.016, 0.0, 360.0, color="red")
    # plot
    opst.pre.section.plot_fiber_sec_cmds(sec_tag=1)

Let's look at another example.

.. jupyter-execute::

    sectag = 2
    opst.pre.section.section("Fiber", sectag, "-GJ", 1.0e6)
    opst.pre.section.patch("quad", 1, 20, 20, -1, -1, 1, -1, 2, 3, -2, 3, color="blue", opacity=0.25)
    opst.pre.section.layer(
        "straight", 1, 20, np.pi * 0.02**2, *[-0.9, -0.9], *[1.9, 2.9], color="black"
    )
    opst.pre.section.fiber(0, 1, np.pi * 0.05**2, 1, color="red")
    # plot
    opst.pre.section.plot_fiber_sec_cmds(sec_tag=2)

