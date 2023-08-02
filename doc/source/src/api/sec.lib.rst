Section Library
------------------

.. autoclass:: opstool.preprocessing.section_library
   :members:
   :inherited-members:

Example
++++++++

.. jupyter-execute::

    import opstool as opst

    sec_lib = opst.section_library
    sec = sec_lib.octagonal_box_section(
        h=2, b=3, aa=0.3, bb=0.3, tw=0.3, tf1=0.2, tf2=0.25
    )
    sec.view(engine="mpl")
    print(sec.get_frame_props())

.. jupyter-execute::

    import opstool as opst

    sec_lib = opst.section_library
    sec = sec_lib.box_section(
        h=3, b1=2, b2=3, tw=0.3, tf1=0.2, tf2=0.25
    )
    sec.view(engine="mpl")
    print(sec.get_frame_props())