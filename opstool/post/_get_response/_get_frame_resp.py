import numpy as np
import openseespy.opensees as ops
import xarray as xr

from ._response_base import ResponseBase, _expand_to_uniform_array

ELASTIC_BEAM_CLASSES = [3, 5, 5001, 145, 146, 63, 631]
N_SECS_ELASTIC_BEAM = 7

class FrameRespStepData(ResponseBase):

    def __init__(self, ele_tags=None, ele_load_data=None):
        self.resp_names = [
            "localForces",
            "basicForces",
            "basicDeformations",
            "plasticDeformation",
            "sectionForces",
            "sectionDeformations",
            "sectionLocs",
        ]
        self.resp_steps = None
        self.step_track = 0
        self.ele_tags = ele_tags
        self.ele_load_data = ele_load_data
        self.times = []
        self.initialize()

    def initialize(self):
        self.resp_steps = []
        self.add_data_one_step(self.ele_tags, self.ele_load_data)
        self.times = [0.0]
        self.step_track = 0

    def reset(self):
        self.initialize()

    def add_data_one_step(self, ele_tags, ele_load_data):
        local_forces = _get_beam_local_force(ele_tags, ("localForces", "localForce"))
        basic_forces = _get_beam_basic_resp(ele_tags, ("basicForce", "basicForces"))
        basic_defos = _get_beam_basic_resp(
            ele_tags,
            (
                "basicDeformation",
                "basicDeformations",
                "chordRotation",
                "chordDeformation",
                "deformations",
            ),
        )
        plastic_defos = _get_beam_basic_resp(
            ele_tags, ("plasticRotation", "plasticDeformation")
        )
        sec_f, sec_d, sec_locs = _get_beam_sec_resp(ele_tags, ele_load_data, local_forces)
        data_vars = dict()
        data_vars["localForces"] = (["eleTags", "localDofs"], local_forces)
        data_vars["basicForces"] = (["eleTags", "basicDofs"], basic_forces)
        data_vars["basicDeformations"] = (["eleTags", "basicDofs"], basic_defos)
        data_vars["plasticDeformation"] = (["eleTags", "basicDofs"], plastic_defos)
        data_vars["sectionForces"] = (["eleTags", "secPoints", "secDofs"], sec_f)
        data_vars["sectionDeformations"] = (["eleTags", "secPoints", "secDofs"], sec_d)
        data_vars["sectionLocs"] = (["eleTags", "secPoints"], sec_locs)
        ds = xr.Dataset(
            data_vars=data_vars,
            coords={
                "eleTags": ele_tags,
                "localDofs": [
                    "FX1",
                    "FY1",
                    "FZ1",
                    "MX1",
                    "MY1",
                    "MZ1",
                    "FX2",
                    "FY2",
                    "FZ2",
                    "MX2",
                    "MY2",
                    "MZ2",
                ],
                "basicDofs": ["N", "MZ1", "MZ2", "MY1", "MY2", "T"],
                "secPoints": np.arange(sec_locs.shape[1])+1,
                "secDofs": ["N", "MZ", "VY", "MY", "VZ", "T"],
            },
            attrs={
                "localDofs": "local coord system dofs at end 1 and end 2",
                "basicDofs": "basic coord system dofs at end 1 and end 2",
                "secPoints": "section points No.",
                "secDofs": "section forces and deformations Dofs. "
                           "Note that the section DOFs are only valid for <Elastic Section>, "
                           "<Elastic Shear Section>, and <Fiber Section>. "
                           "For <Aggregator Section>, you should carefully check the data, "
                           "as it may not correspond directly to the DOFs."
            },  # add attributes
        )
        self.resp_steps.append(ds)
        self.times.append(ops.getTime())
        self.step_track += 1

    def _to_xarray(self):
        self.resp_steps = xr.concat(self.resp_steps, dim="time", join="outer")
        self.resp_steps.coords["time"] = self.times

    def get_data(self):
        return self.resp_steps

    def get_track(self):
        return self.step_track

    def save_file(self, dt: xr.DataTree):
        self._to_xarray()
        dt["/FrameResponses"] = self.resp_steps
        return dt

    @staticmethod
    def read_file(dt: xr.DataTree):
        resp_steps = dt["/FrameResponses"].to_dataset()
        return resp_steps

    @staticmethod
    def read_response(dt: xr.DataTree, resp_type: str = None, ele_tags=None):
        ds = FrameRespStepData.read_file(dt)
        if resp_type is None:
            if ele_tags is None:
                return ds
            else:
                return ds.sel(eleTags=ele_tags)
        else:
            if resp_type not in list(ds.keys()):
                raise ValueError(
                    f"resp_type {resp_type} not found in {list(ds.keys())}"
                )
            if ele_tags is not None:
                return ds[resp_type].sel(eleTags=ele_tags)
            else:
                return ds[resp_type]


