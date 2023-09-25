Changelog
=============

v0.8.5
--------------------
- Added the Arg ``show_local_crd_shell`` to display the local axes of shell elements.

v0.8.4
--------------------
- Fixed incorrect calculation of section properties caused by :py:meth:`opstool.preprocessing.SecMesh.centering`
- Added predefined section library :py:class:`opstool.preprocessing.section_library`
- Updated section mesh visualization

v0.8.3
--------------------
- Fixed bugs in show_ele_load in OpsVisPlotly

v0.8.0
--------------------

v0.7.3
--------------------
- Added the quick visualization functions :py:func:`opstool.vis.plot_model` and :py:func:`opstool.vis.plot_eigen`
- Updated class :class:`opstool.analysis.SmartAnalyze`
- Updated args `show_beam_sec` and `beam_sec_paras` in :py:meth:`opstool.vis.OpsVisPyvista.model_vis`.

v0.7.2
--------------------
- Added functions :py:func:`opstool.preprocessing.poly_offset` and :py:func:`opstool.preprocessing.line_offset`
- Fixed the bug in get mp_constraint dof data.
- Added beam section 3D rendering, by Arg `beam_sec` in :py:meth:`opstool.vis.GetFEMdata.get_model_data`,
  and Args `show_beam_sec` and `beam_sec_paras` in :py:meth:`opstool.vis.OpsVisPyvista.model_vis`.


v0.7.1
-------
- Fixed the bug in get mp_constraint data.

v0.7.0
-------
- Added the method :meth:`opstool.vis.GetFEMdata.save_resp_all` and :meth:`opstool.vis.GetFEMdata.get_resp_step`.
- Added the node reactions plot method :meth:`opstool.vis.OpsVisPyvista.react_vis` and :meth:`opstool.vis.OpsVisPlotly.react_vis`.
- Added the method :py:meth:`opstool.preprocessing.SecMesh.get_frame_props`.
- Added the method :py:meth:`opstool.preprocessing.SecMesh.get_stress`.
- Fixed the bug in the calculation of equivalent torsion constants for reference materials in composite sections,
  in :py:meth:`opstool.preprocessing.SecMesh.get_sec_props` and :py:meth:`opstool.preprocessing.SecMesh.get_frame_props`
- Updated the Fiber section visualization :func:`opstool.vis.plot_fiber_sec` and :class:`opstool.vis.FiberSecVis`.

v0.6.0
-------
- Added the unit conversion class :func:`opstool.preprocessing.UnitSystem`.
- Fixed bugs in :func:`opstool.preprocessing.tcl2py`.
- Added the arg `show_constrain_dof` in :meth:`opstool.vis.OpsVisPyvista.model_vis` and :meth:`opstool.vis.OpsVisPlotly.model_vis`.

v0.5.0
-------
- Added the function :func:`~opstool.vis.save_tikz` to save as the ``.tex`` file using `tikz` package, which can be visualized by native ``texlive`` or web-based ``overleaf``.
- Added the class :class:`opstool.analysis.MomentCurvature` to moment-curvature analysis of fiber section.

v0.4.2
-------
- Fixed som bugs in :func:`opstool.preprocessing.tcl2py`.
- Updated the version requirements for mac.

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