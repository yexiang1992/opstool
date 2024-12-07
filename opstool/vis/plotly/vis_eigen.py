from typing import Union, List, Tuple

import numpy as np
import plotly.graph_objs as go
from plotly.subplots import make_subplots


from .plot_utils import (
    PLOT_ARGS,
    _plot_unstru_cmap,
    _plot_lines_cmap,
    _get_line_cells,
    _get_unstru_cells,
    _VTKElementTriangulator,
    _make_lines_plotly,
)
from .vis_model import PlotModelBase
from ...post import load_eigen_data
from ...utils import PKG_NAME, SHAPE_MAP


class PlotEigenBase:
    def __init__(self, model_info, modal_props, eigen_vectors):
        self.nodal_data = model_info["NodalData"]
        self.nodal_tags = self.nodal_data.coords["tags"]
        self.points = self.nodal_data.to_numpy()
        self.ndims = self.nodal_data.attrs["ndims"]
        self.bounds = self.nodal_data.attrs["bounds"]
        self.min_bound_size = self.nodal_data.attrs["minBoundSize"]
        self.max_bound_size = self.nodal_data.attrs["maxBoundSize"]
        self.show_zaxis = False if np.max(self.ndims) <= 2 else True
        # -------------------------------------------------------------
        self.line_data = model_info["AllLineElesData"]
        self.line_cells, self.line_tags = _get_line_cells(self.line_data)
        # -------------------------------------------------------------
        self.unstru_data = model_info["UnstructuralData"]
        self.unstru_tags, self.unstru_cell_types, self.unstru_cells = _get_unstru_cells(
            self.unstru_data
        )
        # --------------------------------------------------
        self.ModalProps = modal_props
        self.EigenVectors = eigen_vectors.to_numpy()[..., :3]
        self.plot_model_base = PlotModelBase(model_info, dict())

        # plotly
        self.pargs = PLOT_ARGS
        self.FIGURE = go.Figure()

    @staticmethod
    def _set_txt_props(txt, color="blue", weight="bold"):
        return f'<span style="color:{color}; font-weight:{weight}">{txt}</span>'

    @staticmethod
    def _get_plotly_unstru_data(points, unstru_cell_types, unstru_cells, scalars):
        grid = _VTKElementTriangulator(points, scalars=scalars)
        for cell_type, cell in zip(unstru_cell_types, unstru_cells):
            grid.add_cell(cell_type, cell)
        return grid.get_results()

    @staticmethod
    def _get_plotly_line_data(points, line_cells, scalars):
        return _make_lines_plotly(points, line_cells, scalars=scalars)

    def _make_eigen_txt(self, step):
        fi = self.ModalProps.loc[:, "eigenFrequency"][step]
        txt = f'<span style="font-weight:bold; font-size:{self.pargs.title_font_size}px">Mode {step + 1}</span>'
        # txt = f"<b>Mode {step + 1}</b>"
        period_txt = self._set_txt_props(f"{1/fi:.6f}; ", color="blue")
        txt += f"<br><b>Period (s):</b> {period_txt}"
        fi_txt = self._set_txt_props(f"{fi:.6f};", color="blue")
        txt += (
            f"<b>Frequency (Hz):</b> {fi_txt}"
        )
        if not self.show_zaxis:
            txt += "<br><b>Modal participation mass ratios (%)</b><br>"
            mx = self.ModalProps.loc[:, "partiMassRatiosMX"][step]
            my = self.ModalProps.loc[:, "partiMassRatiosMY"][step]
            rmz = self.ModalProps.loc[:, "partiMassRatiosRMZ"][step]
            txt += self._set_txt_props(f"{mx:7.3f} {my:7.3f} {rmz:7.3f}", color="blue")
            txt += "<br><b>Cumulative modal participation mass ratios (%)</b><br>"
            mx = self.ModalProps.loc[:, "partiMassRatiosCumuMX"][step]
            my = self.ModalProps.loc[:, "partiMassRatiosCumuMY"][step]
            rmz = self.ModalProps.loc[:, "partiMassRatiosCumuRMZ"][step]
            txt += self._set_txt_props(f"{mx:7.3f} {my:7.3f} {rmz:7.3f}", color="blue")
            txt += "<br><b>{:>7} {:>7} {:>7}</b>".format("X", "Y", "RZ")
        else:
            txt += "<br><b>Modal participation mass ratios (%)</b><br>"
            mx = self.ModalProps.loc[:, "partiMassRatiosMX"][step]
            my = self.ModalProps.loc[:, "partiMassRatiosMY"][step]
            mz = self.ModalProps.loc[:, "partiMassRatiosMZ"][step]
            rmx = self.ModalProps.loc[:, "partiMassRatiosRMX"][step]
            rmy = self.ModalProps.loc[:, "partiMassRatiosRMY"][step]
            rmz = self.ModalProps.loc[:, "partiMassRatiosRMZ"][step]
            txt += self._set_txt_props(
                f"{mx:7.3f} {my:7.3f} {mz:7.3f} {rmx:7.3f} {rmy:7.3f} {rmz:7.3f}", color="blue"
            )
            txt += "<br><b>Cumulative modal participation mass ratios (%)</b><br>"
            mx = self.ModalProps.loc[:, "partiMassRatiosCumuMX"][step]
            my = self.ModalProps.loc[:, "partiMassRatiosCumuMY"][step]
            mz = self.ModalProps.loc[:, "partiMassRatiosCumuMZ"][step]
            rmx = self.ModalProps.loc[:, "partiMassRatiosCumuRMX"][step]
            rmy = self.ModalProps.loc[:, "partiMassRatiosCumuRMY"][step]
            rmz = self.ModalProps.loc[:, "partiMassRatiosCumuRMZ"][step]
            txt += self._set_txt_props(
                f"{mx:7.3f} {my:7.3f} {mz:7.3f} {rmx:7.3f} {rmy:7.3f} {rmz:7.3f}", color="blue"
            )
            txt += (
                f"<br><b>{'X':>7} {'Y':>7} {'Z':>7} {'RX':>7} {'RY':>7} {'RZ':>7}</b>"
            )
            # f'<span style="color:blue; font-weight:bold;">{"X":>7} {"Y":>7} {"Z":>7} {"RX":>7} {"RY":>7} {"RZ":>7}</span>'
        return txt

    def _create_mesh(
        self,
        plotter: list,
        idx,
        coloraxis,
        alpha=1.0,
        style="surface",
        show_origin=False,
        show_bc: bool = True,
        bc_scale: float = 1.0,
        show_mp_constraint: bool = True,
    ):
        step = int(round(idx)) - 1
        eigen_vec = self.EigenVectors[step]
        value_ = np.max(np.sqrt(np.sum(eigen_vec**2, axis=1)))
        alpha_ = self.max_bound_size * self.pargs.scale_factor / value_
        alpha_ = alpha_ * alpha if alpha else alpha_
        eigen_points = self.points + eigen_vec * alpha_
        scalars = np.sqrt(np.sum(eigen_vec**2, axis=1))

        if len(self.unstru_data) > 0:
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
                eigen_points, self.unstru_cell_types, self.unstru_cells, scalars
            )
            _plot_unstru_cmap(
                plotter,
                face_points,
                veci=veci,
                vecj=vecj,
                veck=veck,
                scalars=face_scalars,
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
        if len(self.line_data) > 0:
            line_points, line_mid_points, line_scalars = self._get_plotly_line_data(
                eigen_points, self.line_cells, scalars
            )
            _plot_lines_cmap(
                plotter,
                line_points,
                scalars=line_scalars,
                coloraxis=coloraxis,
                width=self.pargs.line_width,
            )
        if show_bc:
            self.plot_model_base.plot_bc(plotter, bc_scale)
        if show_mp_constraint:
            self.plot_model_base.plot_mp_constraint(
                plotter,
                points_new=eigen_points,
            )
        if show_origin:
            self.plot_model_base.plot_model_one_color(
                plotter,
                color="gray",
                style="wireframe",
            )

    def subplots(self, modei, modej, show_outline, **kargs):
        if modej - modei + 1 > 64:
            raise ValueError("When subplots True, mode_tag range must < 64 for clarify")
        shape = SHAPE_MAP[modej - modei + 1]
        specs = [[{"is_3d": True} for _ in range(shape[1])] for _ in range(shape[0])]
        subplot_titles = []
        for i, idx in enumerate(range(modei, modej + 1)):
            f = self.ModalProps.loc[:, "eigenFrequency"]
            mode = self._set_txt_props(f"{idx}", color="#8eab12")
            period = 1 / f[idx - 1]
            if period < 1e-3:
                t = self._set_txt_props(f"{period:.3E}")
            else:
                t = self._set_txt_props(f"{period:.3f}")
            txt = f"Mode <b>{mode}</b>: T = <b>{t}</b> s"
            subplot_titles.append(txt)
        self.FIGURE = make_subplots(
            rows=shape[0],
            cols=shape[1],
            specs=specs,
            figure=self.FIGURE,
            print_grid=False,
            subplot_titles=subplot_titles,
            horizontal_spacing=0.07 / shape[1],
            vertical_spacing=0.1 / shape[0],
            column_widths=[1] * shape[1],
            row_heights=[1] * shape[0],
        )
        for i, idx in enumerate(range(modei, modej + 1)):
            idxi = int(np.ceil((i + 1) / shape[1]) - 1)
            idxj = int(i - idxi * shape[1])
            plotter = []
            self._create_mesh(plotter, idx, coloraxis=f"coloraxis{i + 1}", **kargs)
            self.FIGURE.add_traces(plotter, rows=idxi + 1, cols=idxj + 1)
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
        scenes = dict()
        coloraxiss = dict()
        if show_outline:
            off_axis = {"showgrid": True, "zeroline": True, "visible": True}
        else:
            off_axis = {"showgrid": False, "zeroline": False, "visible": False}
        for k in range(shape[0] * shape[1]):
            coloraxiss[f"coloraxis{k + 1}"] = dict(
                showscale=False, colorscale=self.pargs.cmap
            )
            if k >= 1:
                if not self.show_zaxis:
                    scenes[f"scene{k + 1}"] = dict(
                        camera=dict(eye=eye, projection=dict(type="orthographic")),
                        xaxis=off_axis,
                        yaxis=off_axis,
                        zaxis=off_axis,
                    )
                else:
                    scenes[f"scene{k + 1}"] = dict(
                        aspectratio=dict(x=1, y=1, z=1),
                        aspectmode="data",
                        camera=dict(eye=eye, projection=dict(type="orthographic")),
                        xaxis=off_axis,
                        yaxis=off_axis,
                        zaxis=off_axis,
                    )
        title = dict(
            font=dict(family="courier", color="black", size=self.pargs.title_font_size),
            text=f"<b>{PKG_NAME} :: Eigen 3D Viewer</b>",
        )
        self.FIGURE.update_layout(
            title=title,
            font=dict(family=self.pargs.font_family),
            template=self.pargs.theme,
            autosize=True,
            showlegend=False,
            coloraxis=dict(showscale=False, colorscale=self.pargs.cmap),
            scene=scene,
            **scenes,
            **coloraxiss,
        )

        return self.FIGURE

    def plot_slides(self, modei, modej, **kargs):
        n_data = None
        for i, idx in enumerate(range(modei, modej + 1)):
            plotter = []
            self._create_mesh(plotter, idx, coloraxis=f"coloraxis{i + 1}", **kargs)
            self.FIGURE.add_traces(plotter)
            if i == 0:
                n_data = len(self.FIGURE.data)
        for i in range(n_data, len(self.FIGURE.data)):
            self.FIGURE.data[i].visible = False
        # Create and add slider
        steps = []
        for i, idx in enumerate(range(modei, modej + 1)):
            # txt = "Mode {}: T = {:.3f} s".format(idx, 1 / f[idx - 1])
            txt = self._make_eigen_txt(idx - 1)
            txt = dict(
                font=dict(family="courier", color="black", size=self.pargs.font_size),
                text=txt,
            )
            step = dict(
                method="update",
                args=[
                    {"visible": [False] * len(self.FIGURE.data)},
                    {"title": txt},
                ],  # layout attribute
                label=str(idx),
            )
            step["args"][0]["visible"][n_data * i : n_data * (i + 1)] = [True] * n_data
            # Toggle i'th trace to "visible"
            steps.append(step)
        sliders = [
            dict(
                active=modej - modei + 1,
                currentvalue={"prefix": "Mode: "},
                pad={"t": 50},
                steps=steps,
            )
        ]
        coloraxiss = {}
        for i in range(modej - modei + 1):
            coloraxiss[f"coloraxis{i + 1}"] = dict(
                colorscale=self.pargs.cmap,
                # cmin=cmins[i],
                # cmax=cmaxs[i],
                showscale=False,
                colorbar=dict(tickfont=dict(size=15)),
            )
        title = dict(
            font=dict(family="courier", color="black", size=self.pargs.title_font_size),
            text=f"<b>{PKG_NAME} :: Eigen 3D Viewer</b>",
        )
        self.FIGURE.update_layout(
            title=title,
            sliders=sliders,
            **coloraxiss,
        )

        return self.FIGURE

    def plot_anim(
        self,
        mode_tag: int = 1,
        n_cycle: int = 5,
        framerate: int = 3,
        alpha: float = 1.0,
        **kargs,
    ):
        alphas = [0.0] + [alpha, -alpha] * n_cycle
        nb_frames = len(alphas)
        times = int(nb_frames / framerate)
        # -----------------------------------------------------------------------------
        # start plot
        frames = []
        for k, alpha in enumerate(alphas):
            plotter = []
            self._create_mesh(
                plotter, mode_tag, alpha=alpha, coloraxis="coloraxis", **kargs
            )
            frames.append(go.Frame(data=plotter, name="step:" + str(k + 1)))
        self.FIGURE = go.Figure(frames=frames)
        # Add data to be displayed before animation starts
        plotter0 = []
        self._create_mesh(
            plotter0, mode_tag, alpha=alpha, coloraxis="coloraxis", **kargs
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
                        "label": "step:" + str(k + 1),
                        "method": "animate",
                    }
                    for k, f in enumerate(self.FIGURE.frames)
                ],
            }
        ]
        # Layout
        f = self.ModalProps.loc[:, "eigenFrequency"][mode_tag - 1]
        txt = "<br> Mode <b>{}</b>: T = <b>{:.3f}</b> s".format(mode_tag, 1 / f)
        self.FIGURE.update_layout(
            title=dict(
                font=dict(
                    family="courier", color="black", size=self.pargs.title_font_size
                ),
                text=f"<b>{PKG_NAME} :: Eigen 3D Viewer</b>" + txt,
            ),
            coloraxis=dict(
                colorscale=self.pargs.cmap,
                showscale=False,
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

    def plot_props_table(self, modei, modej):
        df = self.ModalProps.to_pandas()[modei - 1 : modej]
        df = df.T
        fig = go.Figure(
            data=[
                go.Table(
                    header=dict(values=["modeTags"] + list(df.columns)),
                    cells=dict(
                        values=[df.index] + [df[col].tolist() for col in df.columns],
                        format=[""] + [".3E"] * len(df.columns),
                    ),
                )
            ]
        )
        return fig

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


def plot_eigen(
    mode_tags: Union[List, Tuple, int],
    odb_tag: Union[int, str] = None,
    subplots: bool = False,
    scale: float = 1.0,
    show_outline: bool = False,
    show_origin: bool = False,
    style: str = "surface",
    show_bc: bool = True,
    bc_scale: float = 1.0,
    show_mp_constraint: bool = True,
    solver: str = "-genBandArpack",
):
    """Modal visualization.

    Parameters
    ----------
    mode_tags: Union[List, Tuple]
        The modal range to visualize, [mode i, mode j].
    odb_tag: Union[int, str], default: None
        Tag of output databases (ODB) to be visualized.
        If None, the data will be saved automatically.
    subplots: bool, default: False
        If True, multiple subplots are used to present mode i to mode j.
        Otherwise, they are presented as slides.
    scale: float, default: 1.0
        Zoom the presentation size of the mode shapes.
    show_outline: bool, default: False
        Whether to display the outline of the model.
    show_origin: bool, default: False
        Whether to show the undeformed shape.
    style: str, default: surface
        Visualization mesh style of surfaces and solids.
        One of the following: style='surface' or style='wireframe'
        Defaults to 'surface'. Note that 'wireframe' only shows a wireframe of the outer geometry.
    show_bc: bool, default: True
        Whether to display boundary supports.
    bc_scale: float, default: 1.0
        Scale the size of boundary support display.
    show_mp_constraint: bool, default: True
        Whether to show multipoint (MP) constraint.
    solver : str, optional,
       OpenSees' eigenvalue analysis solver, by default "-genBandArpack".

    Returns
    -------
    fig: `plotly.graph_objects.Figure <https://plotly.com/python-api-reference/generated/plotly.graph_objects.Figure.html>`_
        You can use `fig.show()` to display,
        You can also use `fig.write_html("path/to/file.html")` to save as an HTML file, see
        `Interactive HTML Export in Python <https://plotly.com/python/interactive-html-export/>`_
    """
    if isinstance(mode_tags, int):
        mode_tags = [1, mode_tags]
    resave = True if odb_tag is None else False
    modalProps, eigenvectors, MODEL_INFO = load_eigen_data(
        odb_tag=odb_tag, mode_tag=mode_tags[-1], solver=solver, resave=resave
    )
    modei, modej = int(mode_tags[0]), int(mode_tags[1])
    plotbase = PlotEigenBase(MODEL_INFO, modalProps, eigenvectors)
    if subplots:
        plotbase.subplots(
            modei,
            modej,
            show_outline=show_outline,
            # link_views=link_views,
            alpha=scale,
            style=style,
            show_origin=show_origin,
            show_bc=show_bc,
            bc_scale=bc_scale,
            show_mp_constraint=show_mp_constraint,
        )
    else:
        plotbase.plot_slides(
            modei,
            modej,
            alpha=scale,
            style=style,
            show_origin=show_origin,
            show_bc=show_bc,
            bc_scale=bc_scale,
            show_mp_constraint=show_mp_constraint,
        )

    return plotbase.update_fig(show_outline=show_outline)


def plot_eigen_animation(
    mode_tag: int,
    odb_tag: Union[int, str] = None,
    n_cycle: int = 5,
    framerate: int = 3,
    scale: float = 1.0,
    solver: str = "-genBandArpack",
    show_outline: bool = False,
    show_origin: bool = False,
    style: str = "surface",
    show_bc: bool = True,
    bc_scale: float = 1.0,
    show_mp_constraint: bool = True,
):
    """Modal animation visualization.

    Parameters
    ----------
    mode_tag: int
        The mode tag to display.
    odb_tag: Union[int, str], default: None
        Tag of output databases (ODB) to be visualized.
        If None, the data will be saved automatically.
    n_cycle: int, default: five
        Number of cycles for the display.
    framerate: int, default: three
        Framerate for the display, i.e., the number of frames per second.
    scale: float, default: 1.0
        Zoom the presentation size of the mode shapes.
    solver : str, optional,
       OpenSees' eigenvalue analysis solver, by default "-genBandArpack".
    show_outline: bool, default: False
        Whether to display the outline of the model.
    show_origin: bool, default: False
        Whether to show the undeformed shape.
    style: str, default: surface
        Visualization mesh style of surfaces and solids.
        One of the following: style='surface' or style='wireframe'
        Defaults to 'surface'. Note that 'wireframe' only shows a wireframe of the outer geometry.
    show_bc: bool, default: True
        Whether to display boundary supports.
    bc_scale: float, default: 1.0
        Scale the size of boundary support display.
    show_mp_constraint: bool, default: True
        Whether to show multipoint (MP) constraint.

    Returns
    -------
    fig: `plotly.graph_objects.Figure <https://plotly.com/python-api-reference/generated/plotly.graph_objects.Figure.html>`_
        You can use `fig.show()` to display,
        You can also use `fig.write_html("path/to/file.html")` to save as an HTML file, see
        `Interactive HTML Export in Python <https://plotly.com/python/interactive-html-export/>`_
    """
    resave = True if odb_tag is None else False
    modalProps, eigenvectors, MODEL_INFO = load_eigen_data(
        odb_tag=odb_tag, mode_tag=mode_tag, solver=solver, resave=resave
    )
    plotbase = PlotEigenBase(MODEL_INFO, modalProps, eigenvectors)
    plotbase.plot_anim(
        mode_tag,
        n_cycle=n_cycle,
        framerate=framerate,
        alpha=scale,
        style=style,
        show_origin=show_origin,
        show_bc=show_bc,
        bc_scale=bc_scale,
        show_mp_constraint=show_mp_constraint,
    )
    return plotbase.update_fig(show_outline=show_outline)


def plot_eigen_table(
    mode_tags: Union[List, Tuple, int],
    odb_tag: Union[int, str] = 1,
    solver: str = "-genBandArpack",
):
    """Plot Modal Properties Table.

    Parameters
    ----------
    mode_tags: Union[List, Tuple]
        The modal range to visualize, [mode i, mode j].
    odb_tag: Union[int, str], default: None
        Tag of output databases (ODB) to be visualized.
    solver : str, optional,
       OpenSees' eigenvalue analysis solver, by default "-genBandArpack".

    Returns
    -------
    None
    """
    resave = True if odb_tag is None else False
    if isinstance(mode_tags, int):
        mode_tags = [1, mode_tags]
    modalProps, eigenvectors, MODEL_INFO = load_eigen_data(
        odb_tag=odb_tag, mode_tag=mode_tags[-1], solver=solver, resave=resave
    )
    modei, modej = int(mode_tags[0]), int(mode_tags[1])
    plotbase = PlotEigenBase(MODEL_INFO, modalProps, eigenvectors)
    fig = plotbase.plot_props_table(modei, modej)
    return fig
