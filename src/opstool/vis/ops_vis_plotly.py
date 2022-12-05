"""
Visualizing OpenSeesPy model
"""

import shelve
from typing import Union

import numpy as np
import plotly.graph_objs as go
import plotly.io as pio
from plotly.subplots import make_subplots

from ..utils import check_file, shape_dict


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
        Whether work in a notebook.
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

        filename = self.out_dir + '/ModelData'
        with shelve.open(filename) as db:
            model_info = db["ModelInfo"]
            cells = db["Cell"]

        fig = go.Figure()
        points_no_deform = model_info["coord_no_deform"]
        plotter = []
        # ------------------------------------------------------------------------
        # face plot
        face_cells = [cells["plane"], cells["tetrahedron"], cells["brick"]]
        face_cells_tags = [cells["plane_tags"],
                           cells["tetrahedron_tags"], cells["brick_tags"]]
        face_colors = [self.color_face, self.color_solid, self.color_solid]
        names = ["plane", "tetrahedron", "brick"]
        for ii in range(len(face_cells)):
            if len(face_cells[ii]) > 0:
                face_line_points = []
                face_points = []
                face_mid_points = []
                veci = []
                vecj = []
                veck = []
                for cell in face_cells[ii]:
                    data0 = points_no_deform[cell[1:], :]
                    face_mid_points.append(np.mean(data0, axis=0))
                    data1 = [np.NAN, np.NAN, np.NAN]
                    data = np.vstack([data0, data1])
                    if data0.shape[0] == 3:
                        veci.append(len(face_points) + 0)
                        vecj.append(len(face_points) + 1)
                        veck.append(len(face_points) + 2)
                    else:
                        veci.append(len(face_points) + 0)
                        veci.append(len(face_points) + 0)
                        vecj.append(len(face_points) + 1)
                        vecj.append(len(face_points) + 2)
                        veck.append(len(face_points) + 2)
                        veck.append(len(face_points) + 3)
                        # i, j, k = [0, 0], [1, 2], [2, 3]
                    face_line_points.extend(list(data))
                    face_points.extend(list(data0))
                face_line_points = np.array(face_line_points)
                face_points = np.array(face_points)
                face_mid_points = np.array(face_mid_points)
                plotter.append(
                    go.Scatter3d(   # face lines
                        x=face_line_points[:, 0],
                        y=face_line_points[:, 1],
                        z=face_line_points[:, 2],
                        line=dict(color="black", width=self.line_width / 5),
                        mode="lines",
                        name=names[ii],
                        connectgaps=False,
                        hoverinfo="skip",
                    )
                )
                plotter.append(
                    go.Mesh3d(
                        x=face_points[:, 0],
                        y=face_points[:, 1],
                        z=face_points[:, 2],
                        i=veci,
                        j=vecj,
                        k=veck,
                        name=names[ii],
                        color=face_colors[ii],
                        opacity=opacity,
                        hoverinfo="skip",
                    )
                )
                # hover label
                # ['circle', 'circle-open', 'cross', 'diamond',
                # 'diamond-open', 'square', 'square-open', 'x']
                plotter.append(
                    go.Scatter3d(
                        x=face_mid_points[:, 0],
                        y=face_mid_points[:, 1],
                        z=face_mid_points[:, 2],
                        marker=dict(size=self.point_size, color=face_colors[ii],
                                    symbol='circle-open'),
                        mode="markers",
                        name=names[ii],
                        customdata=face_cells_tags[ii],
                        hovertemplate='<b>tag: %{customdata}</b>',
                    )
                )
        # ------------------------------------------------------------------------
        # line plot
        line_cells = [cells["truss"], cells["link"],
                      cells["beam"], cells["other_line"]]
        line_cells_tags = [cells["truss_tags"], cells["link_tags"],
                           cells["beam_tags"], cells["other_line_tags"]]
        line_colors = [self.color_truss, self.color_link,
                       self.color_line, self.color_line]
        line_widths = [self.line_width, 0.5 * self.line_width,
                       self.line_width, self.line_width]
        names = ["truss", "link", "beam", "other_line"]
        for i in range(len(line_cells)):
            if len(line_cells[i]) > 0:
                line_points = []
                line_mid_points = []
                for cell in line_cells[i]:
                    data0 = points_no_deform[cell[1:], :]
                    data1 = [np.NAN, np.NAN, np.NAN]
                    data = np.vstack([data0, data1])
                    line_points.extend(list(data))
                    line_mid_points.append(np.mean(data0, axis=0))
                line_points = np.array(line_points)
                line_mid_points = np.array(line_mid_points)
                plotter.append(
                    go.Scatter3d(
                        x=line_points[:, 0],
                        y=line_points[:, 1],
                        z=line_points[:, 2],
                        line=dict(color=line_colors[i], width=line_widths[i]),
                        mode="lines",
                        name=names[i],
                        connectgaps=False,
                        hoverinfo="skip",
                    )
                )
                # hover label
                plotter.append(
                    go.Scatter3d(
                        x=line_mid_points[:, 0],
                        y=line_mid_points[:, 1],
                        z=line_mid_points[:, 2],
                        marker=dict(size=self.point_size, color=line_colors[i],
                                    symbol='circle-open'),
                        mode="markers",
                        name=names[i],
                        customdata=line_cells_tags[i],
                        hovertemplate='<b>tag: %{customdata}</b>',
                    )
                )
        # ------------------------------------------------------------------------
        # point plot
        node_labels = [str(i) for i in model_info["NodeTags"]]
        point_plot = go.Scatter3d(
            x=points_no_deform[:, 0],
            y=points_no_deform[:, 1],
            z=points_no_deform[:, 2],
            marker=dict(size=self.point_size, color=self.color_point),
            mode="markers",
            name="Node",
            customdata=node_labels,
            hovertemplate='<b>x: %{x}</b><br>y: %{y}<br>z: %{z} <br>tag: %{customdata}',
        )
        plotter.append(point_plot)
        fig.add_traces(plotter)

        if show_node_label:
            node_labels = [str(i) for i in model_info["NodeTags"]]
            txt_plot = go.Scatter3d(
                x=points_no_deform[:, 0],
                y=points_no_deform[:, 1],
                z=points_no_deform[:, 2],
                text=node_labels,
                textfont=dict(color="#6e750e", size=label_size),
                mode="text",
                name="Node Label",
            )
            fig.add_trace(txt_plot)

        if show_ele_label:
            ele_labels = [str(i) for i in model_info["EleTags"]]
            txt_plot = go.Scatter3d(
                x=model_info["coord_ele_midpoints"][:, 0],
                y=model_info["coord_ele_midpoints"][:, 1],
                z=model_info["coord_ele_midpoints"][:, 2],
                text=ele_labels,
                textfont=dict(color="#650021", size=label_size),
                mode="text",
                name="Ele Label",
            )
            fig.add_trace(txt_plot)

        if np.max(np.abs(points_no_deform[:, -1])) < 1e-5:
            eye = dict(x=0, y=-1e-5, z=1.5)   # for 2D camera
        else:
            eye = dict(x=-1.5, y=-1.5, z=1.5)  # for 3D camera

        if show_local_crd:
            beam_midpoints = model_info["beam_midpoints"]
            beam_xlocal = model_info["beam_xlocal"]
            beam_ylocal = model_info["beam_ylocal"]
            beam_zlocal = model_info["beam_zlocal"]
            length = model_info["max_bound"] / 350
            xcoords = beam_midpoints + length * beam_xlocal
            ycoords = beam_midpoints + length * beam_ylocal
            zcoords = beam_midpoints + length * beam_zlocal
            localx_points = []
            localy_points = []
            localz_points = []
            for i, midpoints in enumerate(beam_midpoints):
                localx_points.append(midpoints)
                localx_points.append(xcoords[i])
                localx_points.append([np.NAN, np.NAN, np.NAN])
                localy_points.append(midpoints)
                localy_points.append(ycoords[i])
                localy_points.append([np.NAN, np.NAN, np.NAN])
                localz_points.append(midpoints)
                localz_points.append(zcoords[i])
                localz_points.append([np.NAN, np.NAN, np.NAN])
            localx_points = np.array(localx_points)
            localy_points = np.array(localy_points)
            localz_points = np.array(localz_points)
            plotter1 = go.Scatter3d(
                x=localx_points[:, 0],
                y=localx_points[:, 1],
                z=localx_points[:, 2],
                line=dict(color="red", width=3.5),
                mode="lines",
                connectgaps=False,
                name='',
                # customdata=['x'] * n_beam,
                hovertemplate='<b>x</b>')
            plotter2 = go.Scatter3d(
                x=localy_points[:, 0],
                y=localy_points[:, 1],
                z=localy_points[:, 2],
                line=dict(color="orange", width=3.5),
                mode="lines",
                connectgaps=False,
                name='',
                hovertemplate='<b>y</b>')
            plotter3 = go.Scatter3d(
                x=localz_points[:, 0],
                y=localz_points[:, 1],
                z=localz_points[:, 2],
                line=dict(color="green", width=3.5),
                mode="lines",
                connectgaps=False,
                name='',
                hovertemplate='<b>z</b>')
            fig.add_traces([plotter1, plotter2, plotter3])

        fig.update_layout(
            template=self.theme,
            autosize=True,
            showlegend=False,
            scene=dict(aspectratio=dict(x=1, y=1, z=1), aspectmode="data",
                       camera=dict(eye=eye, projection=dict(type="orthographic"))),
            title=dict(font=dict(family="courier", color='black', size=25),
                       text=("<b>OpenSeesPy 3D View</b> <br>" +
                             f"Num. of Node: {model_info['num_node']} || Num. of Ele:{model_info['num_ele']}")
                       )
        )
        if not show_outline:
            fig.update_layout(
                scene=dict(xaxis={'showgrid': False, 'zeroline': False, 'visible': False},
                           yaxis={'showgrid': False,
                                  'zeroline': False, 'visible': False},
                           zaxis={'showgrid': False, 'zeroline': False, 'visible': False}, ),
            )
        if save_html:
            if not save_html.endswith(".html"):
                save_html += ".html"
            pio.write_html(fig, file=save_html, auto_open=True)
        if self.notebook:
            fig.show(renderer='notebook')

    def eigen_vis(
            self,
            mode_tags: list[int],
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
        filename = self.out_dir + '/EigenData'
        with shelve.open(filename) as db:
            eigen_data = db["EigenInfo"]

        f = eigen_data["f"]
        eigenvector = eigen_data["eigenvector"]
        num_mode_tag = len(f)
        modei, modej = mode_tags
        modei, modej = int(modei), int(modej)
        if modej > num_mode_tag:
            raise ValueError(
                f"Insufficient number of modes in eigen file {filename}!")

        fig = go.Figure()
        off_axis = {'showgrid': False, 'zeroline': False, 'visible': False}
        title = dict(font=dict(family="courier", color='black', size=25),
                     text="<b>OpenSeesPy Eigen 3D View</b>"
                     )

        # !subplots
        if subplots:
            if modej - modei + 1 > 49:
                raise ValueError(
                    "When subplots True, mode_tag range must < 49 for clarify"
                )
            shape = shape_dict[modej - modei + 1]
            specs = [[{'is_3d': True}
                      for i in range(shape[1])] for j in range(shape[0])]
            subplot_titles = []
            for i, idx in enumerate(range(modei, modej + 1)):
                txt = "Mode {}: T = {:.3f} s".format(idx, 1 / f[idx - 1])
                subplot_titles.append(txt)

            fig = make_subplots(rows=shape[0], cols=shape[1],
                                specs=specs, figure=fig,
                                print_grid=False, subplot_titles=subplot_titles,
                                horizontal_spacing=0.07 / shape[1],
                                vertical_spacing=0.1 / shape[0],
                                column_widths=[1] * shape[1],
                                row_heights=[1] * shape[0]
                                )
            for i, idx in enumerate(range(modei, modej + 1)):
                eigen_vec = eigenvector[idx - 1]
                if alpha is None:
                    alpha_ = (
                        eigen_data["max_bound"] / self.bound_fact /
                        np.max(np.sqrt(np.sum(eigen_vec ** 2, axis=1)))
                    )
                else:
                    alpha_ = alpha
                eigen_points = eigen_data["coord_no_deform"] + \
                    eigen_vec * alpha_
                scalars = np.sqrt(np.sum(eigen_vec ** 2, axis=1))

                idxi = int(np.ceil((i + 1) / shape[1]) - 1)
                idxj = int(i - idxi * shape[1])
                # ---------------------------------------------------------
                if show_origin:
                    points_origin = eigen_data["coord_no_deform"]
                else:
                    points_origin = None
                plotter = _generate_all_mesh(points=eigen_points, scalars=scalars, opacity=opacity,
                                             lines_cells=eigen_data["all_lines"],
                                             face_cells=eigen_data["all_faces"],
                                             coloraxis=f"coloraxis{i + 1}",
                                             points_origin=points_origin,
                                             point_size=self.point_size,
                                             line_width=self.line_width,
                                             show_face_line=show_face_line)
                fig.add_traces(plotter, rows=idxi + 1, cols=idxj + 1)
            scenes = dict()
            coloraxiss = dict()
            if np.max(np.abs(eigen_points[:, -1])) < 1e-8:
                eye = dict(x=0, y=-1e-5, z=1.5)
            else:
                eye = dict(x=-1.5, y=-1.5, z=1.5)
            if show_outline:
                for k in range(shape[0] * shape[1]):
                    coloraxiss[f"coloraxis{k + 1}"] = dict(
                        showscale=False, colorscale=self.color_map)
                    if k >= 1:
                        scenes[f"scene{k + 1}"] = dict(aspectratio=dict(x=1, y=1, z=1), aspectmode="data",
                                                       camera=dict(eye=eye, projection=dict(type="orthographic")))
                fig.update_layout(
                    title=title,
                    template=self.theme,
                    autosize=True,
                    showlegend=False,
                    coloraxis=dict(showscale=False, colorscale=self.color_map),
                    scene=dict(aspectratio=dict(x=1, y=1, z=1), aspectmode="data",
                               camera=dict(eye=eye, projection=dict(type="orthographic"))),
                    **scenes,
                    **coloraxiss
                )
            else:
                for k in range(shape[0] * shape[1]):
                    coloraxiss[f"coloraxis{k + 1}"] = dict(
                        showscale=False, colorscale=self.color_map)
                    if k >= 1:
                        scenes[f"scene{k + 1}"] = dict(aspectratio=dict(x=1, y=1, z=1), aspectmode="data",
                                                       camera=dict(eye=eye,
                                                                   projection=dict(type="orthographic")),
                                                       xaxis=off_axis, yaxis=off_axis, zaxis=off_axis)

                fig.update_layout(
                    title=title,
                    template=self.theme,
                    autosize=True,
                    showlegend=False,
                    coloraxis=dict(showscale=False, colorscale=self.color_map),
                    scene=dict(aspectratio=dict(x=1, y=1, z=1), aspectmode="data",
                               camera=dict(eye=eye, projection=dict(
                                   type="orthographic")),
                               xaxis=off_axis, yaxis=off_axis, zaxis=off_axis),
                    **scenes,
                    **coloraxiss
                )
        # !single mode
        else:
            n_data = None
            cmins = []
            cmaxs = []
            for i, idx in enumerate(range(modei, modej + 1)):
                step = idx - 1
                eigen_vec = eigenvector[step]
                if alpha is None:
                    alpha_ = (
                        eigen_data["max_bound"] / self.bound_fact /
                        np.max(np.sqrt(np.sum(eigen_vec ** 2, axis=1)))
                    )
                else:
                    alpha_ = alpha
                eigen_points = eigen_data["coord_no_deform"] + \
                    eigen_vec * alpha_
                scalars = np.sqrt(np.sum(eigen_vec ** 2, axis=1))
                cmins.append(np.min(scalars))
                cmaxs.append(np.max(scalars))

                # -------------------------------------------------------------
                # start plot
                if show_origin:
                    points_origin = eigen_data["coord_no_deform"]
                else:
                    points_origin = None
                plotter = _generate_all_mesh(points=eigen_points, scalars=scalars, opacity=opacity,
                                             lines_cells=eigen_data["all_lines"],
                                             face_cells=eigen_data["all_faces"],
                                             coloraxis=f"coloraxis{step + 1}",
                                             points_origin=points_origin,
                                             point_size=self.point_size, line_width=self.line_width,
                                             show_face_line=show_face_line)
                fig.add_traces(plotter)
                if i == 0:
                    n_data = len(fig.data)
            for i in range(n_data, len(fig.data)):
                fig.data[i].visible = False
            # Create and add slider
            steps = []
            for i, idx in enumerate(range(modei, modej + 1)):
                txt = "Mode {}: T = {:.3f} s".format(idx, 1 / f[idx - 1])
                step = dict(
                    method="update",
                    args=[{"visible": [False] * len(fig.data)},
                          {"title": txt}],  # layout attribute
                    label=str(idx),
                )
                step["args"][0]["visible"][n_data *
                                           i:n_data * (i + 1)] = [True] * n_data
                # Toggle i'th trace to "visible"
                steps.append(step)
            sliders = [dict(
                active=modej - modei + 1,
                currentvalue={"prefix": "Mode: "},
                pad={"t": 50},
                steps=steps
            )]
            coloraxiss = {}
            for i in range(modej - modei + 1):
                coloraxiss[f"coloraxis{i + 1}"] = dict(colorscale=self.color_map,
                                                       cmin=cmins[i],
                                                       cmax=cmaxs[i],
                                                       colorbar=dict(tickfont=dict(size=15)))

            if np.max(np.abs(eigen_points[:, -1])) < 1e-8:
                eye = dict(x=0, y=-1e-5, z=1.5)
            else:
                eye = dict(x=-1.5, y=-1.5, z=1.5)
            fig.update_layout(
                template=self.theme,
                autosize=True,
                showlegend=False,
                scene=dict(aspectmode="data",
                           camera=dict(eye=eye,
                                       projection=dict(type="orthographic"))),  # orthographic,perspective
                title=title,
                sliders=sliders,
                **coloraxiss
            )
            if not show_outline:
                fig.update_layout(
                    scene=dict(xaxis=off_axis, yaxis=off_axis, zaxis=off_axis),
                )
        if save_html:
            if not save_html.endswith(".html"):
                save_html += ".html"
            pio.write_html(fig, file=save_html, auto_open=True)
        if self.notebook:
            fig.show(renderer='notebook')

    def eigen_anim(
            self,
            mode_tag: int = 1,
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
        filename = self.out_dir + '/EigenData'
        with shelve.open(filename) as db:
            eigen_data = db["EigenInfo"]

        f = eigen_data["f"]
        eigenvector = eigen_data["eigenvector"]
        num_mode_tag = len(f)
        if mode_tag > num_mode_tag:
            raise ValueError("Insufficient number of modes in open file")
        eigen_vec = eigenvector[mode_tag - 1]
        f_ = f[mode_tag - 1]
        if alpha is None:
            alpha_ = (
                eigen_data["max_bound"]
                / self.bound_fact
                / np.max(np.sqrt(np.sum(eigen_vec ** 2, axis=1)))
            )
        else:
            alpha_ = alpha
        eigen_points = eigen_data["coord_no_deform"] + eigen_vec * alpha_
        anti_eigen_points = eigen_data["coord_no_deform"] - eigen_vec * alpha_
        scalars = np.sqrt(np.sum(eigen_vec ** 2, axis=1))
        plt_points = [anti_eigen_points,
                      eigen_data["coord_no_deform"], eigen_points]
        index = [1] + [2, 0] * 3
        nb_frames = len(index)
        times = int(nb_frames / framerate)

        # -----------------------------------------------------------------------------
        # start plot
        frames = []
        for k, idx in enumerate(index):
            points = plt_points[idx]
            xyz = (eigen_data["coord_no_deform"] - points) / alpha_
            xyz_eigen = np.sqrt(np.sum(xyz ** 2, axis=1))
            plotter = _generate_all_mesh(points=points, scalars=xyz_eigen,
                                         point_size=self.point_size, line_width=self.line_width,
                                         opacity=opacity,
                                         lines_cells=eigen_data["all_lines"],
                                         face_cells=eigen_data["all_faces"],
                                         coloraxis="coloraxis",
                                         show_face_line=show_face_line)
            frames.append(go.Frame(data=plotter, name="step:" + str(k + 1)))

        fig = go.Figure(frames=frames)
        # Add data to be displayed before animation starts
        plotter0 = _generate_all_mesh(points=plt_points[index[0]], scalars=scalars * 0,
                                      point_size=self.point_size, line_width=self.line_width,
                                      opacity=opacity,
                                      lines_cells=eigen_data["all_lines"],
                                      face_cells=eigen_data["all_faces"],
                                      coloraxis="coloraxis",
                                      show_face_line=show_face_line)
        fig.add_traces(plotter0)

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
                    for k, f in enumerate(fig.frames)
                ],
            }
        ]
        # Layout
        if np.max(np.abs(eigen_points[:, -1])) < 1e-8:
            eye = dict(x=0, y=-1e-5, z=1.5)
        else:
            eye = dict(x=-1.5, y=-1.5, z=1.5)
        txt = "<br> Mode {}: T = {:.3f} s".format(mode_tag, 1 / f_)
        fig.update_layout(
            title=dict(font=dict(family="courier", color='black', size=25),
                       text="<b>OpenSeesPy Eigen 3D View</b>" + txt
                       ),
            template=self.theme,
            autosize=True,
            showlegend=False,
            coloraxis=dict(colorscale=self.color_map,
                           colorbar=dict(tickfont=dict(size=15))),
            scene=dict(aspectratio=dict(x=1, y=1, z=1), aspectmode="data",
                       camera=dict(eye=eye, projection=dict(
                           type="orthographic"))
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
            sliders=sliders
        )
        if not show_outline:
            fig.update_layout(
                scene=dict(xaxis={'showgrid': False, 'zeroline': False, 'visible': False},
                           yaxis={'showgrid': False,
                                  'zeroline': False, 'visible': False},
                           zaxis={'showgrid': False, 'zeroline': False, 'visible': False}, ),
            )

        if save_html:
            if not save_html.endswith(".html"):
                save_html += ".html"
            pio.write_html(fig, file=save_html, auto_open=True)
        if self.notebook:
            fig.show(renderer='notebook')

    def deform_vis(
            self,
            analysis_tag: int,
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
        analysis_tag: int
            Analysis tag in get_node_resp_step() method.
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

        Returns
        -------
        None
        """

        filename = self.out_dir + f'/NodeRespStepData-{analysis_tag}'
        with shelve.open(filename) as db:
            model_info_steps = db["ModelInfoSteps"]
            cell_steps = db["CellSteps"]
            node_resp_steps = db["NodeRespSteps"]

        num_steps = len(node_resp_steps["disp"])

        # ! max response
        max_disp = [np.max(np.sqrt(np.sum(node_disp ** 2, axis=1)))
                    for node_disp in node_resp_steps["disp"]]
        max_step = np.argmax(max_disp)

        if model_update:
            bounds = model_info_steps["bound"][0]
        else:
            bounds = model_info_steps["bound"]
        max_node_disp = node_resp_steps["disp"][max_step]
        max_node_vel = node_resp_steps["vel"][max_step]
        max_node_accel = node_resp_steps["accel"][max_step]
        # cmap
        if response.lower() == "disp":
            scalars = np.sqrt(np.sum(max_node_disp ** 2, axis=1))
            data = node_resp_steps["disp"]
        elif response.lower() == "vel":
            scalars = np.sqrt(np.sum(max_node_vel ** 2, axis=1))
            data = node_resp_steps["vel"]
        elif response.lower() == "accel":
            scalars = np.sqrt(np.sum(max_node_accel ** 2, axis=1))
            data = node_resp_steps["accel"]
        else:
            raise ValueError("response must be disp, vel, or accel!")
        cmin, cmax = np.min(scalars), np.max(scalars)
        # scale factor
        if alpha is None:
            max_bound = np.max(
                [bounds[1] - bounds[0], bounds[3] - bounds[2], bounds[5] - bounds[4]])
            value = np.max(np.sqrt(np.sum(max_node_disp ** 2, axis=1)))
            alpha_ = max_bound / self.bound_fact / value
        else:
            alpha_ = alpha
        # ------------------------------------------------------------------------
        fig = go.Figure()
        # -------------------------------------------------------------------------
        if slider:
            n_data = None
            for step in range(num_steps):
                node_disp = node_resp_steps["disp"][step]
                if model_update:
                    node_nodeform_coords = model_info_steps["coord_no_deform"][step]
                    bounds = model_info_steps["bound"][step]
                    lines_cells = cell_steps["all_lines"][step]
                    faces_cells = cell_steps["all_faces"][step]
                else:
                    node_nodeform_coords = model_info_steps["coord_no_deform"]
                    bounds = model_info_steps["bound"]
                    lines_cells = cell_steps["all_lines"]
                    faces_cells = cell_steps["all_faces"]
                node_deform_coords = alpha_ * node_disp + node_nodeform_coords
                if show_origin:
                    points_origin = node_nodeform_coords
                else:
                    points_origin = None
                plotter = _generate_all_mesh(points=node_deform_coords, scalars=scalars,
                                             point_size=self.point_size, line_width=self.line_width,
                                             opacity=opacity,
                                             lines_cells=lines_cells,
                                             face_cells=faces_cells,
                                             coloraxis=f"coloraxis{step + 1}",
                                             points_origin=points_origin,
                                             show_face_line=show_face_line)
                fig.add_traces(plotter)
                if step == 0:
                    n_data = len(fig.data)
            for i in range(n_data, len(fig.data)):
                fig.data[i].visible = False
            # ! Create and add slider
            steps = []
            for i in range(num_steps):
                maxx, maxy, maxz = np.max(data[i], axis=0)
                minx, miny, minz = np.min(data[i], axis=0)
                txt = (f"<b>Step {i+1} {response}</b>"
                       f"<br>max.x={maxx:.2E} | min.x={minx:.2E}"
                       f"<br>max.y={maxy:.2E} | min.y={miny:.2E}"
                       f"<br>max.z={maxz:.2E} | min.z={minz:.2E}")
                step = dict(
                    method="update",
                    args=[{"visible": [False] * len(fig.data)},
                          {"title": txt}],  # layout attribute
                    label=str(i + 1),
                )
                idxi, idxj = n_data * i, n_data * (i + 1)
                step["args"][0]["visible"][idxi:idxj] = [True] * n_data
                # Toggle i'th trace to "visible"
                steps.append(step)
            sliders = [dict(
                active=num_steps,
                currentvalue={"prefix": "Step: "},
                pad={"t": 50},
                steps=steps
            )]
            coloraxiss = {}
            for i in range(num_steps):
                coloraxiss[f"coloraxis{i + 1}"] = dict(colorscale=self.color_map,
                                                       cmin=cmin,
                                                       cmax=cmax,
                                                       colorbar=dict(tickfont=dict(size=15)))

            if np.max(np.abs(node_deform_coords[:, -1])) < 1e-5:
                eye = dict(x=0, y=-1e-5, z=1.5)
            else:
                eye = dict(x=-1.5, y=-1.5, z=1.5)
            fig.update_layout(
                template=self.theme,
                autosize=True,
                showlegend=False,
                scene=dict(aspectmode="data",
                           camera=dict(eye=eye,
                                       projection=dict(type="orthographic"))),  # orthographic,perspective
                title=dict(font=dict(family="courier", color='black', size=25),
                           text="<b>OpenSeesPy Deformation 3D View</b>"
                           ),
                sliders=sliders,
                **coloraxiss
            )
        # -------------------------------------------------------------------------
        else:  # plot a single step
            node_disp = node_resp_steps["disp"][max_step]
            if model_update:
                node_nodeform_coords = model_info_steps["coord_no_deform"][max_step]
                bounds = model_info_steps["bound"][max_step]
                lines_cells = cell_steps["all_lines"][max_step]
                faces_cells = cell_steps["all_faces"][max_step]
            else:
                node_nodeform_coords = model_info_steps["coord_no_deform"]
                bounds = model_info_steps["bound"]
                lines_cells = cell_steps["all_lines"]
                faces_cells = cell_steps["all_faces"]
            node_deform_coords = alpha_ * node_disp + node_nodeform_coords
            if show_origin:
                points_origin = node_nodeform_coords
            else:
                points_origin = None
            plotter = _generate_all_mesh(points=node_deform_coords, scalars=scalars,
                                         point_size=self.point_size, line_width=self.line_width,
                                         opacity=opacity,
                                         lines_cells=lines_cells,
                                         face_cells=faces_cells,
                                         coloraxis="coloraxis",
                                         points_origin=points_origin,
                                         show_face_line=show_face_line)
            fig.add_traces(plotter)
            if np.max(np.abs(node_deform_coords[:, -1])) < 1e-5:
                eye = dict(x=0, y=-1e-5, z=1.5)
            else:
                eye = dict(x=-1.5, y=-1.5, z=1.5)
            maxx, maxy, maxz = np.max(node_disp, axis=0)
            minx, miny, minz = np.min(node_disp, axis=0)
            txt = (f"<br>Step {max_step + 1} {response}"
                   f"<br>max.x={maxx:.2E} | min.x={minx:.2E}"
                   f"<br>max.y={maxy:.2E} | min.y={miny:.2E}"
                   f"<br>max.z={maxz:.2E} | min.z={minz:.2E}")
            fig.update_layout(
                template=self.theme,
                autosize=True,
                showlegend=False,
                scene=dict(aspectmode="data",
                           camera=dict(eye=eye,
                                       projection=dict(type="orthographic"))),  # orthographic,perspective
                coloraxis=dict(colorscale=self.color_map, cmin=cmin, cmax=cmax,
                               colorbar=dict(tickfont=dict(size=15))),
                title=dict(font=dict(family="courier", color='black', size=25),
                           text="<b>OpenSeesPy Deformation 3D View</b>" + txt
                           ),
            )
        if not show_outline:
            fig.update_layout(
                scene=dict(xaxis={'showgrid': False, 'zeroline': False, 'visible': False},
                           yaxis={'showgrid': False,
                                  'zeroline': False, 'visible': False},
                           zaxis={'showgrid': False, 'zeroline': False, 'visible': False}, ),
            )
        if save_html:
            if not save_html.endswith(".html"):
                save_html += ".html"
            pio.write_html(fig, file=save_html, auto_open=True)
        if self.notebook:
            fig.show(renderer='notebook')

    def deform_anim(
            self,
            analysis_tag: int,
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
        analysis_tag: int
            Analysis tag in get_node_resp_step() method.
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

        Returns
        -------
        None
        """

        filename = self.out_dir + f'/NodeRespStepData-{analysis_tag}'
        with shelve.open(filename) as db:
            model_info_steps = db["ModelInfoSteps"]
            cell_steps = db["CellSteps"]
            node_resp_steps = db["NodeRespSteps"]

        num_steps = len(node_resp_steps['disp'])
        times = int(num_steps / framerate)

        # ! max response
        max_disp = [np.max(np.sqrt(np.sum(node_disp ** 2, axis=1)))
                    for node_disp in node_resp_steps["disp"]]
        max_step = np.argmax(max_disp)

        if model_update:
            node_nodeform_coords = model_info_steps["coord_no_deform"][0]
            bounds = model_info_steps["bound"][0]
        else:
            node_nodeform_coords = model_info_steps["coord_no_deform"]
            bounds = model_info_steps["bound"]
        max_node_disp = node_resp_steps["disp"][max_step]
        max_node_vel = node_resp_steps["vel"][max_step]
        max_node_accel = node_resp_steps["accel"][max_step]
        # scale factor
        if alpha is None:
            max_bound = np.max(
                [bounds[1] - bounds[0], bounds[3] - bounds[2], bounds[5] - bounds[4]])
            alpha_ = max_bound / self.bound_fact / \
                np.max(np.sqrt(np.sum(max_node_disp ** 2, axis=1)))
        else:
            alpha_ = alpha
        # cmap
        if response.lower() == "disp":
            scalars = np.sqrt(np.sum(max_node_disp ** 2, axis=1))
            data = node_resp_steps["disp"]
        elif response.lower() == "vel":
            scalars = np.sqrt(np.sum(max_node_vel ** 2, axis=1))
            data = node_resp_steps["vel"]
        elif response.lower() == "accel":
            scalars = np.sqrt(np.sum(max_node_accel ** 2, axis=1))
            data = node_resp_steps["accel"]
        else:
            raise ValueError("response must be disp, vel, or accel!")
        cmin, cmax = np.min(scalars), np.max(scalars)

        # -----------------------------------------------------------------------------
        # start plot
        frames = []
        for step in range(num_steps):
            node_disp = node_resp_steps["disp"][step]
            if model_update:
                node_nodeform_coords = model_info_steps["coord_no_deform"][step]
                bounds = model_info_steps["bound"][step]
                lines_cells = cell_steps["all_lines"][step]
                faces_cells = cell_steps["all_faces"][step]
            else:
                node_nodeform_coords = model_info_steps["coord_no_deform"]
                bounds = model_info_steps["bound"]
                lines_cells = cell_steps["all_lines"]
                faces_cells = cell_steps["all_faces"]
            node_deform_coords = alpha_ * node_disp + node_nodeform_coords
            plotter = _generate_all_mesh(points=node_deform_coords, scalars=scalars,
                                         point_size=self.point_size, line_width=self.line_width,
                                         opacity=opacity,
                                         lines_cells=lines_cells,
                                         face_cells=faces_cells,
                                         coloraxis="coloraxis",
                                         show_face_line=show_face_line)
            frames.append(go.Frame(data=plotter, name="step:" + str(step + 1)))

        fig = go.Figure(frames=frames)
        # Add data to be displayed before animation starts
        plotter0 = _generate_all_mesh(points=node_nodeform_coords, scalars=scalars * 0,
                                      point_size=self.point_size, line_width=self.line_width,
                                      opacity=opacity,
                                      lines_cells=lines_cells,
                                      face_cells=faces_cells,
                                      coloraxis="coloraxis",
                                      show_face_line=show_face_line)
        fig.add_traces(plotter0)

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
                    for k, f in enumerate(fig.frames)
                ],
            }
        ]
        # Layout
        for i in range(len(fig.frames)):
            maxx, maxy, maxz = np.max(data[i], axis=0)
            minx, miny, minz = np.min(data[i], axis=0)
            txt = ("<b>OpenSeesPy Defo 3D View</b>"
                   f"<br>Step {i+1} {response}"
                   f"<br>max.x={maxx:.2E} | min.x={minx:.2E}"
                   f"<br>max.y={maxy:.2E} | min.y={miny:.2E}"
                   f"<br>max.z={maxz:.2E} | min.z={minz:.2E}")
            fig.frames[i]['layout'].update(title_text=txt)
        if np.max(np.abs(node_deform_coords[:, -1])) < 1e-8:
            eye = dict(x=0, y=-1e-5, z=1.5)
        else:
            eye = dict(x=-1.5, y=-1.5, z=1.5)

        fig.update_layout(
            title=dict(font=dict(family="courier", color='black', size=25),
                       text="<b>OpenSeesPy Defo 3D View</b>"),
            template=self.theme,
            autosize=True,
            showlegend=False,
            coloraxis=dict(colorscale=self.color_map,
                           colorbar=dict(tickfont=dict(size=15))),
            scene=dict(aspectratio=dict(x=1, y=1, z=1), aspectmode="data",
                       camera=dict(eye=eye, projection=dict(
                           type="orthographic"))
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
            sliders=sliders
        )
        if not show_outline:
            fig.update_layout(
                scene=dict(xaxis={'showgrid': False, 'zeroline': False, 'visible': False},
                           yaxis={'showgrid': False,
                                  'zeroline': False, 'visible': False},
                           zaxis={'showgrid': False, 'zeroline': False, 'visible': False}, ),
            )

        if save_html:
            if not save_html.endswith(".html"):
                save_html += ".html"
            pio.write_html(fig, file=save_html, auto_open=True)
        if self.notebook:
            fig.show(renderer='notebook')

    def frame_resp_vis(self,
                       analysis_tag: int,
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
        analysis_tag: int
            Analysis tag in get_node_resp_step() method.
        ele_tags: int or list[int], default=None
            Element tags to display, if None, all frame elements will display.
        slider: bool, default=False
            If True, responses in all steps will display by slider style.
            If False, the step that max response will display.
        response: str, default='Mz'
            Response type. Optional, "N", "Vy", "Vz", "My", "Mz", "T".
        show_values: bool, default=True
            If True, will show the response values.
        alpha: float, default=None
            Scaling factor.
        opacity: float, default=1.0
            Plane and solid element transparency.
        save_html: str, default='FrameRespVis.html'
            The html file name to output. If False, the html file will not be generated.
        """
        filename = self.out_dir + f'/BeamRespStepData-{analysis_tag}'
        with shelve.open(filename) as db:
            beam_infos = db["BeamInfos"]
            beam_resp_step = db["BeamRespSteps"]

        beam_tags = beam_infos['beam_tags']
        ylocal_map = beam_infos['ylocal']
        zlocal_map = beam_infos['zlocal']
        local_forces_step = beam_resp_step['localForces']

        if ele_tags is None:
            ele_tags = beam_tags
            beam_node_coords = beam_infos['beam_node_coords']
            beam_cells = beam_infos['beam_cells']
            beam_cell_map = beam_infos['beam_cell_map']
            idxs = range(len(beam_cells))
        else:
            ele_tags = np.atleast_1d(ele_tags)
            beam_node_coords = []
            beam_cells = []
            beam_cell_map = {}
            idxs = []
            for i, eletag in enumerate(ele_tags):
                idx = beam_infos['beam_cell_map'][eletag]
                idxs.append(idx)
                nodei, nodej = beam_infos['beam_cells'][idx][1:]
                beam_node_coords.append(beam_infos['beam_node_coords'][nodei])
                beam_node_coords.append(beam_infos['beam_node_coords'][nodej])
                beam_cells.append([2, 2 * i, 2 * i + 1])
                beam_cell_map[eletag] = i
            beam_node_coords = np.array(beam_node_coords)
            beam_cells = np.array(beam_cells)

        idx_plottype_map = dict(n=[0, 6], vy=[1, 7], vz=[2, 8],
                                my=[4, 10], mz=[5, 11], t=[3, 9])
        axis_map_map = dict(n=zlocal_map, vy=ylocal_map, vz=zlocal_map,
                            my=zlocal_map, mz=ylocal_map, t=ylocal_map)
        idx_plottype = idx_plottype_map[response.lower()]
        axis_map = axis_map_map[response.lower()]

        maxv = [np.max(np.max(np.abs(data[:, idx_plottype]), axis=1))
                for data in local_forces_step]
        maxstep = np.argmax(maxv)
        local_forces = local_forces_step[maxstep][:, idx_plottype][idxs]
        cmin, cmax = np.min(local_forces), np.max(local_forces)
        if alpha is None:
            local_forces = local_forces_step[maxstep][:, idx_plottype][idxs]
            max_coord = np.max(beam_node_coords, axis=0)
            min_coord = np.min(beam_node_coords, axis=0)
            max_bound = np.max(max_coord - min_coord)
            maxv = np.amax(np.abs(local_forces))
            alpha_ = max_bound / maxv / 10
        else:
            alpha_ = alpha
        num_steps = len(local_forces_step)

        # ------------------------------------------------------------------------
        fig = go.Figure()
        # -------------------------------------------------------------------------
        if slider:
            n_data = None
            for step in range(num_steps):
                local_forces = local_forces_step[step][:, idx_plottype][idxs]
                local_forces_scale = local_forces * alpha_
                # add force face cells
                # TODO if values symbol versa, need trangle
                label_poins = []
                labels = []
                face_points = []
                face_cells = []
                scalars = []
                for i, eletag in enumerate(ele_tags):
                    axis = axis_map[eletag]
                    anglex = lines_angle(axis, [1, 0, 0])
                    angley = lines_angle(axis, [0, 1, 0])
                    anglez = lines_angle(axis, [0, 0, 1])
                    node1, node2 = beam_cells[beam_cell_map[eletag]][1:]
                    coord1, coord2 = beam_node_coords[node1], beam_node_coords[node2]
                    f1, f2 = local_forces_scale[beam_cell_map[eletag]]
                    f1_, f2_ = local_forces[beam_cell_map[eletag]]
                    dx1, dy1, dz1 = f1 * np.cos(anglex), f1 * \
                        np.cos(angley), f1 * np.cos(anglez)
                    dx2, dy2, dz2 = f2 * np.cos(anglex), f2 * \
                        np.cos(angley), f2 * np.cos(anglez)
                    coord3 = coord2 + np.array([dx2, dy2, dz2])
                    coord4 = coord1 + np.array([dx1, dy1, dz1])
                    label_poins.extend([coord3, coord4])
                    labels.extend([f2_, f1_])
                    n = len(face_points)
                    if f1 * f2 >= 0:
                        face_points.extend([coord1, coord2, coord3, coord4])
                        face_cells.append([4, n, n + 1, n + 2, n + 3])
                        scalars.extend([f1_, f2_, f2_, f1_])
                    else:
                        ratio = np.abs(f2 / f1)
                        ratio = 1 / (ratio + 1)
                        coord0 = coord1 + (coord2 - coord1) * ratio
                        face_points.extend(
                            [coord1, coord0, coord4, coord2, coord0, coord3])
                        face_cells.append([3, n, n + 1, n + 2])
                        face_cells.append([3, n + 3, n + 4, n + 5])
                        scalars.extend([f1_, 0, f1_, f2_, 0, f2_])
                labels = [f"{label:.2E}" for label in labels]
                label_poins = np.array(label_poins)
                face_points = np.array(face_points)
                scalars = np.array(scalars)
                # ----------------------------------------------------------------------------------------
                line_plot = _generate_line_mesh(beam_node_coords, beam_cells, line_width=self.line_width,
                                                color=self.color_line, use_cmap=False)
                face_plot = _generate_face_mesh(face_points, face_cells, show_face_line=False, opacity=opacity,
                                                use_cmap=True, scalars=scalars, coloraxis=f"coloraxis{step+1}")
                fig.add_traces(line_plot + face_plot)
                if show_values:
                    txt_plot = go.Scatter3d(
                        x=label_poins[:, 0],
                        y=label_poins[:, 1],
                        z=label_poins[:, 2],
                        text=labels,
                        textfont=dict(color="#6e750e", size=8),
                        mode="text",
                        name=f"{response}",
                    )
                    fig.add_trace(txt_plot)
                if step == 0:
                    n_data = len(fig.data)
            for i in range(n_data, len(fig.data)):
                fig.data[i].visible = False
            # ! Create and add slider
            steps = []
            for i in range(num_steps):
                maxx = np.max(local_forces_step[i][:, idx_plottype][idxs], axis=0)
                minx = np.min(local_forces_step[i][:, idx_plottype][idxs], axis=0)
                txt = (f"<b>Step {i+1} {response}</b>"
                       f"<br>max.={maxx:.2E}|min.={minx:.2E}")
                step = dict(
                    method="update",
                    args=[{"visible": [False] * len(fig.data)},
                          {"title": txt}],  # layout attribute
                    label=str(i + 1),
                )
                idxi, idxj = n_data * i, n_data * (i + 1) - 1
                step["args"][0]["visible"][idxi:idxj] = [True] * n_data
                # Toggle i'th trace to "visible"
                steps.append(step)
            sliders = [dict(
                active=num_steps,
                currentvalue={"prefix": "Step: "},
                pad={"t": 50},
                steps=steps
            )]
            coloraxiss = {}
            for i in range(num_steps):
                coloraxiss[f"coloraxis{i + 1}"] = dict(colorscale=self.color_map,
                                                       cmin=cmin,
                                                       cmax=cmax,
                                                       colorbar=dict(tickfont=dict(size=15)))

            if np.max(np.abs(beam_node_coords[:, -1])) < 1e-5:
                eye = dict(x=0, y=-1e-5, z=1.5)
            else:
                eye = dict(x=-1.5, y=-1.5, z=1.5)
            fig.update_layout(
                template=self.theme,
                autosize=True,
                showlegend=False,
                scene=dict(aspectmode="data",
                           camera=dict(eye=eye,
                                       projection=dict(type="orthographic"))),  # orthographic,perspective
                title=dict(font=dict(family="courier", color='black', size=25),
                           text="<b>OpenSeesPy Frames Response 3D View</b>"
                           ),
                sliders=sliders,
                **coloraxiss
            )
        # -------------------------------------------------------------------------
        else:  # plot a single step
            local_forces = local_forces_step[maxstep][:, idx_plottype][idxs]
            local_forces_scale = local_forces * alpha_
            # add force face cells
            # TODO if values symbol versa, need trangle
            label_poins = []
            labels = []
            face_points = []
            face_cells = []
            scalars = []
            for i, eletag in enumerate(ele_tags):
                axis = axis_map[eletag]
                anglex = lines_angle(axis, [1, 0, 0])
                angley = lines_angle(axis, [0, 1, 0])
                anglez = lines_angle(axis, [0, 0, 1])
                node1, node2 = beam_cells[beam_cell_map[eletag]][1:]
                coord1, coord2 = beam_node_coords[node1], beam_node_coords[node2]
                f1, f2 = local_forces_scale[beam_cell_map[eletag]]
                f1_, f2_ = local_forces[beam_cell_map[eletag]]
                dx1, dy1, dz1 = f1 * np.cos(anglex), f1 * \
                    np.cos(angley), f1 * np.cos(anglez)
                dx2, dy2, dz2 = f2 * np.cos(anglex), f2 * \
                    np.cos(angley), f2 * np.cos(anglez)
                coord3 = coord2 + np.array([dx2, dy2, dz2])
                coord4 = coord1 + np.array([dx1, dy1, dz1])
                label_poins.extend([coord3, coord4])
                labels.extend([f2_, f1_])
                n = len(face_points)
                if f1 * f2 >= 0:
                    face_points.extend([coord1, coord2, coord3, coord4])
                    face_cells.append([4, n, n + 1, n + 2, n + 3])
                    scalars.extend([f1_, f2_, f2_, f1_])
                else:
                    ratio = np.abs(f2 / f1)
                    ratio = 1 / (ratio + 1)
                    coord0 = coord1 + (coord2 - coord1) * ratio
                    face_points.extend(
                        [coord1, coord0, coord4, coord2, coord0, coord3])
                    face_cells.append([3, n, n + 1, n + 2])
                    face_cells.append([3, n + 3, n + 4, n + 5])
                    scalars.extend([f1_, 0, f1_, f2_, 0, f2_])
            labels = [f"{label:.2E}" for label in labels]
            label_poins = np.array(label_poins)
            face_points = np.array(face_points)
            scalars = np.array(scalars)
            # ----------------------------------------------------------------------------------------
            line_plot = _generate_line_mesh(beam_node_coords, beam_cells, line_width=self.line_width,
                                            color=self.color_line, use_cmap=False)
            face_plot = _generate_face_mesh(face_points, face_cells, show_face_line=False, opacity=opacity,
                                            use_cmap=True, scalars=scalars, coloraxis="coloraxis")
            fig.add_traces(line_plot + face_plot)
            if show_values:
                txt_plot = go.Scatter3d(
                    x=label_poins[:, 0],
                    y=label_poins[:, 1],
                    z=label_poins[:, 2],
                    text=labels,
                    textfont=dict(color="#6e750e", size=8),
                    mode="text",
                    name=f"{response}",
                )
                fig.add_trace(txt_plot)
            if np.max(np.abs(beam_node_coords[:, -1])) < 1e-5:
                eye = dict(x=0, y=-1e-5, z=1.5)
            else:
                eye = dict(x=-1.5, y=-1.5, z=1.5)
            maxx = np.max(local_forces)
            minx = np.min(local_forces)
            txt = (f"<b>Step {i+1} {response}</b>"
                   f"<br>max.={maxx:.2E}|min.={minx:.2E}")
            fig.update_layout(
                template=self.theme,
                autosize=True,
                showlegend=False,
                scene=dict(aspectmode="data",
                           camera=dict(eye=eye,
                                       projection=dict(type="orthographic"))),  # orthographic,perspective
                coloraxis=dict(colorscale=self.color_map, cmin=cmin, cmax=cmax,
                               colorbar=dict(tickfont=dict(size=15))),
                title=dict(font=dict(family="courier", color='black', size=25),
                           text="<b>OpenSeesPy Frames Response 3D View</b>" + txt
                           ),
            )
        fig.update_layout(
            scene=dict(xaxis={'showgrid': False, 'zeroline': False, 'visible': False},
                       yaxis={'showgrid': False, 'zeroline': False, 'visible': False},
                       zaxis={'showgrid': False, 'zeroline': False, 'visible': False}, ),
        )
        if save_html:
            if not save_html.endswith(".html"):
                save_html += ".html"
            pio.write_html(fig, file=save_html, auto_open=True)
        if self.notebook:
            fig.show(renderer='notebook')


def _generate_line_mesh(points, cells, line_width=1, color='blue', scalars=None, use_cmap=False, coloraxis=None):
    """
    generate the mesh from the points and cell
    """
    plotter = []
    line_points = []
    line_scalars = []
    for cell in cells:
        data0 = points[cell[1:], :]
        data1 = [np.NAN, np.NAN, np.NAN]
        data = np.vstack([data0, data1])
        line_points.extend(list(data))
        if use_cmap:
            line_scalars.extend(list(scalars[cell[1:]]) + [np.NAN])
    line_points = np.array(line_points)
    line_scalars = np.array(line_scalars)
    line_dict = dict()
    if use_cmap:
        line_dict = dict(color=scalars, width=line_width,
                         cmin=np.min(scalars), cmax=np.max(scalars),
                         coloraxis=coloraxis)
    else:
        line_dict = dict(color=color, width=line_width)
    plt_obj = go.Scatter3d(
        x=line_points[:, 0],
        y=line_points[:, 1],
        z=line_points[:, 2],
        line=line_dict,
        mode="lines",
        connectgaps=False,
        hoverinfo="skip",
    )
    plotter.append(plt_obj)
    return plotter


def _generate_face_mesh(points, cells, line_width=1,
                        color='blue', scalars=None, use_cmap=False, coloraxis=None,
                        show_face_line=False, opacity=0.75):
    """
    generate the mesh from the points and cell
    """
    plotter = []
    face_line_points = []
    face_points = []
    face_scalars = []
    veci = []
    vecj = []
    veck = []
    for cell in cells:
        data0 = points[cell[1:], :]
        data1 = [np.NAN, np.NAN, np.NAN]
        data = np.vstack([data0, data1])
        if data0.shape[0] == 3:
            veci.append(len(face_points) + 0)
            vecj.append(len(face_points) + 1)
            veck.append(len(face_points) + 2)
        else:
            veci.append(len(face_points) + 0)
            veci.append(len(face_points) + 0)
            vecj.append(len(face_points) + 1)
            vecj.append(len(face_points) + 2)
            veck.append(len(face_points) + 2)
            veck.append(len(face_points) + 3)
            # i, j, k = [0, 0], [1, 2], [2, 3]
        face_line_points.extend(list(data))
        face_points.extend(list(data0))
        if use_cmap:
            face_scalars.extend(list(scalars[cell[1:]]))
    face_line_points = np.array(face_line_points)
    face_points = np.array(face_points)
    face_scalars = np.array(face_scalars)
    # plot new
    if show_face_line:
        plotter.append(
            go.Scatter3d(
                x=face_line_points[:, 0],
                y=face_line_points[:, 1],
                z=face_line_points[:, 2],
                line=dict(color='black', width=line_width),
                mode="lines",
                connectgaps=False,
                hoverinfo="skip",
            )
        )
    if use_cmap:
        kargs = dict(text=face_scalars,
                     intensity=face_scalars,
                     cmin=np.min(scalars),
                     cmax=np.max(scalars),
                     coloraxis=coloraxis)
    else:
        kargs = dict(color=color)
    plotter.append(
        go.Mesh3d(
            x=face_points[:, 0],
            y=face_points[:, 1],
            z=face_points[:, 2],
            i=veci,
            j=vecj,
            k=veck,
            opacity=opacity,
            hoverinfo="skip",
            **kargs
        )
    )
    return plotter


def _generate_all_mesh(points, scalars, opacity, lines_cells, face_cells, point_size=1, line_width=1,
                       points_origin=None, coloraxis="coloraxis", show_face_line=True):
    """
    Auxiliary function for generating all meshes
    """
    plotter = []
    # ------------------------------------------------------------------------
    # face plot
    if len(face_cells) > 0:
        face_line_points = []
        face_points = []
        face_scalars = []
        face_line_origin_points = []
        veci = []
        vecj = []
        veck = []
        for cell in face_cells:
            data0 = points[cell[1:], :]
            data1 = [np.NAN, np.NAN, np.NAN]
            data = np.vstack([data0, data1])
            if points_origin is not None:
                data00 = points_origin[cell[1:], :]
                data11 = [np.NAN, np.NAN, np.NAN]
                data_ori = np.vstack([data00, data11])
                face_line_origin_points.extend(list(data_ori))
            if data0.shape[0] == 3:
                veci.append(len(face_points) + 0)
                vecj.append(len(face_points) + 1)
                veck.append(len(face_points) + 2)
            else:
                veci.append(len(face_points) + 0)
                veci.append(len(face_points) + 0)
                vecj.append(len(face_points) + 1)
                vecj.append(len(face_points) + 2)
                veck.append(len(face_points) + 2)
                veck.append(len(face_points) + 3)
                # i, j, k = [0, 0], [1, 2], [2, 3]
            face_line_points.extend(list(data))
            face_points.extend(list(data0))
            face_scalars.extend(list(scalars[cell[1:]]))

        face_line_points = np.array(face_line_points)
        face_points = np.array(face_points)
        face_scalars = np.array(face_scalars)
        face_line_origin_points = np.array(face_line_origin_points)
        # plot origin
        if points_origin is not None:
            plotter.append(
                go.Scatter3d(
                    x=face_line_origin_points[:, 0],
                    y=face_line_origin_points[:, 1],
                    z=face_line_origin_points[:, 2],
                    line=dict(color='gray', width=line_width / 2),
                    mode="lines",
                    connectgaps=False,
                    hoverinfo="skip",
                )
            )
        # plot new
        if show_face_line:
            plotter.append(
                go.Scatter3d(
                    x=face_line_points[:, 0],
                    y=face_line_points[:, 1],
                    z=face_line_points[:, 2],
                    line=dict(color='black', width=line_width / 3),
                    mode="lines",
                    connectgaps=False,
                    hoverinfo="skip",
                )
            )
        plotter.append(
            go.Mesh3d(
                x=face_points[:, 0],
                y=face_points[:, 1],
                z=face_points[:, 2],
                i=veci,
                j=vecj,
                k=veck,
                text=face_scalars,
                intensity=face_scalars,
                cmin=np.min(scalars),
                cmax=np.max(scalars),
                coloraxis=coloraxis,
                opacity=opacity,
                hoverinfo="skip",
            )
        )
    # ----------------------------
    # line plot
    if len(lines_cells) > 0:
        line_points = []
        line_scalars = []
        line_origin_points = []
        for cell in lines_cells:
            data0 = points[cell[1:], :]
            data1 = [np.NAN, np.NAN, np.NAN]
            data = np.vstack([data0, data1])
            if points_origin is not None:
                data00 = points_origin[cell[1:], :]
                data11 = [np.NAN, np.NAN, np.NAN]
                data_ori = np.vstack([data00, data11])
                line_origin_points.extend(list(data_ori))
            line_points.extend(list(data))
            line_scalars.extend(list(scalars[cell[1:]]) + [np.NAN])
        line_points = np.array(line_points)
        line_scalars = np.array(line_scalars)
        line_origin_points = np.array(line_origin_points)
        # plot origin
        if points_origin is not None:
            plotter.append(
                go.Scatter3d(
                    x=line_origin_points[:, 0],
                    y=line_origin_points[:, 1],
                    z=line_origin_points[:, 2],
                    line=dict(color='gray', width=line_width / 2),
                    mode="lines",
                    connectgaps=False,
                    hoverinfo="skip",
                )
            )
        # plot new
        plotter.append(
            go.Scatter3d(
                x=line_points[:, 0],
                y=line_points[:, 1],
                z=line_points[:, 2],
                line=dict(color=line_scalars, width=line_width,
                          cmin=np.min(scalars), cmax=np.max(scalars),
                          coloraxis=coloraxis,
                          ),
                text=line_scalars,
                mode="lines",
                connectgaps=False,
                hoverinfo="skip",
            )
        )
    # ------------------------------------------------------------------------
    # point plot
    point_plot = go.Scatter3d(
        x=points[:, 0],
        y=points[:, 1],
        z=points[:, 2],
        marker=dict(size=point_size / 10, color=scalars,
                    coloraxis=coloraxis),
        mode="markers",
        hoverinfo="skip",
    )
    plotter.append(point_plot)
    return plotter


def lines_angle(v1, v2):
    # return np.arctan2(np.linalg.norm(np.cross(v1, v2)), np.dot(v1, v2))
    x = np.array(v1)
    y = np.array(v2)
    l_x = np.sqrt(x.dot(x))
    l_y = np.sqrt(y.dot(y))
    cos_ = x.dot(y) / (l_x * l_y)
    angle_r = np.arccos(cos_)
    return angle_r
