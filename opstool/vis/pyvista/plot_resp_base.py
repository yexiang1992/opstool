import numpy as np
import pyvista as pv
import xarray as xr

from .plot_utils import PLOT_ARGS


class PlotResponseBase:
    def __init__(
        self,
        model_info_steps: dict[str, xr.DataArray],
        resp_step: xr.Dataset,
        model_update: bool,
    ):
        self.ModelInfoSteps = model_info_steps
        self.RespSteps = resp_step
        self.ModelUpdate = model_update
        self.time = self.RespSteps.coords["time"].values
        self.num_steps = len(self.time)

        self.points_origin = self._get_node_data(0).to_numpy()
        self.bounds = self._get_node_data(0).attrs["bounds"]
        self.max_bound_size = self._get_node_data(0).attrs["maxBoundSize"]
        model_dims = self._get_node_data(0).attrs["ndims"]
        # # show z-axis in 3d view
        self.show_zaxis = False if np.max(model_dims) <= 2 else True

        # ------------------------------------------------------------
        self.pargs = PLOT_ARGS
        self.resp_step = None  # response data
        self.resp_type = None
        self.component = None  # component to be visualized

        pv.set_plot_theme(PLOT_ARGS.theme)

    def _get_model_data(self, key, idx):
        dims = self.ModelInfoSteps[key].dims
        if self.ModelUpdate:
            da = self.ModelInfoSteps[key].isel(time=idx)
            da = da.dropna(dim=dims[1], how="any")
        else:
            da = self.ModelInfoSteps[key].isel(time=0)
        # tags = da.coords[dims[1]].values
        return da

    def _get_node_data(self, idx):
        return self._get_model_data("NodalData", idx)

    def _get_line_data(self, idx):
        return self._get_model_data("AllLineElesData", idx)

    def _get_unstru_data(self, idx):
        return self._get_model_data("UnstructuralData", idx)

    def _get_bc_data(self, idx):
        return self._get_model_data("FixedNodalData", idx)

    def _get_mp_constraint_data(self, idx):
        return self._get_model_data("MPConstraintData", idx)

    def _get_mp_force_data(self, idx):
        return self._get_model_data("MPForceData", idx)

    def _get_resp_data(self, time_idx, resp_type, component=None):
        # dataset
        dims = self.RespSteps[resp_type].dims
        da = self.RespSteps[resp_type].isel(time=time_idx)
        if self.ModelUpdate:
            da = da.dropna(dim=dims[1], how="all")
        if da.ndim == 1 or component is None:
            return da
        elif da.ndim == 2:
            return da.loc[:, component]
        elif da.ndim == 3:
            return da.loc[:, :, component]
