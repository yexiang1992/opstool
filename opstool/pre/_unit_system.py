import re
import rich

ratio_length = dict(
    inch2m=0.0254,
    inch2dm=0.254,
    inch2cm=2.54,
    inch2mm=25.4,
    inch2km=2.54e-5,
    inch2ft=0.0833333333,
    ft2mm=304.8,
    ft2cm=30.48,
    ft2dm=3.048,
    ft2m=0.3048,
    ft2km=3.048e-4,
    mm2cm=0.1,
    mm2dm=0.01,
    mm2m=0.001,
    mm2km=1e-6,
    cm2dm=0.1,
    cm2m=0.01,
    cm2km=1e-5,
    m2km=1e-3,
)
ratio_force = dict(
    lb2lbf=1,
    lb2kip=0.001,
    lb2n=4.4482216282509,
    lb2kn=4.4482216282509e-3,
    lb2mn=4.448e-6,
    lb2kgf=0.45359236844386,
    lb2tonf=0.0004535923699994,
    lbf2kip=0.001,
    lbf2n=4.4482216282509,
    lbf2kn=4.4482216282509e-3,
    lbf2mn=4.448e-6,
    lbf2kgf=0.45359236844386,
    lbf2tonf=0.0004535923699994,
    kip2n=4448.2216,
    kip2kn=4448.2216e-3,
    kip2mn=4448.2216e-6,
    kip2kgf=453.59236844386,
    kip2tonf=0.4535923699994,
    n2kn=1e-3,
    n2mn=1e-6,
    n2kgf=0.10197162129779283,
    n2tonf=0.0001019716212978,
    kn2mn=1e-3,
    kn2kgf=101.9716212978,
    kn2tonf=0.1019716212978,
    mn2kgf=101971.6212978,
    mn2tonf=101.9716212978,
    kgf2tonf=0.001,
)
ratio_time = dict(sec2msec=0.001)


def ratio_update(ratio_dict):
    temp_dict = dict()
    for key, value in ratio_dict.items():
        idx = key.index("2")
        new_key = key[idx + 1 :] + "2" + key[:idx]
        temp_dict[new_key] = 1 / value
        new_key = key[:idx] + "2" + key[:idx]
        temp_dict[new_key] = 1
    ratio_dict.update(temp_dict)


ratio_update(ratio_length)
ratio_update(ratio_force)
ratio_update(ratio_time)

unit_length = ["inch", "ft", "mm", "cm", "m"]
unit_force = ["lb", "lbf", "kip", "n", "kn", "mn", "kgf", "tonf"]
unit_time = ["sec", "msec"]
unit_mass = ["mg", "g", "kg", "ton", "t", "slug"]
unit_stress = ["pa", "kpa", "mpa", "gpa", "bar", "psi", "ksi", "psf", "ksf"]


class UnitSystem:
    """A class for unit conversion.

    Parameters
    -----------
    length: str, default="m"
        Length unit base. Optional ["inch", "ft", "mm", "cm", "m"].
    force: str, default="kN"
        Force unit base. Optional ["lb"("lbf"), "kip", "n", "kn", "mn", "kgf", "tonf"].
    time: str, default="sec"
        Time unit base. Optional ["sec", "msec"].

    .. note::
        * `Mass` and `stress` units can be automatically determined based on `length` and `force` units,
          optional mass units include ["mg", "g", "kg", "ton"("t"), "slug"],
          and optional stress units include ["pa", "kpa", "mpa", "gpa", "bar", "psi", "ksi", "psf", "ksf"].

        * You can enter any uppercase and lowercase forms, such as ``kn`` and ``kN``, ``mpa`` and ``MPa``
          are equivalent.

        * You can add a number after the unit to indicate a power, such as ``m3`` for ``m*m*m``.
    """

    def __init__(self, length: str = "m", force: str = "kN", time: str = "sec") -> None:
        for unit in unit_length:
            setattr(self, unit, ratio_length[unit + "2" + length.lower()])
        for unit in unit_force:
            setattr(self, unit, ratio_force[unit + "2" + force.lower()])
        for unit in unit_time:
            setattr(self, unit, ratio_time[unit + "2" + time.lower()])
        # mass
        self.kg = self.n * self.sec**2 / self.m
        self.mg, self.g, self.ton = 1e-6 * self.kg, 1e-3 * self.kg, 1e3 * self.kg
        self.t, self.slug, self.slinch = (
            1e3 * self.kg,
            14.593902937 * self.kg,
            175.126836 * self.kg,
        )
        # stress
        self.pa = self.n / (self.m * self.m)
        self.kpa, self.mpa, self.gpa = 1000 * self.pa, 1e6 * self.pa, 1e9 * self.pa
        self.bar = 1e5 * self.pa
        self.psi, self.ksi = 6894.7572932 * self.pa, 6894757.2932 * self.pa
        self.psf, self.ksf = 47.880208 * self.pa, 47880.2468616010 * self.pa

    def __getattr__(self, item):
        v = re.findall(r"-?\d+\.?\d*e?E?-?\d*?", item)
        if v:
            v = float(v[0])
        else:
            return getattr(self, item.lower())
        s = "".join([x for x in item if x.isalpha()])
        base = getattr(self, s)
        return base**v

    def __repr__(self):
        txt = "\n[bold #d20962]Length unit:[/bold #d20962]\n"
        for i, unit in enumerate(unit_length):
            txt += f"{unit}={getattr(self, unit)}; "
            if i > 1 and (i + 1) % 5 == 0:
                txt += "\n"
        txt += "\n\n[bold #f47721]Force unit:[/bold #f47721]\n"
        for i, unit in enumerate(unit_force):
            txt += f"{unit}={getattr(self, unit)}; "
            if i > 1 and (i + 1) % 5 == 0:
                txt += "\n"
        txt += "\n\n[bold #7ac143]Time unit:[/bold #7ac143]\n"
        for i, unit in enumerate(unit_time):
            txt += f"{unit}={getattr(self, unit)}; "
            if i > 1 and (i + 1) % 5 == 0:
                txt += "\n"
        txt += "\n\n[bold #00bce4]Mass unit:[/bold #00bce4]\n"
        for i, unit in enumerate(unit_mass):
            txt += f"{unit}={getattr(self, unit)}; "
            if i > 1 and (i + 1) % 5 == 0:
                txt += "\n"
        txt += "\n\n[bold #7d3f98]Pressure unit:[/bold #7d3f98]\n"
        for i, unit in enumerate(unit_stress):
            txt += f"{unit}={getattr(self, unit)}; "
            if i > 1 and (i + 1) % 5 == 0:
                txt += "\n"
        rich.print(txt)
        return ""
