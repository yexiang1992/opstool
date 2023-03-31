Section Meshing
------------------

.. autoclass:: opstool.preprocessing.SecMesh
   :members:
   :inherited-members:

Example
++++++++

.. jupyter-execute::

    import opstool as opst

    outlines = [[0, 0], [2, 0], [2, 2], [0, 2]]
    obj = opst.add_polygon(outlines)
    sec = opst.SecMesh(sec_name='plain section')
    sec.assign_group(dict(sec=obj))
    sec.assign_mesh_size(dict(sec=0.1))
    sec.mesh()
    sec_props = sec.get_sec_props(display_results=True, plot_centroids=False)
    sec.centring()
    # sec.rotate(45)
    sec.view(fill=True, engine='matplotlib')