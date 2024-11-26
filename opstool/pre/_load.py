import numpy as np
import openseespy.opensees as ops


def ele_load_from_global(ele_tags: list, load_type: str, load_args: list):
    if load_type == "beamUniform":
        if len(load_args) == 2:
            gx, gy, gz = load_args[0], load_args[1], 0.0
        elif len(load_args) == 3:
            gx, gy, gz = load_args

    elif load_type == "beamPoint":
        if len(load_args) == 3:
            gx, gy, gz, xl = load_args[0], load_args[1], 0.0, load_args[3]
        elif len(load_args) == 4:
            gx, gy, gz, xl = load_args


def gen_grav_load(
    exclude_nodes: list = None,
    direction: str = "Z",
    factor: float = -9.81,
):
    """Applying the gravity loads.

    .. Note::
        The mass values are from ``nodeMass(nodeTag)`` command, i.e., ones set in ``mass()`` command.

    Parameters
    -----------
    exclude_nodes: list, default=None
        Excluded node tags, whose masses will not be used to generate gravity loads.
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
    node_tags = ops.getNodeTags()
    if exclude_nodes is not None:
        node_tags = [tag for tag in node_tags if tag not in exclude_nodes]
    load_fact_6d = dict(
        Z=np.array([0.0, 0.0, factor, 0.0, 0.0, 0.0]),
        Y=np.array([0.0, factor, 0.0, 0.0, 0.0, 0.0]),
        X=np.array([factor, 0.0, 0.0, 0.0, 0.0, 0.0]),
    )
    load_fact_3d = dict(
        Z=np.array([0.0, 0.0, factor]),
        Y=np.array([0.0, factor, 0]),
        X=np.array([factor, 0.0, 0.0]),
    )
    load_fact_2d = dict(
        Y=np.array([0.0, factor]),
        X=np.array([factor, 0.0]),
    )
    load_fact_1d = dict(X=np.array([factor, 0.0]))
    load_fact = {6: load_fact_6d, 3: load_fact_3d, 2: load_fact_2d, 1: load_fact_1d}
    for nodetag in node_tags:
        mass = np.array(ops.nodeMass(nodetag))
        loadValues = mass * load_fact[len(mass)][direction]
        ops.load(nodetag, *loadValues)
