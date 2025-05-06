import xarray as xr
import openseespy.opensees as ops

from ._response_base import ResponseBase


class TrussRespStepData(ResponseBase):

    def __init__(self, ele_tags=None):
        self.resp_names = ["axialForce", "axialDefo", "Stress", "Strain"]
        self.resp_steps = None
        self.step_track = 0
        self.ele_tags = ele_tags
        self.times = []
        self.initialize()

    def initialize(self):
        self.resp_steps = []
        self.add_data_one_step(self.ele_tags)
        self.times = [0.0]
        self.step_track = 0

    def reset(self):
        self.initialize()

    def add_data_one_step(self, ele_tags):
        data = _get_truss_resp(ele_tags)
        data_vars = {}
        if len(ele_tags) > 0:
            for name, data_ in zip(self.resp_names, data):
                data_vars[name] = (["eleTags"], data_)
            ds = xr.Dataset(data_vars=data_vars, coords={"eleTags": ele_tags})
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
        dt["/TrussResponses"] = self.resp_steps
        return dt

    @staticmethod
    def read_file(dt: xr.DataTree):
        resp_steps = dt["/TrussResponses"].to_dataset()
        return resp_steps

    @staticmethod
    def read_response(dt: xr.DataTree, resp_type: str = None, ele_tags=None):
        ds = TrussRespStepData.read_file(dt)
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


def _get_truss_resp(truss_tags):
    forces, defos, stressss, strains = [], [], [], []
    for etag in truss_tags:
        etag = int(etag)
        force = ops.eleResponse(etag, "axialForce")
        force = _reshape_resp(force)
        defo = ops.eleResponse(etag, "basicDeformation")
        defo = _reshape_resp(defo)
        stress = ops.eleResponse(etag, "material", "1", "stress")
        stress = _reshape_resp(stress)

        strain = ops.eleResponse(etag, "material", "1", "strain")
        if len(strain) == 0:
            strain = ops.eleResponse(etag, "section", "1", "deformation")
        strain = _reshape_resp(strain)

        forces.append(force)
        defos.append(defo)
        stressss.append(stress)
        strains.append(strain)
    return forces, defos, stressss, strains

def _reshape_resp(data):
    if len(data) == 0:
        return 0.0
    else:
        return data[0]
