import h5py
import warnings
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection, PatchCollection
from matplotlib.tri import Triangulation
from matplotlib.widgets import Slider
from ._plotly_base import _reshape_cell
from ..utils import shape_dict

plt.rc("font", family="Times New Roman")
plt.rcParams["mathtext.fontset"] = "cm"


class OpsVis2D:
    def __init__(
        self,
        point_size: float = 10,
        line_width: float = 3,
        colors_dict: dict = None,
        cmap: str = "jet",
        results_dir: str = "opstool_output",
    ):
        self.point_size = point_size
        self.line_width = line_width
        self.title = "OpenSeesVispy"
        # Initialize the color dict
        colors = dict(
            point="#de0f17",
            line="#2529d8",
            face="#00a78e",
            solid="#f47721",
            truss="#7d3f98",
            link="#7ac143",
            constraint="#1cc7d0",
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
        self.color_map = cmap
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
        local_crd_alpha: float = 1.0,
        show_fix_node: bool = True,
        fix_node_alpha: float = 1.0,
        show_load: bool = False,
        load_alpha: float = 1.0,
        show_constrain_dof: bool = False,
        label_size: float = 10,
        show_outline: bool = True,
        opacity: float = 1.0,
    ):
        filename = self.out_dir + "/" + input_file
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
            if "_tags" not in name:
                cells[name] = _reshape_cell(value)
        points = model_info["coord_no_deform"]
        bounds = model_info["bound"]
        aspect_ratio = (np.max(points[:, 1]) - np.min(points[:, 1])) / (
            np.max(points[:, 0]) - np.min(points[:, 0])
        )

        figsize = (8 / aspect_ratio, 8) if aspect_ratio > 1 else (8, 8 * aspect_ratio)

        fig, ax = plt.subplots(figsize=figsize)

        # >>> point plot
        _plot_point(ax, points=points, size=self.point_size, color=self.color_point)
        # >>> line plot
        line_cells = [cells["truss"], cells["link"], cells["beam"], cells["other_line"]]
        line_colors = [
            self.color_truss,
            self.color_link,
            self.color_line,
            self.color_line,
        ]
        line_widths = [
            self.line_width,
            0.5 * self.line_width,
            self.line_width,
            self.line_width,
        ]
        for i in range(len(line_cells)):
            if len(line_cells[i]) > 0:
                _plot_line(
                    ax,
                    points=points,
                    cells=line_cells[i],
                    color=line_colors[i],
                    width=line_widths[i],
                )
        # >>> face plot
        face_cells = [cells["plane"], cells["tetrahedron"], cells["brick"]]
        face_colors = [self.color_face, self.color_solid, self.color_solid]
        for ii in range(len(face_cells)):
            if len(face_cells[ii]) > 0:
                _plot_face(
                    ax,
                    points=points,
                    cells=face_cells[ii],
                    opacity=opacity,
                    lw=self.line_width / 3,
                    color=face_colors[ii],
                )
        if show_node_label:
            node_labels = [f"N{i}" for i in model_info["NodeTags"]]
            for p, label in zip(points, node_labels):
                ax.annotate(
                    label,
                    p[:2],
                    xytext=(5, 5),
                    textcoords="offset pixels",
                    fontsize=label_size,
                    color="#580f41",
                    zorder=200,
                )
        if show_ele_label:
            ele_labels = [f"E{i}" for i in model_info["EleTags"]]
            for p, label in zip(model_info["coord_ele_midpoints"], ele_labels):
                ax.annotate(
                    label,
                    p[:2],
                    xytext=(0, 0),
                    textcoords="offset pixels",
                    fontsize=label_size,
                    color="#7b0323",
                    zorder=200,
                )
        if show_local_crd:
            _show_beam_local_axes(ax, model_info, local_crd_alpha)
            _show_link_local_axes(ax, model_info, local_crd_alpha)
        _show_mp_constraint(
            ax,
            model_info,
            color=self.color_constraint,
            width=self.line_width / 2,
            show_dofs=show_constrain_dof,
            label_size=label_size,
        )
        if show_fix_node:
            _show_fix_node(
                ax,
                model_info,
                color="#01ff07",
                width=self.line_width / 3,
                alpha=fix_node_alpha,
            )
        if show_load:
            _show_node_load(ax, model_info, load_alpha)
            _show_ele_load(ax, model_info, load_alpha)
        # txt1 = f"OpenSees 2D View"
        # ax.text(0.01, 1.01, txt1, fontsize=label_size+2, ha='left', va='bottom',
        #         transform=ax.transAxes)
        # txt2 = f"Num. of Node:{model_info['num_node']} || Num. of Ele:{model_info['num_ele']}"
        # ax.text(0.99, 1.01, txt2, fontsize=label_size, ha='right', va='bottom',
        #         transform=ax.transAxes)
        space = (bounds[1] - bounds[0]) / 5
        ax.set_xlim(bounds[0] - space, bounds[1] + space)
        space = (bounds[3] - bounds[2]) / 5
        ax.set_ylim(bounds[2] - space, bounds[3] + space)
        ax.tick_params(labelsize=12)
        if not show_outline:
            ax.axis("off")
        plt.tight_layout()
        plt.show()

    def eigen_vis(
        self,
        mode_tags: list,
        input_file: str = "EigenData.hdf5",
        subplots: bool = False,
        alpha: float = 1.0,
        show_outline: bool = False,
        show_origin: bool = False,
        show_point: bool = False,
        show_face_line: bool = True,
        show_cmap: bool = True,
        opacity: float = 1.0,
    ):
        filename = self.out_dir + "/" + input_file
        eigen_data = dict()
        with h5py.File(filename, "r") as f:
            grp = f["EigenInfo"]
            for name, value in grp.items():
                eigen_data[name] = value[...]
        # eigen info
        f = eigen_data["f"]
        eigenvector = eigen_data["eigenvector"]
        num_mode_tag = len(f)
        modei, modej = mode_tags
        modei, modej = int(modei), int(modej)
        if modej > num_mode_tag:
            raise ValueError(f"Insufficient number of modes in eigen file {filename}!")
        ps_ = eigen_data["coord_no_deform"]
        aspect_ratio = (np.max(ps_[:, 1]) - np.min(ps_[:, 1])) / (
            np.max(ps_[:, 0]) - np.min(ps_[:, 0])
        )
        if aspect_ratio > 2:
            aspect_ratio = 2.0
        if aspect_ratio < 0.5:
            aspect_ratio = 0.5
        cmap = self.color_map if show_cmap else None

        def create_mesh(value_i):
            step = int(round(value_i)) - 1
            eigen_veci = eigenvector[step]
            value_i = np.max(np.sqrt(np.sum(eigen_veci**2, axis=1)))
            alpha_i = eigen_data["max_bound"] / self.bound_fact / value_i
            alpha_i *= alpha if alpha is not None else alpha_i
            eigen_pointsi = eigen_data["coord_no_deform"] + eigen_veci * alpha_i
            scalarsi = np.sqrt(np.sum(eigen_veci**2, axis=1))

            ax.clear()
            if show_point:
                _plot_point(
                    ax,
                    eigen_pointsi,
                    self.point_size,
                    color="blue",
                    cmap=cmap,
                    scalars=scalarsi,
                    clim=(np.min(scalarsi), np.max(scalarsi)),
                )
            if len(eigen_data["all_lines"]) > 0:
                _plot_line(
                    ax,
                    eigen_pointsi,
                    _reshape_cell(eigen_data["all_lines"]),
                    width=self.line_width,
                    color="blue",
                    cmap=cmap,
                    n_segs=50,
                    scalars=scalarsi,
                    clim=(np.min(scalarsi), np.max(scalarsi)),
                )
                if show_origin:
                    _plot_line(
                        ax,
                        eigen_data["coord_no_deform"],
                        _reshape_cell(eigen_data["all_lines"]),
                        width=self.line_width / 3,
                        color="gray",
                    )
            if len(eigen_data["all_faces"]) > 0:
                if cmap:
                    _plot_face(
                        ax,
                        eigen_pointsi,
                        _reshape_cell(eigen_data["all_faces"]),
                        lw=0.75,
                        color="blue",
                        cmap=self.color_map,
                        opacity=opacity,
                        scalars=scalarsi,
                        clim=(np.min(scalarsi), np.max(scalarsi)),
                    )
                    if show_face_line:
                        _plot_wireframe(
                            ax,
                            eigen_pointsi,
                            _reshape_cell(eigen_data["all_faces"]),
                            lw=self.line_width / 5,
                            color="k",
                        )
                else:
                    _plot_wireframe(
                        ax,
                        eigen_pointsi,
                        _reshape_cell(eigen_data["all_faces"]),
                        lw=self.line_width,
                        color="blue",
                    )
                if show_origin:
                    _plot_wireframe(
                        ax,
                        eigen_data["coord_no_deform"],
                        _reshape_cell(eigen_data["all_faces"]),
                        lw=self.line_width / 3,
                        color="gray",
                    )
            txti = "Mode {} T = {:.3f} s".format(step + 1, 1 / f[step])
            ax.text(
                0.01,
                1.01,
                txti,
                va="bottom",
                ha="left",
                fontsize=10,
                transform=ax.transAxes,
            )
            minboundi, maxboundi = np.min(eigen_pointsi, axis=0), np.max(
                eigen_pointsi, axis=0
            )
            spacei = (maxboundi - minboundi) / 20
            ax.set(
                xlim=((minboundi - spacei)[0], (maxboundi + spacei)[0]),
                ylim=((minboundi - spacei)[1], (maxboundi + spacei)[1]),
            )
            ax.tick_params(labelsize=10)
            # ax.set_aspect(aspect_ratio)
            if not show_outline:
                ax.axis("off")
            fig.canvas.draw_idle()

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
            if aspect_ratio < 1:
                figsize = (4 * shape[1], 4 * aspect_ratio * shape[0])
            else:
                figsize = (4 / aspect_ratio * shape[1], 4 * shape[0])
            fig, axs = plt.subplots(*shape, figsize=figsize)
            for i, idx in enumerate(range(modei, modej + 1)):
                idxi = int(np.ceil((i + 1) / shape[1]) - 1)
                idxj = int(i - idxi * shape[1])
                ax = axs[idxj] if shape[0] == 1 else axs[idxi, idxj]
                create_mesh(idx)
            plt.tight_layout(pad=0.2)
        else:
            figsize = (
                (6, 6 * aspect_ratio) if aspect_ratio <= 1 else (6 / aspect_ratio, 6)
            )
            fig, ax = plt.subplots(figsize=figsize)
            create_mesh(modei)
            fig.subplots_adjust(left=0.2, bottom=0.2)
            axslider = fig.add_axes([0.2, 0.05, 0.5, 0.05])
            mode_slider = Slider(
                ax=axslider,
                label="Mode",
                valmin=modei,
                valmax=modej,
                valinit=1,
                valfmt="%.0f",
            )
            mode_slider.on_changed(create_mesh)
        plt.show()

    def deform_vis(self):
        pass

    def frame_resp_vis(self):
        pass


