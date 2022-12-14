import warnings
import h5py
import numpy as np
import pyvista as pv

from ..utils import check_file, shape_dict


def _model_vis(
    obj,
    input_file: str = "ModelData.hdf5",
    show_node_label: bool = False,
    show_ele_label: bool = False,
    show_local_crd: bool = False,
    label_size: float = 8,
    show_outline: bool = True,
    opacity: float = 1.0,
    save_fig: str = 'ModelVis.svg'
):
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

    plotter = pv.Plotter(notebook=obj.notebook)
    plotter = _plot_model(obj, plotter, model_info, cells, opacity)

    plotter.add_text(
        "OpenSees 3D View",
        position="upper_left",
        font_size=15,
        # color="black",
        font="courier",
        viewport=True,
    )
    plotter.add_text(
        "Num. of Node: {0} \n Num. of Ele:{1}".format(
            model_info["num_node"], model_info["num_ele"]
        ),
        position="upper_right",
        font_size=10,
        # color="black",
        font="courier",
    )
    if show_outline:
        plotter.show_bounds(
            grid=False,
            location="outer",
            bounds=model_info["bound"],
            show_zaxis=True,
            # color="black",
        )
    if show_node_label:
        node_labels = ["N" + str(i) for i in model_info["NodeTags"]]
        plotter.add_point_labels(
            model_info["coord_no_deform"],
            node_labels,
            text_color="white",
            font_size=label_size,
            point_color=obj.color_point,
            render_points_as_spheres=True,
            point_size=1e-5,
            bold=False,
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
    beam_midpoints = model_info["beam_midpoints"]
    if len(beam_midpoints) == 0:
        warnings.warn("Model has no frame elements!")
        show_local_crd = False
    if show_local_crd:
        beam_xlocal = model_info["beam_xlocal"]
        beam_ylocal = model_info["beam_ylocal"]
        beam_zlocal = model_info["beam_zlocal"]
        length = model_info["max_bound"] / 250
        _ = plotter.add_arrows(beam_midpoints, beam_xlocal, mag=length,
                               color="red")
        _ = plotter.add_arrows(beam_midpoints, beam_ylocal, mag=length,
                               color="orange")
        _ = plotter.add_arrows(beam_midpoints, beam_zlocal, mag=length,
                               color="green")
        plotter.add_point_labels(
            beam_midpoints + length * beam_xlocal,
            ['x'] * beam_midpoints.shape[0],
            text_color="red",
            bold=False,
            shape=None,
            render_points_as_spheres=True,
            point_size=1.e-5,
            always_visible=True,
        )
        plotter.add_point_labels(
            beam_midpoints + length * beam_ylocal,
            ['y'] * beam_midpoints.shape[0],
            text_color="orange",
            bold=False,
            shape=None,
            render_points_as_spheres=True,
            point_size=1.e-5,
            always_visible=True,
        )
        plotter.add_point_labels(
            beam_midpoints + length * beam_zlocal,
            ['z'] * beam_midpoints.shape[0],
            text_color="green",
            bold=False,
            shape=None,
            render_points_as_spheres=True,
            point_size=1.e-5,
            always_visible=True,
        )
    plotter.add_axes()
    plotter.view_isometric()
    if np.max(model_info["model_dims"]) <= 2:
        plotter.view_xy(negative=False)
    if save_fig:
        plotter.save_graphic(save_fig)
    plotter.show(title=obj.title)
    plotter.close()


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
    save_fig: str = "EigenVis.svg"
):
    filename = obj.out_dir + '/' + input_file
    eigen_data = dict()
    with h5py.File(filename, "r") as f:
        grp = f["EigenInfo"]
        for name, value in grp.items():
            eigen_data[name] = value[...]
    # with shelve.open(filename) as db:
    #     eigen_data = db["EigenInfo"]

    f = eigen_data["f"]
    eigenvector = eigen_data["eigenvector"]
    num_mode_tag = len(f)
    modei, modej = mode_tags
    modei, modej = int(modei), int(modej)
    if modej > num_mode_tag:
        raise ValueError(
            f"Insufficient number of modes in eigen file {filename}!")

    # !subplots
    if subplots:
        if modej - modei + 1 > 49:
            raise ValueError(
                "When subplots True, mode_tag range must < 49 for clarify"
            )
        shape = shape_dict[modej - modei + 1]
        subplot_titles = []
        for i, idx in enumerate(range(modei, modej + 1)):
            txt = "Mode {}: T = {:.3f} s".format(idx, 1 / f[idx - 1])
            subplot_titles.append(txt)

        plotter = pv.Plotter(notebook=obj.notebook, shape=shape)
        for i, idx in enumerate(range(modei, modej + 1)):
            eigen_vec = eigenvector[idx - 1]
            if alpha is None:
                alpha_ = (
                    eigen_data["max_bound"] / obj.bound_fact /
                    np.max(np.sqrt(np.sum(eigen_vec ** 2, axis=1)))
                )
            else:
                alpha_ = alpha
            eigen_points = eigen_data["coord_no_deform"] + \
                eigen_vec * alpha_
            scalars = np.sqrt(np.sum(eigen_vec ** 2, axis=1))

            idxi = int(np.ceil((i + 1) / shape[1]) - 1)
            idxj = int(i - idxi * shape[1])

            # ------------------------------------------------------
            plotter.subplot(idxi, idxj)

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
                show_face_line=show_face_line
            )

            # plotter.add_scalar_bar(color='#000000', n_labels=10, label_font_size=8)
            # txt = 'Mode {}\nf = {:.3f} Hz\nT = {:.3f} s'.format(i + 1, f[i], 1 / f[i])
            txt = "Mode {} T = {:.3f} s".format(idx, 1 / f[idx - 1])
            plotter.add_text(
                txt,
                position="upper_right",
                font_size=10,
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
                    font_size=10,
                )
            plotter.add_axes(color="black")

            plotter.link_views()
    # !slide style
    else:
        plotter = pv.Plotter(notebook=obj.notebook)

        def create_mesh(value):
            step = int(round(value)) - 1
            eigen_vec = eigenvector[step]
            if alpha is None:
                alpha_ = (
                    eigen_data["max_bound"] / obj.bound_fact /
                    np.max(np.sqrt(np.sum(eigen_vec ** 2, axis=1)))
                )
            else:
                alpha_ = alpha
            eigen_points = eigen_data["coord_no_deform"] + \
                eigen_vec * alpha_
            scalars = np.sqrt(np.sum(eigen_vec ** 2, axis=1))
            cmin = np.min(scalars)
            cmax = np.max(scalars)
            plotter.clear_actors()
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
                show_face_line=show_face_line
            )

            plotter.add_scalar_bar(
                fmt="%.3e", n_labels=10, label_font_size=12
            )

            # txt = 'Mode {}\nf = {:.3f} Hz\nT = {:.3f} s'.format(mode_tag, f_, 1 / f_)
            txt = "Mode {}\nT = {:.3f} s".format(step + 1, 1 / f[step])
            plotter.add_text(
                txt, position="upper_left", font_size=12, font="courier"
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

        slider = plotter.add_slider_widget(
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
    plotter.show(title=obj.title)
    plotter.close()


def _eigen_anim(
    obj,
    mode_tag: int = 1,
    input_file: str = 'EigenData.hdf5',
    alpha: float = None,
    show_outline: bool = False,
    opacity: float = 1,
    framerate: int = 3,
    show_face_line: bool = True,
    save_fig: str = "EigenAnimation.gif"
):
    filename = obj.out_dir + '/' + input_file
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
    if alpha is None:
        alpha_ = (
            eigen_data["max_bound"]
            / obj.bound_fact
            / np.max(np.sqrt(np.sum(eigen_vec ** 2, axis=1)))
        )
    else:
        alpha_ = alpha
    eigen_points = eigen_data["coord_no_deform"] + eigen_vec * alpha_
    anti_eigen_points = eigen_data["coord_no_deform"] - eigen_vec * alpha_
    scalars = np.sqrt(np.sum(eigen_vec ** 2, axis=1))
    plt_points = [anti_eigen_points,
                  eigen_data["coord_no_deform"], eigen_points]
    # -----------------------------------------------------------------------------
    # start plot
    plotter = pv.Plotter(notebook=obj.notebook)

    if alpha is None:
        alpha_ = (
            eigen_data["max_bound"] / obj.bound_fact /
            np.max(np.sqrt(np.sum(eigen_vec ** 2, axis=1)))
        )
    else:
        alpha_ = alpha
    eigen_points = eigen_data["coord_no_deform"] + eigen_vec * alpha_
    anti_eigen_points = eigen_data["coord_no_deform"] - eigen_vec * alpha_
    scalars = np.sqrt(np.sum(eigen_vec ** 2, axis=1))
    point_plot, line_plot, face_plot = _generate_all_mesh(plotter,
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

    plotter.add_scalar_bar(
        fmt="%.3E", n_labels=10, label_font_size=12
    )

    plotter.add_text(
        "Mode {}\nf = {:.3f} Hz\nT = {:.3f} s".format(
            mode_tag, f_, 1 / f_),
        position="upper_right",
        font_size=12,
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
        plotter.open_gif(save_fig, fps=framerate)
    else:
        plotter.open_movie(save_fig, framerate=framerate)
    plt_points = [anti_eigen_points,
                  eigen_data["coord_no_deform"], eigen_points]
    render = False
    index = [2, 0] * 3
    plotter.write_frame()  # write initial data
    for idx in index:
        points = plt_points[idx]
        xyz = (eigen_data["coord_no_deform"] - points) / alpha_
        xyz_eigen = np.sqrt(np.sum(xyz ** 2, axis=1))
        if point_plot:
            plotter.update_coordinates(
                points, mesh=point_plot, render=render)
            plotter.update_scalars(
                scalars=xyz_eigen, mesh=point_plot, render=render)
        if line_plot:
            plotter.update_scalars(
                scalars=xyz_eigen, mesh=line_plot, render=render)
            plotter.update_coordinates(
                points, mesh=line_plot, render=render)
        if face_plot:
            plotter.update_scalars(
                scalars=xyz_eigen, mesh=face_plot, render=render)
            plotter.update_coordinates(
                points, mesh=face_plot, render=render)
        plotter.update_scalar_bar_range(
            clim=[np.min(xyz_eigen), np.max(xyz_eigen)], name=None
        )
        plotter.write_frame()
    # ----------------------------------------------------------------------------------
    plotter.show(title=obj.title)
    plotter.close()


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
    save_fig: str = "DefoVis.svg",
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

    # with shelve.open(filename) as db:
    #     model_info_steps = db["ModelInfoSteps"]
    #     cell_steps = db["CellSteps"]
    #     node_resp_steps = db["NodeRespSteps"]

    num_steps = len(node_resp_steps["disp"])

    # ! max response
    max_resps = [np.max(np.sqrt(np.sum(resp_ ** 2, axis=1)))
                 for resp_ in node_resp_steps[resp_type]]
    max_step = np.argmax(max_resps)
    max_node_resp = node_resp_steps[resp_type][max_step]
    scalars = np.sqrt(np.sum(max_node_resp ** 2, axis=1))
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
    # Start plot
    # -------------------------------------------------------------------------
    plotter = pv.Plotter(notebook=obj.notebook)

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
        scalars = np.sqrt(np.sum(node_resp ** 2, axis=1))
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
            clim=[cmin, cmax]
        )

        plotter.add_scalar_bar(
            fmt="%.3e", n_labels=10, label_font_size=12
        )

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
    plotter.show(title=obj.title)
    plotter.close()


def _deform_anim(
    obj,
    input_file: str = "NodeRespStepData-1.hdf5",
    response: str = "disp",
    alpha: float = None,
    show_outline: bool = False,
    opacity: float = 1,
    framerate: int = 24,
    show_face_line: bool = True,
    save_fig: str = "DefoAnimation.gif",
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

    # ! max response
    max_resps = [np.max(np.sqrt(np.sum(resp_ ** 2, axis=1)))
                 for resp_ in node_resp_steps[resp_type]]
    max_step = np.argmax(max_resps)
    max_node_resp = node_resp_steps[resp_type][max_step]
    scalars = np.sqrt(np.sum(max_node_resp ** 2, axis=1))
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
    plotter = pv.Plotter(notebook=obj.notebook)

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
        scalars = np.sqrt(np.sum(node_resp ** 2, axis=1))
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
            clim=[cmin, cmax]
        )

        plotter.add_scalar_bar(
            fmt="%.3e", n_labels=10, label_font_size=12
        )

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
    if model_update:
        for step in range(num_steps):
            point_plot, line_plot, face_plot, txt = creat_mesh(step)
            plotter.write_frame()
    else:
        point_plot, line_plot, face_plot, txt = creat_mesh(0)
        for step in range(num_steps):
            node_nodeform_coords = model_info_steps["coord_no_deform"]
            node_resp = node_resp_steps[resp_type][step]
            node_deform_coords = alpha_ * node_resp + node_nodeform_coords
            scalars = np.sqrt(np.sum(node_resp ** 2, axis=1))
            if point_plot:
                if resp_type == "disp":
                    plotter.update_coordinates(
                        node_deform_coords, mesh=point_plot, render=False
                    )
            if line_plot is not None:
                if resp_type == "disp":
                    plotter.update_coordinates(
                        node_deform_coords, mesh=line_plot, render=False
                    )
                plotter.update_scalars(
                    scalars, mesh=line_plot, render=False)
            if face_plot is not None:
                if resp_type == "disp":
                    plotter.update_coordinates(
                        node_deform_coords, mesh=face_plot, render=False
                    )
                plotter.update_scalars(
                    scalars, mesh=face_plot, render=False)
            # plotter.update_scalar_bar_range(clim=[np.min(scalars), np.max(scalars)])
            plotter.write_frame()
            if step < num_steps - 1:
                plotter.remove_actor(txt)
    # ----------------------------------------------------------------------------------
    plotter.show(title=obj.title)
    plotter.close()


def _frame_resp_vis(obj,
                    input_file: str = "BeamRespStepData-1.hdf5",
                    ele_tags: list[int] = None,
                    slider: bool = False,
                    response: str = "Mz",
                    show_values=True,
                    alpha: float = None,
                    opacity: float = 1,
                    save_fig: str = "FrameRespVis.svg"
                    ):
    check_file(save_fig, ['.svg', '.eps', '.ps', 'pdf', '.tex'])
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
    # start plot
    # -------------------------------------------------------------------------
    plotter = pv.Plotter(notebook=obj.notebook)

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
                resp_points.extend(
                    [coord1, coord0, coord4, coord2, coord0, coord3])
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
        line_plot = _generate_mesh(
            beam_node_coords, beam_cells, kind="line")
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
            fmt="%.3e", n_labels=10, label_font_size=12, title=response,
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
    clim=None
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
            line_plot_origin = _generate_mesh(
                points_origin, lines_cells, kind="line"
            )
            plotter.add_mesh(
                line_plot_origin,
                color="gray",
                line_width=line_width / 3,
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
            face_plot_origin = _generate_mesh(
                points_origin, face_cells, kind="face"
            )
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
            line_width=obj.line_width / 5,
        )

    if len(cells["beam"]) > 0:
        beam_plot = _generate_mesh(
            model_info["coord_no_deform"], cells["beam"], kind="line"
        )
        plotter.add_mesh(
            beam_plot,
            color=obj.color_line,
            render_lines_as_tubes=False,
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
    return plotter
