import numpy as np
import openseespy.opensees as ops


def beam_geom_transf(
    nodeTagI: int, nodeTagJ: int, transfType: str, dI: list = None, dJ: list = None
):
    """Output the geometric transformation tag of the beam element according to the node tag previously defined.
    This function divide beam elements into two classes, vertical ones and non-vertical ones,
    vertical elements ``vecxz = [-1, 0, 0]``, and non-vertical elements ``vecxz = [0, 0, 1]``.
    See `geomTransf commands doc <https://openseespydoc.readthedocs.io/en/latest/src/geomTransf.html>`_

    Parameters
    ----------
    nodeTagI : int
        Previously defined I-end node tag.
    nodeTagJ : int
        Previously defined J-end node tag.
    transfType : str
        Geometric transformation type, one of ['Linear', 'PDelta', 'Corotational'].
    dI: list, optional, default=None
        joint offset values – offsets specified with respect to the global coordinate
        system for element-end node i (the number of arguments depends on the dimensions of the current model).
    dJ: list, optional, default=None
        joint offset values – offsets specified with respect to the global coordinate
        system for element-end node j (the number of arguments depends on the dimensions of the current model).

    Returns
    -------
    int
        Geometric transformation tag that this function internally defined.
    """
    coordI, coordJ = ops.nodeCoord(nodeTagI), ops.nodeCoord(nodeTagJ)
    if len(coordI) < 3 or len(coordJ) < 3:
        raise ValueError("This geometric transformations only for 3D!")
    if transfType not in ["Linear", "PDelta", "Corotational"]:
        raise ValueError(
            "transfType must be one of ['Linear', 'PDelta', 'Corotational']!"
        )
    coordI = np.array(coordI)
    coordJ = np.array(coordJ)
    xaxis = coordJ - coordI
    global_z = [0, 0, 1]
    cos_angle = xaxis.dot(global_z) / (np.linalg.norm(xaxis) * np.linalg.norm(global_z))
    if np.abs(1 - cos_angle**2) < 1e-10:
        tag = _creat_geom_transf(transfType, dI=dI, dJ=dJ, ver=True)
    else:
        tag = _creat_geom_transf(transfType, dI=dI, dJ=dJ, ver=False)
    return tag


def _creat_geom_transf(
    transfType: str, dI: list = None, dJ: list = None, ver: bool = False
):
    CrdTransfTags = ops.getCrdTransfTags()
    if len(CrdTransfTags) > 0:
        tag = int(np.max(CrdTransfTags) + 1)
    else:
        tag = 1
    if ver:
        vecxz = [-1.0, 0.0, 0.0]
    else:
        vecxz = [0.0, 0.0, 1.0]
    if dI is None and dJ is None:
        ops.geomTransf(transfType, tag, *vecxz)
    elif dI and dJ:
        ops.geomTransf(transfType, tag, *vecxz, "-jntOffset", *dI, *dJ)
    else:
        raise ValueError("dI and dJ must be both None or input at the same time!")
    return tag
