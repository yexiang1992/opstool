import h5py
import numpy as np

COLORS = dict(
    point="Maroon",
    line="Blue",
    face="Green",
    solid="Violet",
    truss="pink",
    link="SkyBlue",
    constraint="Lime",
)


def _write_head(file, width=12, height=30, d3: bool = True):
    with open(file, "w", encoding="utf8") as f:
        f.write("% This file was created by opstool, all rights reserved!\n")
        f.write("\\documentclass{standalone}\n")
        f.write("\\usepackage[dvipsnames, svgnames, x11names]{xcolor}\n")
        f.write(
            "\\usepackage[left=0cm,top=0cm,right=0cm,nohead,nofoot]{geometry}\n")
        f.write("\\usepackage{tikz}\n")
        if d3:
            f.write("\\usepackage{tikz-3dplot}\n")
        f.write("\\usepackage[siunitx]{circuitikz} %[symbols]\n")
        f.write("\\usepackage[outline]{contour} % glow around text\n")
        f.write("\\usetikzlibrary{arrows,arrows.meta}\n")
        f.write("\\usetikzlibrary{decorations.markings}\n")
        f.write("\\usepackage[active,tightpage]{preview}\n")
        f.write("\\PreviewEnvironment{tikzpicture}\n")
        if d3:
            # 120 degree azimuth and 30 degree of elevation
            f.write("\\tdplotsetmaincoords{120}{30}\n")
        f.write("\\setlength\PreviewBorder{2mm}\n\n")
        f.write(
            f"\\geometry{{paperwidth={width}cm, paperheight={height}cm, margin=0cm}}\n")
        f.write(
            f"\n\\tikzstyle{{link}}=[R,color={COLORS['link']},thick,{COLORS['link']}]\n")
        f.write(
            f"\\tikzstyle{{constraint}}=[short,color={COLORS['constraint']},thick,{COLORS['constraint']}]\n")
        f.write("\n\\begin{document}\n")
        if d3:
            f.write(
                "\n\\begin{tikzpicture}[tdplot_main_coords]\n\n")
        else:
            f.write("\n\\begin{tikzpicture}\n\n")


def _write_end(file):
    with open(file, "a", encoding="utf8") as f:
        f.write("\n\end{tikzpicture}\n")
        f.write("\n\end{document}\n")


def _def_points(file, points, d3):
    with open(file, "a", encoding="utf8") as f:
        if d3:
            for i, p in enumerate(points):
                f.write(
                    f"\coordinate (P{i}) at ({p[0]}, {p[1]}, {p[2]});\n")
        else:
            for i, p in enumerate(points):
                f.write(
                    f"\coordinate (P{i}) at ({p[0]}, {p[1]});\n")


def _write_points(file, points, size, opacity=1.0, color="black"):
    with open(file, "a", encoding="utf8") as f:
        for i, p in enumerate(points):
            f.write(
                f"\shade[ball color={color}, fill opacity={opacity}] (P{i}) circle ({size}pt);\n")


def _write_lines(file, cells, line_width, opacity,
                 line_color="black", line_type="beam"):
    cells = np.reshape(cells, (-1, 3))
    if len(cells) > 0:
        with open(file, "a", encoding="utf8") as f:
            for cell in cells:
                idx1 = cell[1]
                idx2 = cell[2]
                f.write(
                    f"\draw[{line_color},line width={line_width}pt, opacity={opacity}] "
                    f"(P{idx1}) -- (P{idx2});\n")
                # if line_type.lower() == "link":
                #     f.write(
                #         f"\draw[line width={line_width}pt] "
                #         f"(P{idx1}) to[link] (P{idx2});\n")
                # else:
                #     f.write(
                #         f"\draw[{line_color},line width={line_width}pt] "
                #         f"(P{idx1}) -- (P{idx2});\n")


def _write_constraint(file, model_info, scale, line_width, d3,
                      line_color="black"):
    points = model_info["ConstrainedCoords"] * scale
    cells = model_info["ConstrainedCells"]
    cells = np.reshape(cells, (-1, 3))
    midcoords = model_info["ConstrainedMidCoords"] * scale
    dofs = model_info["ConstrainedDofs"]
    dofs = ["".join([str(k) for k in dof]) for dof in dofs]
    if len(cells) > 0:
        if d3:
            with open(file, "a", encoding="utf8") as f:
                for cell, mp, dof in zip(cells, midcoords, dofs):
                    p1 = points[cell[1]]
                    p2 = points[cell[2]]
                    f.write(
                        f"\draw[{line_color},line width={line_width}pt] "
                        f"({p1[0]}, {p1[1]}, {p1[2]}) to[constraint] ({p2[0]}, {p2[1]}, {p2[2]});\n")
                    # f.write(
                    #     f"\path ({mp[0]}, {mp[1]}, {mp[2]}) "
                    #     f"node[above,{line_color},font=\\fontsize{{{label_size}pt}}{{{label_size}pt}}] {{{dof}}};\n")
        else:
            with open(file, "a", encoding="utf8") as f:
                for cell, mp, dof in zip(cells, midcoords, dofs):
                    p1 = points[cell[1]]
                    p2 = points[cell[2]]
                    f.write(
                        f"\draw[{line_color},line width={line_width}pt] "
                        f"({p1[0]}, {p1[1]}) to[constraint] ({p2[0]}, {p2[1]});\n")
                    # f.write(
                    #     f"\path ({mp[0]}, {mp[1]}) "
                    #     f"node[above,{line_color},font=\\fontsize{{{label_size}pt}}{{{label_size}pt}}] {{{dof}}};\n")


