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
from ...utils import _get_random_color


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
        self.area = 0.0
        self.Iy = 0.0
        self.Iz = 0.0
        self.J = 0.0

        # * data group
        self.group_map = dict()
        self.mat_ops_map = dict()
        self.mesh_size_map = dict()

        # *rebar data
        self.rebar_data = []

        # * section geo props
        self.sec_props = dict()
        self.frame_sec_props = dict()

        self.color_map = dict()
        self.is_centring = False

    def assign_group(self, group: dict):
        """Assign the group dict for each mesh.

        Parameters
        ------------
        group : dict[str, any]
            A dict of name as key, geometry obj as value.

        Returns
        ----------
        instance
        """
        self.group_map = group
        return self

    def get_group(self,):
        """Return the group dict for each geometry obj.

        Returns
        ----------
        group : dict[str, any]
        """
        return self.group_map

    def assign_mesh_size(self, mesh_size: dict = None):
        """Assign the mesh size dict for each mesh.

        Parameters
        ------------
        mesh_size : dict[str, float], default=None
            A dict of name as key, mesh size as value.
            The mesh sizes describe the maximum mesh element area to be
            used in the finite-element mesh for each Geometry object.
            If default None is used, the mesh size of each Geometry will be
            calculate by its area / 100.

        Returns
        ------------
        instance
        """
        if not self.group_map:
            raise ValueError("The assign_group method should be run first!")
        if mesh_size is None:
            mesh_size = dict()
            for name, geom in self.group_map.items():
                area = geom.calculate_area()
                mesh_size[name] = area / 100
        else:
            for name in mesh_size.keys():
                if name not in self.group_map.keys():
                    raise ValueError(
                        f"{name} is not specified in the assign_group function!"
                    )
        self.mesh_size_map = mesh_size
        return self

    def assign_ops_matTag(self, mat_tag: dict):
        """Assign the mesh size dict for each mesh.

        Parameters
        --------------
        mat_tag : dict[str, int]
            A dict of name as key, OpenSees matTag previous defined as value.

        Returns
        ----------
        instance
        """
        if not self.group_map:
            raise ValueError("The assign_group method should be run first!")
        for name in mat_tag.keys():
            if name not in self.group_map.keys():
                raise ValueError(
                    f"{name} is not specified in the assign_group method!"
                )
        self.mat_ops_map = mat_tag
        return self

    def assign_group_color(self, colors: dict):
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
        self.color_map = colors
        return self

    def mesh(self, plot_mesh: bool = False):
        """Mesh the section.

        Parameters
        ----------
        plot_mesh: bool, default=False
            If True, plot the mesh by ``sectionproperties``.

        Returns
        ----------
        None
        """
        geoms = []
        mesh_sizes = []
        if not self.color_map:
            for name in self.group_map.keys():
                self.color_map[name] = _get_random_color()
        # mat_names = [geom.material.name for geom in self.group_map.values()]
        for name, geom in self.group_map.items():
            # if len(mat_names) != len(set(mat_names)):
            if geom.material is None:
                geom.material = add_material(name=name, color=self.color_map[name])
            else:
                geom.material = add_material(
                    name=name,
                    elastic_modulus=geom.material.elastic_modulus,
                    poissons_ratio=geom.material.poissons_ratio,
                    yield_strength=geom.material.yield_strength,
                    density=geom.material.density,
                    color=self.color_map[name],
                )
            geoms.append(geom)
            mesh_sizes.append(self.mesh_size_map[name])
        if len(geoms) > 1:
            geom_obj = CompoundGeometry(geoms)
            mesh_obj = geom_obj.create_mesh(mesh_sizes=mesh_sizes)
        else:
            geom_obj = geoms[0]
            mesh_obj = geom_obj.create_mesh(mesh_sizes=mesh_sizes[0])
        self.section = Section(geom_obj, time_info=False)
        self.mesh_obj = mesh_obj.mesh
        self._get_mesh_data()
        if plot_mesh:
            self.section.plot_mesh(materials=True, alpha=0.90)

    def _get_mesh_data(self):
        # * mesh data
        vertices = self.mesh_obj["vertices"]
        self.points = np.array(vertices)
        triangles = self.mesh_obj["triangles"][:, :3]
        triangle_attributes = self.mesh_obj["triangle_attributes"]
        attributes = np.unique(triangle_attributes)
        for name, attri in zip(self.group_map.keys(), attributes):
            idx = triangle_attributes == attri
            self.cells_map[name] = triangles[idx[:, 0]]
        # * fiber data
        iys, izs = [], []
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
                iys.append(area_ * xyo[1] ** 2)
                izs.append(area_ * xyo[0] ** 2)
            self.areas_map[name] = np.array(areas)
            self.centers_map[name] = np.array(centers)
        centers = []
        areas = []
        for name in self.cells_map.keys():
            centers.append(self.centers_map[name])
            areas.append(self.areas_map[name])
        centers = np.vstack(centers)
        areas = np.hstack(areas)
        self.area = np.sum(areas)
        self.center = areas @ centers / self.area
        self.Iy = np.sum(iys)
        self.Iz = np.sum(izs)

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

    def get_area(self):
        """Return section area.

        Returns
        -------
        Float
        """
        area = 0
        if self.frame_sec_props:
            area = self.frame_sec_props["A"]
        elif self.sec_props:
            area = self.sec_props["A"]
        else:
            area = self.area
        return area

    def get_iy(self):
        """Return Moment of inertia of the section around the y-axis.

        Returns
        -------
        Float
        """
        iy = 0
        if self.frame_sec_props:
            iy = self.frame_sec_props["Iy"]
        elif self.sec_props:
            iy = self.sec_props["Iy"]
        else:
            iy = self.Iy
        return iy

    def get_iz(self):
        """Return Moment of inertia of the section around the z-axis.

        Returns
        -------
        Float
        """
        iz = 0
        if self.frame_sec_props:
            iz = self.frame_sec_props["Iz"]
        elif self.sec_props:
            iz = self.sec_props["Iz"]
        else:
            iz = self.Iz
        return iz

    def get_j(self):
        """Return section torsion constant.

        Returns
        -------
        Float
        """
        j = 10000
        if self.frame_sec_props:
            j = self.frame_sec_props["J"]
        elif self.sec_props:
            j = self.sec_props["J"]
        else:
            self.get_frame_props()
            j = self.frame_sec_props["J"]
        return j

    def _run_sec_props(self, Eref, Gref):
        self.section.calculate_geometric_properties()
        self.section.calculate_warping_properties()
        section = self.section
        # Second moments of area centroidal axis
        ixx_c, iyy_c, ixy_c = section.get_ic()
        # Elastic centroid
        cx, cy = (0.0, 0.0) if self.is_centring else section.get_c()
        # Elastic section moduli about the centroidal axis with respect to the top and bottom fibres
        zxx_plus, zxx_minus, zyy_plus, zyy_minus = section.get_z()
        # Principal bending axis angle
        phi = section.get_phi()
        # Shear area for loading about the centroidal axis
        area_sx, area_sy = section.get_As()
        # mass
        mass = section.get_mass()
        # Effective Material Properties
        E_eff = section.get_e_eff()
        G_eff = section.get_g_eff()
        # Nu_eff = section.get_nu_eff()
        if Eref == 1.0:  # not composite section
            area = section.get_area()
            # St. Venant torsion constant
            j = section.get_j()
        else:
            area = section.get_ea() / Eref
            # St. Venant torsion constant
            j_ = section.get_j()
            j = G_eff / E_eff * j_ / Gref
        self.area = area
        self.Iy = ixx_c / Eref
        self.Iz = iyy_c / Eref
        self.J = j
        if self.rebar_data:
            all_rebar_area = 0
            for data in self.rebar_data:
                rebar_xy = data["rebar_xy"]
                dia = data["dia"]
                rebar_coords = []
                rebar_areas = []
                for xy in rebar_xy:
                    rebar_coords.append(xy)
                    rebar_areas.append(np.pi / 4 * dia**2)
                all_rebar_area += np.sum(rebar_areas)
            rho_rebar = all_rebar_area / area
        else:
            rho_rebar = 0
        sec_props = dict(
            A=area,
            Asy=area_sx / Eref,
            Asz=area_sy / Eref,
            centroid=(cx, cy),
            Iy=ixx_c / Eref,
            Iz=iyy_c / Eref,
            Iyz=ixy_c / Eref,
            Wyt=zxx_plus / Eref,
            Wyb=zxx_minus / Eref,
            Wzt=zyy_plus / Eref,
            Wzb=zyy_minus / Eref,
            J=j,
            phi=phi,
            mass=mass,
            rho_rebar=rho_rebar,
        )
        self.sec_props = sec_props

    def get_sec_props(
        self,
        Eref: float = 1.0,
        Gref: float = None,
        display_results: bool = False,
        fmt: str = '8.3E',
        plot_centroids: bool = False,
    ):
        """
        Solving Section Geometry Properties by Finite Element Method, by ``sectionproperties`` pacakge.
        See `sectionproperties doc <https://sectionproperties.readthedocs.io/en/latest/rst/post.html
        #getting-specific-section-properties>`_

        This command may be slower. If you don't need features such as shear area, you can use
        method :py:meth:`~opstool.preprocessing.SecMesh.get_frame_props`.

        Parameters
        -----------
        Eref: float, default=1.0
            Reference modulus of elasticity, it is important to analyze the composite section.
            If it is not a composite section, please ignore this parameter and the following `Gref`.
            See `sectionproperties doc <https://sectionproperties.readthedocs.io/en/latest/rst/post.html
            #how-material-properties-affect-results>`_
        Gref: float, default=None
            Reference shear modulus, useful for torsional constant calculations of composite section.
            If None, Gref = 0.5 * Eref.
        display_results : bool, default=True
            whether to display the results.
        fmt : str, optional
            Number formatting string when display_results=True.
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
            * Elastic section moduli about the centroidal axis with respect to the
              top and bottom fibres (Wyt, Wyb, Wzt, Wzb)
            * Torsion constant (J)
            * Principal axis angle (phi)
            * Section mass (mass), only true if material density is defined,
              otherwise geometric area (mass density is 1)
            * ratio of reinforcement (rho_rebar)

        .. note::

            If it is not a composite section, please ignore the `Eref` and `Gref` parameters;
            Otherwise, please use the `Eref` and `Gref` parameters, all section properties will
            be converted according to the reference material, and the mechanical properties of
            the reference material are then used in the practical analysis.

            Note that according to the OpenSees convention,
            the x-axis refers to the normal direction of the section,
            the y-axis refers to the abscissa,
            and the z-axis refers to the ordinate direction.
        """
        if Gref is None:
            Gref = 0.5 * Eref
        self._run_sec_props(Eref, Gref)
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
            console = Console()
            console.print(table)
        if plot_centroids:
            self.section.plot_centroids()
        return self.sec_props

    def get_frame_props(
        self,
        Eref: float = 1.0,
        Gref: float = None,
        display_results: bool = False,
        fmt: str = '8.3E'
    ):
        """Calculates and returns the properties required for a frame analysis.
        See `sectionproperties doc <https://sectionproperties.readthedocs.io/en/latest/rst/api.html
        #sectionproperties.analysis.section.Section.calculate_frame_properties>`_

        This method is fast, but cannot calculate the shear area compared to the
        method :py:meth:`~opstool.preprocessing.SecMesh.get_sec_props`.

        Parameters
        ----------
        Eref: float, default=1.0
            Reference modulus of elasticity, it is important to analyze the composite section.
            If it is not a composite section, please ignore this parameter and the following `Gref`.
            See `sectionproperties doc <https://sectionproperties.readthedocs.io/en/latest/rst/post.html#
            how-material-properties-affect-results>`_
        Gref: float, default=None
            Reference shear modulus, useful for torsional constant calculations of composite section.
            If None, Gref = 0.5 * Eref.
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
              the top and bottom fibres (Wyt, Wyb, Wzt, Wzb)
            * Torsion constant (J)
            * Principal axis angle (phi)
            * Section mass (mass), only true if material density is defined,
              otherwise geometric area (mass density is 1)
            * ratio of reinforcement (rho_rebar)

        .. note::

            If it is not a composite section, please ignore the `Eref` and `Gref` parameters;
            Otherwise, please use the `Eref` and `Gref` parameters, all section properties will
            be converted according to the reference material, and the mechanical properties of
            the reference material are then used in the practical analysis.

            Note that according to the OpenSees convention,
            the x-axis refers to the normal direction of the section,
            the y-axis refers to the abscissa,
            and the z-axis refers to the ordinate direction.
        """
        if Gref is None:
            Gref = 0.5 * Eref
        # self.section.calculate_geometric_properties()
        (ea, ixx_c, iyy_c, ixy_c, j, phi) = self.section.calculate_frame_properties(
            solver_type="direct"
        )
        cx, cy = (0.0, 0.0) if self.is_centring else self.section.get_c()
        mass, ga = 0, 0
        for el in self.section.elements:
            (area_, _, _, _, _, _, _, g, rho) = el.geometric_properties()
            mass += area_ * rho
            ga += area_ * g
        self.section.section_props.calculate_centroidal_properties(self.section.mesh)
        zxx_plus, zxx_minus, zyy_plus, zyy_minus = self.section.get_z()
        E_eff = self.section.section_props.ea / self.section.section_props.area
        G_eff = ga / self.section.section_props.area
        area = ea / Eref
        if Eref != 1.0:  # composite section
            # St. Venant torsion constant
            j = G_eff / E_eff * j / Gref
        self.area = area
        self.Iy = ixx_c / Eref
        self.Iz = iyy_c / Eref
        self.J = j
        if self.rebar_data:
            all_rebar_area = 0
            for data in self.rebar_data:
                rebar_xy = data["rebar_xy"]
                dia = data["dia"]
                rebar_coords = []
                rebar_areas = []
                for xy in rebar_xy:
                    rebar_coords.append(xy)
                    rebar_areas.append(np.pi / 4 * dia**2)
                all_rebar_area += np.sum(rebar_areas)
            rho_rebar = all_rebar_area / area
        else:
            rho_rebar = 0
        sec_props = dict(
            A=area,
            centroid=(cx, cy),
            Iy=ixx_c / Eref,
            Iz=iyy_c / Eref,
            Iyz=ixy_c / Eref,
            Wyt=zxx_plus / Eref,
            Wyb=zxx_minus / Eref,
            Wzt=zyy_plus / Eref,
            Wzb=zyy_minus / Eref,
            J=j,
            phi=phi,
            mass=mass,
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
                "mass",
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
                "Section mass",
                "Ratio of reinforcement",
            ]
            table = Table(title="Frame Section Properties")
            table.add_column("Symbol", style="cyan", no_wrap=True)
            table.add_column("Value", style="magenta")
            table.add_column("Definition", style="green")
            for sym_, def_ in zip(syms, defs):
                if sym_ != "centroid":
                    table.add_row(
                        sym_,
                        "{:>{fmt}}".format(sec_props[sym_], fmt=fmt),
                        def_
                    )
                else:
                    table.add_row(
                        sym_,
                        f"({sec_props[sym_][0]:>{fmt}}, {sec_props[sym_][1]:>{fmt}})",
                        def_,
                    )
            console = Console()
            console.print(table)
        self.frame_sec_props = sec_props
        return sec_props

    def display_all_results(self, fmt: str = '8.6e'):
        """Prints all results that have been calculated by ``sectionproperties`` to the terminal.

        Parameters
        ----------
        fmt : str, optional
            Number formatting string.
        """
        if not self.sec_props:
            self._run_sec_props()
        self.section.display_results(fmt=fmt)

    def get_stress(
        self,
        N: float = 0,
        Vy: float = 0,
        Vz: float = 0,
        Myy: float = 0,
        Mzz: float = 0,
        Mxx: float = 0,
        plot_stress: str = None,
        cmap: str = "coolwarm",
        normalize: bool = True,
    ):
        """Calculates the cross-section stress resulting from design actions and returns
        a list of dictionaries containing the cross-section stresses for each region by
        method :py:meth:`~opstool.preprocessing.SecMesh.assign_group`.

        .. note::

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

            **Combined Stress Plots**:

            * "xx"--combined normal stress resulting from all actions;
            * "xy"--y-component of the shear stress resulting from all actions;
            * "xz"-- z-component of the shear stress resulting from all actions;
            * "xyz"--resultant shear stress resulting from all actions;
            * "p1"--major principal stress resulting from all actions;
            * "p3"-- Minor principal stress resulting from all actions;
            * "vm"--von Mises stress resulting from all actions;

            **Primary Stress Plots**:

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
            N=N, Vx=Vy, Vy=Vz, Mxx=Myy, Myy=Mzz, Mzz=Mxx
        )
        name_map = dict(
            xx="sig_zz",
            xy="sig_zx",
            xz="sig_zy",
            xyz="sig_zxy",
            p1="sig_1",
            p3="sig_3",
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

        if plot_stress:
            # ------------Primary Stress Plots
            if plot_stress == "n_xx":
                stress_post.plot_stress_n_zz(
                    title=r"Stress Contour Plot - $\sigma_{xx,N}$",
                    cmap=cmap,
                    normalize=normalize,
                )
            elif plot_stress == "myy_xx":
                stress_post.plot_stress_mxx_zz(
                    title=r"Stress Contour Plot - $\sigma_{xx,Myy}$",
                    cmap=cmap,
                    normalize=normalize,
                )
            elif plot_stress == "mzz_xx":
                stress_post.plot_stress_myy_zz(
                    title=r"Stress Contour Plot - $\sigma_{xx,Mzz}$",
                    cmap=cmap,
                    normalize=normalize,
                )
            elif plot_stress == "m_xx":
                stress_post.plot_stress_m_zz(
                    title=r"Stress Contour Plot - $\sigma_{xx,\Sigma M}$",
                    cmap=cmap,
                    normalize=normalize,
                )
            elif plot_stress == "mxx_xy":
                stress_post.plot_stress_mzz_zx(
                    title="Stress Contour Plot - $\\tau_{xy,Mxx}$",
                    cmap=cmap,
                    normalize=normalize,
                )
            elif plot_stress == "mxx_xz":
                stress_post.plot_stress_mzz_zy(
                    title="Stress Contour Plot - $\\tau_{xz,Mxx}$",
                    cmap=cmap,
                    normalize=normalize,
                )
            elif plot_stress == "mxx_xyz":
                stress_post.plot_stress_mzz_zxy(
                    title="Stress Contour Plot - $\\tau_{xyz,Mxx}$",
                    cmap=cmap,
                    normalize=normalize,
                )
            elif plot_stress == "vy_xy":
                stress_post.plot_stress_vx_zx(
                    title="Stress Contour Plot - $\\tau_{xy,Vy}$",
                    cmap=cmap,
                    normalize=normalize,
                )
            elif plot_stress == "vy_xz":
                stress_post.plot_stress_vx_zy(
                    title="Stress Contour Plot - $\\tau_{xz,Vy}$",
                    cmap=cmap,
                    normalize=normalize,
                )
            elif plot_stress == "vy_xyz":
                stress_post.plot_stress_vx_zxy(
                    title=r"Stress Contour Plot - $\tau_{xyz,Vy}",
                    cmap=cmap,
                    normalize=normalize,
                )
            elif plot_stress == "vz_xy":
                stress_post.plot_stress_vy_zx(
                    title="Stress Contour Plot - $\\tau_{xy,Vz}$",
                    cmap=cmap,
                    normalize=normalize,
                )
            elif plot_stress == "vz_xz":
                stress_post.plot_stress_vy_zy(
                    title="Stress Contour Plot - $\\tau_{xz,Vz}$",
                    cmap=cmap,
                    normalize=normalize,
                )
            elif plot_stress == "vz_xyz":
                stress_post.plot_stress_vy_zxy(
                    title="Stress Contour Plot - $\\tau_{xyz,Vz}$",
                    cmap=cmap,
                    normalize=normalize,
                )
            elif plot_stress == "v_xy":
                stress_post.plot_stress_v_zx(
                    title="Stress Contour Plot - $\\tau_{xy,V}$",
                    cmap=cmap,
                    normalize=normalize,
                )
            elif plot_stress == "v_xz":
                stress_post.plot_stress_v_zy(
                    title="Stress Contour Plot - $\\tau_{xz,V}$",
                    cmap=cmap,
                    normalize=normalize,
                )
            elif plot_stress == "v_xyz":
                stress_post.plot_stress_v_zxy(
                    title="Stress Contour Plot - $\\tau_{xyz,V}$",
                    cmap=cmap,
                    normalize=normalize,
                )
            # ------------Combined Stress Plots
            elif plot_stress == "xx":
                stress_post.plot_stress_zz(
                    title=r"Stress Contour Plot - $\sigma_{xx}$",
                    cmap=cmap,
                    normalize=normalize,
                )
            elif plot_stress == "xy":
                stress_post.plot_stress_zx(
                    title="Stress Contour Plot - $\\tau_{xy}$",
                    cmap=cmap,
                    normalize=normalize,
                )
            elif plot_stress == "xz":
                stress_post.plot_stress_zy(
                    title="Stress Contour Plot - $\\tau_{xz}$",
                    cmap=cmap,
                    normalize=normalize,
                )
            elif plot_stress == "xyz":
                stress_post.plot_stress_zxy(
                    title="Stress Contour Plot - $\\tau_{xyz}$",
                    cmap=cmap,
                    normalize=normalize,
                )
            elif plot_stress == "p1":
                stress_post.plot_stress_1(
                    title=r"Stress Contour Plot - $\sigma_{1}$",
                    cmap=cmap,
                    normalize=normalize,
                )
            elif plot_stress == "p3":
                stress_post.plot_stress_3(
                    title=r"Stress Contour Plot - $\sigma_{3}$",
                    cmap=cmap,
                    normalize=normalize,
                )
            elif plot_stress == "vm":
                stress_post.plot_stress_vm(
                    title=r"Stress Contour Plot - $\sigma_{vM}$",
                    cmap=cmap,
                    normalize=normalize,
                )
            elif plot_stress == "all":
                for name in name_map.keys():
                    _ = self.get_stress(
                        N=N,
                        Vy=Vy,
                        Vz=Vz,
                        Myy=Myy,
                        Mzz=Mzz,
                        Mxx=Mxx,
                        plot_stress=name,
                        cmap=cmap,
                        normalize=normalize,
                    )
            else:
                raise ValueError("not supported plot_stress type!")

        stresses_temp = stress_post.get_stress()
        stresses = []
        for stress in stresses_temp:
            temp = dict()
            temp["Region"] = stress["Material"]
            for name, value in name_map.items():
                temp["sig_" + name] = stress[value]
            stresses.append(temp)
        return stresses

    def centring(self):
        """
        Move the section centroid to (0, 0).

        Returns
        ---------
         None
        """
        self.points -= self.center
        names = self.centers_map.keys()
        for name in names:
            self.centers_map[name] -= self.center
        # move rebar
        for i, data in enumerate(self.rebar_data):
            self.rebar_data[i]["rebar_xy"] -= self.center
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

        x_rot, y_rot = sec_rotation(self.points[:, 0], self.points[:, 1], theta)
        self.points[:, 0], self.points[:, 1] = x_rot, y_rot

        names = self.centers_map.keys()
        for name in names:
            x_rot, y_rot = sec_rotation(
                self.centers_map[name][:, 0], self.centers_map[name][:, 1], theta
            )
            self.centers_map[name][:, 0], self.centers_map[name][:, 1] = x_rot, y_rot
        # rebar
        for i, data in enumerate(self.rebar_data):
            rebar_xy = self.rebar_data[i]["rebar_xy"]
            x_rot, y_rot = sec_rotation(rebar_xy[:, 0], rebar_xy[:, 1], theta)
            (
                self.rebar_data[i]["rebar_xy"][:, 0],
                self.rebar_data[i]["rebar_xy"][:, 1],
            ) = (x_rot, y_rot)

    def opspy_cmds(self, secTag: int, GJ: float = None, G: float = None):
        """Generate openseespy fiber section command.

        Parameters
        ------------
        secTag : int
            The section tag assigned in OpenSees.
        GJ : float, default = None
            Torsion stiffness.
            Note that at least one of GJ and G needs to be specified,
            and if both, it will be calculated by GJ.
        G : float, default = None
            Shear modulus.The torsion constant is automatically calculated by the program.
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
                area = np.pi / 4 * dia**2
                ops.fiber(xy[0], xy[1], area, matTag)

    def to_file(self, output_path: str, secTag: int, GJ: float = None, G: float = None):
        """Output the opensees fiber code to file.

        Parameters
        -------------
        output_path : str
            The filepath to save, e.g., r"my_dir/my_section.py"
        secTag : int
            The section tag assigned in OpenSees.
        GJ : float, default = None
            Torsion stiffness.
            Note that at least one of GJ and G needs to be specified,
            and if both, it will be calculated by GJ.
        G : float, default = None
            Shear modulus.The torsion constant is automatically calculated by the program.
            Note that at least one of GJ and G needs to be specified,
            and if both, it will be calculated by GJ.

        Returns
        ---------
        None

        Notes
        -----
        Notes that output_path must be endswith ``.py`` or ``.tcl``,
        function will create the file by a right style.
        """
        if GJ is None:
            if G is None:
                raise ValueError("GJ and G need to assign at least one!")
            else:
                GJ = G * self.get_j()

        names = self.centers_map.keys()
        if output_path.endswith(".tcl"):
            self._to_tcl(output_path, names, secTag, GJ)
        elif output_path.endswith(".py"):
            self._to_py(output_path, names, secTag, GJ)
        else:
            raise ValueError("output_path must endwith .tcl or .py!")

    def _to_tcl(self, output_path, names, sec_tag, gj):
        with open(output_path, "w+") as output:
            output.write("# This document was created from opstool.SecMesh\n")
            output.write("# Author: Yexiang Yan  yexiang_yan@outlook.com\n\n")
            output.write(f"set secTag {sec_tag}\n")
            temp = "{"
            output.write(
                f"section fiberSec $secTag -GJ {gj} {temp};    # Define the fiber section\n"
            )
            for name in names:
                centers = self.centers_map[name]
                areas = self.areas_map[name]
                mat_tag = self.mat_ops_map[name]
                for center, area in zip(centers, areas):
                    output.write(
                        f"    fiber  {center[0]:.8E}  {center[1]:.8E}  {area:.8E}  {mat_tag}\n"
                    )
            # rebar
            for data in self.rebar_data:
                output.write("    # Define Rebar\n")
                rebar_xy = data["rebar_xy"]
                dia = data["dia"]
                mat_tag = data["matTag"]
                for xy in rebar_xy:
                    area = np.pi / 4 * dia**2
                    output.write(
                        f"    fiber {xy[0]:.8E} {xy[1]:.8E} {area:.8E} {mat_tag}\n"
                    )
            output.write("};    # end of fibersection definition")

    def _to_py(self, output_path, names, sec_tag, gj):
        with open(output_path, "w+") as output:
            output.write("# This document was created from opstool.SecMesh\n")
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
                        f"ops.fiber({center[0]:.8E}, {center[1]:.8E}, {area:.8E}, {mat_tag})\n"
                    )
            # rebar
            for data in self.rebar_data:
                output.write("# Define Rebar\n")
                rebar_xy = data["rebar_xy"]
                dia = data["dia"]
                mat_tag = data["matTag"]
                for xy in rebar_xy:
                    area = np.pi / 4 * dia**2
                    output.write(
                        f"ops.fiber({xy[0]:.8E}, {xy[1]:.8E}, {area:.8E}, {mat_tag})\n"
                    )

    def view(
        self,
        fill: bool = True,
        engine: str = "plotly",
        save_html: str = None,
        on_notebook: bool = False,
        show_hover: bool = False,
    ):
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
        show_hover: bool, default=False
            If True, the figure will show the hover labels.

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
        if engine.lower().startswith("m"):
            self._plot_mpl(fill, aspect_ratio)
        elif engine.lower().startswith("p"):
            self._plot_plotly(fill, aspect_ratio, save_html, show_hover=show_hover)
        else:
            raise ValueError(
                f"not supported engine {engine}! optional, 'plotly' or 'matplotlib'!"
            )

    def _plot_mpl(self, fill, aspect_ratio):
        # matplotlib plot
        if aspect_ratio <= 0.333:
            aspect_ratio = 0.333
        if aspect_ratio >= 3:
            aspect_ratio = 3
        fig, ax = plt.subplots(figsize=(8, 8))
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
                ax.plot([], [], "^", label=name, color=self.color_map[name])

        for data in self.rebar_data:
            color = data["color"]
            rebar_xy = data["rebar_xy"]
            dia = data["dia"]
            rebar_coords = []
            for xy in rebar_xy:
                rebar_coords.append(xy)
            patches = [plt.Circle((xy[0], xy[1]), dia / 2) for xy in rebar_coords]
            coll = PatchCollection(patches, facecolors=color)
            ax.add_collection(coll)

        ax.set_aspect(aspect_ratio)
        ax.set_title(self.sec_name, fontsize=26, fontfamily="SimSun")
        ax.legend(
            fontsize=18,
            shadow=False,
            markerscale=3,
            loc='center left',
            ncol=len(self.group_map),
            bbox_to_anchor=(1.01, 0.5),
            bbox_transform=ax.transAxes,
        )
        ax.set_xlabel("y", fontsize=22)
        ax.set_ylabel("z", fontsize=22)
        ax.tick_params(labelsize=18)
        plt.tight_layout()
        plt.show()

    def _plot_plotly(
        self, fill, aspect_ratio, save_html,
        show_hover: bool = True
    ):
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
                points = np.vstack([points0, [points0[0]], [[np.NAN, np.NAN]]])
                face_points.append(points)
            face_points = np.vstack(face_points)
            areas = np.array(areas).reshape((len(areas), 1))
            center_areas = np.hstack([centers, areas])
            center_areas_labels = [
                f"<b>xo:{d[0]:.2e}</b><br>yo:{d[1]:.2e}<br>area:{d[2]:.2e}"
                for d in center_areas
            ]
            n_cells_map[name] = len(center_areas_labels)
            if fill:
                tplot.append(
                    go.Scatter(
                        x=face_points[:, 0],
                        y=face_points[:, 1],
                        fill="toself",
                        fillcolor=self.color_map[name],
                        line=dict(color="black", width=0.75),
                        connectgaps=False,
                        opacity=0.75,
                        hoverinfo="skip",
                    )
                )
            else:
                tplot.append(
                    go.Scatter(
                        x=face_points[:, 0],
                        y=face_points[:, 1],
                        mode="lines",
                        line=dict(color=self.color_map[name], width=1.2),
                        connectgaps=False,
                        hoverinfo="skip",
                    )
                )
            # hover label
            if show_hover:
                tplot.append(
                    go.Scatter(
                        x=center_areas[:, 0],
                        y=center_areas[:, 1],
                        marker=dict(
                            size=0, color=self.color_map[name], symbol="diamond-open"
                        ),
                        mode="markers",
                        name=label,
                        customdata=center_areas_labels,
                        hovertemplate="%{customdata}",
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
                shapes.append(
                    dict(
                        type="circle",
                        xref="x",
                        yref="y",
                        x0=xo - r,
                        y0=yo - r,
                        x1=xo + r,
                        y1=yo + r,
                        line_color=color,
                        fillcolor=color,
                    )
                )
        # -------------------------------------
        txt = "Num. of Mesh: "
        for k, v in n_cells_map.items():
            txt += f"| {k}--{v} "
        txt += f"| total--{n_cells}"
        if aspect_ratio <= 0.3:
            width, height = 1600, 1600 * 0.3
        elif aspect_ratio > 0.3 and aspect_ratio <= 1.0:
            width, height = 1600, 1600 * aspect_ratio
        elif aspect_ratio > 1.0 and aspect_ratio <= 3.333:
            width, height = 900 / aspect_ratio, 900
        else:
            width, height = 900 / 3.333, 900
        fig.update_layout(
            shapes=shapes,
            width=width,
            height=height,
            template="plotly",
            autosize=True,
            showlegend=False,
            scene=dict(aspectratio=dict(x=1, y=aspect_ratio), aspectmode="data"),
            title=dict(
                font=dict(family="courier", color="black", size=18),
                text=f"<b>{self.sec_name}</b> <br>" + f"{txt}",
            ),
        )
        fig.update_xaxes(tickfont_size=18, ticks="outside")
        fig.update_yaxes(tickfont_size=18, ticks="outside")
        if save_html:
            pio.write_html(fig, file=save_html, auto_open=True)
        else:
            fig.show()


class Rebars:
    """
    A class to create the rebar point.
    """

    def __init__(self) -> None:
        self.rebar_data = []

    def add_rebar_line(
        self,
        points: list,
        dia: float,
        gap: float = 0.1,
        n: int = None,
        closure: bool = False,
        matTag: int = None,
        color: str = "black",
        group_name: str = None,
    ):
        """Add rebar along a line, can be a line or polygon.

        Parameters
        ----------
        points: list[list[float, float]]
            A list of rebar coords, [(x1, y1), (x2, y2),...,(xn, yn)],
            in which each element represents a corner point,
            and every two corner points are divided by the arg `gap`.
        dia: float
            Rebar dia.
        gap: float, default=0.1
            Rebar space.
        n: int, default=None
            The number of rebars, if not None,
            update the Arg `gap` according to `n`.
            This means that if you know the number of rebars,
            you don't need to input `gap` or set `gap` to any number.
        closure: bool, default=False
            If True, the rebar line is a closed loop.
        matTag: int
            OpenSees mat Tag for rebar previously defined.
        color: str or rgb tuple.
            Color to plot rebar.
        group_name: str
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
        xo: list,
        radius: float,
        dia: float,
        gap: float = 0.1,
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
        angle1: float
            The start angle, degree.
        angle2: float
            The end angle, deree.
        matTag: int
            OpenSees material matTag for rebar previously defined.
        color: str or rgb tuple.
            Color to plot rebar.
        group_name: str
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
            nums.append(len(data["rebar_xy"]))
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
        mass density
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
    outline: list,
    holes: list = None,
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


def add_circle(
    xo: list,
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
        material_ = None
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


def offset(points: list, d: float):
    """Offsets closed polygons, same as :py:func:`opstool.preprocessing.poly_offset`

    Parameters
    ----------
    points  : list[list[float, float]]
        A list containing the coordinate points, [(x1, y1),(x2, y2),...,(xn.yn)].
    d : float
        Offsets closed polygons, positive values offset inwards, negative values outwards.

    Returns
    -------
    coords: list[[float, float]]

    Examples
    ----------
    >>> import opstool as opst
    >>> outlines1 = [[0, 0], [0, 1], [1, 1]]
    >>> outlines2 = opst.offset(outlines1, d=0.1)
    >>> outlines3 = [[0, 0], [0, 1], [1, 1], [1, 0]]
    >>> outlines4 = opst.offset(outlines3, d=0.1)
    """
    ply = Polygon(points)
    ply_off = ply.buffer(-d, cap_style=3, join_style=2)
    return list(ply_off.exterior.coords)


def poly_offset(points: list, d: float):
    """Offsets closed polygons, same as :py:func:`opstool.preprocessing.offset`

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
    >>> lines2 = opst.line_offset(lines, d=0.1)
    >>> lines = [[0, 0], [0, 1], [1, 1]]
    >>> lines3 = opst.line_offset(lines, d=0.1)
    >>> lines = [[0, 0], [0, 1], [1, 0]]
    >>> lines4 = opst.line_offset(lines, d=0.1)
    """
    ls = LineString(points)
    ls_off = ls.offset_curve(-d, quad_segs=16, join_style=2, mitre_limit=5.0)
    return list(ls_off.coords)


def sec_rotation(x, y, theta):
    """
    Rotate the section coordinates counterclockwise by theta
    """
    x_new = x * np.cos(theta) + y * np.sin(theta)
    y_new = -x * np.sin(theta) + y * np.cos(theta)
    return x_new, y_new