def _show_mp_constraint(ax, model_info, color, width, show_dofs, label_size):
    points = model_info["ConstrainedCoords"]
    cells = _reshape_cell(model_info["ConstrainedCells"])
    midcoords = model_info["ConstrainedMidCoords"]
    dofs = model_info["ConstrainedDofs"]
    dofs = ["".join([str(k) for k in dof if k != -1]) for dof in dofs]
    if len(cells) > 0:
        _plot_line(ax, points, cells=cells, color=color, width=width)
        if show_dofs:
            for p, label in zip(midcoords, dofs):
                ax.annotate(
                    label,
                    p[:2],
                    xytext=(5, 5),
                    textcoords="offset pixels",
                    fontsize=label_size,
                    color=color,
                    zorder=200,
                )


def _show_fix_node(ax, model_info, color, width, alpha):
    fixed_dofs = model_info["FixNodeDofs"]
    fixed_coords = model_info["FixNodeCoords"]
    beam_lengths = model_info["beam_lengths"]
    if len(beam_lengths) > 0:
        s = np.mean(beam_lengths) / 5
    else:
        s = (model_info["max_bound"] + model_info["min_bound"]) / 50
    s *= alpha
    if len(fixed_coords) > 0:
        points = []
        for coord, dof in zip(fixed_coords, fixed_dofs):
            x, y, _ = coord
            if dof[0] == -1 and dof[1] == -1 and dof[2] == -1:
                points.extend(
                    [
                        [x - s / 2, y - s],
                        [x + s / 2, y - s],
                        [x + s / 2, y],
                        [x - s / 2, y],
                        [x - s / 2, y - s],
                        [x + s / 2, y],
                        [x - s / 2, y],
                        [x + s / 2, y - s],
                        [np.nan, np.nan],
                    ]
                )
            else:
                points.extend(
                    [
                        [x - s / 2, y - 0.866 * s],
                        [x + s / 2, y - 0.866 * s],
                        [x, y],
                        [x - s / 2, y - 0.866 * s],
                        [np.nan, np.nan],
                    ]
                )
        points = np.array(points)
        ax.plot(points[:, 0], points[:, 1], c=color, lw=width, zorder=80)


