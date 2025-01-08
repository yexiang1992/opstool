from functools import partial
from typing import Union, List, Tuple

import numpy as np
import pyvista as pv

from .plot_utils import (
    PLOT_ARGS,
    _plot_all_mesh_cmap,
    _get_line_cells,
    _get_unstru_cells,
)
from .vis_model import PlotModelBase
from ...post import load_eigen_data
from ...utils import CONSTANTS
PKG_NAME = CONSTANTS.get_pkg_name()
SHAPE_MAP = CONSTANTS.get_shape_map()


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
        self.pargs = PLOT_ARGS
        self.ModalProps = modal_props
        self.EigenVectors = eigen_vectors.to_numpy()[..., :3]
        self.plot_model_base = PlotModelBase(model_info, dict())
        pv.set_plot_theme(PLOT_ARGS.theme)

    def _make_eigen_txt(self, step):
        fi = self.ModalProps.loc[:, "eigenFrequency"][step]
        txt = f"Mode {step + 1}\nperiod: {1 / fi:.6f} s; freq: {fi:.6f} Hz\n"
        if not self.show_zaxis:
            txt += "modal participation mass ratios (%)\n"
            mx = self.ModalProps.loc[:, "partiMassRatiosMX"][step]
            my = self.ModalProps.loc[:, "partiMassRatiosMY"][step]
            rmz = self.ModalProps.loc[:, "partiMassRatiosRMZ"][step]
            txt += f"{mx:7.3f} {my:7.3f} {rmz:7.3f}\n"
            txt += "cumulative modal participation mass ratios (%)\n"
            mx = self.ModalProps.loc[:, "partiMassRatiosCumuMX"][step]
            my = self.ModalProps.loc[:, "partiMassRatiosCumuMY"][step]
            rmz = self.ModalProps.loc[:, "partiMassRatiosCumuRMZ"][step]
            txt += f"{mx:7.3f} {my:7.3f} {rmz:7.3f}\n"
            txt += "{:>7} {:>7} {:>7}\n".format("X", "Y", "RZ")
        else:
            txt += "modal participation mass ratios (%)\n"
            mx = self.ModalProps.loc[:, "partiMassRatiosMX"][step]
            my = self.ModalProps.loc[:, "partiMassRatiosMY"][step]
            mz = self.ModalProps.loc[:, "partiMassRatiosMZ"][step]
            rmx = self.ModalProps.loc[:, "partiMassRatiosRMX"][step]
            rmy = self.ModalProps.loc[:, "partiMassRatiosRMY"][step]
            rmz = self.ModalProps.loc[:, "partiMassRatiosRMZ"][step]
            txt += f"{mx:7.3f} {my:7.3f} {mz:7.3f} {rmx:7.3f} {rmy:7.3f} {rmz:7.3f}\n"
            txt += "cumulative modal participation mass ratios (%)\n"
            mx = self.ModalProps.loc[:, "partiMassRatiosCumuMX"][step]
            my = self.ModalProps.loc[:, "partiMassRatiosCumuMY"][step]
            mz = self.ModalProps.loc[:, "partiMassRatiosCumuMZ"][step]
            rmx = self.ModalProps.loc[:, "partiMassRatiosCumuRMX"][step]
            rmy = self.ModalProps.loc[:, "partiMassRatiosCumuRMY"][step]
            rmz = self.ModalProps.loc[:, "partiMassRatiosCumuRMZ"][step]
            txt += f"{mx:7.3f} {my:7.3f} {mz:7.3f} {rmx:7.3f} {rmy:7.3f} {rmz:7.3f}\n"
            txt += "{:>7} {:>7} {:>7} {:>7} {:>7} {:>7}\n".format(
                "X", "Y", "Z", "RX", "RY", "RZ"
            )
        return txt

    def _create_mesh(
        self,
        plotter,
        idx,
        idxi=None,
        idxj=None,
        alpha=1.0,
        style="surface",
        show_outline=False,
        show_origin=False,
        show_bc: bool = True,
        bc_scale: float = 1.0,
        show_mp_constraint: bool = True,
    ):
        if idxi is not None and idxj is not None:
            plotter.subplot(idxi, idxj)
            subplots = True
        else:
            plotter.clear_actors()
            subplots = False
        step = int(round(idx)) - 1
        eigen_vec = self.EigenVectors[step]
        value_ = np.max(np.sqrt(np.sum(eigen_vec**2, axis=1)))
        alpha_ = self.max_bound_size * self.pargs.scale_factor / value_
        alpha_ = alpha_ * alpha if alpha else alpha_
        eigen_points = self.points + eigen_vec * alpha_
        scalars = np.sqrt(np.sum(eigen_vec**2, axis=1))
        point_plot, line_plot, solid_plot = _plot_all_mesh_cmap(
            plotter,
            eigen_points,
            self.line_cells,
            self.unstru_cells,
            self.unstru_cell_types,
            scalars=scalars,
            cmap=self.pargs.cmap,
            clim=None,
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
            pos_origin=self.points,
        )
        if not subplots:
            txt = self._make_eigen_txt(step)
            plotter.add_text(
                txt,
                position="lower_right",
                font_size=self.pargs.font_size,
                font="courier",
            )
        else:
            period = 1 / self.ModalProps.loc[:, "eigenFrequency"][step]
            if period < 1e-3:
                txt = f"Mode {step + 1}  T = {period:.3E} s"
            else:
                txt = f"Mode {step + 1}  T = {period:.3f} s"
            plotter.add_text(
                txt,
                position="upper_left",
                font_size=self.pargs.title_font_size,
                font="courier",
            )
            # txt = self._make_eigen_txt(step)
            # plotter.add_text(txt, position="lower_right", font_size=label_size, font="courier")
        if show_bc:
            self.plot_model_base.plot_bc(plotter, bc_scale)
        if show_mp_constraint:
            mp_plot = self.plot_model_base.plot_mp_constraint(
                plotter,
                points_new=eigen_points,
            )
        else:
            mp_plot = None
        if show_outline:
            plotter.show_bounds(
                grid=False,
                location="outer",
                bounds=self.bounds,
                show_zaxis=self.show_zaxis,
            )
        plotter.add_axes(interactive=True)
        return point_plot, line_plot, solid_plot, alpha_, mp_plot

    def subplots(self, plotter, modei, modej, link_views=True, **kargs):
        if modej - modei + 1 > 64:
            raise ValueError("When subplots True, mode_tag range must < 64 for clarify")
        shape = SHAPE_MAP[modej - modei + 1]
        for i, idx in enumerate(range(modei, modej + 1)):
            idxi = int(np.ceil((i + 1) / shape[1]) - 1)
            idxj = int(i - idxi * shape[1])
            self._create_mesh(plotter, idx, idxi, idxj, **kargs)
        if link_views:
            plotter.link_views()

    def plot_slides(self, plotter, modei, modej, **kargs):
        plotter.add_slider_widget(
            partial(self._create_mesh, plotter, **kargs),
            [modei, modej],
            value=modei,
            pointa=(0.01, 0.925),
            pointb=(0.45, 0.925),
            title="Mode",
            title_opacity=1,
            # title_color="black",
            fmt="%.0f",
            title_height=0.03,
            slider_width=0.03,
            tube_width=0.008,
        )

    def plot_anim(
        self,
        plotter,
        mode_tag: int = 1,
        n_cycle: int = 5,
        framerate: int = 3,
        savefig: str = "EigenAnimation.gif",
        **kargs,
    ):
        point_plot, line_plot, solid_plot, alpha_, mp_plot = self._create_mesh(
            plotter, mode_tag, **kargs
        )
        # animation
        if savefig.endswith(".gif"):
            plotter.open_gif(savefig, fps=framerate, palettesize=64)
        else:
            plotter.open_movie(savefig, framerate=framerate, quality=7)
        eigen_vec = self.EigenVectors[mode_tag - 1]
        eigen_points = self.points + eigen_vec * alpha_
        anti_eigen_points = self.points - eigen_vec * alpha_
        plt_points = [anti_eigen_points, self.points, eigen_points]
        index = [2, 0] * n_cycle
        plotter.write_frame()  # write initial data
        for idx in index:
            points = plt_points[idx]
            xyz = (self.points - points) / alpha_
            xyz_eigen = np.sqrt(np.sum(xyz**2, axis=1))
            if point_plot:
                point_plot["scalars"] = xyz_eigen
                point_plot.points = points
            if line_plot:
                line_plot["scalars"] = xyz_eigen
                line_plot.points = points
            if solid_plot:
                solid_plot["scalars"] = xyz_eigen
                solid_plot.points = points
            if mp_plot:
                mp_plot.points = points
            plotter.update_scalar_bar_range(
                clim=[np.min(xyz_eigen), np.max(xyz_eigen)], name=None
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


def plot_eigen(
    mode_tags: Union[List, Tuple, int],
    odb_tag: Union[int, str] = None,
    subplots: bool = False,
    link_views: bool = True,
    scale: float = 1.0,
    show_outline: bool = False,
    show_origin: bool = False,
    style: str = "surface",
    cpos: str = "iso",
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
        If None, data will be saved automatically.
    subplots: bool, default: False
        If True, multiple subplots are used to present mode i to mode j.
        Otherwise, they are presented as slides.
    link_views: bool, default: True
        Link the views' cameras when subplots=True.
    scale: float, default: 1.0
        Zoom the presentation size of the mode shapes.
    show_outline: bool, default: False
        Whether to display the outline of the model.
    show_origin: bool, default: False
        Whether to show the undeformed shape.
    style: str, default: surface
        Visualization the mesh style of surfaces and solids.
        One of the following: style='surface', style='wireframe', style='points', style='points_gaussian'.
        Defaults to 'surface'. Note that 'wireframe' only shows a wireframe of the outer geometry.
    cpos: str, default: iso
        Model display perspective, optional: "iso", "xy", "yx", "xz", "zx", "yz", "zy".
        If 3d, defaults to "iso". If 2d, defaults to "xy".
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
    Plotting object of PyVista to display vtk meshes or numpy arrays.
    See `pyvista.Plotter <https://docs.pyvista.org/api/plotting/_autosummary/pyvista.plotter>`_.

    You can use
    `Plotter.show <https://docs.pyvista.org/api/plotting/_autosummary/pyvista.plotter.show#pyvista.Plotter.show>`_.
    to display the plotting window.

    You can also use
    `Plotter.export_html <https://docs.pyvista.org/api/plotting/_autosummary/pyvista.plotter.export_html#pyvista.Plotter.export_html>`_.
    to export this plotter as an interactive scene to an HTML file.
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
        shape = SHAPE_MAP[modej - modei + 1]
        plotter = pv.Plotter(
            notebook=PLOT_ARGS.notebook,
            shape=shape,
            line_smoothing=PLOT_ARGS.line_smoothing,
            polygon_smoothing=PLOT_ARGS.polygon_smoothing,
            off_screen=PLOT_ARGS.off_screen,
        )
        plotbase.subplots(
            plotter,
            modei,
            modej,
            link_views=link_views,
            alpha=scale,
            style=style,
            show_outline=show_outline,
            show_origin=show_origin,
            show_bc=show_bc,
            bc_scale=bc_scale,
            show_mp_constraint=show_mp_constraint,
        )
    else:
        plotter = pv.Plotter(
            notebook=PLOT_ARGS.notebook,
            line_smoothing=PLOT_ARGS.line_smoothing,
            polygon_smoothing=PLOT_ARGS.polygon_smoothing,
        )
        plotbase.plot_slides(
            plotter,
            modei,
            modej,
            alpha=scale,
            style=style,
            show_outline=show_outline,
            show_origin=show_origin,
            show_bc=show_bc,
            bc_scale=bc_scale,
            show_mp_constraint=show_mp_constraint,
        )
    if PLOT_ARGS.anti_aliasing:
        plotter.enable_anti_aliasing(PLOT_ARGS.anti_aliasing)
    return plotbase.update(plotter, cpos)


def plot_eigen_animation(
    mode_tag: int,
    odb_tag: Union[int, str] = None,
    n_cycle: int = 5,
    framerate: int = 3,
    savefig: str = "EigenAnimation.gif",
    off_screen: bool = True,
    cpos: str = "iso",
    solver: str = "-genBandArpack",
    **kargs,
):
    """Modal animation visualization.

    Parameters
    ----------
    mode_tag: int
        The mode tag to display.
    odb_tag: Union[int, str], default: None
        Tag of output databases (ODB) to be visualized.
        If None, data will be saved automatically.
    n_cycle: int, default: five
        Number of cycles for the display.
    framerate: int, default: three
        Framerate for the display, i.e., the number of frames per second.
    savefig: str, default: EigenAnimation.gif
        Path to save the animation. The suffix can be ``.gif`` or ``.mp4``.
    off_screen: bool, default: True
        Whether to display the plotting window.
        If True, the plotting window will not be displayed.
    cpos: str, default: iso
        Model display perspective, optional: "iso", "xy", "yx", "xz", "zx", "yz", "zy".
        If 3d, defaults to "iso". If 2d, defaults to "xy".
    solver : str, optional,
        OpenSees' eigenvalue analysis solver, by default "-genBandArpack".
    kargs: dict, optional parameters,
        see ``plot_eigen``.

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
    resave = True if odb_tag is None else False
    modalProps, eigenvectors, MODEL_INFO = load_eigen_data(
        odb_tag=odb_tag, mode_tag=mode_tag, solver=solver, resave=resave
    )
    plotbase = PlotEigenBase(MODEL_INFO, modalProps, eigenvectors)
    plotter = pv.Plotter(
        notebook=PLOT_ARGS.notebook,
        line_smoothing=PLOT_ARGS.line_smoothing,
        polygon_smoothing=PLOT_ARGS.polygon_smoothing,
        off_screen=off_screen,
    )
    plotbase.plot_anim(
        plotter,
        mode_tag,
        n_cycle=n_cycle,
        framerate=framerate,
        savefig=savefig,
        **kargs,
    )
    if PLOT_ARGS.anti_aliasing:
        plotter.enable_anti_aliasing(PLOT_ARGS.anti_aliasing)
    print(f"Animation saved to {savefig}!")
    return plotbase.update(plotter, cpos)
