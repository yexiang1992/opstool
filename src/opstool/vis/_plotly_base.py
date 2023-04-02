import warnings

import h5py
import numpy as np
import plotly.graph_objs as go
import plotly.io as pio
from plotly.subplots import make_subplots

from ..utils import shape_dict


def _make_faces(points, cells):
    face_line_points = []
    face_points = []
    face_mid_points = []
    veci = []
    vecj = []
    veck = []
    for cell in cells:
        data0 = points[cell[1:], :]
        face_mid_points.append(np.mean(data0, axis=0))
        data1 = [np.NAN, np.NAN, np.NAN]
        data = np.vstack([data0, data0[0], data1])
        if data0.shape[0] == 3:
            veci.append(len(face_points) + 0)
            vecj.append(len(face_points) + 1)
            veck.append(len(face_points) + 2)
        elif data0.shape[0] == 6:
            veci.append(len(face_points) + 0)
            vecj.append(len(face_points) + 3)
            veck.append(len(face_points) + 5)
            veci.append(len(face_points) + 3)
            vecj.append(len(face_points) + 1)
            veck.append(len(face_points) + 4)
            veci.append(len(face_points) + 5)
            vecj.append(len(face_points) + 3)
            veck.append(len(face_points) + 4)
            veci.append(len(face_points) + 5)
            vecj.append(len(face_points) + 4)
            veck.append(len(face_points) + 2)
        elif data0.shape[0] == 4:
            veci.append(len(face_points) + 0)
            veci.append(len(face_points) + 0)
            vecj.append(len(face_points) + 1)
            vecj.append(len(face_points) + 2)
            veck.append(len(face_points) + 2)
            veck.append(len(face_points) + 3)
            # i, j, k = [0, 0], [1, 2], [2, 3]
        elif data0.shape[0] == 8:
            veci.append(len(face_points) + 0)
            vecj.append(len(face_points) + 4)
            veck.append(len(face_points) + 7)
            veci.append(len(face_points) + 4)
            vecj.append(len(face_points) + 1)
            veck.append(len(face_points) + 5)
            veci.append(len(face_points) + 2)
            vecj.append(len(face_points) + 6)
            veck.append(len(face_points) + 5)
            veci.append(len(face_points) + 3)
            vecj.append(len(face_points) + 7)
            veck.append(len(face_points) + 6)
            veci.append(len(face_points) + 5)
            vecj.append(len(face_points) + 6)
            veck.append(len(face_points) + 7)
            veci.append(len(face_points) + 4)
            vecj.append(len(face_points) + 5)
            veck.append(len(face_points) + 7)
        face_line_points.extend(list(data))
        face_points.extend(list(data0))
    face_line_points = np.array(face_line_points)
    face_points = np.array(face_points)
    face_mid_points = np.array(face_mid_points)
    return (face_points, face_line_points, face_mid_points,
            veci, vecj, veck)


def _make_lines(points, cells):
    line_points = []
    line_mid_points = []
    for cell in cells:
        data0 = points[cell[1:], :]
        data1 = [np.NAN, np.NAN, np.NAN]
        data = np.vstack([data0, data1])
        line_points.extend(list(data))
        line_mid_points.append(np.mean(data0, axis=0))
    line_points = np.array(line_points)
    line_mid_points = np.array(line_mid_points)
    return line_points, line_mid_points


def _make_fix_node(model_info):
    fixed_dofs = model_info["FixNodeDofs"]
    fixed_coords = model_info["FixNodeCoords"]
    beam_lengths = model_info["beam_lengths"]
    if len(beam_lengths) > 0:
        s = (np.max(beam_lengths) + np.min(beam_lengths)) / 20
    else:
        s = (model_info["max_bound"] + model_info["min_bound"]) / 100
    points = []
    for coord, dof in zip(fixed_coords, fixed_dofs):
        x, y, z = coord
        if dof[0] == -1:
            points.extend([[x, y - s / 2, z], [x, y + s / 2, z],
                           [x, y + s / 2, z - s], [x, y - s / 2, z - s],
                           [x, y - s / 2, z], [np.NAN, np.NAN, np.NAN]])
        if dof[1] == -1:
            points.extend([[x - s / 2, y, z], [x + s / 2, y, z],
                           [x + s / 2, y, z - s], [x - s / 2, y, z - s],
                           [x - s / 2, y, z], [np.NAN, np.NAN, np.NAN]])
        if dof[2] == -1:
            points.extend([[x - s / 2, y - s / 2, z - s / 2], [x + s / 2, y - s / 2, z - s / 2],
                           [x + s / 2, y + s / 2, z - s / 2], [x -
                                                               s / 2, y + s / 2, z - s / 2],
                           [x - s / 2, y - s / 2, z - s / 2], [np.NAN, np.NAN, np.NAN]])
    points = np.array(points)
    return points


def _model_vis(
        obj,
        input_file: str = "ModelData.hdf5",
        show_node_label: bool = False,
        show_ele_label: bool = False,
        show_local_crd: bool = False,
        show_fix_node: bool = True,
        show_constrain_dof: bool = False,
        label_size: float = 8,
        show_outline: bool = True,
        opacity: float = 1.0,
        save_html: str = 'ModelVis.html'
):
    # read hdf5 file
    # -------------------------------------------
    filename = obj.out_dir + '/' + input_file
    model_info = dict()
    cells = dict()
    with h5py.File(filename, "r") as f:
        grp1 = f["ModelInfo"]
        for name in grp1.keys():
            model_info[name] = grp1[name][...]
        grp2 = f["Cell"]
        for name in grp2.keys():
            cells[name] = grp2[name][...]
    for name, value in cells.items():
        cells[name] = _reshape_cell(value)
    fig = _plot_model(obj, model_info, cells,
                      show_node_label=show_node_label,
                      show_ele_label=show_ele_label,
                      show_local_crd=show_local_crd,
                      show_fix_node=show_fix_node,
                      show_constrain_dof=show_constrain_dof,
                      label_size=label_size,
                      show_outline=show_outline,
                      opacity=opacity)
    if save_html:
        if not save_html.endswith(".html"):
            save_html += ".html"
        pio.write_html(fig, file=save_html, auto_open=True)
    if obj.notebook:
        fig.show()


