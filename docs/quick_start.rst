.. _quickstart:

Quick Start
=============

Introduction to opstool
------------------------

**opstool** is a powerful and user-friendly library designed to simplify and enhance structural analysis workflows 
with **OpenSees** and **OpenSeesPy**. 
It provides advanced tools for preprocessing, postprocessing, and visualization, making structural 
simulations more efficient and accessible.

**Key Features:**

1. **Preprocessing Tools**:
   
   - *Fiber Section Meshing*: Generate detailed fiber meshes for various geometries.
   - *GMSH Integration*: Import and convert `Gmsh <https://gmsh.info/>`__ models, including geometry, mesh, and physical groups.
   - *Unit System Management*: Ensure consistency with automatic unit conversions.
   - *Mass Generation*: Automate lumped mass calculations.


2. **Postprocessing Capabilities**:
   
   - Easy retrieval and interpretation of analysis results using `xarray <https://docs.xarray.dev/en/stable/index.html#>`__.

3. **Visualization**:
   
   - Powered by `PyVista <https://docs.pyvista.org/>`__ (VTK-based) and `Plotly <https://plotly.com/python/>`__ (web-based).
   - Nearly identical APIs for flexible visualization of model geometry, modal analysis, and simulation results.
   - Supports most common OpenSees elements.

4. **Intelligent Analysis**:
   
   - Features like automatic step size adjustment and algorithm switching to optimize simulation workflows.
   - Moment-Curvature Analysis: Generate moment-curvature curves for various sections.


**Why Choose opstool?**

- **Efficiency**: Streamlines complex workflows, reducing time spent on repetitive tasks.
- **Flexibility**: Provides nearly identical interfaces for different visualization engines.
- **Accessibility**: Makes advanced structural analysis tools like OpenSeesPy more approachable to users of all levels.

``opstool`` is actively evolving, with continuous additions of new features planned for the future.
With ``opstool``, you can focus on what matters most: 
understanding and solving your structural engineering challenges. 
Whether you are building models, visualizing results, or interpreting data, 
``opstool`` is your go-to solution for OpenSeesPy workflows.


Quick Visualization Guide
---------------------------

Below is a quick guide to getting started with visualization in opstool:

`Quick Model and Eigen Visualization <src/quick_start/plot_model.ipynb>`_.