import re
import numpy as np
import pyvista as pv
from shapely import LineString
from sectionproperties.pre.geometry import Geometry

pv.set_plot_theme("document")


def var_line_string(pointsi: list[list[float, float]],
                    pointsj: list[list[float, float]],
                    path: list, n_sec: float = 2,
                    closure: bool = False,
                    y_degree: int = 1, y_sym_plane: str = "j-0",
                    z_degree: int = 2, z_sym_plane: str = "j-0"):
    """Returns the varied line string.

    Parameters
    ----------
    pointsi : list[list[float, float]]
        I end line points.
    pointsj : list[list[float, float]]
        J end line points.
    path : list
        Coordinate path of section normal,
        such as [(x1, y1, z1), (x2, y2, z2), ... , (xn, yn, zn)].
    n_sec : float, optional
        The number of sections within each line segment between two coords in Arg `path`,
        by default 2.
    closure: bool, default=False
        If True, the line is a closed loop.
    y_degree : int, optional
        The polynomial order of the y-axis dimension variation of the section,
        1=linear, 2=parabolic, by default 1.
    y_sym_plane : str, optional, by default "j-0"
        When `y_degree`=2, specify the position of the symmetry plane, where the derivative is 0.
        The format is "i-{d}" or "j-{d}", which means that the distance from end i or end j is d.
        For example, "j-0" refers to end j, and "j-1.5" refers to the position 1.5 away from end j.
    z_degree : int, optional
        The polynomial order of the z-axis dimension variation of the section,
        1=linear, 2=parabolic, by default 2.
    z_sym_plane : str, optional, by default "j-0"
        When `z_degree`=2, specify the position of the symmetry plane, where the derivative is 0.
        The format is "i-{d}" or "j-{d}", which means that the distance from end i or end j is d.
        For example, "j-0" refers to end j, and "j-1.5" refers to the position 1.5 away from end j.

    Returns
    --------
    list[list[list[float, float]]]
        A list of lines, the number of which is determined by `path` and `n_sec`.
    """
    length, cum_length, _ = _get_path_len(path, n_sec)
    if closure:
        if pointsi[-1] != pointsi[0]:
            pointsi = list(pointsi)
            pointsi.append(pointsi[0])
        if pointsj[-1] != pointsj[0]:
            pointsj = list(pointsj)
            pointsj.append(pointsj[0])
    linesi = LineString(pointsi)
    linesj = LineString(pointsj)
    yi, zi = linesi.xy
    yj, zj = linesj.xy
    cum_points = []
    for x in cum_length:
        points_ = []
        for i in range(len(yi)):
            y = _get_coord(0, yi[i], length, yj[i], x,
                           degree=y_degree, sym_plane=y_sym_plane)
            z = _get_coord(0, zi[i], length, zj[i], x,
                           degree=z_degree, sym_plane=z_sym_plane)
            points_.append((y, z))
        cum_points.append(points_)
    return cum_points


