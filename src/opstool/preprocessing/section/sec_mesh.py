"""
SecMesh: A module to mesh the cross-section with triangular fibers
"""

import matplotlib.pyplot as plt
import numpy as np
import openseespy.opensees as ops
import plotly.graph_objects as go
import plotly.io as pio
from matplotlib.collections import PatchCollection
from sectionproperties.analysis.section import Section
from sectionproperties.pre.geometry import CompoundGeometry, Geometry
from sectionproperties.pre.pre import Material
from shapely.geometry import LineString, Polygon
from rich.console import Console
from rich.table import Table


def _to_section(geom_obj, time_info=False):
    return Section(geom_obj, time_info)


class SecMesh:
    """A class to mesh the cross-section with triangular fibers.

    Parameters
    --------------
    sec_name : str
        Assign a name to the section.

    Returns
    -----------
    None
    """

    def __init__(self, sec_name: str = "My Section"):

        self.sec_name = sec_name

        # * mesh obj
        self.mesh_obj = None
        self.section = None
        self.points = None
        self.cells_map = dict()
        self.centers_map = dict()
        self.areas_map = dict()
        self.center = None

        # * data group
        self.group_map = dict()
        self.mat_ops_map = dict()
        self.mesh_size_map = dict()

        # *rebar data
        self.rebar_data = []

        # * section geo props
        self.sec_props = dict()

        self.color_map = dict()
        self.colors_default = [
            "#ffb900",
            "#037ef3",
            "#1aafd0",
            "#fc636b",
            "#11862f",
            "#832561",
            "#f48924",
            "#52565e",
        ]
        self.is_centring = False

    def assign_group(self, group: dict[str, any]):
        """Assign the group dict for each mesh.

        Parameters
        ------------
        group : dict
            A dict of name as key, geometry obj as value.

        Returns
        ----------
        instance
        """
        self.group_map = group.copy()
        return self

    def assign_mesh_size(self, mesh_size: dict[str, float]):
        """Assign the mesh size dict for each mesh.

        Parameters
        ------------
        mesh_size : dict[str, float]
            A dict of name as key, mesh size as value.

        Returns
        ------------
        instance
        """
        if not self.group_map:
            raise ValueError("The assign_group method should be run first!")
        for name in mesh_size.keys():
            if name not in self.group_map.keys():
                raise ValueError(
                    f"{name} is not specified in the assign_group function!"
                )
        self.mesh_size_map = mesh_size.copy()
        return self

    def assign_ops_matTag(self, mat_tag: dict[str, int]):
        """Assign the mesh size dict for each mesh.

        Parameters
        --------------
        mat_tag : dict[str, int]
            A dict of name as key, opensees matTag previous defined as value.

        Returns
        ----------
        instance
        """
        if not self.group_map:
            raise ValueError("The assign_group method should be run first!")
        for name in mat_tag.keys():
            if name not in self.group_map.keys():
                raise ValueError(
                    f"{name} is not specified in the assign_group function!"
                )
        self.mat_ops_map = mat_tag.copy()
        return self

    def assign_group_color(self, colors):
        """Assign the color dict to plot the section.

        Parameters
        -------------
        colors : dict[str, str]
            A dict of name as key, color as value.
        """
        if not self.group_map:
            raise ValueError("The assign_group method should be run first!")
        for name in colors.keys():
            if name not in self.group_map.keys():
                raise ValueError(
                    f"{name} is not specified in the assign_group function!"
                )
        self.color_map = colors.copy()
        return self

    def mesh(self):
        """Mesh the section.

        Returns
        ----------
        None
        """
        geoms = []
        mesh_sizes = []
        for name, geom in self.group_map.items():
            geoms.append(geom)
            mesh_sizes.append(self.mesh_size_map[name] / 10)
        geom_obj = CompoundGeometry(geoms)
        mesh_obj = geom_obj.create_mesh(mesh_sizes=mesh_sizes)
        self.section = _to_section(geom_obj, time_info=False)
        self.mesh_obj = mesh_obj.mesh
        self._get_mesh_data()

    def _get_mesh_data(self):
        # * mesh data
        vertices = self.mesh_obj["vertices"]
        self.points = vertices
        triangles = self.mesh_obj["triangles"][:, :3]
        triangle_attributes = self.mesh_obj["triangle_attributes"]
        attributes = np.unique(triangle_attributes)
        for name, attri in zip(self.group_map.keys(), attributes):
            idx = triangle_attributes == attri
            self.cells_map[name] = triangles[idx[:, 0]]
        # * fiber data
        for name, faces in self.cells_map.items():
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
            self.areas_map[name] = np.array(areas)
            self.centers_map[name] = np.array(centers)

    def add_rebars(self, rebars_obj):
        """Add rebars.

        Parameters
        ----------
        rebars_obj : mesh obj
            The instance of Rebars class.

        Returns
        ----------
        None
        """
        self.rebar_data = rebars_obj.rebar_data

    def get_fiber_data(self):
        """Return fiber data.

        Returns
        -------
        Tuple(dict, dict)
            fiber center dict, fiber area dict
        """
        return self.centers_map, self.areas_map

    def _run_sec_props(self, Eref, section):
        if Eref == 1:
            area = section.get_area()
        else:
            area = section.get_ea() / Eref
        # Second moments of area centroidal axis (ixx_c, iyy_c, ixy_c)
        ixx_c, iyy_c, ixy_c = section.get_ic()
        cx, cy = section.get_c()  # Elastic centroid (cx, cy)
        phi = section.get_phi()  # Principal bending axis angle
        j = section.get_j()  # St. Venant torsion constant
        # Shear area for loading about the centroidal axis (A_sx, A_sy)
        area_sx, area_sy = section.get_As()
        # Effective Material Properties
        E_eff = section.get_e_eff()
        G_eff = section.get_g_eff()
        Nu_eff = section.get_nu_eff()
        if self.rebar_data:
            all_rebar_area = 0
            for data in self.rebar_data:
                rebar_xy = data["rebar_xy"]
                dia = data["dia"]
                rebar_coords = []
                rebar_areas = []
                for xy in rebar_xy:
                    rebar_coords.append(xy)
                    rebar_areas.append(np.pi / 4 * dia ** 2)
                all_rebar_area += np.sum(rebar_areas)
            rho_rebar = all_rebar_area / area
        else:
            rho_rebar = 0
        # lump
        sec_props = dict(
            A=area,
            Asy=area_sx / Eref,
            Asz=area_sy / Eref,
            centroid=(cx, cy),
            Iy=ixx_c / Eref,
            Iz=iyy_c / Eref,
            Iyz=ixy_c / Eref,
            J=j / Eref,
            phi=phi,
            rho_rebar=rho_rebar,
            E_eff=E_eff,
            G_eff=G_eff,
            Nu_eff=Nu_eff
        )
        self.sec_props = sec_props

    def get_sec_props(self, Eref: float = 1.0,
                      display_results: bool = False,
                      plot_centroids: bool = False):
        """
        Solving Section Geometry Properties by Finite Element Method, by `sectionproperties` pacakge.

        Parameters
        -----------
        Eref: float, default=1.0
            Reference modulus of elasticity, it is important to analyze the composite section.
            See `sectionproperties doc <https://sectionproperties.readthedocs.io/en/latest/rst/post.html>`_
        display_results : bool, default=True
            whether to display the results.
        plot_centroids : bool, default=False
            whether to plot centroids

        Returns
        -----------
        sec_props: dict
            section props dict, including:

            * Cross-sectional area (A)
            * Shear area (Asy, Asz)
            * Elastic centroid (centroid)
            * Second moments of area about the centroidal axis (Iy, Iz, Iyz)
            * Torsion constant (J)
            * Principal axis angle (phi)
            * ratio of reinforcement (rho_rebar)
            * Effective elastic modulus: E_eff;
            * Effective shear modulus: G_eff;
            * Effective Poisson’s ratio: Nu_eff.

            If materials are specified for the cross-section, the area,
            second moments of area and torsion constant are elastic modulus weighted.
        """

        section = self.section
        section.calculate_geometric_properties()
        section.calculate_warping_properties()
        # area, ixx_c, iyy_c, ixy_c, j, phi = section.calculate_frame_properties(
        #    solver_type='direct')
        self._run_sec_props(Eref, section)
        if display_results:
            # section.display_results()
            syms = ["A", "Asy", "Asz", "centroid", "Iy", "Iz", "Iyz",
                    "J", "phi", "rho_rebar", "E_eff", "G_eff", "Nu_eff"]
            defs = ["Cross-sectional area", "Shear area y-axis", "Shear area z-axis", "Elastic centroid",
                    "Moment of inertia y-axis", "Moment of inertia z-axis", "Product of inertia",
                    "Torsion constant", "Principal axis angle", "Ratio of reinforcement", "Effective elastic modulus",
                    "Effective shear modulus", "Effective Poisson’s ratio"]
            table = Table(title="Section Properties")
            table.add_column("Symbol", style="cyan", no_wrap=True)
            table.add_column("Value", style="magenta")
            table.add_column("Definition", style="green")
            for sym_, def_ in zip(syms, defs):
                if sym_ != "centroid":
                    table.add_row(sym_, f"{self.sec_props[sym_]:.3f}", def_)
                else:
                    table.add_row(sym_,
                                  f"({self.sec_props[sym_][0]:.3f}, {self.sec_props[sym_][1]:.3f})",
                                  def_)
            console = Console()
            console.print(table)
        if plot_centroids:
            section.plot_centroids()
        return self.sec_props

    def centring(self):
        """
        Move the section centroid to (0, 0).

        Returns
        ---------
         None
        """
        centers_map, areas_map = self.get_fiber_data()
        centers = []
        areas = []
        for name in self.cells_map.keys():
            centers.append(centers_map[name])
            areas.append(areas_map[name])
        centers = np.vstack(centers)
        areas = np.hstack(areas)
        center = areas @ centers / np.sum(areas)
        self.center = center
        self.points -= center
        names = self.centers_map.keys()
        for name in names:
            self.centers_map[name] -= center
        # move rebar
        for i, data in enumerate(self.rebar_data):
            self.rebar_data[i]["rebar_xy"] -= center
        self.is_centring = True

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

        x_rot, y_rot = sec_rotation(
            self.points[:, 0], self.points[:, 1], theta)
        self.points[:, 0], self.points[:, 1] = x_rot, y_rot

        names = self.centers_map.keys()
        for name in names:
            x_rot, y_rot = sec_rotation(
                self.centers_map[name][:, 0],
                self.centers_map[name][:, 1], theta
            )
            self.centers_map[name][:,
                                   0], self.centers_map[name][:, 1] = x_rot, y_rot
        # rebar
        for i, data in enumerate(self.rebar_data):
            rebar_xy = self.rebar_data[i]["rebar_xy"]
            x_rot, y_rot = sec_rotation(rebar_xy[:, 0], rebar_xy[:, 1], theta)
            (
                self.rebar_data[i]["rebar_xy"][:, 0],
                self.rebar_data[i]["rebar_xy"][:, 1],
            ) = (x_rot, y_rot)

    def opspy_cmds(self, secTag: int, GJ: float):
        """Generate openseespy fiber section command.

        Parameters
        ------------
        secTag : int
            The section tag assigned in OpenSees.
        GJ : float
            Torsion stiffness.

        Returns
        ----------
        None
        """
        ops.section("Fiber", secTag, "-GJ", GJ)

        names = self.centers_map.keys()
        for name in names:
            centers = self.centers_map[name]
            areas = self.areas_map[name]
            matTag = self.mat_ops_map[name]
            for center, area in zip(centers, areas):
                ops.fiber(center[0], center[1], area, matTag)
        # rebars
        for data in self.rebar_data:
            rebar_xy = data["rebar_xy"]
            dia = data["dia"]
            matTag = data["matTag"]
            for xy in rebar_xy:
                area = np.pi / 4 * dia ** 2
                ops.fiber(xy[0], xy[1], area, matTag)

    def to_file(self, output_path: str, secTag: int, GJ: float):
        """Output the opensees fiber code to file.

        Parameters
        -------------
        output_path : str
            The filepath to save, e.g., r"my_dir/my_section.py"
        secTag : int
            The section tag assigned in OpenSees.
        GJ : float
            Torsion stiffness.

        Returns
        ---------
        None

        Notes
        -----
        Notes that output_path must be endswith ``.py`` or ``.tcl``,
        function will create the file by a right style.
        """
        names = self.centers_map.keys()
        if output_path.endswith(".tcl"):
            self._to_tcl(output_path, names, secTag, GJ)
        elif output_path.endswith(".py"):
            self._to_py(output_path, names, secTag, GJ)
        else:
            raise ValueError("output_path must endwith .tcl or .py!")

    def _to_tcl(self, output_path, names, sec_tag, gj):
        with open(output_path, "w+") as output:
            output.write("# This document was created from SecMesh\n")
            output.write("# Author: Yexiang Yan  yexiang_yan@outlook.com\n\n")
            output.write(f"set secTag {sec_tag}\n")
            temp = "{"
            output.write(
                f"section fiberSec $secTag -GJ {gj}{temp};    # Define the fiber section\n"
            )
            for name in names:
                centers = self.centers_map[name]
                areas = self.areas_map[name]
                mat_tag = self.mat_ops_map[name]
                for center, area in zip(centers, areas):
                    output.write(
                        f"    fiber  {center[0]:.3E}  {center[1]:.3E}  {area:.3E}  {mat_tag}\n"
                    )
            # rebar
            for data in self.rebar_data:
                output.write("    # Define Rebar\n")
                rebar_xy = data["rebar_xy"]
                dia = data["dia"]
                mat_tag = data["matTag"]
                for xy in rebar_xy:
                    area = np.pi / 4 * dia ** 2
                    output.write(
                        f"    fiber {xy[0]:.3E} {xy[1]:.3E} {area:.3E} {mat_tag}\n"
                    )
            output.write("};    # end of fibersection definition")

    def _to_py(self, output_path, names, sec_tag, gj):
        with open(output_path, "w+") as output:
            output.write("# This document was created from SecMesh\n")
            output.write("# Author: Yexiang Yan  yexiang_yan@outlook.com\n\n")
            output.write("import openseespy.opensees as ops\n\n\n")
            output.write(
                f"ops.section('Fiber', {sec_tag}, '-GJ', {gj})  # Define the fiber section\n"
            )
            for name in names:
                centers = self.centers_map[name]
                areas = self.areas_map[name]
                mat_tag = self.mat_ops_map[name]
                for center, area in zip(centers, areas):
                    output.write(
                        f"ops.fiber({center[0]:.3E}, {center[1]:.3E}, {area:.3E}, {mat_tag})\n"
                    )
            # rebar
            for data in self.rebar_data:
                output.write("# Define Rebar\n")
                rebar_xy = data["rebar_xy"]
                dia = data["dia"]
                mat_tag = data["matTag"]
                for xy in rebar_xy:
                    area = np.pi / 4 * dia ** 2
                    output.write(
                        f"ops.fiber({xy[0]:.3E}, {xy[1]:.3E}, {area:.3E}, {mat_tag})\n"
                    )

    def view(self, fill: bool = True, engine: str = "plotly",
             save_html: str = "SecMesh.html",
             on_notebook: bool = False):
        """Display the section mesh.

        Parameters
        -----------
        fill : bool, default=True
             Whether to fill the trangles.
        engine: str, default='plotly'
            Plot engine, optional "plotly" or "matplotlib".
        save_html: str, default="SecMesh.html"
            If set, the figure will save as a html file, only useful for engine="plotly".
            If False or None, this parameter will be ignored.
        on_notebook: bool, default=False
            If True, the figure will display in a notebook.

        Returns
        --------
        None
        """

        # self.section.display_mesh_info()
        # self.section.plot_mesh()
        if not self.color_map:
            for i, name in enumerate(self.group_map.keys()):
                self.color_map[name] = self.colors_default[i]
        vertices = self.points
        x = vertices[:, 0]
        y = vertices[:, 1]
        aspect_ratio = (np.max(y) - np.min(y)) / (np.max(x) - np.min(x))
        if engine.lower().startswith("m"):
            self._plot_mpl(fill, aspect_ratio)
        elif engine.lower().startswith("p"):
            self._plot_plotly(fill, aspect_ratio, save_html, on_notebook)
        else:
            raise ValueError(
                f"not supported engine {engine}! optional, 'plotly' or 'matplotlib'!")

    def _plot_mpl(self, fill, aspect_ratio):
        # matplotlib plot
        fig, ax = plt.subplots(figsize=(8, 8 * aspect_ratio))
        # ax.set_facecolor("#efefef")
        # view the mesh
        vertices = self.points  # the coords of each triangle vertex
        for name, faces in self.cells_map.items():
            # faces = faces.astype(np.int64)
            if not fill:
                x = vertices[:, 0]
                y = vertices[:, 1]
                ax.triplot(
                    x, y, triangles=faces, color=self.color_map[name], lw=1, zorder=-10
                )
                ax.plot(
                    [], [], "^", label=name, mec=self.color_map[name], mfc="white"
                )  # for legend illustration only
            else:
                x = vertices[:, 0]
                y = vertices[:, 1]
                ax.triplot(x, y, triangles=faces, lw=0.25, color="k")
                patches = [
                    plt.Polygon(vertices[face_link, :2], True) for face_link in faces
                ]
                coll = PatchCollection(
                    patches,
                    facecolors=self.color_map[name],
                    edgecolors="k",
                    linewidths=0.25,
                    zorder=-10,
                )
                ax.add_collection(coll)
                ax.plot([], [], "^", label=name,
                        color=self.color_map[name])

        for data in self.rebar_data:
            color = data["color"]
            rebar_xy = data["rebar_xy"]
            dia = data["dia"]
            rebar_coords = []
            for xy in rebar_xy:
                rebar_coords.append(xy)
            patches = [
                plt.Circle((xy[0], xy[1]), dia / 2)
                for xy in rebar_coords
            ]
            coll = PatchCollection(patches, facecolors=color)
            ax.add_collection(coll)

        # ax.set_aspect("equal")
        ax.set_title(self.sec_name, fontsize=26, fontfamily="SimSun")
        ax.legend(
            fontsize=18,
            shadow=False,
            markerscale=3,
            loc=10,
            ncol=len(self.group_map),
            bbox_to_anchor=(0.5, -0.2),
            bbox_transform=ax.transAxes,
        )
        ax.tick_params(labelsize=18)
        plt.show()

    def _plot_plotly(self, fill, aspect_ratio, save_html, on_notebook):
        vertices = self.points  # the coords of each triangle vertex
        n_cells = 0
        n_cells_map = dict()
        fig = go.Figure()
        tplot = []
        for name, faces in self.cells_map.items():
            if not self.mat_ops_map:
                label = f"<b>{name}</b>"
            else:
                label = f"<b>{name}</b><br>matTag:{self.mat_ops_map[name]}"
            face_points = []
            areas = []
            centers = []
            for i, cell in enumerate(faces):
                n_cells += 1
                points0 = vertices[cell]
                x1, y1 = points0[0, :2]
                x2, y2 = points0[1, :2]
                x3, y3 = points0[2, :2]
                area_ = 0.5 * np.abs(
                    x2 * y3 + x1 * y2 + x3 * y1 - x3 * y2 - x2 * y1 - x1 * y3
                )
                areas.append(area_)
                centers.append(np.mean(points0, axis=0))
                points = np.vstack(
                    [points0, [points0[0]], [[np.NAN, np.NAN]]])
                face_points.append(points)
            face_points = np.vstack(face_points)
            areas = np.array(areas).reshape((len(areas), 1))
            center_areas = np.hstack([centers, areas])
            center_areas_labels = [f"<b>xo:{d[0]:.2e}</b><br>yo:{d[1]:.2e}<br>area:{d[2]:.2e}"
                                   for d in center_areas]
            n_cells_map[name] = len(center_areas_labels)
            if fill:
                tplot.append(go.Scatter(x=face_points[:, 0], y=face_points[:, 1],
                                        fill="toself", fillcolor=self.color_map[name],
                                        line=dict(
                                            color='black', width=0.75),
                                        connectgaps=False, opacity=0.75,
                                        hoverinfo="skip", ))
            else:
                tplot.append(go.Scatter(x=face_points[:, 0], y=face_points[:, 1],
                                        mode='lines',
                                        line=dict(
                                            color=self.color_map[name], width=1.2),
                                        connectgaps=False,
                                        hoverinfo="skip", ))
            # hover label
            tplot.append(
                go.Scatter(
                    x=center_areas[:, 0],
                    y=center_areas[:, 1],
                    marker=dict(size=0, color=self.color_map[name],
                                symbol='diamond-open'),
                    mode="markers",
                    name=label,
                    customdata=center_areas_labels,
                    hovertemplate='%{customdata}',
                )
            )
        fig.add_traces(tplot)
        # rebars
        shapes = []
        for data in self.rebar_data:
            color = data["color"]
            rebar_xy = data["rebar_xy"]
            r = data["dia"] / 2
            for xo, yo in rebar_xy:
                shapes.append(dict(type="circle",
                                   xref="x", yref="y",
                                   x0=xo - r, y0=yo - r, x1=xo + r, y1=yo + r,
                                   line_color=color,
                                   fillcolor=color,
                                   ))
        # -------------------------------------
        txt = "Num. of Mesh: "
        for k, v in n_cells_map.items():
            txt += f"| {k}--{v} "
        txt += f"| total--{n_cells}"
        fig.update_layout(
            shapes=shapes,
            width=800,
            height=800 * aspect_ratio,
            template="plotly",
            autosize=True,
            showlegend=False,
            scene=dict(aspectratio=dict(
                x=1, y=aspect_ratio), aspectmode="data"),
            title=dict(font=dict(family="courier", color='black', size=20),
                       text=f"<b>{self.sec_name}</b> <br>" + f"{txt}")
        )
        fig.update_xaxes(tickfont_size=18, ticks="outside")
        fig.update_yaxes(tickfont_size=18, ticks="outside")
        if save_html:
            pio.write_html(fig, file=save_html, auto_open=True)
        if on_notebook:
            fig.show()


