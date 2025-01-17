from typing import Union
from collections import defaultdict

import numpy as np
import openseespy.opensees as ops
import matplotlib.pyplot as plt


def apply_load_distribution(
    node_tags: Union[list, tuple, int] = None,
    coord_axis: str = "z",
    load_axis: str = "x",
    dist_type: str = "triangle",
    sum_normalized: bool = True,
    plot: bool = False,
):
    """
    Apply load distribution along specified coordinate axis.

    .. Note::
        The load is applied to the ``OpenSeesPy`` domain.
        If sum_normalized=True, The sum of the loads for all nodes is 1.0.
        If sum_normalized=False, The maximum load is set to 1.0.

    Parameters:
    -----------
    node_tags : list, tuple, int, optional
        The node tags where the load will be applied.
        If None, the function will apply the load to all nodes.
    coord_axis : str, default='z'
        The coordinate axis along which the load is distributed ('x', 'y', or 'z').
    load_axis : str, default='x'
        The load direction ('x', 'y', or 'z').
    dist_type : str, default='triangle'
        Type of distribution ('triangle', "parabola", 'half_parabola_concave', 'half_parabola_convex', 'uniform').
    sum_normalized : bool, default=True
        If True, the loads are normalized to ensure their sum is 1.0.
        If False, the maximum load is set to 1.0.
    plot : bool, optional
        If True, plots the load distribution graph.

    Returns:
    --------
    node_loads : dict
        A dictionary containing the node tags and the corresponding normalized loads.
    """
    if node_tags is None:
        node_tags = ops.getNodeTags()
    else:
        if isinstance(node_tags, int):
            node_tags = [node_tags]
    # Retrieve the coordinates of all nodes
    axis_index = {"x": 0, "y": 1, "z": 2}[coord_axis.lower()]
    node_coords = {node: ops.nodeCoord(node)[axis_index] for node in node_tags}
    node_coords = dict(sorted(node_coords.items(), key=lambda item: item[1]))
    min_coord = min(coords for coords in node_coords.values())
    node_coords = {node: coord - min_coord for node, coord in node_coords.items()}
    max_coord = max(coords for coords in node_coords.values())

    # Calculate the load for each node based on the specified distribution type
    coord_list = []
    load_list = []
    for node, coord in node_coords.items():
        if dist_type.lower() == "triangle":
            load = coord / max_coord
        elif dist_type.lower() == "parabola":
            load = (coord / max_coord) * (1 - coord / max_coord)
        elif dist_type.lower() == "half_parabola_concave":
            load = 4 * (coord / max_coord) ** 2
        elif dist_type.lower() == "half_parabola_convex":
            a = -1 / (max_coord**2)
            load = a * (coord - max_coord) ** 2 + 1
        elif dist_type.lower() == "uniform":
            load = 1
        else:
            raise ValueError(f"Invalid distribution type {dist_type}.")

        coord_list.append(coord + min_coord)
        load_list.append(load)

    # Normalize loads to ensure their sum is 1.0
    if sum_normalized:
        sum_loads = sum(load_list)
        normalized_load_list = [load / sum_loads for load in load_list]
    else:
        max_load = max(load_list)
        normalized_load_list = [load / max_load for load in load_list]
    normalized_load_dict = dict(zip(node_coords.keys(), normalized_load_list))

    # Apply normalized loads to the nodes
    for node, load in zip(node_coords, normalized_load_list):
        ndf = ops.getNDF(node)[0]
        if load_axis.lower() == "x":
            if ndf == 3:
                ops.load(node, load, 0, 0)
            elif ndf == 6:
                ops.load(node, load, 0, 0, 0, 0, 0)
        elif load_axis.lower() == "y":
            if ndf == 3:
                ops.load(node, 0, load, 0)
            elif ndf == 6:
                ops.load(node, 0, load, 0, 0, 0, 0)
        elif load_axis.lower() == "z":
            if ndf == 3:
                ops.load(node, 0, 0, load)
            elif ndf == 6:
                ops.load(node, 0, 0, load, 0, 0, 0)

    if plot:
        coord_color = "#2c6fbb"
        load_color = "#c0737a"
        plt.figure(figsize=(8, 5))
        max_load = max(normalized_load_list)
        aspect_ratio = max_load / max_coord
        plt.scatter(
            normalized_load_list,
            coord_list,
            color=load_color,
            zorder=100,
            label="Loads",
        )
        plt.plot(normalized_load_list, coord_list, load_color, zorder=10)
        plt.plot([0] * len(coord_list), coord_list, color=coord_color, zorder=10)
        plt.scatter([0] * len(coord_list), coord_list, color=coord_color, zorder=100)
        for coord, load in zip(coord_list, normalized_load_list):
            plt.plot([0, load], [coord, coord], load_color, zorder=10)
        plt.plot()
        plt.xlabel("p")
        plt.ylabel(f"{coord_axis}")
        # plt.title(f"Load Distribution: {distribution_type.capitalize()}")
        # plt.legend()
        plt.grid(True, zorder=-100)
        plt.gca().set_aspect(aspect_ratio * 5)

    return normalized_load_dict


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

    .. Note::
        This function will automatically call the
        `EleLoad Command <https://opensees.berkeley.edu/wiki/index.php/EleLoad_Command>`_ to generate element loads.
        However, you need to create ``timeSeries`` and load ``pattern`` objects externally in advance.
        The load generated by this function will belong to the load pattern closest to it.

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
    Transforms point loads for beam elements from global to local coordinates.

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


