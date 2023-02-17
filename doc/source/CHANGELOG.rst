Changelog
==========

v0.4.1
-------
- Fixed some bugs in the arg ``show_local_crd`` in :meth:`opstool.vis.OpsVisPyvista.model_vis` and :meth:`opstool.vis.OpsVisPlotly.model_vis`

v0.4.0
-------
- update vis module, add multi-point constraint plot

v0.3.0
--------
- Added the class :class:`opstool.analysis.SmartAnalyze`
- Added the functions :func:`opstool.preprocessing.var_line_string` and :func:`opstool.preprocessing.vis_var_sec`
  to create variable fiber cross-section meshes.

v0.2.0
--------
- Moved the fiber section mesh commands to :mod:`opstool.preprocessing.section`
- Updated docs
- Updated NineNodeQuad, SixNodeTri, TwentyNodeBrick, etc., element visualization.

v0.1.0
--------
- Added the function :func:`opstool.preprocessing.tcl2py` to convert tcl code to openseespy code
- Change the file that model data saved by :class:`opstool.vis.GetFEMdata` to ``hdf5`` style
- Added the arg ``stop_cond`` in :meth:`opstool.vis.GetFEMdata.get_node_resp_step`,
  :meth:`opstool.vis.GetFEMdata.get_frame_resp_step`, and :meth:`opstool.vis.GetFEMdata.get_fiber_resp_step`
- Added the arg ``save_file`` in various method of :class:`opstool.vis.GetFEMdata`.
- Added the arg ``input_file`` in various method of :class:`opstool.vis.OpsVisPlotly` and
  :class:`opstool.vis.OpsVisPyvista`
- Deleted the arg ``analysis_tag`` in :meth:`opstool.vis.GetFEMdata.get_node_resp_step`,
  :meth:`opstool.vis.GetFEMdata.get_frame_resp_step`, and :meth:`opstool.vis.GetFEMdata.get_fiber_resp_step`,
  and the method of :class:`opstool.vis.OpsVisPlotly` and :class:`opstool.vis.OpsVisPyvista`.
  You can assign the different analysis cases by ``save_file`` and ``input_file`` args
- Updated document

v0.0.7
--------
- Updated :meth:`opstool.vis.OpsVisPyvista.model_vis` parameter `show_local_crd`, show local x, y, z labels.
- Fixed the `on_notebook` parameter bug with :class:`opstool.vis.OpsVisPlotly`
- Updated document


v0.0.6
---------

- Added :class:`opstool.vis.OpsVisPyvista`
- Fixed a bug with frame element response visualization, :mod:`opstool.vis.OpsVisPlotly.frame_resp_vis`
- Updated document

v0.0.5
---------

- Initial release.