"""
SecMesh: A module to mesh the cross-section with triangular fibers
"""

import matplotlib.pyplot as plt
import numpy as np
import openseespy.opensees as ops
from typing import Union
from matplotlib.collections import PatchCollection
from sectionproperties.analysis.section import Section
from sectionproperties.pre.geometry import CompoundGeometry, Geometry
from sectionproperties.pre.pre import Material, DEFAULT_MATERIAL
from shapely.geometry import LineString, Polygon
from rich.table import Table
from ...utils import CONSOLE, PKG_PREFIX, get_random_color, get_random_color_rich


def create_circle_points(
    xo: list,
    radius: float,
    angles: Union[list, tuple] = (0.0, 360),
    n_sub: int = 40,
):
    """Add the circle geom obj.

    Parameters
    ----------
    xo : list[float, float]
        Center coords, [(xc, yc)].
    radius: float
        radius.
    angles : Union[list, tuple], default=(0.0, 360)
        The start angle and the end angle, deree
    n_sub: int, default=40
        The partition number of the perimeter.

    Returns
    -------
    points: list[list[float, float]]
        coord points on arc line.
    """
    angle1, angle2 = angles
    angle1 = angle1 / 180 * np.pi
    angle2 = angle2 / 180 * np.pi
    x, y = xo[0], xo[1]
    angles = np.linspace(angle1, angle2, n_sub + 1)
    points = [[x + radius * np.cos(ang), y + radius * np.sin(ang)] for ang in angles]
    return points


def offset(points: list, d: float):
    """Offsets closed polygons.

    Parameters
    ----------
    points : list[list[float, float]]
        A list containing the coordinate points, [(x1, y1),(x2, y2),...,(xn.yn)].
    d : float
        Offsets closed polygons, positive values offset inwards, negative values outwards.

    Returns
    -------
    coords: list[[float, float]], new offset points.

    Examples
    ----------
    >>> import opstool as opst
    >>> outlines1 = [[0, 0], [0, 1], [1, 1]]
    >>> outlines2 = opst.pre.section.offset(outlines1, d=0.1)
    >>> outlines3 = [[0, 0], [0, 1], [1, 1], [1, 0]]
    >>> outlines4 = opst.pre.section.offset(outlines3, d=0.1)
    """
    ply = Polygon(points)
    ply_off = ply.buffer(-d, cap_style="flat", join_style="mitre")
    return list(ply_off.exterior.coords)


def poly_offset(points: list, d: float):
    """Offsets closed polygons, same as :py:func:`opstool.pre.section.offset`

    Parameters
    ----------
    points  : list[list[float, float]]
        A list containing the coordinate points, [(x1, y1),(x2, y2),...,(xn.yn)].
    d : float
        Offsets closed polygons, positive values offset inwards, negative values outwards.

    Returns
    -------
    coords: list[[float, float]]
    """
    return offset(points=points, d=d)


def line_offset(points: list, d: float):
    """Offset a distance from a non-closed line ring on its right or its left side.

    Parameters
    ----------
    points  : list[list[float, float]]
        A list containing the coordinate points, [(x1, y1),(x2, y2),...,(xn.yn)].
    d : float
        Offsets non-closed line ring, negative for left side offset, positive for right side offset.

    Returns
    -------
    coords: list[[float, float]]

    Examples
    ----------
    >>> import opstool as opst
    >>> lines = [[0, 0], [0, 1]]
    >>> lines2 = opst.pre.section.line_offset(lines, d=0.1)
    >>> lines = [[0, 0], [0, 1], [1, 1]]
    >>> lines3 = opst.pre.section.line_offset(lines, d=0.1)
    >>> lines = [[0, 0], [0, 1], [1, 0]]
    >>> lines4 = opst.pre.section.line_offset(lines, d=0.1)
    """
    ls = LineString(points)
    ls_off = ls.offset_curve(-d, quad_segs=16, join_style="mitre", mitre_limit=5.0)
    return list(ls_off.coords)


def create_material(
    name: str = "default",
    elastic_modulus: float = 1.0,
    poissons_ratio: float = 0.0,
    yield_strength: float = 1.0,
    density: float = 1.0,
    color: str = "w",
):
    """Create a meterial object of
    `sectionproperties material <https://sectionproperties.readthedocs.io/en/stable/user_guide/materials.html>`_.

    Parameters
    ----------
    name : str, default='default'
        meterial name.
    elastic_modulus : float, default==1
        elastic_modulus.
    poissons_ratio : float, default=0
        poissons_ratio
    yield_strength : float, default==1
        yield_strength
    density : float, default=1
        mass density
    color: str, default='w'
        plot color by ``sectionproperties``.

    Returns
    -------
    `sectionproperties material <https://sectionproperties.readthedocs.io/en/stable/user_guide/materials.html>`_
    """
    return Material(
        name=name,
        elastic_modulus=elastic_modulus,
        poissons_ratio=poissons_ratio,
        yield_strength=yield_strength,
        density=density,
        color=color,
    )


def create_polygon_patch(
    outline: list,
    holes: list = None,
    material=None,
):
    """Add a polygon plane geom object.

    Parameters
    ----------
    outline : list[list[float, float]]
        The coords list of polygon points, [(x1, y1), (x2, y2),...,(xn, yn)]
    holes: list[list[list[float, float]]].
        Hole of the section, a list of multiple hole coords, [hole1, hole2,...holeN],
        holeN=[(x1, y1), (x2, y2),...,(xn, yn)].
    material: material obj
        The instance from :py:func:`opstool.pre.section.create_material`

    Returns
    -------
    polygon geom obj
    """
    if material is None:
        material_ = DEFAULT_MATERIAL
    else:
        material_ = material
    # close or not
    vec = np.array(outline[0]) - np.array(outline[-1])
    if np.linalg.norm(vec) < 1e-8:
        outline = outline[:-1]
    if holes is not None:
        for i, hole in enumerate(holes):
            vec = np.array(hole[0]) - np.array(hole[-1])
            if np.linalg.norm(vec) < 1e-8:
                holes[i] = hole[:-1]
    ply = Polygon(outline, holes)
    geometry = Geometry(geom=ply, material=material_)
    return geometry


def create_circle_patch(
    xo: list,
    radius: float,
    holes: Union[None, list, tuple] = None,
    angle1: float = 0.0,
    angle2: float = 360,
    n_sub: int = 40,
    material=None,
):
    """Add the circle geom obj.

    Parameters
    ----------
    xo : list[float, float]
        Center coords, [(xc, yc)].
    radius: float
        radius.
    holes: list[list[list[float, float]]].
        Hole of the section, a list of multiple hole coords, [hole1, hole2,...holeN],
        holeN=[(x1, y1), (x2, y2),...,(xn, yn)].
    angle1 : float
        The start angle, degree
    angle2 : float
        The end angle, deree
    n_sub: int
        The partition number of the perimeter.
    material: material obj
        The instance from :py:func:`opstool.pre.section.create_material`.

    Returns
    -------
    Cirle geom obj.
    """
    if material is None:
        material_ = DEFAULT_MATERIAL
    else:
        material_ = material
    angle1 = angle1 / 180 * np.pi
    angle2 = angle2 / 180 * np.pi
    x, y = xo[0], xo[1]
    angles = np.linspace(angle1, angle2, n_sub + 1)
    points = [[x + radius * np.cos(ang), y + radius * np.sin(ang)] for ang in angles]
    ply = Polygon(points, holes)
    geometry = Geometry(geom=ply, material=material_)
    return geometry


