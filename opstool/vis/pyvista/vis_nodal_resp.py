from functools import partial
from typing import Union

import numpy as np
import pyvista as pv

from .plot_resp_base import PlotResponseBase
from .plot_utils import (
    PLOT_ARGS,
    _plot_all_mesh_cmap,
    _get_line_cells,
    _get_unstru_cells,
)
from .vis_model import _plot_bc, _get_bc_points_cells, _plot_mp_constraint
from ...post import loadODB


class PlotNodalResponse(PlotResponseBase):

    def __init__(
        self,
        model_info_steps,
        node_resp_steps,
        model_update,
    ):
        super().__init__(model_info_steps, node_resp_steps, model_update)

    def set_comp_resp_type(self, resp_type, component):
        if resp_type.lower() in ["disp", "dispacement"]:
            self.resp_type = "disp"
        elif resp_type.lower() in ["vel", "velocity"]:
            self.resp_type = "vel"
        elif resp_type.lower() in ["accel", "acceleration"]:
            self.resp_type = "accel"
        elif resp_type.lower() in ["reaction", "reactionforce"]:
            self.resp_type = "reaction"
        elif resp_type.lower() in ["reactionincinertia", "reactionincinertiaforce"]:
            self.resp_type = "reactionIncInertia"
        elif resp_type.lower() in ["rayleighforces", "rayleigh"]:
            self.resp_type = "rayleighForces"
        elif resp_type.lower() in ["pressure"]:
            self.resp_type = "pressure"
        else:
            raise ValueError(
                f"Invalid response type: {resp_type}. "
                "Valid options are: disp, vel, accel, reaction, reactionIncInertia, rayleighForces, pressure."
            )
        if isinstance(component, str):
            self.component = component.upper()
        else:
            self.component = list(component)

    def _get_resp_clim_peak(self, idx="absMax"):
        resps = []
        resps_norm = []
        for i in range(self.num_steps):
            da = self._get_resp_data(i, self.resp_type, self.component)
            resps.append(da)
            if da.ndim == 1:
                resps_norm.append(da)
            else:
                resps_norm.append(np.linalg.norm(da, axis=1))
        if isinstance(idx, str):
            if idx.lower() == "absmax":
                resp = [np.max(np.abs(data)) for data in resps]
                step = np.argmax(resp)
            elif idx.lower() == "max":
                resp = [np.max(data) for data in resps]
                step = np.argmax(resp)
            elif idx.lower() == "absmin":
                resp = [np.min(np.abs(data)) for data in resps]
                step = np.argmin(resp)
            elif idx.lower() == "min":
                resp = [np.min(data) for data in resps]
                step = np.argmin(resp)
            else:
                raise ValueError("Invalid argument, one of [absMax, absMin, Max, Min]")
        else:
            step = int(idx)
        max_resps = [np.max(resp) for resp in resps_norm]
        min_resps = [np.min(resp) for resp in resps_norm]
        cmin, cmax = np.min(min_resps), np.max(max_resps)
        return cmin, cmax, step

    def _get_deformation_data(self, idx):
        data = self._get_resp_data(idx, "disp", ["UX", "UY", "UZ"])
        return data

    def _get_defo_scale_factor(self):
        scalars = []
        for i in range(self.num_steps):
            defo = self._get_deformation_data(i)
            scalars.append(np.max(np.linalg.norm(defo, axis=1)))
        maxv = np.max(scalars)
        if maxv == 0:
            alpha_ = 0.0
        else:
            alpha_ = self.max_bound_size * self.pargs.scale_factor / maxv
        return float(alpha_)

    def _make_title(self, resp, step, time):
        if resp.ndim == 1:
            # max_resp = np.max(resp)
            # min_resp = np.min(resp)
            max_norm = np.max(np.abs(resp))
            min_norm = np.min(np.abs(resp))
        else:
            # max_resp = np.max(resp, axis=0)
            # min_resp = np.min(resp, axis=0)
            norm = np.linalg.norm(resp, axis=1)
            max_norm, min_norm = np.max(norm), np.min(norm)
        if self.resp_type == "disp":
            title = "Displacement"
        elif self.resp_type == "vel":
            title = "Velocity"
        elif self.resp_type == "accel":
            title = "Acceleration"
        else:
            title = f"{self.resp_type.capitalize()}"
        if isinstance(self.component, (list, tuple)):
            dof = ",".join(self.component)
        else:
            dof = self.component
        info = {
            "title": title,
            "dof": dof,
            "min": min_norm,
            "max": max_norm,
            "step": step,
            "time": time
        }
        lines = [
            f"* {info['title']}",
            f"* {info['dof']} (DOF)",
            f"{info['min']:.3E} (norm.min)",
            f"{info['max']:.3E} (norm.max)",
            f"{info['step']}(step); "
            f"{info['time']:.3f}(time)",
        ]
        if self.unit:
            info["unit"] = self.unit
            lines.insert(2, f"{info['unit']} (unit)")

        max_len = max(len(line) for line in lines)
        padded_lines = [line.rjust(max_len) for line in lines]
        text = "\n".join(padded_lines)
        return text + "\n"

    def _create_mesh(
        self,
        plotter,
        value,
        alpha=1.0,
        clim=None,
        style="surface",
        show_outline=False,
        show_origin=False,
        show_bc: bool = True,
        bc_scale: float = 1.0,
        show_mp_constraint: bool = False,
        cpos="iso"
    ):
        step = int(round(value))
        node_nodeform_coords_da = self._get_node_data(step)
        bounds = self._get_node_data(step).attrs["bounds"]
        model_dims = self._get_node_data(step).attrs["ndims"]
        line_cells, _ = _get_line_cells(self._get_line_data(step))
        _, unstru_cell_types, unstru_cells = _get_unstru_cells(
            self._get_unstru_data(step)
        )
        t_ = self.time[step]
        node_disp_da = self._get_deformation_data(step)
        node_resp_da = self._get_resp_data(step, self.resp_type, self.component)
        is_coord_equal = np.array_equal(
            node_nodeform_coords_da.coords["tags"].values,
            node_disp_da.coords["nodeTags"].values
        )
        if not is_coord_equal:
            common_coords = np.intersect1d(
                node_nodeform_coords_da.coords["tags"].values,
                node_disp_da.coords["nodeTags"].values
            )
            node_nodeform_coords_da = node_nodeform_coords_da.sel({"tags": common_coords})
            node_disp_da = node_disp_da.sel({"nodeTags": common_coords})
            node_resp_da = node_resp_da.sel({"nodeTags": common_coords})
        node_nodeform_coords = node_nodeform_coords_da.to_numpy()
        node_disp = node_disp_da.to_numpy()
        node_resp = node_resp_da.to_numpy()
        if alpha > 0.0:
            node_deform_coords = alpha * node_disp + node_nodeform_coords
        else:
            node_deform_coords = node_nodeform_coords
        if node_resp.ndim == 1:
            scalars = node_resp
        else:
            scalars = np.linalg.norm(node_resp, axis=1)
        plotter.clear_actors()  # ! clear
        point_plot, line_plot, solid_plot = _plot_all_mesh_cmap(
            plotter,
            node_deform_coords,
            line_cells,
            unstru_cells,
            unstru_cell_types,
            scalars=scalars,
            cmap=self.pargs.cmap,
            clim=clim,
            lw=self.pargs.line_width,
            show_edges=self.pargs.show_mesh_edges,
            edge_color=self.pargs.mesh_edge_color,
            edge_width=self.pargs.mesh_edge_width,
            opacity=self.pargs.mesh_opacity,
            style=style,
            show_scalar_bar=False,
            point_size=self.pargs.point_size,
            render_lines_as_tubes=self.pargs.render_lines_as_tubes,
            render_points_as_spheres=self.pargs.render_lines_as_tubes,
            show_origin=show_origin,
            pos_origin=node_nodeform_coords,
        )
        title = self._make_title(node_resp, step, t_)
        # text = plotter.add_text(
        #     title,
        #     position="upper_right",
        #     font_size=self.pargs.title_font_size/2,
        #     font="courier",
        # )
        scalar_bar = plotter.add_scalar_bar(
            title=title,
            **self.pargs.scalar_bar_kargs
        )
        # scalar_bar.SetTitle(title)
        title_prop = scalar_bar.GetTitleTextProperty()
        title_prop.SetJustificationToRight()
        title_prop.BoldOn()
        self.show_zaxis = False if np.max(model_dims) <= 2 else True
        if show_outline:
            plotter.show_bounds(
                grid=False,
                location="outer",
                bounds=bounds,
                show_zaxis=self.show_zaxis,
            )
        plotter.add_axes()
        bc_plot, mp_plot = None, None
        if show_bc:
            fixed_node_data = self._get_bc_data(step)
            if len(fixed_node_data) > 0:
                fix_tags = fixed_node_data["tags"].values
                node_disp_fix = node_disp_da.sel({"nodeTags": fix_tags}).to_numpy()
                fixed_data = fixed_node_data.to_numpy()
                fixed_dofs = fixed_data[:, -6:].astype(int)
                if alpha > 0.0:
                    fixed_coords = alpha * node_disp_fix + fixed_data[:, :3]
                else:
                    fixed_coords = fixed_data[:, :3]
                max_bound = self._get_node_data(step).attrs["maxBoundSize"]
                min_bound = self._get_node_data(step).attrs["minBoundSize"]
                s = (max_bound + min_bound) / 100 * bc_scale
                bc_plot = _plot_bc(
                    plotter,
                    fixed_dofs,
                    fixed_coords,
                    s,
                    show_zaxis=self.show_zaxis,
                    color=self.pargs.color_bc,
                )
        if show_mp_constraint:
            mp_constraint_data = self._get_mp_constraint_data(step)
            if len(mp_constraint_data) > 0:
                cells = mp_constraint_data.to_numpy()[:, :3].astype(int)
                mp_plot = _plot_mp_constraint(
                    plotter,
                    node_deform_coords,
                    cells,
                    None,
                    None,
                    self.pargs.line_width / 2,
                    self.pargs.color_constraint,
                    show_dofs=False,
                )
        self.update(plotter, cpos=cpos)
        return point_plot, line_plot, solid_plot, scalar_bar, bc_plot, mp_plot

    def _update_mesh(
        self,
        value,
        point_plot=None,
        line_plot=None,
        solid_plot=None,
        scalar_bar=None,
        bc_plot=None,
        mp_plot=None,
        alpha=1.0,
        bc_scale: float = 1.0
    ):
        step = int(round(value))
        po = self._get_node_data(step).to_numpy()
        t_ = self.time[step]
        if alpha > 0.0:
            node_disp = self._get_deformation_data(step).to_numpy()
            points = alpha * node_disp + po
        else:
            points = po
        node_resp = self._get_resp_data(step, self.resp_type, self.component)
        if node_resp.ndim == 1:
            scalars = node_resp
        else:
            scalars = np.linalg.norm(node_resp, axis=1)
        if point_plot:
            point_plot["scalars"] = scalars
            point_plot.points = points
        if line_plot:
            line_plot["scalars"] = scalars
            line_plot.points = points
        if solid_plot:
            solid_plot["scalars"] = scalars
            solid_plot.points = points
        # plotter.update_scalar_bar_range(clim=[np.min(scalars), np.max(scalars)])
        if scalar_bar:
            title = self._make_title(node_resp, step, t_)
            # cbar.SetTitle(title)
            scalar_bar.SetTitle(title)
        if mp_plot:
            bc_plot.points = points
        if bc_plot:
            fixed_node_data = self._get_bc_data(step)
            fixed_data = fixed_node_data.to_numpy()
            fixed_dofs = fixed_data[:, -6:].astype(int)
            fixed_coords = fixed_data[:, :3]
            max_bound = self._get_node_data(step).attrs["maxBoundSize"]
            min_bound = self._get_node_data(step).attrs["minBoundSize"]
            s = (max_bound + min_bound) / 100 * bc_scale
            bc_points, _ = _get_bc_points_cells(
                fixed_coords,
                fixed_dofs,
                s,
                self.show_zaxis,
            )
            bc_plot.points = bc_points

    def plot_slide(
        self,
        plotter,
        alpha=1.0,
        show_defo=True,
        show_bc: bool = True,
        bc_scale: float = 1.0,
        show_mp_constraint: bool = True,
        style="surface",
        show_outline=False,
        show_origin=False,
        cpos="iso",
        **kargs,
    ):
        cmin, cmax, _ = self._get_resp_clim_peak()
        clim = (cmin, cmax)
        if show_defo:
            alpha_ = self._get_defo_scale_factor()
            alpha_ = alpha_ * alpha if alpha else alpha_
        else:
            alpha_ = 0.0
        if self.ModelUpdate:
            func = partial(
                self._create_mesh,
                plotter,
                alpha=alpha_,
                clim=clim,
                show_bc=show_bc,
                bc_scale=bc_scale,
                show_mp_constraint=show_mp_constraint,
                style=style,
                show_outline=show_outline,
                show_origin=show_origin,
                cpos=cpos
            )
        else:
            point_plot, line_plot, solid_plot, cbar, bc_plot, mp_plot = (
                self._create_mesh(
                    plotter,
                    self.num_steps - 1,
                    alpha=alpha_,
                    clim=clim,
                    show_bc=show_bc,
                    bc_scale=bc_scale,
                    show_mp_constraint=show_mp_constraint,
                    style=style,
                    show_outline=show_outline,
                    show_origin=show_origin,
                    cpos=cpos
                )
            )
            func = partial(
                self._update_mesh,
                point_plot=point_plot,
                line_plot=line_plot,
                solid_plot=solid_plot,
                scalar_bar=cbar,
                bc_plot=bc_plot,
                mp_plot=mp_plot,
                alpha=alpha_,
                bc_scale=bc_scale,
                **kargs,
            )
        plotter.add_slider_widget(
            func,
            [0, self.num_steps - 1],
            value=self.num_steps - 1,
            pointa=(0.01, 0.925),
            pointb=(0.45, 0.925),
            title="Step",
            title_opacity=1,
            # title_color="black",
            fmt="%.0f",
            title_height=0.03,
            slider_width=0.03,
            tube_width=0.008,
        )

    def plot_peak_step(
        self,
        plotter,
        step="absMax",
        alpha=1.0,
        show_defo=True,
        show_bc: bool = True,
        bc_scale: float = 1.0,
        show_mp_constraint: bool = True,
        style="surface",
        show_outline=False,
        show_origin=False,
        cpos="iso",
    ):
        cmin, cmax, step = self._get_resp_clim_peak(idx=step)
        clim = (cmin, cmax)
        if show_defo:
            alpha_ = self._get_defo_scale_factor()
            alpha_ = alpha_ * alpha if alpha else alpha_
        else:
            alpha_ = 0.0
        self._create_mesh(
            plotter=plotter,
            value=step,
            alpha=alpha_,
            clim=clim,
            show_bc=show_bc,
            bc_scale=bc_scale,
            show_mp_constraint=show_mp_constraint,
            style=style,
            show_outline=show_outline,
            show_origin=show_origin,
            cpos=cpos
        )

    def plot_anim(
        self,
        plotter,
        alpha=1.0,
        show_defo=True,
        framerate: int = None,
        savefig: str = "NodalRespAnimation.gif",
        show_bc: bool = True,
        bc_scale: float = 1.0,
        show_mp_constraint: bool = True,
        style="surface",
        show_outline=False,
        show_origin=False,
        cpos="iso"
    ):
        if framerate is None:
            framerate = np.ceil(self.num_steps / 10)
        if savefig.endswith(".gif"):
            plotter.open_gif(savefig, fps=framerate)
        else:
            plotter.open_movie(savefig, framerate=framerate)
        cmin, cmax, max_step = self._get_resp_clim_peak()
        clim = (cmin, cmax)
        if show_defo:
            alpha_ = self._get_defo_scale_factor()
            alpha_ = alpha_ * alpha if alpha else alpha_
        else:
            alpha_ = 0.0
        # plotter.write_frame()  # write initial data
        if self.ModelUpdate:
            for step in range(self.num_steps):
                self._create_mesh(
                    plotter=plotter,
                    value=step,
                    alpha=alpha_,
                    clim=clim,
                    show_bc=show_bc,
                    bc_scale=bc_scale,
                    show_mp_constraint=show_mp_constraint,
                    style=style,
                    show_outline=show_outline,
                    show_origin=show_origin,
                    cpos=cpos
                )
                plotter.write_frame()
        else:
            point_plot, line_plot, solid_plot, text, bc_plot, mp_plot = (
                self._create_mesh(
                    plotter,
                    self.num_steps - 1,
                    alpha=alpha_,
                    show_bc=show_bc,
                    bc_scale=bc_scale,
                    show_mp_constraint=show_mp_constraint,
                    style=style,
                    show_outline=show_outline,
                    show_origin=show_origin,
                    cpos=cpos
                )
            )
            plotter.write_frame()
            for step in range(self.num_steps):
                self._update_mesh(
                    value=step,
                    point_plot=point_plot,
                    line_plot=line_plot,
                    solid_plot=solid_plot,
                    text=text,
                    bc_plot=bc_plot,
                    mp_plot=mp_plot,
                    alpha=alpha_,
                    bc_scale=bc_scale,
                )
                plotter.write_frame()

    def update(self, plotter, cpos):
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


