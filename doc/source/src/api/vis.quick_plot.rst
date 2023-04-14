Fast model and eigenvalue visualization
-------------------------------------------------

``opstool`` provides functions ``plot_model`` and ``plot_eigen`` to quickly plot model and eigenmodes.

plot_model
+++++++++++

.. autofunction:: opstool.vis.plot_model

plot_eigen
+++++++++++

.. autofunction:: opstool.vis.plot_eigen

Example
++++++++

.. code-block:: python

    import openseespy.opensees as ops
    import opstool as opst

    # opst.load_ops_examples("ArchBridge")
    opst.load_ops_examples("CableStayedBridge")
    # opst.load_ops_examples("Dam")
    # opst.load_ops_examples("Frame3D")
    # load_ops_examples("Igloo")
    # load_ops_examples("Pier")
    # opst.load_ops_examples("SuspensionBridge")

    # ------------------------
    # or your model code here
    # ------------------------
    
    opst.plot_model(backend="pyvista")    # or backend="plotly"

.. image:: images/plot_model.png
   :align: center

.. code-block:: python

    opst.plot_eigen(mode_tags=[1, 12], backend="pyvista", subplots=True)   # or backend="plotly"

.. image:: images/plot_eigen.png
   :align: center
