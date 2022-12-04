import numpy as np
import openseespy.opensees as ops


def gen_grav_load(ts_tag: int, pattern_tag: int,
                  direction: str = "Z",
                  factor: float = -9.81):
    """Applying the gravity loads.

    Notes
    -----
    The mass values are from ``nodeMass(nodeTag)`` command, i.e., ones set in ``mass()`` command.

    Parameters
    -----------
    ts_tag: int
        The timeSeries tag you must assign.
    pattern_tag: int
        The pattern tag you must assign.
    direction: str, default="Z"
        The gravity load direction.
    factor: float, default=-9.81
        The factor applied to the mass values, it should be the multiplication of gravitational acceleration
        and directional indicators, e.g., -9.81, where 9.81 is the gravitational acceleration
        and -1 indicates along the negative Z axis.
        Of course, it can be multiplied by an additional factor to account for additional constant loads,
        e.g., 1.05 * (-9.81).

    Returns
    --------
    None

    """
    direction = direction.upper()
    ops.timeSeries('Linear', int(ts_tag))
    ops.pattern('Plain', int(pattern_tag), int(ts_tag))
    node_tags = ops.getNodeTags()
    load_fact_6d = dict(Z=np.array([0.0, 0.0, factor, 0.0, 0.0, 0.0]),
                        Y=np.array([0.0, factor, 0.0, 0.0, 0.0, 0.0]),
                        X=np.array([factor, 0.0, 0.0, 0.0, 0.0, 0.0]),
                        )
    load_fact_3d = dict(Z=np.array([0.0, 0.0, factor]),
                        Y=np.array([0.0, factor, 0]),
                        X=np.array([factor, 0.0, 0.0]),
                        )
    load_fact_2d = dict(Y=np.array([0.0, factor]),
                        X=np.array([factor, 0.0]),
                        )
    load_fact_1d = dict(X=np.array([factor, 0.0]))
    load_fact = {6: load_fact_6d, 3: load_fact_3d,
                 2: load_fact_2d, 1: load_fact_1d}
    for nodetag in node_tags:
        mass = np.array(ops.nodeMass(nodetag))
        loadValues = mass * load_fact[len(mass)][direction]
        if np.sum(np.abs(loadValues)) > 1e-10:
            ops.load(nodetag, *loadValues)
