Convert tcl code to OpenSeesPy commands
============================================

For details of the parameters see :func:`opstool.preprocessing.tcl2py`.

.. code-block:: python

    import opstool as opst

    opst.tcl2py(input_file='mycode.tcl',
                output_file='mycode.py',
                prefix="ops")

.. tip::
    * This function will flatten your `tcl` code, including loops, judgments, assignments, proc, etc.
    * Do not use assignment statements for openseens commands, such as ``set ok [analyze 1]``, ``set lambdaN [eigen 10]``, it will trigger an error!
    * It is recommended to remove `analysis related tcl code` and keep only commands such as model building and load definition to avoid possible exceptions. The `analysis-related python code` you can add manually, although this function provides the ability to convert the analysis tcl code.