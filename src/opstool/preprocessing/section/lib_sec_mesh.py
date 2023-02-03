import numpy as np
from sec_mesh import SecMesh, add_material, add_polygon, add_circle, offset, Rebars


def rc_rect(b: float, h: float, cover: float,
            rebar_dia: float, rebar_gap: float,
            cover_mesh_size: float, core_mesh_size: float,
            cover_ops_matTag: int, core_ops_matTag: int):
    outlines = [[-b / 2, -h / 2], [b / 2, -h / 2],
                [b / 2, h / 2], [-b / 2, h / 2]]
    coverlines = offset(outlines, d=cover)
    cover_obj = add_polygon(outlines, holes=[coverlines])
    core_obj = add_polygon(coverlines)
    sec = SecMesh(sec_name="Rectangular RC Section")
    sec.assign_group(dict(cover=cover_obj, core=core_obj))
    sec.assign_mesh_size(dict(cover=cover_mesh_size, core=core_mesh_size))
    sec.assign_ops_matTag(dict(cover=cover_ops_matTag, core=core_ops_matTag))
    sec.assign_group_color(dict(cover="gray", core="#677a04"))
    sec.mesh()
    # rebars
    rebars = Rebars()
    rebar_lines = offset(outlines, d=cover + rebar_dia / 2)
    rebars.add_rebar_line(
        points=rebar_lines, dia=rebar_dia, gap=rebar_gap, color="black",
    )
    sec.add_rebars(rebars)
    return sec


sec1 = rc_rect(b=1, h=1, cover=0.06,
               rebar_dia=0.032, rebar_gap=0.1,
               cover_mesh_size=0.01, core_mesh_size=0.02,
               cover_ops_matTag=1, core_ops_matTag=2)
sec1.view(engine='m')