def _show_beam_local_axes(ax, model_info, alpha):
    beam_xlocal = model_info["beam_xlocal"]
    beam_ylocal = model_info["beam_ylocal"]
    beam_midpoints = model_info["beam_midpoints"]
    if len(beam_midpoints) > 0:
        ax.quiver(
            beam_midpoints[:, 0],
            beam_midpoints[:, 1],
            beam_xlocal[:, 0],
            beam_xlocal[:, 1],
            color="#cf6275",
            zorder=200,
        )
        ax.quiver(
            beam_midpoints[:, 0],
            beam_midpoints[:, 1],
            beam_ylocal[:, 0],
            beam_ylocal[:, 1],
            color="#04d8b2",
            zorder=200,
        )


def _show_link_local_axes(ax, model_info, alpha):
    link_xlocal = model_info["link_xlocal"]
    link_ylocal = model_info["link_ylocal"]
    link_midpoints = model_info["link_midpoints"]
    if len(link_midpoints) > 0:
        ax.quiver(
            link_midpoints[:, 0],
            link_midpoints[:, 1],
            link_xlocal[:, 0],
            link_xlocal[:, 1],
            color="#cf6275",
            zorder=200,
        )
        ax.quiver(
            link_midpoints[:, 0],
            link_midpoints[:, 1],
            link_ylocal[:, 0],
            link_ylocal[:, 1],
            color="#04d8b2",
            zorder=200,
        )


