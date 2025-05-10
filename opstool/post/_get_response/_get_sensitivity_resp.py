import numpy as np
import openseespy.opensees as ops
import xarray as xr

from ._response_base import ResponseBase


class SensitivityRespStepData(ResponseBase):
    def __init__(
            self,
            node_tags=None,
            ele_tags=None,
            sens_para_tags=None,
            model_update: bool = False,
            dtype: dict = None
    ):
        self.resp_names = [
            "disp",
            "vel",
            "accel",
            "pressure",
            "lambdas",
            # "sensSectionForce",
        ]
        self.node_tags = node_tags if node_tags is not None else ops.getNodeTags()
        self.ele_tags = ele_tags if ele_tags is not None else []
        self.sens_para_tags = sens_para_tags if sens_para_tags is not None else ops.getParamTags()
        self.resp_steps = None
        self.resp_steps_list = []  # for model update
        self.resp_steps_dict = dict()  # for non-update
        self.times = []
        self.step_track = 0

        self.model_update = model_update
        self.dtype = dict(int=np.int32, float=np.float32)
        if isinstance(dtype, dict):
            self.dtype.update(dtype)

        self.attrs = {
            "UX": "Displacement in X direction",
            "UY": "Displacement in Y direction",
            "UZ": "Displacement in Z direction",
            "RX": "Rotation about X axis",
            "RY": "Rotation about Y axis",
            "RZ": "Rotation about Z axis",
        }
        self.DOFs = ["UX", "UY", "UZ", "RX", "RY", "RZ"]
        self.patternTags = None

        self.initialize()

    def initialize(self):
        self.resp_steps = None
        self.resp_steps_list = []
        for name in self.resp_names:
            self.resp_steps_dict[name] = []
        self.add_data_one_step(self.node_tags, self.sens_para_tags)
        self.times = [0.0]
        self.step_track = 0

    def reset(self):
        self.initialize()

    def add_data_one_step(self, node_tags, sens_para_tags):
        if node_tags is None:
            node_tags = self.node_tags
        if sens_para_tags is None:
            sens_para_tags = self.sens_para_tags
        disp, vel, accel, pressure = _get_nodal_sens_resp(node_tags, sens_para_tags, dtype=self.dtype)
        lambdas_ = _get_sens_lambda(sens_para_tags, dtype=self.dtype)

        if self.patternTags is None:
            self.patternTags = [] if len(lambdas_) == 0 else np.arange(lambdas_.shape[1]) + 1

        if self.model_update:
            datas = [disp, vel, accel]
            data_vars = {}
            for name, data_ in zip(["disp", "vel", "accel"], datas):
                data_vars[name] = (["paraTags", "nodeTags", "DOFs"], data_)
            data_vars["pressure"] = (["paraTags", "nodeTags"], pressure)
            data_vars["lambdas"] = (["paraTags", "patternTags"], lambdas_)
            # can have different dimensions and coordinates
            ds = xr.Dataset(
                data_vars=data_vars,
                coords={
                    "paraTags": sens_para_tags,
                    "nodeTags": node_tags,
                    "DOFs": self.DOFs,
                    "patternTags": self.patternTags
                },
                attrs=self.attrs,
            )
            self.resp_steps_list.append(ds)
        else:
            datas = [disp, vel, accel, pressure, lambdas_]
            for name, data_ in zip(self.resp_names, datas):
                self.resp_steps_dict[name].append(data_)

        self.times.append(ops.getTime())
        self.step_track += 1

    def get_data(self):
        return self.resp_steps

    def get_track(self):
        return self.step_track

    def _to_xarray(self):
        if self.model_update:
            self.resp_steps = xr.concat(self.resp_steps_list, dim="time", join="outer")
            self.resp_steps.coords["time"] = self.times
        else:
            data_vars = {}
            for name in ["disp", "vel", "accel"]:
                data_vars[name] = (["time", "paraTags", "nodeTags", "DOFs"], self.resp_steps_dict[name])
            data_vars["pressure"] = (["time", "paraTags", "nodeTags"], self.resp_steps_dict["pressure"])
            data_vars["lambdas"] = (["time", "paraTags", "patternTags"], self.resp_steps_dict["lambdas"])
            self.resp_steps = xr.Dataset(
                data_vars=data_vars,
                coords={
                    "paraTags": self.sens_para_tags,
                    "nodeTags": self.node_tags,
                    "DOFs": self.DOFs,
                    "patternTags": self.patternTags
                },
                attrs=self.attrs,
            )

    def save_file(self, dt: xr.DataTree):
        self._to_xarray()
        dt["/SensitivityResponses"] = self.resp_steps
        return dt

    @staticmethod
    def read_file(dt: xr.DataTree):
        # (eleTag, steps, resp_type)
        resp_steps = dt["/SensitivityResponses"].to_dataset()
        return resp_steps

    @staticmethod
    def read_response(dt: xr.DataTree, resp_type: str = None):
        ds = SensitivityRespStepData.read_file(dt)
        if resp_type is None:
            return ds
        else:
            if resp_type not in list(ds.keys()):
                raise ValueError(
                    f"resp_type {resp_type} not found in {list(ds.keys())}"
                )
            return ds[resp_type]