def _write_faces(file, cells, color, opacity):
    if len(cells) > 0:
        with open(file, "a", encoding="utf8") as f:
            i = 0
            while i < len(cells):
                num = cells[i]
                idxs = cells[i + 1:i + num + 1]
                i += num+1
                txt = ""
                for idx in idxs:
                    txt += f"(P{idx}) -- "
                txt += "cycle;\n"
                f.write(
                    f"\draw [line width=1pt, draw=black, fill={color}, fill opacity={opacity}]\n" + txt)


def save_tikz(input_file: str,
              output_file: str = "ModelData.tex",
              point_size: float = 5,
              line_width: float = 3,
              face_opacity: float = 0.6,
              solid_opacity: float = 0.6,
              point_opacity: float = 0.8,
              line_opacity: float = 1.0,
              color_dict: dict = None,):
    """Save the ``OpenSeesPy`` model data as a ``tikz`` command file in ``latex``,
    and then you can open it in your local tex editor, or run it online in ``overleaf``.

    Parameters
    ----------
    input_file : str
        The input model data file, e.g., "opstool_output/ModelData.hdf5".
    output_file : str, optional
        The output tex file contains the tikz commands, by default "ModelData.tex"
    point_size : float, optional
        The point size in ``pt`` unit, by default 5
    line_width : float, optional
        The line width in ``pt`` unit, by default 3
    face_opacity : float, optional
        The opacity of face elements, by default 0.75
    solid_opacity : float, optional
        The opacity of solid elements, by default 0.75
    point_opacity : float, optional
        The opacity of point, by default 0.75
    line_opacity : float, optional
        The opacity of line elements, by default 1.0
    color_dict : dict, optional
        The color of each type of element, by default None.
        The valid color string must be one of the ``xcolor`` package.
        If None, color_dict = dict(point="Maroon", line="Blue", face="Green",
        solid="Violet", truss="pink", link="SkyBlue", constraint="Lime")
    """
    if color_dict:
        COLORS.update(color_dict)
    # get hdf5 data
    model_info = dict()
    cells = dict()
    with h5py.File(input_file, "r") as f:
        grp1 = f["ModelInfo"]
        for name in grp1.keys():
            model_info[name] = grp1[name][...]
        grp2 = f["Cell"]
        for name in grp2.keys():
            cells[name] = grp2[name][...]
    points = model_info["coord_no_deform"]
    D3 = False if np.max(np.abs(points[:, -1])) < 1e-5 else True
    bound = np.max(points, axis=0) - np.min(points, axis=0)
    aspect_ratio = np.max([bound[1] / bound[0], bound[2] / bound[0]])
    if aspect_ratio > 1:
        paperwidth, paperheight = 100 / aspect_ratio, 100
    else:
        paperwidth, paperheight = 100, 100 * aspect_ratio
    scale = paperwidth / bound[0] / 1.2
    points *= scale
    # write head
    _write_head(output_file, width=paperwidth, height=paperheight, d3=D3)
    # plot
    _def_points(output_file, points, d3=D3)
    cell_types = ["truss", "link", "beam", "other_line"]
    keys = ["truss", "link", "line", "line"]
    widths = [line_width, line_width/2, line_width, line_width]
    for ctype, key, width in zip(cell_types, keys, widths):
        _write_lines(output_file, cells[ctype],
                     line_width=width, opacity=line_opacity,
                     line_color=COLORS[key], line_type=ctype)
    _write_constraint(output_file, model_info, scale, line_width=line_width / 2,
                      d3=D3, line_color=COLORS['constraint'])
    _write_faces(output_file, cells["plane"],
                 color=COLORS['face'], opacity=face_opacity)
    _write_faces(output_file, cells["tetrahedron"],
                 color=COLORS['solid'], opacity=solid_opacity)
    _write_faces(output_file, cells["brick"],
                 color=COLORS['solid'], opacity=solid_opacity)
    _write_points(output_file, points, size=point_size,
                  opacity=point_opacity, color=COLORS['point'])

    # write end
    _write_end(output_file)
