from typing import Union

import numpy as np
import plotly.graph_objs as go

from .plot_resp_base import PlotResponseBase

from .plot_utils import (
    _plot_points_cmap,
    _plot_unstru_cmap,
    _plot_all_mesh,
    _get_line_cells,
    _get_unstru_cells,
    _get_plotly_dim_scene
)
from ...post import loadODB
from ...utils import CONSTANTS
PKG_NAME = CONSTANTS.get_pkg_name()


class PlotUnstruResponse(PlotResponseBase):

    def __init__(self, model_info_steps, resp_step, model_update):
        super().__init__(model_info_steps, resp_step, model_update)
        self.ele_type = "Shell"

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
        _plot_all_mesh(
            plotter, line_points, face_line_points, color=color, width=1.5
        )

    def _get_unstru_data(self, step):
        if self.ele_type.lower() == "shell":
            return self._get_model_data("ShellData", step)
        elif self.ele_type.lower() == "plane":
            return self._get_model_data("PlaneData", step)
        elif self.ele_type.lower() in ["brick", "solid"]:
            return self._get_model_data("BrickData", step)
        else:
            raise ValueError(
                f"Invalid element type {self.ele_type}! "
                "Valid options are: Shell, Plane, Brick."
            )

    def _set_comp_resp_type(self, ele_type, resp_type, component):
        self.ele_type = ele_type
        self.resp_type = resp_type
        self.component = component

    def _make_unstru_info(self, ele_tags, step):
        pos = self._get_node_data(step).to_numpy()
        unstru_data = self._get_unstru_data(step)
        if ele_tags is None:
            tags, cell_types, cells = _get_unstru_cells(unstru_data)
        else:
            tags = np.atleast_1d(ele_tags)
            cells = unstru_data.sel(eleTags=tags)
            tags, cell_types, cells = _get_unstru_cells(cells)
        return tags, pos, cells, cell_types

    def refactor_resp_step(self, ele_tags, ele_type, resp_type: str, component: str):
        self._set_comp_resp_type(ele_type, resp_type, component)
        resps = []
        if self.ModelUpdate or ele_tags is not None:
            for i in range(self.num_steps):
                tags, _, _, _ = self._make_unstru_info(ele_tags, i)
                da = self._get_resp_data(i, self.resp_type, self.component)
                da = da.sel(eleTags=tags)
                resps.append(da.mean(dim="GaussPoints", skipna=True))
        else:
            for i in range(self.num_steps):
                da = self._get_resp_data(i, self.resp_type, self.component)
                resps.append(da.mean(dim="GaussPoints", skipna=True))
        self.resp_step = resps

    def _get_resp_peak(self):
        resp_step = self.resp_step
        maxv = [np.max(np.abs(data)) for data in resp_step]
        maxstep = np.argmax(maxv)
        cmin, cmax = self._get_resp_clim()
        return maxstep, (cmin, cmax)

    def _get_resp_clim(self):
        maxv = [np.max(data) for data in self.resp_step]
        minv = [np.min(data) for data in self.resp_step]
        cmin, cmax = np.min(minv), np.max(maxv)
        return cmin, cmax

    def _create_mesh(
        self,
        plotter,
        value,
        ele_tags=None,
        plot_all_mesh=True,
        clim=None,
        coloraxis="coloraxis",
        style="surface",
        show_values=False,
    ):
        step = int(round(value))
        tags, pos, cells, cell_types = self._make_unstru_info(ele_tags, step)
        resps = self.resp_step[step].to_numpy()
        scalars = resps
        #  ---------------------------------
        if plot_all_mesh:
            self._plot_all_mesh(plotter, step=step)
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
            pos, cell_types, cells, scalars, scalars_by_element=True
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
        if show_values:
            _plot_points_cmap(
                plotter, face_points, scalars=face_scalars, clim=clim, coloraxis=coloraxis,
                name=self.resp_type, size=self.pargs.point_size
            )

    def _make_txt(self, step):
        resp = self.resp_step[step].to_numpy()
        maxv, minv = np.max(resp), np.min(resp)
        t_ = self.time[step]
        title = f'<span style="font-weight:bold; font-size:{self.pargs.title_font_size}">{PKG_NAME}'
        title += f" :: {self.ele_type} Responses 3D Viewer</span><br><br><br>"
        title += f"<b>{self.resp_type.capitalize()}</b> --> "
        comp = (
            self.component
            if isinstance(self.component, str)
            else " ".join(self.component)
        )
        title += f"<b>{comp}</b><br>"
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
        style="surface",
        show_values=False,
    ):
        plot_all_mesh = True if ele_tags is None else False
        _, clim = self._get_resp_peak()
        n_data = None
        for i in range(self.num_steps):
            plotter = []
            self._create_mesh(
                plotter,
                i,
                ele_tags=ele_tags,
                clim=clim,
                coloraxis=f"coloraxis{i + 1}",
                show_values=show_values,
                plot_all_mesh=plot_all_mesh,
                style=style,
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
            step["args"][0]["visible"][n_data * i: n_data * (i + 1)] = [True] * n_data
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
        style="surface",
        show_values=False,
    ):
        plot_all_mesh = True if ele_tags is None else False
        max_step, clim = self._get_resp_peak()
        plotter = []
        self._create_mesh(
            plotter=plotter,
            value=max_step,
            ele_tags=ele_tags,
            clim=clim,
            coloraxis="coloraxis",
            show_values=show_values,
            plot_all_mesh=plot_all_mesh,
            style=style,
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
        framerate: int = None,
        style="surface",
        show_values=False,
    ):
        if framerate is None:
            framerate = np.ceil(self.num_steps / 11)
        nb_frames = self.num_steps
        times = int(nb_frames / framerate)
        # ---------------------------------------------
        plot_all_mesh = True if ele_tags is None else False
        _, clim = self._get_resp_peak()
        # -----------------------------------------------------------------------------
        # start plot
        frames = []
        for i in range(nb_frames):
            plotter = []
            self._create_mesh(
                plotter=plotter,
                value=i,
                ele_tags=ele_tags,
                clim=clim,
                coloraxis="coloraxis",
                show_values=show_values,
                plot_all_mesh=plot_all_mesh,
                style=style,
            )
            frames.append(go.Frame(data=plotter, name="step:" + str(i)))
        self.FIGURE = go.Figure(frames=frames)
        # Add data to be displayed before animation starts
        plotter0 = []
        self._create_mesh(
            plotter0,
            0,
            ele_tags=ele_tags,
            clim=clim,
            coloraxis="coloraxis",
            show_values=show_values,
            plot_all_mesh=plot_all_mesh,
            style=style,
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
            scene = _get_plotly_dim_scene(mode="2d", show_outline=show_outline)
        else:
            scene = _get_plotly_dim_scene(mode="3d", show_outline=show_outline)
        self.FIGURE.update_layout(
            template=self.pargs.theme,
            autosize=True,
            showlegend=False,
            scene=scene,
            # title=title,
            font=dict(family=self.pargs.font_family),
        )
        return self.FIGURE


def plot_unstruct_responses(
    odb_tag: Union[int, str] = 1,
    ele_type: str = "Shell",
    ele_tags: Union[int, list] = None,
    slides: bool = False,
    resp_type: str = "sectionForces",
    resp_dof: str = "MXX",
    style: str = "surface",
    show_outline: bool = False,
    show_values: bool = False,
):
    """Visualizing unstructured element (Shell, Plane, Brick) Response.

    .. Note::
        The responses at all Gaussian points are averaged.

    Parameters
    ----------
    odb_tag: Union[int, str], default: 1
        Tag of output databases (ODB) to be visualized.
    ele_tags: Union[int, list], default: None
        The tags of elements to be visualized.
        If None, all elements are selected.
    slides: bool, default: False
        Display the response for each step in the form of a slideshow.
        Otherwise, show the step with the largest response.
    ele_type: str, default: "Shell"
        Element type, optional, one of ["Shell", "Plane", "Solid"].
    resp_type: str, default: None
        Response type, which dependents on the element type `ele_type`.

        #. For ``Shell`` elements, one of ["sectionForces", "sectionDeformations"].
            I.e., section forces and deformations at Gaussian integration points (per unit length).
            If None, defaults to "sectionForces".
        #. For ``Plane`` elements, one of ["stresses", "strains"].
            I.e., stresses and strains at Gaussian integration points.
            If None, defaults to "stresses".
        #. For ``Brick`` or ``Solid`` elements, one of ["stresses", "strains"].
            I.e., stresses and strains at Gaussian integration points.
            If None, defaults to "stresses".

    resp_dof: str, default: None
        Dof to be visualized, which dependents on the element type `ele_type`.

        .. Note::
            The `resp_dof` here is consistent with stress-strain (force-deformation),
            and whether it is stress or strain depends on the parameter `resp_type`.

        #. For ``Shell`` elements, one of ["FXX", "FYY", "FXY", "MXX", "MYY", "MXY", "VXZ", "VYZ"].
            If None, defaults to "MXX".
        #. For ``Plane`` elements, one of ["sigma11", "sigma22", "sigma12", "p1", "p2", "sigma_vm", "tau_max"].

            * "sigma11, sigma22, sigma12": Normal stress and shear stress (strain) in the x-y plane.
            * "p1, p2": Principal stresses (strains).
            * "sigma_vm": Von Mises stress.
            * "tau_max": Maximum shear stress (strains).
            * If None, defaults to "sigma_vm".

        #. For ``Brick`` or ``Solid`` elements, one of ["sigma11", "sigma22", "sigma33", "sigma12", "sigma23", "sigma13", "p1", "p2", "p3", "sigma_vm", "tau_max", "sigma_oct", "tau_oct"]

            * "sigma11, sigma22, sigma33": Normal stress (strain) along x, y, z.
            * "sigma12, sigma23, sigma13": Shear stress (strain).
            * "p1, p2, p3": Principal stresses (strains).
            * "sigma_vm": Von Mises stress.
            * "tau_max": Maximum shear stress (strains).
            * "sigma_oct": Octahedral normal stress (strains).
            * "tau_oct": Octahedral shear stress (strains).
            * If None, defaults to "sigma_vm".

    style: str, default: surface
        Visualization mesh style of surfaces and solids.
        One of the following: style='surface' or style='wireframe'
        Defaults to 'surface'. Note that 'wireframe' only shows a wireframe of the outer geometry.
    show_values: bool, default: True
        Whether to display the response value.
    show_outline: bool, default: False
        Whether to display the outline of the model.

    Returns
    -------
    fig: `plotly.graph_objects.Figure <https://plotly.com/python-api-reference/generated/plotly.graph_objects.Figure.html>`_
        You can use `fig.show()` to display,
        You can also use `fig.write_html("path/to/file.html")` to save as an HTML file, see
        `Interactive HTML Export in Python <https://plotly.com/python/interactive-html-export/>`_
    """
    ele_type, resp_type, resp_dof = _check_input(ele_type, resp_type, resp_dof)
    model_info_steps, model_update, resp_step = loadODB(odb_tag, resp_type=ele_type)
    plotbase = PlotUnstruResponse(model_info_steps, resp_step, model_update)
    plotbase.refactor_resp_step(
        ele_tags=ele_tags, ele_type=ele_type, resp_type=resp_type, component=resp_dof
    )
    if slides:
        plotbase.plot_slide(
            ele_tags=ele_tags,
            style=style,
            show_values=show_values,
        )
    else:
        plotbase.plot_peak_step(
            ele_tags=ele_tags,
            style=style,
            show_values=show_values,
        )
    return plotbase.update_fig(show_outline)


def plot_unstruct_responses_animation(
    odb_tag: Union[int, str] = 1,
    ele_tags: Union[int, list] = None,
    framerate: int = None,
    ele_type: str = "Shell",
    resp_type: str = None,
    resp_dof: str = None,
    style: str = "surface",
    show_outline: bool = False,
    show_values: bool = False,
):
    """Unstructured element (Shell, Plane, Brick) response animation.

    .. Note::
        The responses at all Gaussian points are averaged.

    Parameters
    ----------
    odb_tag: Union[int, str], default: 1
        Tag of output databases (ODB) to be visualized.
    ele_tags: Union[int, list], default: None
        The tags of truss elements to be visualized. If None, all truss elements are selected.
    ele_type: str, default: "Shell"
        Element type, optional, one of ["Shell", "Plane", "Solid"].
    framerate: int, default: None
        Framerate for the display, i.e., the number of frames per second.
    resp_type: str, default: None
        Response type, which dependents on the element type `ele_type`.

        #. For ``Shell`` elements, one of ["sectionForces", "sectionDeformations"].
            I.e., section forces and deformations at Gaussian integration points (per unit length).
            If None, defaults to "sectionForces".
        #. For ``Plane`` elements, one of ["stresses", "strains"].
            I.e., stresses and strains at Gaussian integration points.
            If None, defaults to "stresses".
        #. For ``Brick`` or ``Solid`` elements, one of ["stresses", "strains"].
            I.e., stresses and strains at Gaussian integration points.
            If None, defaults to "stresses".

    resp_dof: str, default: None
        Dof to be visualized, which dependents on the element type `ele_type`.

        .. Note::
            The `resp_dof` here is consistent with stress-strain (force-deformation),
            and whether it is stress or strain depends on the parameter `resp_type`.

        #. For ``Shell`` elements, one of ["FXX", "FYY", "FXY", "MXX", "MYY", "MXY", "VXZ", "VYZ"].
            If None, defaults to "MXX".
        #. For ``Plane`` elements, one of ["sigma11", "sigma22", "sigma12", "p1", "p2", "sigma_vm", "tau_max"].

            * "sigma11, sigma22, sigma12": Normal stress and shear stress (strain) in the x-y plane.
            * "p1, p2": Principal stresses (strains).
            * "sigma_vm": Von Mises stress.
            * "tau_max": Maximum shear stress (strains).
            * If None, defaults to "sigma_vm".

        #. For ``Brick`` or ``Solid`` elements, one of ["sigma11", "sigma22", "sigma33", "sigma12", "sigma23", "sigma13", "p1", "p2", "p3", "sigma_vm", "tau_max", "sigma_oct", "tau_oct"]

            * "sigma11, sigma22, sigma33": Normal stress (strain) along x, y, z.
            * "sigma12, sigma23, sigma13": Shear stress (strain).
            * "p1, p2, p3": Principal stresses (strains).
            * "sigma_vm": Von Mises stress.
            * "tau_max": Maximum shear stress (strains).
            * "sigma_oct": Octahedral normal stress (strains).
            * "tau_oct": Octahedral shear stress (strains).
            * If None, defaults to "sigma_vm".

    style: str, default: surface
        Visualization mesh style of surfaces and solids.
        One of the following: style='surface' or style='wireframe'
        Defaults to 'surface'. Note that 'wireframe' only shows a wireframe of the outer geometry.
    show_values: bool, default: True
        Whether to display the response value.
    show_outline: bool, default: False
        Whether to display the outline of the model.

    Returns
    -------
    fig: `plotly.graph_objects.Figure <https://plotly.com/python-api-reference/generated/plotly.graph_objects.Figure.html>`_
        You can use `fig.show()` to display,
        You can also use `fig.write_html("path/to/file.html")` to save as an HTML file, see
        `Interactive HTML Export in Python <https://plotly.com/python/interactive-html-export/>`_
    """
    ele_type, resp_type, resp_dof = _check_input(ele_type, resp_type, resp_dof)
    model_info_steps, model_update, resp_step = loadODB(odb_tag, resp_type=ele_type)
    plotbase = PlotUnstruResponse(model_info_steps, resp_step, model_update)
    plotbase.refactor_resp_step(
        ele_tags=ele_tags, ele_type=ele_type, resp_type=resp_type, component=resp_dof
    )
    plotbase.plot_anim(
        ele_tags=ele_tags,
        framerate=framerate,
        style=style,
        show_values=show_values,
    )
    return plotbase.update_fig(show_outline)


def _check_input(ele_type, resp_type, resp_dof):
    if ele_type.lower() == "shell":
        if resp_type is None:
            resp_type = "sectionForces"
        if resp_type.lower() in ["sectionforces", "forces", "sectionforce", "force"]:
            resp_type = "sectionForces"
        elif resp_type.lower() in [
            "sectiondeformations",
            "sectiondeformation",
            "secdeformations",
            "secdeformation",
            "deformations",
            "deformation",
            "defo",
            "secdefo",
        ]:
            resp_type = "sectionDeformations"
        else:
            raise ValueError(
                f"Not supported response type {resp_type}! "
                "Valid options are: sectionForces, sectionDeformations."
            )
        if resp_dof is None:
            resp_dof = "MXX"
        if resp_dof.lower() not in [
            "fxx",
            "fyy",
            "fxy",
            "mxx",
            "myy",
            "mxy",
            "vxz",
            "vyz",
        ]:
            raise ValueError(
                f"Not supported component {resp_dof}! "
                "Valid options are: FXX, FYY, FXY, MXX, MYY, MXY, VXZ, VYZ."
            )
    elif ele_type.lower() == "plane":
        ele_type = "Plane"
        if resp_type is None:
            resp_type = "Stresses"
        if resp_type.lower() in ["stresses", "stress"]:
            if resp_dof is None:
                resp_dof = "sigma_vm"
            if resp_dof.lower() in ["p1", "p2", "sigma_vm", "tau_max"]:
                resp_type = "stressMeasures"
            elif resp_dof.lower() in ["sigma11", "sigma22", "sigma12"]:
                resp_type = "Stresses"
            else:
                raise ValueError(
                    f"Not supported component {resp_dof}! "
                    "Valid options are: sigma11, sigma22, sigma12, p1, p2, sigma_vm, tau_max."
                )
        elif resp_type.lower() in ["strains", "strain"]:
            if resp_dof is None:
                resp_dof = "sigma_vm"
            if resp_dof.lower() in ["p1", "p2", "sigma_vm", "tau_max"]:
                resp_type = "strainMeasures"
            elif resp_dof.lower() in ["sigma11", "sigma22", "sigma12"]:
                resp_type = "Strains"
                resp_dof = resp_dof.replace("sigma", "eps")
            else:
                raise ValueError(
                    f"Not supported component {resp_dof}! "
                    "Valid options are: sigma11, sigma22, sigma12, p1, p2, sigma_vm, tau_max."
                )
        else:
            raise ValueError(
                f"Not supported response type {resp_type}! "
                "Valid options are: Stresses, Strains."
            )

    elif ele_type.lower() in ["brick", "solid"]:
        ele_type = "Brick"
        if resp_type is None:
            resp_type = "Stresses"
        if resp_type.lower() in ["stresses", "stress"]:
            if resp_dof is None:
                resp_dof = "sigma_vm"
            if resp_dof.lower() in ["p1", "p2", "p3", "sigma_vm", "tau_max", "sigma_oct", "tau_oct"]:
                resp_type = "stressMeasures"
            elif resp_dof.lower() in ["sigma11", "sigma22", "sigma33", "sigma12", "sigma23", "sigma13"]:
                resp_type = "Stresses"
            else:
                raise ValueError(
                    f"Not supported component {resp_dof}! "
                    "Valid options are: sigma11, sigma22, sigma33, sigma12, sigma23, sigma13, "
                    "p1, p2, p3, sigma_vm, tau_max, sigma_oct, tau_oct!"
                )
        elif resp_type.lower() in ["strains", "strain"]:
            if resp_dof is None:
                resp_dof = "sigma_vm"
            if resp_dof.lower() in ["p1", "p2", "p3", "sigma_vm", "tau_max", "sigma_oct", "tau_oct"]:
                resp_type = "strainMeasures"
            elif resp_dof.lower() in ["sigma11", "sigma22", "sigma33", "sigma12", "sigma23", "sigma13"]:
                resp_type = "Strains"
                resp_dof = resp_dof.replace("sigma", "eps")
            else:
                raise ValueError(
                    f"Not supported component {resp_dof}! "
                    "Valid options are: sigma11, sigma22, sigma12, p1, p2, sigma_vm, tau_max."
                )
        else:
            raise ValueError(
                f"Not supported response type {resp_type}! "
                "Valid options are: Stresses, Strains."
            )
    else:
        raise ValueError(
            f"Not supported element type {ele_type}! "
            "Valid options are: Shell, Plane, Solid."
        )
    return ele_type, resp_type, resp_dof