def _show_node_load(ax, model_info, alpha):
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
        alpha_ = np.mean(beam_lengths) / maxdata / 3.5
    else:
        alpha_ = (model_info["max_bound"] + model_info["min_bound"]) / 20 / maxdata
    alpha_ *= alpha
    patterntags = np.unique(node_load_info[:, 0])
    cmap = plt.get_cmap("Spectral")
    colors = cmap(np.linspace(0, 1, len(patterntags)))
    xyzlocals = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
    for p, ptag in enumerate(patterntags):
        idx = np.abs(node_load_info[:, 0] - ptag) < 1e-3
        coords = points[node_load_info[idx, -1]]
        for i in range(2):
            data = np.ravel(load_data[idx, i])
            axis = np.reshape(xyzlocals[i] * len(coords), (-1, 3))
            for j in range(len(axis)):
                axis[j] *= data[j] * alpha_
            if np.sum(np.abs(data)) > 1e-12:
                ax.quiver(
                    coords[:, 0],
                    coords[:, 1],
                    axis[:, 0],
                    axis[:, 1],
                    color=colors[p],
                    zorder=200,
                    pivot="tip",
                    angles="xy",
                    scale_units="xy",
                    scale=1,
                    width=0.003,
                    headwidth=4,
                    headlength=5,
                    headaxislength=4.5,
                )


def _show_ele_load(ax, model_info, alpha):
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
        alpha_ = np.mean(beam_lengths) / maxdata / 5
    else:
        alpha_ = (model_info["max_bound"] + model_info["min_bound"]) / 20 / maxdata
    alpha_ *= alpha
    cmap = plt.get_cmap("rainbow")
    colors = cmap(np.linspace(0, 1, len(patterntags)))
    for p, ptag in enumerate(patterntags):
        idx = np.abs(new_ptags - ptag) < 1e-3
        coords = new_points[idx]
        for i in range(3):
            data = np.ravel(load_data[idx, i])
            axis = new_locals[idx, 3 * i : 3 * i + 3]
            for j in range(len(axis)):
                axis[j] *= data[j] * alpha_
            if np.sum(np.abs(data)) > 1e-12:
                ax.quiver(
                    coords[:, 0],
                    coords[:, 1],
                    axis[:, 0],
                    axis[:, 1],
                    color=colors[p],
                    zorder=200,
                    pivot="tip",
                    angles="xy",
                    scale_units="xy",
                    scale=1,
                    width=0.003,
                    headwidth=4,
                    headlength=5,
                    headaxislength=4.5,
                )


