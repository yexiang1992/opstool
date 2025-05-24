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
    _plot_unstru_cmap,
)


class PlotUnstruResponse(PlotResponseBase):
    def __init__(self, model_info_steps, resp_step, model_update):
        super().__init__(model_info_steps, resp_step, model_update)
        self.ele_type = "Shell"

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

    def _get_unstru_data(self, step):
        if self.ele_type.lower() == "shell":
            return self._get_model_data("ShellData", step)
        elif self.ele_type.lower() == "plane":
            return self._get_model_data("PlaneData", step)
        elif self.ele_type.lower() in ["brick", "solid"]:
            return self._get_model_data("BrickData", step)
        else:
            raise ValueError(f"Invalid element type {self.ele_type}! Valid options are: Shell, Plane, Brick.")  # noqa: TRY003

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
                raise ValueError("Invalid argument, one of [absMax, absMin, Max, Min]")  # noqa: TRY003
        else:
            step = int(idx)
        cmin, cmax = self._get_resp_clim()
        return step, (cmin, cmax)

    def _get_resp_clim(self):
        maxv = [np.max(data) for data in self.resp_step]
        minv = [np.min(data) for data in self.resp_step]
        cmin, cmax = np.min(minv), np.max(maxv)
        return cmin, cmax

    def _make_title(self, scalars, step, time):
        if self.resp_type.lower() == "stressmeasures":
            resp_type = "Stress Measures"
        elif self.resp_type.lower() == "strainmeasures":
            resp_type = "Strain Measures"
        else:
            resp_type = self.resp_type.capitalize()
        info = {
            "title": self.ele_type.capitalize(),
            "resp_type": resp_type,
            "dof": self.component.capitalize(),
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

    def _get_mesh_data(self, step, ele_tags):
        tags, pos, cells, cell_types = self._make_unstru_info(ele_tags, step)
        scalars = self.resp_step[step].to_numpy()
        return pos, cells, cell_types, scalars

    def _create_mesh(self, plotter, value, ele_tags=None, plot_all_mesh=True, clim=None, style="surface", cpos="iso"):
        step = round(value)
        pos, cells, cell_types, scalars = self._get_mesh_data(value, ele_tags)
        #  ---------------------------------
        plotter.clear_actors()  # !!!!!!
        if plot_all_mesh:
            self._plot_all_mesh(plotter, color="gray", step=step)
        resp_plot = _plot_unstru_cmap(
            plotter,
            pos=pos,
            cells=cells,
            cell_types=cell_types,
            scalars=scalars,
            cmap=self.pargs.cmap,
            clim=clim,
            show_scalar_bar=False,
            show_edges=self.pargs.show_mesh_edges,
            edge_color=self.pargs.mesh_edge_color,
            edge_width=self.pargs.mesh_edge_width,
            opacity=self.pargs.mesh_opacity,
            style=style,
        )

        title = self._make_title(scalars, step, self.time[step])
        scalar_bar = plotter.add_scalar_bar(title=title, **self.pargs.scalar_bar_kargs)
        if scalar_bar:
            # scalar_bar.SetTitle(title)
            title_prop = scalar_bar.GetTitleTextProperty()
            title_prop.SetJustificationToRight()
            title_prop.BoldOn()

        self.update(plotter, cpos)
        return resp_plot, scalar_bar

    def _update_mesh(self, step, ele_tags, resp_plot, scalar_bar):
        step = round(step)
        pos, cells, cell_types, scalars = self._get_mesh_data(step, ele_tags)

        if resp_plot:
            resp_plot["scalars"] = scalars

        if scalar_bar:
            title = self._make_title(scalars, step, self.time[step])
            scalar_bar.SetTitle(title)

    def plot_slide(self, plotter, ele_tags=None, style="surface", plot_model=True, cpos="iso"):
        _, clim = self._get_resp_peak()
        if self.ModelUpdate:
            func = partial(
                self._create_mesh,
                plotter,
                ele_tags=ele_tags,
                clim=clim,
                plot_all_mesh=plot_model,
                style=style,
                cpos=cpos,
            )
        else:
            resp_plot, scalar_bar = self._create_mesh(
                plotter,
                self.num_steps - 1,
                ele_tags=ele_tags,
                clim=clim,
                plot_all_mesh=plot_model,
                style=style,
                cpos=cpos,
            )
            func = partial(self._update_mesh, ele_tags=ele_tags, resp_plot=resp_plot, scalar_bar=scalar_bar)
        plotter.add_slider_widget(func, [0, self.num_steps - 1], value=self.num_steps - 1, **self.slider_widget_args)

    def plot_peak_step(self, plotter, step="absMax", ele_tags=None, style="surface", plot_model=True, cpos="iso"):
        step, clim = self._get_resp_peak(idx=step)
        self._create_mesh(
            plotter=plotter, value=step, ele_tags=ele_tags, clim=clim, plot_all_mesh=plot_model, style=style, cpos=cpos
        )

    def plot_anim(
        self,
        plotter,
        ele_tags=None,
        framerate: Optional[int] = None,
        savefig: str = "ShellRespAnimation.gif",
        style="surface",
        plot_model=True,
        cpos="iso",
    ):
        if framerate is None:
            framerate = np.ceil(self.num_steps / 11)
        if savefig.endswith(".gif"):
            plotter.open_gif(savefig, fps=framerate)
        else:
            plotter.open_movie(savefig, framerate=framerate)
        _, clim = self._get_resp_peak()
        # plotter.write_frame()  # write initial data

        if self.ModelUpdate:
            for step in range(self.num_steps):
                self._create_mesh(
                    plotter, step, ele_tags=ele_tags, clim=clim, plot_all_mesh=plot_model, style=style, cpos=cpos
                )
                plotter.write_frame()
        else:
            resp_plot, scalar_bar = self._create_mesh(
                plotter,
                0,
                ele_tags=ele_tags,
                clim=clim,
                plot_all_mesh=plot_model,
                style=style,
                cpos=cpos,
            )
            plotter.write_frame()
            for step in range(1, self.num_steps):
                self._update_mesh(
                    step=step,
                    ele_tags=ele_tags,
                    resp_plot=resp_plot,
                    scalar_bar=scalar_bar,
                )
                plotter.write_frame()


def plot_unstruct_responses(
    odb_tag: Union[int, str] = 1,
    ele_type: str = "Shell",
    ele_tags: Optional[Union[int, list]] = None,
    slides: bool = False,
    step: Union[int, str] = "absMax",
    resp_type: str = "sectionForces",
    resp_dof: str = "MXX",
    unit_symbol: Optional[str] = None,
    style: str = "surface",
    cpos: str = "iso",
    plot_model: bool = True,
) -> pv.Plotter:
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
        Otherwise, show the step with the following ``step`` parameter.
    step: Union[int, str], default: "absMax"
        If slides = False, this parameter will be used as the step to plot.
        If str, Optional: [absMax, absMin, Max, Min].
        If int, this step will be demonstrated (counting from 0).
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

    unit_symbol: str, default: None
        Unit symbol to be displayed in the plot.
    style: str, default: surface
        Visualization the mesh style of surfaces and solids.
        One of the following: style='surface', style='wireframe', style='points', style='points_gaussian'.
        Defaults to 'surface'. Note that 'wireframe' only shows a wireframe of the outer geometry.
    cpos: str, default: iso
        Model display perspective, optional: "iso", "xy", "yx", "xz", "zx", "yz", "zy".
        If 3d, defaults to "iso". If 2d, defaults to "xy".
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
    ele_type, resp_type, resp_dof = _check_input(ele_type, resp_type, resp_dof)
    model_info_steps, model_update, resp_step = loadODB(odb_tag, resp_type=ele_type)
    plotter = pv.Plotter(
        notebook=PLOT_ARGS.notebook,
        line_smoothing=PLOT_ARGS.line_smoothing,
        polygon_smoothing=PLOT_ARGS.polygon_smoothing,
        off_screen=PLOT_ARGS.off_screen,
    )
    plotbase = PlotUnstruResponse(model_info_steps, resp_step, model_update)
    plotbase.set_unit_symbol(unit_symbol)
    plotbase.refactor_resp_step(ele_tags=ele_tags, ele_type=ele_type, resp_type=resp_type, component=resp_dof)
    if slides:
        plotbase.plot_slide(
            plotter,
            ele_tags=ele_tags,
            style=style,
            cpos=cpos,
            plot_model=plot_model,
        )
    else:
        plotbase.plot_peak_step(plotter, ele_tags=ele_tags, step=step, style=style, cpos=cpos, plot_model=plot_model)
    if PLOT_ARGS.anti_aliasing:
        plotter.enable_anti_aliasing(PLOT_ARGS.anti_aliasing)
    return plotbase.update(plotter, cpos)


def plot_unstruct_responses_animation(
    odb_tag: Union[int, str] = 1,
    ele_tags: Optional[Union[int, list]] = None,
    framerate: Optional[int] = None,
    ele_type: str = "Shell",
    resp_type: Optional[str] = None,
    resp_dof: Optional[str] = None,
    unit_symbol: Optional[str] = None,
    savefig: Optional[str] = None,
    off_screen: bool = True,
    style: str = "surface",
    cpos: str = "iso",
    plot_model: bool = True,
) -> pv.Plotter:
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
    savefig: str, default: None
        Path to save the animation. The suffix can be ``.gif`` or ``.mp4``.
    off_screen: bool, default: True
        Off-screen rendering, i.e., not showing the rendering window.
        If False, the rendering window will be displayed.
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

    unit_symbol: str, default: None
        Unit symbol to be displayed in the plot.
    style: str, default: surface
        Visualization the mesh style of surfaces and solids.
        One of the following: style='surface', style='wireframe', style='points', style='points_gaussian'.
        Defaults to 'surface'. Note that 'wireframe' only shows a wireframe of the outer geometry.
    cpos: str, default: iso
        Model display perspective, optional: "iso", "xy", "yx", "xz", "zx", "yz", "zy".
        If 3d, defaults to "iso". If 2d, defaults to "xy".
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
    ele_type, resp_type, resp_dof = _check_input(ele_type, resp_type, resp_dof)
    if savefig is None:
        savefig = f"{ele_type.capitalize()}RespAnimation.gif"
    model_info_steps, model_update, resp_step = loadODB(odb_tag, resp_type=ele_type)
    plotter = pv.Plotter(
        notebook=PLOT_ARGS.notebook,
        line_smoothing=PLOT_ARGS.line_smoothing,
        polygon_smoothing=PLOT_ARGS.polygon_smoothing,
        off_screen=off_screen,
    )
    plotbase = PlotUnstruResponse(model_info_steps, resp_step, model_update)
    plotbase.set_unit_symbol(unit_symbol)
    plotbase.refactor_resp_step(ele_tags=ele_tags, ele_type=ele_type, resp_type=resp_type, component=resp_dof)
    plotbase.plot_anim(
        plotter, ele_tags=ele_tags, framerate=framerate, savefig=savefig, style=style, cpos=cpos, plot_model=plot_model
    )
    if PLOT_ARGS.anti_aliasing:
        plotter.enable_anti_aliasing(PLOT_ARGS.anti_aliasing)
    print(f"Animation has been saved as {savefig}!")
    return plotbase.update(plotter, cpos)


def _check_input(ele_type, resp_type, resp_dof):
    if ele_type.lower() == "shell":
        ele_type = "Shell"
        resp_type, resp_dof = _check_input_shell(resp_type, resp_dof)
    elif ele_type.lower() == "plane":
        ele_type = "Plane"
        resp_type, resp_dof = _check_input_plane(resp_type, resp_dof)
    elif ele_type.lower() in ["brick", "solid"]:
        ele_type = "Brick"
        resp_type, resp_dof = _check_input_solid(resp_type, resp_dof)
    else:
        raise ValueError(f"Not supported element type {ele_type}! Valid options are: Shell, Plane, Brick.")  # noqa: TRY003
    return ele_type, resp_type, resp_dof


def _check_input_shell(resp_type, resp_dof):
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
        raise ValueError(  # noqa: TRY003
            f"Not supported response type {resp_type}! Valid options are: sectionForces, sectionDeformations."
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
        raise ValueError(  # noqa: TRY003
            f"Not supported component {resp_dof}! Valid options are: FXX, FYY, FXY, MXX, MYY, MXY, VXZ, VYZ."
        )
    return resp_type, resp_dof


def _check_input_plane(resp_type, resp_dof):
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
            raise ValueError(  # noqa: TRY003
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
            raise ValueError(  # noqa: TRY003
                f"Not supported component {resp_dof}! "
                "Valid options are: sigma11, sigma22, sigma12, p1, p2, sigma_vm, tau_max."
            )
    else:
        raise ValueError(f"Not supported response type {resp_type}! Valid options are: Stresses, Strains.")  # noqa: TRY003
    return resp_type, resp_dof


def _check_input_solid(resp_type, resp_dof):
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
            raise ValueError(  # noqa: TRY003
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
            raise ValueError(  # noqa: TRY003
                f"Not supported component {resp_dof}! "
                "Valid options are: sigma11, sigma22, sigma12, p1, p2, sigma_vm, tau_max."
            )
    else:
        raise ValueError(f"Not supported response type {resp_type}! Valid options are: Stresses, Strains.")  # noqa: TRY003
    return resp_type, resp_dof
