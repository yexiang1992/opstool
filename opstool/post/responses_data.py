from typing import Union

import openseespy.opensees as ops
import xarray as xr

from ._get_response import (
    ModelInfoStepData,
    NodalRespStepData,
    TrussRespStepData,
    FrameRespStepData,
    LinkRespStepData,
    FiberSecRespStepData,
    ShellRespStepData,
    PlaneRespStepData,
    BrickRespStepData,
)
from .eigen_data import save_eigen_data
from .model_data import save_model_data
from ..utils import RESULTS_DIR, get_random_color, CONSOLE, PKG_PREFIX


class CreateODB:
    """Create an output database (ODB) to save response data.

    Parameters
    ------------
    odb_tag: Union[int, str], default: 1
        Tag of output databases (ODB) to be saved.
    model_update: bool, default: False
        Whether to update the model data.

        .. Note::
            If True, the model data will be updated at each step.
            If no nodes and elements are added or removed during the analysis of your model,
            keep this parameter set to **`False`**.
            Enabling model updates unnecessarily can increase memory usage and slow down performance.

    save_nodal_resp: bool, default: True
        Whether to save nodal responses.
    save_frame_resp: bool, default: True
        Whether to save frame element responses.
    save_truss_resp: bool, default: True
        Whether to save truss element responses.
    save_link_resp: bool, default: True
        Whether to save link element responses.
    save_shell_resp: bool, default: True
        Whether to save shell element responses.
    save_fiber_sec_resp: bool, default: True
        Whether to save fiber section responses.
    save_plane_resp: bool, default: True
        Whether to save plane element responses.
    save_brick_resp: bool, default: True
        Whether to save brick element responses.
    """

    def __init__(
            self,
            odb_tag: Union[int, str] = 1,
            model_update: bool = False,
            save_nodal_resp: bool = True,
            save_frame_resp: bool = True,
            save_truss_resp: bool = True,
            save_link_resp: bool = True,
            save_shell_resp: bool = True,
            save_fiber_sec_resp: bool = True,
            save_plane_resp: bool = True,
            save_brick_resp: bool = True,
    ):
        self.odb_tag = odb_tag
        self.model_update = model_update
        self.save_nodal_resp = save_nodal_resp
        self.save_frame_resp = save_frame_resp
        self.save_truss_resp = save_truss_resp
        self.save_link_resp = save_link_resp
        self.save_shell_resp = save_shell_resp
        self.save_fiber_sec_resp = save_fiber_sec_resp
        self.save_plane_resp = save_plane_resp
        self.save_brick_resp = save_brick_resp

        self.ModelInfo = None
        self.NodalResp = None
        self.FrameResp = None
        self.TrussResp = None
        self.LinkResp = None
        self.ShellResp = None
        self.FiberSecResp = None
        self.PlaneResp = None
        self.BrickResp = None

        self.initialize()

    def initialize(self):
        self.ModelInfo = ModelInfoStepData(model_update=self.model_update)
        node_tags = self.ModelInfo.get_current_node_tags()
        if len(node_tags) > 0 and self.save_nodal_resp:
            self.NodalResp = NodalRespStepData(node_tags)
        frame_tags = self.ModelInfo.get_current_frame_tags()
        frame_load_data = self.ModelInfo.get_current_frame_load_data()
        if len(frame_tags) > 0 and self.save_frame_resp:
            self.FrameResp = FrameRespStepData(frame_tags, frame_load_data)
        truss_tags = self.ModelInfo.get_current_truss_tags()
        if len(truss_tags) > 0 and self.save_truss_resp:
            self.TrussResp = TrussRespStepData(truss_tags)
        link_tags = self.ModelInfo.get_current_link_tags()
        if len(link_tags) > 0 and self.save_link_resp:
            self.LinkResp = LinkRespStepData(link_tags)
        shell_tags = self.ModelInfo.get_current_shell_tags()
        if len(shell_tags) > 0 and self.save_shell_resp:
            self.ShellResp = ShellRespStepData(shell_tags)
        if self.save_fiber_sec_resp:
            self.FiberSecResp = FiberSecRespStepData()
        plane_tags = self.ModelInfo.get_current_plane_tags()
        if len(plane_tags) > 0 and self.save_plane_resp:
            self.PlaneResp = PlaneRespStepData(plane_tags)
        brick_tags = self.ModelInfo.get_current_brick_tags()
        if len(brick_tags) > 0 and self.save_brick_resp:
            self.BrickResp = BrickRespStepData(brick_tags)

    def reset(self):
        if self.ModelInfo is not None:
            self.ModelInfo.reset()
        if self.NodalResp is not None:
            self.NodalResp.reset()
        if self.FrameResp is not None:
            self.FrameResp.reset()
        if self.TrussResp is not None:
            self.TrussResp.reset()
        if self.LinkResp is not None:
            self.LinkResp.reset()
        if self.ShellResp is not None:
            self.ShellResp.reset()
        if self.FiberSecResp is not None:
            self.FiberSecResp.reset()
        if self.PlaneResp is not None:
            self.PlaneResp.reset()
        if self.BrickResp is not None:
            self.BrickResp.reset()

    def fetch_response_step(self, print_info: bool = False):
        """Extract response data for the current moment.

        Parameters
        ------------
        print_info: bool, optional
            print information, by default, False
        """
        self.ModelInfo.add_data_one_step()
        node_tags = self.ModelInfo.get_current_node_tags()
        if len(node_tags) > 0 and self.save_nodal_resp:
            self.NodalResp.add_data_one_step(node_tags)
        frame_tags = self.ModelInfo.get_current_frame_tags()
        frame_load_data = self.ModelInfo.get_current_frame_load_data()
        if len(frame_tags) > 0 and self.save_frame_resp:
            self.FrameResp.add_data_one_step(frame_tags, frame_load_data)
        truss_tags = self.ModelInfo.get_current_truss_tags()
        if len(truss_tags) > 0 and self.save_truss_resp:
            self.TrussResp.add_data_one_step(truss_tags)
        link_tags = self.ModelInfo.get_current_link_tags()
        if len(link_tags) > 0 and self.save_link_resp:
            self.LinkResp.add_data_one_step(link_tags)
        shell_tags = self.ModelInfo.get_current_shell_tags()
        if len(shell_tags) > 0 and self.save_shell_resp:
            self.ShellResp.add_data_one_step(shell_tags)
        if self.save_fiber_sec_resp:
            self.FiberSecResp.add_data_one_step()
        plane_tags = self.ModelInfo.get_current_plane_tags()
        if len(plane_tags) > 0 and self.save_plane_resp:
            self.PlaneResp.add_data_one_step(plane_tags)
        brick_tags = self.ModelInfo.get_current_brick_tags()
        if len(brick_tags) > 0 and self.save_brick_resp:
            self.BrickResp.add_data_one_step(brick_tags)

        time = ops.getTime()
        if print_info:
            color = get_random_color()
            CONSOLE.print(
                f"{PKG_PREFIX} The responses data at time [bold {color}]{time:.4f}[/] has been fetched!"
            )

    def save_response(self):
        """
        Save all response data to a file name ``RespStepData-{odb_tag}.nc``.
        """
        filename = f"{RESULTS_DIR}/" + f"RespStepData-{self.odb_tag}.nc"
        dt = xr.DataTree(name="RespStepData")

        if self.ModelInfo is not None:
            self.ModelInfo.save_file(dt)
        if self.NodalResp is not None:
            self.NodalResp.save_file(dt)
        if self.FrameResp is not None:
            self.FrameResp.save_file(dt)
        if self.TrussResp is not None:
            self.TrussResp.save_file(dt)
        if self.LinkResp is not None:
            self.LinkResp.save_file(dt)
        if self.ShellResp is not None:
            self.ShellResp.save_file(dt)
        if self.FiberSecResp is not None:
            self.FiberSecResp.save_file(dt)
        if self.PlaneResp is not None:
            self.PlaneResp.save_file(dt)
        if self.BrickResp is not None:
            self.BrickResp.save_file(dt)

        dt.to_netcdf(filename, mode="w", engine="netcdf4")

        color = get_random_color()
        CONSOLE.print(
            f"{PKG_PREFIX} All responses data with odb_tag = {self.odb_tag} "
            f"saved in [bold {color}]{filename}[/]!"
        )

    def save_eigen_data(
            self,
            mode_tag: int = 1,
            solver: str = "-genBandArpack",
    ):
        """Save modal analysis data.

        Parameters
        ----------
        mode_tag : int, optional,
            Modal tag, all modal data smaller than this modal tag will be saved, by default 1
        solver : str, optional,
           OpenSees' eigenvalue analysis solver, by default "-genBandArpack".
        """
        save_eigen_data(odb_tag=self.odb_tag, mode_tag=mode_tag, solver=solver)

    def save_model_data(
            self,
    ):
        """Save the model data from the current domain."""
        save_model_data(odb_tag=self.odb_tag)


