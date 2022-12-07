
OpenSeesPy Model Visualization
=================================

Currently, Module :mod:`opstool.vis` provides two major roles, OpenSeesPy model (including responses) visualization and 
fiber section (including responses) visualization. 
Before visualization, class :class:`~opstool.vis.GetFEMdata` is needed to get data from the current domain of OpenSeesPy. 
The class :class:`~opstool.vis.GetFEMdata` automatically generates the result files in the specified output directory, 
which is read automatically by the visualization class :class:`~opstool.vis.OpsVisPlotly`, :class:`~opstool.vis.OpsVisPyvista`,
and :class:`~opstool.vis.FiberSecVis`.

.. tip:: 
   The module :mod:`opstool.vis` provides two plotting engines to visualize the OpenSeesPy model, including ``plotly`` and ``pyvista``.
   The visualization classes are :class:`~opstool.vis.OpsVisPlotly` and :class:`~opstool.vis.OpsVisPyvista` respectively. 
   ``Plotly`` renders images based on the web, and ``pyvista`` is a python wrapper for the C++ visualization package ``VTK``. 
   In general, ``plotly`` renders a bit slower than ``pyvista``, but provides powerful interactivity. 
   The choice depends on your preference, but both have almost the same interface.

Here are some guidelines on model visualization and fiber section visualization.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   notebooks/mod_vis_plotly.ipynb
   notebooks/mod_vis_pyvista.ipynb
   notebooks/mod_vis_fibersec.ipynb

