import warnings
import numpy as np
import xarray as xr
import openseespy.opensees as ops
from typing import Union

from ._response_base import ResponseBase


class FiberSecData:
    ELE_SEC_TAGS = []
    ELE_SEC_KEYS = []
    FIBER_GEO_DATA = dict()

    @classmethod
    def add_data(cls, ele_tags=None):
        if ele_tags is None:
            ele_tags = []
        elif isinstance(ele_tags, str) and ele_tags.lower() == "all":
            ele_tags = ops.getEleTags()
        else:
            ele_tags = np.atleast_1d(ele_tags)
        for ele_tag in ele_tags:
            sec_locs = ops.sectionLocation(int(ele_tag))
            if isinstance(sec_locs, list) and len(sec_locs) > 0:
                for i in range(len(sec_locs)):
                    cls.ELE_SEC_TAGS.append((ele_tag, i + 1))
        for ele_sec_i in cls.ELE_SEC_TAGS:
            ele_tag = ele_sec_i[0]
            sec_tag = ele_sec_i[1]
            key = f"{ele_tag}-{sec_tag}"
            cls.ELE_SEC_KEYS.append(key)
            fiber_data = _get_fiber_sec_data(ele_tag, sec_tag)
            cls.FIBER_GEO_DATA[key] = fiber_data[:, :4]

    @classmethod
    def get_ele_sec_tags(cls):
        return cls.ELE_SEC_TAGS

    @classmethod
    def get_ele_sec_keys(cls):
        return cls.ELE_SEC_KEYS

    @classmethod
    def get_fiber_geo_data(cls):
        return cls.FIBER_GEO_DATA


def set_fiber_sec_data(ele_tags: Union[str, list] = None):
    FiberSecData.add_data(ele_tags)


class FiberSecRespStepData(ResponseBase):

    def __init__(self):
        self.ELE_SEC_TAGS = FiberSecData.get_ele_sec_tags()
        self.ELE_SEC_KEYS = FiberSecData.get_ele_sec_keys()
        self.FIBER_GEO_DATA = FiberSecData.get_fiber_geo_data()

        self.resp_steps = None
        self.times = []
        self.step_track = 0
        self.initialize()

    def initialize(self):
        self.resp_steps = []
        self.add_data_one_step()
        self.step_track = 0
        self.times = [0.0]

    def reset(self):
        self.initialize()

    def add_data_one_step(self):
        stressAndStrain = dict()
        defoAndForce = []
        for ele_sec in self.ELE_SEC_TAGS:
            ele_tag = ele_sec[0]
            sec_num = ele_sec[1]
            key = f"sd-{ele_tag}-{sec_num}"
            fiber_data = _get_fiber_sec_data(ele_tag, sec_num)
            stressAndStrain[key] = fiber_data[:, -2:]
            # -----------------------------------------------------------------------
            defo_forces = ops.eleResponse(
                ele_tag, "section", f"{sec_num}", "forceAndDeformation"
            )
            if len(defo_forces) == 4:
                defo_forces = [
                    defo_forces[0],  # epsilon
                    defo_forces[1],  # kappaz
                    0.0,  # kappay
                    0.0,  # theta
                    defo_forces[2],  # P
                    defo_forces[3],  # Mz
                    0.0,  # My
                    0.0,  # T
                ]
            defoAndForce.append(defo_forces)
            # ---------------------------------------------------------------
        data_vars = {}
        if len(defoAndForce) > 0:
            for name, data_ in stressAndStrain.items():
                data_vars[name] = (("fiberTags", "stress-strain"), data_)
            data_vars["defoAndForce"] = (("eleSecs", "defo-force"), defoAndForce)
            ds = xr.Dataset(
                data_vars=data_vars,
                coords={
                    "eleSecs": self.ELE_SEC_KEYS,
                    "stress-strain": ["stress", "strain"],
                    "defo-force": [
                        "eps",
                        "kappaz",
                        "kappay",
                        "theta",
                        "P",
                        "Mz",
                        "My",
                        "T",
                    ],
                },
            )
        else:
            ds = xr.Dataset(data_vars={"none": xr.DataArray([])})

        self.resp_steps.append(ds)
        self.step_track += 1
        self.times.append(ops.getTime())

    def _to_xarray(self):
        self.resp_steps = xr.concat(self.resp_steps, dim="time", join="outer")
        self.resp_steps.coords["time"] = self.times
        for key, value in self.FIBER_GEO_DATA.items():
            self.resp_steps["geo-" + key] = xr.DataArray(
                value,
                coords={"data": ["y", "z", "area", "mat"]},
                dims=("fiberTags", "data"),
                name="FiberSectionResponses",
            )

    def get_data(self):
        return self.resp_steps

    def get_track(self):
        return self.step_track

    def save_file(self, dt: xr.DataTree):
        self._to_xarray()
        dt["/FiberSectionResponses"] = self.resp_steps
        return dt

    @staticmethod
    def read_file(dt: xr.DataTree):
        resp_steps = dt["/FiberSectionResponses"].to_dataset()
        return resp_steps


def _get_fiber_sec_data(ele_tag: int, sec_num: int = 1):
    """Get the fiber sec data for a beam element.

    Parameters
    ----------
    ele_tag: int
        The element tag to which the sec is to be displayed.
    sec_num: int
        Which integration point sec is displayed, tag from 1 from segment i to j.

    Returns
    -------
    fiber_data: ArrayLike
    """
    # Extract fiber data using eleResponse() command
    sec_loc = ops.sectionLocation(ele_tag)
    if len(sec_loc) == 0:
        raise ValueError(f"eleTag {ele_tag} have no fiber sec!")
    if sec_num > len(sec_loc):
        warnings.warn(
            f"Section number {sec_num} larger than max number {len(sec_loc)} of elemeng with tag {ele_tag}!"
            f"Section number {sec_num} set to {len(sec_loc)}!"
        )
        sec_num = len(sec_loc)
    ele_tag = int(ele_tag)
    fiber_data = ops.eleResponse(ele_tag, "sec", f"{sec_num}", "fiberData2")
    if len(fiber_data) == 0:
        fiber_data = ops.eleResponse(ele_tag, "sec", "fiberData2")
    # From column 1 to 6: "yCoord", "zCoord", "area", 'mat', "stress", "strain"
    fiber_data = np.reshape(fiber_data, (-1, 6))  # to six columns
    return fiber_data
