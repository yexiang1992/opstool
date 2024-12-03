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
from ...utils import gram_schmidt, PKG_NAME


class PlotTrussResponse(PlotResponseBase):

    def __init__(self, model_info_steps, truss_resp_step, model_update):
        super().__init__(model_info_steps, truss_resp_step, model_update)

    def _get_truss_data(self, step):
        return self._get_model_data("TrussData", step)

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

    def _get_resp_peak(self):
        resp_step = self.resp_step
        maxv = [np.max(np.abs(data)) for data in resp_step]
        maxstep = np.argmax(maxv)
        maxv = np.max(maxv)
        cmin, cmax = self._get_truss_resp_clim()
        if maxv == 0:
            alpha_ = 0.0
        else:
            alpha_ = self.max_bound_size * self.pargs.scale_factor / maxv
        return maxstep, (cmin, cmax), alpha_

    def _get_truss_resp_clim(self):
        maxv = [np.max(data) for data in self.resp_step]
        minv = [np.min(data) for data in self.resp_step]
        cmin, cmax = np.min(minv), np.max(maxv)
        return cmin, cmax

    def _create_mesh(
        self,
        plotter,
        value,
        ele_tags=None,
        show_values=True,
        plot_all_mesh=True,
        clim=None,
        coloraxis="coloraxis",
        alpha=1.0,
        line_width=1.5,
    ):
        step = int(round(value))
        truss_tags, truss_coords, truss_cells = self._make_truss_info(ele_tags, step)
        resps = self.resp_step[step].to_numpy()
        resp_points, resp_cells = [], []
        scalars = []
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
        resp_points = np.array(resp_points)
        scalars = np.array(scalars)
        #  ---------------------------------
        if plot_all_mesh:
            self._plot_all_mesh(plotter, step=step)
        line_points, line_mid_points = self._get_plotly_line_data(
            truss_coords, truss_cells, scalars=None
        )
        _plot_lines(
            plotter,
            pos=line_points,
            width=self.pargs.line_width,
            color=self.pargs.color_truss,
            name="Truss",
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
        resp = self.resp_step[step].to_numpy()
        maxv = np.max(resp)
        minv = np.min(resp)
        t_ = self.time[step]
        title = f'<span style="font-weight:bold; font-size:{self.pargs.title_font_size}">{PKG_NAME}'
        title += " :: Truss Responses 3D Viewer</span><br><br><br>"
        title += f"<b>{self.resp_type.capitalize()}</b><br>"
        # comp = (
        #     self.component
        #     if isinstance(self.component, str)
        #     else " ".join(self.component)
        # )
        # title += f"<b>{comp}</b><br>"
        maxv = self._set_txt_props(f"{maxv:.3E}")
        minv = self._set_txt_props(f"{minv:.3E}")
        title += f"<b>Max.:</b> {maxv}<br><b>Min.:</b> {minv}"
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
        show_values=True,
        alpha=1.0,
        line_width=1.5,
    ):
        plot_all_mesh = True if ele_tags is None else False
        _, clim, alpha_ = self._get_resp_peak()
        n_data = None
        for i in range(self.num_steps):
            plotter = []
            self._create_mesh(
                plotter,
                i,
                alpha=alpha_ * alpha,
                ele_tags=ele_tags,
                clim=clim,
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
        show_values=True,
        alpha=1.0,
        line_width=1.5,
    ):
        plot_all_mesh = True if ele_tags is None else False
        max_step, clim, alpha_ = self._get_resp_peak()

        plotter = []
        self._create_mesh(
            plotter=plotter,
            value=max_step,
            ele_tags=ele_tags,
            alpha=alpha_ * alpha,
            clim=clim,
            coloraxis="coloraxis",
            show_values=show_values,
            plot_all_mesh=plot_all_mesh,
            line_width=line_width,
        )
        self.FIGURE.add_traces(plotter)
        txt = self._make_txt(max_step)
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
        show_values=True,
        alpha=1.0,
        framerate: int = None,
        line_width=1.5,
    ):
        if framerate is None:
            framerate = np.ceil(self.num_steps / 10)
        plot_all_mesh = True if ele_tags is None else False
        _, clim, alpha_ = self._get_resp_peak()
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
                ele_tags=ele_tags,
                alpha=alpha_ * alpha,
                clim=clim,
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
            alpha=alpha_,
            ele_tags=ele_tags,
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