def vis_var_sec(sec_meshes: list, path: list, n_sec: float, on_notebook: bool = False):
    """Visualize varied section meshes.

    Parameters
    ----------
    sec_meshes : list
        _description_
    path : list
        Coordinate path of section normal,
        such as [(x1, y1, z1), (x2, y2, z2), ... , (xn, yn, zn)].
    n_sec : float
        The number of sections within each line segment between two coords in Arg `path`.
    on_notebook : bool, optional, by default False
        If True, display on the notebook.
    """
    _, _, cum_coord = _get_path_len(path, n_sec)
    plotter = pv.Plotter(notebook=on_notebook)
    cum_coord = np.array(cum_coord, dtype=np.float32)
    point_plot1 = pv.PolyData(cum_coord)
    plotter.add_mesh(point_plot1, color='black',
                     point_size=5, render_points_as_spheres=True)
    path = np.array(path, dtype=np.float32)
    point_plot2 = pv.PolyData(path)
    plotter.add_mesh(point_plot2, color='#8f1402',
                     point_size=10, render_points_as_spheres=True)
    line_cells = []
    for i in range(len(path) - 1):
        line_cells.extend([2, i, i + 1])

    line_plot = _generate_mesh(path, line_cells, kind="line")
    plotter.add_mesh(
        line_plot,
        color='black',
        render_lines_as_tubes=False,
        line_width=2,
    )
    local_axes = _get_path_local_axes(path, n_sec)
    for i in range(len(sec_meshes)):
        sec_mesh = sec_meshes[i]
        center0 = cum_coord[i]
        _, vecy, vecz = local_axes[i]
        points = sec_mesh.points
        points = (points[:, 0].reshape((-1, 1)) @ np.reshape(vecy, (1, 3)) +
                  points[:, 1].reshape((-1, 1)) @ np.reshape(vecz, (1, 3)))
        points += center0
        for name, faces in sec_mesh.cells_map.items():
            faces = np.insert(faces, 0, values=3, axis=1)
            face_plot = _generate_mesh(
                points, faces, kind="face"
            )
            plotter.add_mesh(
                face_plot, color=sec_mesh.color_map[name], show_edges=True, opacity=1
            )
        for rdata in sec_mesh.rebar_data:
            color = rdata["color"]
            r = rdata["dia"] / 2
            rebar_xy = np.array(rdata["rebar_xy"])
            rebar_xy = (rebar_xy[:, 0].reshape((-1, 1)) @ np.reshape(vecy, (1, 3)) +
                        rebar_xy[:, 1].reshape((-1, 1)) @ np.reshape(vecz, (1, 3)))
            rebar_xy += center0
            spheres = []
            for coord in rebar_xy:
                spheres.append(pv.Sphere(radius=r, center=coord))
            merged = pv.MultiBlock(spheres)
            plotter.add_mesh(merged, color=color)
    plotter.add_axes()
    plotter.view_isometric()
    plotter.show(title="opstool")


def _get_path_len(path, n_sec):
    n = len(path)
    length = 0
    cum_length = []
    cum_coord = []
    for i in range(n - 1):
        p1 = np.array(path[i])
        p2 = np.array(path[i + 1])
        seg = np.sqrt(np.sum((p2 - p1) ** 2))
        for j in range(n_sec):
            cum_length.append(length + seg / (n_sec - 1) * j)
            cum_coord.append(p1 + (p2 - p1) / (n_sec - 1) * j)
        length += seg
    cum_length = np.array(cum_length, dtype=np.float32)
    cum_coord = np.array(cum_coord, dtype=np.float32)
    return length, cum_length, cum_coord


def _get_path_local_axes(path, n_sec):
    n = len(path)
    local_axes = []
    for i in range(n - 1):
        p1 = np.array(path[i])
        p2 = np.array(path[i + 1])
        local_x = (p2 - p1) / np.linalg.norm(p2 - p1)
        global_z = np.array([0, 0, 1])
        cos2 = local_x @ global_z / \
            (np.linalg.norm(local_x) * np.linalg.norm(global_z))
        if np.abs(1 - cos2) < 1e-12:
            vecxz = [-1, 0, 0]
        else:
            vecxz = [0, 0, 1]
        local_y = np.cross(vecxz, local_x)
        local_z = np.cross(local_x, local_y)
        local_y /= np.linalg.norm(local_y)
        local_z /= np.linalg.norm(local_z)
        for j in range(n_sec):
            local_axes.append([local_x, local_y, local_z])
    return local_axes


def _get_coord(x1, y1, x2, y2, x, degree=1, sym_plane="j-0"):
    if degree == 1:
        y = y1 + (y2 - y1) * (x - x1) / (x2 - x1)
    elif degree == 2:
        d = float(re.findall(r"\d+\.?\d*", sym_plane)[0])
        if sym_plane[0].lower() == 'j':
            a = (y2 - y1) / (x2 ** 2 - x1 ** 2 - 2 * (x2 + d) * (x2 - x1))
            b = -2 * a * (x2 + d)
            c = y1 - a * x1 ** 2 - b * x1
            y = a * x ** 2 + b * x + c
        elif sym_plane[0].lower() == 'i':
            a = (y2 - y1) / (x2 ** 2 - x1 ** 2 - 2 * (x1 - d) * (x2 - x1))
            b = -2 * a * (x1 - d)
            c = y1 - a * x1 ** 2 - b * x1
            y = a * x ** 2 + b * x + c
        else:
            raise ValueError(f"Error arg sym_plane={sym_plane}!")
    else:
        raise ValueError("Currently only support degree=1 or 2!")
    return y


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

