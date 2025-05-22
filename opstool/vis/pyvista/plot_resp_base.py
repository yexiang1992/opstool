from typing import Optional

import numpy as np
import pyvista as pv
import xarray as xr

from .plot_utils import PLOT_ARGS

slider_widget_args = {
    "pointa": (0.01, 0.925),
    "pointb": (0.45, 0.925),
    "title": "Step",
    "title_opacity": 1,
    # title_color="black",
    "fmt": "%.0f",
    "title_height": 0.03,
    "slider_width": 0.03,
    "tube_width": 0.008,
}


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
        self.show_zaxis = not np.max(model_dims) <= 2

        # ------------------------------------------------------------
        self.pargs = PLOT_ARGS
        self.resp_step = None  # response data
        self.resp_type = None
        self.component = None  # component to be visualized
        self.unit = ""  # unit symbol

        self.slider_widget_args = slider_widget_args

        pv.set_plot_theme(PLOT_ARGS.theme)

    def set_unit_symbol(self, symbol: Optional[str] = None):
        # unit
        if symbol is not None:
            self.unit = symbol

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
        return None

    def update(self, plotter: pv.Plotter, cpos):
        cpos = cpos.lower()
        viewer = {
            "xy": plotter.view_xy,
            "yx": plotter.view_yx,
            "xz": plotter.view_xz,
            "zx": plotter.view_zx,
            "yz": plotter.view_yz,
            "zy": plotter.view_zy,
            "iso": plotter.view_isometric,
        }
        if not self.show_zaxis and cpos not in ["xy", "yx"]:
            cpos = "xy"
            plotter.enable_2d_style()
            plotter.enable_parallel_projection()
        viewer[cpos]()
        return plotter
