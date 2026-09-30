from __future__ import annotations

from collections.abc import Iterable

import numpy as np
import xarray as xr

from ...utils import get_opensees_module, suppress_ops_print
from ._response_base import ResponseBase, expand_to_uniform_array

ops = get_opensees_module()

RESP_NAME = "FrameResponses"

ELASTIC_BEAM_CLASSES = [3, 4, 5, 5001, 145, 146, 63, 631]

SECTION_TYPE_MAP = {
    "ElasticSection3d": ["P", "MZ", "MY", "T"],
    "ElasticShearSection3d": ["P", "MZ", "VY", "MY", "VZ", "T"],
    "ElasticTubeSection3d": ["P", "MZ", "MY", "T", "VY", "VZ"],
    "FiberSection3d": ["P", "MZ", "MY", "T"],
    "FiberSection3dThermal": ["P", "MZ", "MY", "T"],
    "FiberSectionGJ": ["P", "MZ", "MY", "T"],
    "FiberSectionGJThermal": ["P", "MZ", "MY", "T"],
    "FiberSectionAsym3d": ["P", "MZ", "MY", "W", "T"],
    "FiberSectionWarping3d": ["P", "MZ", "MY", "W", "B", "T"],
    "NDFiberSection3d": ["P", "MZ", "MY", "VY", "VZ", "T"],
    "SectionAggregator3d": ["P", "MZ", "MY", "T", "VY", "VZ"],
    "TimoshenkoSection3d": ["P", "MZ", "MY", "VZ", "VY", "T"],
    "ASDCoupledHinge3D": ["P", "MY", "MZ", "VY", "VZ", "T"],
    # ---------------------------------------------
    "ElasticSection2d": ["P", "MZ"],
    "ElasticShearSection2d": ["P", "MZ", "VY"],
    "ElasticWarpingShearSection2d": ["P", "MZ", "VY", "R", "Q"],
    "FiberSection2d": ["P", "MZ"],
    "FiberSection2dThermal": ["P", "MZ"],
    "Isolator2spring": ["P", "VY", "MZ"],
    "NDFiberSection2d": ["P", "MZ", "VY"],
    "NDFiberSectionWarping2d": ["P", "MZ", "VY", "R", "Q"],
    "SectionAggregator2d": ["P", "MZ", "VY"],
    "ElasticBDShearSection2d": ["P", "MZ", "VY"],
    "WSection2d": ["P", "MZ", "MY", "VY", "VZ", "T"],
}
SECTION_TYPE_DOF_MAP = {"P": 0, "MZ": 1, "VY": 2, "MY": 3, "VZ": 4, "T": 5, "R": None, "Q": None, "B": None}


