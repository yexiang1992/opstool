import openseespy.opensees as ops
import xarray as xr

from ._response_base import ResponseBase


class LinkRespStepData(ResponseBase):

    def __init__(self, ele_tags=None):
        self.resp_names = ["basicDeformation", "basicForce"]
        self.resp_steps = None
        self.step_track = 0
        self.ele_tags = ele_tags
        self.times = []
        self.initialize()

    def initialize(self):
        self.resp_steps = []
        self.add_data_one_step(self.ele_tags)
        self.step_track = 0
        self.times = [0.0]

    def reset(self):
        self.initialize()

    def add_data_one_step(self, ele_tags):
        data = _get_link_resp(ele_tags)
        data_vars = {}
        if len(ele_tags) > 0:
            for name, data_ in zip(self.resp_names, data):
                data_vars[name] = (["eleTags", "DOFs"], data_)
            ds = xr.Dataset(
                data_vars=data_vars,
                coords={
                    "eleTags": ele_tags,
                    "DOFs": ["UX", "UY", "UZ", "RX", "RY", "RZ"],
                },
                attrs={
                    "DOFs": "The DOFs are aligned with the local coordinate system. "
                            "Note that these DOFs are not necessarily valid unless all degrees of freedom are "
                            "assigned to the material (e.g., all six DOFs in 3D). "
                            "For cases where the material is assigned to only partial DOFs, "
                            "the actual DOFs are arranged sequentially, with the remaining ones padded with zeros."
                }
            )
        else:
            for name, data_ in zip(self.resp_names, data):
                data_vars[name] = xr.DataArray([])
            ds = xr.Dataset(data_vars=data_vars)
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
        dt["/LinkResponses"] = self.resp_steps
        return dt

    @staticmethod
    def read_file(dt: xr.DataTree):
        resp_steps = dt["/LinkResponses"].to_dataset()
        return resp_steps

    @staticmethod
    def read_response(dt: xr.DataTree, resp_type: str = None, ele_tags=None):
        ds = LinkRespStepData.read_file(dt)
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


def _get_link_resp(link_tags):
    defos, forces = [], []
    for etag in link_tags:
        etag = int(etag)
        defo = _get_link_resp_by_type(
            etag,
            (
                "basicDeformations",
                "basicDeformation",
                "deformations",
                "deformation",
                "basicDisplacements",
                "basicDisplacement",
            ),
        )
        force = _get_link_resp_by_type(etag, ("basicForces", "basicForce"))
        defos.append(defo)
        forces.append(force)
    return defos, forces


def _get_link_resp_by_type(etag, etypes):
    etag = int(etag)
    ntags = ops.eleNodes(etag)
    ndim = len(ops.nodeCoord(ntags[0]))
    resp = []
    for name in etypes:
        resp = ops.eleResponse(etag, name)
        if len(resp) > 0:
            break
    if len(resp) == 0:
        resp = [0.0] * 6
    elif ndim == 2 and len(resp) == 3:
        resp = [resp[0], resp[1], 0.0, 0.0, 0.0, resp[2]]
    elif len(resp) < 6:  # don't know dofs
        resp = resp + [0.0] * (6 - len(resp))
    elif len(resp) > 6:
        resp = resp[:6]
    return resp
