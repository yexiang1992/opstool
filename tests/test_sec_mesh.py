import numpy as np
from opstool import (Rebars, SecMesh, add_circle,
                     add_material, add_polygon, offset)

#
# case 1
outlines = [[0, 0], [2, 0], [2, 2], [0, 2], [0, 0]]
obj = add_polygon(outlines)
sec = SecMesh()
sec.assign_group(dict(sec=obj))
sec.assign_mesh_size(dict(sec=0.1))
sec.mesh()
sec_props = sec.get_sec_props(display_results=True, plot_centroids=False)
sec_props2 = sec.get_frame_props(display_results=True)
sec.centring()
# sec.rotate(45)
sec.view(fill=True, engine='plotly', save_html="SecMesh.html")

stress = sec.get_stress(N=-10000, Vy=1000, Vz=1000,
                        Myy=10000, Mzz=10000, Mxx=100000, plot_stress='vy_xyz',)

# case 2
outlines = [[0, 0], [2, 0], [2, 2], [0, 2]]
coverlines = offset(outlines, d=0.05)
cover = add_polygon(outlines, holes=[coverlines])
core = add_polygon(coverlines)
sec = SecMesh()
sec.assign_group(dict(cover=cover, core=core))
sec.assign_mesh_size(dict(cover=0.02, core=0.05))
sec.assign_group_color(dict(cover="gray", core="green"))
sec.mesh()
_ = sec.get_sec_props(display_results=True, plot_centroids=False)
_ = sec.get_frame_props(display_results=True)
sec.centring()
# sec.rotate(45)
sec.view(fill=True, engine='plotly', save_html="SecMesh.html")

# case 3
outlines = [[0, 0], [2, 0], [2, 2], [0, 2]]
coverlines = offset(outlines, d=0.05)
cover = add_polygon(outlines, holes=[coverlines])
holelines = [[0.5, 0.5], [1.5, 0.5], [1.5, 1.5], [0.5, 1.5]]
core = add_polygon(coverlines, holes=[holelines])
sec = SecMesh()
sec.assign_group(dict(cover=cover, core=core))
sec.assign_mesh_size(dict(cover=0.02, core=0.05))
sec.assign_group_color(dict(cover="gray", core="green"))
sec.mesh()
# add rebars
rebars = Rebars()
rebar_lines1 = offset(outlines, d=0.05 + 0.032 / 2)
rebars.add_rebar_line(
    points=rebar_lines1, dia=0.032, gap=0.1, color="red",
)
rebar_lines2 = offset(holelines, d=-(0.05 + 0.02 / 2))
rebars.add_rebar_line(
    points=rebar_lines2, dia=0.020, gap=0.1, color="black",
)
rebar_lines3 = [[0.3, 0.3], [1.7, 0.3], [1.7, 1.7], [0.3, 1.7]]
rebars.add_rebar_line(
    points=rebar_lines3, dia=0.026, gap=0.15, closure=True,
    color="blue",
)
# add to the sec
sec.add_rebars(rebars)

# sec.get_sec_props(display_results=True, plot_centroids=False)
sec.get_frame_props(display_results=True)
sec.centring()
# sec.rotate(45)
sec.view(fill=True, engine='plotly', save_html="SecMesh.html")

# case 4
outlines = [[0, 0], [2, 0], [2, 2], [0, 2]]
coverlines = offset(outlines, d=0.05)
cover = add_polygon(outlines, holes=[coverlines])
holelines = [[0.5, 0.5], [1.5, 0.5], [1.5, 1.5], [0.5, 1.5]]
core = add_polygon(coverlines, holes=[holelines])
sec = SecMesh()
sec.assign_group(dict(cover=cover, core=core))
sec.assign_mesh_size(dict(cover=0.02, core=0.05))
sec.assign_group_color(dict(cover="gray", core="green"))
sec.assign_ops_matTag(dict(cover=1, core=2))
sec.mesh()
# add rebars
rebars = Rebars()
rebar_lines1 = offset(outlines, d=0.05 + 0.032 / 2)
rebars.add_rebar_line(
    points=rebar_lines1, dia=0.032, gap=0.1, color="red", matTag=3
)
rebar_lines2 = offset(holelines, d=-(0.05 + 0.02 / 2))
rebars.add_rebar_line(
    points=rebar_lines2, dia=0.020, gap=0.1, color="black", matTag=3
)
rebar_lines3 = [[0.3, 0.3], [1.7, 0.3], [1.7, 1.7], [0.3, 1.7]]
rebars.add_rebar_line(
    points=rebar_lines3, dia=0.026, gap=0.15, closure=True,
    color="blue", matTag=3
)
# add to the sec
sec.add_rebars(rebars)
sec_props = sec.get_sec_props(display_results=True, plot_centroids=False)
sec.centring()
# sec.rotate(45)
sec.view(fill=True, engine='plotly', save_html="SecMesh.html")
G = 10000
sec.to_file("mysec.py", secTag=1, GJ=G * sec_props['J'])