class FrameRespStepData(ResponseBase):
    def __init__(
        self,
        ele_tags,
        ele_load_data,
        elastic_frame_sec_points: int = 7,
        section_response_dof: dict[str, Iterable[str]] | None = None,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.resp_name = RESP_NAME
        self.resp_types = [
            "localForces",
            "basicForces",
            "basicDeformations",
            "plasticDeformation",
            "sectionForces",
            "sectionDeformations",
            "sectionLocs",
        ]
        self.ele_tags = ele_tags

        if isinstance(section_response_dof, dict):
            SECTION_TYPE_MAP.update(section_response_dof)

        self.elastic_frame_sec_points = elastic_frame_sec_points

        self.localDofs = ["FX1", "FY1", "FZ1", "MX1", "MY1", "MZ1", "FX2", "FY2", "FZ2", "MX2", "MY2", "MZ2"]
        self.basicDofs = ["N", "MZ1", "MZ2", "MY1", "MY2", "T"]
        self.secDofs = ["N", "MZ", "VY", "MY", "VZ", "T"]
        self.secPoints = None
        self.sec_loc_dofs = None
        self.attrs = {
            "localDofs": "local coord system dofs at end 1 and end 2",
            "basicDofs": "basic coord system dofs at end 1 and end 2",
            "secPoints": "section points No.",
            "secDofs": "section forces and deformations Dofs. "
            "Note that the section DOFs are only valid for <Elastic Section>, "
            "<Elastic Shear Section>, and <Fiber Section>. "
            "For <Aggregator Section>, you should carefully check the data, "
            "as it may not correspond directly to the DOFs.",
            "Notes": "Note that the deformations are displacements and rotations in the basicDofs;"
            "And strains and curvatures in the secDofs",
        }

        self.add_resp_data_one_step(ele_tags, ele_load_data)

    def add_resp_data_one_step(self, ele_tags, ele_load_data):
        local_forces = _get_beam_local_force(ele_tags, ("localForces", "localForce"), dtype=self.dtype)
        basic_forces = _get_beam_basic_resp(ele_tags, ("basicForce", "basicForces"), dtype=self.dtype)
        basic_defos = _get_beam_basic_resp(
            ele_tags,
            (
                "basicDeformation",
                "basicDeformations",
                "chordRotation",
                "chordDeformation",
                "deformations",
            ),
            dtype=self.dtype,
        )
        plastic_defos = _get_beam_basic_resp(ele_tags, ("plasticRotation", "plasticDeformation"), dtype=self.dtype)
        sec_f, sec_d, sec_locs = _get_beam_sec_resp(
            ele_tags, ele_load_data, local_forces, basic_defos, self.elastic_frame_sec_points, dtype=self.dtype
        )
        if self.sec_loc_dofs is None:
            if sec_locs.shape[-1] == 2:
                self.sec_loc_dofs = ["alpha", "X"]
            elif sec_locs.shape[-1] == 3:
                self.sec_loc_dofs = ["alpha", "X", "Y"]
            elif sec_locs.shape[-1] == 4:
                self.sec_loc_dofs = ["alpha", "X", "Y", "Z"]
            else:
                self.sec_loc_dofs = [f"loc{i + 1}" for i in range(sec_locs.shape[-1])]
        if self.secPoints is None:
            self.secPoints = np.arange(sec_locs.shape[1]) + 1

        if self.model_update:
            data_vars = {}
            data_vars["localForces"] = (["eleTags", "localDofs"], local_forces)
            data_vars["basicForces"] = (["eleTags", "basicDofs"], basic_forces)
            data_vars["basicDeformations"] = (["eleTags", "basicDofs"], basic_defos)
            data_vars["plasticDeformation"] = (["eleTags", "basicDofs"], plastic_defos)
            data_vars["sectionForces"] = (["eleTags", "secPoints", "secDofs"], sec_f)
            data_vars["sectionDeformations"] = (["eleTags", "secPoints", "secDofs"], sec_d)
            data_vars["sectionLocs"] = (["eleTags", "secPoints", "locs"], sec_locs)
            ds = xr.Dataset(
                data_vars=data_vars,
                coords={
                    "eleTags": ele_tags,
                    "localDofs": self.localDofs,
                    "basicDofs": self.basicDofs,
                    "secPoints": self.secPoints,
                    "secDofs": self.secDofs,
                    "locs": self.sec_loc_dofs,
                },
                attrs=self.attrs,
            )
            self.resp_step_data_list.append(ds)
        else:
            datas = [local_forces, basic_forces, basic_defos, plastic_defos, sec_f, sec_d, sec_locs]
            for name, da in zip(self.resp_types, datas):
                self.resp_step_data_dict[name].append(da)
        self.move_one_step(time_value=ops.getTime())

    def add_resp_data_to_dataset(self):

        self.times = np.array(self.times, dtype=self.dtype["float"])
        if self.model_update:
            self.resp_step_data = xr.concat(self.resp_step_data_list, dim="time", join="outer")
            self.resp_step_data.coords["time"] = self.times
        else:
            data_vars = {}
            data_vars["localForces"] = (["time", "eleTags", "localDofs"], self.resp_step_data_dict["localForces"])
            data_vars["basicForces"] = (["time", "eleTags", "basicDofs"], self.resp_step_data_dict["basicForces"])
            data_vars["basicDeformations"] = (
                ["time", "eleTags", "basicDofs"],
                self.resp_step_data_dict["basicDeformations"],
            )
            data_vars["plasticDeformation"] = (
                ["time", "eleTags", "basicDofs"],
                self.resp_step_data_dict["plasticDeformation"],
            )
            data_vars["sectionForces"] = (
                ["time", "eleTags", "secPoints", "secDofs"],
                self.resp_step_data_dict["sectionForces"],
            )
            data_vars["sectionDeformations"] = (
                ["time", "eleTags", "secPoints", "secDofs"],
                self.resp_step_data_dict["sectionDeformations"],
            )
            data_vars["sectionLocs"] = (
                ["time", "eleTags", "secPoints", "locs"],
                self.resp_step_data_dict["sectionLocs"],
            )
            self.resp_step_data = xr.Dataset(
                data_vars=data_vars,
                coords={
                    "time": self.times,
                    "eleTags": self.ele_tags,
                    "localDofs": self.localDofs,
                    "basicDofs": self.basicDofs,
                    "secPoints": self.secPoints,
                    "secDofs": self.secDofs,
                    "locs": self.sec_loc_dofs,
                },
                attrs=self.attrs,
            )

    @staticmethod
    def read_response(
        dt: xr.DataTree | list[xr.DataTree],
        resp_type: str | None = None,
        ele_tags=None,
        unit_factors: dict | None = None,
        lazy: bool = True,
    ) -> xr.Dataset | xr.DataArray:
        dts = dt if isinstance(dt, (list, tuple)) else [dt]
        if not dts:
            return xr.Dataset()

        dss: list[xr.Dataset] = []
        for t in dts:
            if RESP_NAME not in t:
                continue
            ds = t[f"/{RESP_NAME}"].ds
            if ds is None:
                continue

            # 1) preselect variable(s)
            if resp_type is not None:
                if resp_type not in ds.data_vars:
                    continue
                ds = ds[[resp_type]]

            # 2) early nodeTags selection
            ds = FrameRespStepData._select_ele_tags(ds, ele_tags=ele_tags)

            # 3) if not lazy, load per-part to avoid lazy-concat instability
            if not lazy:
                ds = ds.load()

            dss.append(ds)

        if not dss:
            return xr.Dataset()

        resp_steps = dss[0] if len(dss) == 1 else xr.concat(dss, dim="time", join="outer", fill_value=np.nan)

        resp_steps = _unit_transform(resp_steps, unit_factors)

        if resp_type is not None and resp_type in resp_steps:
            return resp_steps[resp_type]
        return resp_steps


def _unit_transform(ds: xr.Dataset, unit_factors: dict) -> xr.Dataset:
    if not unit_factors:
        return ds

    # ---- take factors, default = 1.0 ----
    ff = float(unit_factors.get("force", 1.0))
    mf = float(unit_factors.get("moment", 1.0))
    cf = float(unit_factors.get("curvature", 1.0))
    df = float(unit_factors.get("disp", 1.0))

    rules = {
        "localForces": (
            "localDofs",
            [
                (["FX1", "FY1", "FZ1", "FX2", "FY2", "FZ2"], ff),
                (["MX1", "MY1", "MZ1", "MX2", "MY2", "MZ2"], mf),
            ],
        ),
        "basicForces": ("basicDofs", [(["N"], ff), (["MZ1", "MZ2", "MY1", "MY2", "T"], mf)]),
        "basicDeformations": ("basicDofs", [(["N"], df)]),
        "plasticDeformation": ("basicDofs", [(["N"], df)]),
        "sectionForces": ("secDofs", [(["N", "VY", "VZ"], ff), (["MZ", "MY", "T"], mf)]),
        "sectionDeformations": ("secDofs", [(["MZ", "MY", "T"], cf)]),
        "sectionLocs": ("locs", [(["X", "Y", "Z"], df)]),
    }

    def apply(da: xr.DataArray, dim: str, groups: list[tuple[list[str], float]]) -> xr.DataArray:
        c = da.coords.get(dim, None)
        if c is None:
            return da
        out = da
        for keys, fac in groups:
            if fac == 1.0:
                continue  # no-op, avoid useless graph nodes
            m = c.isin(keys)
            out = out.where(~m, out * fac)
        return out

    updates = {v: apply(ds[v], dim, groups) for v, (dim, groups) in rules.items() if v in ds.data_vars}

    return ds.assign(**updates) if updates else ds


def _get_beam_local_force(beam_tags: Iterable[int], resp_types: Iterable[str], dtype: dict):
    local_forces = []
    for eletag in beam_tags:
        eletag = int(eletag)
        forces = []
        for name in resp_types:
            forces = ops.eleResponse(eletag, name)
            if len(forces) > 0:
                break
        if len(forces) == 0:
            forces = [0.0] * 12
        elif len(forces) == 6:
            forces = [
                forces[0],  # Fx
                forces[1],  # Fy
                0.0,  # Fz
                0.0,  # Mx
                0.0,  # My
                forces[2],  # Mz
                forces[3],
                forces[4],
                0.0,
                0.0,
                0.0,
                forces[5],
            ]
        elif len(forces) > 12:
            forces = forces[:6] + forces[7:12]
        # Change the signs
        forces = [
            -forces[0],  # Fx1
            -forces[1],  # Fy1
            -forces[2],  # Fz1
            -forces[3],  # Mx1
            forces[4],  # My1
            -forces[5],  # Mz1
            forces[6],  # Fx2
            forces[7],  # Fy2
            forces[8],  # Fz2
            forces[9],  # Mx2
            -forces[10],  # Mz2
            forces[11],  # Mz2
        ]
        local_forces.append(forces)
    return np.array(local_forces, dtype=dtype["float"])


def _get_beam_basic_resp(beam_tags: Iterable[int], resp_types: Iterable[str], dtype: dict):
    basic_resps = []
    for ele_tag in beam_tags:
        ele_tag = int(ele_tag)
        resp = []
        for name in resp_types:
            resp = ops.eleResponse(ele_tag, name)
            if len(resp) > 0:
                break
        if len(resp) == 0:
            resp = [0.0] * 6
        elif len(resp) == 3:
            resp = [
                resp[0],  # N
                resp[1],  # MZ1
                resp[2],  # Mz2
                0.0,  # My1
                0.0,  # My2
                0.0,  # T
            ]
        resp = [
            resp[0],  # N
            -resp[1],  # MZ1
            resp[2],  # Mz2
            resp[3],  # My1
            -resp[4],  # My2
            resp[5],  # T
        ]
        basic_resps.append(resp)
    return np.array(basic_resps, dtype=dtype["float"])


def _get_beam_sec_resp(
    beam_tags: Iterable[int],
    ele_load_data: xr.DataArray,
    local_forces: Iterable,
    basic_disp: Iterable,
    n_secs_elastic_beam: int,
    dtype: dict,
):
    pattern_tags, load_eletags = _extract_pattern_info(ele_load_data)
    beam_secF, beam_secD, beam_locs = [], [], []

    beam_lengths, start_coords, end_coords = _get_ele_length(beam_tags)

    for eletag, length, local_f, basic_d in zip(beam_tags, beam_lengths, local_forces, basic_disp):
        eletag = int(eletag)
        if ops.getEleClassTags(eletag)[0] in ELASTIC_BEAM_CLASSES:
            xlocs = np.linspace(0, 1.0, n_secs_elastic_beam)
            sec_f = _get_elastic_sec_forces(eletag, length, ele_load_data, pattern_tags, load_eletags, local_f, xlocs)
            sec_d = _get_elastic_sec_defo(eletag, sec_f, basic_d, length, xlocs)
        else:
            xlocs, sec_f, sec_d = _get_nonlinear_section_response(eletag, length)

        # adjust signs
        sec_f[:, 1] = -sec_f[:, 1]  # Mz
        sec_f[:, 2] = -sec_f[:, 2]  # Vy
        sec_d[:, 1] = -sec_d[:, 1]  # Mz
        sec_d[:, 2] = -sec_d[:, 2]  # Vy

        beam_locs.append(np.array(xlocs))
        beam_secF.append(np.array(sec_f))
        beam_secD.append(np.array(sec_d))

    beam_locs = expand_to_uniform_array(beam_locs, dtype=dtype["float"])
    beam_secF = expand_to_uniform_array(beam_secF, dtype=dtype["float"])
    beam_secD = expand_to_uniform_array(beam_secD, dtype=dtype["float"])
    beam_sec_locs = _get_ele_sec_coords(start_coords, end_coords, beam_locs)

    return beam_secF, beam_secD, beam_sec_locs.astype(dtype["float"])


def _extract_pattern_info(ele_load_data: xr.DataArray):
    pattern_tags, load_eletags = [], []
    if len(ele_load_data) > 0:
        petags = ele_load_data.coords["PatternEleTags"].values
        for item in petags:
            num1, num2 = item.split("-")
            pattern_tags.append(int(num1))
            load_eletags.append(int(num2))
    return np.array(pattern_tags), np.array(load_eletags)


def _get_section_locs(eletag: int, length: float):
    sec_locs = ops.sectionLocation(eletag)
    if not sec_locs:
        num_secs = 0
        for i in range(100000):
            output = ops.sectionForce(eletag, i + 1)
            if not output:
                break
            num_secs += 1
        if num_secs == 0:
            sec_locs = np.array([])
        elif num_secs == 1:
            sec_locs = np.array([0.5])
        else:
            sec_locs = np.linspace(0, 1, num_secs)
    else:
        sec_locs = np.array(sec_locs) / length
    return sec_locs


def _get_nonlinear_section_response(eletag: int, length: float):
    xlocs, sec_f, sec_d = [], [], []
    sec_locs = _get_section_locs(eletag, length)
    for i, loc in enumerate(sec_locs):
        xlocs.append(loc)
        forces = _format_sec_resp(eletag, i + 1, "Force")
        defos = _format_sec_resp(eletag, i + 1, "Deformation")
        sec_f.append(forces)
        sec_d.append(defos)
    if len(xlocs) == 0:
        xlocs = [0.0]
        sec_f = [[np.nan] * 6]
        sec_d = [[np.nan] * 6]
    xlocs, sec_f, sec_d = np.array(xlocs), np.array(sec_f), np.array(sec_d)
    return xlocs, sec_f, sec_d


def _format_sec_resp(etag: int, secnum: int, resp_type: str):
    if resp_type == "Force":
        resp = ops.sectionForce(etag, secnum)
    elif resp_type == "Deformation":
        resp = ops.sectionDeformation(etag, secnum)
    else:
        resp = None

    full_resp = [0.0] * 6

    if not resp:
        return full_resp

    sec_tags = ops.sectionTag(etag)  # section tags along the element
    if sec_tags and len(sec_tags) > 0:
        sec_tag = sec_tags[secnum - 1]
        sec_type = ops.classType("section", sec_tag)
        if sec_type == "SectionAggregator" and "SectionAggregator" not in SECTION_TYPE_MAP:
            sec_type = "ElasticSection3d" if len(resp) > 3 else "ElasticSection2d"
        dof_names = SECTION_TYPE_MAP.get(sec_type)
        if dof_names is not None:
            dof_map = [SECTION_TYPE_DOF_MAP[name] for name in dof_names]
            for val, dof in zip(resp, dof_map):
                if dof is not None:
                    full_resp[dof] = val
            return full_resp
    # Fallback based on length of resp
    for i in range(min(len(resp), 6)):
        full_resp[i] = resp[i]
    return full_resp


def _get_param_value(eletag, param_name):
    paramTag = 1
    paramTags = ops.getParamTags()
    if len(paramTags) > 0:
        paramTag = max(paramTags) + 1
    ops.parameter(paramTag, "element", eletag, param_name)
    value = ops.getParamValue(paramTag)
    ops.remove("parameter", paramTag)
    return value


def _get_elastic_sec_defo(eletag, sec_force, basic_d, length, xlocs):
    with suppress_ops_print():
        # A = _get_param_value(eletag, "A")
        E = _get_param_value(eletag, "E")
        Iz = _get_param_value(eletag, "Iz")
        Iy = _get_param_value(eletag, "Iy")
        G = _get_param_value(eletag, "G")
        # J = _get_param_value(eletag, "J")
        Avy = _get_param_value(eletag, "Avy")
        Avz = _get_param_value(eletag, "Avz")

    # N1, Mz1, Vy1, My1, Vz1, T1
    eps = 1e-10
    sec_d = np.zeros_like(sec_force)
    oneOverL, xi6 = 1.0 / length, 6 * xlocs
    sec_d[:, 0] = basic_d[0] * oneOverL  # N
    sec_d[:, 5] = basic_d[5] * oneOverL  # T
    if E * Iz > eps:
        sec_d[:, 1] = sec_force[:, 1] / (E * Iz)  # MZ
    else:
        sec_d[:, 1] = oneOverL * ((xi6 - 4.0) * (-basic_d[1]) + (xi6 - 2.0) * basic_d[2])  # MZ
    if E * Iy > eps:
        sec_d[:, 3] = sec_force[:, 3] / (E * Iy)  # MY
    else:
        sec_d[:, 3] = oneOverL * ((xi6 - 4.0) * basic_d[3] + (xi6 - 2.0) * (-basic_d[4]))  # MY
    if G * Avy > eps:
        sec_d[:, 2] = sec_force[:, 2] / (G * Avy)
    if G * Avz > eps:
        sec_d[:, 4] = sec_force[:, 4] / (G * Avz)
    return sec_d


def _get_elastic_sec_forces(ele_tag, length, ele_load_data, pattern_tags, load_eletags, local_force, xlocs):
    sec_locs = xlocs
    sec_x = sec_locs * length
    sec_f = np.full((len(xlocs), 6), 0.0)
    local_force = [-1, -1, -1, -1, 1, -1, 1, 1, 1, 1, -1, 1] * np.array(local_force)  # Change the signs to original
    # N1, Mz1, Vy1, My1, Vz1, T1
    sec_f[:, 0] = -local_force[0]
    sec_f[:, 1] = -local_force[5] + local_force[1] * sec_x
    sec_f[:, 2] = local_force[1]
    sec_f[:, 3] = -local_force[4] - local_force[2] * sec_x
    sec_f[:, 4] = -local_force[2]
    sec_f[:, 5] = -local_force[3]
    if ele_tag in load_eletags:
        idx = np.abs(load_eletags - ele_tag) < 1e-4
        load_data = ele_load_data[idx, 2:].data
        ptags = pattern_tags[idx]
        factors = [ops.getLoadFactor(int(ptag)) for ptag in ptags]
    else:
        load_data = [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]]
        factors = [0.0]
    for ldata, factor in zip(load_data, factors):
        wya, wyb, wza, wzb, wxa, wxb, xa, xb = ldata
        if xb > xa and np.abs(xb - xa - 1) < 1e-2:  # Full uniform load
            wx, wy, wz = wxa * factor, wya * factor, wza * factor
            sec_f[:, 0] += -wx * sec_x
            sec_f[:, 1] += 0.5 * wy * sec_x**2
            sec_f[:, 2] += wy * sec_x
            sec_f[:, 3] += -0.5 * wz * sec_x * sec_x
            sec_f[:, 4] += -wz * sec_x
        elif xb < xa:  # Point Load
            px, py, pz = wxa * factor, wya * factor, wza * factor
            xa = xa * length
            idx = sec_x > xa
            sec_f[idx, 0] += -px
            sec_f[idx, 1] += py * (sec_x[idx] - xa)
            sec_f[idx:, 2] += py
            sec_f[idx:, 3] += -pz * (sec_x[idx] - xa)
            sec_f[idx:, 4] += -pz
        elif xb > xa and np.abs(xb - xa - 1) > 1e-2:  # Partial uniform load
            wx, wy, wz = wxa * factor, wya * factor, wza * factor
            xa = xa * length
            xb = xb * length
            idx2 = (sec_x > xa) & (sec_x < xb)
            idx3 = sec_x >= xb
            sec_f[idx2, 0] += -wx * (sec_x[idx2] - xa)
            sec_f[idx2, 1] += 0.5 * wy * (sec_x[idx2] - xa) ** 2
            sec_f[idx2, 2] += wy * (sec_x[idx2] - xa)
            sec_f[idx2, 3] += -0.5 * wz * (sec_x[idx2] - xa) ** 2
            sec_f[idx2, 4] += -wz * (sec_x[idx2] - xa)
            # ------------------------------
            sec_f[idx3, 0] += -wx * (xb - xa)
            sec_f[idx3, 1] += wy * (xb - xa) * (sec_x[idx3] - 0.5 * (xb + xa))
            sec_f[idx3, 2] += wy * (xb - xa)
            sec_f[idx3, 3] += -wz * (xb - xa) * (sec_x[idx3] - 0.5 * (xb + xa))
            sec_f[idx3, 4] += -wz * (xb - xa)
    return sec_f


def _get_ele_length(ele_tags):
    coords1, coords2 = [], []
    for ele_tag in ele_tags:
        ele_tag = int(ele_tag)
        nodes = ops.eleNodes(ele_tag)
        coords1.append(ops.nodeCoord(nodes[0]))
        coords2.append(ops.nodeCoord(nodes[1]))
    start = np.array(coords1)
    end = np.array(coords2)
    return np.linalg.norm(end - start, axis=1), start, end


def _get_ele_sec_coords(start, end, sec_locs):
    coords = start[:, None, :] + (end - start)[:, None, :] * sec_locs[..., None]
    locs_expanded = sec_locs[..., None]
    return np.concatenate([locs_expanded, coords], axis=-1)