class Rebars:
    """
    A class to create the rebar point.
    """

    def __init__(self) -> None:
        self.rebar_data = []

    def add_rebar_line(
        self,
        points: list[list[float, float]],
        dia: float,
        gap: float,
        n: int = None,
        closure: bool = False,
        matTag: int = None,
        color: str = "black",
        group_name: str = None,
    ):
        """Add rebar along a line, can be a line or polygon.

        Parameters
        ----------
        points : list[list[float, float]]
            A list of rebar coords, [(x1, y1), (x2, y2),...,(xn, yn)]
        dia : float
            Rebar dia.
        gap : float
            Rebar space.
        n : None
            The number of rebars, if not None,
            update the Arg `gap` according to `n`.
        closure: bool, default=False
            If True, the rebar line is a closed loop.
        matTag : int
            OpenSees mat Tag for rebar previously defined.
        color : str or rgb tuple.
            Color to plot rebar.
        group_name : str
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
            rebar_xy=rebar_xy, color=color, name=group_name, dia=dia, matTag=matTag
        )
        self.rebar_data.append(data)

    def add_rebar_circle(
        self,
        xo: list[float, float],
        radius: float,
        dia: float,
        gap: float,
        n: int = None,
        angle1: float = 0.0,
        angle2: float = 360,
        matTag: int = None,
        color: str = "black",
        group_name: str = None,
    ):
        """Add the rebars along a circle.

        Parameters
        ----------
        xo : list[float, float]
            Center coords, [(xc, yc)].
        radius: float
            radius.
        dia : float
            rebar dia.
        gap : float
            Rebar space
        n : None
            The number of rebars, if not None,
            update the Arg `gap` according to `n`.
        angle1 : float
            The start angle, degree
        angle2 : float
            The end angle, deree
        matTag : int
            OpenSees mat Tag for rebar previously defined.
        color : str or rgb tuple.
            Color to plot rebar.
        group_name : str
            Assign rebar group name.

        Returns
        -------
        None
        """
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
        # if np.abs(angle2 - angle1 - 2 * np.pi) < 1e-6:
        #     rebar_xy = points[:-1]
        # else:
        #     rebar_xy = points
        rebar_xy = points
        data = dict(
            rebar_xy=rebar_xy, color=color, name=group_name, dia=dia, matTag=matTag
        )
        self.rebar_data.append(data)

    def get_rebars_num(self):
        """Returns the number of rebars in each layer.

        Returns
        -------
        list[int]
            The number of rebars in each layer.
        """
        nums = []
        for data in self.rebar_data:
            nums.append(len(data['rebar_xy']))
        return nums


def add_material(
    name="default",
    elastic_modulus=1,
    poissons_ratio=0,
    yield_strength=1,
    density=1,
    color="w",
):
    """Add a meterial.

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
        density
    color : str or rgb tuple, default=='w'
        color for plot this material.

    Returns
    -------
    Material instance
    """
    return Material(
        name=name,
        elastic_modulus=elastic_modulus,
        poissons_ratio=poissons_ratio,
        yield_strength=yield_strength,
        density=density,
        color=color,
    )


def add_polygon(
    outline: list[list[float, float]],
    holes: list[list[list[float, float]]] = None,
    material=None,
):
    """Add polygon plane geom obj.

    Parameters
    ----------
    outline : list[list[float, float]]
        The coords list of polygon points, [(x1, y1), (x2, y2),...,(xn, yn)]
    holes: list[list[list[float, float]]].
        Hole of the section, a list of multiple hole coords, [hole1, hole2,...holeN],
        holeN=[(x1, y1), (x2, y2),...,(xn, yn)].
    material: material obj
        The instance from add_material().

    Returns
    -------
    polygon obj
    """
    if material is None:
        material_ = add_material()
    else:
        material_ = material
    ply = Polygon(outline, holes)
    geometry = Geometry(geom=ply, material=material_)
    return geometry


def add_circle(
    xo: list[float, float],
    radius: float,
    holes=None,
    angle1=0.0,
    angle2=360,
    n_sub=40,
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
        The instance from add_material().

    Returns
    -------
    None
    """
    if material is None:
        material_ = add_material()
    else:
        material_ = material
    angle1 = angle1 / 180 * np.pi
    angle2 = angle2 / 180 * np.pi
    x, y = xo[0], xo[1]
    angles = np.linspace(angle1, angle2, n_sub + 1)
    points = [[x + radius * np.cos(ang), y + radius * np.sin(ang)]
              for ang in angles]
    ply = Polygon(points, holes)
    geometry = Geometry(geom=ply, material=material_)
    return geometry


def _lines_subdivide(x, y, gap):
    """
    The polylines consisting of coordinates x and y are divided by the gap.
    """
    x_new = []
    y_new = []
    for i in range(len(x) - 1):
        x1, y1 = x[i], y[i]
        x2, y2 = x[i + 1], y[i + 1]
        length = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        n = int(np.ceil(length / gap))
        x_new.extend(np.linspace(x1, x2, n, endpoint=True)[:-1].tolist())
        y_new.extend(np.linspace(y1, y2, n, endpoint=True)[:-1].tolist())
    x_new.append(x[-1])
    y_new.append(y[-1])
    new_line = np.column_stack((x_new, y_new))
    return new_line


def offset(points: list[list[float, float]], d: float):
    """Offsets closed polygons

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
    ply = Polygon(points)
    ply_off = ply.buffer(-d, cap_style=3, join_style=2)
    return list(ply_off.exterior.coords)


def sec_rotation(x, y, theta):
    """
    Rotate the section coordinates counterclockwise by theta
    """
    x_new = x * np.cos(theta) + y * np.sin(theta)
    y_new = -x * np.sin(theta) + y * np.cos(theta)
    return x_new, y_new