def transform_surface_uniform_load(
        ele_tags: Union[int, list[int], tuple, np.ndarray[int]],
        p: Union[float, list[float], np.ndarray[float]] = 0.0,
) -> None:
    """
    Converts uniform surface loads into equivalent nodal forces in the global coordinate system.
    According to the static equivalence principle, the distributed load is equivalent to the node load.

    .. Note::
        This function will automatically call the
        `NodalLoad Command <https://opensees.berkeley.edu/wiki/index.php?title=NodalLoad_Command>`_ to
        generate nodal loads.
        However, you need to create ``timeSeries`` and load ``pattern`` objects externally in advance.
        The load generated by this function will belong to the load pattern closest to it.

    Parameters
    ----------
    ele_tags : int, list, tuple, np.ndarray
        Surface element tags.
    p : float, list, np.ndarray, default=0.0
        Uniform surface load magnitude (per unit area) along the surface normal direction.
        The positive direction of the normal is obtained by the cross-product of the I-J and J-K edges.
        If a list or numpy array is provided, the length should be the same as the number of elements.
    """
    ele_tags = np.atleast_1d(ele_tags)
    ele_tags = [int(tag) for tag in ele_tags]
    if isinstance(p, (int, float)):
        uniform_loads = [p] * len(ele_tags)
    else:
        uniform_loads = p

    nodal_forces = defaultdict(lambda : np.zeros(3))
    nodal_dofs = dict()

    for etag, load in zip(ele_tags, uniform_loads):
        node_ids = ops.eleNodes(etag)
        vertices = np.array([ops.nodeCoord(node_id) for node_id in node_ids])
        # Compute area and normal based on an element type
        if len(node_ids) == 3:  # Triangle
            area, normal = _compute_tri_area_and_normal(vertices)
        elif len(node_ids) == 4:  # Quadrilateral
            area, normal = _compute_quad_area_and_normal(vertices)
        else:
            raise ValueError(f"Unsupported element type with {len(node_ids)} nodes.")
        # Compute total force on the element
        element_force = load * area * normal  # Total force vector in global coordinates
        # Distribute force to each node equally
        force_per_node = element_force / len(node_ids)

        # Accumulate forces to the global nodal forces dictionary
        for node_id in node_ids:
            nodal_forces[node_id] += force_per_node
            nodal_dofs[node_id] = ops.getNDF(node_id)[0]
    for key, value in nodal_forces.items():
        ndf = nodal_dofs[key]
        if ndf == 3:
            ops.load(key, *value)
        elif ndf == 6:
            ops.load(key, *value, 0, 0, 0)
        elif ndf == 2:
            ops.load(key, *value[:2])


def _compute_tri_area_and_normal(vertices):
    """
    Compute the area and normal vector of a triangular element.

    Parameters
    ----------
    vertices : numpy.ndarray
        Coordinates of the triangle's vertices, shape (3, 3).

    Returns
    -------
    area : float
        Area of the triangle.
    normal : numpy.ndarray
        Unit normal vector of the triangle, shape (3,).
    """
    # Edges: IJ and JK
    edge_ij = vertices[1] - vertices[0]
    edge_jk = vertices[2] - vertices[1]

    # Compute cross product
    cross_product = np.cross(edge_ij, edge_jk)
    norm = np.linalg.norm(cross_product)
    area = 0.5 * norm
    # Normalize the normal vector
    normal = cross_product / norm
    return area, normal


def _compute_quad_area_and_normal(vertices):
    """
    Compute the area and normal vector of a quadrilateral element.

    Parameters
    ----------
    vertices : numpy.ndarray
        Coordinates of the quadrilateral's vertices, shape (4, 3).

    Returns
    -------
    area : float
        Area of the quadrilateral.
    normal : numpy.ndarray
        Unit normal vector of the quadrilateral, shape (3,).
    """
    # Divide quadrilateral into two triangles
    triangle1 = vertices[:3]
    triangle2 = np.array([vertices[0], vertices[2], vertices[3]])

    # Compute areas and normals
    area1, normal1 = _compute_tri_area_and_normal(triangle1)
    area2, normal2 = _compute_tri_area_and_normal(triangle2)

    # Average the normals and normalize
    normal = (normal1 + normal2) / 2.0
    # normal = normal / np.linalg.norm(normal)
    return area1 + area2, normal