def loadODB(obd_tag, resp_type: str = "Nodal"):
    """Load saved response data.

    Parameters
    ----------

    Returns
    --------
    Relevant to a response type.
    """
    filename = f"{RESULTS_DIR}/" + f"RespStepData-{obd_tag}.nc"
    dt = xr.open_datatree(filename, engine="netcdf4").load()

    color = get_random_color()
    CONSOLE.print(
        f"{PKG_PREFIX} Loading response data from [bold {color}]{filename}[/] ..."
    )
    model_info_steps, model_update = ModelInfoStepData.read_file(dt)
    if resp_type.lower() == "nodal":
        resp_step = NodalRespStepData.read_file(dt)
    elif resp_type.lower() == "frame":
        resp_step = FrameRespStepData.read_file(dt)
    elif resp_type.lower() == "fibersec":
        resp_step = FiberSecRespStepData.read_file(dt)
    elif resp_type.lower() == "truss":
        resp_step = TrussRespStepData.read_file(dt)
    elif resp_type.lower() == "link":
        resp_step = LinkRespStepData.read_file(dt)
    elif resp_type.lower() == "shell":
        resp_step = ShellRespStepData.read_file(dt)
    elif resp_type.lower() == "plane":
        resp_step = PlaneRespStepData.read_file(dt)
    elif resp_type.lower() == "brick":
        resp_step = BrickRespStepData.read_file(dt)
    else:
        raise ValueError(f"Unsupported response type {resp_type}!")

    return model_info_steps, model_update, resp_step


