import numpy as np
import openseespy.opensees as ops
import xarray as xr

from ._response_base import ResponseBase, _expand_to_uniform_array
from ...utils import OPS_ELE_TAGS

class BrickRespStepData(ResponseBase):

    def __init__(self, ele_tags=None):
        self.resp_names = [
            "Stresses",
            "Strains",
        ]
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
        stresses, strains = _get_gauss_resp(ele_tags)
        data_vars = dict()
        data_vars["Stresses"] = (["eleTags", "GaussPoints", "DOFs"], stresses)
        data_vars["Strains"] = (["eleTags", "GaussPoints", "DOFs"], strains)
        ndofs = stresses.shape[-1]
        if ndofs == 13:
            dofs = ["sigma11", "sigma22", "sigma33", "sigma12", "sigma23", "sigma13",
                    "p1", "p2", "p3", "sigma_vm", "tau_max", "sigma_oct", "tau_oct"]
        else:
            dofs = ["sigma11", "sigma22", "sigma33", "sigma12", "sigma23", "sigma13", "eta_r",
                    "p1", "p2", "p3", "sigma_vm", "tau_max", "sigma_oct", "tau_oct"]
        ds = xr.Dataset(
            data_vars=data_vars,
            coords={
                "eleTags": ele_tags,
                "GaussPoints": np.arange(stresses.shape[1])+1,
                "DOFs": dofs,
            },
            attrs={
                "sigma11, sigma22, sigma33": "Normal stress (strain) along x, y, z.",
                "sigma12, sigma23, sigma13": "Shear stress (strain).",
                "p1, p2, p3": "Principal stresses (strains).",
                "eta_r": "Ratio between the shear (deviatoric) stress and peak shear strength at the current confinement",
                "sigma_vm": "Von Mises stress.",
                "tau_max": "Maximum shear stress (strains).",
                "sigma_oct": "Octahedral normal stress (strains).",
                "tau_oct": "Octahedral shear stress (strains).",
            },
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
        dt["/SolidResponses"] = self.resp_steps
        return dt

    @staticmethod
    def read_file(dt: xr.DataTree):
        resp_steps = dt["/SolidResponses"].to_dataset()
        return resp_steps

    @staticmethod
    def read_response(dt: xr.DataTree, resp_type: str = None, ele_tags=None):
        ds = BrickRespStepData.read_file(dt)
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


def _get_gauss_resp(ele_tags):
    stresses, strains = [], []
    for etag in ele_tags:
        etag = int(etag)
        stress = ops.eleResponse(etag, "stresses")
        strain = ops.eleResponse(etag, "strains")
        strain = np.reshape(strain, (-1, 6))
        if ops.getEleClassTags(etag)[0] in OPS_ELE_TAGS.UP:
            stress = np.reshape(stress, (-1, 7))
            eta_r = stress[:, -1].reshape(-1, 1)
            strain = np.hstack((strain, eta_r))
        else:
            stress = np.reshape(stress, (-1, 6))
        stresses.append(stress)
        strains.append(strain)
    stresses = _expand_to_uniform_array(stresses)
    strains = _expand_to_uniform_array(strains)

    stress_measures = _calculate_stresses_measures(stresses[..., :6])
    strain_measures = _calculate_stresses_measures(strains[..., :6])

    stresses = np.concatenate((stresses, stress_measures), axis=-1)
    strains = np.concatenate((strains, strain_measures), axis=-1)

    return stresses, strains


def _calculate_stresses_measures(stress_array):
    """
    Calculate various stresses from the stress values at Gaussian points.

    Parameters:
    stress_array (numpy.ndarray): A 3D array with shape (num_elements, num_gauss_points, num_stresses).

    Returns:
    dict: A dictionary containing the calculated stresses for each element.
    """
    # Extract individual stress components
    sig11 = stress_array[..., 0]  # Normal stress in x-direction
    sig22 = stress_array[..., 1]  # Normal stress in y-direction
    sig33 = stress_array[..., 2]  # Normal stress in z-direction
    sig12 = stress_array[..., 3]  # Shear stress in xy-plane
    sig23 = stress_array[..., 4]  # Shear stress in yz-plane
    sig13 = stress_array[..., 5]  # Shear stress in xz-plane

    # Calculate von Mises stress for each Gauss point
    sig_vm = np.sqrt(
        0.5 * ((sig11 - sig22) ** 2 + (sig22 - sig33) ** 2 + (sig33 - sig11) ** 2)
        + 3 * (sig12 ** 2 + sig13 ** 2 + sig23 ** 2)
    )

    # Calculate principal stresses
    # Using the stress tensor to calculate eigenvalues
    stress_tensor = assemble_stress_tensor(stress_array)
    # Calculate principal stresses (eigenvalues)
    principal_stresses = np.linalg.eigvalsh(stress_tensor)  # Returns sorted eigenvalues
    p1 = principal_stresses[..., 2]  # Maximum principal stress
    p2 = principal_stresses[..., 1]  # Intermediate principal stress
    p3 = principal_stresses[..., 0]  # Minimum principal stress

    # Calculate maximum shear stress
    tau_max = np.abs(p1 - p3) / 2

    # Calculate octahedral normal stress
    sig_oct = (p1 + p2 + p3) / 3

    # Calculate octahedral shear stress
    tau_oct = 1 / 3 * np.sqrt((p1 - p2) ** 2 + (p2 - p3) ** 2 + (p3 - p1) ** 2)

    data = np.stack([p1, p2, p3, sig_vm, tau_max, sig_oct, tau_oct], axis=-1)

    return data


def assemble_stress_tensor(stress_array):
    """
    Assemble a 3D stress array into a 4D stress tensor array.
    """
    num_elements, num_gauss_points, _ = stress_array.shape
    stress_tensor = np.full((num_elements, num_gauss_points, 3, 3), np.nan)
    for i in range(num_elements):
        for j in range(num_gauss_points):
            sig11 = stress_array[i, j, 0]  # Normal stress in x-direction
            sig22 = stress_array[i, j, 1]  # Normal stress in y-direction
            sig33 = stress_array[i, j, 2]  # Normal stress in z-direction
            tau12 = stress_array[i, j, 3]  # Shear stress in xy-plane
            tau23 = stress_array[i, j, 4]  # Shear stress in yz-plane
            tau13 = stress_array[i, j, 5]  # Shear stress in xz-plane
            st = np.array(
                [
                    [sig11, tau12, tau13],
                    [tau12, sig22, tau23],
                    [tau13, tau23, sig33],
                ]
            )
            stress_tensor[i, j, ...] = st
    return np.nan_to_num(stress_tensor, nan=0.0)
