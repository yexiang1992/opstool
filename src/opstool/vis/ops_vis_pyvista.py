"""
Visualizing OpenSeesPy model based on pyvista
"""

import pyvista as pv

from ..utils import check_file
from ._pyvista_base import (
    _deform_anim,
    _deform_vis,
    _deform_peak_vis,
    _eigen_anim,
    _eigen_vis,
    _frame_resp_vis,
    _model_vis,
    _react_vis,
)


class OpsVisPyvista:
    """A class to visualize OpenSeesPy model based on
    `pyvista <https://docs.pyvista.org/index.html>`_.

    Parameters
    -----------
    point_size: float, default=1
        The render size of node.
    line_width: float, default=3
        The width of line element.
    colors_dict: dict,
        The dict for ele color, default color you can see by the class attribute ``default_colors``.
    theme: str, default='document'
        Plot theme for pyvista, optional 'default', 'paraview', 'document', 'dark'.
    color_map: str, default="jet"
        color map to display the cloud plot for pyvista.
        optional 'jet', 'rainbow', 'hot', 'afmhot', 'copper', 'winter', 'cool', 'coolwarm', 'gist_earth',
        'bone', 'binary', 'gray', or any
        `Matplotlib colormap <https://matplotlib.org/stable/tutorials/colors/colormaps.html>`_ .
    on_notebook: bool, default=False
        Whether work in a notebook.
    results_dir: str, default="opstool_output"
        The dir that results saved.

    Returns
    --------
    None
    """

    def __init__(
            self,
            point_size: float = 1,
            line_width: float = 3,
            colors_dict: dict = None,
            theme: str = "document",
            color_map: str = "jet",
            on_notebook: bool = False,
            results_dir: str = "opstool_output",
    ):
        # ------------------------------
        self.point_size = point_size
        self.line_width = line_width
        self.title = "opstool"
        # Initialize the color dict
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
        # -------------------------------------------------
        self.theme = theme
        pv.set_plot_theme(theme)
        self.color_map = color_map
        self.notebook = on_notebook
        # -------------------------------------------------
        self.out_dir = results_dir
        # -------------------------------------------------
        self.bound_fact = 30
        self.anti_aliasing = "msaa"

    def set_color(
        self, point: str = "#580f41", line: str = "#0504aa",
        face: str = "#00c16e", solid: str = "#0cb9c1",
        truss: str = "#7552cc", link: str = "#01ff07",
        constraint: str = "#00ffff"
    ):
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

    def set_anti_aliasing(self, aa_type: str = "msaa"):
        """
        Make edges (lines) appear softer and less pixelated.

        Parameters
        -----------
        aa_type: str, default = "msaa"
            Anti-aliasing type. See the notes below. One of the following:

            * ``"ssaa"`` - Super-Sample Anti-Aliasing
            * ``"msaa"`` - Multi-Sample Anti-Aliasing
            * ``"fxaa"`` - Fast Approximate Anti-Aliasing
        """
        self.anti_aliasing = aa_type

    def model_vis(
            self,
            input_file: str = "ModelData.hdf5",
            show_node_label: bool = False,
            show_ele_label: bool = False,
            label_size: float = 10,
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
            show_outline: bool = True,
            opacity: float = 1.0,
            save_fig: str = "ModelVis.svg",
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
                even if the value is 0.

        load_alpha: float, default = 1.0
            On existing displays, the scaling factor for the load arrow sizes.
        show_constrain_dof: bool, default=False
            Whether to display labels for constrained degrees of freedom.
        show_beam_sec: bool default = False
            Whether to render the 3d section of beam or truss elements.
            If True, the Arg `beam_sec` in :py:meth:`opstool.vis.GetFEMdata.get_model_data`
            must be assigned in advance.
        beam_sec_paras: dict defalut = None,
            A dict to control beam section render, optional key: color, opacity, texture.
            For texture, you can pass an image file with color=None,
            if texture is None, it will be ignored.
        label_size: float, default=8
            The foontsize of node and ele labels, as well as local axis labels.
        show_outline: bool, default=True
            Whether to show the axis frame.
        opacity: float, default=1.0
            Plane and solid element transparency.
        save_fig: str, default='ModelVis.svg'
            The file name to output. If False or None, the file will not be generated.
            The supported formats are:

            * '.svg'
            * '.eps'
            * '.ps'
            * '.pdf'
            * '.tex'

        Returns
        --------
        None
        """
        check_file(save_fig, [".svg", ".eps", ".ps", "pdf", ".tex"])
        _model_vis(
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
            save_fig=save_fig,
        )

    def eigen_vis(
            self,
            mode_tags: list,
            input_file: str = "EigenData.hdf5",
            subplots: bool = False,
            link_views: bool = True,
            alpha: float = 1.0,
            show_outline: bool = False,
            show_origin: bool = False,
            label_size: float = 15,
            opacity: float = 1.0,
            show_face_line: bool = True,
            save_fig: str = "EigenVis.svg",
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
            If True, subplots in a figure. If False, plot in a slider style.
        link_views: bool, default=True
            If True, link the views’ cameras, only usefuly when subplots is True.
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
        save_fig: str, default='EigenVis.svg'
            The file name to output. If False or None, the file will not be generated.
            The supported formats are:

            * '.svg'
            * '.eps'
            * '.ps'
            * '.pdf'
            * '.tex'

        Returns
        --------
        None
        """
        check_file(save_fig, [".svg", ".eps", ".ps", "pdf", ".tex"])
        _eigen_vis(
            self,
            mode_tags=mode_tags,
            input_file=input_file,
            subplots=subplots,
            link_views=link_views,
            alpha=alpha,
            show_outline=show_outline,
            show_origin=show_origin,
            label_size=label_size,
            opacity=opacity,
            show_face_line=show_face_line,
            save_fig=save_fig,
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
            save_fig: str = "EigenAnimation.gif",
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
            Scaling factor, scale further on existing display.
        show_outline: bool, default=False
            Whether to display the axes.
        label_size: float, default=15
            The fontsize of text labels.
        opacity: float, default=1.0
            Plane and solid element transparency.
        framerate: int
            The number of frames per second.
        show_face_line: bool, default=True
            If True, the edges of plate and solid elements will be displayed.
        save_fig: str, default='EigenAnimation.gif'
            The output file name, must end with `.gif` or `.mp4`.
            You can export to any folder, such as "C:mydir/myfile.gif", but the folder `mydir` must exist.

        Returns
        --------
        None
        """
        check_file(save_fig, [".gif", ".mp4"])
        _eigen_anim(
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
            save_fig=save_fig,
        )

    def react_vis(
            self,
            input_file: str = "NodeReactionStepData-1.hdf5",
            slider: bool = False,
            direction: str = "Fz",
            show_values: bool = True,
            show_outline: bool = False,
            save_fig: str = "ReactionVis.svg",
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
        save_fig: str, default='ReactionVis.svg'
            The output file name, must end with `.gif` or `.mp4`.
            You can export to any folder, such as "C:mydir/myfile.gif", but the folder `mydir` must exist.
        """
        _react_vis(
            self,
            input_file=input_file,
            slider=slider,
            direction=direction,
            show_values=show_values,
            show_outline=show_outline,
            save_fig=save_fig,
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
            save_fig: str = "DefoVis.svg",
            model_update: bool = False,
    ):
        """Visualize the deformation of the model at a certain analysis step.

        Parameters
        ----------
        input_file: str, default = "NodeRespStepData-1.hdf5",
            The filename that node responses data saved by
            :py:meth:`opstool.vis.GetFEMdata.get_node_resp_step`.

            .. warning::
                Be careful not to include any path, only filename,
                the file will be loaded from the directory ``results_dir``.

        slider: bool, default=False
            If True, responses in all steps will display by slider style.
            If False, the step that max response will display.
        response: str, default='disp'
            Response type. Optional, "disp", "vel", "accel".
        alpha: float, default=1.0
            Scaling factor, scale further on existing display.
        show_outline: bool, default=False
            Whether to display the axes.
        show_origin: bool, default=False
            Whether to show undeformed shape.
        show_face_line: bool, default=True
            If True, the edges of plate and solid elements will be displayed.
        opacity: float, default=1.0
            Plane and solid element transparency.
        save_fig: str, default='DefoVis.svg'
            The file name to output. If False or None, the file will not be generated.
            The supported formats are:

            * '.svg'
            * '.eps'
            * '.ps'
            * '.pdf'
            * '.tex'

        model_update: bool, default False
            whether to update the model domain data at each analysis step,
            this will be useful if model data has changed.
            For example, some elements and nodes were removed.
            This parameter must same as that in :py:meth:`opstool.vis.GetFEMdata.get_node_resp_step`.

        Returns
        --------
        None
        """
        check_file(save_fig, [".svg", ".eps", ".ps", "pdf", ".tex"])
        _deform_vis(
            self,
            input_file=input_file,
            slider=slider,
            response=response,
            alpha=alpha,
            show_outline=show_outline,
            show_origin=show_origin,
            show_face_line=show_face_line,
            opacity=opacity,
            save_fig=save_fig,
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
            save_fig: str = "DefoAnimation.gif",
            model_update: bool = False,
    ):
        """Deformation animation of the model.

        Parameters
        ----------
        input_file: str, default = "NodeRespStepData-1.hdf5",
            The filename that node responses data saved by
            :py:meth:`opstool.vis.GetFEMdata.get_node_resp_step`.

            .. warning::
                Be careful not to include any path, only filename,
                the file will be loaded from the directory ``results_dir``.

        response: str, default='disp'
            Response type. Optional, "disp", "vel", "accel".
        alpha: float, default=1.0
            Scaling factor, scale further on existing display.
        show_outline: bool, default=False
            Whether to display the axes.
        show_face_line: bool, default=True
            If True, the edges of plate and solid elements will be displayed.
        framerate: int, default=24
            The number of frames per second.
        opacity: float, default=1.0
            Plane and solid element transparency.
        save_fig: str, default='DefoAnimation.gif'
            The output file name, must end with `.gif` or `.mp4`.
            You can export to any folder, such as "C:mydir/myfile.gif", but the folder `mydir` must exist.
        model_update: bool, default False
            whether to update the model domain data at each analysis step,
            this will be useful if model data has changed.
            For example, some elements and nodes were removed.
            This parameter must same as that in :py:meth:`opstool.vis.GetFEMdata.get_node_resp_step`.

        Returns
        --------
        None
        """
        check_file(save_fig, [".gif", ".mp4"])
        _deform_anim(
            self,
            input_file=input_file,
            response=response,
            alpha=alpha,
            show_outline=show_outline,
            opacity=opacity,
            framerate=framerate,
            show_face_line=show_face_line,
            save_fig=save_fig,
            model_update=model_update,
        )

    def deform_peak_vis(
            self,
            input_file: str = "NodeRespStepData-1.hdf5",
            response: str = "disp",
            alpha: float = 1.0,
            show_outline: bool = False,
            show_origin: bool = False,
            show_face_line: bool = True,
            opacity: float = 1,
            save_fig: str = "DefoVis.svg"
    ):
        """Visualize the node peak responses of the model at all analysis steps.
        That is to say, the response of each node in each direction is the absolute maximum
        value in all its time steps.

        .. note::
            This method does not support the arg `model_update`,
            i.e. model nodes and elements do not change during the analysis.

        Parameters
        ----------
        input_file: str, default = "NodeRespStepData-1.hdf5",
            The filename that node responses data saved by
            :py:meth:`opstool.vis.GetFEMdata.get_node_resp_step`.

            .. warning::
                Be careful not to include any path, only filename,
                the file will be loaded from the directory ``results_dir``.

        response: str, default='disp'
            Response type. Optional, "disp", "vel", "accel".
        alpha: float, default=1.0
            Scaling factor, scale further on existing display.
        show_outline: bool, default=False
            Whether to display the axes.
        show_origin: bool, default=False
            Whether to show undeformed shape.
        show_face_line: bool, default=True
            If True, the edges of plate and solid elements will be displayed.
        opacity: float, default=1.0
            Plane and solid element transparency.
        save_fig: str, default='DefoVis.svg'
            The file name to output. If False or None, the file will not be generated.
            The supported formats are:

            * '.svg'
            * '.eps'
            * '.ps'
            * '.pdf'
            * '.tex'

        Returns
        --------
        None
        """
        _deform_peak_vis(
            self,
            input_file=input_file,
            response=response,
            alpha=alpha,
            show_outline=show_outline,
            show_origin=show_origin,
            show_face_line=show_face_line,
            opacity=opacity,
            save_fig=save_fig
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
            save_fig: str = "FrameRespVis.svg",
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
            Scaling factor, scale further on existing display..
        opacity: float, default=1.0
            Plane and solid element transparency.
        save_fig: str, default='FrameRespVis.svg'
            The file name to output. If False or None, the file will not be generated.
            The supported formats are:

            * '.svg'
            * '.eps'
            * '.ps'
            * '.pdf'
            * '.tex'

        Returns
        --------
        None
        """
        check_file(save_fig, [".svg", ".eps", ".ps", "pdf", ".tex"])
        _frame_resp_vis(
            self,
            input_file=input_file,
            ele_tags=ele_tags,
            slider=slider,
            response=response,
            show_values=show_values,
            alpha=alpha,
            opacity=opacity,
            save_fig=save_fig,
        )
