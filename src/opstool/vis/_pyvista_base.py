import warnings

import h5py
import numpy as np
import matplotlib.pyplot as plt
import pyvista as pv

from ..utils import check_file, shape_dict


def _model_vis(
    obj,
    input_file: str = "ModelData.hdf5",
    show_node_label: bool = False,
    show_ele_label: bool = False,
    label_size: float = 10,
    show_local_crd: bool = False,
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
    filename = obj.out_dir + "/" + input_file
    model_info = dict()
    cells = dict()
    with h5py.File(filename, "r") as f:
        grp1 = f["ModelInfo"]
        for name in grp1.keys():
            model_info[name] = grp1[name][...]
        grp2 = f["Cell"]
        for name in grp2.keys():
            cells[name] = grp2[name][...]

    plotter = pv.Plotter(notebook=obj.notebook, line_smoothing=True)
    _plot_model(obj, plotter, model_info, cells, opacity)

    txt = f"OpenSees 3D View\nNum. of Node:{model_info['num_node']}\nNum. of Ele:{model_info['num_ele']}"
    plotter.add_text(txt, position="upper_right", font_size=12, font="courier")
    if show_outline:
        show_zaxis = False if np.max(model_info["model_dims"]) <= 2 else True
        plotter.show_bounds(
            grid=False,
            location="outer",
            bounds=model_info["bound"],
            show_zaxis=show_zaxis,
        )
    if show_node_label:
        node_labels = ["N" + str(i) for i in model_info["NodeTags"]]
        plotter.add_point_labels(
            model_info["coord_no_deform"],
            node_labels,
            text_color="white",
            font_size=label_size,
            point_color=obj.color_point,
            bold=False,
            render_points_as_spheres=True,
            point_size=1e-5,
            always_visible=True,
        )
    if show_ele_label:
        ele_labels = ["E" + str(i) for i in model_info["EleTags"]]
        plotter.add_point_labels(
            model_info["coord_ele_midpoints"],
            ele_labels,
            text_color="#ff796c",
            font_size=label_size,
            bold=False,
            always_visible=True,
        )
    # local axes
    if show_local_crd:
        _show_beam_local_axes(
            plotter, model_info, alpha=local_crd_alpha, label_size=label_size
        )
        _show_link_local_axes(
            plotter, model_info, alpha=local_crd_alpha, label_size=label_size
        )
    # fix nodes
    if show_fix_node:
        _show_fix_node(plotter, model_info, alpha=fix_node_alpha)
    if show_beam_sec:
        beam_sec_paras_ = dict(color="#5170d7", opacity=0.25, texture=False)
        if beam_sec_paras is not None:
            beam_sec_paras_.update(beam_sec_paras)
        _show_beam_sec(plotter, model_info, cells, beam_sec_paras_)
    # mp constraint lines
    _show_mp_constraint(obj, plotter, model_info, show_constrain_dof)
    if show_load:
        _show_node_load(plotter, model_info, load_alpha)
        _show_ele_load(plotter, model_info, load_alpha)
    plotter.add_axes()
    plotter.view_isometric()
    if np.max(model_info["model_dims"]) <= 2:
        plotter.view_xy(negative=False)
    if save_fig:
        plotter.save_graphic(save_fig)
    plotter.enable_anti_aliasing("msaa")
    plotter.show(title=obj.title)
    plotter.close()


def _show_mp_constraint(obj, plotter, model_info, show_dofs):
    points = model_info["ConstrainedCoords"]
    cells = model_info["ConstrainedCells"]
    midcoords = model_info["ConstrainedMidCoords"]
    dofs = model_info["ConstrainedDofs"]
    dofs = ["".join([str(k) for k in dof if k != -1]) for dof in dofs]
    if len(cells) > 0:
        mesh = _generate_mesh(points, cells, kind="line")
        plotter.add_mesh(
            mesh,
            color=obj.color_constraint,
            render_lines_as_tubes=False,
            line_width=obj.line_width / 3,
        )
        if show_dofs:
            plotter.add_point_labels(
                midcoords,
                dofs,
                text_color=obj.color_constraint,
                font_size=12,
                bold=True,
                show_points=False,
                always_visible=True,
                shape_opacity=0,
            )


def _show_beam_sec(plotter, model_info, cells, paras):
    ext_points = model_info["line_sec_ext_points"]
    int_points = model_info["line_sec_int_points"]
    sec_points = model_info["line_sec_points"]
    ext_cells = cells["line_sec_ext"]
    int_cells = cells["line_sec_int"]
    sec_cells = cells["line_sec"]
    if paras["texture"]:
        texture = pv.read_texture(paras["texture"])
    else:
        texture = None
    if len(ext_cells) > 0:
        ext = _generate_mesh(ext_points, ext_cells, kind="face")
        if texture is not None:
            ext.texture_map_to_plane(inplace=True)
        plotter.add_mesh(
            ext,
            show_edges=False,
            color=paras["color"],
            opacity=paras["opacity"],
            texture=texture,
        )
    if len(int_cells) > 0:
        intt = _generate_mesh(int_points, int_cells, kind="face")
        if texture is not None:
            intt.texture_map_to_plane(inplace=True)
        plotter.add_mesh(
            intt,
            show_edges=False,
            color=paras["color"],
            opacity=paras["opacity"],
            texture=texture,
        )
    if len(sec_cells) > 0:
        sec = _generate_mesh(sec_points, sec_cells, kind="face")
        if texture is not None:
            sec.texture_map_to_plane(inplace=True)
        plotter.add_mesh(
            sec,
            show_edges=False,
            color=paras["color"],
            opacity=paras["opacity"],
            texture=texture,
        )


def _show_node_load(plotter, model_info, alpha: float = 1.0):
    points = model_info["coord_no_deform"]
    node_load_info = np.array(model_info["node_load_info"])
    node_load_data = np.array(model_info["node_load_data"])
    if len(node_load_info) == 0:
        return None
    loc, load_data = 0, []
    for info in node_load_info:
        ndm = info[2]
        ndf = info[3]
        data = node_load_data[loc : loc + ndf]
        if ndm <= 2 and ndf <= 3:
            load_data.append([data[0], data[1], 0])  # x, y
        else:
            load_data.append([data[0], data[1], data[2]])  # x, y, z
        loc += ndf
    load_data = np.array(load_data)
    maxdata = np.max(np.abs(load_data))
    beam_lengths = model_info["beam_lengths"]
    if len(beam_lengths) > 0:
        alpha_ = np.mean(beam_lengths) / maxdata / 2
    else:
        alpha_ = (model_info["max_bound"] + model_info["min_bound"]) / 20 / maxdata
    alpha_ *= alpha
    patterntags = np.unique(node_load_info[:, 0])
    cmap = plt.get_cmap("Spectral")
    colors = cmap(np.linspace(0, 1, len(patterntags)))
    xyzlocals = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
    geom = pv.Arrow(
        start=(-1.0, 0, 0), tip_length=0.25, tip_radius=0.1, shaft_radius=0.03
    )
    for p, ptag in enumerate(patterntags):
        idx = np.abs(node_load_info[:, 0] - ptag) < 1e-3
        coords = points[node_load_info[idx, -1]]
        for i in range(3):
            ply = pv.PolyData(coords)
            data = np.ravel(load_data[idx, i])
            ply["scalars"] = np.abs(data)
            ply["vectors"] = np.reshape(xyzlocals[i] * len(coords), (-1, 3))
            for j in range(len(ply["vectors"])):
                ply["vectors"][j] *= np.sign(data[j])
            glyphs = ply.glyph(
                orient="vectors", scale="scalars", factor=alpha_, geom=geom
            )
            plotter.add_mesh(glyphs, show_scalar_bar=False, color=colors[p])


def _show_ele_load(plotter, model_info, alpha: float = 1.0):
    points = model_info["coord_no_deform"]
    ele_load_info = model_info["ele_load_info"]
    ele_load_data = model_info["ele_load_data"]
    ele_load_locals = model_info["ele_load_locals"]
    if len(ele_load_info) == 0:
        return None
    patterntags = np.unique(ele_load_info[:, 0])
    new_points = []
    new_locals = []
    new_ptags = []
    load_data = []
    loc = 0
    for i, info in enumerate(ele_load_info):
        ptag, _, classtag, nidx1, nidx2 = info
        coord1, coord2 = points[nidx1], points[nidx2]
        local_axis = ele_load_locals[i]
        if classtag == 3:  # beamUniform2D, Wya <Wxa>
            wy, wx = ele_load_data[loc : loc + 2]
            wz = 0.0
            n = 11
            xl = np.linspace(0, 1, n)
            wx, wy, wz = [wx] * n, [wy] * n, [wz] * n
            localaxis = [local_axis] * n
            new_ptags.extend([ptag] * n)
            loc += 2
        elif classtag == 12:  # beamUniform2D, Wya <Wxa> <aL> <bL> <Wyb> <Wxb>
            wya, wyb, wxa, wxb, al, bl = ele_load_data[loc : loc + 6]
            n = int((bl - al) / 0.1) + 1
            xl = np.linspace(al, bl, n)
            wy = np.interp(xl, [0, 1], [wya, wyb])
            wx = np.interp(xl, [0, 1], [wxa, wxb])
            wz = wy * 0
            localaxis = [local_axis] * n
            new_ptags.extend([ptag] * n)
            loc += 6
        elif classtag == 5:  # beamUniform3D wy, wz, wx
            wy, wz, wx = ele_load_data[loc : loc + 3]
            n = 11
            xl = np.linspace(0, 1, n)
            wx, wy, wz = [wx] * n, [wy] * n, [wz] * n
            localaxis = [local_axis] * n
            new_ptags.extend([ptag] * n)
            loc += 3
        elif classtag == 4:  # beamPoint2D, Py xL <Px>
            wy, wx, xl = ele_load_data[loc : loc + 3]
            wz = 0
            localaxis = [local_axis]
            new_ptags.append(ptag)
            loc += 3
        elif classtag == 6:  # beamPoint3D, Py, Pz, x, N
            wy, wz, wx, xl = ele_load_data[loc : loc + 4]
            localaxis = [local_axis]
            new_ptags.append(ptag)
            loc += 4
        else:
            warnings.warn(
                "Currently load visualization only supports-->"
                "<beamUniform2D,beamUniform3D,beamPoint2D,beamPoint3D>!"
            )
        xs = np.interp(xl, [0, 1], [coord1[0], coord2[0]])
        ys = np.interp(xl, [0, 1], [coord1[1], coord2[1]])
        zs = np.interp(xl, [0, 1], [coord1[2], coord2[2]])
        new_points.append(np.column_stack([xs, ys, zs]))
        new_locals.append(localaxis)
        load_data.append(np.column_stack([wx, wy, wz]))
    new_points = np.vstack(new_points)
    new_locals = np.vstack(new_locals)
    load_data = np.vstack(load_data)
    new_ptags = np.array(new_ptags)
    maxdata = np.max(np.abs(load_data))
    beam_lengths = model_info["beam_lengths"]
    if len(beam_lengths) > 0:
        alpha_ = np.mean(beam_lengths) / maxdata / 2
    else:
        alpha_ = (model_info["max_bound"] + model_info["min_bound"]) / 20 / maxdata
    alpha_ *= alpha
    cmap = plt.get_cmap("rainbow")
    colors = cmap(np.linspace(0, 1, len(patterntags)))
    geom = pv.Arrow(
        start=(-1.0, 0, 0), tip_length=0.25, tip_radius=0.1, shaft_radius=0.03
    )
    for p, ptag in enumerate(patterntags):
        idx = np.abs(new_ptags - ptag) < 1e-3
        coords = new_points[idx]
        for i in range(3):
            ply = pv.PolyData(coords)
            data = np.ravel(load_data[idx, i])
            ply["scalars"] = np.abs(data)
            ply["vectors"] = new_locals[idx, 3 * i : 3 * i + 3]
            for j in range(len(ply["vectors"])):
                ply["vectors"][j] *= np.sign(data[j])
            glyphs = ply.glyph(
                orient="vectors", scale="scalars", factor=alpha_, geom=geom
            )
            plotter.add_mesh(glyphs, show_scalar_bar=False, color=colors[p])


def _show_beam_local_axes(
    plotter, model_info, alpha: float = 1.0, label_size: float = 10
):
    beam_xlocal = model_info["beam_xlocal"]
    beam_ylocal = model_info["beam_ylocal"]
    beam_zlocal = model_info["beam_zlocal"]
    beam_midpoints = model_info["beam_midpoints"]
    beam_lengths = model_info["beam_lengths"]
    if len(beam_lengths) > 0:
        length = np.mean(beam_lengths) / 6 * alpha
        _ = plotter.add_arrows(beam_midpoints, beam_xlocal, mag=length, color="#cf6275")
        _ = plotter.add_arrows(beam_midpoints, beam_ylocal, mag=length, color="#04d8b2")
        _ = plotter.add_arrows(beam_midpoints, beam_zlocal, mag=length, color="#9aae07")
        plotter.add_point_labels(
            beam_midpoints + length * beam_xlocal,
            ["x"] * beam_midpoints.shape[0],
            font_size=label_size,
            text_color="#cf6275",
            bold=False,
            shape=None,
            render_points_as_spheres=True,
            point_size=1.0e-5,
            always_visible=True,
        )
        plotter.add_point_labels(
            beam_midpoints + length * beam_ylocal,
            ["y"] * beam_midpoints.shape[0],
            font_size=label_size,
            text_color="#04d8b2",
            bold=False,
            shape=None,
            render_points_as_spheres=True,
            point_size=1.0e-5,
            always_visible=True,
        )
        plotter.add_point_labels(
            beam_midpoints + length * beam_zlocal,
            ["z"] * beam_midpoints.shape[0],
            font_size=label_size,
            text_color="#9aae07",
            bold=False,
            shape=None,
            render_points_as_spheres=True,
            point_size=1.0e-5,
            always_visible=True,
        )
    else:
        warnings.warn("Model has no frame elements when show_local_crd=True!")


def _show_link_local_axes(
    plotter, model_info, alpha: float = 1.0, label_size: float = 10
):
    link_xlocal = model_info["link_xlocal"]
    link_ylocal = model_info["link_ylocal"]
    link_zlocal = model_info["link_zlocal"]
    link_midpoints = model_info["link_midpoints"]
    link_lengths = model_info["link_lengths"]
    if len(link_midpoints) > 0:
        length = np.mean(link_lengths) / 6 * alpha
        _ = plotter.add_arrows(link_midpoints, link_xlocal, mag=length, color="#cf6275")
        _ = plotter.add_arrows(link_midpoints, link_ylocal, mag=length, color="#04d8b2")
        _ = plotter.add_arrows(link_midpoints, link_zlocal, mag=length, color="#9aae07")
        plotter.add_point_labels(
            link_midpoints + length * link_xlocal,
            ["x"] * link_midpoints.shape[0],
            text_color="#cf6275",
            font_size=label_size,
            bold=False,
            shape=None,
            render_points_as_spheres=True,
            point_size=1.0e-5,
            always_visible=True,
        )
        plotter.add_point_labels(
            link_midpoints + length * link_ylocal,
            ["y"] * link_midpoints.shape[0],
            text_color="#04d8b2",
            font_size=label_size,
            bold=False,
            shape=None,
            render_points_as_spheres=True,
            point_size=1.0e-5,
            always_visible=True,
        )
        plotter.add_point_labels(
            link_midpoints + length * link_zlocal,
            ["z"] * link_midpoints.shape[0],
            text_color="#9aae07",
            font_size=label_size,
            bold=False,
            shape=None,
            render_points_as_spheres=True,
            point_size=1.0e-5,
            always_visible=True,
        )
    else:
        # warnings.warn("Model has no link elements!")
        pass


def _show_fix_node(plotter, model_info, alpha: float = 1.0):
    fixed_dofs = model_info["FixNodeDofs"]
    fixed_coords = model_info["FixNodeCoords"]
    beam_lengths = model_info["beam_lengths"]
    D2 = True if np.max(model_info["model_dims"]) <= 2 else False
    if len(beam_lengths) > 0:
        s = np.mean(beam_lengths) / 6 * alpha
    else:
        s = (model_info["max_bound"] + model_info["min_bound"]) / 100 * alpha
    if len(fixed_coords) > 0:
        points, cells = [], []
        for coord, dof in zip(fixed_coords, fixed_dofs):
            x, y, z = coord
            if D2:
                z += s / 2
                y -= s / 2
            if dof[0] == -1:
                idx = len(points)
                points.extend(
                    [
                        [x, y - s / 2, z],
                        [x, y + s / 2, z],
                        [x, y + s / 2, z - s],
                        [x, y - s / 2, z - s],
                    ]
                )
                cells.extend(
                    [
                        2,
                        idx,
                        idx + 1,
                        2,
                        idx + 1,
                        idx + 2,
                        2,
                        idx + 2,
                        idx + 3,
                        2,
                        idx + 3,
                        idx,
                    ]
                )
            if dof[1] == -1:
                idx = len(points)
                points.extend(
                    [
                        [x - s / 2, y, z],
                        [x + s / 2, y, z],
                        [x + s / 2, y, z - s],
                        [x - s / 2, y, z - s],
                    ]
                )
                cells.extend(
                    [
                        2,
                        idx,
                        idx + 1,
                        2,
                        idx + 1,
                        idx + 2,
                        2,
                        idx + 2,
                        idx + 3,
                        2,
                        idx + 3,
                        idx,
                    ]
                )
            if dof[2] == -1:
                idx = len(points)
                points.extend(
                    [
                        [x - s / 2, y - s / 2, z - s / 2],
                        [x + s / 2, y - s / 2, z - s / 2],
                        [x + s / 2, y + s / 2, z - s / 2],
                        [x - s / 2, y + s / 2, z - s / 2],
                    ]
                )
                cells.extend(
                    [
                        2,
                        idx,
                        idx + 1,
                        2,
                        idx + 1,
                        idx + 2,
                        2,
                        idx + 2,
                        idx + 3,
                        2,
                        idx + 3,
                        idx,
                    ]
                )
        fix_plot = _generate_mesh(points, cells, kind="line")
        plotter.add_mesh(
            fix_plot, color="#01ff07", render_lines_as_tubes=False, line_width=2
        )
    else:
        warnings.warn("Model has no fix nodes!")


def _show_link(obj, plotter, points, cells):
    cells = np.reshape(cells, (-1, 3))
    points_zero = []
    points_nonzero = []
    cells_nonzero = []
    for cell in cells:
        idx1, idx2 = cell[1:]
        coord1, coord2 = points[idx1], points[idx2]
        length = np.sqrt(np.sum((coord2 - coord1) ** 2))
        if np.abs(length) < 1e-8:
            points_zero.append(coord1)
        else:
            xaxis = np.array(coord2 - coord1)
            global_z = [0.0, 0.0, 1.0]
            cos_angle = xaxis.dot(global_z) / (
                np.linalg.norm(xaxis) * np.linalg.norm(global_z)
            )
            if np.abs(1 - cos_angle**2) < 1e-10:
                yaxis = np.cross([-1.0, 0.0, 0.0], xaxis)
            else:
                yaxis = np.cross(global_z, xaxis)
            xaxis = xaxis / np.linalg.norm(xaxis)
            yaxis = yaxis / np.linalg.norm(yaxis)
            idx = len(points_nonzero)
            for i in range(5):
                cells_nonzero.extend([2, idx + i, idx + i + 1])
            points_nonzero.extend(
                [
                    coord1 + 0.25 * length * xaxis,
                    coord1 + 0.25 * length * xaxis - 0.25 * length * yaxis,
                    coord1 + 0.5 * length * xaxis + 0.25 * length * yaxis,
                    coord1 + 0.5 * length * xaxis - 0.25 * length * yaxis,
                    coord1 + 0.75 * length * xaxis + 0.25 * length * yaxis,
                    coord1 + 0.75 * length * xaxis,
                ]
            )
    # plot
    if len(points_zero) > 0:
        plotter.add_mesh(
            pv.PolyData(points_zero),
            color=obj.color_link,
            point_size=obj.point_size * 2,
            render_points_as_spheres=True,
        )
    if len(points_nonzero) > 0:
        link_plot = _generate_mesh(points_nonzero, cells_nonzero, kind="line")
        plotter.add_mesh(
            link_plot,
            color=obj.color_link,
            render_lines_as_tubes=False,
            line_width=obj.line_width / 2,
        )


def _plot_model(obj, plotter, model_info, cells, opacity):
    point_plot = pv.PolyData(model_info["coord_no_deform"])
    plotter.add_mesh(
        point_plot,
        color=obj.color_point,
        point_size=obj.point_size,
        render_points_as_spheres=True,
    )

    if len(cells["truss"]) > 0:
        truss_plot = _generate_mesh(
            model_info["coord_no_deform"], cells["truss"], kind="line"
        )
        plotter.add_mesh(
            truss_plot,
            color=obj.color_truss,
            render_lines_as_tubes=True,
            line_width=obj.line_width,
        )

    if len(cells["link"]) > 0:
        link_plot = _generate_mesh(
            model_info["coord_no_deform"], cells["link"], kind="line"
        )
        plotter.add_mesh(
            link_plot,
            color=obj.color_link,
            render_lines_as_tubes=False,
            line_width=obj.line_width / 2,
        )
        _show_link(obj, plotter, model_info["coord_no_deform"], cells["link"])

    if len(cells["beam"]) > 0:
        beam_plot = _generate_mesh(
            model_info["coord_no_deform"], cells["beam"], kind="line"
        )
        plotter.add_mesh(
            beam_plot,
            color=obj.color_line,
            render_lines_as_tubes=True,
            line_width=obj.line_width,
        )

    if len(cells["other_line"]) > 0:
        other_line_plot = _generate_mesh(
            model_info["coord_no_deform"], cells["other_line"], kind="line"
        )
        plotter.add_mesh(
            other_line_plot,
            color=obj.color_line,
            render_lines_as_tubes=True,
            line_width=obj.line_width,
        )

    if len(cells["plane"]) > 0:
        face_plot = _generate_mesh(
            model_info["coord_no_deform"], cells["plane"], kind="face"
        )
        plotter.add_mesh(
            face_plot, color=obj.color_face, show_edges=True, opacity=opacity
        )

    if len(cells["tetrahedron"]) > 0:
        tet_plot = _generate_mesh(
            model_info["coord_no_deform"], cells["tetrahedron"], kind="face"
        )
        plotter.add_mesh(
            tet_plot, color=obj.color_solid, show_edges=True, opacity=opacity
        )

    if len(cells["brick"]) > 0:
        bri_plot = _generate_mesh(
            model_info["coord_no_deform"], cells["brick"], kind="face"
        )
        plotter.add_mesh(
            bri_plot, color=obj.color_solid, show_edges=True, opacity=opacity
        )


def _eigen_vis(
    obj,
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
    filename = obj.out_dir + "/" + input_file
    eigen_data = dict()
    with h5py.File(filename, "r") as f:
        grp = f["EigenInfo"]
        for name, value in grp.items():
            eigen_data[name] = value[...]

    f = eigen_data["f"]
    eigenvector = eigen_data["eigenvector"]
    show_zaxis = False if np.max(eigen_data["model_dims"]) <= 2 else True
    num_mode_tag = len(f)
    modei, modej = mode_tags
    modei, modej = int(modei), int(modej)
    if modej > num_mode_tag:
        raise ValueError(f"Insufficient number of modes in eigen file {filename}!")

    # -----------------------------------------------------------------------
    def create_mesh(idx, idxi=None, idxj=None):
        if idxi is not None and idxj is not None:
            plotter.subplot(idxi, idxj)
        else:
            plotter.clear_actors()
        step = int(round(idx)) - 1
        eigen_vec = eigenvector[step]
        value_ = np.max(np.sqrt(np.sum(eigen_vec**2, axis=1)))
        alpha_ = eigen_data["max_bound"] / obj.bound_fact / value_
        alpha_ = alpha * alpha if alpha else alpha_
        eigen_points = eigen_data["coord_no_deform"] + eigen_vec * alpha_
        scalars = np.sqrt(np.sum(eigen_vec**2, axis=1))
        _ = _generate_all_mesh(
            plotter,
            eigen_points,
            scalars,
            opacity,
            obj.color_map,
            eigen_data["all_lines"],
            eigen_data["all_faces"],
            show_origin=show_origin,
            points_origin=eigen_data["coord_no_deform"],
            point_size=obj.point_size,
            line_width=obj.line_width,
            show_face_line=show_face_line,
        )
        # plotter.add_scalar_bar(fmt="%.3e", n_labels=10, label_font_size=12)
        # txt = 'Mode {}\nf = {:.3f} Hz\nT = {:.3f} s'.format(mode_tag, f_, 1 / f_)
        txt = "Mode {}\nT = {:.3f} s".format(step + 1, 1 / f[step])
        plotter.add_text(
            txt, position="upper_left", font_size=label_size, font="courier"
        )
        if show_outline:
            plotter.show_bounds(
                grid=False,
                location="outer",
                bounds=eigen_data["bound"],
                show_zaxis=show_zaxis,
                # color="black",
            )
        plotter.add_axes()

    # !subplots
    if subplots:
        if modej - modei + 1 > 49:
            raise ValueError("When subplots True, mode_tag range must < 49 for clarify")
        shape = shape_dict[modej - modei + 1]
        plotter = pv.Plotter(notebook=obj.notebook, shape=shape, line_smoothing=True)
        for i, idx in enumerate(range(modei, modej + 1)):
            idxi = int(np.ceil((i + 1) / shape[1]) - 1)
            idxj = int(i - idxi * shape[1])
            create_mesh(idx, idxi, idxj)
        if link_views:
            plotter.link_views()
    # !slide style
    else:
        plotter = pv.Plotter(notebook=obj.notebook, line_smoothing=True)
        plotter.add_slider_widget(
            create_mesh,
            [modei, modej],
            value=modei,
            pointa=(0.4, 0.9),
            pointb=(0.9, 0.9),
            title="Mode",
            title_opacity=1,
            # title_color="black",
            fmt="%.0f",
            title_height=0.03,
            slider_width=0.03,
            tube_width=0.01,
        )
    plotter.view_isometric()
    if np.max(eigen_data["model_dims"]) <= 2:
        plotter.view_xy(negative=False)
    if save_fig:
        plotter.save_graphic(save_fig)
    plotter.enable_anti_aliasing("msaa")
    plotter.show(title=obj.title)
    plotter.close()


def _eigen_anim(
    obj,
    mode_tag: int = 1,
    input_file: str = "EigenData.hdf5",
    n_cycle: int = 5,
    label_size: float = 15,
    alpha: float = None,
    show_outline: bool = False,
    opacity: float = 1,
    framerate: int = 3,
    show_face_line: bool = True,
    save_fig: str = "EigenAnimation.gif",
):
    filename = obj.out_dir + "/" + input_file
    eigen_data = dict()
    with h5py.File(filename, "r") as f:
        grp = f["EigenInfo"]
        for name, value in grp.items():
            eigen_data[name] = value[...]

    f = eigen_data["f"]
    eigenvector = eigen_data["eigenvector"]
    num_mode_tag = len(f)
    if mode_tag > num_mode_tag:
        raise ValueError("Insufficient number of modes in open file")
    eigen_vec = eigenvector[mode_tag - 1]
    f_ = f[mode_tag - 1]
    value_ = np.max(np.sqrt(np.sum(eigen_vec**2, axis=1)))
    alpha_ = eigen_data["max_bound"] / obj.bound_fact / value_
    alpha_ = alpha_ * alpha if alpha else alpha_
    eigen_points = eigen_data["coord_no_deform"] + eigen_vec * alpha_
    anti_eigen_points = eigen_data["coord_no_deform"] - eigen_vec * alpha_
    scalars = np.sqrt(np.sum(eigen_vec**2, axis=1))
    plt_points = [anti_eigen_points, eigen_data["coord_no_deform"], eigen_points]
    # -----------------------------------------------------------------------------
    # start plot
    plotter = pv.Plotter(notebook=obj.notebook, line_smoothing=True)

    value_ = np.max(np.sqrt(np.sum(eigen_vec**2, axis=1)))
    alpha_ = eigen_data["max_bound"] / obj.bound_fact / value_
    alpha_ = alpha_ * alpha if alpha else alpha_
    eigen_points = eigen_data["coord_no_deform"] + eigen_vec * alpha_
    anti_eigen_points = eigen_data["coord_no_deform"] - eigen_vec * alpha_
    scalars = np.sqrt(np.sum(eigen_vec**2, axis=1))
    point_plot, line_plot, face_plot = _generate_all_mesh(
        plotter,
        eigen_data["coord_no_deform"],
        scalars * 0,
        opacity,
        obj.color_map,
        eigen_data["all_lines"],
        eigen_data["all_faces"],
        show_origin=False,
        points_origin=eigen_data["coord_no_deform"],
        show_scalar_bar=True,
        point_size=obj.point_size,
        line_width=obj.line_width,
        show_face_line=show_face_line,
    )

    plotter.add_scalar_bar(fmt="%.3E", n_labels=10, label_font_size=12)

    plotter.add_text(
        "Mode {}\nf = {:.3f} Hz\nT = {:.3f} s".format(mode_tag, f_, 1 / f_),
        position="upper_right",
        font_size=label_size,
        # color="black",
        font="courier",
    )
    if show_outline:
        plotter.show_bounds(
            grid=False,
            location="outer",
            bounds=eigen_data["bound"],
            show_zaxis=True,
            # color="black",
        )
    plotter.add_axes()
    # plotter.add_text('OpenSees 3D View', position='upper_left', font_size=16, color='black', font='courier')
    plotter.view_isometric()
    if np.max(eigen_data["model_dims"]) <= 2:
        plotter.view_xy(negative=False)

    # animation
    # ----------------------------------------------------------------------------
    if save_fig.endswith(".gif"):
        plotter.open_gif(save_fig, fps=framerate, palettesize=64)
    else:
        plotter.open_movie(save_fig, framerate=framerate, quality=7)
    plt_points = [anti_eigen_points, eigen_data["coord_no_deform"], eigen_points]
    render = False
    index = [2, 0] * n_cycle
    plotter.write_frame()  # write initial data
    for idx in index:
        points = plt_points[idx]
        xyz = (eigen_data["coord_no_deform"] - points) / alpha_
        xyz_eigen = np.sqrt(np.sum(xyz**2, axis=1))
        if point_plot:
            plotter.update_coordinates(points, mesh=point_plot, render=render)
            plotter.update_scalars(scalars=xyz_eigen, mesh=point_plot, render=render)
        if line_plot:
            plotter.update_scalars(scalars=xyz_eigen, mesh=line_plot, render=render)
            plotter.update_coordinates(points, mesh=line_plot, render=render)
        if face_plot:
            plotter.update_scalars(scalars=xyz_eigen, mesh=face_plot, render=render)
            plotter.update_coordinates(points, mesh=face_plot, render=render)
        plotter.update_scalar_bar_range(
            clim=[np.min(xyz_eigen), np.max(xyz_eigen)], name=None
        )
        plotter.write_frame()
    # ----------------------------------------------------------------------------------
    plotter.enable_anti_aliasing("msaa")
    plotter.show(title=obj.title)
    plotter.close()


def _react_vis(
    obj,
    input_file: str = "NodeReactionStepData-1.hdf5",
    slider: bool = False,
    direction: str = "Fz",
    show_values: bool = True,
    show_outline: bool = False,
    save_fig: str = "ReactionVis.svg",
):
    direct = direction.lower()
    if direct not in ["fx", "fy", "fz", "mx", "my", "mz"]:
        raise ValueError(
            "response must be one of ['Fx', 'Fy', 'Fz', 'Mx', 'My', 'Mz']!"
        )
    filename = obj.out_dir + "/" + input_file
    node_react_steps = []
    with h5py.File(filename, "r") as f:
        Nsteps = int(f["Nsteps"][...])
        node_coords = f["NodeReactCoords"][...]
        model_dims = f["model_dims"][...]
        NodeTags = f["NodeReactTags"][...]
        num_nodes = node_coords.shape[0]
        grp = f["NodeReactSteps"]
        for i in range(Nsteps):
            node_react_steps.append(grp[f"step{i + 1}"][...])
    if np.max(model_dims) < 3:
        D2 = True
    else:
        D2 = False
    max_bound = np.max(np.max(node_coords, axis=0) - np.min(node_coords, axis=0))
    axis_dict = dict(
        fx=(1, 0.0, 0.0),
        fy=(0.0, 1, 0.0),
        fz=(0.0, 0.0, 1),
        mx=(1, 0.0, 0.0),
        my=(0.0, 1, 0.0),
        mz=(0.0, 0.0, 1),
    )
    color_dict = dict(
        fx="#d20962",
        fy="#f47721",
        fz="#7ac143",
        mx="#00a78e",
        my="#00bce4",
        mz="#7d3f98",
    )
    if D2:
        reactidx_dict = dict(fx=0, fy=1, fz=None, mx=None, my=None, mz=2)
    else:
        reactidx_dict = dict(fx=0, fy=1, fz=2, mx=3, my=4, mz=5)

    plotter = pv.Plotter(notebook=obj.notebook, line_smoothing=True)

    def create_mesh(value):
        step = int(round(value)) - 1
        f = node_react_steps[step][:, reactidx_dict[direct]]
        idxmax, idxmin = np.argmax(f), np.argmin(f)
        plotter.clear_actors()  # !!!!!!
        # point plot
        point_plot = pv.PolyData(node_coords)
        plotter.add_mesh(
            point_plot,
            color=obj.color_point,
            point_size=obj.point_size,
            render_points_as_spheres=True,
        )
        point_plot2 = pv.PolyData(node_coords[[idxmax, idxmin]])
        plotter.add_mesh(
            point_plot2,
            color="red",
            point_size=obj.point_size * 2,
            render_points_as_spheres=True,
        )
        # arrow plot
        length = max_bound / 30
        axis = np.zeros_like(node_coords)
        for i in range(num_nodes):
            axis[i] = np.array(axis_dict[direct]) * np.sign(f[i])
        arrow_ends = node_coords - length * axis
        _ = plotter.add_arrows(arrow_ends, axis, mag=length, color=color_dict[direct])
        labels = [f"{data:.3E}" for data in f]
        plotter.add_point_labels(
            arrow_ends,
            labels,
            bold=False,
            shape=None,
            render_points_as_spheres=True,
            point_size=1.0e-5,
            always_visible=True,
        )

        plotter.add_text(
            "OpenSeesPy Node Reactions View",
            position="upper_left",
            shadow=True,
            font_size=16,
            # color="black",
            font="courier",
        )
        txt = (
            f"Step {step + 1} {direction}\n"
            f"max={f[idxmax]:.3E} | nodeTag={NodeTags[idxmax]}\n"
            f"min={f[idxmin]:.3E} | nodeTag={NodeTags[idxmin]}"
        )
        plotter.add_text(
            txt,
            position="upper_right",
            shadow=True,
            font_size=12,
            # color="black",
            font="courier",
        )

        if show_outline:
            plotter.show_bounds(
                grid=False,
                location="outer",
                show_zaxis=True,
                # color="black",
            )
        plotter.add_axes()

    if slider:
        _ = plotter.add_slider_widget(
            create_mesh,
            [1, Nsteps],
            value=Nsteps,
            pointa=(0.0, 0.9),
            pointb=(0.5, 0.9),
            title="Step",
            title_opacity=1,
            # title_color="black",
            fmt="%.0f",
            title_height=0.03,
            slider_width=0.03,
            tube_width=0.01,
        )
    # -------------------------------------------------------------------------
    else:  # plot a single step
        idx = np.argmax(
            [
                np.max(np.abs(react[:, reactidx_dict[direct]]))
                for react in node_react_steps
            ]
        )
        create_mesh(idx + 1)
    plotter.view_isometric()
    if D2:
        plotter.view_xy(negative=False)
    if save_fig:
        plotter.save_graphic(save_fig)
    plotter.enable_anti_aliasing("msaa")
    plotter.show(title=obj.title)
    plotter.close()


def _deform_vis(
    obj,
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
    resp_type = response.lower()
    if resp_type not in ["disp", "vel", "accel"]:
        raise ValueError("response must be 'disp', 'vel', or 'accel'!")

    filename = obj.out_dir + "/" + input_file
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
    max_resps = [
        np.max(np.sqrt(np.sum(resp_**2, axis=1)))
        for resp_ in node_resp_steps[resp_type]
    ]
    max_step = np.argmax(max_resps)
    max_node_resp = node_resp_steps[resp_type][max_step]
    scalars = np.sqrt(np.sum(max_node_resp**2, axis=1))
    cmin, cmax = np.min(scalars), np.max(scalars)
    if model_update:
        bounds = model_info_steps["bound"][0]
        model_dims = model_info_steps["model_dims"][0]
    else:
        bounds = model_info_steps["bound"]
        model_dims = model_info_steps["model_dims"]
    # scale factor
    if resp_type == "disp":
        max_bound = np.max(
            [bounds[1] - bounds[0], bounds[3] - bounds[2], bounds[5] - bounds[4]]
        )
        value = np.max(np.sqrt(np.sum(max_node_resp**2, axis=1)))
        alpha_ = max_bound / obj.bound_fact / value
        alpha_ = alpha_ * alpha if alpha else alpha_
    else:
        alpha_ = 0
    # ------------------------------------------------------------------------
    # Start plot
    # -------------------------------------------------------------------------
    plotter = pv.Plotter(notebook=obj.notebook, line_smoothing=True)

    def create_mesh(value):
        step = int(round(value)) - 1
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
        node_resp = node_resp_steps[resp_type][step]
        node_deform_coords = alpha_ * node_resp + node_nodeform_coords
        scalars = np.sqrt(np.sum(node_resp**2, axis=1))
        plotter.clear_actors()  # !!!!!!
        _ = _generate_all_mesh(
            plotter,
            node_deform_coords,
            scalars,
            opacity,
            obj.color_map,
            lines_cells=lines_cells,
            face_cells=faces_cells,
            show_origin=show_origin,
            points_origin=node_nodeform_coords,
            point_size=obj.point_size,
            line_width=obj.line_width,
            show_face_line=show_face_line,
            clim=[cmin, cmax],
        )

        plotter.add_scalar_bar(fmt="%.3e", n_labels=10, label_font_size=12)

        plotter.add_text(
            "OpenSees 3D View",
            position="upper_left",
            shadow=True,
            font_size=16,
            # color="black",
            font="courier",
        )
        plotter.add_text(
            "peak of {}, step: {}\n"
            "min.x = {:.3E}  max.x = {:.3E}\n"
            "min.y = {:.3E}  max.y = {:.3E}\n"
            "min.z = {:.3E}  max.z = {:.3E}\n".format(
                response,
                step + 1,
                np.min(node_resp[:, 0]),
                np.max(node_resp[:, 0]),
                np.min(node_resp[:, 1]),
                np.max(node_resp[:, 1]),
                np.min(node_resp[:, 2]),
                np.max(node_resp[:, 2]),
            ),
            position="upper_right",
            shadow=True,
            font_size=12,
            # color="black",
            font="courier",
        )

        if show_outline:
            plotter.show_bounds(
                grid=False,
                location="outer",
                bounds=bounds,
                show_zaxis=True,
                # color="black",
            )
        plotter.add_axes()

    if slider:
        _ = plotter.add_slider_widget(
            create_mesh,
            [1, num_steps],
            value=num_steps,
            pointa=(0.0, 0.9),
            pointb=(0.5, 0.9),
            title="Step",
            title_opacity=1,
            # title_color="black",
            fmt="%.0f",
            title_height=0.03,
            slider_width=0.03,
            tube_width=0.01,
        )
    # -------------------------------------------------------------------------
    else:  # plot a single step
        create_mesh(max_step + 1)
    plotter.view_isometric()
    if np.max(model_dims) <= 2:
        plotter.view_xy(negative=False)
    if save_fig:
        plotter.save_graphic(save_fig)
    plotter.enable_anti_aliasing("msaa")
    plotter.show(title=obj.title)
    plotter.close()


def _deform_anim(
    obj,
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
    resp_type = response.lower()
    if resp_type not in ["disp", "vel", "accel"]:
        raise ValueError("response must be 'disp', 'vel', or 'accel'!")

    filename = obj.out_dir + "/" + input_file
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
    max_resps = [
        np.max(np.sqrt(np.sum(resp_**2, axis=1)))
        for resp_ in node_resp_steps[resp_type]
    ]
    max_step = np.argmax(max_resps)
    max_node_resp = node_resp_steps[resp_type][max_step]
    scalars = np.sqrt(np.sum(max_node_resp**2, axis=1))
    cmin, cmax = np.min(scalars), np.max(scalars)
    if model_update:
        bounds = model_info_steps["bound"][0]
        model_dims = model_info_steps["model_dims"][0]
    else:
        bounds = model_info_steps["bound"]
        model_dims = model_info_steps["model_dims"]
    # scale factor
    if resp_type == "disp":
        max_bound = np.max(
            [bounds[1] - bounds[0], bounds[3] - bounds[2], bounds[5] - bounds[4]]
        )
        value = np.max(np.sqrt(np.sum(max_node_resp**2, axis=1)))
        alpha_ = max_bound / obj.bound_fact / value
        alpha_ = alpha_ * alpha if alpha else alpha_
    else:
        alpha_ = 0
    # -----------------------------------------------------------------------------
    # start plot
    plotter = pv.Plotter(notebook=obj.notebook, line_smoothing=True)

    def creat_mesh(step):
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
        node_resp = node_resp_steps[resp_type][step]
        node_deform_coords = alpha_ * node_resp + node_nodeform_coords
        scalars = np.sqrt(np.sum(node_resp**2, axis=1))
        plotter.clear_actors()  # !!!!!!
        point_plot, line_plot, face_plot = _generate_all_mesh(
            plotter,
            node_deform_coords,
            scalars,
            opacity,
            obj.color_map,
            lines_cells=lines_cells,
            face_cells=faces_cells,
            point_size=obj.point_size,
            line_width=obj.line_width,
            show_face_line=show_face_line,
            clim=[cmin, cmax],
        )

        plotter.add_scalar_bar(fmt="%.3e", n_labels=10, label_font_size=12)

        txt = plotter.add_text(
            "peak of {}, step: {}\n"
            "min.x = {:.3E}  max.x = {:.3E}\n"
            "min.y = {:.3E}  max.y = {:.3E}\n"
            "min.z = {:.3E}  max.z = {:.3E}\n".format(
                resp_type,
                step + 1,
                np.min(node_resp[:, 0]),
                np.max(node_resp[:, 0]),
                np.min(node_resp[:, 1]),
                np.max(node_resp[:, 1]),
                np.min(node_resp[:, 2]),
                np.max(node_resp[:, 2]),
            ),
            position="upper_right",
            font_size=12,
            # color="black",
            font="courier",
        )

        if show_outline:
            plotter.show_bounds(
                grid=False,
                location="outer",
                bounds=bounds,
                show_zaxis=True,
                # color="black",
            )
        plotter.add_axes()
        # plotter.add_text('OpenSees 3D View', position='upper_left', font_size=16, color='black', font='courier')
        plotter.view_isometric()
        if np.max(model_dims) <= 2:
            plotter.view_xy(negative=False)
        return point_plot, line_plot, face_plot, txt

    # animation
    # ----------------------------------------------------------------------------
    if save_fig.endswith(".gif"):
        plotter.open_gif(save_fig, fps=framerate)
    else:
        plotter.open_movie(save_fig, framerate=framerate)
    # plotter.write_frame()  # write initial data
    for step in range(num_steps):
        _ = creat_mesh(step)
        plotter.write_frame()

    # ----------------------------------------------------------------------------------
    plotter.enable_anti_aliasing("msaa")
    plotter.show(title=obj.title)
    plotter.close()


def _frame_resp_vis(
    obj,
    input_file: str = "BeamRespStepData-1.hdf5",
    ele_tags: list = None,
    slider: bool = False,
    response: str = "Mz",
    show_values=True,
    alpha: float = 1.0,
    opacity: float = 1,
    save_fig: str = "FrameRespVis.svg",
):
    check_file(save_fig, [".svg", ".eps", ".ps", "pdf", ".tex"])
    filename = obj.out_dir + "/" + input_file
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
    beam_tags = beam_infos["beam_tags"]
    if len(beam_tags) == 0:
        warnings.warn("Model has no frame elements!")
        return None
    ylocals = beam_infos["ylocal"]
    zlocals = beam_infos["zlocal"]
    ylocal_map = {beam_tags[i]: ylocals[i] for i in range(len(beam_tags))}
    zlocal_map = {beam_tags[i]: zlocals[i] for i in range(len(beam_tags))}
    local_forces_step = beam_resp_step["localForces"]
    num_steps = len(local_forces_step)

    if ele_tags is None:
        ele_tags = beam_tags
        beam_node_coords = beam_infos["beam_node_coords"]
        beam_cells = beam_infos["beam_cells"]
        beam_cell_map = {beam_tags[i]: i for i in range(len(beam_tags))}
        idxs = range(len(beam_tags))
    else:
        ele_tags = np.atleast_1d(ele_tags)
        beam_node_coords = []
        beam_cells = []
        idxs = []
        beam_cell_map = {}
        for i, eletag in enumerate(ele_tags):
            idx = beam_infos["beam_cell_map"][eletag]
            idxs.append(idx)
            beam_cell_map[eletag] = i
            nodei, nodej = beam_infos["beam_cells"][idx, 1:]
            beam_node_coords.append(beam_infos["beam_node_coords"][nodei])
            beam_node_coords.append(beam_infos["beam_node_coords"][nodej])
            beam_cells.append([2, 2 * i, 2 * i + 1])
        beam_node_coords = np.array(beam_node_coords)
        beam_cells = np.array(beam_cells)

    idx_plottype_map = dict(
        fx=[0, 6], fy=[1, 7], fz=[2, 8], my=[4, 10], mz=[5, 11], mx=[3, 9]
    )
    f_sign_map = dict(
        fx=[-1, 1], fy=[-1, 1], fz=[-1, 1], my=[1, -1], mz=[-1, 1], mx=[1, -1]
    )
    axis_sign_map = dict(fx=1, fy=1, fz=1, my=-1, mz=-1, mx=-1)
    axis_map_map = dict(
        fx=zlocal_map,
        fy=ylocal_map,
        fz=zlocal_map,
        my=zlocal_map,
        mz=ylocal_map,
        mx=zlocal_map,
    )
    idx_plottype = idx_plottype_map[response.lower()]
    axis_map = axis_map_map[response.lower()]
    axis_sign = axis_sign_map[response.lower()]
    local_forces_step = [
        data[:, idx_plottype][idxs] * np.array(f_sign_map[response.lower()])
        for data in local_forces_step
    ]  # new

    maxv = [np.max(np.abs(data)) for data in local_forces_step]
    maxstep = np.argmax(maxv)
    local_forces_max = local_forces_step[maxstep]
    cmin, cmax = np.min(local_forces_max), np.max(local_forces_max)
    max_coord = np.max(beam_node_coords, axis=0)
    min_coord = np.min(beam_node_coords, axis=0)
    max_bound = np.max(max_coord - min_coord)
    maxv = np.amax(np.abs(local_forces_max))
    alpha_ = max_bound / maxv / obj.bound_fact
    alpha_ = alpha_ * alpha if alpha else alpha_

    # ------------------------------------------------------------------------
    # start plot
    # -------------------------------------------------------------------------
    plotter = pv.Plotter(notebook=obj.notebook, line_smoothing=True)

    def create_mesh(value):
        step = int(round(value)) - 1
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
                resp_cells.extend([4, n, n + 1, n + 2, n + 3])
                scalars.extend([f1_, f2_, f2_, f1_])
            else:
                ratio = np.abs(f2 / f1)
                ratio = 1 / (ratio + 1)
                coord0 = coord1 + (coord2 - coord1) * ratio
                resp_points.extend([coord1, coord0, coord4, coord2, coord0, coord3])
                resp_cells.extend([3, n, n + 1, n + 2])
                resp_cells.extend([3, n + 3, n + 4, n + 5])
                scalars.extend([f1_, 0, f1_, f2_, 0, f2_])
        labels = [f"{label:.2E}" for label in labels]
        label_poins = np.array(label_poins)
        resp_points = np.array(resp_points)
        scalars = np.array(scalars)
        #  ---------------------------------
        plotter.clear_actors()  # !!!!!!
        point_plot = pv.PolyData(beam_node_coords)
        plotter.add_mesh(
            point_plot,
            color=obj.color_point,
            point_size=obj.point_size,
            render_points_as_spheres=True,
            show_scalar_bar=False,
        )
        line_plot = _generate_mesh(beam_node_coords, beam_cells, kind="line")
        plotter.add_mesh(
            line_plot,
            color="black",
            render_lines_as_tubes=True,
            line_width=obj.line_width / 3,
            show_scalar_bar=False,
        )

        resp_plot = _generate_mesh(resp_points, resp_cells, kind="face")
        resp_plot.point_data["data0"] = scalars
        plotter.add_mesh(
            resp_plot,
            colormap=obj.color_map,
            scalars=scalars,
            clim=[cmin, cmax],
            show_edges=False,
            opacity=opacity,
            interpolate_before_map=True,
            show_scalar_bar=False,
        )
        plotter.add_scalar_bar(
            fmt="%.3e",
            n_labels=10,
            label_font_size=12,
            title=response,
        )
        plotter.add_axes()
        plotter.add_text(
            "OpenSees 3D View",
            position="upper_left",
            font_size=15,
            # color="black",
            font="courier",
            viewport=True,
        )
        plotter.add_text(
            "peak of {}, step: {}\n"
            "min = {:.3E}\nmax = {:.3E}\n".format(
                response, step + 1, np.min(scalars), np.max(scalars)
            ),
            position="upper_right",
            shadow=True,
            font_size=12,
            # color="black",
            font="courier",
        )
        if show_values:
            plotter.add_point_labels(
                label_poins,
                labels,
                # text_color="white",
                font_size=10,
                bold=False,
                always_visible=True,
            )

    if slider:
        _ = plotter.add_slider_widget(
            create_mesh,
            [1, num_steps],
            value=num_steps,
            pointa=(0.0, 0.9),
            pointb=(0.5, 0.9),
            title="Step",
            title_opacity=1,
            # title_color="black",
            fmt="%.0f",
            title_height=0.03,
            slider_width=0.03,
            tube_width=0.01,
        )
    # -------------------------------------------------------------------------
    else:  # plot a single step
        create_mesh(maxstep + 1)
    plotter.view_isometric()
    if np.max(np.abs(beam_node_coords[:, -1])) < 1e-5:
        plotter.view_xy(negative=False)
    if save_fig:
        plotter.save_graphic(save_fig)
    plotter.enable_anti_aliasing("msaa")
    plotter.show(title=obj.title)
    plotter.close()


def _generate_mesh(points, cells, kind="line"):
    """
    generate the mesh from the points and cells
    """
    if kind == "line":
        pltr = pv.PolyData()
        pltr.points = points
        pltr.lines = cells
    elif kind == "face":
        pltr = pv.PolyData()
        pltr.points = points
        pltr.faces = cells
    else:
        raise ValueError(f"not supported {kind}!")
    return pltr


def _generate_all_mesh(
    plotter,
    points,
    scalars,
    opacity,
    colormap,
    lines_cells,
    face_cells,
    show_origin=False,
    points_origin=None,
    show_scalar_bar=False,
    point_size=1,
    line_width=1,
    show_face_line=True,
    clim=None,
):
    """
    Auxiliary function for generating all meshes
    """
    if clim is None:
        clim = [np.min(scalars), np.max(scalars)]
    sargs = dict(
        title_font_size=16,
        label_font_size=12,
        shadow=True,
        n_labels=10,
        italic=False,
        fmt="%.3E",
        font_family="arial",
    )

    # point_plot = pv.PolyData(points)
    # point_plot.point_data["data0"] = scalars
    # plotter.add_mesh(
    #     point_plot,
    #     colormap=colormap,
    #     scalars=scalars,
    #     clim=clim,
    #     interpolate_before_map=True,
    #     point_size=point_size,
    #     render_points_as_spheres=True,
    #     show_scalar_bar=show_scalar_bar,
    #     scalar_bar_args=sargs,
    # )
    point_plot = None
    if len(lines_cells) > 0:
        if show_origin:
            line_plot_origin = _generate_mesh(points_origin, lines_cells, kind="line")
            plotter.add_mesh(
                line_plot_origin,
                color="gray",
                line_width=line_width / 2,
                show_scalar_bar=False,
            )
        line_plot = _generate_mesh(points, lines_cells, kind="line")
        line_plot.point_data["data0"] = scalars
        plotter.add_mesh(
            line_plot,
            colormap=colormap,
            scalars=scalars,
            interpolate_before_map=True,
            clim=clim,
            show_scalar_bar=show_scalar_bar,
            render_lines_as_tubes=True,
            line_width=line_width,
        )
    else:
        line_plot = None

    if len(face_cells) > 0:
        if show_origin:
            face_plot_origin = _generate_mesh(points_origin, face_cells, kind="face")
            plotter.add_mesh(
                face_plot_origin,
                color="gray",
                style="wireframe",
                show_scalar_bar=False,
                show_edges=True,
                line_width=line_width / 3,
            )
        face_plot = _generate_mesh(points, face_cells, kind="face")
        face_plot.point_data["data0"] = scalars
        plotter.add_mesh(
            face_plot,
            colormap=colormap,
            scalars=scalars,
            clim=clim,
            show_edges=show_face_line,
            opacity=opacity,
            interpolate_before_map=True,
            show_scalar_bar=show_scalar_bar,
        )
    else:
        face_plot = None

    return point_plot, line_plot, face_plot