# Case 5
outlines = [[0.5, 0], [7.5, 0], [8, 0.5], [8, 4.5],
            [7.5, 5], [0.5, 5], [0, 4.5], [0, 0.5]]
cover_d = 0.08
coverlines = offset(outlines, d=cover_d)
cover = add_polygon(outlines, holes=[coverlines])
holelines1 = [[1, 1], [3.5, 1], [3.5, 4], [1, 4]]
holelines2 = [[4.5, 1], [7, 1], [7, 4], [4.5, 4]]
core = add_polygon(coverlines, holes=[holelines1, holelines2])
sec = SecMesh()
sec.assign_group(dict(cover=cover, core=core))
sec.assign_mesh_size(dict(cover=0.2, core=0.4))
sec.assign_group_color(dict(cover="gray", core="green"))
sec.assign_ops_matTag(dict(cover=1, core=2))
sec.mesh()
# add rebars
rebars = Rebars()
rebar_lines1 = offset(outlines, d=cover_d + 0.032 / 2)
rebars.add_rebar_line(
    points=rebar_lines1, dia=0.032, gap=0.15, color="red", matTag=3
)
rebar_lines2 = offset(holelines1, d=-(0.05 + 0.02 / 2))
rebars.add_rebar_line(
    points=rebar_lines2, dia=0.020, gap=0.2, color="black", matTag=3
)
rebar_lines3 = offset(holelines2, d=-(0.05 + 0.02 / 2))
rebars.add_rebar_line(
    points=rebar_lines3, dia=0.020, gap=0.2, color="black", matTag=3
)
# add to the sec
sec.add_rebars(rebars)
# sec_props = sec.get_sec_props(display_results=True, plot_centroids=False)
sec.get_frame_props(display_results=True)
sec.centring()
# sec.rotate(45)
sec.view(fill=True, engine='plotly', save_html="SecMesh.html")
G = 10000
sec.to_file("mysec.py", secTag=1, GJ=G * sec_props['J'])
stress = sec.get_stress(N=-10000, Vy=1000, Vz=1000,
                        Myy=10000, Mzz=10000, Mxx=100000, plot_stress='all',)

# case 6
cover_d = 0.05
all = add_circle(xo=[0, 0], radius=0.75)
core = add_circle(xo=[0, 0], radius=0.75 - cover_d)
cover = all - core
sec = SecMesh()
sec.assign_group(dict(cover=cover, core=core))
sec.assign_mesh_size(dict(cover=0.02, core=0.08))
sec.assign_group_color(dict(cover="gray", core="green"))
sec.assign_ops_matTag(dict(cover=1, core=2))
sec.mesh()
# add rebars
rebars = Rebars()
rebars.add_rebar_circle(xo=[0, 0], radius=0.75 - 0.026 / 2 - cover_d,
                        dia=0.026, gap=0.15, matTag=3)
# add to the sec
sec.add_rebars(rebars)
sec_props = sec.get_sec_props(display_results=True, plot_centroids=False)
_ = sec.get_frame_props(display_results=True)
sec.centring()
# sec.rotate(45)
sec.view(fill=True, engine='plotly', save_html="SecMesh.html")
G = 10000
sec.to_file("mysec.py", secTag=1, GJ=G * sec_props['J'])
stress = sec.get_stress(N=-10000, Vy=1000, Vz=1000,
                        Myy=10000, Mzz=10000, Mxx=100000, plot_stress='all',)

# case 7
left_circ_angles = np.linspace(90, 270, 20)
right_circ_angles = np.linspace(-90, 90, 20)
left_circ_lines = []
right_circ_lines = []
r = 2
b = 4
for ang in left_circ_angles:
    ang = ang / 180 * np.pi
    left_circ_lines.append([0 + r * np.cos(ang), r + r * np.sin(ang)])
for ang in right_circ_angles:
    ang = ang / 180 * np.pi
    right_circ_lines.append([b + r * np.cos(ang), r + r * np.sin(ang)])
