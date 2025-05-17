from functools import partial
from typing import Union

import numpy as np
import pyvista as pv

from .plot_resp_base import PlotResponseBase
from .plot_utils import (
    PLOT_ARGS,
    _plot_all_mesh,
    _plot_lines,
    _plot_lines_cmap,
    _get_line_cells,
    _get_unstru_cells,
)
from ...post import loadODB
from ...utils import gram_schmidt


class PlotTrussResponse(PlotResponseBase):

    def __init__(self, model_info_steps, truss_resp_step, model_update):
        super().__init__(model_info_steps, truss_resp_step, model_update)

    def _get_truss_data(self, step):
        return self._get_model_data("TrussData", step)

    def _plot_all_mesh(self, plotter, color="gray", step=0):
        pos = self._get_node_data(step).to_numpy()
        line_cells, _ = _get_line_cells(self._get_line_data(step))
        _, unstru_cell_types, unstru_cells = _get_unstru_cells(
            self._get_unstru_data(step)
        )

        _plot_all_mesh(
            plotter,
            pos,
            line_cells,
            unstru_cells,
            unstru_cell_types,
            color=color,
            render_lines_as_tubes=False,
        )

    def _set_resp_type(self, resp_type: str):
        if resp_type.lower() in ["axialforce", "force"]:
            resp_type = "axialForce"
        elif resp_type.lower() in ["axialdefo", "axialdeformation", "deformation"]:
            resp_type = "axialDefo"
        elif resp_type.lower() in ["stress", "axialstress"]:
            resp_type = "Stress"
        elif resp_type.lower() in ["strain", "axialstrain"]:
            resp_type = "Strain"
        else:
            raise ValueError(
                f"Not supported response type {resp_type}! "
                "Valid options are: axialForce, axialDefo, Stress, Strain."
            )
        self.resp_type = resp_type

    def _make_truss_info(self, ele_tags, step):
        pos = self._get_node_data(step).to_numpy()
        truss_data = self._get_truss_data(step)
        if ele_tags is None:
            truss_tags = truss_data.coords["eleTags"].values
            truss_cells = truss_data.to_numpy().astype(int)
        else:
            truss_tags = np.atleast_1d(ele_tags)
            truss_cells = truss_data.sel(eleTags=truss_tags).to_numpy().astype(int)
        truss_node_coords = []
        truss_cells_new = []
        for i, cell in enumerate(truss_cells):
            nodei, nodej = cell[1:]
            truss_node_coords.append(pos[nodei])
            truss_node_coords.append(pos[nodej])
            truss_cells_new.append([2, 2 * i, 2 * i + 1])
        truss_node_coords = np.array(truss_node_coords)
        return truss_tags, truss_node_coords, truss_cells_new

    def refactor_resp_step(self, resp_type: str, ele_tags):
        self._set_resp_type(resp_type)
        resps = []
        if self.ModelUpdate or ele_tags is not None:
            for i in range(self.num_steps):
                truss_tags, _, _ = self._make_truss_info(ele_tags, i)
                da = self._get_resp_data(i, self.resp_type)
                da = da.sel(eleTags=truss_tags)
                resps.append(da)
        else:
            for i in range(self.num_steps):
                da = self._get_resp_data(i, self.resp_type)
                resps.append(da)
        self.resp_step = resps  # update

    def _get_resp_peak(self, idx="absMax"):
        if isinstance(idx, str):
            if idx.lower() == "absmax":
                resp = [np.max(np.abs(data)) for data in self.resp_step]
                step = np.argmax(resp)
            elif idx.lower() == "max":
                resp = [np.max(data) for data in self.resp_step]
                step = np.argmax(resp)
            elif idx.lower() == "absmin":
                resp = [np.min(np.abs(data)) for data in self.resp_step]
                step = np.argmin(resp)
            elif idx.lower() == "min":
                resp = [np.min(data) for data in self.resp_step]
                step = np.argmin(resp)
            else:
                raise ValueError("Invalid argument, one of [absMax, absMin, Max, Min]")
        else:
            step = int(idx)
        resp = self.resp_step[step]
        maxv = np.amax(np.abs(resp))
        if maxv == 0:
            alpha_ = 0.0
        else:
            alpha_ = self.max_bound_size * self.pargs.scale_factor / maxv
        cmin, cmax = self._get_truss_resp_clim()
        return step, (cmin, cmax), float(alpha_)

    def _get_truss_resp_clim(self):
        maxv = [np.max(data) for data in self.resp_step]
        minv = [np.min(data) for data in self.resp_step]
        cmin, cmax = np.min(minv), np.max(maxv)
        return cmin, cmax

    def _make_title(self, scalars, step, time):
        info = {
            "title": self.resp_type.capitalize(),
            "min": np.min(scalars),
            "max": np.max(scalars),
            "step": step,
            "time": time
        }
        lines = [
            f"* {info['title']}",
            f"{info['min']:.3E} (min)",
            f"{info['max']:.3E} (max)",
            f"{info['step']} (step)",
            f"{info['time']:.3f} (time)",
        ]
        if self.unit:
            info["unit"] = self.unit
            lines.insert(1, f"{info['unit']} (unit)")
        max_len = max(len(line) for line in lines)
        padded_lines = [line.rjust(max_len) for line in lines]
        text = "\n".join(padded_lines)
        return text + "\n"

    def _create_mesh(
        self,
        plotter,
        value,
        ele_tags=None,
        show_values=True,
        plot_all_mesh=True,
        clim=None,
        alpha=1.0,
        line_width=1.5,
        cpos="iso"
    ):
        step = int(round(value))
        truss_tags, truss_coords, truss_cells = self._make_truss_info(ele_tags, step)
        resps = self.resp_step[step].to_numpy()
        resp_points, resp_cells = [], []
        scalars = []
        label_points, labels = [], []
        for cell, resp in zip(truss_cells, resps):
            coord1 = np.array(truss_coords[cell[1]])
            coord2 = np.array(truss_coords[cell[2]])
            xaxis = coord2 - coord1
            length = np.linalg.norm(xaxis)
            xaxis = xaxis / length
            cos_theta = np.dot(xaxis, [0, 0, 1])
            if 1 - cos_theta**2 < 1e-4:
                axis_up = [1, 0, 0]
            elif self.show_zaxis:
                axis_up = [0, 0, 1]
            else:
                axis_up = [0, 1, 0]
            _, plot_axis, _ = gram_schmidt(xaxis, axis_up)
            coord3 = coord1 + alpha * resp * plot_axis
            coord4 = coord2 + alpha * resp * plot_axis
            coord_upper = [coord3 + length / 12 * i * xaxis for i in range(13)] + [
                coord4
            ]
            coord_lower = [coord1 + length / 12 * i * xaxis for i in range(13)] + [
                coord3
            ]
            for i in range(len(coord_upper)):
                resp_cells.append([2, len(resp_points), len(resp_points) + 1])
                resp_points.extend([coord_lower[i], coord_upper[i]])
                scalars.extend([resp, resp])
            label_points.append((coord3 + coord4) / 2)
            labels.append(resp)
        labels = [f"{label:.3E}" for label in labels]
        label_points = np.array(label_points)
        resp_points = np.array(resp_points)
        scalars = np.array(scalars)
        #  ---------------------------------
        plotter.clear_actors()  # !!!!!!
        if plot_all_mesh:
            self._plot_all_mesh(plotter, color="gray", step=step)
        _ = _plot_lines(
            plotter,
            pos=truss_coords,
            cells=truss_cells,
            width=self.pargs.line_width,
            color=self.pargs.color_truss,
            render_lines_as_tubes=self.pargs.render_lines_as_tubes,
        )
        resp_plot = _plot_lines_cmap(
            plotter,
            resp_points,
            resp_cells,
            scalars,
            width=line_width,
            cmap=self.pargs.cmap,
            clim=clim,
            render_lines_as_tubes=self.pargs.render_lines_as_tubes,
            show_scalar_bar=False,
        )
        title = self._make_title(scalars, step, self.time[step])
        # _ = plotter.add_text(
        #     title,
        #     position="upper_right",
        #     font_size=self.pargs.title_font_size,
        #     font="courier",
        # )
        scalar_bar = plotter.add_scalar_bar(
            title=title,
            **self.pargs.scalar_bar_kargs
        )

        if show_values:
            plotter.add_point_labels(
                label_points,
                labels,
                # text_color="white",
                font_size=self.pargs.font_size,
                bold=True,
                always_visible=True,
                shape=None,
                shape_opacity=0.0,
            )
        self.update(plotter, cpos)
        return resp_plot

    def plot_slide(
        self,
        plotter,
        ele_tags=None,
        show_values=True,
        alpha=1.0,
        line_width=1.5,
        cpos="iso"
    ):
        plot_all_mesh = True if ele_tags is None else False
        _, clim, alpha_ = self._get_resp_peak()
        func = partial(
            self._create_mesh,
            plotter,
            ele_tags=ele_tags,
            clim=clim,
            plot_all_mesh=plot_all_mesh,
            show_values=show_values,
            alpha=alpha * alpha_,
            line_width=line_width,
            cpos=cpos
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
        ele_tags=None,
        step="absMax",
        show_values=True,
        alpha=1.0,
        line_width=1.5,
        cpos="iso"
    ):
        plot_all_mesh = True if ele_tags is None else False
        step, clim, alpha_ = self._get_resp_peak(idx=step)
        self._create_mesh(
            plotter=plotter,
            value=step,
            ele_tags=ele_tags,
            show_values=show_values,
            clim=clim,
            plot_all_mesh=plot_all_mesh,
            alpha=alpha * alpha_,
            line_width=line_width,
            cpos=cpos
        )

    def plot_anim(
        self,
        plotter,
        ele_tags=None,
        show_values=True,
        alpha=1.0,
        framerate: int = None,
        savefig: str = "TrussRespAnimation.gif",
        line_width=1.5,
        cpos="iso"
    ):
        if framerate is None:
            framerate = np.ceil(self.num_steps / 10)
        if savefig.endswith(".gif"):
            plotter.open_gif(savefig, fps=framerate)
        else:
            plotter.open_movie(savefig, framerate=framerate)
        plot_all_mesh = True if ele_tags is None else False
        _, clim, alpha_ = self._get_resp_peak()
        # plotter.write_frame()  # write initial data
        for step in range(self.num_steps):
            self._create_mesh(
                plotter,
                step,
                ele_tags=ele_tags,
                show_values=show_values,
                clim=clim,
                plot_all_mesh=plot_all_mesh,
                alpha=alpha * alpha_,
                line_width=line_width,
                cpos=cpos
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


def plot_truss_responses(
    odb_tag: Union[int, str] = 1,
    ele_tags: Union[int, list] = None,
    slides: bool = False,
    step: Union[int, str] = "absMax",
    show_values: bool = True,
    resp_type: str = "axialForce",
    unit_symbol: str = None,
    alpha: float = 1.0,
    line_width: float = 1.5,
    cpos: str = "iso",
) -> pv.Plotter:
    """Visualizing Truss Response.

    Parameters
    ----------
    odb_tag: Union[int, str], default: 1
        Tag of output databases (ODB) to be visualized.
    ele_tags: Union[int, list], default: None
        The tags of truss elements to be visualized. If None, all truss elements are selected.
    slides: bool, default: False
        Display the response for each step in the form of a slideshow.
        Otherwise, show the step with the following ``step`` parameter.
    step: Union[int, str], default: "absMax"
        If slides = False, this parameter will be used as the step to plot.
        If str, Optional: [absMax, absMin, Max, Min].
        If int, this step will be demonstrated (counting from 0).
    show_values: bool, default: True
        Whether to display the response value.
    resp_type: str, default: "axialForce"
        Response type, optional, one of ["axialForce", "axialDefo", "Stress", "Strain"].
    unit_symbol: str, default: None
        Unit symbol to be displayed in the plot.
    alpha: float, default: 1.0
        Scale the size of the response graph.

        .. Note::
            You can adjust the scale to make the response graph more visible.
            A negative number will reverse the direction.

    line_width: float, default: 1.5.
        Line width of the response graph.
    cpos: str, default: iso
        Model display perspective, optional: "iso", "xy", "yx", "xz", "zx", "yz", "zy".
        If 3d, defaults to "iso". If 2d, defaults to "xy".

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
    model_info_steps, model_update, truss_resp_step = loadODB(
        odb_tag, resp_type="Truss"
    )
    plotter = pv.Plotter(
        notebook=PLOT_ARGS.notebook,
        line_smoothing=PLOT_ARGS.line_smoothing,
        off_screen=PLOT_ARGS.off_screen
    )
    plotbase = PlotTrussResponse(model_info_steps, truss_resp_step, model_update)
    plotbase.set_unit_symbol(unit_symbol)
    plotbase.refactor_resp_step(resp_type=resp_type, ele_tags=ele_tags)
    if slides:
        plotbase.plot_slide(
            plotter,
            ele_tags=ele_tags,
            show_values=show_values,
            alpha=alpha,
            line_width=line_width,
            cpos=cpos
        )
    else:
        plotbase.plot_peak_step(
            plotter,
            ele_tags=ele_tags,
            step=step,
            show_values=show_values,
            alpha=alpha,
            line_width=line_width,
            cpos=cpos
        )
    if PLOT_ARGS.anti_aliasing:
        plotter.enable_anti_aliasing(PLOT_ARGS.anti_aliasing)
    return plotbase.update(plotter, cpos)


def plot_truss_responses_animation(
    odb_tag: Union[int, str] = 1,
    ele_tags: Union[int, list] = None,
    framerate: int = None,
    savefig: str = "TrussRespAnimation.gif",
    off_screen: bool = True,
    show_values: bool = False,
    resp_type: str = "axialForce",
    unit_symbol: str = None,
    alpha: float = 1.0,
    line_width: float = 1.5,
    cpos: str = "iso",
) -> pv.Plotter:
    """Truss response animation.

    Parameters
    ----------
    odb_tag: Union[int, str], default: 1
        Tag of output databases (ODB) to be visualized.
    ele_tags: Union[int, list], default: None
        The tags of truss elements to be visualized. If None, all truss elements are selected.
    framerate: int, default: None
        Framerate for the display, i.e., the number of frames per second.
    savefig: str, default: TrussRespAnimation.gif
        Path to save the animation. The suffix can be ``.gif`` or ``.mp4``.
    off_screen: bool, default: True
        Whether to display the plotting window.
        If True, the plotting window will not be displayed.
    show_values: bool, default: False
        Whether to display the response value.
    resp_type: str, default: "axialForce"
        Response type, optional, one of ["axialForce", "axialDefo", "Stress", "Strain"].
    unit_symbol: str, default: None
        Unit symbol to be displayed in the plot.
    alpha: float, default: 1.0
        Scale the size of the response graph.

        .. Note::
            You can adjust the scale to make the response graph more visible.
            A negative number will reverse the direction.

    line_width: float, default: 1.5.
        Line width of the response graph.
    cpos: str, default: iso
        Model display perspective, optional: "iso", "xy", "yx", "xz", "zx", "yz", "zy".
        If 3d, defaults to "iso". If 2d, defaults to "xy".

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
    model_info_steps, model_update, truss_resp_step = loadODB(
        odb_tag, resp_type="Truss"
    )
    plotter = pv.Plotter(
        notebook=PLOT_ARGS.notebook,
        line_smoothing=PLOT_ARGS.line_smoothing,
        off_screen=off_screen
    )
    plotbase = PlotTrussResponse(model_info_steps, truss_resp_step, model_update)
    plotbase.set_unit_symbol(unit_symbol)
    plotbase.refactor_resp_step(resp_type=resp_type, ele_tags=ele_tags)
    plotbase.plot_anim(
        plotter,
        ele_tags=ele_tags,
        show_values=show_values,
        alpha=alpha,
        framerate=framerate,
        savefig=savefig,
        line_width=line_width,
        cpos=cpos
    )
    if PLOT_ARGS.anti_aliasing:
        plotter.enable_anti_aliasing(PLOT_ARGS.anti_aliasing)
    print(f"Animation saved as {savefig}!")
    return plotbase.update(plotter, cpos)
