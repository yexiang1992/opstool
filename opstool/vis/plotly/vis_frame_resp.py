from typing import Union

import numpy as np
import plotly.graph_objs as go

from .plot_resp_base import PlotResponseBase

from .plot_utils import (
    _plot_points_cmap,
    _plot_lines,
    _plot_lines_cmap,
    _plot_all_mesh,
    _get_line_cells,
    _get_unstru_cells,
)
from ...post import loadODB
from ...utils import CONSTANTS
PKG_NAME = CONSTANTS.get_pkg_name()


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

    def _plot_all_mesh(self, plotter, color="#738595", step=0):
        pos = self._get_node_data(step).to_numpy()
        line_cells, _ = _get_line_cells(self._get_line_data(step))
        _, unstru_cell_types, unstru_cells = _get_unstru_cells(
            self._get_unstru_data(step)
        )
        (
            face_points,
            face_line_points,
            face_mid_points,
            veci,
            vecj,
            veck,
        ) = self._get_plotly_unstru_data(
            pos, unstru_cell_types, unstru_cells, scalars=None
        )
        line_points, line_mid_points = self._get_plotly_line_data(
            pos, line_cells, scalars=None
        )
        _plot_all_mesh(plotter, line_points, face_line_points, color=color, width=1.5)

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
            alpha_ = self.max_bound_size / maxv * self.pargs.scale_factor
        return alpha_, maxstep, (cmin, cmax)

    def _get_resp_clim(self):
        maxv = [np.max(data) for data in self.resp_step]
        minv = [np.min(data) for data in self.resp_step]
        cmin, cmax = np.min(minv), np.max(maxv)
        return cmin, cmax

    def _get_resp_mesh(
        self, beam_node_coords, beam_cells, sec_locs, resp, resp_scale, axis_data
    ):
        resp_points, resp_cells, scalars = [], [], []
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
            idx += len(pos)
        resp_points = np.array(resp_points)
        scalars = np.array(scalars)
        resp_cells = np.array(resp_cells)
        return resp_points, resp_cells, scalars

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
        coloraxis="coloraxis",
    ):
        step = int(round(value))
        resp = self.resp_step[step]
        resp_scale = resp * alpha
        beam_tags, beam_node_coords, beam_cells, yaxis, zaxis = self._make_frame_info(
            ele_tags, step
        )
        axis_data = yaxis if self.plot_axis == "y" else zaxis
        sec_locs = self.sec_locs[step]
        resp_points, resp_cells, scalars = self._get_resp_mesh(
            beam_node_coords, beam_cells, sec_locs, resp, resp_scale, axis_data
        )
        #  ---------------------------------
        if plot_all_mesh:
            self._plot_all_mesh(plotter, color="gray", step=step)
        line_points, line_mid_points = self._get_plotly_line_data(
            beam_node_coords, beam_cells, scalars=None
        )
        _plot_lines(
            plotter,
            pos=line_points,
            width=self.pargs.line_width,
            color=self.pargs.color_beam,
            name="Frame",
            hoverinfo="skip",
        )
        line_points, line_mid_points, line_scalars = self._get_plotly_line_data(
            resp_points, resp_cells, scalars
        )
        _plot_lines_cmap(
            plotter,
            line_points,
            scalars=line_scalars,
            coloraxis=coloraxis,
            clim=clim,
            width=line_width,
        )
        if show_values:
            _plot_points_cmap(
                plotter,
                resp_points,
                scalars=scalars,
                clim=clim,
                coloraxis=coloraxis,
                name=self.resp_type,
                size=self.pargs.point_size,
            )

    def _make_txt(self, step):
        resp = self.resp_step[step].data
        maxv, minv = np.max(resp), np.min(resp)
        t_ = self.time[step]
        title = f'<span style="font-weight:bold; font-size:{self.pargs.title_font_size}">{PKG_NAME}'
        title += " :: Frame Responses 3D Viewer</span><br><br><br>"
        title += f"<b>{self.resp_type.capitalize()}</b> --> "
        comp = (
            self.component
            if isinstance(self.component, str)
            else " ".join(self.component)
        )
        title += f"<b>{comp}</b><br>"
        maxv = self._set_txt_props(f"{maxv:.3E}")
        minv = self._set_txt_props(f"{minv:.3E}")
        title += f"<b>Max.:</b> {maxv}<br><b>Min.:</b> {minv}<br>"
        step_txt = self._set_txt_props(f"{step}")
        title += f"<br><b>step:</b> {step_txt}; "
        t_txt = self._set_txt_props(f"{t_:.3f}")
        title += f"<b>time</b>: {t_txt}"
        txt = dict(
            font=dict(size=self.pargs.font_size),
            text=title,
        )
        return txt

    def plot_slide(
        self,
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
        n_data = None
        for i in range(self.num_steps):
            plotter = []
            self._create_mesh(
                plotter,
                i,
                alpha=alpha_ * alpha,
                clim=clim,
                ele_tags=ele_tags,
                coloraxis=f"coloraxis{i + 1}",
                show_values=show_values,
                plot_all_mesh=plot_all_mesh,
                line_width=line_width,
            )
            self.FIGURE.add_traces(plotter)
            if i == 0:
                n_data = len(self.FIGURE.data)
        for i in range(0, len(self.FIGURE.data) - n_data):
            self.FIGURE.data[i].visible = False
        # Create and add slider
        steps = []
        for i in range(self.num_steps):
            txt = self._make_txt(i)
            step = dict(
                method="update",
                args=[
                    {"visible": [False] * len(self.FIGURE.data)},
                    {"title": txt},
                ],  # layout attribute
                label=str(i),
            )
            step["args"][0]["visible"][n_data * i : n_data * (i + 1)] = [True] * n_data
            # Toggle i'th trace to "visible"
            steps.append(step)
        sliders = [
            dict(
                active=self.num_steps,
                currentvalue={"prefix": "Step: "},
                pad={"t": 50},
                steps=steps,
            )
        ]
        coloraxiss = {}
        for i in range(self.num_steps):
            coloraxiss[f"coloraxis{i + 1}"] = dict(
                colorscale=self.pargs.cmap,
                cmin=clim[0],
                cmax=clim[1],
                showscale=True,
                colorbar=dict(tickfont=dict(size=15)),
            )
        self.FIGURE.update_layout(
            sliders=sliders,
            **coloraxiss,
        )

    def plot_peak_step(
        self,
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
        plotter = []
        self._create_mesh(
            plotter,
            maxstep,
            alpha=alpha_ * alpha,
            clim=clim,
            ele_tags=ele_tags,
            coloraxis=f"coloraxis",
            show_values=show_values,
            plot_all_mesh=plot_all_mesh,
            line_width=line_width,
        )
        self.FIGURE.add_traces(plotter)
        txt = self._make_txt(maxstep)
        self.FIGURE.update_layout(
            coloraxis=dict(
                colorscale=self.pargs.cmap,
                cmin=clim[0],
                cmax=clim[1],
                colorbar=dict(tickfont=dict(size=self.pargs.font_size - 2)),
            ),
            title=txt,
        )

    def plot_anim(
        self,
        ele_tags=None,
        alpha=1.0,
        resp_type=None,
        component=None,
        show_values=True,
        framerate: int = None,
        line_width=1.0,
    ):
        if framerate is None:
            framerate = np.ceil(self.num_steps / 10)
        plot_all_mesh = True if ele_tags is None else False
        self.refactor_resp_data(ele_tags, resp_type, component)
        alpha_, maxstep, clim = self._get_resp_scale_factor()
        nb_frames = self.num_steps
        times = int(nb_frames / framerate)
        # -----------------------------------------------------------------------------
        # start plot
        frames = []
        for i in range(nb_frames):
            plotter = []
            self._create_mesh(
                plotter=plotter,
                value=i,
                alpha=alpha_ * alpha,
                clim=clim,
                ele_tags=ele_tags,
                coloraxis="coloraxis",
                show_values=show_values,
                plot_all_mesh=plot_all_mesh,
                line_width=line_width,
            )
            frames.append(go.Frame(data=plotter, name="step:" + str(i)))
        self.FIGURE = go.Figure(frames=frames)
        # Add data to be displayed before animation starts
        plotter0 = []
        self._create_mesh(
            plotter0,
            0,
            ele_tags=ele_tags,
            alpha=alpha_,
            coloraxis="coloraxis",
            clim=clim,
            show_values=show_values,
            plot_all_mesh=plot_all_mesh,
            line_width=line_width,
        )
        self.FIGURE.add_traces(plotter0)

        def frame_args(duration):
            return {
                "frame": {"duration": duration},
                "mode": "immediate",
                "fromcurrent": True,
                "transition": {"duration": duration, "easing": "linear"},
            }

        sliders = [
            {
                "pad": {"b": 10, "t": 60},
                "len": 0.9,
                "x": 0.1,
                "y": 0,
                "steps": [
                    {
                        "args": [[f.name], frame_args(0)],
                        "label": "step:" + str(k),
                        "method": "animate",
                    }
                    for k, f in enumerate(self.FIGURE.frames)
                ],
            }
        ]
        # Layout
        for i in range(len(self.FIGURE.frames)):
            txt = self._make_txt(i)
            self.FIGURE.frames[i]["layout"].update(title=txt)
        self.FIGURE.update_layout(
            coloraxis=dict(
                colorscale=self.pargs.cmap,
                cmin=clim[0],
                cmax=clim[1],
                colorbar=dict(tickfont=dict(size=15)),
            ),
            updatemenus=[
                {
                    "buttons": [
                        {
                            "args": [None, frame_args(times)],
                            "label": "&#9654;",  # play symbol
                            "method": "animate",
                        },
                        {
                            "args": [[None], frame_args(0)],
                            "label": "&#9724;",  # pause symbol
                            "method": "animate",
                        },
                    ],
                    "direction": "left",
                    "pad": {"r": 10, "t": 70},
                    "type": "buttons",
                    "x": 0.1,
                    "y": 0,
                }
            ],
            sliders=sliders,
        )

    def update_fig(self, show_outline: bool = False):
        if not self.show_zaxis:
            eye = dict(x=0.0, y=-0.1, z=10)  # for 2D camera
            scene = dict(
                camera=dict(eye=eye, projection=dict(type="orthographic")),
            )
        else:
            eye = dict(x=-3.5, y=-3.5, z=3.5)  # for 3D camera
            scene = dict(
                aspectratio=dict(x=1, y=1, z=1),
                aspectmode="data",
                camera=dict(eye=eye, projection=dict(type="orthographic")),
            )
        self.FIGURE.update_layout(
            template=self.pargs.theme,
            autosize=True,
            showlegend=False,
            scene=scene,
            # title=title,
            font=dict(family=self.pargs.font_family),
        )

        if not show_outline:
            self.FIGURE.update_layout(
                scene=dict(
                    xaxis={"showgrid": False, "zeroline": False, "visible": False},
                    yaxis={"showgrid": False, "zeroline": False, "visible": False},
                    zaxis={"showgrid": False, "zeroline": False, "visible": False},
                ),
            )
        return self.FIGURE


def plot_frame_responses(
    odb_tag: Union[int, str] = 1,
    ele_tags: Union[int, list] = None,
    resp_type: str = "sectionForces",
    resp_dof: str = "MZ",
    slides: bool = False,
    scale: float = 1.0,
    show_values: bool = False,
    line_width: float = 5.0,
    show_outline: bool = False,
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

    line_width: float, default: 1.5.
        Line width of the response graph.
    show_outline: bool, default: False
        Whether to display the outline of the model.

    Returns
    -------
    fig: `plotly.graph_objects.Figure <https://plotly.com/python-api-reference/generated/plotly.graph_objects.Figure.html>`_
        You can use `fig.show()` to display,
        You can also use `fig.write_html("path/to/file.html")` to save as an HTML file, see
        `Interactive HTML Export in Python <https://plotly.com/python/interactive-html-export/>`_
    """
    model_info_steps, model_update, beam_resp_steps = loadODB(
        odb_tag, resp_type="Frame"
    )
    plotbase = PlotFrameResponse(model_info_steps, beam_resp_steps, model_update)
    if slides:
        plotbase.plot_slide(
            ele_tags=ele_tags,
            alpha=scale,
            show_values=show_values,
            resp_type=resp_type,
            component=resp_dof,
            line_width=line_width,
        )
    else:
        plotbase.plot_peak_step(
            ele_tags=ele_tags,
            alpha=scale,
            show_values=show_values,
            resp_type=resp_type,
            component=resp_dof,
            line_width=line_width,
        )
    return plotbase.update_fig(show_outline=show_outline)


def plot_frame_responses_animation(
    odb_tag: Union[int, str] = 1,
    ele_tags: Union[int, list] = None,
    resp_type: str = "sectionForces",
    resp_dof: str = "MZ",
    scale: float = 1.0,
    show_values: bool = False,
    framerate: int = None,
    line_width: float = 1.5,
    show_outline: bool = False,
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
    line_width: float, default: 1.5.
        Line width of the response graph.
    show_outline: bool, default: False
        Whether to display the outline of the model.

    Returns
    -------
    fig: `plotly.graph_objects.Figure <https://plotly.com/python-api-reference/generated/plotly.graph_objects.Figure.html>`_
        You can use `fig.show()` to display,
        You can also use `fig.write_html("path/to/file.html")` to save as an HTML file, see
        `Interactive HTML Export in Python <https://plotly.com/python/interactive-html-export/>`_
    """
    model_info_steps, model_update, beam_resp_steps = loadODB(
        odb_tag, resp_type="Frame"
    )
    plotbase = PlotFrameResponse(model_info_steps, beam_resp_steps, model_update)
    plotbase.plot_anim(
        ele_tags=ele_tags,
        alpha=scale,
        show_values=show_values,
        resp_type=resp_type,
        component=resp_dof,
        framerate=framerate,
        line_width=line_width,
    )
    return plotbase.update_fig(show_outline=show_outline)