def _get_beam_local_force(beam_tags, resp_types):
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
        local_forces.append(forces)
    return np.array(local_forces)


def _get_beam_basic_resp(beam_tags, resp_types):
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
        basic_resps.append(resp)
    return np.array(basic_resps)


def _get_beam_sec_resp(beam_tags, ele_load_data, local_forces):
    pattern_tags, load_eletags = [], []
    if len(ele_load_data) > 0:
        petags = ele_load_data.coords["PatternEleTags"].values
        for item in petags:
            num1, num2 = item.split("-")
            pattern_tags.append(int(num1))
            load_eletags.append(int(num2))
    pattern_tags = np.array(pattern_tags)
    load_eletags = np.array(load_eletags)
    # -----------------------------------------------------
    beam_secF, beam_secD, beam_locs = [], [], []
    beam_lengths = _get_ele_length(beam_tags)
    for eletag, length, local_f in zip(beam_tags, beam_lengths, local_forces):
        eletag = int(eletag)
        if ops.getEleClassTags(eletag)[0] in ELASTIC_BEAM_CLASSES:  # elastic beam
            xlocs = np.linspace(0, 1.0, N_SECS_ELASTIC_BEAM)
            sec_f = _get_sec_forces(eletag, length, ele_load_data, pattern_tags, load_eletags, local_f, xlocs)
            sec_d = np.zeros_like(sec_f)
        else:
            xlocs = []
            sec_f, sec_d = [], []
            locs = ops.sectionLocation(eletag)
            locs = locs / length
            for i, loc in enumerate(locs):
                xlocs.append(loc)
                forces = ops.sectionForce(eletag, i + 1)
                if len(forces) == 0:
                    forces = [0.0] * 6
                elif len(forces) == 2:  # 2D fiber section
                    forces = [forces[0], forces[1], 0.0, 0.0, 0.0, 0.0]  # N, Mz
                elif len(forces) == 3:  # N, Mz, Vy
                    forces = [forces[0], forces[1], forces[2], 0.0, 0.0, 0.0]
                elif len(forces) == 4:  # N, Mz, My, T, fiber 3D
                    forces = [forces[0], forces[1], 0.0, forces[2], 0.0, forces[3]]
                elif len(forces) == 5:  # maybe SectionAggregator
                    forces = [forces[0], forces[1], forces[4], forces[2], 0.0, forces[3]]
                elif len(forces) > 6:  # maybe SectionAggregator
                    forces = forces[:6]
                defos = ops.sectionDeformation(eletag, i + 1)
                if len(defos) == 0:
                    defos = [0.0] * 6
                elif len(defos) == 2:
                    defos = [defos[0], defos[1], 0.0, 0.0, 0.0, 0.0]
                elif len(defos) == 3:
                    defos = [defos[0], defos[1], defos[2], 0.0, 0.0, 0.0]
                elif len(defos) == 4:
                    defos = [defos[0], defos[1], 0.0, defos[2], 0.0, defos[3]]
                elif len(defos) == 5:
                    defos = [defos[0], defos[1], defos[4], defos[2], 0.0, defos[3]]
                elif len(defos) > 6:
                    defos = defos[:6]
                sec_f.append(forces)  # N, Mz, Vy, My, Vz, T
                sec_d.append(defos)  # N, Mz, Vy, My, Vz, T
        beam_locs.append(xlocs)
        beam_secF.append(sec_f)
        beam_secD.append(sec_d)
    beam_locs = _expand_to_uniform_array(beam_locs)
    beam_secF = _expand_to_uniform_array(beam_secF)
    beam_secD = _expand_to_uniform_array(beam_secD)
    return beam_secF, beam_secD, beam_locs


def _get_sec_forces(ele_tag, length, ele_load_data, pattern_tags, load_eletags, local_force, xlocs):
    sec_locs = xlocs
    sec_x = sec_locs * length
    sec_f = np.full((len(xlocs), 6), 0.0)
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
        if xb > xa and np.abs(xb - xa - 1) < 1e-2:   # Full uniform load
            wx, wy, wz = wxa * factor, wya * factor, wza * factor
            sec_f[:, 0] += -wx * sec_x
            sec_f[:, 1] += 0.5 * wy * sec_x ** 2
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
            idx2 = sec_x > xa & sec_x < xb
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
    diff = np.array(coords1) - np.array(coords2)
    return np.linalg.norm(diff, axis=1)