# class VarSecMesh:
#     """A class for generating meshes with variable fiber cross-sections.

#     Parameters
#     ----------
#     meshi : Instance of the class ``SecMesh``.
#         I end section.
#     meshj : Instance of the class ``SecMesh``.
#         J end section.
#     path : list
#         Coordinate path of section normal,
#         such as [(x1, y1), (x2, y2), ... , (xn, yn)]
#     n_sec : float, optional
#         The number of sections within each line segment between two coords in Arg `path`,
#         by default 2.
#     y_degree : int, optional
#         The polynomial order of the y-axis dimension variation of the section,
#         1=linear, 2=parabolic, by default 1.
#     y_sym_plane : str, optional, by default "j-0"
#         When `y_degree`=2, specify the position of the symmetry plane, where the derivative is 0.
#         The format is "i-{d}" or "j-{d}", which means that the distance from end i or end j is d.
#         For example, "j-0" refers to end j, and "j-1.5" refers to the position 1.5 away from end j.
#     z_degree : int, optional
#         The polynomial order of the z-axis dimension variation of the section,
#         1=linear, 2=parabolic, by default 2.
#     z_sym_plane : str, optional, by default "j-0"
#         When `z_degree`=2, specify the position of the symmetry plane, where the derivative is 0.
#         The format is "i-{d}" or "j-{d}", which means that the distance from end i or end j is d.
#         For example, "j-0" refers to end j, and "j-1.5" refers to the position 1.5 away from end j.
#     """

#     def __init__(self, meshi: SecMesh, meshj: SecMesh,
#                  path: list, n_sec: float = 2,
#                  y_degree: int = 1, y_sym_plane: str = "j-0",
#                  z_degree: int = 2, z_sym_plane: str = "j-0"):
#         if meshi.center is None or meshj.center is None:
#             raise ValueError("meshi and meshj must run centring() method!")
#         for i in range(len(path)):
#             p = np.atleast_1d(path[i])
#             if len(p) == 1:
#                 path[i] = np.append(p, [0, 0])
#             elif len(p) == 2:
#                 path[i] = np.append(p, [0])
#             else:
#                 path[i] = p
#         path = np.array(path, dtype=np.float32)
#         self.meshi = meshi
#         self.meshj = meshj
#         self.path = path
#         self.n_sec = n_sec
#         self.y_degree = y_degree
#         self.y_sym_plane = y_sym_plane
#         self.z_degree = z_degree
#         self.z_sym_plane = z_sym_plane

#         self.new_sec_mesh = []
#         self.new_sec_props = []
#         self.path_length = None
#         self.path_cum_length = None
#         self.path_cum_coord = None

#     def get_sec_mesh(self):
#         """Get the fiber section mesh on the `path`.

#         Returns
#         -------
#         list,
#             A list of instances of class ``SecMesh`,
#             the number of which is determined by `path` and `n_sec`.
#         """
#         length, cum_length, cum_coord = _get_path_len(self.path, self.n_sec)
#         self.path_length, self.path_cum_length, self.path_cum_coord = length, cum_length, cum_coord
#         for x in self.path_cum_length:
#             group_map, mesh_size_map, mat_ops_map = _get_map(self.meshi, self.meshj, length, x,
#                                                              self.y_degree, self.y_sym_plane,
#                                                              self.z_degree, self.z_sym_plane)
#             rebar_data = _get_rebar_data(self.meshi, self.meshj, length, x,
#                                          self.y_degree, self.y_sym_plane, self.z_degree, self.z_sym_plane)

