Arbitrary Unit Conversion
---------------------------

.. autoclass:: opstool.preprocessing.UnitSystem
   :members:
   :inherited-members:


Example
++++++++

.. jupyter-execute::

    import opstool as opst

    UNIT = opst.UnitSystem(length="mm", force="N")
    print(UNIT.m, UNIT.cm, UNIT.inch, UNIT.cm3)
    print(UNIT.kN, UNIT.lb)
    print(UNIT.KPa, UNIT.MPa, UNIT.GPa, UNIT.ksi)
    print(UNIT)

.. jupyter-execute::

    UNIT = opst.UnitSystem(length="m", force="kN")
    print(UNIT)

.. jupyter-execute::

    UNIT = opst.UnitSystem(length="ft", force="lb")
    print(UNIT)