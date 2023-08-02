import numpy as np
from shapely import LineString
from .sec_mesh import (Rebars, SecMesh, add_circle, add_material,
                       add_polygon, offset, poly_offset, line_offset)

class section_library:

    def L_section(
        h: float, b: float, tw: float, tf: float,
        mesh_size: float = None,
        ops_matTag: int = 1,
        color: str = "#04d8b2"
    ):
        """L-shaped section.

        .. raw:: html

        <a href="https://sm.ms/image/3dnTRLefGOJVjHQ" target="_blank"><img src="https://s2.loli.net/2023/08/02/3dnTRLefGOJVjHQ.png" ></a>

        Parameters
        ----------
        h : float
            Section total height.
        b : float
            Section total width.
        tw : float
            Section web thickness.
        tf : float
            Section flange thickness.
        mesh_size : float, optional
            The mesh size, by default None
        ops_matTag : int, optional
            Already defined OpenSees material tags, by default 1
        color : str, optional
            Color for visualization, by default "#04d8b2"

        Returns
        -------
        The instance of the class :py:class:`~opstool.preprocessing.SecMesh`.
        """
        if mesh_size is None:
            mesh_size = (h / 20) * (b / 20) / 2
        outlines = [[0, 0], [b, 0], [b, tf],
                    [tw, tf], [tw, h], [0, h]]
        poly = add_polygon(outlines)

        sec = SecMesh(sec_name="L-shaped Section")
        sec.assign_group(dict(poly=poly))
        sec.assign_mesh_size(dict(poly=mesh_size))
        sec.assign_ops_matTag(dict(poly=ops_matTag))
        sec.assign_group_color(dict(poly=color))
        sec.mesh()
        sec.centring()
        return sec

    def L_flip_section(
        h: float, b: float, tw: float, tf: float,
        mesh_size: float = None,
        ops_matTag: int = 1,
        color: str = "#04d8b2"
    ):
        """Fipped L-shaped section.

        Parameters
        ----------
        h : float
            Section total height.
        b : float
            Section total width.
        tw : float
            Section web thickness.
        tf : float
            Section flange thickness.
        mesh_size : float, optional
            The mesh size, by default None
        ops_matTag : int, optional
            Already defined OpenSees material tags, by default 1
        color : str, optional
            Color for visualization, by default "#04d8b2"

        Returns
        -------
        The instance of the class :py:class:`~opstool.preprocessing.SecMesh`.
        """
        if mesh_size is None:
            mesh_size = (h / 20) * (b / 20) / 2
        outlines1 = [[0, 0], [tw, 0], [tw, h-tf], [0, h-tf]]
        outlines2 = [[0, h-tf], [b, h-tf], [b, h], [0, h]]
        poly1 = add_polygon(outlines1)
        poly2 = add_polygon(outlines2)

        sec = SecMesh(sec_name="Flip L-shaped Section")
        sec.assign_group(dict(poly1=poly1, poly2=poly2))
        sec.assign_mesh_size(dict(poly1=mesh_size, poly2=mesh_size))
        sec.assign_ops_matTag(dict(poly1=ops_matTag, poly2=ops_matTag))
        sec.assign_group_color(dict(poly1=color, poly2=color))
        sec.mesh()
        sec.centring()
        return sec

    def I_section(
        h: float, b1: float, b2: float, tw: float, tf1: float, tf2: float,
        mesh_size: float = None,
        ops_matTag: int = 1,
        color: str = "#04d8b2"
    ):
        """I-shaped section.

        .. raw:: html

        <a href="https://sm.ms/image/iYVKsW6cuGFfNxB" target="_blank"><img src="https://s2.loli.net/2023/08/02/iYVKsW6cuGFfNxB.png" ></a>

        Parameters
        ----------
        h : float
            Section total height.
        b1 : float
            Section total width of top flange.
        b2 : float
            Section total width of bottom flange.
        tw : float
            Section web thickness.
        tf1 : float
            Section top flange thickness.
        tf2 : float
            Section fbottom lange thickness.
        mesh_size : float, optional
            The mesh size, by default None
        ops_matTag : int, optional
            Already defined OpenSees material tags, by default 1
        color : str, optional
            Color for visualization, by default "#04d8b2"

        Returns
        -------
        The instance of the class :py:class:`~opstool.preprocessing.SecMesh`.
        """
        if mesh_size is None:
            mesh_size = (h / 20) * (b2 / 20) / 2
        diff_b = (b2 - b1) / 2
        outlines = [[0, 0], [b2, 0], [b2, tf2], [0.5*(b2+tw), tf2],
                    [0.5*(b2+tw), h-tf1], [b2-diff_b, h-tf1], [b2-diff_b, h],
                    [diff_b, h], [diff_b, h-tf1], [0.5*(b2-tw), h-tf1],
                    [0.5*(b2-tw), tf2], [0, tf2]]
        poly = add_polygon(outlines)

        sec = SecMesh(sec_name="I-shaped Section")
        sec.assign_group(dict(poly=poly))
        sec.assign_mesh_size(dict(poly=mesh_size))
        sec.assign_ops_matTag(dict(poly=ops_matTag))
        sec.assign_group_color(dict(poly=color))
        sec.mesh()
        sec.centring()
        return sec

    def T_section(
        h: float, b: float, tw: float, tf: float,
        mesh_size: float = None,
        ops_matTag: int = 1,
        color: str = "#04d8b2"
    ):
        """T-shaped section.

        Parameters
        ----------
        h : float
            Section total height.
        b : float
            Section total width.
        tw : float
            Section web thickness.
        tf : float
            Section flange thickness.
        mesh_size : float, optional
            The mesh size, by default None
        ops_matTag : int, optional
            Already defined OpenSees material tags, by default 1
        color : str, optional
            Color for visualization, by default "#04d8b2"

        Returns
        -------
        The instance of the class :py:class:`~opstool.preprocessing.SecMesh`.
        """
        if mesh_size is None:
            mesh_size = (h / 20) * (b / 20) / 2
        outlines = [[0.5*(b-tw), 0], [0.5*(b+tw), 0], [0.5*(b+tw), h-tf], [b, h-tf],
                    [b, h], [0, h], [0, h-tf], [0.5*(b-tw), h-tf]]
        poly = add_polygon(outlines)

        sec = SecMesh(sec_name="T-shaped Section")
        sec.assign_group(dict(poly=poly))
        sec.assign_mesh_size(dict(poly=mesh_size))
        sec.assign_ops_matTag(dict(poly=ops_matTag))
        sec.assign_group_color(dict(poly=color))
        sec.mesh()
        sec.centring()
        return sec

    def T_flip_section(
        h: float, b: float, tw: float, tf: float,
        mesh_size: float = None,
        ops_matTag: int = 1,
        color: str = "#04d8b2"
    ):
        """Fipped T-shaped section.

        Parameters
        ----------
        h : float
            Section total height.
        b : float
            Section total width.
        tw : float
            Section web thickness.
        tf : float
            Section flange thickness.
        mesh_size : float, optional
            The mesh size, by default None
        ops_matTag : int, optional
            Already defined OpenSees material tags, by default 1
        color : str, optional
            Color for visualization, by default "#04d8b2"

        Returns
        -------
        The instance of the class :py:class:`~opstool.preprocessing.SecMesh`.
        """
        if mesh_size is None:
            mesh_size = (h / 20) * (b / 20) / 2
        outlines = [[0, 0], [b, 0], [b, tf], [0.5*(b+tw), tf], [0.5*(b+tw), h],
                    [0.5*(b-tw), h], [0.5*(b-tw), tf], [0, tf]]
        poly = add_polygon(outlines)

        sec = SecMesh(sec_name="Flip T-shaped Section")
        sec.assign_group(dict(poly=poly))
        sec.assign_mesh_size(dict(poly=mesh_size))
        sec.assign_ops_matTag(dict(poly=ops_matTag))
        sec.assign_group_color(dict(poly=color))
        sec.mesh()
        sec.centring()
        return sec

    def channel_section(
        h: float, b: float, tw: float, tf1: float, tf2: float,
        mesh_size: float = None,
        ops_matTag: int = 1,
        color: str = "#04d8b2"
    ):
        """Channel-shaped section.

        .. raw:: html

        <a href="https://sm.ms/image/fRtxJPDWYo3uHOa" target="_blank"><img src="https://s2.loli.net/2023/08/02/fRtxJPDWYo3uHOa.png" ></a>

        Parameters
        ----------
        h : float
            Section total height.
        b : float
            Section total width.
        tw : float
            Section web thickness.
        tf1 : float
            Section top flange thickness.
        tf2 : float
            Section bottom flange thickness.
        mesh_size : float, optional
            The mesh size, by default None
        ops_matTag : int, optional
            Already defined OpenSees material tags, by default 1
        color : str, optional
            Color for visualization, by default "#04d8b2"

        Returns
        -------
        The instance of the class :py:class:`~opstool.preprocessing.SecMesh`.
        """
        if mesh_size is None:
            mesh_size = (h / 20) * (b / 20) / 2
        outlines = [[0, 0], [b, 0], [b, tf2], [tw, tf2],
                    [tw, h-tf1], [b, h-tf1], [b, h], [0, h]]
        poly = add_polygon(outlines)

        sec = SecMesh(sec_name="Channel Section")
        sec.assign_group(dict(poly=poly))
        sec.assign_mesh_size(dict(poly=mesh_size))
        sec.assign_ops_matTag(dict(poly=ops_matTag))
        sec.assign_group_color(dict(poly=color))
        sec.mesh()
        sec.centring()
        return sec

    def rect_section(
        h: float, b: float,
        mesh_size: float = None,
        ops_matTag: int = 1,
        color: str = "#04d8b2"
    ):
        """Solid rectangular section.

        Parameters
        ----------
        h : float
            Section total height.
        b : float
            Section total width.
        mesh_size : float, optional
            The mesh size, by default None
        ops_matTag : int, optional
            Already defined OpenSees material tags, by default 1
        color : str, optional
            Color for visualization, by default "#04d8b2"

        Returns
        -------
        The instance of the class :py:class:`~opstool.preprocessing.SecMesh`.
        """
        if mesh_size is None:
            mesh_size = (h / 20) * (b / 20) / 2
        outlines = [[0, 0], [b, 0], [b, h], [0, h]]
        poly = add_polygon(outlines)

        sec = SecMesh(sec_name="Rectangular Section")
        sec.assign_group(dict(poly=poly))
        sec.assign_mesh_size(dict(poly=mesh_size))
        sec.assign_ops_matTag(dict(poly=ops_matTag))
        sec.assign_group_color(dict(poly=color))
        sec.mesh()
        sec.centring()
        return sec

    def trapezoid_section(
        h: float, b1: float, b2: float,
        mesh_size: float = None,
        ops_matTag: int = 1,
        color: str = "#04d8b2"
    ):
        """Solid trapezoid section.

        Parameters
        ----------
        h : float
            Section total height.
        b1 : float
            Section total width of top flange.
        b2 : float
            Section total width of bottom flange.
        mesh_size : float, optional
            The mesh size, by default None
        ops_matTag : int, optional
            Already defined OpenSees material tags, by default 1
        color : str, optional
            Color for visualization, by default "#04d8b2"

        Returns
        -------
        The instance of the class :py:class:`~opstool.preprocessing.SecMesh`.
        """
        if mesh_size is None:
            mesh_size = (h / 20) * ((b1+b2) / 20) / 2
        diff_b = (b2 - b1) / 2
        outlines = [[0, 0], [b2, 0], [b2-diff_b, h], [diff_b, h]]
        poly = add_polygon(outlines)

        sec = SecMesh(sec_name="Trapezoid Section")
        sec.assign_group(dict(poly=poly))
        sec.assign_mesh_size(dict(poly=mesh_size))
        sec.assign_ops_matTag(dict(poly=ops_matTag))
        sec.assign_group_color(dict(poly=color))
        sec.mesh()
        sec.centring()
        return sec

    def box_section(
        h: float, b1: float, b2: float, tw: float, tf1: float, tf2: float,
        mesh_size: float = None,
        ops_matTag: int = 1,
        color: str = "#04d8b2"
    ):
        """Quadrilateral box section.

        Parameters
        ----------
        h : float
            Section total height.
        b1 : float
            Section total width of top flange.
        b2 : float
            Section total width of bottom flange.
        tw : float
            Section web thickness.
        tf1 : float
            Section top flange thickness.
        tf2 : float
            Section bottom flange thickness.
        mesh_size : float, optional
            The mesh size, by default None
        ops_matTag : int, optional
            Already defined OpenSees material tags, by default 1
        color : str, optional
            Color for visualization, by default "#04d8b2"

        Returns
        -------
        The instance of the class :py:class:`~opstool.preprocessing.SecMesh`.
        """
        if mesh_size is None:
            mesh_size = (h / 20) * ((b1 + b2) / 40) / 2
        diff_b = (b2 - b1) / 2
        bottom, right = LineString([[0, 0], [b2, 0]]), LineString([[b2, 0], [b2-diff_b, h]])
        top, left = LineString([[b2-diff_b, h], [diff_b, h]]), LineString([[diff_b, h], [0, 0]])
        bottom1 = bottom.parallel_offset(tf2, 'left', join_style=2)
        right1 = right.parallel_offset(tw, 'left', join_style=2)
        top1 = top.parallel_offset(tf1, 'left', join_style=2)
        left1 = left.parallel_offset(tw, 'left', join_style=2)
        outlines1 = [[0, 0], [b2, 0], [b2-diff_b, h], [diff_b, h]]
        outlines2 = [
            left1.intersection(bottom1),
            bottom1.intersection(right1),
            right1.intersection(top1),
            top1.intersection(left1)
        ]
        poly = add_polygon(outlines1, holes=[outlines2])

        sec = SecMesh(sec_name="Box Section")
        sec.assign_group(dict(poly=poly))
        sec.assign_mesh_size(dict(poly=mesh_size))
        sec.assign_ops_matTag(dict(poly=ops_matTag))
        sec.assign_group_color(dict(poly=color))
        sec.mesh()
        sec.centring()
        return sec

    def circular_section(
        d: float,
        mesh_size: float = None,
        ops_matTag: int = 1,
        color: str = "#04d8b2"
    ):
        """Solid circular section.

        Parameters
        ----------
        d : float
            Section diameter.
        mesh_size : float, optional
            The mesh size, by default None
        ops_matTag : int, optional
            Already defined OpenSees material tags, by default 1
        color : str, optional
            Color for visualization, by default "#04d8b2"

        Returns
        -------
        The instance of the class :py:class:`~opstool.preprocessing.SecMesh`.
        """
        if mesh_size is None:
            perimeter = np.pi * d
            mesh_size = (perimeter / 40) * (perimeter / 40) / 2
        angles = np.linspace(0, 2*np.pi, 41)
        xs = 0.5 * d * np.cos(angles)
        ys = 0.5 * d * np.sin(angles)
        outlines = [(x, y) for x, y in zip(xs, ys)]
        poly = add_polygon(outlines)

        sec = SecMesh(sec_name="Circular Section")
        sec.assign_group(dict(poly=poly))
        sec.assign_mesh_size(dict(poly=mesh_size))
        sec.assign_ops_matTag(dict(poly=ops_matTag))
        sec.assign_group_color(dict(poly=color))
        sec.mesh()
        return sec

    def pipe_section(
        d: float, tw: float,
        mesh_size: float = None,
        ops_matTag: int = 1,
        color: str = "#04d8b2"
    ):
        """Pipe section.

        Parameters
        ----------
        d : float
            Section diameter.
        tw : float
            Section pipe thickness.
        mesh_size : float, optional
            The mesh size, by default None
        ops_matTag : int, optional
            Already defined OpenSees material tags, by default 1
        color : str, optional
            Color for visualization, by default "#04d8b2"

        Returns
        -------
        The instance of the class :py:class:`~opstool.preprocessing.SecMesh`.
        """
        if mesh_size is None:
            perimeter = np.pi * d
            mesh_size = (perimeter / 40) * (perimeter / 40) / 2
        angles = np.linspace(0, 2*np.pi, 41)
        xs = 0.5 * d * np.cos(angles)
        ys = 0.5 * d * np.sin(angles)
        outlines = [(x, y) for x, y in zip(xs, ys)]
        xs = (0.5 * d - tw) * np.cos(angles)
        ys = (0.5 * d - tw) * np.sin(angles)
        hole = [(x, y) for x, y in zip(xs, ys)]
        poly = add_polygon(outlines, holes=[hole])

        sec = SecMesh(sec_name="Tube Section")
        sec.assign_group(dict(poly=poly))
        sec.assign_mesh_size(dict(poly=mesh_size))
        sec.assign_ops_matTag(dict(poly=ops_matTag))
        sec.assign_group_color(dict(poly=color))
        sec.mesh()
        return sec

    def circular_end_section(
        h: float, b: float,
        mesh_size: float = None,
        ops_matTag: int = 1,
        color: str = "#04d8b2"
    ):
        """Solid circular-end section.

        .. raw:: html

        <a href="https://sm.ms/image/9uIQFOJnHqYTZi5" target="_blank"><img src="https://s2.loli.net/2023/08/02/9uIQFOJnHqYTZi5.png" ></a>

        Parameters
        ----------
        h : float
            Section total height.
        b : float
            Section width of rectangular part.
        mesh_size : float, optional
            The mesh size, by default None
        ops_matTag : int, optional
            Already defined OpenSees material tags, by default 1
        color : str, optional
            Color for visualization, by default "#04d8b2"

        Returns
        -------
        The instance of the class :py:class:`~opstool.preprocessing.SecMesh`.
        """
        r = h / 2
        if mesh_size is None:
            mesh_size = (b / 10) * (h / 10) / 2
        # right half circle
        angles = np.linspace(-np.pi/2, np.pi/2, 21)
        xs = r * np.cos(angles) + b / 2
        ys = r * np.sin(angles)
        right_circ = [(x, y) for x, y in zip(xs, ys)]
        # left half circle
        angles = np.linspace(np.pi/2, 3*np.pi/2, 21)
        xs = r * np.cos(angles) - b / 2
        ys = r * np.sin(angles)
        left_circ = [(x, y) for x, y in zip(xs, ys)]
        outlines = right_circ + left_circ
        poly = add_polygon(outlines)

        sec = SecMesh(sec_name="Circular-End Section")
        sec.assign_group(dict(poly=poly))
        sec.assign_mesh_size(dict(poly=mesh_size))
        sec.assign_ops_matTag(dict(poly=ops_matTag))
        sec.assign_group_color(dict(poly=color))
        sec.mesh()
        sec.centring()
        return sec

    def circular_end_hollow_section(
        h: float, b: float, tw: float,
        mesh_size: float = None,
        ops_matTag: int = 1,
        color: str = "#04d8b2"
    ):
        """Hollow circular-end section.

        Parameters
        ----------
        h : float
            Section total height.
        b : float
            Section width of rectangular part.
        tw : float
            Section wall thickness.
        mesh_size : float, optional
            The mesh size, by default None
        ops_matTag : int, optional
            Already defined OpenSees material tags, by default 1
        color : str, optional
            Color for visualization, by default "#04d8b2"

        Returns
        -------
        The instance of the class :py:class:`~opstool.preprocessing.SecMesh`.
        """
        r = h / 2
        if mesh_size is None:
            mesh_size = (b / 20) * (h / 20) / 2
        # right half circle
        angles = np.linspace(-np.pi/2, np.pi/2, 21)
        xs = r * np.cos(angles) + b / 2
        ys = r * np.sin(angles)
        right_circ = [(x, y) for x, y in zip(xs, ys)]
        # left half circle
        angles = np.linspace(np.pi/2, 3*np.pi/2, 21)
        xs = r * np.cos(angles) - b / 2
        ys = r * np.sin(angles)
        left_circ = [(x, y) for x, y in zip(xs, ys)]
        outlines = right_circ + left_circ
        hole = offset(outlines, tw)
        poly = add_polygon(outlines, holes=[hole])

        sec = SecMesh(sec_name="Circular-End Hollow Section")
        sec.assign_group(dict(poly=poly))
        sec.assign_mesh_size(dict(poly=mesh_size))
        sec.assign_ops_matTag(dict(poly=ops_matTag))
        sec.assign_group_color(dict(poly=color))
        sec.mesh()
        sec.centring()
        return sec

    def octagonal_section(
        h: float, b: float, aa: float, bb: float,
        mesh_size: float = None,
        ops_matTag: int = 1,
        color: str = "#04d8b2"
    ):
        """Solid octagonal section.

        Parameters
        ----------
        h : float
            Section total height.
        b : float
            Section total width.
        aa : float
            Section chamfer width.
        bb : float
            Section chamfer height.
        mesh_size : float, optional
            The mesh size, by default None
        ops_matTag : int, optional
            Already defined OpenSees material tags, by default 1
        color : str, optional
            Color for visualization, by default "#04d8b2"

        Returns
        -------
        The instance of the class :py:class:`~opstool.preprocessing.SecMesh`.
        """
        if mesh_size is None:
            mesh_size = (h / 12) * (b / 12) / 2
        outlines = [[aa, 0], [b-aa, 0], [b, bb], [b, h-bb],
                    [b-aa, h], [aa, h], [0, h-bb], [0, bb]]
        poly = add_polygon(outlines)

        sec = SecMesh(sec_name="Octagonal Section")
        sec.assign_group(dict(poly=poly))
        sec.assign_mesh_size(dict(poly=mesh_size))
        sec.assign_ops_matTag(dict(poly=ops_matTag))
        sec.assign_group_color(dict(poly=color))
        sec.mesh()
        sec.centring()
        return sec

    def octagonal_hollow_section(
        h: float, b: float, aa: float, bb: float, tw: float,
        mesh_size: float = None,
        ops_matTag: int = 1,
        color: str = "#04d8b2"
    ):
        """Hollow octagonal section.

        Parameters
        ----------
        h : float
            Section total height.
        b : float
            Section total width.
        aa : float
            Section chamfer width.
        bb : float
            Section chamfer height.
        tw : float
            Section wall thickness.
        mesh_size : float, optional
            The mesh size, by default None
        ops_matTag : int, optional
            Already defined OpenSees material tags, by default 1
        color : str, optional
            Color for visualization, by default "#04d8b2"

        Returns
        -------
        The instance of the class :py:class:`~opstool.preprocessing.SecMesh`.
        """
        if mesh_size is None:
            mesh_size = (h / 12) * (b / 12) / 2
        outlines = [[aa, 0], [b-aa, 0], [b, bb], [b, h-bb],
                    [b-aa, h], [aa, h], [0, h-bb], [0, bb]]
        hole = offset(outlines, tw)
        poly = add_polygon(outlines, holes=[hole])

        sec = SecMesh(sec_name="Octagonal Hollow Section")
        sec.assign_group(dict(poly=poly))
        sec.assign_mesh_size(dict(poly=mesh_size))
        sec.assign_ops_matTag(dict(poly=ops_matTag))
        sec.assign_group_color(dict(poly=color))
        sec.mesh()
        sec.centring()
        return sec

    def octagonal_box_section(
        h: float, b: float, aa: float, bb: float, tw: float, tf1: float, tf2: float,
        mesh_size: float = None,
        ops_matTag: int = 1,
        color: str = "#04d8b2"
    ):
        """Box section with octagonal hole.

        .. raw:: html

        <a href="https://sm.ms/image/ec4JOQozC6USZwW" target="_blank"><img src="https://s2.loli.net/2023/08/02/ec4JOQozC6USZwW.png" ></a>

        Parameters
        ----------
        h : float
            Section total height.
        b : float
            Section total width.
        aa : float
            Chamfer width of octagonal hole.
        bb : float
            Chamfer height of octagonal hole.
        tw : float
            Section web thickness.
        tf1 : float
            Section top flange thickness.
        tf2 : float
            Section bottom flange thickness.
        mesh_size : float, optional
            The mesh size, by default None
        ops_matTag : int, optional
            Already defined OpenSees material tags, by default 1
        color : str, optional
            Color for visualization, by default "#04d8b2"

        Returns
        -------
        The instance of the class :py:class:`~opstool.preprocessing.SecMesh`.
        """
        if mesh_size is None:
            mesh_size = (h / 12) * (b / 12) / 2
        h, b = h - tf1 - tf2, b - 2 * tw
        hole = [
            [aa, 0], [b-aa, 0], [b, bb], [b, h-bb],
            [b-aa, h], [aa, h], [0, h-bb], [0, bb]
        ]
        outlines = [
            [-tw, -tf2], [b+tw, -tf2], [b+tw, h+tf1], [-tw, h+tf1],
        ]
        poly = add_polygon(outlines, holes=[hole])

        sec = SecMesh(sec_name="Octagonal Box Section")
        sec.assign_group(dict(poly=poly))
        sec.assign_mesh_size(dict(poly=mesh_size))
        sec.assign_ops_matTag(dict(poly=ops_matTag))
        sec.assign_group_color(dict(poly=color))
        sec.mesh()
        sec.centring()
        return sec


# def sec_plot(
#         sec,
#         fill: bool = True,
#         engine: str = "plotly",
#         save_html: str = None):
#     """Display the section mesh.

#     Parameters
#     -----------
#     fill: bool, default=True
#         Whether to fill the trangles.
#     engine: str, default='plotly'
#         Plot engine, optional "plotly" or "matplotlib".
#     save_html: str, default="SecMesh.html"
#         If set, the figure will save as a html file, only useful for engine="plotly".
#         If False or None, this parameter will be ignored.

#     Returns
#     --------
#     None
#     """
#     sec.view(fill=fill, engine=engine, save_html=save_html, show_hover=False)


# def get_sec_frame_props(sec, *args, **kargs):
#     return sec.get_frame_props(*args, **kargs)

# def get_sec_props(sec, *args, **kargs):
#     return sec.get_sec_props(*args, **kargs)
