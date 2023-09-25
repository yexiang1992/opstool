"""
Visualizing OpenSeesPy model
"""
import plotly.io as pio
from ._plotly_base import (
    _deform_anim,
    _deform_vis,
    _eigen_anim,
    _eigen_vis,
    _frame_resp_vis,
    _model_vis,
    _react_vis,
)


class OpsVisPlotly:
    """A class to visualize OpenSeesPy model based on plotly.

    Parameters
    ----------
    point_size: float
        The render size of node.
    line_width: float
        The width of line element;
    colors_dict: dict,
        The dict for ele color, default color you can see by the class attribute ``default_colors``.
    theme: str, default=plotly
        Plot theme, optional "plotly", "plotly_white", "plotly_dark", "ggplot2", "seaborn", "simple_white", "none".
    color_map: str, default="jet"
        color map to display the cloud plot. Optional, [‘aggrnyl’, ‘agsunset’, ‘algae’, ‘amp’, ‘armyrose’, ‘balance’,
        ‘blackbody’, ‘bluered’, ‘blues’, ‘blugrn’, ‘bluyl’, ‘brbg’, ‘brwnyl’, ‘bugn’, ‘bupu’, ‘burg’, ‘burgyl’,
        ‘cividis’, ‘curl’, ‘darkmint’, ‘deep’, ‘delta’, ‘dense’, ‘earth’, ‘edge’, ‘electric’, ‘emrld’, ‘fall’,
        ‘geyser’, ‘gnbu’, ‘gray’, ‘greens’, ‘greys’, ‘haline’, ‘hot’, ‘hsv’, ‘ice’, ‘icefire’, ‘inferno’, ‘jet’,
        ‘magenta’, ‘magma’, ‘matter’, ‘mint’, ‘mrybm’, ‘mygbm’, ‘oranges’, ‘orrd’, ‘oryel’, ‘oxy’, ‘peach’, ‘phase’,
        ‘picnic’, ‘pinkyl’, ‘piyg’, ‘plasma’, ‘plotly3’, ‘portland’, ‘prgn’, ‘pubu’, ‘pubugn’, ‘puor’, ‘purd’, ‘purp’,
        ‘purples’, ‘purpor’, ‘rainbow’, ‘rdbu’, ‘rdgy’, ‘rdpu’, ‘rdylbu’, ‘rdylgn’, ‘redor’, ‘reds’, ‘solar’,
        ‘spectral’, ‘speed’, ‘sunset’, ‘sunsetdark’, ‘teal’, ‘tealgrn’, ‘tealrose’, ‘tempo’, ‘temps’, ‘thermal’,
        ‘tropic’, ‘turbid’, ‘turbo’, ‘twilight’, ‘viridis’, ‘ylgn’, ‘ylgnbu’, ‘ylorbr’, ‘ylorrd’].
    on_notebook: bool, default=False
        Whether work in a jupyter notebook.

        .. note::
            This argument is deprecated since v0.8.0, you can call the ``show`` method to display figure.

    results_dir: str, default="opstool_output"
        The dir that results saved.

    Returns
    -------
    None
    """

    def __init__(
        self,
        point_size: float = 2,
        line_width: float = 4,
        colors_dict: dict = None,
        theme: str = "plotly",
        color_map: str = "jet",
        on_notebook: bool = False,
        results_dir: str = "opstool_output",
    ):
        # ------------------------------
        self.point_size = point_size
        self.line_width = line_width
        self.title = "opstool"
        colors = dict(
            point="#580f41",
            line="#0504aa",
            face="#00c16e",
            solid="#0cb9c1",
            truss="#7552cc",
            link="#01ff07",
            constraint="#00ffff",
        )
        if colors_dict is not None:
            colors.update(colors_dict)
        self.default_colors = colors
        self.color_point = colors["point"]
        self.color_line = colors["line"]
        self.color_face = colors["face"]
        self.color_solid = colors["solid"]
        self.color_truss = colors["truss"]
        self.color_link = colors["link"]
        self.color_constraint = colors["constraint"]
        self.theme = theme
        self.color_map = color_map
        self.notebook = on_notebook
        self.out_dir = results_dir
        self.bound_fact = 30

    def set_color(self, point: str = "#580f41", line: str = "#0504aa",
                  face: str = "#00c16e", solid: str = "#0cb9c1",
                  truss: str = "#7552cc", link: str = "#01ff07",
                  constraint: str = "#00ffff"):
        """Set the color for various element types.

        Paramaters
        -----------
        point: str, default="#580f41"
            Nodal color.
        line: str, default="#0504aa"
            Line element color, including beams.
        face: str, default="#00c16e"
            The color of planar elements, including 2D solid elements, plate and shell elements.
        solid: str, default="#0cb9c1"
            The color of solid elements.
        truss: str, default="#7552cc"
            Truss color.
        link: str, default="#01ff07"
            The color of link and bearing elements.
        constraint: str, default="#00ffff"
            The color of multi-point constraint.
        """
        self.color_point = point
        self.color_line = line
        self.color_face = face
        self.color_solid = solid
        self.color_truss = truss
        self.color_link = link
        self.color_constraint = constraint

    def write_html(self, fig, filepath, **kwargs):
        """Write a figure to an HTML file representation.

        .. note::
            Added since v0.8.0.
            The purpose is to replace the argument ``save_html`` in various visualization method.

        Parameters
        -----------
        fig: Figure object.
        filepath: str, output file path.
            A string representing a local file path or a writeable object
            (e.g. a pathlib.Path object or an open file descriptor).
        kwargs:
            Available key parameters see
            https://plotly.com/python-api-reference/generated/plotly.io.write_html.html?highlight=write#plotly.io.write_html.
        """
        pio.write_html(fig, filepath, **kwargs)

    def show(self, fig, *args, **kwargs):
        """Show a figure using either the default renderer(s) or the renderer(s) specified by the renderer argument.

        .. note::
            Added since v0.8.0.

        Parameters
        ----------
        fig : Figure object.
        renderer : str or None (default None)
            A string containing the names of one or more registered renderers (separated by ‘+’ characters) or None.
            If None, then the default renderers specified in plotly.io.renderers.default are used.
        validate : bool (default True))
            True if the figure should be validated before being shown, False otherwise.
        width : int or float
            An integer or float that determines the number of pixels wide the plot is.
            The default is set in plotly.js.
        height : int or float
            An integer or float that determines the number of pixels wide the plot is.
            The default is set in plotly.js.
        config : dict
            A dict of parameters to configure the figure. The defaults are set in plotly.js.

        Returns
        --------
        None
        """
        fig.show(*args, **kwargs)

    def model_vis(
        self,
        input_file: str = "ModelData.hdf5",
        show_node_label: bool = False,
        show_ele_label: bool = False,
        show_local_crd: bool = False,
        show_local_crd_shell: bool = False,
        local_crd_alpha: float = 1.0,
        show_fix_node: bool = True,
        fix_node_alpha: float = 1.0,
        show_load: bool = False,
        load_alpha: float = 1.0,
        show_constrain_dof: bool = False,
        show_beam_sec: bool = False,
        beam_sec_paras: dict = None,
        label_size: float = 8,
        show_outline: bool = True,
        opacity: float = 1.0,
        save_html: str = None,
    ):
        """
        Visualize the model in the current domain.

        Parameters
        ----------
        input_file: str, default = "ModelData.hdf5",
            The filename that model data saved by
            :py:meth:`opstool.vis.GetFEMdata.get_model_data`.

            .. warning::
                Be careful not to include any path, only filename,
                the file will be loaded from the directory ``results_dir``.

        show_node_label: bool, default=False
            Whether to display the node label.
        show_ele_label: bool, default=False
            Whether to display the ele label.
        show_local_crd: bool, default=False
            Whether to display the local axes of beam and link elements.
        show_local_crd_shell: bool, default=False
            Whether to display the local axes of shell elements.
        local_crd_alpha: float, default=1.0
            On existing displays, the scaling factor for the local axis sizes.
        show_fix_node: bool, default=True
            Whether to display the fix nodes.
        fix_node_alpha: float, default=1.0
            On existing displays, the scaling factor for the boundary symbol sizes.
        show_load: bool, default = False
            Whether to display node and beam element loads.
            The sizes of the arrow are related to the size of its load.
            If you want to further control the size, you can use `load_alpha`.
            Currently only supported beam element load types include
            <beamUniform2D, beamUniform3D, beamPoint2D, beamPoint3D>.

            .. note::
                Please make sure that all dofs (or directions) have values
                when adding the ``load`` or ``eleLoad`` command,
                even if the value is 0.0.

        load_alpha: float, default = 1.0
            On existing displays, the scaling factor for the load arrow sizes.
        show_constrain_dof: bool, default=False
            Whether to display labels for constrained degrees of freedom.
        show_beam_sec: bool default = False
            Whether to render the 3d section of beam or truss elements.
            If True, the Arg `beam_sec` in :py:meth:`opstool.vis.GetFEMdata.get_model_data`
            must be assigned in advance.
        beam_sec_paras: dict defalut = None,
            A dict to control beam section render, optional key: color, opacity.
            Note that the backend plotly does not currently support texture.
        label_size: float, default=8
            The fontsize of node and ele label.
        show_outline: bool, default=True
            Whether to show the axis frame.
        opacity: float, default=1.0
            Plane and solid element transparency.
        save_html: str, default=None
            The html file name to output. If False, the html file will not be generated.

            .. note::
                This argument is deprecated since v0.8.0, you can call the ``write_html`` method to
                write an html file.

        Returns
        --------
        Plotly Figure object
            You can call the ``write_html`` method to output an html file, and the ``show`` method will display it.

        """
        return _model_vis(
            self,
            input_file=input_file,
            show_node_label=show_node_label,
            show_ele_label=show_ele_label,
            show_local_crd=show_local_crd,
            local_crd_alpha=local_crd_alpha,
            show_local_crd_shell=show_local_crd_shell,
            show_fix_node=show_fix_node,
            fix_node_alpha=fix_node_alpha,
            show_load=show_load,
            load_alpha=load_alpha,
            show_constrain_dof=show_constrain_dof,
            show_beam_sec=show_beam_sec,
            beam_sec_paras=beam_sec_paras,
            label_size=label_size,
            show_outline=show_outline,
            opacity=opacity,
            save_html=save_html,
        )

    def eigen_vis(
        self,
        mode_tags: list,
        input_file: str = "EigenData.hdf5",
        subplots: bool = False,
        alpha: float = 1.0,
        show_outline: bool = False,
        show_origin: bool = False,
        label_size: float = 15,
        opacity: float = 1.0,
        show_face_line: bool = True,
        save_html: str = None,
    ):
        """Eigenvalue Analysis Visualization.

        Parameters
        ----------
        mode_tags: list[int], or tuple[int]
            Mode tags to be shown, if list or tuple [mode1, mode2], display the multiple modes from mode1 to mode2.
        input_file: str, default = 'EigenData.hdf5',
            The filename that eigen data saved by
            :py:meth:`opstool.vis.GetFEMdata.get_eigen_data`.

            .. warning::
                Be careful not to include any path, only filename,
                the file will be loaded from the directory ``results_dir``.

        subplots: bool, default=False
            If True, subplots in a figure. If False, plot in a slide style.
        alpha: float, default=1.0
            Model scaling factor, scale further on existing display.
        show_outline: bool, default=True
            Whether to display the axes.
        show_origin: bool, default=False
            Whether to show undeformed shape.
        label_size: float, default=15
            The fontsize of text labels.
        opacity: float, default=1.0
            Plane and solid element transparency.
        show_face_line: bool, default=True
            If True, the edges of plate and solid elements will be displayed.
        save_html: str, default=None
            The html file name to output. If False, the html file will not be generated.

            .. note::
                This argument is deprecated since v0.8.0, you can call the ``write_html`` method to
                write an html file.

        Returns
        --------
        Plotly Figure object
            You can call the ``write_html`` method to output an html file, and the ``show`` method will display it.
        """
        return _eigen_vis(
            self,
            mode_tags=mode_tags,
            input_file=input_file,
            subplots=subplots,
            alpha=alpha,
            show_outline=show_outline,
            show_origin=show_origin,
            label_size=label_size,
            opacity=opacity,
            show_face_line=show_face_line,
            save_html=save_html,
        )

    def eigen_anim(
        self,
        mode_tag: int = 1,
        input_file: str = "EigenData.hdf5",
        n_cycle: int = 5,
        alpha: float = 1.0,
        show_outline: bool = False,
        label_size: float = 15,
        opacity: float = 1,
        framerate: int = 3,
        show_face_line: bool = True,
        save_html: str = None,
    ):
        """Animation of Modal Analysis.

        Parameters
        ----------
        mode_tag: int
            The mode tag.
        input_file: str, default = 'EigenData.hdf5',
            The filename that eigen data saved by
            :py:meth:`opstool.vis.GetFEMdata.get_eigen_data`.

            .. warning::
                Be careful not to include any path, only filename,
                the file will be loaded from the directory ``results_dir``.

        n_cycle: int, default = 5,
            The number of cycles in the positive and negative directions of the modal deformation.
        alpha: float, default=1.0
            Model scaling factor, scale further on existing display.
        show_outline: bool, default=False
            Whether to display the axes.
        opacity: float, default=1.0
            Plane and solid element transparency.
        framerate: int
            The number of frames per second.
        show_face_line: bool, default=True
            If True, the edges of plate and solid elements will be displayed.
        save_html: str, default=None
            The html file name to output. If False, the html file will not be generated.

            .. note::
                This argument is deprecated since v0.8.0, you can call the ``write_html`` method to
                write an html file.

        Returns
        --------
        Plotly Figure object
            You can call the ``write_html`` method to output an html file, and the ``show`` method will display it.
        """
        return _eigen_anim(
            self,
            mode_tag=mode_tag,
            input_file=input_file,
            n_cycle=n_cycle,
            alpha=alpha,
            show_outline=show_outline,
            label_size=label_size,
            opacity=opacity,
            framerate=framerate,
            show_face_line=show_face_line,
            save_html=save_html,
        )

    def react_vis(
        self,
        input_file: str = "NodeReactionStepData-1.hdf5",
        slider: bool = False,
        direction: str = "Fz",
        show_values: bool = True,
        show_outline: bool = False,
        save_html: str = None,
    ):
        """Plot the node reactions.

        Parameters
        ----------
        input_file : str, optional, default="NodeReactionStepData-1.hdf5"
            The filename that eigen data saved by
            :py:meth:`opstool.vis.GetFEMdata.get_node_react_step` or
            :py:meth:`opstool.vis.GetFEMdata.save_resp_all`.

            .. warning::
                Be careful not to include any path, only filename,
                the file will be loaded from the directory ``results_dir``.

        slider: bool, default=False
            If True, responses in all steps will display by slider style.
            If False, the step that max response will display.
        direction : str, optional, by default "Fz"
            Type of reaction, if 2D, only be one of ['Fx', 'Fy', 'Mz'];
            if 3D, one of ['Fx', 'Fy', 'Fz', 'Mx', 'My', 'Mz']
        show_values : bool, optional, by default True
            If True, will show the reaction values.
        show_outline: bool, default=False
            Whether to display the axes.
        save_html: str, default=None
            The html file name to output. If False, the html file will not be generated.

            .. note::
                This argument is deprecated since v0.8.0, you can call the ``write_html`` method to
                write an html file.

        Returns
        --------
        Plotly Figure object
            You can call the ``write_html`` method to output an html file, and the ``show`` method will display it.
        """
        return _react_vis(
            self,
            input_file=input_file,
            slider=slider,
            direction=direction,
            show_values=show_values,
            show_outline=show_outline,
            save_html=save_html,
        )

    def deform_vis(
        self,
        input_file: str = "NodeRespStepData-1.hdf5",
        slider: bool = False,
        response: str = "disp",
        alpha: float = 1.0,
        show_outline: bool = False,
        show_origin: bool = False,
        show_face_line: bool = True,
        opacity: float = 1,
        save_html: str = None,
        model_update: bool = False,
    ):
        """Visualize the deformation of the model at a certain analysis step.

        Parameters
        ----------
        input_file: str, default = "NodeRespStepData-1.hdf5",
            The filename that node responses data saved by
            :py:meth:`opstool.vis.GetFEMdata.get_node_resp_step` or
            :py:meth:`opstool.vis.GetFEMdata.save_resp_all`.

            .. warning::
                Be careful not to include any path, only filename,
                the file will be loaded from the directory ``results_dir``.

        slider: bool, default=False
            If True, responses in all steps will display by slider style.
            If False, the step that max response will display.
        response: str, default='disp'
            Response type. Optional, "disp", "vel", "accel".
        alpha: float, default=1.0
            Model scaling factor, scale further on existing display.
        show_outline: bool, default=False
            Whether to display the axes.
        show_origin: bool, default=False
            Whether to show undeformed shape.
        show_face_line: bool, default=True
            If True, the edges of plate and solid elements will be displayed.
        opacity: float, default=1.0
            Plane and solid element transparency.
        save_html: str, default=None
            The html file name to output. If False, the html file will not be generated.

            .. note::
                This argument is deprecated since v0.8.0, you can call the ``write_html`` method to
                write an html file.

        model_update: bool, default False
            whether to update the model domain data at each analysis step,
            this will be useful if model data has changed.
            For example, some elements and nodes were removed.
            This parameter must same as that in :py:meth:`opstool.vis.GetFEMdata.get_node_resp_step`.

        Returns
        --------
        Plotly Figure object
            You can call the ``write_html`` method to output an html file, and the ``show`` method will display it.
        """
        return _deform_vis(
            self,
            input_file=input_file,
            slider=slider,
            response=response,
            alpha=alpha,
            show_outline=show_outline,
            show_origin=show_origin,
            show_face_line=show_face_line,
            opacity=opacity,
            save_html=save_html,
            model_update=model_update,
        )

    def deform_anim(
        self,
        input_file: str = "NodeRespStepData-1.hdf5",
        response: str = "disp",
        alpha: float = 1.0,
        show_outline: bool = False,
        opacity: float = 1,
        framerate: int = 24,
        show_face_line: bool = True,
        save_html: str = None,
        model_update: bool = False,
    ):
        """Deformation animation of the model.

        Parameters
        ----------
        input_file: str, default = "NodeRespStepData-1.hdf5",
            The filename that node responses data saved by
            :py:meth:`opstool.vis.GetFEMdata.get_node_resp_step` or
            :py:meth:`opstool.vis.GetFEMdata.save_resp_all`.

            .. warning::
                Be careful not to include any path, only filename,
                the file will be loaded from the directory ``results_dir``.

        response: str, default='disp'
            Response type. Optional, "disp", "vel", "accel".
        alpha: float, default=1.0
            Model scaling factor, scale further on existing display.
        show_outline: bool, default=False
            Whether to display the axes.
        show_face_line: bool, default=True
            If True, the edges of plate and solid elements will be displayed.
        framerate: int, default=24
            The number of frames per second.
        opacity: float, default=1.0
            Plane and solid element transparency.
        save_html: str, default=None
            The html file name to output. If False, the html file will not be generated.

            .. note::
                This argument is deprecated since v0.8.0, you can call the ``write_html`` method to
                write an html file.

        model_update: bool, default False
            whether to update the model domain data at each analysis step,
            this will be useful if model data has changed.
            For example, some elements and nodes were removed.
            This parameter must same as that in :py:meth:`opstool.vis.GetFEMdata.get_node_resp_step`.

        Returns
        --------
        Plotly Figure object
            You can call the ``write_html`` method to output an html file, and the ``show`` method will display it.
        """

        return _deform_anim(
            self,
            input_file=input_file,
            response=response,
            alpha=alpha,
            show_outline=show_outline,
            opacity=opacity,
            framerate=framerate,
            show_face_line=show_face_line,
            save_html=save_html,
            model_update=model_update,
        )

    def frame_resp_vis(
        self,
        input_file: str = "BeamRespStepData-1.hdf5",
        ele_tags: list = None,
        slider: bool = False,
        response: str = "Mz",
        show_values=True,
        alpha: float = 1.0,
        opacity: float = 1,
        save_html: str = None,
    ):
        """
        Display the force response of frame elements.

        Parameters
        ----------
        input_file: str, default = "BeamRespStepData-1.hdf5",
            The filename that beam frame elements responses data saved by
            :py:meth:`opstool.vis.GetFEMdata.get_frame_resp_step` or
            :py:meth:`opstool.vis.GetFEMdata.save_resp_all`.

            .. warning::
                Be careful not to include any path, only filename,
                the file will be loaded from the directory ``results_dir``.

        ele_tags: int or list[int], default=None
            Element tags to display, if None, all frame elements will display.
        slider: bool, default=False
            If True, responses in all steps will display by slider style.
            If False, the step that max response will display.
        response: str, default='Mz'
            Response type. Optional, "Fx", "Fy", "Fz", "My", "Mz", "Mx".
        show_values: bool, default=True
            If True, will show the response values.
        alpha: float, default=1.0
            Model scaling factor, scale further on existing display.
        opacity: float, default=1.0
            Plane and solid element transparency.
        save_html: str, default=None
            The html file name to output. If False, the html file will not be generated.

            .. note::
                This argument is deprecated since v0.8.0, you can call the ``write_html`` method to
                write an html file.

        Returns
        --------
        Plotly Figure object
            You can call the ``write_html`` method to output an html file, and the ``show`` method will display it.
        """
        return _frame_resp_vis(
            self,
            input_file=input_file,
            ele_tags=ele_tags,
            slider=slider,
            response=response,
            show_values=show_values,
            alpha=alpha,
            opacity=opacity,
            save_html=save_html,
        )
