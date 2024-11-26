Automatic Unit Conversion
===========================

As we all know, the units should be unified in the finite element analysis.
Common basic units include ``length``, ``force``, and ``time``.
The units of the base system can be combined in any combination, but other units
including ``pressure``, ``stress``, ``mass``, etc.
should be unified with base system.
In order to facilitate unit processing in the model, ``opstool`` has developed a class that
can automatically perform unit conversion based on the basic units you set. 

For details of the parameters see :func:`opstool.pre.UnitSystem`.

.. jupyter-execute::

    import numpy as np
    import matplotlib.pyplot as plt
    import openseespy.opensees as ops
    import opstool as opst

    length_unit = "m"  # base unit
    force_unit = "kN"  # base unit

    UNIT = opst.pre.UnitSystem(length=length_unit, force=force_unit)

    print("Length:", UNIT.mm, UNIT.mm2, UNIT.cm, UNIT.m, UNIT.inch, UNIT.ft)
    print("Force", UNIT.N, UNIT.kN, UNIT.lbf, UNIT.kip)
    print("Stress", UNIT.MPa, UNIT.kPa, UNIT.Pa, UNIT.psi, UNIT.ksi)
    print("Mass", UNIT.g, UNIT.kg, UNIT.ton, UNIT.slug)
    # print(UNIT)

These other units will be automatically converted to the base units you have set!

Truss example
----------------

Let's look at a truss example.
You can set the practical values of structural parameters in the model,
and :func:`~opstool.pre.UnitSystem` will help you automatically convert to the base unit system you specify.

.. jupyter-execute::

    def model(UNIT):
        ops.wipe()
        ops.model('basic', '-ndm', 2, '-ndf', 2)
        # create nodes
        ops.node(1, 0, 0)
        ops.node(2, 144.0 * UNIT.cm,  0)
        ops.node(3, 2.0 * UNIT.m,  0)
        ops.node(4,  80. * UNIT.cm, 96.0 * UNIT.cm)
        ops.mass(4, 100 * UNIT.kg, 100 * UNIT.kg)
        # set boundary condition
        ops.fix(1, 1, 1)
        ops.fix(2, 1, 1)
        ops.fix(3, 1, 1)
        # define materials
        ops.uniaxialMaterial("Elastic", 1, 3000.0 * UNIT.N / UNIT.cm2)
        # define elements
        ops.element("Truss", 1, 1, 4, 100.0 * UNIT.cm2, 1)
        ops.element("Truss", 2, 2, 4, 50.0 * UNIT.cm2, 1)
        ops.element("Truss", 3, 3, 4, 50.0 * UNIT.cm2, 1)
        # eigen
        omega = np.sqrt(ops.eigen('-fullGenLapack', 2))
        f = omega / (2 * np.pi)
        # create TimeSeries
        ops.timeSeries("Linear", 1)
        ops.pattern("Plain", 1, 1)
        ops.load(4, 10.0 * UNIT.kN, -5.0 * UNIT.kN)

        # ------------------------------
        # Start of analysis generation
        # ------------------------------
        ops.system("BandSPD")
        ops.numberer("RCM")
        ops.constraints("Plain")
        ops.integrator("LoadControl", 1.0 / 10)
        ops.algorithm("Linear")
        ops.analysis("Static")
        u = []
        forces = []
        for _ in range(10):
            ops.analyze(1)
            u.append(ops.nodeDisp(4))
            ops.reactions()
            forces.append(ops.nodeReaction(2))
        u = np.array(u)
        forces = np.array(forces)
        return u, forces, f

Results
----------------

Three Cases:

.. jupyter-execute::

    length_unit1 = "m"
    force_unit1 = "kN"
    UNIT1 = opst.pre.UnitSystem(length=length_unit1, force=force_unit1)
    u1, forces1, f1 = model(UNIT=UNIT1)

    length_unit2 = "cm"
    force_unit2 = "N"
    UNIT2 = opst.pre.UnitSystem(length=length_unit2, force=force_unit2)
    u2, forces2, f2 = model(UNIT=UNIT2)

    length_unit3 = "ft"
    force_unit3 = "lbf"
    UNIT3 = opst.pre.UnitSystem(length=length_unit3, force=force_unit3)
    u3, forces3, f3 = model(UNIT=UNIT3)

Let's verify it!

Structure Frequency
+++++++++++++++++++++

.. jupyter-execute::

    print("structure frequency 1:", f1)
    print("structure frequency 2:", f2)
    print("structure frequency 3:", f3)

The structural frequencies are consistent, it really has nothing to do with the unit system!

Node 4 Displacement
+++++++++++++++++++++

.. jupyter-execute::

    print("Dispalcement at node4:")

    # print("Dispalcement at node4 case 1:", u1, length_unit1)
    # print("Dispalcement at node4 case 2:", u2, length_unit2)
    # print("Dispalcement at node4 case 3:", u3, length_unit3)

    print(f"{length_unit2}/{length_unit1}")
    print(u2/u1)
    print(f"{length_unit3}/{length_unit1}")
    print(u3/u1)

Node 2 Reactions
+++++++++++++++++++++

.. jupyter-execute::

    print("Reaction at node2:")

    # print("Reaction at node2 case 1:", forces1, force_unit1)
    # print("Reaction at node2 case 2:", forces2, force_unit2)
    # print("Reaction at node2 case 3:", forces3, force_unit3)

    print(f"{force_unit2}/{force_unit1}")
    print(forces2/forces1)
    print(f"{force_unit3}/{force_unit1}")
    print(forces3/forces1)

The displacement and force values depend on the base unit system you set up, but they are proportional to each other.
Well, the rest is left to you to verify.

Remember that you are free to change the base unit system without rewriting the model code.