def plot_nodal_responses(
    odb_tag: Union[int, str] = 1,
    slides: bool = False,
    step: Union[int, str] = "absMax",
    scale: float = 1.0,
    show_defo: bool = True,
    resp_type: str = "disp",
    resp_dof: Union[list, tuple, str] = ("UX", "UY", "UZ"),
    unit_symbol: str = None,
    cpos: str = "iso",
    show_bc: bool = True,
    bc_scale: float = 1.0,
    show_mp_constraint: bool = False,
    show_undeformed: bool = False,
    style: str = "surface",
    show_outline: bool = False,
) -> pv.Plotter:
    """Visualizing Node Responses.

    Parameters
    ----------
    odb_tag: Union[int, str], default: 1
        Tag of output databases (ODB) to be visualized.
    slides: bool, default: False
        Display the response for each step in the form of a slideshow.
        Otherwise, show the step with the following ``step`` parameter.
    step: Union[int, str], default: "absMax"
        If slides = False, this parameter will be used as the step to plot.
        If str, Optional: [absMax, absMin, Max, Min].
        If int, this step will be demonstrated (counting from 0).
    scale: float, default: 1.0
        Scales the size of the deformation presentation.
    show_defo: bool, default: True
        Whether to display the deformed shape.
    resp_type: str, default: disp
        Type of response to be visualized.
        Optional: "disp", "vel", "accel", "reaction", "reactionIncInertia", "rayleighForces", "pressure".
    resp_dof: str, default: ("UX", "UY", "UZ")
        Component to be visualized.
        Optional: "UX", "UY", "UZ", "RX", "RY", "RZ".
        You can also pass on a list or tuple to display multiple dimensions, for example, ["UX", "UY"],
        ["UX", "UY", "UZ"], ["RX", "RY", "RZ"], ["RX", "RY"], ["RY", "RZ"], ["RX", "RZ"], and so on.

        .. Note::
            If the nodes include fluid pressure dof,
            such as those used for ...UP elements, the pore pressure should be extracted using ``resp_type="vel"``,
            and ``resp_dof="UZ"``.

    unit_symbol: str, default: None
        Unit symbol to be displayed in the plot.
    cpos: str, default: iso
        Model display perspective, optional: "iso", "xy", "yx", "xz", "zx", "yz", "zy".
        If 3d, defaults to "iso". If 2d, defaults to "xy".
    show_bc: bool, default: True
        Whether to display boundary supports.
    bc_scale: float, default: 1.0
        Scale the size of boundary support display.
    show_mp_constraint: bool, default: False
        Whether to show multipoint (MP) constraint.
    show_undeformed: bool, default: False
        Whether to show the undeformed shape of the model.
    show_outline: bool, default: False
        Whether to display the outline of the model.
    style: str, default: surface
        Visualization mesh style of surfaces and solids.
        One of the following: style='surface', style='wireframe', style='points', style='points_gaussian'.
        Defaults to 'surface'. Note that 'wireframe' only shows a wireframe of the outer geometry.

    Returns
    -------
    Plotting object of PyVista to display vtk meshes or numpy arrays.
    See `pyvista.Plotter <https://docs.pyvista.org/api/plotting/_autosummary/pyvista.plotter>`_.

    You can use
    `Plotter.show <https://docs.pyvista.org/api/plotting/_autosummary/pyvista.plotter.show#pyvista.Plotter.show>`_.
    to display the plotting window.

    You can also use
    `Plotter.export_html <https://docs.pyvista.org/api/plotting/_autosummary/pyvista.plotter.export_html#pyvista.Plotter.export_html>`_.
    to export this plotter as an interactive scene to an HTML file.
    """
    model_info_steps, model_update, node_resp_steps = loadODB(
        odb_tag, resp_type="Nodal"
    )
    plotter = pv.Plotter(
        notebook=PLOT_ARGS.notebook,
        line_smoothing=PLOT_ARGS.line_smoothing,
        polygon_smoothing=PLOT_ARGS.polygon_smoothing,
        off_screen=PLOT_ARGS.off_screen,
    )
    plotbase = PlotNodalResponse(model_info_steps, node_resp_steps, model_update)
    plotbase.set_unit_symbol(unit_symbol)
    plotbase.set_comp_resp_type(resp_type=resp_type, component=resp_dof)
    if slides:
        plotbase.plot_slide(
            plotter,
            alpha=scale,
            show_defo=show_defo,
            show_bc=show_bc,
            bc_scale=bc_scale,
            show_mp_constraint=show_mp_constraint,
            style=style,
            show_outline=show_outline,
            show_origin=show_undeformed,
            cpos=cpos
        )
    else:
        plotbase.plot_peak_step(
            plotter,
            step=step,
            alpha=scale,
            show_defo=show_defo,
            show_bc=show_bc,
            bc_scale=bc_scale,
            show_mp_constraint=show_mp_constraint,
            style=style,
            show_outline=show_outline,
            show_origin=show_undeformed,
            cpos=cpos
        )
    if PLOT_ARGS.anti_aliasing:
        plotter.enable_anti_aliasing(PLOT_ARGS.anti_aliasing)
    return plotbase.update(plotter, cpos)


