
import numpy as np
import xarray as xr
import openseespy.opensees as ops


def get_node_data() -> xr.DataArray:
    """Get nodal data from the OpenSees model.

    Returns:
    ---------
    node_data : xarray.DataArray
        Nodal data array with coordinates and tags.
    """
    node_ndims, node_ndofs, node_coords = [], [], []
    node_tags = ops.getNodeTags()
    for i, tag in enumerate(node_tags):
        coord = ops.nodeCoord(tag)
        ndim = ops.getNDM(tag)[0]
        ndof = ops.getNDF(tag)[0]
        if ndim == 1:
            coord.extend([0, 0])
        elif ndim == 2:
            coord.extend([0])
        node_ndims.append(ndim)
        node_ndofs.append(ndof)
        node_coords.append(coord)
    if len(node_coords) > 0:
        node_data = xr.DataArray(
            node_coords,
            coords={
                "nodeTags": node_tags,
                "coords": ["Xloc", "Yloc", "Zloc"],
            },
            dims=["nodeTags", "coords"],
            attrs={
                "numNodes": len(node_tags),
                "ndofs": tuple(node_ndofs),
                "ndims": tuple(node_ndims),
            }
        )
    else:
        node_data = xr.DataArray(node_coords)
    node_data.name = "NodalData"
    return node_data


def get_node_mass() -> xr.DataArray:
    """Get nodal mass data from the OpenSees model.

    Returns:
    ---------
    node_mass : xarray.DataArray
        Nodal mass data array with mass values and tags.
    """
    node_mass = []
    node_tags = ops.getNodeTags()
    for i, tag in enumerate(node_tags):
        mass = ops.nodeMass(tag)
        ndm = ops.getNDM(tag)[0]
        ndf = ops.getNDF(tag)[0]
        if ndm == 1:
            mass.extend([0., 0., 0., 0., 0.])
        elif ndm == 2 and ndf == 3:
            mass = [mass[0], mass[1], 0.0, 0.0, 0.0, mass[2]]
        elif ndm == 2 and ndf == 2:
            mass = [mass[0], mass[1], 0.0, 0.0, 0.0, 0.0]
        elif ndm == 3 and ndf == 3:
            mass = [mass[0], mass[1], mass[2], 0.0, 0.0, 0.0]
        elif ndm == 3 and ndf == 4:
            mass = [mass[0], mass[1], mass[2], 0.0, 0.0, mass[3]]
        elif ndm == 3 and ndf == 6:
            mass = [mass[0], mass[1], mass[2], mass[3], mass[4], mass[5]]
        node_mass.append(mass)
    if len(node_mass) > 0:
        node_mass = xr.DataArray(
            node_mass,
            coords={
                "nodeTags": node_tags,
                "mass": ["UX", "UY", "UZ", "RX", "RY", "RZ"],
            },
            dims=["nodeTags", "mass"],
        )
    else:
        node_mass = xr.DataArray([])
    node_mass.name = "NodalMass"
    return node_mass