def create_patch_from_dxf(
    filepath: str, spline_delta: float = 0.1, degrees_per_segment: float = 1
):
    """An interface for the creation of Geometry objects from CAD .dxf files.
    See
    `sectionproperties docs <https://sectionproperties.readthedocs.io/en/stable/examples/geometry/geometry_cad.html>`_.

    .. note:

        Note that loading multiple regions from a .dxf file is not currently supported.
        A possible workaround could involve saving each region as a separate .dxf file,
        importing each region individually using create_patch_from_dxf(),
        then combining the regions using the + operator.

    Parameters
    ----------
    filepath: str|path
        A path-like object for the dxf file.
    spline_delta: float, default = 0.1
        Splines are not supported in shapely, so they are approximated as polylines,
        this argument affects the spline sampling rate.
    degrees_per_segment: float, default = 1
        The number of degrees discretized as a single line segment.

    Returns
    -------
    geom obj.
    """
    return Geometry.from_dxf(
        dxf_filepath=filepath,
        spline_delta=spline_delta,
        degrees_per_segment=degrees_per_segment,
    )


def set_patch_material(geom, material=DEFAULT_MATERIAL):
    """Assign material to a geom patch.

    Parameters
    ----------
    geom: geom obj | list[geom obj]
        The geometry object.
    material: material obj | list[material obj]
        The material object of :py:func:`opstool.pre.section.create_material`.
    """
    if isinstance(geom, (list, tuple, set)):
        for geo, mat in zip(geom, material):
            geo.material = mat
    else:
        geom.material = material


