import numpy as np
import openseespy.opensees as ops
import xarray as xr

from ._response_base import ResponseBase


class NodalRespStepData(ResponseBase):
    def __init__(self, node_tags=None):
        self.nodal_resp_names = [
            "disp",
            "vel",
            "accel",
            "reaction",
            "reactionIncInertia",
            "rayleighForces",
            "pressure",
            # sensitivity
            # "dispSensitivity",
            # "velSensitivity",
            # "accSensitivity",
        ]
        self.node_tags = node_tags if node_tags is not None else ops.getNodeTags()
        self.resp_steps = None
        self.times = []
        self.step_track = 0
        self.initialize()

    def initialize(self):
        self.resp_steps = []
        self.add_data_one_step(self.node_tags)
        self.times = [0.0]
        self.step_track = 0

    def reset(self):
        self.initialize()

    def add_data_one_step(self, node_tags):
        # node_tags = ops.getNodeTags()
        disp, vel, accel, pressure = _get_nodal_resp(node_tags)
        reacts, reacts_inertia, rayleigh_forces = _get_nodal_react(node_tags)
        datas = [disp, vel, accel, reacts, reacts_inertia, rayleigh_forces]
        data_vars = {}
        for name, data_ in zip(self.nodal_resp_names, datas):
            data_vars[name] = (["nodeTags", "DOFs"], data_)
        data_vars["pressure"] = (["nodeTags"], pressure)
        # can have different dimensions and coordinates
        ds = xr.Dataset(
            data_vars=data_vars,
            coords={
                "nodeTags": node_tags,
                "DOFs": ["UX", "UY", "UZ", "RX", "RY", "RZ"],
            },
            attrs={
                "UX": "Displacement in X direction",
                "UY": "Displacement in Y direction",
                "UZ": "Displacement in Z direction",
                "RX": "Rotation about X axis",
                "RY": "Rotation about Y axis",
                "RZ": "Rotation about Z axis",
            },
        )
        self.resp_steps.append(ds)
        self.times.append(ops.getTime())
        self.step_track += 1

    def get_data(self):
        return self.resp_steps

    def get_track(self):
        return self.step_track

    def _to_xarray(self):
        self.resp_steps = xr.concat(self.resp_steps, dim="time", join="outer")
        self.resp_steps.coords["time"] = self.times

    def save_file(self, dt: xr.DataTree):
        self._to_xarray()
        dt["/NodalResponses"] = self.resp_steps
        return dt

    @staticmethod
    def read_file(dt: xr.DataTree):
        # (eleTag, steps, resp_type)
        node_resp_steps = dt["/NodalResponses"].to_dataset()
        return node_resp_steps

    @staticmethod
    def read_response(dt: xr.DataTree, resp_type: str = None, node_tags=None):
        ds = NodalRespStepData.read_file(dt)
        if resp_type is None:
            if node_tags is None:
                return ds
            else:
                return ds.sel(nodeTags=node_tags)
        else:
            if resp_type not in list(ds.keys()):
                raise ValueError(
                    f"resp_type {resp_type} not found in {list(ds.keys())}"
                )
            if node_tags is not None:
                return ds[resp_type].sel(nodeTags=node_tags)
            else:
                return ds[resp_type]


def _get_nodal_resp(node_tags):
    node_disp = []  # 6 data each row, Ux, Uy, Uz, Rx, Ry, Rz
    node_vel = []  # 6 data each row, Ux, Uy, Uz, Rx, Ry, Rz
    node_accel = []  # 6 data each row, Ux, Uy, Uz, Rx, Ry, Rz
    node_pressure = []  # 1 data each row, P
    for i, tag in enumerate(node_tags):
        tag = int(tag)
        if tag in ops.getNodeTags():
            coord = ops.nodeCoord(tag)
            disp = ops.nodeDisp(tag)
            vel = ops.nodeVel(tag)
            accel = ops.nodeAccel(tag)
            if len(coord) == 1:
                disp.extend([0, 0, 0, 0, 0])
                vel.extend([0, 0, 0, 0, 0])
                accel.extend([0, 0, 0, 0, 0])
            elif len(coord) == 2:
                if len(disp) == 2:  # 2 ndim 2 dof
                    disp.extend([0, 0, 0, 0])
                    vel.extend([0, 0, 0, 0])
                    accel.extend([0, 0, 0, 0])
                elif len(disp) >= 3:  # 2 ndim 3 dof
                    disp = [disp[0], disp[1], 0.0, 0.0, 0.0, disp[2]]
                    vel = [vel[0], vel[1], 0.0, 0.0, 0.0, vel[2]]
                    accel = [accel[0], accel[1], 0.0, 0.0, 0.0, accel[2]]
            else:
                if len(disp) == 3:  # 3 ndim 3 dof
                    disp.extend([0, 0, 0])
                    vel.extend([0, 0, 0])
                    accel.extend([0, 0, 0])
                elif len(disp) == 4:  # 3 ndim 4 dof
                    disp = [disp[0], disp[1], disp[2], 0.0, 0.0, disp[3]]
                    vel = [vel[0], vel[1], vel[2], 0.0, 0.0, vel[3]]
                    accel = [accel[0], accel[1], accel[2], 0.0, 0.0, accel[3]]
                elif len(disp) < 6:  # 3 ndim 6 dof
                    disp.extend([0] * (6 - len(disp)))
                    vel.extend([0] * (6 - len(vel)))
                    accel.extend([0] * (6 - len(accel)))
                elif len(disp) > 6:
                    disp = disp[:6]
                    vel = vel[:6]
                    accel = accel[:6]
        else:
            disp = [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]
            vel = [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]
            accel = [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]
        node_disp.append(disp)
        node_vel.append(vel)
        node_accel.append(accel)
        node_pressure.append(ops.nodePressure(tag))
    node_disp = np.array(node_disp, dtype=float)
    node_vel = np.array(node_vel, dtype=float)
    node_accel = np.array(node_accel, dtype=float)
    node_pressure = np.array(node_pressure, dtype=float)
    return node_disp, node_vel, node_accel, node_pressure


def _get_nodal_react(node_tags):
    def get_react(tags):
        forces = []  # 6 data each row, Ux, Uy, Uz, Rx, Ry, Rz
        for tag in tags:
            tag = int(tag)
            if tag in ops.getNodeTags():
                coord = ops.nodeCoord(tag)
                fo = ops.nodeReaction(tag)
                if len(coord) == 1:
                    fo.extend([0.0, 0.0, 0.0, 0.0, 0.0])
                elif len(coord) == 2:
                    if len(fo) == 2:
                        fo.extend([0.0, 0.0, 0.0, 0.0])
                    elif len(fo) >= 3:
                        fo = [fo[0], fo[1], 0.0, 0.0, 0.0, fo[2]]
                else:
                    if len(fo) == 3:
                        fo.extend([0.0, 0.0, 0.0])
                    elif len(fo) < 6:  # 3 ndim 6 dof
                        fo.extend([0] * (6 - len(fo)))
                    elif len(fo) > 6:
                        fo = fo[:6]
            else:
                fo = [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]
            forces.append(fo)
        return forces

    ops.reactions()
    reacts = np.array(get_react(node_tags), dtype=float)
    # rayleighForces
    ops.reactions("-rayleigh")
    rayleigh_forces = np.array(get_react(node_tags), dtype=float)
    # Include Inertia
    ops.reactions("-dynamic")
    reacts_inertia = np.array(get_react(node_tags), dtype=float)
    return reacts, reacts_inertia, rayleigh_forces