def _get_nodal_sens_resp(node_tags, sens_para_tags, dtype):
    all_node_tags = ops.getNodeTags()
    all_sens_disp = []
    all_sens_vel = []
    all_sens_accel = []
    all_sens_pressure = []
    for para_tag in sens_para_tags:
        para_tag = int(para_tag)
        node_sens_disp = []
        node_sens_vel = []
        node_sens_accel = []
        node_sens_pressure = []
        for ntag in node_tags:
            ntag = int(ntag)
            if ntag in all_node_tags:
                coord = ops.nodeCoord(ntag)
                disp = ops.nodeDisp(ntag)
                ndim = len(coord)
                ndof = len(disp)
                sens_disp = [ops.sensNodeDisp(ntag, i + 1, para_tag) for i in range(ndof)]
                sens_vel = [ops.sensNodeVel(ntag, i + 1, para_tag) for i in range(ndof)]
                sens_accel = [ops.sensNodeAccel(ntag, i + 1, para_tag) for i in range(ndof)]
                if ndim == 1:
                    sens_disp.extend([0, 0, 0, 0, 0])
                    sens_vel.extend([0, 0, 0, 0, 0])
                    sens_accel.extend([0, 0, 0, 0, 0])
                elif ndim == 2:
                    if ndof == 2:  # 2 ndim 2 dof
                        sens_disp.extend([0, 0, 0, 0])
                        sens_vel.extend([0, 0, 0, 0])
                        sens_accel.extend([0, 0, 0, 0])
                    elif ndof >= 3:  # 2 ndim 3 dof
                        sens_disp = [sens_disp[0], sens_disp[1], 0.0, 0.0, 0.0, sens_disp[2]]
                        sens_vel = [sens_vel[0], sens_vel[1], 0.0, 0.0, 0.0, sens_vel[2]]
                        sens_accel = [sens_accel[0], sens_accel[1], 0.0, 0.0, 0.0, sens_accel[2]]
                else:
                    if ndof == 3:  # 3 ndim 3 dof
                        sens_disp.extend([0, 0, 0])
                        sens_vel.extend([0, 0, 0])
                        sens_accel.extend([0, 0, 0])
                    elif ndof == 4:  # 3 ndim 4 dof
                        sens_disp = [sens_disp[0], sens_disp[1], sens_disp[2], 0.0, 0.0, sens_disp[3]]
                        sens_vel = [sens_vel[0], sens_vel[1], sens_vel[2], 0.0, 0.0, sens_vel[3]]
                        sens_accel = [sens_accel[0], sens_accel[1], sens_accel[2], 0.0, 0.0, sens_accel[3]]
                    elif ndof < 6:  # 3 ndim 6 dof
                        sens_disp.extend([0] * (6 - len(sens_disp)))
                        sens_vel.extend([0] * (6 - len(sens_vel)))
                        sens_accel.extend([0] * (6 - len(sens_accel)))
                    elif ndof > 6:
                        sens_disp = sens_disp[:6]
                        sens_vel = sens_vel[:6]
                        sens_accel = sens_accel[:6]
            else:
                sens_disp = [np.nan] * 6
                sens_vel = [np.nan] * 6
                sens_accel = [np.nan] * 6
            node_sens_disp.append(sens_disp)
            node_sens_vel.append(sens_vel)
            node_sens_accel.append(sens_accel)
            node_sens_pressure.append(ops.sensNodePressure(ntag, para_tag))
        all_sens_disp.append(node_sens_disp)
        all_sens_vel.append(node_sens_vel)
        all_sens_accel.append(node_sens_accel)
        all_sens_pressure.append(node_sens_pressure)
    all_sens_disp = np.array(all_sens_disp, dtype=dtype["float"])
    all_sens_vel = np.array(all_sens_vel, dtype=dtype["float"])
    all_sens_accel = np.array(all_sens_accel, dtype=dtype["float"])
    all_sens_pressure = np.array(all_sens_pressure, dtype=dtype["float"])
    return all_sens_disp, all_sens_vel, all_sens_accel, all_sens_pressure


def _get_sens_lambda(sens_para_tags, dtype):
    pattern_tags = ops.getPatterns()
    all_sens_lambdas = []
    for para_tag in sens_para_tags:
        para_tag = int(para_tag)
        sens_lambads = []
        for ptag in pattern_tags:
            sens_lambads.append(ops.sensLambda(ptag, para_tag))
        all_sens_lambdas.append(sens_lambads)
    return np.array(all_sens_lambdas, dtype=dtype["float"])


def _get_sec_sens(ele_tags, sens_para_tags):
    pass
