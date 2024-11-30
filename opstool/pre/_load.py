from typing import Union

import numpy as np
import openseespy.opensees as ops


def create_gravity_load(
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


gen_grav_load = create_gravity_load


def _construct_transform_matrix_beam(ele_tags):
    """
    Constructs the transformation matrix from the global coordinate system to the local coordinate system.

    Returns
    -------
    T : numpy.ndarray
        A 3x3 transformation matrix mapping global coordinates to local coordinates.
    ndim: int
        The dimensions of the model.
    """
    # Calculate the local coordinate axes
    ele_tags = np.atleast_1d(ele_tags)
    ele_tags = [int(tag) for tag in ele_tags]
    T = []
    ndim = 2
    for etag in ele_tags:
        ele_nodes = ops.eleNodes(etag)
        coords = ops.nodeCoord(ele_nodes[0])
        ndim_ = len(coords)
        if ndim_ > ndim:
            ndim = ndim_
        xaxis = ops.eleResponse(etag, "xaxis")
        yaxis = ops.eleResponse(etag, "yaxis")
        zaxis = ops.eleResponse(etag, "zaxis")
        T.append([xaxis, yaxis, zaxis])
    return np.array(T), ndim, ele_tags


def transform_beam_uniform_load(
        ele_tags: Union[int, list[int], tuple, np.ndarray[int]],
        wx: Union[float, list[float], np.ndarray[float]] = 0.0,
        wy: Union[float, list[float], np.ndarray[float]] = 0.0,
        wz: Union[float, list[float], np.ndarray[float]] = 0.0,
) -> None:
    """
    Transforms a uniformly distributed beam load from the global coordinate system to the local coordinate system.

    Parameters
    -----------
    ele_tags : int, list, tuple, np.ndarray
        Beam element tags.
    wx : float, list, np.ndarray, default=0.0
        Uniformly distributed load in the `global X` direction.
        If a list or numpy array is provided, the length should be the same as the number of elements.
    wy : float, list, np.ndarray, default=0.0
        Uniformly distributed load in the `global Y` direction.
        If a list or numpy array is provided, the length should be the same as the number of elements.
    wz : float, list, np.ndarray, default=0.0
        Uniformly distributed load in the `global Z` direction.
        If a list or numpy array is provided, the length should be the same as the number of elements.

    Returns
    -------
    q_local : numpy.ndarray
        Uniformly distributed load in the local coordinate system [qx_local, qy_local, qz_local].
    """
    T, ndim, ele_tags = _construct_transform_matrix_beam(ele_tags)
    q_globals = np.atleast_2d(np.array([wx, wy, wz]))
    if q_globals.shape[0] == 1 and T.shape[0] > 1:
        q_globals = np.repeat(q_globals, T.shape[0], axis=0)
    q_locals = np.einsum('nij,nj->ni', T, q_globals)
    if ndim == 3:
        for qlocal, etag in zip(q_locals, ele_tags):
            qlocal = [float(q) for q in qlocal]
            ops.eleLoad("-ele", etag, "-type", "-beamUniform", qlocal[1], qlocal[2], qlocal[0])
    else:
        for qlocal, etag in zip(q_locals, ele_tags):
            qlocal = [float(q) for q in qlocal]
            ops.eleLoad("-ele", etag, "-type", "-beamUniform", qlocal[1], qlocal[0])


def transform_beam_point_load(
        ele_tags: Union[int, list[int], tuple, np.ndarray[int]],
        px: Union[float, list[float], np.ndarray[float]] = 0.0,
        py: Union[float, list[float], np.ndarray[float]] = 0.0,
        pz: Union[float, list[float], np.ndarray[float]] = 0.0,
        xl: Union[float, list[float], np.ndarray[float]] = 0.5
) -> None:
    """
    Transforms point loads for multiple beam elements from global to local coordinates.

    Parameters
    ----------
    ele_tags : int, list, tuple, np.ndarray
        Beam element tags.
    px : float, list, np.ndarray, default=0.0
        Point load in the `global X` direction.
        If a list or numpy array is provided, the length should be the same as the number of elements.
    py : float, list, np.ndarray, default=0.0
        Point load in the `global Y` direction.
        If a list or numpy array is provided, the length should be the same as the number of elements.
    pz : float, list, np.ndarray, default=0.0
        Point load in the `global Z` direction.
        If a list or numpy array is provided, the length should be the same as the number of elements.
    xl : float, list, np.ndarray, default=0.5
        The position of the point load along the beam element in a local coord system.
        If a list or numpy array is provided, the length should be the same as the number of elements.
    """
    # Compute global positions of point loads
    T, ndim, ele_tags = _construct_transform_matrix_beam(ele_tags)
    p_globals = np.atleast_2d(np.array([px, py, pz]))
    if p_globals.shape[0] == 1 and T.shape[0] > 1:
        p_globals = np.repeat(p_globals, T.shape[0], axis=0)
    xls = np.atleast_2d(xl)
    if xls.shape[0] == 1 and T.shape[0] > 1:
        xls = np.repeat(xls, T.shape[0], axis=0)

    # Transform point loads and positions to local coordinates
    p_locals = np.einsum('nij,nj->ni', T, p_globals)

    if ndim == 3:
        for plocal, etag, xl in zip(p_locals, ele_tags, xls):
            plocal = [float(p) for p in plocal]
            ops.eleLoad("-ele", etag, "-type", "-beamPoint", plocal[1], plocal[2], xl[0], plocal[0])
    else:
        for plocal, etag, xl in zip(p_locals, ele_tags, xls):
            plocal = [float(p) for p in plocal]
            ops.eleLoad("-ele", etag, "-type", "-beamPoint", plocal[1], xl[0], plocal[0])