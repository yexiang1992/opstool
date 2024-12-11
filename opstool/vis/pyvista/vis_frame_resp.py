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


class PlotFrameResponse(PlotResponseBase):

    def __init__(self, model_info_steps, beam_resp_step, model_update):
        super().__init__(model_info_steps, beam_resp_step, model_update)
        self.resp_factor = 1.0
        self.plot_axis = None
        self.sec_locs = None

    def _set_comp_resp_type(self, resp_type, component):
        if resp_type.lower() in ["localforces", "localforce"]:
            self.resp_type = "localForces"
        elif resp_type.lower() in ["basicforces", "basicforce"]:
            self.resp_type = "basicForces"
        elif resp_type.lower() in [
            "basicdeformations",
            "basicdeformation",
            "basicdefo",
        ]:
            self.resp_type = "basicDeformations"
        elif resp_type.lower() in [
            "plasticdeformation",
            "plasticdeformations",
            "plasticdefo",
        ]:
            self.resp_type = "plasticDeformation"
        elif resp_type.lower() in ["sectionforces", "sectionforce"]:
            self.resp_type = "sectionForces"
        elif resp_type.lower() in [
            "sectiondeformations",
            "sectiondeformation",
            "sectiondefo",
        ]:
            self.resp_type = "sectionDeformations"
        else:
            raise ValueError(
                f"Invalid response type: {resp_type}. "
                "Valid options are: localForces, basicForces, basicDeformations, "
                "plasticDeformations, sectionForces, sectionDeformations."
            )
        self._set_comp_type(component)

    def _set_comp_type(self, comp_type):
        if self.resp_type == "localForces":
            if comp_type.upper() == "FX":
                self.component = ["FX1", "FX2"]
                self.resp_factor = np.array([-1.0, 1.0])
                self.plot_axis = "y"
            elif comp_type.upper() == "FY":
                self.component = ["FY1", "FY2"]
                self.resp_factor = np.array([-1.0, 1.0])
                self.plot_axis = "y"
            elif comp_type.upper() == "FZ":
                self.component = ["FZ1", "FZ2"]
                self.resp_factor = np.array([-1.0, 1.0])
                self.plot_axis = "z"
            elif comp_type.upper() == "MX":
                self.component = ["MX1", "MX2"]
                self.resp_factor = np.array([-1.0, 1.0])
                self.plot_axis = "y"
            elif comp_type.upper() == "MY":
                self.component = ["MY1", "MY2"]
                self.plot_axis = "z"
                self.resp_factor = np.array([1.0, -1.0])
            elif comp_type.upper() == "MZ":
                self.component = ["MZ1", "MZ2"]
                self.resp_factor = np.array([-1.0, 1.0])
                self.plot_axis = "y"
            else:
                raise ValueError(
                    f"Invalid component type for localForces: {comp_type}. "
                    "Valid options are: FX, FY, FZ, MX, MY, MZ."
                )
        elif self.resp_type in [
            "basicForces",
            "basicDeformations",
            "plasticDeformation",
        ]:
            if comp_type.upper() == "N":
                self.component = ["N", "N"]
                self.plot_axis = "y"
            elif comp_type.upper() == "MZ":
                self.component = ["MZ1", "MZ2"]
                self.resp_factor = np.array([-1.0, 1.0])
                self.plot_axis = "y"
            elif comp_type.upper() == "MY":
                self.component = ["MY1", "MY2"]
                self.resp_factor = np.array([1.0, -1.0])
                self.plot_axis = "z"
            elif comp_type.upper() == "T":
                self.component = ["T", "T"]
                self.plot_axis = "y"
            else:
                raise ValueError(
                    f"Invalid component type for {self.resp_type}: {comp_type}. "
                    "Valid options are: N, MZ, MY, T."
                )
        else:
            if comp_type.upper() == "N":
                self.component = comp_type.upper()
                self.plot_axis = "y"
            elif comp_type.upper() == "MZ":
                self.component = comp_type.upper()
                self.plot_axis = "y"
            elif comp_type.upper() == "VY":
                self.component = comp_type.upper()
                self.plot_axis = "y"
            elif comp_type.upper() == "MY":
                self.component = comp_type.upper()
                self.plot_axis = "z"
            elif comp_type.upper() == "VZ":
                self.component = comp_type.upper()
                self.plot_axis = "z"
            elif comp_type.upper() == "T":
                self.component = comp_type.upper()
                self.plot_axis = "y"
            else:
                raise ValueError(
                    f"Invalid component type for {self.resp_type}: {comp_type}. "
                    "Valid options are: N, MZ, VY, MY, VZ, T."
                )

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

    def _get_beam_data(self, step):
        return self._get_model_data("BeamData", step)

    def _make_frame_info(self, ele_tags, step):
        pos = self._get_node_data(step).to_numpy()
        beam_data = self._get_beam_data(step)
        beam_node_coords = []
        beam_cells = []
        if ele_tags is None:
            beam_tags = beam_data.coords["eleTags"].values
            beam_cells_orign = (
                beam_data.loc[:, ["numNodes", "nodeI", "nodeJ"]].to_numpy().astype(int)
            )
            yaxis = beam_data.loc[:, ["yaxis-x", "yaxis-y", "yaxis-z"]]
            zaxis = beam_data.loc[:, ["zaxis-x", "zaxis-y", "zaxis-z"]]
            for i, cell in enumerate(beam_cells_orign):
                nodei, nodej = cell[1:]
                beam_node_coords.append(pos[int(nodei)])
                beam_node_coords.append(pos[int(nodej)])
                beam_cells.append([2, 2 * i, 2 * i + 1])
        else:
            beam_tags = np.atleast_1d(ele_tags)
            beam_info = beam_data.sel(eleTags=beam_tags)
            yaxis, zaxis = [], []
            for i, etag in enumerate(beam_tags):
                nodei, nodej = beam_info.loc[etag, ["nodeI", "nodeJ"]]
                beam_node_coords.append(pos[int(nodei)])
                beam_node_coords.append(pos[int(nodej)])
                beam_cells.append([2, 2 * i, 2 * i + 1])
                yaxis.append(beam_info.loc[etag, ["yaxis-x", "yaxis-y", "yaxis-z"]])
                zaxis.append(beam_info.loc[etag, ["zaxis-x", "zaxis-y", "zaxis-z"]])
        beam_node_coords = np.array(beam_node_coords)
        yaxis, zaxis = np.array(yaxis), np.array(zaxis)
        return beam_tags, beam_node_coords, beam_cells, yaxis, zaxis

    def _get_sec_loc(self, step):
        sec_loc = self._get_resp_data(step, "sectionLocs", None)
        return sec_loc

    def refactor_resp_data(self, ele_tags, resp_type, component):
        self._set_comp_resp_type(resp_type, component)
        resps, sec_locs = [], []
        if self.ModelUpdate or ele_tags is not None:
            for i in range(self.num_steps):
                beam_tags, _, _, _, _ = self._make_frame_info(ele_tags, i)
                da = self._get_resp_data(i, self.resp_type, self.component)
                da = da.sel(eleTags=beam_tags) * self.resp_factor
                resps.append(da)
                sec_da = self._get_sec_loc(i)
                sec_locs.append(sec_da.sel(eleTags=beam_tags))
        else:
            for i in range(self.num_steps):
                da = self._get_resp_data(i, self.resp_type, self.component)
                resps.append(da * self.resp_factor)
                sec_da = self._get_sec_loc(i)
                sec_locs.append(sec_da)

        self.resp_step = resps
        self.sec_locs = sec_locs

    def _get_resp_scale_factor(self):
        maxv = [np.max(np.abs(data)) for data in self.resp_step]
        maxstep = np.argmax(maxv)
        resp_max = self.resp_step[maxstep]
        cmin, cmax = self._get_resp_clim()
        maxv = np.amax(np.abs(resp_max))
        if maxv == 0:
            alpha_ = 0.0
        else:
            alpha_ = self.max_bound_size * self.pargs.scale_factor / maxv
        return alpha_, maxstep, (cmin, cmax)

    def _get_resp_clim(self):
        maxv = [np.max(data) for data in self.resp_step]
        minv = [np.min(data) for data in self.resp_step]
        cmin, cmax = np.min(minv), np.max(maxv)
        return cmin, cmax

    def _get_resp_mesh(
        self, beam_node_coords, beam_cells, sec_locs, resp, resp_scale, axis_data
    ):
        label_poins, labels, resp_points, resp_cells, scalars = [], [], [], [], []
        idx, resp, resp_scale, sec_locs = (
            0,
            resp.to_numpy(),
            resp_scale.to_numpy(),
            sec_locs.to_numpy(),
        )
        for i, cell in enumerate(beam_cells):
            axis = axis_data[i]
            node1, node2 = cell[1:]
            coord1, coord2 = beam_node_coords[node1], beam_node_coords[node2]
            if self.resp_type in [
                "localForces",
                "basicForces",
                "basicDeformations",
                "plasticDeformation",
            ]:
                f1, f2 = resp_scale[i]
                f1_, f2_ = resp[i]
                locs = np.linspace(0, 1, 11)
                force = np.interp(locs, [0, 1], [f1_, f2_])
                force_scale = np.interp(locs, [0, 1], [f1, f2])
            else:
                locs = sec_locs[i][~np.isnan(sec_locs[i])]
                force = resp[i][~np.isnan(resp[i])]
                force_scale = resp_scale[i][~np.isnan(resp_scale[i])]
            pos1 = np.array([coord1 + loc * (coord2 - coord1) for loc in locs])
            pos2 = [coord + force_scale[i] * axis for i, coord in enumerate(pos1)]
            pos2 = np.array(pos2)
            pos = np.empty(
                (pos1.shape[0] + pos2.shape[0], pos1.shape[1]), dtype=pos1.dtype
            )
            pos[0::2] = pos1
            pos[1::2] = pos2
            resp_points.extend(pos)
            resp_cells.extend(
                [(2, idx + i, idx + i + 1) for i in range(0, len(pos), 2)]
            )
            resp_cells.extend(
                [(2, idx + i + 1, idx + i + 3) for i in range(0, len(pos) - 2, 2)]
            )
            scalars.extend(np.repeat(force, 2))
            if self.resp_type in [
                "localForces",
                "basicForces",
                "basicDeformations",
                "plasticDeformation",
            ]:
                label_poins.extend([pos2[0], pos2[-1]])
                labels.extend([force[0], force[-1]])
            else:
                label_poins.extend(pos2)
                labels.extend(force)
            idx += len(pos)
        labels = [f"{label:.2E}" for label in labels]
        label_poins = np.array(label_poins)
        resp_points = np.array(resp_points)
        scalars = np.array(scalars)
        return resp_points, resp_cells, scalars, labels, label_poins

    def _create_mesh(
        self,
        plotter,
        value,
        ele_tags=None,
        alpha=1.0,
        show_values=True,
        plot_all_mesh=True,
        clim=None,
        line_width=1.0,
    ):
        step = int(round(value))
        resp = self.resp_step[step]
        resp_scale = resp * alpha
        beam_tags, beam_node_coords, beam_cells, yaxis, zaxis = self._make_frame_info(
            ele_tags, step
        )
        axis_data = yaxis if self.plot_axis == "y" else zaxis
        sec_locs = self.sec_locs[step]
        resp_points, resp_cells, scalars, labels, label_poins = self._get_resp_mesh(
            beam_node_coords, beam_cells, sec_locs, resp, resp_scale, axis_data
        )
        #  ---------------------------------
        plotter.clear_actors()  # !!!!!!
        if plot_all_mesh:
            self._plot_all_mesh(plotter, color="gray", step=step)
        # point_plot = _plot_points(
        #     plotter, pos=beam_node_coords, color=self.pargs.color_point,
        #     size=self.pargs.point_size,
        #     render_points_as_spheres=self.pargs.render_points_as_spheres
        # )
        line_plot = _plot_lines(
            plotter,
            pos=beam_node_coords,
            cells=beam_cells,
            width=self.pargs.line_width,
            color="black",
            render_lines_as_tubes=self.pargs.render_lines_as_tubes,
        )
        resp_plot = _plot_lines_cmap(
            plotter,
            resp_points,
            resp_cells,
            scalars,
            width=line_width,  # self.pargs.line_width,
            cmap=self.pargs.cmap,
            clim=clim,
            render_lines_as_tubes=self.pargs.render_lines_as_tubes,
            show_scalar_bar=False,
        )
        t_ = self.time[step]
        title = self.resp_type + "\n"
        title += f"step: {step};" + f" time: {t_:.4f}\n"
        title += "min = {:.3E}\nmax = {:.3E}\n".format(np.min(scalars), np.max(scalars))
        text = plotter.add_text(
            title,
            position="upper_right",
            font_size=self.pargs.title_font_size,
            font="courier",
        )
        _ = plotter.add_scalar_bar(
            fmt="%.3e",
            n_labels=10,
            bold=True,
            vertical=True,
            font_family="courier",
            label_font_size=self.pargs.font_size,
            title_font_size=self.pargs.title_font_size,
            position_x=0.875,
        )
        if show_values:
            plabel = plotter.add_point_labels(
                label_poins,
                labels,
                # text_color="white",
                font_size=self.pargs.font_size,
                bold=False,
                always_visible=True,
                shape_opacity=0.0,
            )
        else:
            plabel = None
        return line_plot, resp_plot, text, plabel

    def plot_slide(
        self,
        plotter,
        ele_tags=None,
        alpha=1.0,
        resp_type=None,
        component=None,
        show_values=True,
        line_width=1.0,
    ):
        plot_all_mesh = True if ele_tags is None else False
        self.refactor_resp_data(ele_tags, resp_type, component)
        alpha_, maxstep, clim = self._get_resp_scale_factor()
        func = partial(
            self._create_mesh,
            plotter,
            ele_tags=ele_tags,
            clim=clim,
            alpha=alpha * alpha_,
            plot_all_mesh=plot_all_mesh,
            show_values=show_values,
            line_width=line_width,
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
        alpha=1.0,
        resp_type=None,
        component=None,
        show_values=True,
        line_width=1.0,
    ):
        plot_all_mesh = True if ele_tags is None else False
        self.refactor_resp_data(ele_tags, resp_type, component)
        alpha_, maxstep, clim = self._get_resp_scale_factor()
        self._create_mesh(
            plotter=plotter,
            value=maxstep,
            alpha=alpha * alpha_,
            ele_tags=ele_tags,
            show_values=show_values,
            clim=clim,
            plot_all_mesh=plot_all_mesh,
            line_width=line_width,
        )

    def plot_anim(
        self,
        plotter,
        ele_tags=None,
        alpha=1.0,
        resp_type=None,
        component=None,
        show_values=True,
        framerate: int = None,
        savefig: str = "FrameForcesAnimation.gif",
        line_width=1.0,
    ):
        if framerate is None:
            framerate = np.ceil(self.num_steps / 10)
        if savefig.endswith(".gif"):
            plotter.open_gif(savefig, fps=framerate)
        else:
            plotter.open_movie(savefig, framerate=framerate)
        plot_all_mesh = True if ele_tags is None else False
        self.refactor_resp_data(ele_tags, resp_type, component)
        alpha_, maxstep, clim = self._get_resp_scale_factor()
        # plotter.write_frame()  # write initial data
        for step in range(self.num_steps):
            self._create_mesh(
                plotter,
                step,
                ele_tags=ele_tags,
                alpha=alpha * alpha_,
                show_values=show_values,
                clim=clim,
                plot_all_mesh=plot_all_mesh,
                line_width=line_width,
            )
            plotter.write_frame()

    def update(self, plotter, cpos):
        viewer = {
            "xy": plotter.view_xy,
            "yx": plotter.view_yx,
            "xz": plotter.view_xz,
            "zx": plotter.view_zx,
            "yz": plotter.view_yz,
            "zy": plotter.view_zy,
            "iso": plotter.view_isometric,
        }
        if not self.show_zaxis:
            cpos = "xy"
        viewer[cpos]()
        return plotter


