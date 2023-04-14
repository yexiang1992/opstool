
from .get_model_data import GetFEMdata
from .ops_vis_pyvista import OpsVisPyvista
from .ops_vis_plotly import OpsVisPlotly


def plot_model(backend: str = "pyvista",
               point_size: float = 1,
               line_width: float = 3,
               colors_dict: dict = None,
               on_notebook: bool = False,
               show_node_label: bool = False,
               show_ele_label: bool = False,
               show_local_crd: bool = False,
               show_fix_node: bool = True,
               show_constrain_dof: bool = False,
               label_size: float = 8,
               show_outline: bool = True,
               opacity: float = 1.0):
    """Plot model quickly.

    Parameters
    ----------
    backend : str, optional "pyvista" or "plotly"
        Plot backend, by default "pyvista"
    point_size: float, default=1
        The render size of node.
    line_width: float, default=3
        The width of line element.
    colors_dict: dict,
        The dict for ele color, default color you can see by the class attribute ``default_colors``.
    on_notebook: bool, default=False
        Whether work in a notebook.
    show_node_label: bool, default=False
            Whether to display the node label.
    show_ele_label: bool, default=False
        Whether to display the ele label.
    show_local_crd: bool, default=False
        Whether to display the local axes of beam and link elements.
    show_fix_node: bool, default=True
        Whether to display the fix nodes.
    show_constrain_dof: bool, default=False
        Whether to display labels for constrained degrees of freedom.
    label_size: float, default=8
        The foontsize of node and ele label.
    show_outline: bool, default=True
        Whether to show the axis frame.
    opacity: float, default=1.0
        Plane and solid element transparency.
    """
    ModelData = GetFEMdata(results_dir="opstool_output")
    ModelData.get_model_data(save_file="ModelData.hdf5")
    if backend.lower() == "pyvista":
        opsvis = OpsVisPyvista(point_size=point_size, line_width=line_width,
                               colors_dict=colors_dict, theme="document",
                               color_map="jet", on_notebook=on_notebook,
                               results_dir="opstool_output")
        opsvis.model_vis(input_file="ModelData.hdf5",
                         show_node_label=show_node_label,
                         show_ele_label=show_ele_label,
                         show_local_crd=show_local_crd,
                         show_fix_node=show_fix_node,
                         show_constrain_dof=show_constrain_dof,
                         label_size=label_size,
                         show_outline=show_outline,
                         opacity=opacity,
                         save_fig=None)
    elif backend.lower() == "plotly":
        opsvis = OpsVisPlotly(point_size=point_size, line_width=line_width,
                              colors_dict=colors_dict, theme="plotly",
                              color_map="jet", on_notebook=on_notebook,
                              results_dir="opstool_output")
        opsvis.model_vis(input_file="ModelData.hdf5",
                         show_node_label=show_node_label,
                         show_ele_label=show_ele_label,
                         show_local_crd=show_local_crd,
                         show_fix_node=show_fix_node,
                         show_constrain_dof=show_constrain_dof,
                         label_size=label_size,
                         show_outline=show_outline,
                         opacity=opacity,
                         save_html='ModelVis.html')
    else:
        raise ValueError("Arg backend must be one of ['pyvista', 'plotly']!")


def plot_eigen(mode_tags: list,
               solver: str = "-genBandArpack",
               backend: str = "pyvista",
               point_size: float = 1,
               line_width: float = 3,
               on_notebook: bool = False,
               subplots: bool = False,
               link_views: bool = True,
               alpha: float = None,
               show_outline: bool = False,
               show_origin: bool = False,
               opacity: float = 1.0,
               show_face_line: bool = True):
    """Fast eigen visualization.

    Parameters
    ----------
    mode_tags: list[int], or tuple[int]
        Mode tags to be shown, if list or tuple [mode1, mode2], display the multiple modes from mode1 to mode2.
    solver: str, default '-genBandArpack'
        type of solver, optional '-genBandArpack', '-fullGenLapack',
        see https://openseespydoc.readthedocs.io/en/latest/src/eigen.html.
    backend : str, optional "pyvista" or "plotly"
        Plot backend, by default "pyvista"
    point_size: float, default=1
        The render size of node.
    line_width: float, default=3
        The width of line element.
    on_notebook: bool, default=False
        Whether work in a notebook.
    subplots: bool, default=False
        If True, subplots in a figure. If False, plot in a slider style.
    link_views: bool, default=True
        If True, link the views’ cameras, only usefuly when subplots is True, and backend='pyvista'.
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
    """
    ModelData = GetFEMdata(results_dir="opstool_output")
    ModelData.get_eigen_data(mode_tag=mode_tags[-1], solver=solver,
                             save_file='EigenData.hdf5')
    if backend.lower() == "pyvista":
        opsvis = OpsVisPyvista(point_size=point_size, line_width=line_width,
                               theme="document", color_map="jet",
                               on_notebook=on_notebook,
                               results_dir="opstool_output")
        opsvis.eigen_vis(input_file='EigenData.hdf5',
                         mode_tags=mode_tags, subplots=subplots,
                         alpha=alpha, show_outline=show_outline,
                         show_origin=show_origin, opacity=opacity,
                         show_face_line=show_face_line,
                         link_views=link_views,
                         save_fig=None)
    elif backend.lower() == "plotly":
        opsvis = OpsVisPlotly(point_size=point_size, line_width=line_width,
                              theme="plotly", color_map="jet",
                              on_notebook=on_notebook,
                              results_dir="opstool_output")
        opsvis.eigen_vis(input_file='EigenData.hdf5',
                         mode_tags=mode_tags, subplots=subplots,
                         alpha=alpha, show_outline=show_outline,
                         show_origin=show_origin, opacity=opacity,
                         show_face_line=show_face_line,
                         save_html="EigenVis.html")
    else:
        raise ValueError("Arg backend must be one of ['pyvista', 'plotly']!")