def get_nodal_responses(
        odb_tag: int,
        resp_type: str = None,
        node_tags: Union[list, tuple, int] = None
) -> xr.Dataset:
    """Read nodal responses data from a file.

    Parameters
    ----------
    odb_tag: Union[int, str], default: one
        Tag of output databases (ODB) to be read.
    resp_type: str, default: disp
        Type of response to be read.
        Optional:

        * "disp" - Displacement at the node.
        * "vel" - Velocity at the node.
        * "accel" - Acceleration at the node.
        * "reaction" - Reaction forces at the node.
        * "reactionIncInertia" - Reaction forces including inertial effects.
        * "rayleighForces" - Forces resulting from Rayleigh damping.
        * "pressure" - Pressure applied to the node.
        * If None, return all responses.

    node_tags: Union[list, tuple, int], default: None
        Node tags to be read.
        Such as [1, 2, 3] or numpy.array([1, 2, 3]) or 1.
        If None, return all nodal responses.

        .. Note::
            If some nodes are deleted during the analysis,
            their response data will be filled with `numpy.nan`.

    Returns
    ---------
    NodalResp: xarray.Dataset
        Nodal responses' data.

    .. Note::
        The returned data can be viewed using `.dims` and `.coords` to view the
        dimension names and coordinates.
        You can further index or process the data.

    """
    filename = f"{RESULTS_DIR}/" + f"RespStepData-{odb_tag}.nc"
    dt = xr.open_datatree(filename, engine="netcdf4")

    color = get_random_color()
    CONSOLE.print(
        f"{PKG_PREFIX} Loading response data from [bold {color}]{filename}[/] ..."
    )

    nodal_resp = NodalRespStepData.read_response(dt, resp_type=resp_type, node_tags=node_tags)
    return nodal_resp


