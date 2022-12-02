import numpy as np
import openseespy.opensees as ops


def gen_grav_load(ts_tag: int, pattern_tag: int,
                  g: float = 9.81, factor: float = -1.0, direction: str = "Z"):
    direction = direction.upper()
    ops.timeSeries('Linear', int(ts_tag))
    ops.pattern('Plain', int(pattern_tag), int(ts_tag))
    node_tags = ops.getNodeTags()
    load_fact_6d = dict(Z=np.array([0.0, 0.0, factor * g, 0.0, 0.0, 0.0]),
                        Y=np.array([0.0, factor * g, 0.0, 0.0, 0.0, 0.0]),
                        X=np.array([factor * g, 0.0, 0.0, 0.0, 0.0, 0.0]),
                        )
    load_fact_3d = dict(Z=np.array([0.0, 0.0, factor * g]),
                        Y=np.array([0.0, factor * g, 0]),
                        X=np.array([factor * g, 0.0, 0.0]),
                        )
    load_fact_2d = dict(Y=np.array([0.0, factor * g]),
                        X=np.array([factor * g, 0.0]),
                        )
    load_fact_1d = dict(X=np.array([factor * g, 0.0]))
    load_fact = {6: load_fact_6d, 3: load_fact_3d,
                 2: load_fact_2d, 1: load_fact_1d}
    for nodetag in node_tags:
        mass = np.array(ops.nodeMass(nodetag))
        loadValues = mass * load_fact[len(mass)][direction]
        if np.sum(np.abs(loadValues)) > 1e-10:
            ops.load(nodetag, *loadValues)
