"""
Visualizing OpenSeesPy model
"""

from ._plotly_base import _model_vis, _eigen_vis, _eigen_anim, _deform_vis, _deform_anim, _frame_resp_vis


class OpsVisPlotly:
    """A class to visualize OpenSeesPy model based on plotly.

    Parameters
    ----------
    point_size: float
        The render size of node.
    line_width: float
        The width of line element;
    colors_dict: dict,
        default: dict(point='#840000', line='#0165fc', face='#06c2ac', solid='#f48924', truss="#7552cc", link="#00c16e")
        The dict for ele color.
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
    results_dir: str, default="opstool_output"
        The dir that results saved.

    Returns
    -------
    None
    """

    def __init__(
        self,
        point_size: float = 5,
        line_width: float = 5,
        colors_dict: dict = None,
        theme: str = "plotly",
        color_map: str = "jet",
        on_notebook: bool = False,
        results_dir: str = "opstool_output"
    ):
        # ------------------------------
        self.point_size = point_size
        self.line_width = line_width
        self.title = "OpenSeesVispy"
        # Initialize the color dict
        colors = dict(
            point="#003666",
            line="#037ef3",
            face="#0cb9c1",
            solid="#7552cc",
            truss="#00a4e4",
            link="#f48924",
        )
        if colors_dict is not None:
            colors.update(colors_dict)
        self.color_point = colors["point"]
        self.color_line = colors["line"]
        self.color_face = colors["face"]
        self.color_solid = colors["solid"]
        self.color_truss = colors["truss"]
        self.color_link = colors["link"]
        # -------------------------------------------------
        self.theme = theme
        self.color_map = color_map

        self.notebook = on_notebook
        # -------------------------------------------------
        self.out_dir = results_dir
        # -------------------------------------------------
        self.bound_fact = 30

    def model_vis(
        self,
        input_file: str = "ModelData.hdf5",
        show_node_label: bool = False,
        show_ele_label: bool = False,
        show_local_crd: bool = False,
        label_size: float = 8,
        show_outline: bool = True,
        opacity: float = 1.0,
        save_html: str = 'ModelVis.html'
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
                the file will be saved to the directory ``results_dir``.

        show_node_label: bool, default=False
            Whether to display the node label.
        show_ele_label: bool, default=False
            Whether to display the ele label.
        show_local_crd: bool, default=False
            Whether to display the local coordinate system.
        label_size: float, default=8
            The foontsize of node and ele label.
        show_outline: bool, default=True
            Whether to show the axis frame.
        opacity: float, default=1.0
            Plane and solid element transparency.
        save_html: str, default='ModelVis.html'
            The html file name to output. If False, the html file will not be generated.

        Returns
        --------
        None

        """
        _model_vis(self,
                   input_file=input_file,
                   show_node_label=show_node_label,
                   show_ele_label=show_ele_label,
                   show_local_crd=show_local_crd,
                   label_size=label_size,
                   show_outline=show_outline,
                   opacity=opacity,
                   save_html=save_html
                   )

    def eigen_vis(
        self,
        mode_tags: list[int],
        input_file: str = 'EigenData.hdf5',
        subplots: bool = False,
        alpha: float = None,
        show_outline: bool = False,
        show_origin: bool = False,
        opacity: float = 1.0,
        show_face_line: bool = True,
        save_html: str = "EigenVis"
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
                the file will be saved to the directory ``results_dir``.

        subplots: bool, default=False
            If True, subplots in a figure. If False, plot in a slide style.
        alpha: float, default=None
            Model scaling factor, the default value is 1/5 of the model boundary according to the maximum deformation.
        show_outline: bool, default=True
            Whether to display the axes.
        show_origin: bool, default=False
            Whether to show undeformed shape.
        opacity: float, default=1.0
            Plane and solid element transparency.
        show_face_line: bool, default=True
            If True, the edges of plate and solid elements will be displayed.
        save_html: str, default='EigenVis.html'
            The html file name to output. If False, the html file will not be generated.

        Returns
        -------
        None
        """
        _eigen_vis(self,
                   mode_tags=mode_tags,
                   input_file=input_file,
                   subplots=subplots,
                   alpha=alpha,
                   show_outline=show_outline,
                   show_origin=show_origin,
                   opacity=opacity,
                   show_face_line=show_face_line,
                   save_html=save_html)

    def eigen_anim(
        self,
        mode_tag: int = 1,
        input_file: str = 'EigenData.hdf5',
        alpha: float = None,
        show_outline: bool = False,
        opacity: float = 1,
        framerate: int = 3,
        show_face_line: bool = True,
        save_html: str = "EigenAnimation"
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
                the file will be saved to the directory ``results_dir``.

        alpha: float, default=None
            Scaling factor, the default value is 1/5 of the model boundary according to the maximum deformation.
        show_outline: bool, default=False
            Whether to display the axes.
        opacity: float, default=1.0
            Plane and solid element transparency.
        framerate: int
            The number of frames per second.
        show_face_line: bool, default=True
            If True, the edges of plate and solid elements will be displayed.
        save_html: str, default='EigenAnimation.html'
            The html file name to output. If False, the html file will not be generated.

        Returns
        -------
        None
        """
        _eigen_anim(self,
                    mode_tag=mode_tag,
                    input_file=input_file,
                    alpha=alpha,
                    show_outline=show_outline,
                    opacity=opacity,
                    framerate=framerate,
                    show_face_line=show_face_line,
                    save_html=save_html
                    )

    def deform_vis(
        self,
        input_file: str = "NodeRespStepData-1.hdf5",
        slider: bool = False,
        response: str = "disp",
        alpha: float = None,
        show_outline: bool = False,
        show_origin: bool = False,
        show_face_line: bool = True,
        opacity: float = 1,
        save_html: str = "DefoVis",
        model_update: bool = False
    ):
        """Visualize the deformation of the model at a certain analysis step.

        Parameters
        ----------
        input_file: str, default = "NodeRespStepData-1.hdf5",
            The filename that node responses data saved by
            :py:meth:`opstool.vis.GetFEMdata.get_node_resp_step`.

            .. warning::
                Be careful not to include any path, only filename,
                the file will be saved to the directory ``results_dir``.

        slider: bool, default=False
            If True, responses in all steps will display by slider style.
            If False, the step that max response will display.
        response: str, default='disp'
            Response type. Optional, "disp", "vel", "accel".
        alpha: float, default=None
            Scaling factor, the default value is 1/5 of the model boundary according to the maximum deformation.
        show_outline: bool, default=False
            Whether to display the axes.
        show_origin: bool, default=False
            Whether to show undeformed shape.
        show_face_line: bool, default=True
            If True, the edges of plate and solid elements will be displayed.
        opacity: float, default=1.0
            Plane and solid element transparency.
        save_html: str, default='DefoVis.html'
            The html file name to output. If False, the html file will not be generated.
        model_update: bool, default False
            whether to update the model domain data at each analysis step,
            this will be useful if model data has changed.
            For example, some elements and nodes were removed.
            This parameter must same as that in :py:meth:`opstool.vis.GetFEMdata.get_node_resp_step`.

        Returns
        -------
        None
        """
        _deform_vis(self,
                    input_file=input_file,
                    slider=slider,
                    response=response,
                    alpha=alpha,
                    show_outline=show_outline,
                    show_origin=show_origin,
                    show_face_line=show_face_line,
                    opacity=opacity,
                    save_html=save_html,
                    model_update=model_update
                    )

    def deform_anim(
        self,
        input_file: str = "NodeRespStepData-1.hdf5",
        response: str = "disp",
        alpha: float = None,
        show_outline: bool = False,
        opacity: float = 1,
        framerate: int = 24,
        show_face_line: bool = True,
        save_html: str = "DefoAnimation",
        model_update: bool = False
    ):
        """Deformation animation of the model.

        Parameters
        ----------
        input_file: str, default = "NodeRespStepData-1.hdf5",
            The filename that node responses data saved by
            :py:meth:`opstool.vis.GetFEMdata.get_node_resp_step`.

            .. warning::
                Be careful not to include any path, only filename,
                the file will be saved to the directory ``results_dir``.

        response: str, default='disp'
            Response type. Optional, "disp", "vel", "accel".
        alpha: float, default=None
            Scaling factor, the default value is 1/5 of the model boundary according to the maximum deformation.
        show_outline: bool, default=False
            Whether to display the axes.
        show_face_line: bool, default=True
            If True, the edges of plate and solid elements will be displayed.
        framerate: int, default=24
            The number of frames per second.
        opacity: float, default=1.0
            Plane and solid element transparency.
        save_html: str, default='DefoAnimation.html'
            The html file name to output. If False, the html file will not be generated.
        model_update: bool, default False
            whether to update the model domain data at each analysis step,
            this will be useful if model data has changed.
            For example, some elements and nodes were removed.
            This parameter must same as that in :py:meth:`opstool.vis.GetFEMdata.get_node_resp_step`.

        Returns
        -------
        None
        """

        _deform_anim(self,
                     input_file=input_file,
                     response=response,
                     alpha=alpha,
                     show_outline=show_outline,
                     opacity=opacity,
                     framerate=framerate,
                     show_face_line=show_face_line,
                     save_html=save_html,
                     model_update=model_update
                     )

    def frame_resp_vis(self,
                       input_file: str = "BeamRespStepData-1.hdf5",
                       ele_tags: list[int] = None,
                       slider: bool = False,
                       response: str = "Mz",
                       show_values=True,
                       alpha: float = None,
                       opacity: float = 1,
                       save_html: str = "FrameRespVis"
                       ):
        """
        Display the force response of frame elements.

        Parameters
        ----------
        input_file: str, default = "BeamRespStepData-1.hdf5",
            The filename that beam frame elements responses data saved by
            :py:meth:`opstool.vis.GetFEMdata.get_frame_resp_step`.

            .. warning::
                Be careful not to include any path, only filename,
                the file will be saved to the directory ``results_dir``.

        ele_tags: int or list[int], default=None
            Element tags to display, if None, all frame elements will display.
        slider: bool, default=False
            If True, responses in all steps will display by slider style.
            If False, the step that max response will display.
        response: str, default='Mz'
            Response type. Optional, "Fx", "Fy", "Fz", "My", "Mz", "Mx".
        show_values: bool, default=True
            If True, will show the response values.
        alpha: float, default=None
            Scaling factor.
        opacity: float, default=1.0
            Plane and solid element transparency.
        save_html: str, default='FrameRespVis.html'
            The html file name to output. If False, the html file will not be generated.
        """
        _frame_resp_vis(self,
                        input_file=input_file,
                        ele_tags=ele_tags,
                        slider=slider,
                        response=response,
                        show_values=show_values,
                        alpha=alpha,
                        opacity=opacity,
                        save_html=save_html
                        )