def _plot_point(ax, points, size, color="black", cmap=None, scalars=None, clim=None):
    points = np.array(points)
    x, y = points[:, 0], points[:, 1]
    if cmap:
        sc = ax.scatter(
            x,
            y,
            s=size**2,
            c=scalars,
            marker="o",
            cmap=cmap,
            vmin=clim[0],
            vmax=clim[1],
            zorder=100,
        )
    else:
        sc = ax.scatter(
            x, y, s=size**2, c=color, marker="o", edgecolors="k", zorder=100
        )
    return sc


def _plot_line(
    ax,
    points,
    cells,
    width,
    color="blue",
    scalars=None,
    cmap=None,
    clim=None,
    n_segs=50,
):
    points = np.array(points)
    cells = np.array(cells)
    line_points = []
    line_scalars = []
    for cell in cells:
        data = points[cell[1:], :]
        xs_ = np.linspace(data[0, 0], data[1, 0], n_segs + 1)
        ys_ = np.linspace(data[0, 1], data[1, 1], n_segs + 1)
        for i in range(n_segs):
            line_points.append([[xs_[i], ys_[i]], [xs_[i + 1], ys_[i + 1]]])
        if cmap:
            xcs_ = np.arange(n_segs) + 0.5
            zs = np.interp(xcs_, [0, n_segs], scalars[cell[1:]])
            zs[0], zs[-1] = scalars[cell[1:]]
            line_scalars.extend(zs)
    line_points = np.array(line_points)
    line_scalars = np.array(line_scalars)
    if cmap:
        # norm = plt.Normalize(np.min(line_scalars), np.max(line_scalars))
        lc = LineCollection(
            line_points, linewidths=width, zorder=80, cmap=cmap, array=line_scalars
        )
        # Set the values used for colormapping
        lc.set(clim=clim)
        lc.set_array(line_scalars)
        ax.add_collection(lc)
    else:
        lc = LineCollection(line_points, linewidths=width, zorder=80)
        lc.set(color=color)
        ax.add_collection(lc)
    return lc


def _plot_face(
    ax,
    points,
    cells,
    lw=1.0,
    color="green",
    scalars=None,
    cmap=None,
    clim=None,
    opacity=1.0,
):
    points = np.array(points)
    cells = np.array(cells)
    if cmap:
        x, y = points[:, 0], points[:, 1]
        triangles = []
        for cell in cells:
            data0 = cell[1:]
            if data0.shape[0] == 3:
                triangles.append(data0)
            elif data0.shape[0] == 6:
                triangles.append([data0[0], data0[1], data0[5]])
                triangles.append([data0[1], data0[2], data0[3]])
                triangles.append([data0[3], data0[4], data0[5]])
                triangles.append([data0[1], data0[3], data0[5]])
            elif data0.shape[0] == 4:
                triangles.append([data0[0], data0[1], data0[2]])
                triangles.append([data0[0], data0[2], data0[3]])
            elif data0.shape[0] == 8:
                triangles.append([data0[0], data0[1], data0[7]])
                triangles.append([data0[1], data0[2], data0[3]])
                triangles.append([data0[3], data0[4], data0[5]])
                triangles.append([data0[5], data0[6], data0[7]])
                triangles.append([data0[3], data0[5], data0[7]])
                triangles.append([data0[1], data0[3], data0[7]])

        triangles = np.array(triangles)
        triangulation = Triangulation(x, y, triangles)
        obj = ax.tricontourf(
            triangulation,
            scalars,
            150,
            zorder=50,
            cmap=cmap,
            vmin=clim[0],
            vmax=clim[1],
        )
    else:
        patches = [
            plt.Polygon(points[face_link, :2], closed=True, alpha=opacity)
            for face_link in cells[:, 1:]
        ]
        obj = PatchCollection(
            patches,
            facecolors=color,
            edgecolors="k",
            linewidths=lw,
            zorder=60,
            alpha=opacity,
        )
        ax.add_collection(obj)
    return obj


def _plot_wireframe(
    ax,
    points,
    cells,
    lw=1.0,
    color="gray",
):
    points = np.array(points)
    cells = np.array(cells)
    line_points = []
    for cell in cells:
        data0 = points[cell[1:], :2]
        data = np.row_stack([data0, data0[0]])
        line_points.append(data)
    lc = LineCollection(line_points, linewidths=lw, zorder=60)
    lc.set(color=color)
    ax.add_collection(lc)
    return lc