def plot_truss_responses(
    odb_tag: Union[int, str] = 1,
    ele_tags: Union[int, list] = None,
    slides: bool = False,
    show_values: bool = True,
    resp_type: str = "axialForce",
    alpha: float = 1.0,
    show_outline: bool = False,
    line_width: float = 1.5,
):
    """Visualizing Truss Response.

    Parameters
    ----------
    odb_tag: Union[int, str], default: 1
        Tag of output databases (ODB) to be visualized.
    ele_tags: Union[int, list], default: None
        The tags of truss elements to be visualized. If None, all truss elements are selected.
    slides: bool, default: False
        Display the response for each step in the form of a slideshow.
        Otherwise, show the step with the largest response.
    show_values: bool, default: True
        Whether to display the response value.
    resp_type: str, default: "axialForce"
        Response type, optional, one of ["axialForce", "axialDefo", "Stress", "Strain"].
    alpha: float, default: 1.0
        Scale the size of the response graph.

        .. Note::
            You can adjust the scale to make the response graph more visible.
            A negative number will reverse the direction.

    show_outline: bool, default: False
        Whether to display the outline of the model.
    line_width: float, default: 1.5.
        Line width of the response graph.

    Returns
    -------
    fig: `plotly.graph_objects.Figure <https://plotly.com/python-api-reference/generated/plotly.graph_objects.Figure.html>`_
        You can use `fig.show()` to display,
        You can also use `fig.write_html("path/to/file.html")` to save as an HTML file, see
        `Interactive HTML Export in Python <https://plotly.com/python/interactive-html-export/>`_
    """
    model_info_steps, model_update, truss_resp_step = loadODB(
        odb_tag, resp_type="Truss"
    )
    plotbase = PlotTrussResponse(model_info_steps, truss_resp_step, model_update)
    plotbase.refactor_resp_step(resp_type=resp_type, ele_tags=ele_tags)
    if slides:
        plotbase.plot_slide(
            ele_tags=ele_tags,
            show_values=show_values,
            alpha=alpha,
            line_width=line_width,
        )
    else:
        plotbase.plot_peak_step(
            show_values=show_values,
            alpha=alpha,
            line_width=line_width,
        )
    return plotbase.update_fig(show_outline=show_outline)


def plot_truss_responses_animation(
    odb_tag: Union[int, str] = 1,
    ele_tags: Union[int, list] = None,
    framerate: int = None,
    show_values: bool = False,
    resp_type: str = "axialForce",
    alpha: float = 1.0,
    show_outline: bool = False,
    line_width: float = 1.5,
):
    """Truss response animation.

    Parameters
    ----------
    odb_tag: Union[int, str], default: 1
        Tag of output databases (ODB) to be visualized.
    ele_tags: Union[int, list], default: None
        The tags of truss elements to be visualized. If None, all truss elements are selected.
    framerate: int, default: None
        Framerate for the display, i.e., the number of frames per second.
    show_values: bool, default: False
        Whether to display the response value.
    resp_type: str, default: "axialForce"
        Response type, optional, one of ["axialForce", "axialDefo", "Stress", "Strain"].
    alpha: float, default: 1.0
        Scale the size of the response graph.

        .. Note::
            You can adjust the scale to make the response graph more visible.
            A negative number will reverse the direction.

    show_outline: bool, default: False
        Whether to display the outline of the model.
    line_width: float, default: 1.5.
        Line width of the response graph.

    Returns
    -------
    fig: `plotly.graph_objects.Figure <https://plotly.com/python-api-reference/generated/plotly.graph_objects.Figure.html>`_
        You can use `fig.show()` to display,
        You can also use `fig.write_html("path/to/file.html")` to save as an HTML file, see
        `Interactive HTML Export in Python <https://plotly.com/python/interactive-html-export/>`_
    """
    model_info_steps, model_update, truss_resp_step = loadODB(
        odb_tag, resp_type="Truss"
    )
    plotbase = PlotTrussResponse(model_info_steps, truss_resp_step, model_update)
    plotbase.refactor_resp_step(resp_type=resp_type, ele_tags=ele_tags)
    plotbase.plot_anim(
        ele_tags=ele_tags,
        show_values=show_values,
        alpha=alpha,
        framerate=framerate,
        line_width=line_width,
    )
    return plotbase.update_fig(show_outline=show_outline)