def plot_frame_responses(
    odb_tag: Union[int, str] = 1,
    ele_tags: Union[int, list] = None,
    resp_type: str = "sectionForces",
    resp_dof: str = "MZ",
    slides: bool = False,
    scale: float = 1.0,
    show_values: bool = False,
    cpos: str = "iso",
    line_width: float = 1.5,
):
    """Plot the responses of the frame element.

    Parameters
    ----------
    odb_tag: Union[int, str], default: 1
        Tag of output databases (ODB) to be visualized.
    ele_tags: Union[int, list], default: None
        The tags of frame elements to be visualized. If None, all frame elements are selected.
    resp_type: str, default: "sectionforces"
        Response type, optional, one of ["localForces", "basicForces", "basicDeformations",
        "plasticDeformation", "sectionForces", "sectionDeformations"].
    resp_dof: str, default: "MZ"
        Component type corrsponding to the resp_type.

         - For `localForces`: ["FX", "FY", "FZ", "MX", "MY", "MZ"]
         - For `basicForces`: ["N", "MZ", "MY", "T"]
         - For `basicDeformations`: ["N", "MZ", "MY", "T"]
         - For `plasticDeformation`: ["N", "MZ", "MY", "T"]
         - For `sectionForces`: ["N", "MZ", "VY", "MY", "VZ", "T"]
         - For `sectionDeformations`: ["N", "MZ", "VY", "MY", "VZ", "T"]

         .. Note::
           For `sectionForces` and `sectionDeformations`,
           not all sections include the shear dof VY and VZ.
           For instance, in the most commonly used 3D fiber cross-sections,
           only the axial force N, bending moments MZ and MY, and torsion T are available.

    slides: bool, default: False
        Display the response for each step in the form of a slideshow.
        Otherwise, show the step with the largest response.
    show_values: bool, default: True
        Whether to display the response value.
    scale: float, default: 1.0
        Scale the size of the response graph.

        .. Note::
            You can adjust the scale to make the response graph more visible.
            A negative number will reverse the direction.

    cpos: str, default: iso
        Model display perspective, optional: "iso", "xy", "yx", "xz", "zx", "yz", "zy".
        If 3d, defaults to "iso". If 2d, defaults to "xy".
    line_width: float, default: 1.5.
        Line width of the response graph.

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
    model_info_steps, model_update, beam_resp_steps = loadODB(
        odb_tag, resp_type="Frame"
    )
    plotter = pv.Plotter(
        notebook=PLOT_ARGS.notebook,
        line_smoothing=PLOT_ARGS.line_smoothing,
        off_screen=PLOT_ARGS.off_screen,
    )
    plotbase = PlotFrameResponse(model_info_steps, beam_resp_steps, model_update)
    if slides:
        plotbase.plot_slide(
            plotter,
            ele_tags=ele_tags,
            alpha=scale,
            show_values=show_values,
            resp_type=resp_type,
            component=resp_dof,
            line_width=line_width,
        )
    else:
        plotbase.plot_peak_step(
            plotter,
            ele_tags=ele_tags,
            alpha=scale,
            show_values=show_values,
            resp_type=resp_type,
            component=resp_dof,
            line_width=line_width,
        )
    if PLOT_ARGS.anti_aliasing:
        plotter.enable_anti_aliasing(PLOT_ARGS.anti_aliasing)
    return plotbase.update(plotter, cpos)


def plot_frame_responses_animation(
    odb_tag: Union[int, str] = 1,
    ele_tags: Union[int, list] = None,
    resp_type: str = "sectionForces",
    resp_dof: str = "MZ",
    scale: float = 1.0,
    show_values: bool = False,
    cpos: str = "iso",
    framerate: int = None,
    savefig: str = "FrameForcesAnimation.gif",
    line_width: float = 1.5,
):
    """Animate the responses of frame elements.

    Parameters
    ----------
    odb_tag: Union[int, str], default: 1
        Tag of output databases (ODB) to be visualized.
    ele_tags: Union[int, list], default: None
        The tags of frame elements to be visualized. If None, all frame elements are selected.
    resp_type: str, default: "sectionforces"
        Response type, optional, one of ["localForces", "basicForces", "basicDeformations",
        "plasticDeformation", "sectionForces", "sectionDeformations"].
    resp_dof: str, default: "MZ"
        Component type corrsponding to the resp_type.

         - For `localForces`: ["FX", "FY", "FZ", "MX", "MY", "MZ"]
         - For `basicForces`: ["N", "MZ", "MY", "T"]
         - For `basicDeformations`: ["N", "MZ", "MY", "T"]
         - For `plasticDeformation`: ["N", "MZ", "MY", "T"]
         - For `sectionForces`: ["N", "MZ", "VY", "MY", "VZ", "T"]
         - For `sectionDeformations`: ["N", "MZ", "VY", "MY", "VZ", "T"]

         .. Note::
           For `sectionForces` and `sectionDeformations`,
           not all sections include the shear dof VY and VZ.
           For instance, in the most commonly used 3D fiber cross-sections,
           only the axial force N, bending moments MZ and MY, and torsion T are available.

    scale: float, default: 1.0
        Scale the size of the response graph.

        .. Note::
            You can adjust the scale to make the response graph more visible.
            A negative number will reverse the direction.

    show_values: bool, default: True
        Whether to display the response value.
    framerate: int, default: None
        Framerate for the display, i.e., the number of frames per second.
    savefig: str, default: FrameForcesAnimation.gif
        Path to save the animation. The suffix can be ``.gif`` or ``.mp4``.
    cpos: str, default: iso
        Model display perspective, optional: "iso", "xy", "yx", "xz", "zx", "yz", "zy".
        If 3d, defaults to "iso". If 2d, defaults to "xy".
    line_width: float, default: 1.5.
        Line width of the response graph.

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
    model_info_steps, model_update, beam_resp_steps = loadODB(
        odb_tag, resp_type="Frame"
    )
    plotter = pv.Plotter(
        notebook=PLOT_ARGS.notebook,
        line_smoothing=PLOT_ARGS.line_smoothing,
        off_screen=PLOT_ARGS.off_screen,
    )
    plotbase = PlotFrameResponse(model_info_steps, beam_resp_steps, model_update)
    plotbase.plot_anim(
        plotter,
        ele_tags=ele_tags,
        alpha=scale,
        show_values=show_values,
        resp_type=resp_type,
        component=resp_dof,
        framerate=framerate,
        savefig=savefig,
        line_width=line_width,
    )
    if PLOT_ARGS.anti_aliasing:
        plotter.enable_anti_aliasing(PLOT_ARGS.anti_aliasing)
    return plotbase.update(plotter, cpos)
