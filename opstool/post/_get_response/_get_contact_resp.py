import openseespy.opensees as ops
import xarray as xr

from ._response_base import ResponseBase
from ...utils import suppress_ops_print


class ContactRespStepData(ResponseBase):

    def __init__(self, ele_tags=None):
        self.resp_names = [
            "localForces", "localDisp", "slips"
        ]
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
        with suppress_ops_print():
            forces, defos, slips = _get_contact_resp(ele_tags)
        data_vars = {}
        if len(ele_tags) > 0:
            data_vars["localForces"] = (["eleTags", "localDOFs"], forces)
            data_vars["localDisp"] = (["eleTags", "localDOFs"], defos)
            data_vars["slips"] = (["eleTags", "slipDOFs"], slips)
            ds = xr.Dataset(
                data_vars=data_vars,
                coords={
                    "eleTags": ele_tags,
                    "localDOFs": ["N", "Tx", "Ty"],
                    "slipDOFs": ["Tx", "Ty"],
                },
                attrs={
                    "N": "Normal force or deformation",
                    "Tx": "Tangential force or deformation in the x-direction",
                    "Ty": "Tangential force or deformation in the y-direction",
                }
            )
        else:
            data_vars["localForces"] = xr.DataArray([])
            data_vars["localDisp"] = xr.DataArray([])
            data_vars["slips"] = xr.DataArray([])
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
        dt["/ContactResponses"] = self.resp_steps
        return dt

    @staticmethod
    def read_file(dt: xr.DataTree):
        resp_steps = dt["/ContactResponses"].to_dataset()
        return resp_steps

    @staticmethod
    def read_response(dt: xr.DataTree, resp_type: str = None, ele_tags=None):
        ds = ContactRespStepData.read_file(dt)
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


def _get_contact_resp(link_tags):
    defos, forces, slips = [], [], []
    for etag in link_tags:
        etag = int(etag)
        defo = _get_contact_resp_by_type(
            etag,("localDisplacement", "localDispJump"),
        )
        force = _get_contact_resp_by_type(
            etag, ("localForce", "localForces", "forcescalars", "forcescalar")
        )
        slip = _get_contact_resp_by_type(etag, ("slip",), slip=True)
        defos.append(defo)
        forces.append(force)
        slips.append(slip)
    return forces, defos, slips


def _get_contact_resp_by_type(etag, etypes, slip=False):
    etag = int(etag)
    resp = []
    for name in etypes:
        resp = ops.eleResponse(etag, name)
        if len(resp) > 0:
            break
    if not slip:
        if len(resp) == 0:
            resp = [0.0] * 3
        elif len(resp) == 2:
            resp = [resp[0], resp[1], 0.0]
        else:
            resp = [resp[0], resp[1], resp[2]]
    else:
        if len(resp) == 0:
            resp = [0.0] * 2
        elif len(resp) == 1:
            resp = [resp[0], resp[0]]
        else:
            resp = [resp[0], resp[1]]
    return resp