def _plot_model(obj, model_info, cells,
                show_node_label: bool = False,
                show_ele_label: bool = False,
                show_local_crd: bool = False,
                show_fix_node: bool = True,
                show_constrain_dof: bool = False,
                label_size: float = 8,
                show_outline: bool = True,
                opacity: float = 1.0,):
    fig = go.Figure()
    plotter = []
    points_no_deform = model_info["coord_no_deform"]
    # >>> face plot
    face_cells = [cells["plane"], cells["tetrahedron"], cells["brick"]]
    face_cells_tags = [cells["plane_tags"],
                       cells["tetrahedron_tags"], cells["brick_tags"]]
    face_colors = [obj.color_face, obj.color_solid, obj.color_solid]
    names = ["plane", "tetrahedron", "brick"]
    for ii in range(len(face_cells)):
        if len(face_cells[ii]) > 0:
            (face_points, face_line_points, face_mid_points,
             veci, vecj, veck) = _make_faces(points_no_deform, face_cells[ii])
            x, y, z = face_points[:, 0], face_points[:, 1], face_points[:, 2]
            plotter.append(go.Mesh3d(x=x, y=y, z=z, i=veci, j=vecj, k=veck,
                                     name=names[ii], color=face_colors[ii],
                                     opacity=opacity, hoverinfo="skip"))
            x, y, z = [face_line_points[:, j] for j in range(3)]
            plotter.append(go.Scatter3d(x=x, y=y, z=z,
                                        line=dict(color="black",
                                                  width=obj.line_width / 2),
                                        mode="lines", name=names[ii],
                                        connectgaps=False, hoverinfo="skip"))
            x, y, z = [face_mid_points[:, j] for j in range(3)]
            plotter.append(
                go.Scatter3d(x=x, y=y, z=z,
                             marker=dict(size=obj.point_size, color=face_colors[ii],
                                         symbol='circle-open'),
                             mode="markers", name=names[ii],
                             customdata=face_cells_tags[ii],
                             hovertemplate='<b>tag: %{customdata}</b>'))
    # >>> line plot
    line_cells = [cells["truss"], cells["link"],
                  cells["beam"], cells["other_line"]]
    line_cells_tags = [cells["truss_tags"], cells["link_tags"],
                       cells["beam_tags"], cells["other_line_tags"]]
    line_colors = [obj.color_truss, obj.color_link,
                   obj.color_line, obj.color_line]
    line_widths = [obj.line_width, 0.5 * obj.line_width,
                   obj.line_width, obj.line_width]
    names = ["truss", "link", "beam", "other_line"]
    for i in range(len(line_cells)):
        if len(line_cells[i]) > 0:
            line_points, line_mid_points = _make_lines(
                points_no_deform, line_cells[i])
            x, y, z = line_points[:, 0], line_points[:, 1], line_points[:, 2]
            plotter.append(go.Scatter3d(x=x, y=y, z=z,
                                        line=dict(
                                            color=line_colors[i], width=line_widths[i]),
                                        mode="lines", name=names[i],
                                        connectgaps=False, hoverinfo="skip"))
            x, y, z = [line_mid_points[:, j] for j in range(3)]  # hover label
            plotter.append(go.Scatter3d(x=x, y=y, z=z,
                                        marker=dict(size=obj.point_size, color=line_colors[i],
                                                    symbol='circle-open'),
                                        mode="markers", name=names[i],
                                        customdata=line_cells_tags[i],
                                        hovertemplate='<b>tag: %{customdata}</b>'))
    # point plot
    node_labels = [str(i) for i in model_info["NodeTags"]]
    x, y, z = [points_no_deform[:, j] for j in range(3)]
    plotter.append(go.Scatter3d(x=x, y=y, z=z,
                                marker=dict(size=obj.point_size,
                                            color=obj.color_point),
                                mode="markers", name="Node", customdata=node_labels,
                                hovertemplate='<b>x: %{x}</b><br>y: %{y}<br>z: %{z} <br>tag: %{customdata}'))

    if show_node_label:
        txt_plot = go.Scatter3d(x=x, y=y, z=z, text=node_labels,
                                textfont=dict(color="#6e750e",
                                              size=label_size),
                                mode="text", name="Node Label")
        plotter.append(txt_plot)

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
        plotter.append(txt_plot)

    if show_fix_node:
        fix_points = _make_fix_node(model_info)
        if len(fix_points) > 0:
            x, y, z = fix_points[:, 0], fix_points[:, 1], fix_points[:, 2]
            fix_plot = go.Scatter3d(x=x, y=y, z=z,
                                    line=dict(color="#01ff07", width=2),
                                    mode="lines", connectgaps=False, hoverinfo="skip")
            plotter.append(fix_plot)
        else:
            warnings.warn("Model has no fix nodes!")

    # local axes
    if show_local_crd:
        beam_midpoints = model_info["beam_midpoints"]
        beam_lengths = model_info["beam_lengths"]
        if len(beam_midpoints) > 0:
            beam_xlocal = model_info["beam_xlocal"]
            beam_ylocal = model_info["beam_ylocal"]
            beam_zlocal = model_info["beam_zlocal"]
            length = (np.max(beam_lengths) + np.min(beam_lengths)) / 20
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
                line=dict(color="#cf6275", width=obj.line_width * 1.5),
                mode="lines",
                connectgaps=False,
                name='',
                # customdata=['x'] * n_beam,
                hovertemplate='<b>x</b>')
            plotter2 = go.Scatter3d(
                x=localy_points[:, 0],
                y=localy_points[:, 1],
                z=localy_points[:, 2],
                line=dict(color="#04d8b2", width=obj.line_width * 1.5),
                mode="lines",
                connectgaps=False,
                name='',
                hovertemplate='<b>y</b>')
            plotter3 = go.Scatter3d(
                x=localz_points[:, 0],
                y=localz_points[:, 1],
                z=localz_points[:, 2],
                line=dict(color="#9aae07", width=obj.line_width * 1.5),
                mode="lines",
                connectgaps=False,
                name='',
                hovertemplate='<b>z</b>')
            plotter.extend([plotter1, plotter2, plotter3])
        else:
            warnings.warn(
                "Model has no frame elements when show_local_crd=True!")
        # link axes
        link_midpoints = model_info["link_midpoints"]
        link_lengths = model_info["link_lengths"]
        if len(link_midpoints) > 0:
            link_xlocal = model_info["link_xlocal"]
            link_ylocal = model_info["link_ylocal"]
            link_zlocal = model_info["link_zlocal"]
            length = (np.max(link_lengths) + np.min(link_lengths)) / 6
            xcoords = link_midpoints + length * link_xlocal
            ycoords = link_midpoints + length * link_ylocal
            zcoords = link_midpoints + length * link_zlocal
            localx_points = []
            localy_points = []
            localz_points = []
            for i, midpoints in enumerate(link_midpoints):
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
                line=dict(color="#cf6275", width=obj.line_width * 1.5),
                mode="lines",
                connectgaps=False,
                name='',
                # customdata=['x'] * n_beam,
                hovertemplate='<b>x</b>')
            plotter2 = go.Scatter3d(
                x=localy_points[:, 0],
                y=localy_points[:, 1],
                z=localy_points[:, 2],
                line=dict(color="#04d8b2", width=obj.line_width * 1.5),
                mode="lines",
                connectgaps=False,
                name='',
                hovertemplate='<b>y</b>')
            plotter3 = go.Scatter3d(
                x=localz_points[:, 0],
                y=localz_points[:, 1],
                z=localz_points[:, 2],
                line=dict(color="#9aae07", width=obj.line_width * 1.5),
                mode="lines",
                connectgaps=False,
                name='',
                hovertemplate='<b>z</b>')
            plotter.extend([plotter1, plotter2, plotter3])
    # mp constraint lines
    _show_mp_constraint(obj, plotter, model_info, show_constrain_dof)

    fig.add_traces(plotter)

    if np.max(np.abs(points_no_deform[:, -1])) < 1e-6:
        eye = dict(x=0., y=-0.1, z=10)  # for 2D camera
        scene = dict(camera=dict(
            eye=eye, projection=dict(type="orthographic")))
    else:
        eye = dict(x=-3.5, y=-3.5, z=3.5)  # for 3D camera
        scene = dict(aspectratio=dict(x=1, y=1, z=1), aspectmode="data",
                     camera=dict(eye=eye, projection=dict(type="orthographic")))

    fig.update_layout(
        template=obj.theme,
        autosize=True,
        showlegend=False,
        scene=scene,
        title=dict(font=dict(family="courier", color='black', size=25),
                   text=("<b>OpenSeesPy 3D View</b> <br>"
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
    return fig


def _show_mp_constraint(obj, plotter, model_info, show_dofs):
    points = model_info["ConstrainedCoords"]
    cells = model_info["ConstrainedCells"]
    cells = _reshape_cell(cells)
    dofs = model_info["ConstrainedDofs"]
    dofs = ["".join([str(k) for k in dof if k != -1]) for dof in dofs]
    if len(cells) > 0:
        line_points, line_mid_points = _make_lines(points, cells)
        x, y, z = line_points[:, 0], line_points[:, 1], line_points[:, 2]
        plotter.append(go.Scatter3d(x=x, y=y, z=z,
                                    line=dict(
                                        color=obj.color_constraint,
                                        width=obj.line_width / 3),
                                    mode="lines", name="mp constraint",
                                    connectgaps=False, hoverinfo="skip"))
        if show_dofs:
            x, y, z = [line_mid_points[:, j] for j in range(3)]
            txt_plot = go.Scatter3d(x=x, y=y, z=z, text=dofs,
                                    textfont=dict(color=obj.color_constraint,
                                                  size=12),
                                    mode="text", name="constraint dofs")
            plotter.append(txt_plot)


def _eigen_vis(
        obj,
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
    # read
    filename = obj.out_dir + '/' + input_file
    eigen_data = dict()
    with h5py.File(filename, "r") as f:
        grp = f["EigenInfo"]
        for name, value in grp.items():
            eigen_data[name] = value[...]
    eigen_data["all_lines"] = _reshape_cell(eigen_data["all_lines"])
    eigen_data["all_faces"] = _reshape_cell(eigen_data["all_faces"])

    f = eigen_data["f"]
    eigenvector = eigen_data["eigenvector"]
    num_mode_tag = len(f)
    modei, modej = mode_tags
    modei, modej = int(modei), int(modej)
    if modej > num_mode_tag:
        raise ValueError(
            f"Insufficient number of modes in eigen file {filename}!")

    fig = go.Figure()
    title = dict(font=dict(family="courier", color='black', size=25),
                 text="<b>OpenSeesPy Eigen 3D View</b>"
                 )
    if show_outline:
        off_axis = {'showgrid': True, 'zeroline': True, 'visible': True}
    else:
        off_axis = {'showgrid': False, 'zeroline': False, 'visible': False}

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
                value_ = np.max(np.sqrt(np.sum(eigen_vec ** 2, axis=1)))
                alpha_ = (
                    eigen_data["max_bound"] / obj.bound_fact / value_
                )
            else:
                alpha_ = alpha
            eigen_points = eigen_data["coord_no_deform"] + eigen_vec * alpha_
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
                                         point_size=obj.point_size,
                                         line_width=obj.line_width,
                                         show_face_line=show_face_line)
            fig.add_traces(plotter, rows=idxi + 1, cols=idxj + 1)
        if np.max(np.abs(eigen_data["coord_no_deform"][:, -1])) < 1e-8:
            eye = dict(x=0., y=-0.1, z=10)  # for 2D camera
            scene = dict(camera=dict(
                eye=eye, projection=dict(type="orthographic")),
                xaxis=off_axis, yaxis=off_axis, zaxis=off_axis)
        else:
            eye = dict(x=-3.5, y=-3.5, z=3.5)  # for 3D camera
            scene = dict(aspectratio=dict(x=1, y=1, z=1), aspectmode="data",
                         camera=dict(eye=eye, projection=dict(
                             type="orthographic")),
                         xaxis=off_axis, yaxis=off_axis, zaxis=off_axis)
        scenes = dict()
        coloraxiss = dict()
        for k in range(shape[0] * shape[1]):
            coloraxiss[f"coloraxis{k + 1}"] = dict(
                showscale=False, colorscale=obj.color_map)
            if k >= 1:
                if np.max(np.abs(eigen_data["coord_no_deform"][:, -1])) < 1e-8:
                    scenes[f"scene{k + 1}"] = dict(camera=dict(eye=eye,
                                                               projection=dict(type="orthographic")),
                                                   xaxis=off_axis, yaxis=off_axis, zaxis=off_axis)
                else:
                    scenes[f"scene{k + 1}"] = dict(aspectratio=dict(x=1, y=1, z=1), aspectmode="data",
                                                   camera=dict(eye=eye,
                                                               projection=dict(type="orthographic")),
                                                   xaxis=off_axis, yaxis=off_axis, zaxis=off_axis)
        fig.update_layout(
            title=title,
            template=obj.theme,
            autosize=True,
            showlegend=False,
            coloraxis=dict(showscale=False, colorscale=obj.color_map),
            scene=scene,
            **scenes,
            **coloraxiss
        )
    # !slider style
    else:
        n_data = None
        cmins = []
        cmaxs = []
        for i, idx in enumerate(range(modei, modej + 1)):
            step = idx - 1
            eigen_vec = eigenvector[step]
            if alpha is None:
                value_ = np.max(np.sqrt(np.sum(eigen_vec ** 2, axis=1)))
                alpha_ = (
                    eigen_data["max_bound"] / obj.bound_fact / value_
                )
            else:
                alpha_ = alpha
            eigen_points = eigen_data["coord_no_deform"] + eigen_vec * alpha_
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
                                         coloraxis=f"coloraxis{i + 1}",
                                         points_origin=points_origin,
                                         point_size=obj.point_size, line_width=obj.line_width,
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
            coloraxiss[f"coloraxis{i + 1}"] = dict(colorscale=obj.color_map,
                                                   cmin=cmins[i],
                                                   cmax=cmaxs[i],
                                                   colorbar=dict(tickfont=dict(size=15)))

        if np.max(np.abs(eigen_data["coord_no_deform"][:, -1])) < 1e-8:
            eye = dict(x=0., y=-0.1, z=10)  # for 2D camera
            scene = dict(camera=dict(
                eye=eye, projection=dict(type="orthographic")),
                xaxis=off_axis, yaxis=off_axis, zaxis=off_axis)
        else:
            eye = dict(x=-3.5, y=-3.5, z=3.5)  # for 3D camera
            scene = dict(aspectratio=dict(x=1, y=1, z=1), aspectmode="data",
                         camera=dict(eye=eye, projection=dict(
                             type="orthographic")),
                         xaxis=off_axis, yaxis=off_axis, zaxis=off_axis)
        fig.update_layout(
            template=obj.theme,
            autosize=True,
            showlegend=False,
            scene=scene,
            title=title,
            sliders=sliders,
            **coloraxiss
        )
    if save_html:
        if not save_html.endswith(".html"):
            save_html += ".html"
        pio.write_html(fig, file=save_html, auto_open=True)
    if obj.notebook:
        fig.show()


def _eigen_anim(
        obj,
        mode_tag: int = 1,
        input_file: str = 'EigenData.hdf5',
        n_cycle: int = 5,
        alpha: float = None,
        show_outline: bool = False,
        opacity: float = 1,
        framerate: int = 3,
        show_face_line: bool = True,
        save_html: str = "EigenAnimation"
):
    filename = obj.out_dir + '/' + input_file
    eigen_data = dict()
    with h5py.File(filename, "r") as f:
        grp = f["EigenInfo"]
        for name, value in grp.items():
            eigen_data[name] = value[...]
    eigen_data["all_lines"] = _reshape_cell(eigen_data["all_lines"])
    eigen_data["all_faces"] = _reshape_cell(eigen_data["all_faces"])

    f = eigen_data["f"]
    eigenvector = eigen_data["eigenvector"]
    num_mode_tag = len(f)
    if mode_tag > num_mode_tag:
        raise ValueError("Insufficient number of modes in open file")
    eigen_vec = eigenvector[mode_tag - 1]
    f_ = f[mode_tag - 1]
    if alpha is None:
        value_ = np.max(np.sqrt(np.sum(eigen_vec ** 2, axis=1)))
        alpha_ = (
            eigen_data["max_bound"] / obj.bound_fact / value_
        )
    else:
        alpha_ = alpha
    eigen_points = eigen_data["coord_no_deform"] + eigen_vec * alpha_
    anti_eigen_points = eigen_data["coord_no_deform"] - eigen_vec * alpha_
    scalars = np.sqrt(np.sum(eigen_vec ** 2, axis=1))
    plt_points = [anti_eigen_points,
                  eigen_data["coord_no_deform"], eigen_points]
    index = [1] + [2, 0] * n_cycle
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
                                     point_size=obj.point_size, line_width=obj.line_width,
                                     opacity=opacity,
                                     lines_cells=eigen_data["all_lines"],
                                     face_cells=eigen_data["all_faces"],
                                     coloraxis="coloraxis",
                                     show_face_line=show_face_line)
        frames.append(go.Frame(data=plotter, name="step:" + str(k + 1)))

    fig = go.Figure(frames=frames)
    # Add data to be displayed before animation starts
    plotter0 = _generate_all_mesh(points=plt_points[index[0]], scalars=scalars * 0,
                                  point_size=obj.point_size, line_width=obj.line_width,
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
    if np.max(np.abs(eigen_data["coord_no_deform"][:, -1])) < 1e-8:
        eye = dict(x=0., y=-0.1, z=10)  # for 2D camera
        scene = dict(camera=dict(
            eye=eye, projection=dict(type="orthographic")))
    else:
        eye = dict(x=-3.5, y=-3.5, z=3.5)  # for 3D camera
        scene = dict(aspectratio=dict(x=1, y=1, z=1), aspectmode="data",
                     camera=dict(eye=eye, projection=dict(
                         type="orthographic")))
    txt = "<br> Mode {}: T = {:.3f} s".format(mode_tag, 1 / f_)
    fig.update_layout(
        title=dict(font=dict(family="courier", color='black', size=25),
                   text="<b>OpenSeesPy Eigen 3D View</b>" + txt
                   ),
        template=obj.theme,
        autosize=True,
        showlegend=False,
        coloraxis=dict(colorscale=obj.color_map,
                       colorbar=dict(tickfont=dict(size=15))),
        scene=scene,
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
    if obj.notebook:
        fig.show()


def _react_vis(obj,
               input_file: str = "NodeReactionStepData-1.hdf5",
               slider: bool = False,
               direction: str = "Fz",
               show_values: bool = True,
               show_outline: bool = False,
               save_html: str = "ReactionVis"):
    direct = direction.lower()
    if direct not in ['fx', 'fy', 'fz', 'mx', 'my', 'mz']:
        raise ValueError(
            "response must be one of ['Fx', 'Fy', 'Fz', 'Mx', 'My', 'Mz']!")
    filename = obj.out_dir + '/' + input_file
    node_react_steps = []
    with h5py.File(filename, "r") as f:
        Nsteps = int(f["Nsteps"][...])
        node_coords = f["NodeReactCoords"][...]
        model_dims = f['model_dims'][...]
        NodeTags = f["NodeReactTags"][...]
        num_nodes = node_coords.shape[0]
        grp = f["NodeReactSteps"]
        for i in range(Nsteps):
            node_react_steps.append(grp[f"step{i + 1}"][...])
    if np.max(model_dims) < 3:
        D2 = True
    else:
        D2 = False
    x, y, z = [node_coords[:, j] for j in range(3)]
    max_bound = np.max(np.max(node_coords, axis=0) -
                       np.min(node_coords, axis=0))
    axis_dict = dict(fx=(1, 0., 0.), fy=(0., 1, 0.), fz=(0., 0., 1),
                     mx=(1, 0., 0.), my=(0., 1, 0.), mz=(0., 0., 1))
    color_dict = dict(fx="#d20962", fy="#f47721", fz="#7ac143",
                      mx="#00a78e", my="#00bce4", mz="#7d3f98")
    if D2:
        reactidx_dict = dict(fx=0, fy=1, fz=None, mx=None, my=None, mz=2)
    else:
        reactidx_dict = dict(fx=0, fy=1, fz=2, mx=3, my=4, mz=5)

    fig = go.Figure()

    def creat_plot(step):
        f = node_react_steps[step][:, reactidx_dict[direct]]
        idxmax, idxmin = np.argmax(f), np.argmin(f)
        # point plot
        labels = [
            f"<b>tag: {tag}</b><br>{direction}: {fi:.3E}" for tag, fi in zip(NodeTags, f)]
        point_plot = go.Scatter3d(x=x, y=y, z=z,
                                  marker=dict(size=obj.point_size,
                                              color=obj.color_point),
                                  mode="markers", name="Node Reactions",
                                  customdata=labels,
                                  hovertemplate='%{customdata}')
        fig.add_trace(point_plot)
        if show_values:
            labels = [f"{fi:.3E}" for fi in f]
            txt_plot = go.Scatter3d(x=x, y=y, z=z, text=labels,
                                    textfont=dict(color="#6e750e",
                                                  size=10),
                                    mode="text", hoverinfo='skip',)
            fig.add_trace(txt_plot)
        # max min point plot
        labels = [
            f"<b>tag: {NodeTags[idx]}</b><br>{direction}: {f[idx]:.3E}" for idx in [idxmax, idxmin]]
        point_plot2 = go.Scatter3d(x=x[[idxmax, idxmin]], y=y[[idxmax, idxmin]], z=z[[idxmax, idxmin]],
                                   marker=dict(size=obj.point_size * 1.25,
                                               color=obj.color_point,
                                               symbol=['x'] * 2),
                                   mode="markers", name="Node Reactions",
                                   customdata=labels,
                                   hovertemplate='%{customdata}')
        fig.add_trace(point_plot2)
        # line plot
        line_ends = np.zeros_like(node_coords)
        for i in range(num_nodes):
            line_ends[i] = node_coords[i] - \
                np.array(axis_dict[direct]) * \
                max_bound / 30 * np.sign(f[i])
        line_points = []
        line_cells = []
        for point1, point2 in zip(node_coords, line_ends):
            line_points.extend([point2, point1])
            line_cells.extend([2, len(line_points)-2, len(line_points)-1])
        line_cells = np.reshape(line_cells, (-1, 3))
        line_plot = _generate_line_mesh(points=line_points, cells=line_cells,
                                        line_width=obj.line_width * 2, color=color_dict[direct])
        fig.add_traces(line_plot)
        arrow_plot = _creat_arrows(points=line_points, cells=line_cells,
                                   color=color_dict[direct])
        fig.add_traces(arrow_plot)

    if slider:
        n_data = None
        for step in range(Nsteps):
            creat_plot(step)
            if step == 0:
                n_data = len(fig.data)

        for i in range(0, len(fig.data) - n_data):
            fig.data[i].visible = False
        # ! Create and add slider
        steps = []
        for i in range(Nsteps):
            f = node_react_steps[i][:, reactidx_dict[direct]]
            idxmax, idxmin = np.argmax(f), np.argmin(f)
            txt = (f"<b>Step {i + 1} {direction}</b>"
                   f"<br>max={f[idxmax]:.3E} | nodeTag={NodeTags[idxmax]}"
                   f"<br>min={f[idxmin]:.3E} | nodeTag={NodeTags[idxmin]}")
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
            active=Nsteps,
            currentvalue={"prefix": "Step: "},
            pad={"t": 50},
            steps=steps
        )]
        if D2:
            eye = dict(x=0., y=-0.1, z=10)  # for 2D camera
            scene = dict(camera=dict(
                eye=eye, projection=dict(type="orthographic")))
        else:
            eye = dict(x=-3.5, y=-3.5, z=3.5)  # for 3D camera
            scene = dict(aspectratio=dict(x=1, y=1, z=1), aspectmode="data",
                         camera=dict(eye=eye, projection=dict(
                             type="orthographic")))
        fig.update_layout(
            template=obj.theme,
            autosize=True,
            showlegend=False,
            scene=scene,  # orthographic,perspective
            title=dict(font=dict(family="courier", color='black', size=25),
                       text=f"<b>OpenSeesPy Node Reactions View</b>"
                       ),
            sliders=sliders,
        )
    else:  # a sing step
        idx = np.argmax([np.max(np.abs(react[:, reactidx_dict[direct]]))
                        for react in node_react_steps])
        creat_plot(idx)
        f = node_react_steps[idx][:, reactidx_dict[direct]]
        idxmax, idxmin = np.argmax(f), np.argmin(f)
        txt = (f"<b>OpenSeesPy Node Reactions View</b>"
               f"<br>Step {i + 1} {direction}"
               f"<br>max={f[idxmax]:.3E} | nodeTag={NodeTags[idxmax]}"
               f"<br>min={f[idxmin]:.3E} | nodeTag={NodeTags[idxmin]}")
        if D2:
            eye = dict(x=0., y=-0.1, z=10)  # for 2D camera
            scene = dict(camera=dict(
                eye=eye, projection=dict(type="orthographic")))
        else:
            eye = dict(x=-3.5, y=-3.5, z=3.5)  # for 3D camera
            scene = dict(aspectratio=dict(x=1, y=1, z=1), aspectmode="data",
                         camera=dict(eye=eye, projection=dict(
                             type="orthographic")))
        fig.update_layout(
            template=obj.theme,
            autosize=True,
            showlegend=False,
            scene=scene,  # orthographic,perspective
            title=dict(font=dict(family="courier", color='black', size=25),
                       text=txt
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
    if obj.notebook:
        fig.show()


def _deform_vis(
        obj,
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
    resp_type = response.lower()
    if resp_type not in ['disp', 'vel', 'accel']:
        raise ValueError("response must be 'disp', 'vel', or 'accel'!")
    # ------------------------------------------------
    filename = obj.out_dir + '/' + input_file
    model_info_steps = dict()
    cell_steps = dict()
    node_resp_steps = dict()
    with h5py.File(filename, "r") as f:
        n = int(f["Nsteps"][...])
        grp1 = f["ModelInfoSteps"]
        grp2 = f["CellSteps"]
        if model_update:
            for name, value_ in grp1.items():
                temp = []
                for i in range(n):
                    temp.append(value_[f"step{i + 1}"][...])
                model_info_steps[name] = temp
            for name, value_ in grp2.items():
                temp = []
                for i in range(n):
                    temp.append(value_[f"step{i + 1}"][...])
                cell_steps[name] = temp
        else:
            for name, value_ in grp1.items():
                model_info_steps[name] = value_[...]
            for name, value_ in grp2.items():
                cell_steps[name] = value_[...]
        grp3 = f["NodeRespSteps"]
        for name, value_ in grp3.items():
            temp = []
            for i in range(n):
                temp.append(value_[f"step{i + 1}"][...])
            node_resp_steps[name] = temp

    num_steps = len(node_resp_steps["disp"])
    # ! max response
    max_resps = [np.max(np.sqrt(np.sum(resp_ ** 2, axis=1)))
                 for resp_ in node_resp_steps[resp_type]]
    max_step = np.argmax(max_resps)
    max_node_resp = node_resp_steps[resp_type][max_step]
    scalars = np.sqrt(np.sum(max_node_resp ** 2, axis=1))
    data = node_resp_steps[resp_type]
    cmin, cmax = np.min(scalars), np.max(scalars)
    if model_update:
        bounds = model_info_steps["bound"][0]
        model_dims = model_info_steps["model_dims"][0]
    else:
        bounds = model_info_steps["bound"]
        model_dims = model_info_steps["model_dims"]
    # scale factor
    if resp_type == "disp":
        if alpha is None:
            max_bound = np.max(
                [bounds[1] - bounds[0], bounds[3] - bounds[2], bounds[5] - bounds[4]])
            value = np.max(np.sqrt(np.sum(max_node_resp ** 2, axis=1)))
            alpha_ = max_bound / obj.bound_fact / value
        else:
            alpha_ = alpha
    else:
        alpha_ = 0
    # ------------------------------------------------------------------------
    fig = go.Figure()
    # -------------------------------------------------------------------------
    if slider:
        n_data = None
        for step in range(num_steps):
            if model_update:
                node_nodeform_coords = model_info_steps["coord_no_deform"][step]
                lines_cells = _reshape_cell(cell_steps["all_lines"][step])
                faces_cells = _reshape_cell(cell_steps["all_faces"][step])
            else:
                node_nodeform_coords = model_info_steps["coord_no_deform"]
                lines_cells = _reshape_cell(cell_steps["all_lines"])
                faces_cells = _reshape_cell(cell_steps["all_faces"])
            node_resp = node_resp_steps[resp_type][step]
            node_deform_coords = alpha_ * node_resp + node_nodeform_coords
            if show_origin:
                points_origin = node_nodeform_coords
            else:
                points_origin = None
            scalars = np.sqrt(np.sum(node_resp ** 2, axis=1))
            plotter = _generate_all_mesh(points=node_deform_coords, scalars=scalars,
                                         point_size=obj.point_size, line_width=obj.line_width,
                                         opacity=opacity,
                                         lines_cells=lines_cells,
                                         face_cells=faces_cells,
                                         coloraxis=f"coloraxis{step + 1}",
                                         points_origin=points_origin,
                                         show_face_line=show_face_line)
            fig.add_traces(plotter)
            if step == 0:
                n_data = len(fig.data)
        for i in range(0, len(fig.data) - n_data):
            fig.data[i].visible = False
        # ! Create and add slider
        steps = []
        for i in range(num_steps):
            maxx, maxy, maxz = np.max(data[i], axis=0)
            minx, miny, minz = np.min(data[i], axis=0)
            txt = (f"<b>Step {i + 1} {response}</b>"
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
            coloraxiss[f"coloraxis{i + 1}"] = dict(colorscale=obj.color_map,
                                                   cmin=cmin,
                                                   cmax=cmax,
                                                   colorbar=dict(tickfont=dict(size=15)))
        if np.max(model_dims) <= 2:
            eye = dict(x=0., y=-0.1, z=10)  # for 2D camera
            scene = dict(camera=dict(
                eye=eye, projection=dict(type="orthographic")))
        else:
            eye = dict(x=-3.5, y=-3.5, z=3.5)  # for 3D camera
            scene = dict(aspectratio=dict(x=1, y=1, z=1), aspectmode="data",
                         camera=dict(eye=eye, projection=dict(
                             type="orthographic")))
        fig.update_layout(
            template=obj.theme,
            autosize=True,
            showlegend=False,
            scene=scene,  # orthographic,perspective
            title=dict(font=dict(family="courier", color='black', size=25),
                       text="<b>OpenSeesPy Deformation 3D View</b>"
                       ),
            sliders=sliders,
            **coloraxiss
        )
    # -------------------------------------------------------------------------
    else:  # plot a single step
        step = max_step
        if model_update:
            node_nodeform_coords = model_info_steps["coord_no_deform"][step]
            lines_cells = _reshape_cell(cell_steps["all_lines"][step])
            faces_cells = _reshape_cell(cell_steps["all_faces"][step])
        else:
            node_nodeform_coords = model_info_steps["coord_no_deform"]
            lines_cells = _reshape_cell(cell_steps["all_lines"])
            faces_cells = _reshape_cell(cell_steps["all_faces"])
        node_resp = node_resp_steps[resp_type][step]
        node_deform_coords = alpha_ * node_resp + node_nodeform_coords
        if show_origin:
            points_origin = node_nodeform_coords
        else:
            points_origin = None
        scalars = np.sqrt(np.sum(node_resp ** 2, axis=1))
        plotter = _generate_all_mesh(points=node_deform_coords, scalars=scalars,
                                     point_size=obj.point_size, line_width=obj.line_width,
                                     opacity=opacity,
                                     lines_cells=lines_cells,
                                     face_cells=faces_cells,
                                     coloraxis="coloraxis",
                                     points_origin=points_origin,
                                     show_face_line=show_face_line)
        fig.add_traces(plotter)
        if np.max(np.abs(node_deform_coords[:, -1])) < 1e-5:
            eye = dict(x=0., y=-0.1, z=10)  # for 2D camera
            scene = dict(camera=dict(
                eye=eye, projection=dict(type="orthographic")))
        else:
            eye = dict(x=-3.5, y=-3.5, z=3.5)  # for 3D camera
            scene = dict(aspectratio=dict(x=1, y=1, z=1), aspectmode="data",
                         camera=dict(eye=eye, projection=dict(
                             type="orthographic")))
        maxx, maxy, maxz = np.max(node_resp, axis=0)
        minx, miny, minz = np.min(node_resp, axis=0)
        txt = (f"<br>Step {max_step + 1} {response}"
               f"<br>max.x={maxx:.2E} | min.x={minx:.2E}"
               f"<br>max.y={maxy:.2E} | min.y={miny:.2E}"
               f"<br>max.z={maxz:.2E} | min.z={minz:.2E}")
        fig.update_layout(
            template=obj.theme,
            autosize=True,
            showlegend=False,
            scene=scene,
            coloraxis=dict(colorscale=obj.color_map, cmin=cmin, cmax=cmax,
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
    if obj.notebook:
        fig.show()


def _deform_anim(
        obj,
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
    resp_type = response.lower()
    if resp_type not in ['disp', 'vel', 'accel']:
        raise ValueError("response must be 'disp', 'vel', or 'accel'!")
    filename = obj.out_dir + '/' + input_file
    model_info_steps = dict()
    cell_steps = dict()
    node_resp_steps = dict()
    with h5py.File(filename, "r") as f:
        n = int(f["Nsteps"][...])
        grp1 = f["ModelInfoSteps"]
        grp2 = f["CellSteps"]
        if model_update:
            for name, value_ in grp1.items():
                temp = []
                for i in range(n):
                    temp.append(value_[f"step{i + 1}"][...])
                model_info_steps[name] = temp
            for name, value_ in grp2.items():
                temp = []
                for i in range(n):
                    temp.append(value_[f"step{i + 1}"][...])
                cell_steps[name] = temp
        else:
            for name, value_ in grp1.items():
                model_info_steps[name] = value_[...]
            for name, value_ in grp2.items():
                cell_steps[name] = value_[...]
        grp3 = f["NodeRespSteps"]
        for name, value_ in grp3.items():
            temp = []
            for i in range(n):
                temp.append(value_[f"step{i + 1}"][...])
            node_resp_steps[name] = temp

    num_steps = len(node_resp_steps["disp"])
    times = int(num_steps / framerate)

    # ! max response
    max_resps = [np.max(np.sqrt(np.sum(resp_ ** 2, axis=1)))
                 for resp_ in node_resp_steps[resp_type]]
    max_step = np.argmax(max_resps)
    max_node_resp = node_resp_steps[resp_type][max_step]
    scalars = np.sqrt(np.sum(max_node_resp ** 2, axis=1))
    data = node_resp_steps[resp_type]
    cmin, cmax = np.min(scalars), np.max(scalars)
    if model_update:
        bounds = model_info_steps["bound"][0]
        model_dims = model_info_steps["model_dims"][0]
    else:
        bounds = model_info_steps["bound"]
        model_dims = model_info_steps["model_dims"]
    # scale factor
    if resp_type == "disp":
        if alpha is None:
            max_bound = np.max(
                [bounds[1] - bounds[0], bounds[3] - bounds[2], bounds[5] - bounds[4]])
            value = np.max(np.sqrt(np.sum(max_node_resp ** 2, axis=1)))
            alpha_ = max_bound / obj.bound_fact / value
        else:
            alpha_ = alpha
    else:
        alpha_ = 0

    # -----------------------------------------------------------------------------
    # start plot
    def create_mesh(stepi):
        if model_update:
            node_nodeform_coords_ = model_info_steps["coord_no_deform"][stepi]
            lines_cells_ = _reshape_cell(cell_steps["all_lines"][stepi])
            faces_cells_ = _reshape_cell(cell_steps["all_faces"][stepi])
        else:
            node_nodeform_coords_ = model_info_steps["coord_no_deform"]
            lines_cells_ = _reshape_cell(cell_steps["all_lines"])
            faces_cells_ = _reshape_cell(cell_steps["all_faces"])
        node_resp_ = node_resp_steps[resp_type][stepi]
        node_deform_coords_ = alpha_ * node_resp_ + node_nodeform_coords_
        scalars_ = np.sqrt(np.sum(node_resp_ ** 2, axis=1))
        plotter_ = _generate_all_mesh(points=node_deform_coords_, scalars=scalars_,
                                      point_size=obj.point_size, line_width=obj.line_width,
                                      opacity=opacity,
                                      lines_cells=lines_cells_,
                                      face_cells=faces_cells_,
                                      coloraxis="coloraxis",
                                      show_face_line=show_face_line)
        return plotter_

    frames = []
    for step in range(num_steps):
        plotter = create_mesh(step)
        frames.append(go.Frame(data=plotter, name="step:" + str(step + 1)))

    fig = go.Figure(frames=frames)
    # Add data to be displayed before animation starts
    plotter0 = create_mesh(num_steps - 1)
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
               f"<br>Step {i + 1} {response}"
               f"<br>max.x={maxx:.2E} | min.x={minx:.2E}"
               f"<br>max.y={maxy:.2E} | min.y={miny:.2E}"
               f"<br>max.z={maxz:.2E} | min.z={minz:.2E}")
        fig.frames[i]['layout'].update(title_text=txt)
    if np.max(model_dims) < 3:
        eye = dict(x=0., y=-0.1, z=10)  # for 2D camera
        scene = dict(camera=dict(
            eye=eye, projection=dict(type="orthographic")))
    else:
        eye = dict(x=-3.5, y=-3.5, z=3.5)  # for 3D camera
        scene = dict(aspectratio=dict(x=1, y=1, z=1), aspectmode="data",
                     camera=dict(eye=eye, projection=dict(
                         type="orthographic")))

    fig.update_layout(
        title=dict(font=dict(family="courier", color='black', size=25),
                   text="<b>OpenSeesPy Defo 3D View</b>"),
        template=obj.theme,
        autosize=True,
        showlegend=False,
        coloraxis=dict(colorscale=obj.color_map,
                       cmin=cmin,
                       cmax=cmax,
                       colorbar=dict(tickfont=dict(size=15))),
        scene=scene,
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
    if obj.notebook:
        fig.show()


def _frame_resp_vis(obj,
                    input_file: str = "BeamRespStepData-1.hdf5",
                    ele_tags: list[int] = None,
                    slider: bool = False,
                    response: str = "Mz",
                    show_values=True,
                    alpha: float = None,
                    opacity: float = 1,
                    save_html: str = "FrameRespVis"
                    ):
    filename = obj.out_dir + '/' + input_file
    beam_infos = dict()
    beam_resp_step = dict()
    with h5py.File(filename, "r") as f:
        n = int(f["Nsteps"][...])
        grp1 = f["BeamInfos"]
        for name, value_ in grp1.items():
            beam_infos[name] = value_[...]
        grp2 = f["BeamRespSteps"]
        for name, value_ in grp2.items():
            temp = []
            for i in range(n):
                temp.append(value_[f"step{i + 1}"][...])
            beam_resp_step[name] = temp

    # -------------------------------------
    beam_tags = beam_infos['beam_tags']
    if len(beam_tags) == 0:
        warnings.warn("Model has no frame elements!")
        return None
    ylocals = beam_infos['ylocal']
    zlocals = beam_infos['zlocal']
    ylocal_map = {beam_tags[i]: ylocals[i] for i in range(len(beam_tags))}
    zlocal_map = {beam_tags[i]: zlocals[i] for i in range(len(beam_tags))}
    local_forces_step = beam_resp_step['localForces']
    num_steps = len(local_forces_step)

    if ele_tags is None:
        ele_tags = beam_tags
        beam_node_coords = beam_infos['beam_node_coords']
        beam_cells = beam_infos['beam_cells']
        beam_cell_map = {beam_tags[i]: i for i in range(len(beam_tags))}
        idxs = range(len(beam_tags))
    else:
        ele_tags = np.atleast_1d(ele_tags)
        beam_node_coords = []
        beam_cells = []
        idxs = []
        beam_cell_map = {}
        for i, eletag in enumerate(ele_tags):
            idx = beam_infos['beam_cell_map'][eletag]
            idxs.append(idx)
            beam_cell_map[eletag] = i
            nodei, nodej = beam_infos['beam_cells'][idx, 1:]
            beam_node_coords.append(beam_infos['beam_node_coords'][nodei])
            beam_node_coords.append(beam_infos['beam_node_coords'][nodej])
            beam_cells.append([2, 2 * i, 2 * i + 1])
        beam_node_coords = np.array(beam_node_coords)
        beam_cells = np.array(beam_cells)

    idx_plottype_map = dict(fx=[0, 6], fy=[1, 7], fz=[2, 8],
                            my=[4, 10], mz=[5, 11], mx=[3, 9])
    f_sign_map = dict(fx=[-1, 1], fy=[-1, 1], fz=[-1, 1],
                      my=[1, -1], mz=[-1, 1], mx=[1, -1])
    axis_sign_map = dict(fx=1, fy=1, fz=1,
                         my=-1, mz=-1, mx=-1)
    axis_map_map = dict(fx=zlocal_map, fy=ylocal_map, fz=zlocal_map,
                        my=zlocal_map, mz=ylocal_map, mx=zlocal_map)
    idx_plottype = idx_plottype_map[response.lower()]
    axis_map = axis_map_map[response.lower()]
    axis_sign = axis_sign_map[response.lower()]
    local_forces_step = [data[:, idx_plottype][idxs] * np.array(f_sign_map[response.lower()])
                         for data in local_forces_step]  # new

    maxv = [np.max(np.abs(data))
            for data in local_forces_step]
    maxstep = np.argmax(maxv)
    local_forces_max = local_forces_step[maxstep]
    cmin, cmax = np.min(local_forces_max), np.max(local_forces_max)
    if alpha is None:
        max_coord = np.max(beam_node_coords, axis=0)
        min_coord = np.min(beam_node_coords, axis=0)
        max_bound = np.max(max_coord - min_coord)
        maxv = np.amax(np.abs(local_forces_max))
        alpha_ = max_bound / maxv / obj.bound_fact
    else:
        alpha_ = alpha

    # ------------------------------------------------------------------------
    fig = go.Figure()
    # -------------------------------------------------------------------------
    if slider:
        n_data = None
        for step in range(num_steps):
            local_forces = local_forces_step[step]
            local_forces_scale = local_forces * alpha_
            # add force face cells
            # TODO if values symbol versa, need trangle
            label_poins = []
            labels = []
            resp_points = []
            resp_cells = []
            scalars = []
            for i, eletag in enumerate(ele_tags):
                axis = axis_map[eletag]
                node1, node2 = beam_cells[beam_cell_map[eletag], 1:]
                coord1, coord2 = beam_node_coords[node1], beam_node_coords[node2]
                f1, f2 = local_forces_scale[beam_cell_map[eletag]]
                f1_, f2_ = local_forces[beam_cell_map[eletag]]
                coord3 = coord2 + f2 * axis * axis_sign
                coord4 = coord1 + f1 * axis * axis_sign
                label_poins.extend([coord3, coord4])
                labels.extend([f2_, f1_])
                n = len(resp_points)
                if f1 * f2 >= 0:
                    resp_points.extend([coord1, coord2, coord3, coord4])
                    resp_cells.append([4, n, n + 1, n + 2, n + 3])
                    scalars.extend([f1_, f2_, f2_, f1_])
                else:
                    ratio = np.abs(f2 / f1)
                    ratio = 1 / (ratio + 1)
                    coord0 = coord1 + (coord2 - coord1) * ratio
                    resp_points.extend(
                        [coord1, coord0, coord4, coord2, coord0, coord3])
                    resp_cells.append([3, n, n + 1, n + 2])
                    resp_cells.append([3, n + 3, n + 4, n + 5])
                    scalars.extend([f1_, 0, f1_, f2_, 0, f2_])
            labels = [f"{label:.2E}" for label in labels]
            label_poins = np.array(label_poins)
            resp_points = np.array(resp_points)
            scalars = np.array(scalars)
            # ----------------------------------------------------------------------------------------
            line_plot = _generate_line_mesh(beam_node_coords, beam_cells, line_width=obj.line_width,
                                            color="black", use_cmap=False)
            resp_plot = _generate_face_mesh(resp_points, resp_cells, show_face_line=False, opacity=opacity,
                                            use_cmap=True, scalars=scalars, coloraxis="coloraxis")
            point_plot = _generate_point_mesh(resp_points, point_size=obj.point_size / 2,
                                              use_cmap=True, hover_name=response,
                                              scalars=scalars, coloraxis="coloraxis")
            # resp_plot = _generate_line_mesh(resp_points, resp_cells, line_width=obj.line_width,
            #                                 use_cmap=True, scalars=scalars, coloraxis="coloraxis")
            fig.add_traces(line_plot + resp_plot + point_plot)
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
        for i in range(0, len(fig.data) - n_data):
            fig.data[i].visible = False
        # ! Create and add slider
        steps = []
        for i in range(num_steps):
            maxx = np.max(local_forces_step[i])
            minx = np.min(local_forces_step[i])
            txt = (f"<b>Step {i + 1} {response}</b>"
                   f"<br>max.={maxx:.2E}|min.={minx:.2E}")
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
            coloraxiss[f"coloraxis{i + 1}"] = dict(colorscale=obj.color_map,
                                                   cmin=cmin,
                                                   cmax=cmax,
                                                   colorbar=dict(tickfont=dict(size=15)))

        if np.max(np.abs(beam_node_coords[:, -1])) < 1e-5:
            eye = dict(x=0., y=-0.1, z=10)  # for 2D camera
            scene = dict(camera=dict(
                eye=eye, projection=dict(type="orthographic")))
        else:
            eye = dict(x=-3.5, y=-3.5, z=3.5)  # for 3D camera
            scene = dict(aspectratio=dict(x=1, y=1, z=1), aspectmode="data",
                         camera=dict(eye=eye, projection=dict(
                             type="orthographic")))
        fig.update_layout(
            template=obj.theme,
            autosize=True,
            showlegend=False,
            scene=scene,
            title=dict(font=dict(family="courier", color='black', size=25),
                       text="<b>OpenSeesPy Frames Response 3D View</b>"
                       ),
            sliders=sliders,
            **coloraxiss
        )
    # -------------------------------------------------------------------------
    else:  # plot a single step
        local_forces = local_forces_step[maxstep]
        local_forces_scale = local_forces * alpha_
        # add force face cells
        # TODO if values symbol versa, need trangle
        label_poins = []
        labels = []
        resp_points = []
        resp_cells = []
        scalars = []
        for i, eletag in enumerate(ele_tags):
            axis = axis_map[eletag]
            node1, node2 = beam_cells[beam_cell_map[eletag], 1:]
            coord1, coord2 = beam_node_coords[node1], beam_node_coords[node2]
            f1, f2 = local_forces_scale[beam_cell_map[eletag]]
            f1_, f2_ = local_forces[beam_cell_map[eletag]]
            coord3 = coord2 + f2 * axis * axis_sign
            coord4 = coord1 + f1 * axis * axis_sign
            label_poins.extend([coord3, coord4])
            labels.extend([f2_, f1_])
            n = len(resp_points)
            if f1 * f2 >= 0:
                resp_points.extend([coord1, coord2, coord3, coord4])
                resp_cells.append([4, n, n + 1, n + 2, n + 3])
                scalars.extend([f1_, f2_, f2_, f1_])
            else:
                ratio = np.abs(f2 / f1)
                ratio = 1 / (ratio + 1)
                coord0 = coord1 + (coord2 - coord1) * ratio
                resp_points.extend(
                    [coord1, coord0, coord4, coord2, coord0, coord3])
                resp_cells.append([3, n, n + 1, n + 2])
                resp_cells.append([3, n + 3, n + 4, n + 5])
                scalars.extend([f1_, 0, f1_, f2_, 0, f2_])
        labels = [f"{label:.2E}" for label in labels]
        label_poins = np.array(label_poins)
        resp_points = np.array(resp_points)
        scalars = np.array(scalars)
        # ----------------------------------------------------------------------------------------
        line_plot = _generate_line_mesh(beam_node_coords, beam_cells, line_width=obj.line_width,
                                        color="black", use_cmap=False)
        resp_plot = _generate_face_mesh(resp_points, resp_cells, show_face_line=False, opacity=opacity,
                                        use_cmap=True, scalars=scalars, coloraxis="coloraxis")
        point_plot = _generate_point_mesh(resp_points, point_size=obj.point_size / 2,
                                          use_cmap=True, hover_name=response,
                                          scalars=scalars, coloraxis="coloraxis")
        # resp_plot = _generate_line_mesh(resp_points, resp_cells, line_width=obj.line_width,
        #                                 use_cmap=True, scalars=scalars, coloraxis="coloraxis")
        fig.add_traces(line_plot + resp_plot + point_plot)
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
            eye = dict(x=0., y=-0.1, z=10)  # for 2D camera
            scene = dict(camera=dict(
                eye=eye, projection=dict(type="orthographic")))
        else:
            eye = dict(x=-3.5, y=-3.5, z=3.5)  # for 3D camera
            scene = dict(aspectratio=dict(x=1, y=1, z=1), aspectmode="data",
                         camera=dict(eye=eye, projection=dict(
                             type="orthographic")))
        maxx = np.max(local_forces)
        minx = np.min(local_forces)
        txt = (f"<br>Step {maxstep + 1} {response}"
               f"<br>max.={maxx:.2E} | min.={minx:.2E}")
        fig.update_layout(
            template=obj.theme,
            autosize=True,
            showlegend=False,
            scene=scene,
            coloraxis=dict(colorscale=obj.color_map, cmin=cmin, cmax=cmax,
                           colorbar=dict(tickfont=dict(size=15))),
            title=dict(font=dict(family="courier", color='black', size=25),
                       text="<b>OpenSeesPy Frames Response 3D View</b>" + txt
                       ),
        )
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
    if obj.notebook:
        fig.show()


def _generate_point_mesh(points, point_size=1, color='black',
                         scalars=None, use_cmap=False, coloraxis=None,
                         hover_name=''):
    plotter = []
    if use_cmap:
        point_plot = go.Scatter3d(
            x=points[:, 0],
            y=points[:, 1],
            z=points[:, 2],
            marker=dict(size=point_size, color=scalars,
                        coloraxis=coloraxis),
            mode="markers",
            name=hover_name,
            customdata=scalars,
            hovertemplate='<b>%{customdata}</b>'
            # hoverinfo="skip",
        )
    else:
        point_plot = go.Scatter3d(
            x=points[:, 0],
            y=points[:, 1],
            z=points[:, 2],
            marker=dict(size=point_size, color=color),
            mode="markers",
        )
    plotter.append(point_plot)
    return plotter


def _generate_line_mesh(points, cells, line_width=1, color='blue', scalars=None, use_cmap=False, coloraxis=None):
    """
    generate the mesh from the points and cell
    """
    points = np.array(points)
    cells = np.array(cells)
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
    if use_cmap:
        line_dict = dict(color=line_scalars, width=line_width,
                         cmin=np.min(line_scalars), cmax=np.max(line_scalars),
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
        data = np.vstack([data0, data0[0], data1])
        if data0.shape[0] == 3:
            veci.append(len(face_points) + 0)
            vecj.append(len(face_points) + 1)
            veck.append(len(face_points) + 2)
        elif data0.shape[0] == 6:
            veci.append(len(face_points) + 0)
            vecj.append(len(face_points) + 3)
            veck.append(len(face_points) + 5)
            veci.append(len(face_points) + 3)
            vecj.append(len(face_points) + 1)
            veck.append(len(face_points) + 4)
            veci.append(len(face_points) + 5)
            vecj.append(len(face_points) + 3)
            veck.append(len(face_points) + 4)
            veci.append(len(face_points) + 5)
            vecj.append(len(face_points) + 4)
            veck.append(len(face_points) + 2)
        elif data0.shape[0] == 4:
            veci.append(len(face_points) + 0)
            veci.append(len(face_points) + 0)
            vecj.append(len(face_points) + 1)
            vecj.append(len(face_points) + 2)
            veck.append(len(face_points) + 2)
            veck.append(len(face_points) + 3)
            # i, j, k = [0, 0], [1, 2], [2, 3]
        elif data0.shape[0] == 8:
            veci.append(len(face_points) + 0)
            vecj.append(len(face_points) + 4)
            veck.append(len(face_points) + 7)
            veci.append(len(face_points) + 4)
            vecj.append(len(face_points) + 1)
            veck.append(len(face_points) + 5)
            veci.append(len(face_points) + 2)
            vecj.append(len(face_points) + 6)
            veck.append(len(face_points) + 5)
            veci.append(len(face_points) + 3)
            vecj.append(len(face_points) + 7)
            veck.append(len(face_points) + 6)
            veci.append(len(face_points) + 5)
            vecj.append(len(face_points) + 6)
            veck.append(len(face_points) + 7)
            veci.append(len(face_points) + 4)
            vecj.append(len(face_points) + 5)
            veck.append(len(face_points) + 7)
        face_line_points.extend(list(data))
        face_points.extend(list(data0))
        if use_cmap:
            face_scalars.extend(list(scalars[cell[1:]]))
    face_line_points = np.array(face_line_points)
    face_points = np.array(face_points)
    face_scalars = np.array(face_scalars)
    # plot new
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
    # face lines
    if show_face_line:
        plotter.append(
            go.Scatter3d(
                x=face_line_points[:, 0],
                y=face_line_points[:, 1],
                z=face_line_points[:, 2],
                line=dict(color='black', width=line_width / 2),
                mode="lines",
                connectgaps=False,
                hoverinfo="skip",
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
            data = np.vstack([data0, data0[0], data1])
            if points_origin is not None:
                data00 = points_origin[cell[1:], :]
                data11 = [np.NAN, np.NAN, np.NAN]
                data_ori = np.vstack([data00, data00[0], data11])
                face_line_origin_points.extend(list(data_ori))
            if data0.shape[0] == 3:
                veci.append(len(face_points) + 0)
                vecj.append(len(face_points) + 1)
                veck.append(len(face_points) + 2)
            elif data0.shape[0] == 6:
                veci.append(len(face_points) + 0)
                vecj.append(len(face_points) + 3)
                veck.append(len(face_points) + 5)
                veci.append(len(face_points) + 3)
                vecj.append(len(face_points) + 1)
                veck.append(len(face_points) + 4)
                veci.append(len(face_points) + 5)
                vecj.append(len(face_points) + 3)
                veck.append(len(face_points) + 4)
                veci.append(len(face_points) + 5)
                vecj.append(len(face_points) + 4)
                veck.append(len(face_points) + 2)
            elif data0.shape[0] == 4:
                veci.append(len(face_points) + 0)
                veci.append(len(face_points) + 0)
                vecj.append(len(face_points) + 1)
                vecj.append(len(face_points) + 2)
                veck.append(len(face_points) + 2)
                veck.append(len(face_points) + 3)
                # i, j, k = [0, 0], [1, 2], [2, 3]
            elif data0.shape[0] == 8:
                veci.append(len(face_points) + 0)
                vecj.append(len(face_points) + 4)
                veck.append(len(face_points) + 7)
                veci.append(len(face_points) + 4)
                vecj.append(len(face_points) + 1)
                veck.append(len(face_points) + 5)
                veci.append(len(face_points) + 2)
                vecj.append(len(face_points) + 6)
                veck.append(len(face_points) + 5)
                veci.append(len(face_points) + 3)
                vecj.append(len(face_points) + 7)
                veck.append(len(face_points) + 6)
                veci.append(len(face_points) + 5)
                vecj.append(len(face_points) + 6)
                veck.append(len(face_points) + 7)
                veci.append(len(face_points) + 4)
                vecj.append(len(face_points) + 5)
                veck.append(len(face_points) + 7)
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
        if show_face_line:
            plotter.append(
                go.Scatter3d(
                    x=face_line_points[:, 0],
                    y=face_line_points[:, 1],
                    z=face_line_points[:, 2],
                    line=dict(color='black', width=line_width / 2),
                    mode="lines",
                    connectgaps=False,
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
    # ---------------------------------------
    # point plot
    point_plot = go.Scatter3d(
        x=points[:, 0],
        y=points[:, 1],
        z=points[:, 2],
        marker=dict(size=point_size / 2, color=scalars,
                    coloraxis=coloraxis),
        mode="markers",
        name='',
        customdata=scalars,
        hovertemplate='<b>%{customdata}</b>'
        # hoverinfo="skip",
    )
    plotter.append(point_plot)
    return plotter


def _creat_arrows(points, cells, color,
                  arrow_tip_ratio=0.9, arrow_starting_ratio=1.0,
                  anchor_tip=True):
    points = np.array(points)
    cells = np.array(cells)
    x, y, z = points[:, 0], points[:, 1], points[:, 2]
    x_, y_, z_ = [], [], []
    u, v, w = [], [], []
    for p in cells:
        x_.append(x[p[1]] + arrow_starting_ratio*(x[p[2]] - x[p[1]]))
        y_.append(y[p[1]] + arrow_starting_ratio*(y[p[2]] - y[p[1]]))
        z_.append(z[p[1]] + arrow_starting_ratio*(z[p[2]] - z[p[1]]))
        u.append(arrow_tip_ratio*(x[p[2]] - x[p[1]]))
        v.append(arrow_tip_ratio*(y[p[2]] - y[p[1]]))
        w.append(arrow_tip_ratio*(z[p[2]] - z[p[1]]))
    arrow_plot = []
    for i in range(len(cells)):
        if anchor_tip:
            arrow_plot.append(go.Cone(x=[x_[i]], y=[y_[i]], z=[z_[i]],
                                      u=[u[i]], v=[v[i]], w=[w[i]],
                                      sizemode="absolute",
                                      anchor='tip', hoverinfo='skip',
                                      showlegend=False, showscale=False,
                                      colorscale=[[0, color], [1, color]]))
        else:
            arrow_plot.append(go.Cone(x=[x_[i]], y=[y_[i]], z=[z_[i]],
                                      u=[u[i]], v=[v[i]], w=[w[i]],
                                      sizemode="absolute",
                                      hoverinfo='skip',
                                      showlegend=False, showscale=False,
                                      colorscale=[[0, color], [1, color]]))
    return arrow_plot


def _reshape_cell(data):
    if len(data) > 0:
        i = 0
        data2 = []
        while True:
            n = data[i]
            data2.append(data[i:i + n + 1])
            i += n + 1
            if i >= len(data):
                break
    else:
        data2 = []
    return data2