outlines = left_circ_lines + right_circ_lines
cover_d = 0.08
coverlines = offset(outlines, d=cover_d)
cover = add_polygon(outlines, holes=[coverlines])
core = add_polygon(coverlines)
sec = SecMesh()
sec.assign_group(dict(cover=cover, core=core))
sec.assign_mesh_size(dict(cover=0.1, core=0.2))
sec.assign_group_color(dict(cover="gray", core="green"))
sec.assign_ops_matTag(dict(cover=1, core=2))
sec.mesh()
# add rebars
rebars = Rebars()
rebar_lines = offset(outlines, d=cover_d + 0.032 / 2)
rebars.add_rebar_line(
    points=rebar_lines, dia=0.032, gap=0.15, color="red", matTag=3
)
# add to the sec
sec.add_rebars(rebars)
# sec_props = sec.get_sec_props(display_results=True, plot_centroids=False)
sec.get_frame_props(display_results=True)
sec.centring()
# sec.rotate(45)
sec.view(fill=True, engine='p', save_html="SecMesh.html")
G = 10000
sec.to_file("mysec.py", secTag=1, GJ=G * sec_props['J'])

# case 8
Ec = 3.45E7
Es = 2.0E8
Nus = 0.3
Nuc = 0.2
tube_d = 0.02
steel_mat = add_material(name='steel', elastic_modulus=Es, poissons_ratio=Nus)
conc_mat = add_material(
    name='conc', elastic_modulus=Ec, poissons_ratio=Nuc)
all = add_circle(xo=[0, 0], radius=0.75)
conc = add_circle(xo=[0, 0], radius=0.75 - tube_d)
tube = all - conc
conc.material = conc_mat
tube.material = steel_mat
sec = SecMesh()
sec.assign_group(dict(tube=tube, conc=conc))
sec.assign_mesh_size(dict(tube=0.1, conc=0.2))
sec.assign_group_color(dict(tube="gray", conc="green"))
sec.assign_ops_matTag(dict(tube=1, conc=2))
sec.mesh()
sec_props = sec.get_sec_props(
    Eref=Ec, display_results=True, plot_centroids=False)
sec_props2 = sec.get_frame_props(
    Eref=Ec, display_results=True)
# sec.rotate(45)
sec.view(fill=True, engine='p', save_html="SecMesh.html")
sec.to_file("mysec.py", secTag=1, GJ=G * sec_props['J'])

# case 9
Ec = 3.45E7
Es = 2.0E8
Nus = 0.3
Nuc = 0.2
steel_mat = add_material(name='steel', elastic_modulus=Es, poissons_ratio=Nus)
conc_mat = add_material(
    name='conc', elastic_modulus=Ec, poissons_ratio=Nuc)
outlines = [[0, 0], [2, 0], [2, 2], [0, 2]]
coverlines = offset(outlines, d=0.05)
cover = add_polygon(outlines, holes=[coverlines], material=conc_mat)
bonelines = [[0.5, 0.5], [1.5, 0.5], [1.5, 0.7], [1.1, 0.7], [1.1, 1.3], [1.5, 1.3], [1.5, 1.5],
             [0.5, 1.5], [0.5, 1.3], [0.9, 1.3], [0.9, 0.7], [0.5, 0.7], [0.5, 0.5]]
core = add_polygon(coverlines, holes=[bonelines], material=conc_mat)
bone = add_polygon(bonelines, material=steel_mat)
sec = SecMesh()
sec.assign_group(dict(cover=cover, core=core, bone=bone))
sec.assign_mesh_size(dict(cover=0.02, core=0.05, bone=0.02))
# sec.assign_group_color(dict(cover="gray", core="blue", bone='yellow'))
sec.assign_ops_matTag(dict(cover=1, core=2, bone=4))
sec.mesh()
# add rebars
rebars = Rebars()
rebar_lines1 = offset(outlines, d=0.05 + 0.032 / 2)
rebars.add_rebar_line(
    points=rebar_lines1, dia=0.032, gap=0.1, color="red", matTag=3
)
# add to the sec
sec.add_rebars(rebars)
sec_props = sec.get_sec_props(
    Eref=Ec, display_results=True, plot_centroids=False)
sec_props2 = sec.get_frame_props(
    Eref=Ec, display_results=True)
# sec.centring()
sec.rotate(0)
Gc = Ec / 2 / (1 + Nuc)
sec.to_file("mysec.py", secTag=1, GJ=Gc * sec_props['J'])
sec.view(fill=True, engine='plotly', save_html="SecMesh.html")
stress = sec.get_stress(N=-10000, Vy=1000, Vz=1000,
                        Myy=10000, Mzz=10000, Mxx=100000, plot_stress='all',
                        normalize=True, cmap='jet')
