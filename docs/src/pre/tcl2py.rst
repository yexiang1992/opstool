Convert Tcl code to OpenSeesPy commands
============================================

For details of the parameters see :func:`opstool.pre.tcl2py`.

.. code-block:: python

    import opstool as opst

    opst.pre.tcl2py(input_file='mycode.tcl',
                output_file='mycode.py',
                prefix="ops")

.. tip::
    
    * This function supports ``Tcl`` syntax and will flatten your ``Tcl`` code, including ``loops``, ``judgments``, ``assignments``, ``proc``, etc.,

    * Do not use assignment statements for OpenSees commands, such as ``set ok [analyze 1]``, ``set lambdaN [eigen 10]``, 
      it will trigger an error! This is because **this function does not run the OpenSees command at all**.

    * If an encoding error is reported, please check the file and delete any special
      characters that exist, such as some Chinese characters that cannot be encoded.