class FiberSecMesh:
    """A class to mesh the cross-section with triangular fibers.

    Parameters
    --------------
    sec_name : str
        Assign a name to the section.
    """

    def __init__(self, sec_name: str = "My Section"):
        self.sec_name = sec_name

        # * mesh obj
        self.mesh_obj = None
        self.section = None
        self.fibrt_points = None
        self.fiber_cells_map = dict()
        self.fiber_centers_map = dict()
        self.fiber_areas_map = dict()
        self.centroid = None
        self.geom_area = 0.0
        self.area = 0.0
        self.Iy = 0.0
        self.Iz = 0.0
        self.J = 0.0

        # * data group
        self.geom_group_map = dict()
        self.mat_ops_map = dict()
        self.mesh_size_map = dict()
        self.color_map = dict()
        self.geom_names = []

        # *rebar data
        self.rebar_data = []

        # * section geo props
        self.sec_props = dict()
        self.frame_sec_props = dict()

        self.is_centring = False

    def add_patch_group(self, patches):
        """Add the patches.

        Parameters
        ------------
        patches : dict|patch|List[patch]
            A dict of name as a key, geometry obj as value.

        Returns
        ----------
        SecMesh instance
        """
        if isinstance(patches, dict):
            self.geom_group_map.update(patches)
        elif isinstance(patches, (list, tuple, set)):
            for patch in patches:
                name = f"patch{len(self.geom_group_map)+1}"
                self.geom_group_map[name] = patch
        else:
            name = f"patch{len(self.geom_group_map)+1}"
            self.geom_group_map[name] = patches
        return self

    def get_patch_group(self):
        """Return the group dict for each geometry obj.

        Returns
        ----------
        group : dict[str, any]
        """
        return self.geom_group_map

    def set_mesh_size(
        self, mesh_size: Union[dict[str, float], list[float], tuple[float], float]
    ):
        """Assign the mesh size dict for each mesh.

        Parameters
        ------------
        mesh_size : dict[str, float] | list[float] | float
            The mesh sizes describe the maximum mesh element size to be
            used in the finite-element mesh for each Geometry object.

            - If dict, name as the key, mesh size as value.
            - If floated, all geoms will use the same meshsize.
            - If list or tuple, the length must be the same as the geoms.

        Returns
        ------------
        instance
        """
        if not self.geom_group_map:
            raise ValueError("The add_patch_group method should be run first!")
        if isinstance(mesh_size, dict):
            for name in mesh_size.keys():
                if name not in self.geom_group_map.keys():
                    raise ValueError(
                        f"{name} is not specified in the add_patch_group function!"
                    )
            self.mesh_size_map.update(mesh_size)
        elif isinstance(mesh_size, (list, tuple, set)):
            for i, name in enumerate(self.geom_group_map.keys()):
                self.mesh_size_map[name] = mesh_size[i]
        else:
            for i, name in enumerate(self.geom_group_map.keys()):
                self.mesh_size_map[name] = mesh_size
        return self

    def set_ops_mat_tag(
        self, mat_tag: Union[dict[str, int], list[int], tuple[int], int]
    ):
        """Assign the opensees mat tag for each mesh.

        Parameters
        --------------
        mat_tag : dict[str, int] | list[int] | int
            - If dict, name as a key, `OpenSees` matTag previously defined as value.
            - If list or tuple, the length must be the same as the geom patches.
            - If int, all patches will use the same matTag.

        Returns
        ----------
        instance
        """
        if not self.geom_group_map:
            raise ValueError("The add_patch_group method should be run first!")
        if isinstance(mat_tag, dict):
            for name in mat_tag.keys():
                if name not in self.geom_group_map.keys():
                    raise ValueError(
                        f"{name} is not specified in the add_patch_group function!"
                    )
            self.mat_ops_map.update(mat_tag)
        elif isinstance(mat_tag, (list, tuple, set)):
            for i, name in enumerate(self.geom_group_map.keys()):
                self.mat_ops_map[name] = mat_tag[i]
        else:
            for i, name in enumerate(self.geom_group_map.keys()):
                self.mat_ops_map[name] = mat_tag
        return self

    def set_mesh_color(self, colors):
        """Assign the color to plot the section.

        Parameters
        -------------
        colors : dict[str, str] | list[str|list|tuple] | str
            If dict, the patch name as a key, color as value.
        """
        if not self.geom_group_map:
            raise ValueError("The add_patch_group method should be run first!")
        if isinstance(colors, dict):
            for name in colors.keys():
                if name not in self.geom_group_map.keys():
                    raise ValueError(
                        f"{name} is not specified in the add_patch_group function!"
                    )
            self.color_map.update(colors)
        elif isinstance(colors, (list, tuple, set)):
            for i, name in enumerate(self.geom_group_map.keys()):
                self.color_map[name] = colors[i]
        else:
            for i, name in enumerate(self.geom_group_map.keys()):
                self.color_map[name] = colors
        return self

    def mesh(self):
        """Mesh the section.

        If set_mesh_size has not been invoked,
        the mesh size of each Geometry will be calculated by its area / 100.

        Returns
        ----------
        None
        """
        if not self.color_map:
            for name in self.geom_group_map.keys():
                self.color_map[name] = get_random_color()
        if not self.mesh_size_map:
            for name, geom in self.geom_group_map.items():
                area = geom.calculate_area()
                self.mesh_size_map[name] = np.sqrt(2 * area / 100)
        geoms, mesh_sizes = [], []
        for name, geom in self.geom_group_map.items():
            if geom.material != DEFAULT_MATERIAL:
                geom.material = create_material(
                    name=name,
                    elastic_modulus=geom.material.elastic_modulus,
                    poissons_ratio=geom.material.poissons_ratio,
                    yield_strength=geom.material.yield_strength,
                    density=geom.material.density,
                    color=self.color_map[name],
                )
            geoms.append(geom)
            mesh_sizes.append(0.5 * self.mesh_size_map[name] ** 2)
            self.geom_names.append(name)
        geom_obj = CompoundGeometry(geoms)
        mesh_obj = geom_obj.create_mesh(mesh_sizes=mesh_sizes)
        self.section = Section(geom_obj, time_info=False)
        self.mesh_obj = mesh_obj.mesh
        self._get_mesh_data()
        txt = get_random_color_rich(self.sec_name)
        CONSOLE.print(f"{PKG_PREFIX}The section {txt} has been successfully meshed!")

    def _get_mesh_data(self):
        # * mesh data
        vertices = self.mesh_obj["vertices"]
        self.points = np.array(vertices)
        triangles = self.mesh_obj["triangles"][:, :3]
        triangle_attributes = self.mesh_obj["triangle_attributes"]
        attributes = np.unique(triangle_attributes)
        for name, attri in zip(self.geom_group_map.keys(), attributes):
            idx = triangle_attributes == attri
            self.fiber_cells_map[name] = triangles[idx[:, 0]]
        # * fiber data
        iys, izs = [], []
        for name, faces in self.fiber_cells_map.items():
            areas = []
            centers = []
            for face in faces:
                idx1, idx2, idx3 = face
                coord1, coord2, coord3 = vertices[idx1], vertices[idx2], vertices[idx3]
                xyo = (coord1 + coord2 + coord3) / 3
                centers.append(xyo)
                x1, y1 = coord1[:2]
                x2, y2 = coord2[:2]
                x3, y3 = coord3[:2]
                area_ = 0.5 * np.abs(
                    x2 * y3 + x1 * y2 + x3 * y1 - x3 * y2 - x2 * y1 - x1 * y3
                )
                areas.append(area_)
                iys.append(area_ * xyo[1] ** 2)
                izs.append(area_ * xyo[0] ** 2)
            self.fiber_areas_map[name] = np.array(areas)
            self.fiber_centers_map[name] = np.array(centers)
        centers = []
        areas = []
        for name in self.fiber_cells_map.keys():
            centers.append(self.fiber_centers_map[name])
            areas.append(self.fiber_areas_map[name])
        centers = np.vstack(centers)
        areas = np.hstack(areas)
        self.geom_area = np.sum(areas)
        self.centroid = areas @ centers / self.geom_area
        self.Iy = np.sum(iys)
        self.Iz = np.sum(izs)

    def get_fiber_data(self):
        """Return fiber data.

        Returns
        -------
        Tuple(dict, dict)
            fiber center dict, fiber area dict
        """
        return self.fiber_centers_map, self.fiber_areas_map

    def add_rebar_points(
        self,
        points: list,
        dia: float,
        ops_mat_tag: int = None,
        color: str = "black",
        group_name: str = "Rebar",
    ):
        """Add rebars by coord points.

        Parameters
        ----------
        points: list[list[float, float]]
            A list of rebar coords, [(x1, y1), (x2, y2),...,(xn, yn)],
            in which each element represents a rebar point.
        dia: float
            Rebar diameter.
        ops_mat_tag: int
            OpenSees mat Tag for rebar previously defined.
        color: str or rgb tuple.
            Color to plot rebar.
        group_name: str, default='Rebar'
            Assign rebar group name

        Returns
        -------
        None
        """
        rebar_xy = np.array(points)
        data = dict(
            rebar_xy=rebar_xy, color=color, name=group_name, dia=dia, matTag=ops_mat_tag
        )
        self.rebar_data.append(data)

    def add_rebar_line(
        self,
        points: list,
        dia: float,
        gap: float = 0.1,
        n: int = None,
        closure: bool = False,
        ops_mat_tag: int = None,
        color: str = "black",
        group_name: str = "Rebar",
    ):
        """Add rebar along a line, can be a line or polygon.

        Parameters
        ----------
        points: list[list[float, float]]
            A list of rebar coords, [(x1, y1), (x2, y2),...,(xn, yn)],
            in which each element represents a corner point,
            and every two corner points are divided by the arg `gap`.
        dia: float
            Rebar diameter.
        gap: float, default=0.1
            Rebar space.
        n: int, default=None
            The number of rebars, if not None,
            update the Arg `gap` according to `n`.
            This means that if you know the number of rebars,
            you don't need to input `gap` or set `gap` to any number.
        closure: bool, default=False
            If True, the rebar line is a closed loop.
        ops_mat_tag: int
            OpenSees mat Tag for rebar previously defined.
        color: str or rgb tuple.
            Color to plot rebar.
        group_name: str, default='Rebar'
            Assign rebar group name

        Returns
        -------
        None
        """
        if closure:
            if points[-1] != points[0]:
                points = list(points)
                points.append(points[0])
        rebar_lines = LineString(points)
        x, y = rebar_lines.xy
        if n:
            gap = rebar_lines.length / (n - 1)
        # mesh rebar points based on spacing
        rebar_xy = _lines_subdivide(x, y, gap)
        data = dict(
            rebar_xy=rebar_xy, color=color, name=group_name, dia=dia, matTag=ops_mat_tag
        )
        self.rebar_data.append(data)

    def add_rebar_circle(
        self,
        xo: list,
        radius: float,
        dia: float,
        gap: float = 0.1,
        n: int = None,
        angles: Union[list, tuple] = (0.0, 360),
        ops_mat_tag: int = None,
        color: str = "black",
        group_name: str = "Rebar",
    ):
        """Add the rebars along a circle.

        Parameters
        ----------
        xo: list[float, float]
            Center coords of circle, [(xc, yc)].
        radius: float
            Radius of circle.
        dia: float
            rebar dia.
        gap: float, default=0.1
            Rebar space.
        n: int, default=None
            The number of rebars, if not None,
            update the Arg `gap` according to `n`.
            This means that if you know the number of rebars,
            you don't need to input `gap` or set `gap` to any number.
        angles: Union[list, tuple], default=[0.0, 360]
            The start angle and end angle, degree.
        ops_mat_tag: int, defaultt=None
            OpenSees material matTag for rebar previously defined.
        color: str or rgb tuple.
            Color to plot rebar.
        group_name: str, default='Rebar'
            Assign rebar group name.

        Returns
        -------
        None
        """
        angle1, angle2 = angles
        angle1 = angle1 / 180 * np.pi
        angle2 = angle2 / 180 * np.pi
        arc_len = (angle2 - angle1) * radius
        if n:
            n_sub = n - 1
        else:
            n_sub = int(arc_len / gap)
        xc, yc = xo[0], xo[1]
        angles = np.linspace(angle1, angle2, n_sub + 1)
        points = [
            [xc + radius * np.cos(ang), yc + radius * np.sin(ang)] for ang in angles
        ]
        rebar_xy = points
        data = dict(
            rebar_xy=rebar_xy, color=color, name=group_name, dia=dia, matTag=ops_mat_tag
        )
        self.rebar_data.append(data)

    def get_rebars_num(self):
        """Returns the number of rebars.

        Returns
        -------
        nums: int, number of rebars.
        """
        nums = 0
        for data in self.rebar_data:
            nums += len(data["rebar_xy"])
        return nums

    def get_rebars_area(self):
        """Returns the total area of rebars.

        Returns
        -------
        area: float, total area of rebars.
        """
        area = 0.0
        if self.rebar_data:
            for data in self.rebar_data:
                rebar_xy = data["rebar_xy"]
                dia = data["dia"]
                rebar_areas = []
                for _ in rebar_xy:
                    rebar_areas.append(np.pi / 4 * dia**2)
                area += np.sum(rebar_areas)
        return area

    def get_centroid(self):
        """Return the centroid.

        Returns
        -------
        centroid: list[float, float], [xc, yc]
        """
        return self.centroid

    def get_area(self):
        """Return section area. For a single-material section, it is the geometric area,
        and for a composite section, it is the equivalent area.

        Returns
        -------
        area: float, section area.
        """
        if self.frame_sec_props:
            return self.frame_sec_props["A"]
        elif self.sec_props:
            return self.sec_props["A"]
        else:
            txt1 = get_random_color_rich("get_frame_props()")
            txt2 = get_random_color_rich("get_sec_props()")
            raise RuntimeError(f"{PKG_PREFIX}Please run method {txt1} or {txt2} first!")

    def get_geom_area(self):
        """Return the total geometric area of a section.

        Returns
        -------
        area: float, section area.
        """
        return self.geom_area

    def get_iy(self):
        """Return Moment of inertia of the section around the y-axis.

        Returns
        -------
        iy: float, Moment of inertia of the section around the y-axis.
        """
        if self.frame_sec_props:
            return self.frame_sec_props["Iy"]
        elif self.sec_props:
            return self.sec_props["Iy"]
        else:
            return self.Iy

    def get_iz(self):
        """Return Moment of inertia of the section around the z-axis.

        Returns
        -------
        iz: float, Moment of inertia of the section around the z-axis.
        """
        if self.frame_sec_props:
            return self.frame_sec_props["Iz"]
        elif self.sec_props:
            return self.sec_props["Iz"]
        else:
            return self.Iz

    def get_j(self):
        """Return section torsion constant.

        Returns
        -------
        j: float, section torsion constant.
        """
        if self.frame_sec_props:
            return self.frame_sec_props["J"]
        elif self.sec_props:
            return self.sec_props["J"]
        else:
            self.get_frame_props()
            return self.frame_sec_props["J"]

    def get_dist_from_centroid(self):
        """Return the distance from section edge to the centroid.

        Returns
        -------
        list, [ztop, zbot, yright, yleft]
            z axis top, z axis bottom, y-axis right, y-axis left
        """
        ymax = self.points[:, 0].max()
        ymin = self.points[:, 0].min()
        zmax = self.points[:, 1].max()
        zmin = self.points[:, 1].min()
        ztop = abs(zmax - self.centroid[1])
        zbot = abs(zmin - self.centroid[1])
        yleft = abs(ymin - self.centroid[0])
        yright = abs(ymax - self.centroid[0])
        return [ztop, zbot, yright, yleft]

    def _run_sec_props(self, Eref: float = 1.0):
        self.section.calculate_geometric_properties()
        self.section.calculate_warping_properties()
        cx, cy = (0.0, 0.0) if self.is_centring else self.section.get_c()
        phi = self.section.get_phi()  # Principal bending axis angle
        if self.section.is_composite():
            ixx_c, iyy_c, ixy_c = self.section.get_eic(Eref)
            # Elastic section moduli about the centroidal axis with respect to the top and bottom fibers
            zxx_plus, zxx_minus, zyy_plus, zyy_minus = self.section.get_ez(Eref)
            # Shear area for loading about the centroidal axis
            area_sx, area_sy = self.section.get_eas(Eref)
            self.area = self.section.get_ea(Eref)
            # St. Venant torsion constant
            self.J = self.section.get_ej(Eref)
            mass = self.section.get_mass()
        else:
            ixx_c, iyy_c, ixy_c = self.section.get_ic()
            zxx_plus, zxx_minus, zyy_plus, zyy_minus = self.section.get_z()
            area_sx, area_sy = self.section.get_as()
            self.area = self.section.get_area()
            self.J = self.section.get_j()
            mass = self.area
        self.Iy = ixx_c
        self.Iz = iyy_c
        rho_rebar = self.get_rebars_area() / self.geom_area
        sec_props = dict(
            A=self.area,
            Asy=area_sx,
            Asz=area_sy,
            centroid=(cx, cy),
            Iy=ixx_c,
            Iz=iyy_c,
            Iyz=ixy_c,
            Wyt=zxx_plus,
            Wyb=zxx_minus,
            Wzt=zyy_plus,
            Wzb=zyy_minus,
            J=self.J,
            phi=phi,
            mass=mass,
            rho_rebar=rho_rebar,
        )
        self.sec_props = sec_props

    def get_sec_props(
        self,
        Eref: float = 1.0,
        display_results: bool = False,
        fmt: str = "8.3E",
        plot_centroids: bool = False,
    ):
        """
        Solving Section Geometry Properties by Finite Element Method, by ``sectionproperties`` pacakge.
        See `sectionproperties results <https://sectionproperties.readthedocs.io/en/latest/user_guide/results.html#>`_

        This command may be slower. If you don't need features such as shear area, you can use
        method :py:meth:`~opstool.preprocessing.SecMesh.get_frame_props`.

        Parameters
        -----------
        Eref: float, default=1.0
            Reference modulus of elasticity, it is important to analyze the composite section.
            If it is not a composite section, please ignore this parameter.
        display_results : bool, default=True
            whether to display the results.
        fmt : str, optional
            Number formatting string when display_results=True.
        plot_centroids : bool, default=False
            whether to plot centroids.

        Returns
        -----------
        sec_props: dict
            section props dict, including:

            * Cross-sectional area (A)
            * Shear area (Asy, Asz)
            * Elastic centroid (centroid)
            * Second moments of area about the centroidal axis (Iy, Iz, Iyz)
            * Elastic section moduli about the centroidal axis with respect to the top and bottom
              fibres (Wyt, Wyb, Wzt, Wzb)

            * Torsion constant (J)
            * Principal axis angle (phi)
            * Section mass (mass), only true if material density is defined,
              otherwise geometric area (mass density is 1)

            * ratio of reinforcement (rho_rebar)

        .. Note::
            If it is not a composite section, please ignore the `Eref` parameter;
            Otherwise, please use the `Eref` parameter, all section properties will
            be transformed according to the reference material, and the mechanical properties of
            the reference material are then used in the practical analysis.

            Note that according to the OpenSees convention,
            the x-axis refers to the normal direction of the section,
            the y-axis refers to the abscissa,
            and the z-axis refers to the ordinate direction.
        """
        self._run_sec_props(Eref)
        if display_results:
            # section.display_results()
            syms = [
                "A",
                "Asy",
                "Asz",
                "centroid",
                "Iy",
                "Iz",
                "Iyz",
                "Wyt",
                "Wyb",
                "Wzt",
                "Wzb",
                "J",
                "phi",
                "mass",
                "rho_rebar",
            ]
            defs = [
                "Cross-sectional area",
                "Shear area y-axis",
                "Shear area z-axis",
                "Elastic centroid",
                "Moment of inertia y-axis",
                "Moment of inertia z-axis",
                "Product of inertia",
                "Section moduli of top fibres y-axis",
                "Section moduli of bottom fibres y-axis",
                "Section moduli of top fibres z-axis",
                "Section moduli of bottom fibres z-axis",
                "Torsion constant",
                "Principal axis angle",
                "Section mass",
                "Ratio of reinforcement",
            ]
            table = Table(title="Section Properties")
            table.add_column("Symbol", style="cyan", no_wrap=True)
            table.add_column("Value", style="magenta")
            table.add_column("Definition", style="green")
            for sym_, def_ in zip(syms, defs):
                if sym_ != "centroid":
                    table.add_row(sym_, f"{self.sec_props[sym_]:>{fmt}}", def_)
                else:
                    table.add_row(
                        sym_,
                        f"({self.sec_props[sym_][0]:>{fmt}}, {self.sec_props[sym_][1]:>{fmt}})",
                        def_,
                    )
            CONSOLE.print(table)
        if plot_centroids:
            self.section.plot_centroids()
        return self.sec_props

    def get_frame_props(
        self, Eref: float = 1.0, display_results: bool = False, fmt: str = "8.3E"
    ):
        """Calculates and returns the properties required for a frame analysis.
        See
        `sectionproperties frame_properties <https://sectionproperties.readthedocs.io/en/stable/gen/sectionproperties.
        analysis.section.Section.html#sectionproperties.analysis.section.Section.calculate_frame_properties>`_

        This method is fast, but cannot calculate the shear area compared to the
        method :py:meth:`~opstool.preprocessing.SecMesh.get_sec_props`.

        Parameters
        ----------
        Eref: float, default=1.0
            Reference modulus of elasticity, it is important to analyze the composite section.
            If it is not a composite section, please ignore this parameter.
            See `<https://sectionproperties.readthedocs.io/en/
            latest/user_guide/results.html#label-material-affects-results>`_
        display_results : bool, default=True
            whether to display the results.
        fmt : str, optional
            Number formatting string when display_results=True.

        Returns
        -----------
        sec_props: dict
            section props dict, including:

            * Cross-sectional area (A)
            * Elastic centroid (centroid)
            * Second moments of area about the centroidal axis (Iy, Iz, Iyz)
            * Elastic section moduli about the centroidal axis with respect to
              the top and bottom fibers (Wyt, Wyb, Wzt, Wzb)

            * Torsion constant (J)
            * Principal axis angle (phi)
            * Section mass (mass), only true if material density is defined, otherwise geometric
              area (mass density is 1)

            * ratio of reinforcement (rho_rebar)

        .. Note::
            If it is not a composite section, please ignore the `Eref` parameter;
            Otherwise, please use the `Eref` parameter, all section properties will
            be transformed according to the reference material, and the mechanical properties of
            the reference material are then used in the practical analysis.

            Note that according to the OpenSees convention,
            the x-axis refers to the normal direction of the section,
            the y-axis refers to the abscissa,
            and the z-axis refers to the ordinate direction.
        """
        # self.section.calculate_geometric_properties()
        (area, ixx_c, iyy_c, ixy_c, j, phi) = self.section.calculate_frame_properties(
            solver_type="direct"
        )
        cx, cy = (0.0, 0.0) if self.is_centring else self.section.get_c()
        # self.section.section_props.calculate_centroidal_properties(self.points)
        if self.section.is_composite():
            zxx_plus, zxx_minus, zyy_plus, zyy_minus = self.section.get_ez(Eref)
            Eeff = self.section.get_e_eff()
            self.area = area * Eeff / Eref
            self.Iy = ixx_c / Eref
            self.Iz = iyy_c / Eref
            self.J = j / Eref
        else:
            self.section.calculate_geometric_properties()
            zxx_plus, zxx_minus, zyy_plus, zyy_minus = self.section.get_z()
            self.area = area
            self.Iy = ixx_c
            self.Iz = iyy_c
            self.J = j
        rho_rebar = self.get_rebars_area() / self.geom_area
        sec_props = dict(
            A=self.area,
            centroid=(cx, cy),
            Iy=self.Iy,
            Iz=self.Iz,
            Iyz=ixy_c,
            Wyt=zxx_plus,
            Wyb=zxx_minus,
            Wzt=zyy_plus,
            Wzb=zyy_minus,
            J=self.J,
            phi=phi,
            rho_rebar=rho_rebar,
        )
        if display_results:
            syms = [
                "A",
                "centroid",
                "Iy",
                "Iz",
                "Iyz",
                "Wyt",
                "Wyb",
                "Wzt",
                "Wzb",
                "J",
                "phi",
                "rho_rebar",
            ]
            defs = [
                "Cross-sectional area",
                "Elastic centroid",
                "Moment of inertia y-axis",
                "Moment of inertia z-axis",
                "Product of inertia",
                "Section moduli of top fibres y-axis",
                "Section moduli of bottom fibres y-axis",
                "Section moduli of top fibres z-axis",
                "Section moduli of bottom fibres z-axis",
                "Torsion constant",
                "Principal axis angle",
                "Ratio of reinforcement",
            ]
            table = Table(title="Frame Section Properties")
            table.add_column("Symbol", style="cyan", no_wrap=True)
            table.add_column("Value", style="magenta")
            table.add_column("Definition", style="green")
            for sym_, def_ in zip(syms, defs):
                if sym_ != "centroid":
                    table.add_row(
                        sym_, "{:>{fmt}}".format(sec_props[sym_], fmt=fmt), def_
                    )
                else:
                    table.add_row(
                        sym_,
                        f"({sec_props[sym_][0]:>{fmt}}, {sec_props[sym_][1]:>{fmt}})",
                        def_,
                    )
            CONSOLE.print(table)
        self.frame_sec_props = sec_props
        return sec_props

    def display_all_results(self, Eref: float = 1.0, fmt: str = "8.6e"):
        """Prints all results that have been calculated by ``sectionproperties`` to the terminal.

        Parameters
        ----------
        Eref: float, default=1.0
            Reference modulus of elasticity, it is important to analyze the composite section.
            If it is not a composite section, please ignore this parameter.
            See `sectionproperties document <https://sectionproperties.readthedocs.io/en/
            latest/user_guide/results.html#label-material-affects-results>`_
        fmt : str, optional
            Number formatting string.
        """
        if not self.sec_props:
            self._run_sec_props(Eref)
        self.section.display_results(fmt=fmt)

    @staticmethod
    def _plot_stress(stress_post, plot_stress, **kargs):
        # ------------Primary Stress Plots
        if plot_stress == "n_xx":
            stress_type = "n_zz"
            title = "Stress Contour Plot - $\\sigma_{xx,N}$"
        elif plot_stress == "myy_xx":
            stress_type = "mxx_zz"
            title = "Stress Contour Plot - $\\sigma_{xx,Myy}$"
        elif plot_stress == "mzz_xx":
            stress_type = "myy_zz"
            title = "Stress Contour Plot - $\\sigma_{xx,Mzz}$"
        elif plot_stress == "m_xx":
            stress_type = "m_zz"
            title = "Stress Contour Plot - $\\sigma_{xx,\\Sigma M}$"
        elif plot_stress == "mxx_xy":
            stress_type = "mzz_zx"
            title = "Stress Contour Plot - $\\tau_{xy,Mxx}$"
        elif plot_stress == "mxx_xz":
            stress_type = "mzz_zy"
            title = "Stress Contour Plot - $\\tau_{xz,Mxx}$"
        elif plot_stress == "mxx_xyz":
            stress_type = "mzz_zxy"
            title = "Stress Contour Plot - $\\tau_{xyz,Mxx}$"
        elif plot_stress == "vy_xy":
            stress_type = "vx_zx"
            title = "Stress Contour Plot - $\\tau_{xy,Vy}$"
        elif plot_stress == "vy_xz":
            stress_type = "vx_zy"
            title = "Stress Contour Plot - $\\tau_{xz,Vy}$"
        elif plot_stress == "vy_xyz":
            stress_type = "vx_zxy"
            title = "Stress Contour Plot - $\\tau_{xyz,Vy}"
        elif plot_stress == "vz_xy":
            stress_type = "vy_zx"
            title = "Stress Contour Plot - $\\tau_{xy,Vz}$"
        elif plot_stress == "vz_xz":
            stress_type = "vy_zy"
            title = "Stress Contour Plot - $\\tau_{xz,Vz}$"
        elif plot_stress == "vz_xyz":
            stress_type = "vy_zxy"
            title = "Stress Contour Plot - $\\tau_{xyz,Vz}$"
        elif plot_stress == "v_xy":
            stress_type = "v_zx"
            title = "Stress Contour Plot - $\\tau_{xy,V}$"
        elif plot_stress == "v_xz":
            stress_type = "v_zy"
            title = "Stress Contour Plot - $\\tau_{xz,V}$"
        elif plot_stress == "v_xyz":
            stress_type = "v_zxy"
            title = "Stress Contour Plot - $\\tau_{xyz,V}$"
        # ------------Combined Stress Plots
        elif plot_stress == "xx":
            stress_type = "zz"
            title = "Stress Contour Plot - $\\sigma_{xx}$"
        elif plot_stress == "xy":
            stress_type = "zx"
            title = "Stress Contour Plot - $\\tau_{xy}$"
        elif plot_stress == "xz":
            stress_type = "zy"
            title = "Stress Contour Plot - $\\tau_{xz}$"
        elif plot_stress == "xyz":
            stress_type = "zxy"
            title = "Stress Contour Plot - $\\tau_{xyz}$"
        elif plot_stress == "p1":
            stress_type = "11"
            title = "Stress Contour Plot - $\\sigma_{1}$"
        elif plot_stress == "p3":
            stress_type = "33"
            title = "Stress Contour Plot - $\\sigma_{3}$"
        elif plot_stress == "vm":
            stress_type = "vm"
            title = "Stress Contour Plot - $\\sigma_{vM}$"
        else:
            raise ValueError("not supported plot_stress type!")
        if stress_type in ["mzz_zxy", "vx_zxy", "vy_zxy", "v_zxy", "zxy"]:
            stress_post.plot_stress_vector(stress=stress_type, title=title, **kargs)
        else:
            stress_post.plot_stress(stress=stress_type, title=title, **kargs)

    def get_stress(
        self,
        N: float = 0,
        Vy: float = 0,
        Vz: float = 0,
        Myy: float = 0,
        Mzz: float = 0,
        Mxx: float = 0,
        plot_stress: str = "all",
        cmap: str = "YlOrBr",
        normalize: bool = False,
        fmt: str = "{x:.4e}",
        colorbar_label: str = "Stress",
        alpha: float = 0.75,
        **kargs,
    ):
        """Calculates the cross-section stress resulting from design actions and returns
        a list of dictionaries containing the cross-section stresses for each region by
        method :py:meth:`~opstool.preprocessing.SecMesh.assign_group`.

        .. Note::
            This function is only available for elastic stress analysis, and reinforcement is ignored.
            The stresses are realistic only if you specify the correct material for each geometry region.

        Parameters
        ----------
        N : float, optional
            Axial force, by default 0
        Vy : float, optional
            Shear force acting in the y-direction, by default 0
        Vz : float, optional
            Shear force acting in the z-direction, by default 0
        Myy : float, optional
            Bending moment about the centroidal yy-axis, by default 0
        Mzz : float, optional
            Bending moment about the centroidal zz-axis, by default 0
        Mxx : float, optional
            Torsion moment about the centroidal xx-axis, by default 0
        plot_stress : str, optional
            plot the various cross-section stresses, by default None.
            Note that according to the OpenSees convention,
            the x-axis refers to the normal direction of the section,
            the y-axis refers to the abscissa,
            and the z-axis refers to the ordinate direction.
            Optional as follows (if plot_stress="all", will plot all stress types):

            - **Combined Stress Plots**:

                * "xx"--combined normal stress resulting from all actions;
                * "xy"--y-component of the shear stress resulting from all actions;
                * "xz"-- z-component of the shear stress resulting from all actions;
                * "xyz"--resultant shear stress resulting from all actions;
                * "p1"--major principal stress resulting from all actions;
                * "p3"-- Minor principal stress resulting from all actions;
                * "vm"--von Mises stress resulting from all actions;

            - **Primary Stress Plots**:

                * "n_xx"--normal stress resulting from the axial load N;
                * "myy_xx"--normal stress resulting from the bending moment Myy;
                * "mzz_xx"--normal stress resulting from the bending moment Mzz;
                * "m_xx"--normal stress resulting from all bending moments Myy+Mzz;
                * "mxx_xy"--y-component of the shear stress resulting from the torsion moment Mxx;
                * "mxx_xz"--z-component of the shear stress resulting from the torsion moment Mxx;
                * "mxx_xyz"--resultant shear stress resulting from the torsion moment Mxx;
                * "vy_xy"--y-component of the shear stress resulting from the shear force Vy;
                * "vy_xz"--z-component of the shear stress resulting from the shear force Vy;
                * "vy_xyz"--resultant shear stress resulting from the shear force Vy;
                * "vz_xy"--y-component of the shear stress resulting from the shear force Vz;
                * "vz_xz"--z-component of the shear stress resulting from the shear force Vz;
                * "vz_xyz"--resultant shear stress resulting from the shear force Vz;
                * "v_xy"--y-component of the shear stress resulting from the sum of the applied shear forces Vy+Vz;
                * "v_xz"--z-component of the shear stress resulting from the sum of the applied shear forces Vy+Vz;
                * "v_xyz"--resultant shear stress resulting from the sum of the applied shear forces Vy+Vz;

        cmap : str, optional
            Matplotlib color map, by default 'coolwarm'
        normalize : bool, optional
            If set to true, the CenteredNorm is used to scale the colormap.
            If set to false, the default linear scaling is used., by default True
        fmt: str
            Number formatting string, see `here <https://docs.python.org/3/library/string.html>`_
        colorbar_label: str, default='Stress'
            Colorbar label
        alpha: float, default=0.75
            Transparency of the mesh outlines

        Returns
        --------
        list[dict]:
            A list of dictionaries containing the cross-section stresses for each region by
            method :py:meth:`~opstool.preprocessing.SecMesh.assign_group`.
        """
        plot_stress = plot_stress.lower()
        if (not self.frame_sec_props) and (not self.sec_props):
            _ = self.get_frame_props()
        if self.section.section_props.omega is None and (
            Vy != 0 or Vz != 0 or Mxx != 0
        ):
            _ = self.get_sec_props()
        stress_post = self.section.calculate_stress(
            n=N, vx=Vy, vy=Vz, mxx=Myy, myy=Mzz, mzz=Mxx
        )
        name_map = dict(
            xx="sig_zz",
            xy="sig_zx",
            xz="sig_zy",
            xyz="sig_zxy",
            p1="sig_11",
            p3="sig_33",
            vm="sig_vm",
            n_xx="sig_zz_n",
            myy_xx="sig_zz_mxx",
            mzz_xx="sig_zz_myy",
            m_xx="sig_zz_m",
            mxx_xy="sig_zx_mzz",
            mxx_xz="sig_zy_mzz",
            mxx_xyz="sig_zxy_mzz",
            vy_xy="sig_zx_vx",
            vy_xz="sig_zy_vx",
            vy_xyz="sig_zxy_vx",
            vz_xy="sig_zx_vy",
            vz_xz="sig_zy_vy",
            vz_xyz="sig_zxy_vy",
            v_xy="sig_zx_v",
            v_xz="sig_zy_v",
            v_xyz="sig_zxy_v",
        )

        if plot_stress.lower() == "all":
            for name in name_map.keys():
                self._plot_stress(
                    stress_post=stress_post,
                    plot_stress=name,
                    cmap=cmap,
                    normalize=normalize,
                    fmt=fmt,
                    colorbar_label=colorbar_label,
                    alpha=alpha,
                    **kargs,
                )
        else:
            self._plot_stress(
                stress_post=stress_post,
                plot_stress=plot_stress,
                cmap=cmap,
                normalize=normalize,
                fmt=fmt,
                colorbar_label=colorbar_label,
                alpha=alpha,
                **kargs,
            )

        stresses_temp = stress_post.get_stress()
        stresses = []
        for stress, name in zip(stresses_temp, self.geom_names):
            temp = dict()
            temp["Region"] = name
            for name2, value in name_map.items():
                temp["sig_" + name2] = stress[value]
            stresses.append(temp)
        return stresses

    def centring(self):
        """
        Move the section centroid to (0, 0).

        Returns
        ---------
        None
        """
        self.points -= self.centroid
        names = self.fiber_centers_map.keys()
        # move fibers
        for name in names:
            self.fiber_centers_map[name] -= self.centroid
        # move rebars
        for i in range(len(self.rebar_data)):
            self.rebar_data[i]["rebar_xy"] -= self.centroid
        # move geoms
        for name, geom in self.geom_group_map.items():
            new_geom = geom.shift_section(-self.centroid[0], -self.centroid[1])
            self.geom_group_map[name] = new_geom
        self.is_centring = True
        self.centroid = np.array([0.0, 0.0])

    def rotate(self, theta: float = 0):
        """Rotate the section clockwise.

        Parameters
        ------------
        theta : float, default=0
             Rotation angle, unit: degree.

        Returns
        ---------
        None
        """
        theta = theta / 180 * np.pi

        if not self.is_centring:
            self.centring()

        x_rot, y_rot = sec_rotation(self.points[:, 0], self.points[:, 1], theta)
        self.points[:, 0], self.points[:, 1] = x_rot, y_rot

        names = self.fiber_centers_map.keys()
        for name in names:
            x_rot, y_rot = sec_rotation(
                self.fiber_centers_map[name][:, 0],
                self.fiber_centers_map[name][:, 1],
                theta,
            )
            self.fiber_centers_map[name][:, 0], self.fiber_centers_map[name][:, 1] = (
                x_rot,
                y_rot,
            )
        # rebar
        for i, data in enumerate(self.rebar_data):
            rebar_xy = self.rebar_data[i]["rebar_xy"]
            x_rot, y_rot = sec_rotation(rebar_xy[:, 0], rebar_xy[:, 1], theta)
            (
                self.rebar_data[i]["rebar_xy"][:, 0],
                self.rebar_data[i]["rebar_xy"][:, 1],
            ) = (x_rot, y_rot)

    def to_opspy_cmds(self, secTag: int, GJ: float = None, G: float = None):
        """Generate openseespy fiber section command.

        Parameters
        ------------
        secTag : int
            The section tag assigned in OpenSees.
        GJ: float, default = None
            Torsion stiffness.
            Note that at least one of GJ and G needs to be specified,
            and if both, it will be calculated by GJ.
        G: float, default = None
            Shear modulus. The program automatically calculates the torsion constant.
            Note that at least one of GJ and G needs to be specified,
            and if both, it will be calculated by GJ.

        Returns
        ----------
        None
        """
        if GJ is None:
            if G is None:
                raise ValueError("GJ and G need to assign at least one!")
            else:
                GJ = G * self.get_j()

        ops.section("Fiber", secTag, "-GJ", GJ)

        names = self.fiber_centers_map.keys()
        for name in names:
            centers = self.fiber_centers_map[name]
            areas = self.fiber_areas_map[name]
            matTag = self.mat_ops_map[name]
            for center, area in zip(centers, areas):
                ops.fiber(center[0], center[1], area, matTag)
        # rebars
        for data in self.rebar_data:
            rebar_xy = data["rebar_xy"]
            dia = data["dia"]
            matTag = data["matTag"]
            for xy in rebar_xy:
                area = np.pi / 4 * dia**2
                ops.fiber(xy[0], xy[1], area, matTag)

    def to_file(
        self,
        output_path: str,
        secTag: int,
        GJ: float = None,
        G: float = None,
        fmt=":.6E",
    ):
        """Output the opensees fiber code to file.

        Parameters
        -------------
        output_path : str
            The filepath to save, e.g., r "my_dir/my_section.py"

            .. Note::
                Notes that output_path must be endswith ``.py`` or ``.tcl``,
                function will create the file by the right style.

        secTag : int
            The section tag assigned in OpenSees.
        GJ: float, default = None
            Torsion stiffness.
            Note that at least one of GJ and G needs to be specified,
            and if both, it will be calculated by GJ.
        G: float, default = None
            Shear modulus. The program automatically calculates the torsion constant.
            Note that at least one of GJ and G needs to be specified,
            and if both, it will be calculated by GJ.
        fmt : str, default = ":.6E"
            Formatting style for floating point numbers.

        Returns
        ---------
        None
        """
        if GJ is None:
            if G is None:
                raise ValueError("GJ and G need to assign at least one!")
            else:
                GJ = G * self.get_j()

        names = self.fiber_centers_map.keys()
        if output_path.endswith(".tcl"):
            self._to_tcl(output_path, names, secTag, GJ, fmt=fmt)
        elif output_path.endswith(".py"):
            self._to_py(output_path, names, secTag, GJ, fmt=fmt)
        else:
            raise ValueError("output_path must endwith .tcl or .py!")
        txt = get_random_color_rich(output_path)
        CONSOLE.print(f"{PKG_PREFIX} The file {txt} has been successfully written!")

    def _to_tcl(self, output_path, names, sec_tag, gj, fmt=":.6E"):
        with open(output_path, "w+") as output:
            output.write("# This document was created from opstool.SecMesh\n")
            output.write("# Author: Yexiang Yan  yexiang_yan@outlook.com\n\n")
            output.write(f"set secTag {sec_tag}\n")
            temp = "{"
            output.write(
                f"section fiberSec $secTag -GJ {gj} {temp};    # Define the fiber section\n"
            )
            txt = f"fiber {{{fmt}}} {{{fmt}}} {{{fmt}}} {{}};\n"
            for name in names:
                centers = self.fiber_centers_map[name]
                areas = self.fiber_areas_map[name]
                mat_tag = self.mat_ops_map[name]
                for center, area in zip(centers, areas):
                    output.write(txt.format(center[0], center[1], area, mat_tag))
            # rebar
            for data in self.rebar_data:
                output.write("    # Define Rebar\n")
                rebar_xy = data["rebar_xy"]
                dia = data["dia"]
                mat_tag = data["matTag"]
                for xy in rebar_xy:
                    area = np.pi / 4 * dia**2
                    output.write(txt.format(xy[0], xy[1], area, mat_tag))
            output.write("};    # end of fibersection definition\n")

    def _to_py(self, output_path, names, sec_tag, gj, fmt=":.6E"):
        with open(output_path, "w+") as output:
            output.write("# This document was created from opstool.SecMesh\n")
            output.write("# Author: Yexiang Yan  yexiang_yan@outlook.com\n\n")
            output.write("import openseespy.opensees as ops\n\n\n")
            output.write(
                f"ops.section('Fiber', {sec_tag}, '-GJ', {gj})  # Define the fiber section\n"
            )
            txt = f"ops.fiber({{{fmt}}}, {{{fmt}}}, {{{fmt}}}, {{}})\n"
            for name in names:
                centers = self.fiber_centers_map[name]
                areas = self.fiber_areas_map[name]
                mat_tag = self.mat_ops_map[name]
                for center, area in zip(centers, areas):
                    output.write(txt.format(center[0], center[1], area, mat_tag))
            # rebar
            for data in self.rebar_data:
                output.write("# Define Rebar\n")
                rebar_xy = data["rebar_xy"]
                dia = data["dia"]
                mat_tag = data["matTag"]
                for xy in rebar_xy:
                    area = np.pi / 4 * dia**2
                    output.write(txt.format(xy[0], xy[1], area, mat_tag))
            output.write("# end of fibersection definition\n")

    def view(self, fill: bool = True, show_legend: bool = True, ax=None):
        """Display the section mesh.

        Parameters
        -----------
        fill : bool, default=True
             Whether to fill the trangles.
        show_legend: bool, default=True
            Whether to show the legend.
        ax : matplotlib.axes.Axes, optional
            The axes to plot the section mesh.

        Returns
        --------
        None
        """

        # self.section.display_mesh_info()
        # self.section.plot_mesh()
        vertices = self.points
        x = vertices[:, 0]
        y = vertices[:, 1]
        aspect_ratio = (np.max(y) - np.min(y)) / (np.max(x) - np.min(x))
        self._plot_mpl(fill, aspect_ratio, show_legend=show_legend, ax=ax)

    def _plot_mpl(self, fill, aspect_ratio, show_legend: bool = True, ax=None):
        # matplotlib plot
        if aspect_ratio <= 0.333:
            aspect_ratio = 0.333
        if aspect_ratio >= 3:
            aspect_ratio = 3
        if aspect_ratio < 1:
            figsize = 8, 8
        else:
            figsize = 6, 6 * aspect_ratio
        if ax is None:
            fig, ax = plt.subplots(figsize=figsize)

        # view the mesh
        vertices = self.points  # the coords of each triangle vertex
        x = vertices[:, 0]
        y = vertices[:, 1]
        for name, faces in self.fiber_cells_map.items():
            # faces = faces.astype(np.int64)
            if not fill:
                ax.triplot(
                    x,
                    y,
                    triangles=faces,
                    color=self.color_map[name],
                    lw=1.5,
                    zorder=-10,
                )
                ax.plot(
                    [],
                    [],
                    "-",
                    label=name,
                    color=self.color_map[name],
                )  # for legend illustration only
            else:
                patches = [
                    plt.Polygon(vertices[face_link, :2], closed=True)
                    for face_link in faces
                ]
                coll = PatchCollection(
                    patches,
                    facecolors=self.color_map[name],
                    edgecolors="k",
                    linewidths=0.25,
                    zorder=-10,
                )
                ax.add_collection(coll)
                # ax.triplot(x, y, triangles=faces, lw=0.3, color="black")
                ax.plot([], [], "s", label=name, color=self.color_map[name])
        # rebars
        rebar_names, rebar_colors = [], []
        for data in self.rebar_data:
            color = data["color"]
            rebar_xy = data["rebar_xy"]
            dia = data["dia"]
            name = data["name"]
            rebar_coords = []
            for xy in rebar_xy:
                rebar_coords.append(xy)
            patches = [plt.Circle((xy[0], xy[1]), dia / 2) for xy in rebar_coords]
            coll = PatchCollection(patches, facecolors=color)
            ax.add_collection(coll)
            if name not in rebar_names or color not in rebar_colors:
                rebar_names.append(name)
                rebar_colors.append(color)
                ax.plot([], [], "o", label=name, color=color)

        ax.set_aspect(aspect_ratio)
        ax.set_title(self.sec_name, fontsize=16)
        if show_legend:
            ax.legend(
                fontsize=12,
                shadow=False,
                markerscale=1.2,
                loc="center left",
                ncol=1,
                bbox_to_anchor=(1.01, 0.5),
                bbox_transform=ax.transAxes,
            )
        ax.set_xlabel("y", fontsize=15)
        ax.set_ylabel("z", fontsize=15)
        ax.tick_params(labelsize=12)
        ax.autoscale()
        plt.tight_layout()
        # plt.show()


def sec_rotation(x, y, theta):
    """
    Rotate the section coordinates counterclockwise by theta
    """
    x_new = x * np.cos(theta) + y * np.sin(theta)
    y_new = -x * np.sin(theta) + y * np.cos(theta)
    return x_new, y_new


def _lines_subdivide(x, y, gap):
    """
    The polylines consisting of coordinates x and y are divided by the gap.
    """
    lengths, mesh_lengths = [0.0], [0.0]
    for i in range(len(x) - 1):
        x1, y1 = x[i], y[i]
        x2, y2 = x[i + 1], y[i + 1]
        length = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        if length > gap:
            n = int(np.around(length / gap))
            mesh_lengths.extend([length / n] * n)
        else:
            mesh_lengths.append(length)
        lengths.append(length)
    cum_lengths = np.cumsum(lengths)
    cum_mesh_lengths = np.cumsum(mesh_lengths)
    xs = np.interp(cum_mesh_lengths, cum_lengths, x)
    ys = np.interp(cum_mesh_lengths, cum_lengths, y)
    new_xy = np.column_stack((xs, ys))
    return new_xy