def get_element_responses(
        odb_tag: int,
        ele_type: str,
        resp_type: str = None,
        ele_tags: Union[list, tuple, int] = None
) -> xr.Dataset:
    """Read nodal responses data from a file.

    Parameters
    ------------
    odb_tag: Union[int, str], default: one
        Tag of output databases (ODB) to be read.
    ele_type: str, default: Frame
        Type of element to be read.
        Optional: "Frame", "Truss", "Link", "Shell", "Plane", "Brick".
    resp_type: str, default: disp
        The response type, which depends on the parameter `ele_type`.
        If None, return all responses to that `ele_type`.

        #. For `Frame`:
            * "localForces": Local forces in the element local coordinate system.
            * "basicForces": Basic forces in the element basic coordinate system.
            * "basicDeformations": Basic deformations in the element basic coordinate system.
            * "plasticDeformation": Plastic deformations in the element basic coordinate system.
            * "sectionForces": Section forces in the element coordinate system.
            * "sectionDeformations": Section deformations in the element coordinate system.
            * "sectionLocs": Section locations, 0.0 to 1.0.
        #. For `Truss`:
            * "axialForce": Axial force.
            * "axialDefo": Axial deformation.
            * "Stress": Stress of material.
            * "Strain": Strain of material.
        #. For `Link`:
            * "basicDeformation": Basic deformation, i.e., pure deformation.
            * "basicForce": Basic force.
        #. For `Shell`:
            * "sectionForces": Sectional forces at Gauss points (per unit length).
            * "sectionDeformations": Sectional deformation at Gauss points (per unit length).
        #. For `Plane`:
            * "stresses": Stresses at Gauss points.
            * "strains": Strains at Gauss points.
        #. For `Brick`:
            * "stresses": Stresses at Gauss points.
            * "strains": Strains at Gauss points.

    ele_tags: Union[list, tuple, int], default: None
        Element tags to be read.
        Such as [1, 2, 3] or numpy.array([1, 2, 3]) or 1.
        If None, return all nodal responses.

        .. note::
            If some nodes are deleted during the analysis,
            their response data will be filled with `numpy.nan`.

    Returns
    ---------
    EleResp: xarray.Dataset
        Element responses' data.

    .. note::
        The returned data can be viewed using `.dims`、`.coords` and `.attrs` to view the
        dimension names and coordinates.
        You can further index or process the data.
    """
    filename = f"{RESULTS_DIR}/" + f"RespStepData-{odb_tag}.nc"
    dt = xr.open_datatree(filename, engine="netcdf4")

    color = get_random_color()
    CONSOLE.print(
        f"{PKG_PREFIX} Loading response data from [bold {color}]{filename}[/] ..."
    )

    if ele_type.lower() == "frame":
        ele_resp = FrameRespStepData.read_response(dt, resp_type=resp_type, ele_tags=ele_tags)
    elif ele_type.lower() == "truss":
        ele_resp = TrussRespStepData.read_response(dt, resp_type=resp_type, ele_tags=ele_tags)
    elif ele_type.lower() == "link":
        ele_resp = LinkRespStepData.read_response(dt, resp_type=resp_type, ele_tags=ele_tags)
    elif ele_type.lower() == "shell":
        ele_resp = ShellRespStepData.read_response(dt, resp_type=resp_type, ele_tags=ele_tags)
    elif ele_type.lower() == "plane":
        ele_resp = PlaneRespStepData.read_response(dt, resp_type=resp_type, ele_tags=ele_tags)
    elif ele_type.lower() == "brick":
        ele_resp = BrickRespStepData.read_response(dt, resp_type=resp_type, ele_tags=ele_tags)
    else:
        raise ValueError(
            f"Unsupported element type {ele_type}, "
            "must in [Frame, Truss, Link, Shell, Plane, Brick]!"
        )

    return ele_resp
