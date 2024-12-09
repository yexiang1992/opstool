from typing import Union

import numpy as np
import plotly.graph_objs as go

from .plot_resp_base import PlotResponseBase

from .plot_utils import (
    _plot_points_cmap,
    _plot_unstru_cmap,
    _plot_lines_cmap,
    _plot_all_mesh,
    _get_line_cells,
    _get_unstru_cells,
)
from .vis_model import _plot_bc, _plot_mp_constraint
from ...post import loadODB
from ...utils import PKG_NAME


class PlotNodalResponse(PlotResponseBase):

    def __init__(
        self,
        model_info_steps,
        node_resp_steps,
        model_update,
    ):
        super().__init__(model_info_steps, node_resp_steps, model_update)
        self.FIGURE = go.Figure()

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

    def _get_resp_clim_peak(self):
        resps = []
        for i in range(self.num_steps):
            da = self._get_resp_data(i, self.resp_type, self.component)
            if da.ndim == 1:
                resps.append(da)
            else:
                resps.append(np.linalg.norm(da, axis=1))
        max_resps = [np.max(resp) for resp in resps]
        min_resps = [np.min(resp) for resp in resps]
        cmin, cmax = np.min(min_resps), np.max(max_resps)
        max_step = np.argmax(max_resps)
        return cmin, cmax, max_step

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
        return alpha_

    def _make_txt(self, step):
        resp = self._get_resp_data(step, self.resp_type, self.component)
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
        # txt = f"{self.comp}:: Max: {max_resp}\n"
        # txt += f"{self.comp}:: Min: {min_resp}\n"
        t_ = self.time[step]
        title = f'<span style="font-weight:bold; font-size:{self.pargs.title_font_size}">{PKG_NAME}'
        title += " :: Nodal Responses 3D Viewer</span><br><br><br>"
        title += f"<b>{self.resp_type.capitalize()}</b> --> "
        comp = (
            self.component
            if isinstance(self.component, str)
            else " ".join(self.component)
        )
        title += f"<b>{comp}</b><br>"
        max_norm = self._set_txt_props(f"{max_norm:.3E}")
        min_norm = self._set_txt_props(f"{min_norm:.3E}")
        title += f"<b>Norm.Max:</b> {max_norm}<br><b>Norm.Min:</b> {min_norm}"
        step_txt = self._set_txt_props(f"{step}")
        title += f"<br><b>step:</b> {step_txt}; "
        t_txt = self._set_txt_props(f"{t_:.3f}")
        title += f"<b>time</b>: {t_txt}"
        txt = dict(
            font=dict(size=self.pargs.font_size),
            text=title,
        )
        return txt

    def _create_mesh(
        self,
        plotter,
        value,
        alpha=1.0,
        clim=None,
        style="surface",
        coloraxis=None,
        show_origin=False,
        show_bc: bool = True,
        bc_scale: float = 1.0,
        show_mp_constraint: bool = True,
    ):
        step = int(round(value))
        node_nodeform_coords = self._get_node_data(step)
        # bounds = self._get_node_data(step).attrs["bounds"]
        # model_dims = self._get_node_data(step).attrs["ndims"]
        line_cells, _ = _get_line_cells(self._get_line_data(step))
        _, unstru_cell_types, unstru_cells = _get_unstru_cells(
            self._get_unstru_data(step)
        )
        # t_ = self.time[step]
        node_disp = self._get_deformation_data(step)
        node_resp = self._get_resp_data(step, self.resp_type, self.component)
        is_coord_equal = np.array_equal(
            node_nodeform_coords.coords["tags"].values,
            node_disp.coords["nodeTags"].values
        )
        if not is_coord_equal:
            common_coords = np.intersect1d(
                node_nodeform_coords.coords["tags"].values,
                node_disp.coords["nodeTags"].values
            )
            node_nodeform_coords = node_nodeform_coords.sel({"tags": common_coords})
            node_disp = node_disp.sel({"nodeTags": common_coords})
            node_resp = node_resp.sel({"nodeTags": common_coords})
        node_nodeform_coords = node_nodeform_coords.to_numpy()
        node_disp = node_disp.to_numpy()
        node_resp = node_resp.to_numpy()
        if alpha > 0.0:
            node_deform_coords = alpha * node_disp + node_nodeform_coords
        else:
            node_deform_coords = node_nodeform_coords
        if node_resp.ndim == 1:
            scalars = node_resp
        else:
            scalars = np.linalg.norm(node_resp, axis=1)
        if len(unstru_cells) > 0:
            (
                face_points,
                face_line_points,
                face_mid_points,
                veci,
                vecj,
                veck,
                face_scalars,
                face_line_scalars,
            ) = self._get_plotly_unstru_data(
                node_deform_coords, unstru_cell_types, unstru_cells, scalars
            )
            _plot_unstru_cmap(
                plotter,
                face_points,
                veci=veci,
                vecj=vecj,
                veck=veck,
                scalars=face_scalars,
                clim=clim,
                coloraxis=coloraxis,
                style=style,
                line_width=self.pargs.line_width,
                opacity=self.pargs.mesh_opacity,
                show_edges=self.pargs.show_mesh_edges,
                edge_color=self.pargs.mesh_edge_color,
                edge_width=self.pargs.mesh_edge_width,
                edge_points=face_line_points,
                edge_scalars=face_line_scalars,
            )
        if len(line_cells) > 0:
            line_points, line_mid_points, line_scalars = self._get_plotly_line_data(
                node_deform_coords, line_cells, scalars
            )
            _plot_lines_cmap(
                plotter,
                line_points,
                scalars=line_scalars,
                coloraxis=coloraxis,
                clim=clim,
                width=self.pargs.line_width,
            )
        _plot_points_cmap(
            plotter, node_deform_coords, scalars=scalars, clim=clim, coloraxis=coloraxis,
            name=self.resp_type, size=self.pargs.point_size
        )
        if show_bc:
            fixed_node_data = self._get_bc_data(step)
            if len(fixed_node_data) > 0:
                fixed_data = fixed_node_data.to_numpy()
                fixed_dofs = fixed_data[:, -6:].astype(int)
                fixed_coords = fixed_data[:, :3]
                max_bound = self._get_node_data(step).attrs["maxBoundSize"]
                min_bound = self._get_node_data(step).attrs["minBoundSize"]
                s = (max_bound + min_bound) / 100 * bc_scale
                _plot_bc(
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
                _plot_mp_constraint(
                    plotter,
                    node_deform_coords,
                    cells,
                    None,
                    self.pargs.line_width / 2,
                    self.pargs.color_constraint,
                    show_dofs=False,
                )
        if show_origin:
            (
                face_points,
                face_line_points,
                face_mid_points,
                veci,
                vecj,
                veck,
            ) = self._get_plotly_unstru_data(
                node_nodeform_coords, unstru_cell_types, unstru_cells, scalars=None
            )
            line_points, line_mid_points = self._get_plotly_line_data(
                node_nodeform_coords, line_cells, scalars=None
            )
            _plot_all_mesh(
                plotter, line_points, face_line_points, color="#738595", width=1.5
            )

    def plot_slide(
        self,
        alpha=1.0,
        show_defo=True,
        show_bc: bool = True,
        bc_scale: float = 1.0,
        show_mp_constraint: bool = True,
        style="surface",
        show_origin=False,
    ):
        cmin, cmax, _ = self._get_resp_clim_peak()
        clim = (cmin, cmax)
        if show_defo:
            alpha_ = self._get_defo_scale_factor()
            alpha_ = alpha_ * alpha if alpha else alpha_
        else:
            alpha_ = 0.0
        n_data = None
        for i in range(self.num_steps):
            plotter = []
            self._create_mesh(
                plotter,
                i,
                alpha=alpha_,
                clim=clim,
                coloraxis=f"coloraxis{i + 1}",
                show_bc=show_bc,
                bc_scale=bc_scale,
                show_mp_constraint=show_mp_constraint,
                style=style,
                show_origin=show_origin,
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
        alpha=1.0,
        show_defo=True,
        show_bc: bool = True,
        bc_scale: float = 1.0,
        show_mp_constraint: bool = True,
        style="surface",
        show_origin=False,
    ):
        cmin, cmax, max_step = self._get_resp_clim_peak()
        clim = (cmin, cmax)
        if show_defo:
            alpha_ = self._get_defo_scale_factor()
            alpha_ = alpha_ * alpha if alpha else alpha_
        else:
            alpha_ = 0.0
        plotter = []
        self._create_mesh(
            plotter=plotter,
            value=max_step,
            alpha=alpha_,
            clim=clim,
            coloraxis="coloraxis",
            show_bc=show_bc,
            bc_scale=bc_scale,
            show_mp_constraint=show_mp_constraint,
            style=style,
            show_origin=show_origin,
        )
        self.FIGURE.add_traces(plotter)
        txt = self._make_txt(max_step)
        self.FIGURE.update_layout(
            coloraxis=dict(
                colorscale=self.pargs.cmap,
                cmin=cmin,
                cmax=cmax,
                colorbar=dict(tickfont=dict(size=self.pargs.font_size - 2)),
            ),
            title=txt,
        )

    def plot_anim(
        self,
        alpha=1.0,
        show_defo=True,
        framerate: int = None,
        show_bc: bool = True,
        bc_scale: float = 1.0,
        show_mp_constraint: bool = True,
        style="surface",
        show_origin=False,
    ):
        if framerate is None:
            framerate = np.ceil(self.num_steps / 10)
        cmin, cmax, _ = self._get_resp_clim_peak()
        clim = (cmin, cmax)
        if show_defo:
            alpha_ = self._get_defo_scale_factor()
            alpha_ = alpha_ * alpha if alpha else alpha_
        else:
            alpha_ = 0.0
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
                alpha=alpha_,
                clim=clim,
                coloraxis="coloraxis",
                show_bc=show_bc,
                bc_scale=bc_scale,
                show_mp_constraint=show_mp_constraint,
                style=style,
                show_origin=show_origin,
            )
            frames.append(go.Frame(data=plotter, name="step:" + str(i)))
        self.FIGURE = go.Figure(frames=frames)
        # Add data to be displayed before animation starts
        plotter0 = []
        self._create_mesh(
            plotter0,
            0,
            alpha=alpha_,
            coloraxis="coloraxis",
            show_bc=show_bc,
            bc_scale=bc_scale,
            show_mp_constraint=show_mp_constraint,
            style=style,
            show_origin=show_origin,
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
                cmin=cmin,
                cmax=cmax,
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


def plot_nodal_responses(
    odb_tag: Union[int, str] = 1,
    slides: bool = False,
    scale: float = 1.0,
    show_defo: bool = True,
    resp_type: str = "disp",
    resp_dof: Union[list, tuple, str] = ("UX", "UY", "UZ"),
    show_bc: bool = True,
    bc_scale: float = 1.0,
    show_mp_constraint: bool = True,
    show_undeformed: bool = False,
    style: str = "surface",
    show_outline: bool = False,
):
    """Visualizing Node Responses.

    Parameters
    ----------
    odb_tag: Union[int, str], default: 1
        Tag of output databases (ODB) to be visualized.
    slides: bool, default: False
        Display the response for each step in the form of a slideshow.
        Otherwise, show the step with the largest response.
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

    show_bc: bool, default: True
        Whether to display boundary supports.
    bc_scale: float, default: 1.0
        Scale the size of boundary support display.
    show_mp_constraint: bool, default: True
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
    fig: `plotly.graph_objects.Figure <https://plotly.com/python-api-reference/generated/plotly.graph_objects.Figure.html>`_
        You can use `fig.show()` to display,
        You can also use `fig.write_html("path/to/file.html")` to save as an HTML file, see
        `Interactive HTML Export in Python <https://plotly.com/python/interactive-html-export/>`_
    """
    model_info_steps, model_update, node_resp_steps = loadODB(
        odb_tag, resp_type="Nodal"
    )
    plotbase = PlotNodalResponse(model_info_steps, node_resp_steps, model_update)
    plotbase.set_comp_resp_type(resp_type=resp_type, component=resp_dof)
    if slides:
        plotbase.plot_slide(
            alpha=scale,
            show_defo=show_defo,
            show_bc=show_bc,
            bc_scale=bc_scale,
            show_mp_constraint=show_mp_constraint,
            style=style,
            show_origin=show_undeformed,
        )
    else:
        plotbase.plot_peak_step(
            alpha=scale,
            show_defo=show_defo,
            show_bc=show_bc,
            bc_scale=bc_scale,
            show_mp_constraint=show_mp_constraint,
            style=style,
            show_origin=show_undeformed,
        )
    return plotbase.update_fig(show_outline=show_outline)


def plot_nodal_responses_animation(
    odb_tag: Union[int, str] = 1,
    framerate: int = None,
    scale: float = 1.0,
    show_defo: bool = True,
    resp_type: str = "disp",
    resp_dof: Union[list, tuple, str] = ("UX", "UY", "UZ"),
    show_bc: bool = True,
    bc_scale: float = 1.0,
    show_mp_constraint: bool = True,
    show_undeformed: bool = False,
    style: str = "surface",
    show_outline: bool = False,
):
    """Visualize node response animation.

    Parameters
    ----------
    odb_tag: Union[int, str], default: 1
        Tag of output databases (ODB) to be visualized.
    framerate: int, default: 5
        Framerate for the display, i.e., the number of frames per second.
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
    show_bc: bool, default: True
        Whether to display boundary supports.
    bc_scale: float, default: 1.0
        Scale the size of boundary support display.
    show_mp_constraint: bool, default: True
        Whether to show multipoint (MP) constraint.
    show_undeformed: bool, default: False
        Whether to show the undeformed shape of the model.
    show_outline: bool, default: False
        Whether to display the outline of the model.
    style: str, default: surface
        Visualization mesh style of surfaces and solids.
        One of the following: style='surface' or style='wireframe'
        Defaults to 'surface'. Note that 'wireframe' only shows a wireframe of the outer geometry.

    Returns
    -------
    fig: `plotly.graph_objects.Figure <https://plotly.com/python-api-reference/generated/plotly.graph_objects.Figure.html>`_
        You can use `fig.show()` to display,
        You can also use `fig.write_html("path/to/file.html")` to save as an HTML file, see
        `Interactive HTML Export in Python <https://plotly.com/python/interactive-html-export/>`_
    """
    model_info_steps, model_update, node_resp_steps = loadODB(
        odb_tag, resp_type="Nodal"
    )
    plotbase = PlotNodalResponse(model_info_steps, node_resp_steps, model_update)
    plotbase.set_comp_resp_type(resp_type=resp_type, component=resp_dof)
    plotbase.plot_anim(
        alpha=scale,
        show_defo=show_defo,
        framerate=framerate,
        show_bc=show_bc,
        bc_scale=bc_scale,
        show_mp_constraint=show_mp_constraint,
        style=style,
        show_origin=show_undeformed,
    )
    return plotbase.update_fig(show_outline=show_outline)
