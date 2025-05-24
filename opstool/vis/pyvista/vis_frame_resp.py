from functools import partial
from typing import Optional, Union

import numpy as np
import pyvista as pv

from ...post import loadODB
from .plot_resp_base import PlotResponseBase
from .plot_utils import (
    PLOT_ARGS,
    _get_line_cells,
    _get_unstru_cells,
    _plot_all_mesh,
    # _plot_lines_cmap,
    _plot_face_cmap,
    _plot_lines,
    _update_point_label_actor,
)


class PlotFrameResponse(PlotResponseBase):
    def __init__(self, model_info_steps, beam_resp_step, model_update):
        super().__init__(model_info_steps, beam_resp_step, model_update)
        self.resp_factor = 1.0
        self.plot_axis = None
        self.sec_locs = None

        self.component_type = None

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
            raise ValueError(  # noqa: TRY003
                f"Invalid response type: {resp_type}. "
                "Valid options are: localForces, basicForces, basicDeformations, "
                "plasticDeformations, sectionForces, sectionDeformations."
            )
        # component type
        self.component_type = component.upper()
        if self.resp_type == "localForces":
            self._set_comp_type_local(component)
        elif self.resp_type in [
            "basicForces",
            "basicDeformations",
            "plasticDeformation",
        ]:
            self._set_comp_type_basic(component)
        else:
            self._set_comp_type_section(component)

    def _set_comp_type_local(self, comp_type):
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
            raise ValueError(  # noqa: TRY003
                f"Invalid component type for localForces: {comp_type}. Valid options are: FX, FY, FZ, MX, MY, MZ."
            )

    def _set_comp_type_basic(self, comp_type):
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
            raise ValueError(  # noqa: TRY003
                f"Invalid component type for {self.resp_type}: {comp_type}. Valid options are: N, MZ, MY, T."
            )

    def _set_comp_type_section(self, comp_type):
        if comp_type.upper() in ["N", "MZ", "VY", "T"]:
            self.component = comp_type.upper()
            self.plot_axis = "y"
        elif comp_type.upper() in ["VZ", "MY"]:
            self.component = comp_type.upper()
            self.plot_axis = "z"
        else:
            raise ValueError(  # noqa: TRY003
                f"Invalid component type for {self.resp_type}: {comp_type}. Valid options are: N, MZ, VY, MY, VZ, T."
            )

    def _plot_all_mesh(self, plotter, color="gray", step=0):
        pos = self._get_node_data(step).to_numpy()
        line_cells, _ = _get_line_cells(self._get_line_data(step))
        _, unstru_cell_types, unstru_cells = _get_unstru_cells(self._get_unstru_data(step))

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
            beam_cells_orign = beam_data.loc[:, ["numNodes", "nodeI", "nodeJ"]].to_numpy().astype(int)
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
        sec_loc = self._get_resp_data(step, "sectionLocs", "alpha")
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

    def _get_resp_scale_factor(self, idx="absMax"):
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
                raise ValueError("Invalid argument, one of [absMax, absMin, Max, Min]")  # noqa: TRY003
        else:
            step = int(idx)
        resp = self.resp_step[step]
        maxv = np.amax(np.abs(resp))
        alpha_ = 0.0 if maxv == 0 else self.max_bound_size * self.pargs.scale_factor / maxv
        cmin, cmax = self._get_resp_clim()
        return float(alpha_), step, (cmin, cmax)

    def _get_resp_clim(self):
        maxv = [np.max(data) for data in self.resp_step]
        minv = [np.min(data) for data in self.resp_step]
        cmin, cmax = np.min(minv), np.max(maxv)
        return cmin, cmax

    def _get_resp_mesh(self, beam_node_coords, beam_cells, sec_locs, resp, resp_scale, axis_data, show_values):
        show_values = "eleMaxMin" if show_values is True else show_values
        label_poins, labels, resp_points, resp_cells, scalars = [], [], [], [], []
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
            pos1 = [coord1 + loc * (coord2 - coord1) for loc in locs]  # lower
            pos2 = [coord + force_scale[i] * axis for i, coord in enumerate(pos1)]  # upper

            for i in range(len(pos1) - 1):
                resp_cells.append([
                    4,
                    len(resp_points),
                    len(resp_points) + 1,
                    len(resp_points) + 2,
                    len(resp_points) + 3,
                ])
                resp_points.extend([pos2[i], pos2[i + 1], pos1[i + 1], pos1[i]])
                scalars.extend([force[i], force[i + 1], force[i + 1], force[i]])
            if isinstance(show_values, str) and show_values.lower() in [
                "elemaxmin",
                "eleminmax",
                "elemax",
                "elemin",
                "all",
            ]:
                if self.resp_type in [
                    "localForces",
                    "basicForces",
                    "basicDeformations",
                    "plasticDeformation",
                ]:
                    label_poins.extend([pos2[0], pos2[-1]])
                    labels.extend([force[0], force[-1]])
                else:
                    if show_values.lower() == "all":
                        label_poins.extend(pos2)
                        labels.extend(force)
                    elif show_values.lower() == "elemax":
                        idx = np.argmax(force)
                        label_poins.append(pos2[idx])
                        labels.append(force[idx])
                    elif show_values.lower() == "elemin":
                        idx = np.argmin(force)
                        label_poins.append(pos2[idx])
                        labels.append(force[idx])
                    else:
                        idxmin = np.argmin(force)
                        idxmax = np.argmax(force)
                        label_poins.extend([pos2[idxmin], pos2[idxmax]])
                        labels.extend([force[idxmin], force[idxmax]])
        resp_points = np.array(resp_points)
        scalars = np.array(scalars)
        if isinstance(show_values, str) and show_values.lower() in ["maxmin", "minmax"]:
            idxmin = np.argmin(scalars)
            idxmax = np.argmax(scalars)
            label_poins.extend([resp_points[idxmin], resp_points[idxmax]])
            labels.extend([scalars[idxmin], scalars[idxmax]])
        fmt = self.pargs.scalar_bar_kargs["fmt"]
        labels = [f"{fmt}" % label for label in labels]
        label_poins = np.array(label_poins)
        return resp_points, resp_cells, scalars, labels, label_poins

    def _make_title(self, scalars, step, time):
        info = {
            "title": "Frame",
            "resp_type": self.resp_type.capitalize(),
            "dof": self.component_type,
            "min": np.min(scalars),
            "max": np.max(scalars),
            "step": step,
            "time": time,
        }
        lines = [
            f"* {info['title']} Responses",
            f"* {info['resp_type']}",
            f"* {info['dof']} (DOF)",
            f"{info['min']:.3E} (min)",
            f"{info['max']:.3E} (max)",
            f"{info['step']}(step); {info['time']:.3f}(time)",
        ]
        if self.unit:
            info["unit"] = self.unit
            lines.insert(3, f"{info['unit']} (unit)")
        max_len = max(len(line) for line in lines)
        padded_lines = [line.rjust(max_len) for line in lines]
        text = "\n".join(padded_lines)
        return text + "\n"

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
        style="surface",
        opacity=1.0,
        cpos="iso",
    ):
        step = round(value)
        resp = self.resp_step[step].to_numpy()
        resp_scale = resp * alpha
        beam_tags, beam_node_coords, beam_cells, yaxis, zaxis = self._make_frame_info(ele_tags, step)
        axis_data = yaxis if self.plot_axis == "y" else zaxis
        sec_locs = self.sec_locs[step].to_numpy()
        resp_points, resp_cells, scalars, labels, label_poins = self._get_resp_mesh(
            beam_node_coords, beam_cells, sec_locs, resp, resp_scale, axis_data, show_values
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
        # resp_plot = _plot_lines_cmap(
        #     plotter,
        #     resp_points,
        #     resp_cells,
        #     scalars,
        #     width=line_width,  # self.pargs.line_width,
        #     cmap=self.pargs.cmap,
        #     clim=clim,
        #     render_lines_as_tubes=self.pargs.render_lines_as_tubes,
        #     show_scalar_bar=False,
        # )
        opacity = 1.0 if style.lower() != "surface" else opacity
        resp_plot = _plot_face_cmap(
            plotter,
            resp_points,
            resp_cells,
            scalars,
            cmap=self.pargs.cmap,
            clim=clim,
            show_edges=False,
            edge_width=line_width,
            opacity=opacity,
            style=style,
            show_scalar_bar=False,
        )

        t_ = self.time[step]
        title = self._make_title(scalars, step, t_)
        scalar_bar = plotter.add_scalar_bar(title=title, **self.pargs.scalar_bar_kargs)
        if scalar_bar:
            # scalar_bar.SetTitle(title)
            title_prop = scalar_bar.GetTitleTextProperty()
            title_prop.SetJustificationToRight()
            title_prop.BoldOn()

        if show_values:
            label_plot = plotter.add_point_labels(
                label_poins,
                labels,
                # text_color="white",
                font_size=self.pargs.font_size,
                font_family="courier",
                bold=False,
                always_visible=True,
                shape=None,
                shape_opacity=0.0,
                show_points=False,
            )
        else:
            label_plot = None
        self.update(plotter, cpos=cpos)
        return line_plot, resp_plot, scalar_bar, label_plot

    def _update_mesh(self, step, alpha, ele_tags, show_values, line_plot, resp_plot, scalar_bar, label_plot, plotter):
        step = round(step)
        resp = self.resp_step[step].to_numpy()
        resp_scale = resp * alpha
        beam_tags, beam_node_coords, beam_cells, yaxis, zaxis = self._make_frame_info(ele_tags, step)
        axis_data = yaxis if self.plot_axis == "y" else zaxis
        sec_locs = self.sec_locs[step].to_numpy()
        resp_points, resp_cells, scalars, labels, label_points = self._get_resp_mesh(
            beam_node_coords, beam_cells, sec_locs, resp, resp_scale, axis_data, show_values
        )

        if line_plot:
            line_plot.points = beam_node_coords
            line_plot.lines = beam_cells

        if resp_plot:
            resp_plot.points = resp_points
            # resp_plot.lines = resp_cells
            resp_plot.faces = resp_cells
            resp_plot["scalars"] = scalars

        if scalar_bar:
            title = self._make_title(scalars, step, self.time[step])
            scalar_bar.SetTitle(title)

        if label_plot:
            # mapper = label_plot.GetMapper()
            text_property = pv.TextProperty(
                bold=False,
                font_size=self.pargs.font_size,
                font_family="courier",
                color=pv.global_theme.font.color,
            )
            _update_point_label_actor(
                label_plot,
                label_points,
                labels,
                text_property=text_property,
                renderer=plotter.renderer,
                shape_opacity=0.0,
                always_visible=True,
            )

    def plot_slide(
        self,
        plotter,
        ele_tags=None,
        alpha=1.0,
        resp_type=None,
        component=None,
        show_values=True,
        line_width=1.0,
        style="surface",
        opacity=1.0,
        plot_model=True,
        cpos="iso",
    ):
        self.refactor_resp_data(ele_tags, resp_type, component)
        alpha_, maxstep, clim = self._get_resp_scale_factor()

        if self.ModelUpdate:
            func = partial(
                self._create_mesh,
                plotter,
                alpha=alpha * alpha_,
                ele_tags=ele_tags,
                show_values=show_values,
                clim=clim,
                plot_all_mesh=plot_model,
                line_width=line_width,
                style=style,
                opacity=opacity,
                cpos=cpos,
            )
        else:
            line_plot, resp_plot, scalar_bar, label_plot = self._create_mesh(
                plotter,
                self.num_steps - 1,
                ele_tags=ele_tags,
                clim=clim,
                plot_all_mesh=plot_model,
                show_values=show_values,
                alpha=alpha * alpha_,
                line_width=line_width,
                style=style,
                opacity=opacity,
                cpos=cpos,
            )
            func = partial(
                self._update_mesh,
                alpha=alpha * alpha_,
                ele_tags=ele_tags,
                show_values=show_values,
                line_plot=line_plot,
                resp_plot=resp_plot,
                scalar_bar=scalar_bar,
                label_plot=label_plot,
                plotter=plotter,
            )
        plotter.add_slider_widget(func, [0, self.num_steps - 1], value=self.num_steps - 1, **self.slider_widget_args)

    def plot_peak_step(
        self,
        plotter,
        ele_tags=None,
        step="absMax",
        alpha=1.0,
        resp_type=None,
        component=None,
        show_values=True,
        line_width=1.0,
        style="surface",
        opacity=1.0,
        plot_model=True,
        cpos="iso",
    ):
        self.refactor_resp_data(ele_tags, resp_type, component)
        alpha_, step, clim = self._get_resp_scale_factor(idx=step)
        self._create_mesh(
            plotter=plotter,
            value=step,
            alpha=alpha * alpha_,
            ele_tags=ele_tags,
            show_values=show_values,
            clim=clim,
            plot_all_mesh=plot_model,
            line_width=line_width,
            style=style,
            opacity=opacity,
            cpos=cpos,
        )

    def plot_anim(
        self,
        plotter,
        ele_tags=None,
        alpha=1.0,
        resp_type=None,
        component=None,
        show_values=True,
        framerate=None,
        savefig: str = "FrameForcesAnimation.gif",
        line_width=1.0,
        style="surface",
        opacity=1.0,
        plot_model=True,
        cpos="iso",
    ):
        if framerate is None:
            framerate = np.ceil(self.num_steps / 10)
        if savefig.endswith(".gif"):
            plotter.open_gif(savefig, fps=framerate)
        else:
            plotter.open_movie(savefig, framerate=framerate)
        self.refactor_resp_data(ele_tags, resp_type, component)
        alpha_, maxstep, clim = self._get_resp_scale_factor()
        # plotter.write_frame()  # write initial data
        if self.ModelUpdate:
            for step in range(self.num_steps):
                self._create_mesh(
                    plotter,
                    step,
                    alpha=alpha * alpha_,
                    ele_tags=ele_tags,
                    show_values=show_values,
                    clim=clim,
                    plot_all_mesh=plot_model,
                    line_width=line_width,
                    style=style,
                    opacity=opacity,
                    cpos=cpos,
                )
                plotter.write_frame()
        else:
            line_plot, resp_plot, scalar_bar, label_plot = self._create_mesh(
                plotter,
                0,
                ele_tags=ele_tags,
                clim=clim,
                plot_all_mesh=plot_model,
                show_values=show_values,
                alpha=alpha * alpha_,
                line_width=line_width,
                style=style,
                opacity=opacity,
                cpos=cpos,
            )
            plotter.write_frame()
            for step in range(1, self.num_steps):
                self._update_mesh(
                    step=step,
                    alpha=alpha * alpha_,
                    ele_tags=ele_tags,
                    show_values=show_values,
                    line_plot=line_plot,
                    resp_plot=resp_plot,
                    scalar_bar=scalar_bar,
                    label_plot=label_plot,
                    plotter=plotter,
                )
                plotter.write_frame()


def plot_frame_responses(
    odb_tag: Union[int, str] = 1,
    ele_tags: Optional[Union[int, list]] = None,
    resp_type: str = "sectionForces",
    resp_dof: str = "MZ",
    unit_symbol: Optional[str] = None,
    slides: bool = False,
    step: Union[int, str] = "absMax",
    scale: float = 1.0,
    show_values: Union[bool, str] = "MaxMin",
    style: str = "surface",
    line_width: float = 1.5,
    opacity: float = 1.0,
    plot_model: bool = True,
    cpos: str = "iso",
) -> pv.Plotter:
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

    unit_symbol: str, default: None
        Unit symbol to be displayed in the plot.
    slides: bool, default: False
        Display the response for each step in the form of a slideshow.
        Otherwise, show the step with the following ``step`` parameter.
    step: Union[int, str], default: "absMax"
        If slides = False, this parameter will be used as the step to plot.
        If str, Optional: [absMax, absMin, Max, Min].
        If int, this step will be demonstrated (counting from 0).
    show_values: Union[bool, str], default: MaxMin
        Whether to display the response value.
        If str, optional: ["MaxMin", "eleMaxMin", "eleMax", "eleMin", "all"].

        - "MaxMin": show the max and min values of the response.
        - "eleMaxMin": show the max and min values of the response for each element.
        - "eleMax": show the max value of the response for each element.
        - "eleMin": show the min value of the response for each element.
        - "all": show all values of the response for each element.

    scale: float, default: 1.0
        Scale the size of the response graph.

        .. Note::
            You can adjust the scale to make the response graph more visible.
            A negative number will reverse the direction.

    cpos: str, default: iso
        Model display perspective, optional: "iso", "xy", "yx", "xz", "zx", "yz", "zy".
        If 3d, defaults to "iso". If 2d, defaults to "xy".
    style: str, default: "surface
        Display style for responses plot, optional, one of ["surface", "wireframe"]
    line_width: float, default: 1.5.
        Line width of the response graph when style="wireframe".
    opacity: float, default: 1.0
        Face opacity when style="surface".
    plot_model: bool, default: True
        Whether to plot the all model or not.

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
    model_info_steps, model_update, beam_resp_steps = loadODB(odb_tag, resp_type="Frame")
    plotter = pv.Plotter(
        notebook=PLOT_ARGS.notebook,
        line_smoothing=PLOT_ARGS.line_smoothing,
        off_screen=PLOT_ARGS.off_screen,
    )
    plotbase = PlotFrameResponse(model_info_steps, beam_resp_steps, model_update)
    plotbase.set_unit_symbol(unit_symbol)
    if slides:
        plotbase.plot_slide(
            plotter,
            ele_tags=ele_tags,
            alpha=scale,
            show_values=show_values,
            resp_type=resp_type,
            component=resp_dof,
            line_width=line_width,
            style=style,
            opacity=opacity,
            plot_model=plot_model,
            cpos=cpos,
        )
    else:
        plotbase.plot_peak_step(
            plotter,
            ele_tags=ele_tags,
            step=step,
            alpha=scale,
            show_values=show_values,
            resp_type=resp_type,
            component=resp_dof,
            line_width=line_width,
            style=style,
            opacity=opacity,
            plot_model=plot_model,
            cpos=cpos,
        )
    if PLOT_ARGS.anti_aliasing:
        plotter.enable_anti_aliasing(PLOT_ARGS.anti_aliasing)
    return plotbase.update(plotter, cpos)


def plot_frame_responses_animation(
    odb_tag: Union[int, str] = 1,
    ele_tags: Optional[Union[int, list]] = None,
    resp_type: str = "sectionForces",
    resp_dof: str = "MZ",
    unit_symbol: Optional[str] = None,
    scale: float = 1.0,
    show_values: Union[bool, str] = "MaxMin",
    cpos: str = "iso",
    framerate: Optional[int] = None,
    savefig: str = "FrameForcesAnimation.gif",
    off_screen: bool = True,
    style: str = "surface",
    line_width: float = 1.5,
    opacity: float = 1.0,
    plot_model: bool = True,
) -> pv.Plotter:
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

    unit_symbol: str, default: None
        Unit symbol to be displayed in the plot.
    scale: float, default: 1.0
        Scale the size of the response graph.

        .. Note::
            You can adjust the scale to make the response graph more visible.
            A negative number will reverse the direction.

    show_values: Union[bool, str], default: MaxMin
        Whether to display the response value.
        If str, optional: ["MaxMin", "eleMaxMin", "eleMax", "eleMin", "all"].

        - "MaxMin": show the max and min values of the response.
        - "eleMaxMin": show the max and min values of the response for each element.
        - "eleMax": show the max value of the response for each element.
        - "eleMin": show the min value of the response for each element.
        - "all": show all values of the response for each element.

    framerate: int, default: None
        Framerate for the display, i.e., the number of frames per second.
    savefig: str, default: FrameForcesAnimation.gif
        Path to save the animation. The suffix can be ``.gif`` or ``.mp4``.
    cpos: str, default: iso
        Model display perspective, optional: "iso", "xy", "yx", "xz", "zx", "yz", "zy".
        If 3d, defaults to "iso". If 2d, defaults to "xy".
    off_screen: bool, default: True
        Whether to display the plotting window.
        If True, the plotting window will not be displayed.
    style: str, default: "surface
        Display style for responses plot, optional, one of ["surface", "wireframe"]
    line_width: float, default: 1.5.
        Line width of the response graph when style="wireframe".
    opacity: float, default: 1.0
        Face opacity when style="surface".
    plot_model: bool, default: True
        Whether to plot the all model or not.

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
    model_info_steps, model_update, beam_resp_steps = loadODB(odb_tag, resp_type="Frame")
    plotter = pv.Plotter(
        notebook=PLOT_ARGS.notebook,
        line_smoothing=PLOT_ARGS.line_smoothing,
        off_screen=off_screen,
    )
    plotbase = PlotFrameResponse(model_info_steps, beam_resp_steps, model_update)
    plotbase.set_unit_symbol(unit_symbol)
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
        style=style,
        opacity=opacity,
        plot_model=plot_model,
        cpos=cpos,
    )
    if PLOT_ARGS.anti_aliasing:
        plotter.enable_anti_aliasing(PLOT_ARGS.anti_aliasing)
    print(f"Animation saved as {savefig}!")
    return plotbase.update(plotter, cpos)