def plot_nodal_responses_animation(
    odb_tag: Union[int, str] = 1,
    framerate: int = None,
    savefig: str = "NodalRespAnimation.gif",
    off_screen: bool = True,
    scale: float = 1.0,
    show_defo: bool = True,
    resp_type: str = "disp",
    resp_dof: Union[list, tuple, str] = ("UX", "UY", "UZ"),
    unit_symbol: str = None,
    show_bc: bool = True,
    bc_scale: float = 1.0,
    show_mp_constraint: bool = False,
    cpos: str = "iso",
    show_undeformed: bool = False,
    style: str = "surface",
    show_outline: bool = False,
) -> pv.Plotter:
    """Visualize node response animation.

    Parameters
    ----------
    odb_tag: Union[int, str], default: 1
        Tag of output databases (ODB) to be visualized.
    framerate: int, default: 5
        Framerate for the display, i.e., the number of frames per second.
    savefig: str, default: NodalRespAnimation.gif
        Path to save the animation. The suffix can be ``.gif`` or ``.mp4``.
    off_screen: bool, default: True
        Whether to display the plotting window.
        If True, the plotting window will not be displayed.
    scale: float, default: 1.0
        Scales the size of the deformation presentation.
    show_defo: bool, default: True
        Whether to display the deformed shape.
    resp_type: str, default: disp
        Type of response to be visualized.
        Optional: "disp", "vel", "accel", "reaction", "reactionIncInertia", "rayleighForces", "pressure".
    resp_dof: str, default: ("UX", "UY", "UZ")
        Component to be visualized.
        Optional: "UX", "UY", "UZ", "RX", "RY", "RZ".
        You can also pass on a list or tuple to display multiple dimensions, for example, ["UX", "UY"],
        ["UX", "UY", "UZ"], ["RX", "RY", "RZ"], ["RX", "RY"], ["RY", "RZ"], ["RX", "RZ"], and so on.
    unit_symbol: str, default: None
        Unit symbol to be displayed in the plot.
    show_bc: bool, default: True
        Whether to display boundary supports.
    bc_scale: float, default: 1.0
        Scale the size of boundary support display.
    show_mp_constraint: bool, default: False
        Whether to show multipoint (MP) constraint.
    cpos: str, default: iso
        Model display perspective, optional: "iso", "xy", "yx", "xz", "zx", "yz", "zy".
        If 3d, defaults to "iso". If 2d, defaults to "xy".
    show_undeformed: bool, default: False
        Whether to show the undeformed shape of the model.
    show_outline: bool, default: False
        Whether to display the outline of the model.
    style: str, default: surface
        Visualization mesh style of surfaces and solids.
        One of the following: style='surface', style='wireframe', style='points', style='points_gaussian'.
        Defaults to 'surface'. Note that 'wireframe' only shows a wireframe of the outer geometry.

    Returns
    -------
    Plotting object of PyVista to display vtk meshes or numpy arrays.
    See `pyvista.Plotter <https://docs.pyvista.org/api/plotting/_autosummary/pyvista.plotter>`_.

    You can use
    `Plotter.show <https://docs.pyvista.org/api/plotting/_autosummary/pyvista.plotter.show#pyvista.Plotter.show>`_.
    to display the plotting window.

    You can also use
    `Plotter.export_html <https://docs.pyvista.org/api/plotting/_autosummary/pyvista.plotter.export_html#pyvista.Plotter.export_html>`_.
    to export this plotter as an interactive scene to an HTML file.
    """
    model_info_steps, model_update, node_resp_steps = loadODB(
        odb_tag, resp_type="Nodal"
    )
    plotter = pv.Plotter(
        notebook=PLOT_ARGS.notebook,
        line_smoothing=PLOT_ARGS.line_smoothing,
        polygon_smoothing=PLOT_ARGS.polygon_smoothing,
        off_screen=off_screen,
    )
    plotbase = PlotNodalResponse(model_info_steps, node_resp_steps, model_update)
    plotbase.set_comp_resp_type(resp_type=resp_type, component=resp_dof, unit=unit_symbol)
    plotbase.plot_anim(
        plotter,
        alpha=scale,
        show_defo=show_defo,
        framerate=framerate,
        savefig=savefig,
        show_bc=show_bc,
        bc_scale=bc_scale,
        show_mp_constraint=show_mp_constraint,
        style=style,
        show_outline=show_outline,
        show_origin=show_undeformed,
        cpos=cpos
    )
    if PLOT_ARGS.anti_aliasing:
        plotter.enable_anti_aliasing(PLOT_ARGS.anti_aliasing)

    print(f"Animation saved to {savefig}!")

    return plotbase.update(plotter, cpos)
