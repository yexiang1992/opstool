.. _quickstart:

Quick Start
=============

Introduction to opstool
------------------------

**opstool** is a powerful and user-friendly library designed to simplify and enhance structural analysis workflows 
with **OpenSees** and **OpenSeesPy**. 
It provides advanced tools for preprocessing, postprocessing, and visualization, making structural 
simulations more efficient and accessible.

Quick Guide
---------------------------

.. toctree::
   :maxdepth: 1
   :caption: Quick Start

   examples/post/Frame2D/test_model.ipynb
   src/quick_start/plot_model.ipynb


Other Features
---------------

1. **Preprocessing Tools**:
   
   - *Fiber Section Meshing*: Generate detailed fiber meshes for various geometries. An example is shown below:
     `Fiber Section Mesh <src/pre/sec_mesh.ipynb>`_
   - *GMSH Integration*: Import and convert `Gmsh <https://gmsh.info/>`__ models, including geometry, mesh, and physical groups.
     An example is shown below: `Converting GMSH to OpenSeesPy <src/pre/read_gmsh.ipynb>`_
   - *Unit System Management*: Ensure consistency with automatic unit conversions.
     An example is shown below: `Automatic Unit Conversion <src/pre/unit_system.rst>`_
   - *Mass Generation*: Automate lumped mass calculations.
     An example is shown below: `Model mass generation <src/pre/model_mass.ipynb>`_
   - *Load Transformation*: Simplify the application of loads.
     An example is shown below: `Load Transformation <src/pre/loads.ipynb>`_
   - *Tcl script to OpenSeesPy*: Convert Tcl scripts to OpenSeesPy scripts.
     An example is shown below: `Tcl to OpenSeesPy <src/pre/tcl2py.rst>`_


2. **Postprocessing Capabilities**:
   
   - Easy retrieval and interpretation of analysis results using `xarray <https://docs.xarray.dev/en/stable/index.html#>`__.
     An example is shown below: `Postprocessing with xarray <src/post/index.ipynb>`_

3. **Visualization**:
   
   - Powered by `PyVista <https://docs.pyvista.org/>`__ (VTK-based) and `Plotly <https://plotly.com/python/>`__ (web-based).
   - Nearly identical APIs for flexible visualization of model geometry, modal analysis, and simulation results.
   - Supports most common OpenSees elements.
   - An example is shown below: `Visualization <src/vis/index.ipynb>`_

4. **Intelligent Analysis**:
   
   - Features like automatic step size adjustment and algorithm switching to optimize simulation workflows.
     An example is shown below: `Intelligent Analysis <src/analysis/smart_analysis.rst>`_
   - Moment-Curvature Analysis: Generate moment-curvature curves for various sections.
     An example is shown below: `Moment-Curvature Analysis <src/analysis/mc_analysis.ipynb>`_