#             secx = SecMesh()
#             secx.assign_group(group_map)
#             secx.assign_mesh_size(mesh_size_map)
#             secx.assign_ops_matTag(mat_ops_map)
#             if not self.meshi.color_map:
#                 for i, name in enumerate(self.meshi.group_map.keys()):
#                     secx.color_map[name] = secx.colors_default[i]
#             else:
#                 secx.color_map = self.meshi.color_map
#             secx.rebar_data = rebar_data
#             secx.mesh()
#             secx.centring()
#             self.new_sec_mesh.append(secx)
#         return self.new_sec_mesh

#     def get_sec_props(self, Eref: float = 1.0):
#         """Solving Section Geometry Properties on the `path`.

#         Parameters
#         ----------
#         Eref: float, default=1.0
#             Reference modulus of elasticity, it is important to analyze the composite section.
#             See `sectionproperties doc <https://sectionproperties.readthedocs.io/en/latest/rst/post.html>`_

#         Returns
#         -------
#         list[dict]
#             Each element is a dict of properties for each section.
#         """
#         for sec_mesh in self.new_sec_mesh:
#             sec_props = sec_mesh.get_sec_props(Eref)
#             self.new_sec_props.append(sec_props)
#         return self.new_sec_props

#     def view(self, on_notebook: bool = False):
#         """Visualize fiber cross-sections on path.

#         Parameters
#         ----------
#         on_notebook : bool, optional, by default False
#             If True, display in the jupyter notebook.
#         """

#         plotter = pv.Plotter(notebook=on_notebook)
#         point_plot1 = pv.PolyData(self.path_cum_coord)
#         plotter.add_mesh(point_plot1, color='black',
#                          point_size=5, render_points_as_spheres=True)
#         point_plot2 = pv.PolyData(self.path)
#         plotter.add_mesh(point_plot2, color='#8f1402',
#                          point_size=10, render_points_as_spheres=True)
#         line_cells = []
#         for i in range(len(self.path) - 1):
#             line_cells.extend([2, i, i + 1])

#         line_plot = _generate_mesh(self.path, line_cells, kind="line")
#         plotter.add_mesh(
#             line_plot,
#             color='black',
#             render_lines_as_tubes=False,
#             line_width=2,
#         )
#         local_axes = _get_path_local_axes(self.path, self.n_sec)
#         for i in range(len(self.new_sec_mesh)):
#             sec_mesh = self.new_sec_mesh[i]
#             center0 = self.path_cum_coord[i]
#             _, vecy, vecz = local_axes[i]
#             points = sec_mesh.points
#             points = (points[:, 0].reshape((-1, 1)) @ np.reshape(vecy, (1, 3)) +
#                       points[:, 1].reshape((-1, 1)) @ np.reshape(vecz, (1, 3)))
#             points += center0
#             for name, faces in sec_mesh.cells_map.items():
#                 faces = np.insert(faces, 0, values=3, axis=1)
#                 face_plot = _generate_mesh(
#                     points, faces, kind="face"
#                 )
#                 plotter.add_mesh(
#                     face_plot, color=sec_mesh.color_map[name], show_edges=True, opacity=1
#                 )
#             for rdata in sec_mesh.rebar_data:
#                 color = rdata["color"]
#                 r = rdata["dia"] / 2
#                 rebar_xy = np.array(rdata["rebar_xy"])
#                 rebar_xy = (rebar_xy[:, 0].reshape((-1, 1)) @ np.reshape(vecy, (1, 3)) +
#                             rebar_xy[:, 1].reshape((-1, 1)) @ np.reshape(vecz, (1, 3)))
#                 rebar_xy += center0
#                 spheres = []
#                 for coord in rebar_xy:
#                     spheres.append(pv.Sphere(radius=r, center=coord))
#                 merged = pv.MultiBlock(spheres)
#                 plotter.add_mesh(merged, color=color)
#         plotter.add_axes()
#         plotter.view_isometric()
#         plotter.show(title="opstool")

