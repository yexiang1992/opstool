
OpenSeesPy Visualization
===============================================

Currently, Module :mod:`opstool.vis` provides two major roles, OpenSeesPy model (including responses) visualization and 
fiber section (including responses) visualization. 
Before visualization, class :class:`~opstool.vis.GetFEMdata` is needed to get data from the current domain of OpenSeesPy. 
The class :class:`~opstool.vis.GetFEMdata` automatically generates the result files in the specified output directory, 
which is read automatically by the visualization class :class:`~opstool.vis.OpsVisPlotly` and :class:`~opstool.vis.FiberSecVis`.

.. note:: The module :mod:`opstool.vis` expects to provide two plotting engines to visualize the OpenSeesPy model, including ``plotly`` and ``pyvista``. Currently, only ``plotly`` is supported. ``pyvista`` will be introduced in a future release. For now, ``plotly`` is preferred for its superior interactivity, but at the expense of speed.



.. toctree::
   :maxdepth: 2
   :caption: Contents:

   notebooks/mod_vis_plotly.ipynb
   notebooks/mod_vis_fibersec.ipynb