# def _get_map(meshi, meshj, length, x, y_degree, y_sym_plane, z_degree, z_sym_plane):
#     group_map = dict()
#     mesh_size_map = dict()
#     mat_ops_map = dict()
#     for name in meshi.group_map.keys():
#         mesh_size_map[name] = (meshi.mesh_size_map[name] +
#                                meshj.mesh_size_map[name]) / 2
#         if meshi.mat_ops_map and meshj.mat_ops_map:
#             mat_ops_map[name] = meshi.mat_ops_map[name]
#         geom_i = meshi.group_map[name].geom
#         geom_j = meshj.group_map[name].geom
#         ext_i = np.array(geom_i.exterior.coords)
#         ext_j = np.array(geom_j.exterior.coords)
#         ext_i -= np.array(meshi.center)
#         ext_j -= np.array(meshj.center)
#         ext_i = _sort_xy(ext_i)
#         ext_j = _sort_xy(ext_j)
#         yi, zi = ext_i[:, 0], ext_i[:, 1]
#         yj, zj = ext_j[:, 0], ext_j[:, 1]
#         ys, zs = [], []
#         for i in range(len(yi)):
#             y = _get_coord(0, yi[i], length, yj[i], x,
#                            degree=y_degree, sym_plane=y_sym_plane)
#             z = _get_coord(0, zi[i], length, zj[i], x,
#                            degree=z_degree, sym_plane=z_sym_plane)
#             ys.append(y)
#             zs.append(z)
#         ext_points = [[ys[i_], zs[i_]] for i_ in range(len(ys))]
#         int_points = []
#         for inti, intj in zip(geom_i.interiors, geom_j.interiors):
#             int_i = np.array(inti.coords)
#             int_j = np.array(intj.coords)
#             int_i -= np.array(meshi.center)
#             int_j -= np.array(meshj.center)
#             yi, zi = int_i[:, 0], int_i[:, 1]
#             yj, zj = int_j[:, 0], int_j[:, 1]
#             ys, zs = [], []
#             for i in range(len(yi)):
#                 y = _get_coord(0, yi[i], length, yj[i], x,
#                                degree=y_degree, sym_plane=y_sym_plane)
#                 z = _get_coord(0, zi[i], length, zj[i], x,
#                                degree=z_degree, sym_plane=z_sym_plane)
#                 ys.append(y)
#                 zs.append(z)
#             int_points.append([[ys[i_], zs[i_]] for i_ in range(len(ys))])
#         ply = Polygon(ext_points, int_points)
#         geometry = Geometry(geom=ply, material=meshi.group_map[name].material)
#         group_map[name] = geometry
#     return group_map, mesh_size_map, mat_ops_map


# def _get_rebar_data(meshi, meshj, length, x, y_degree, y_sym_plane, z_degree, z_sym_plane):
#     rebar_data = []
#     for datai, dataj in zip(meshi.rebar_data, meshj.rebar_data):
#         data = dict()
#         data["dia"] = datai["dia"]
#         data["matTag"] = datai["matTag"]
#         data['color'] = datai['color']
#         rebar_xyi, rebar_xyj = np.array(
#             datai["rebar_xy"]), np.array(dataj["rebar_xy"])
#         rebar_xyi, rebar_xyj = _sort_xy(rebar_xyi), _sort_xy(rebar_xyj)
#         xy = []
#         for xyi, xyj in zip(rebar_xyi, rebar_xyj):
#             y = _get_coord(0, xyi[0], length, xyj[0], x,
#                            degree=y_degree, sym_plane=y_sym_plane)
#             z = _get_coord(0, xyi[1], length, xyj[1], x,
#                            degree=z_degree, sym_plane=z_sym_plane)
#             xy.append([y, z])
#         data["rebar_xy"] = xy
#         rebar_data.append(data)
#     return rebar_data

# def _sort_xy(points):
#     x, y = points[:, 0], points[:, 1]
#     x0, y0 = np.mean(x), np.mean(y)
#     r = np.sqrt((x - x0) ** 2 + (y - y0) ** 2)
#     angles = np.where((y - y0) > 0, np.arccos((x - x0) / r),
#                       2 * np.pi - np.arccos((x - x0) / r))
#     mask = np.argsort(angles)
#     points_ = points[mask]
#     return points_