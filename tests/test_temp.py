import plotly.graph_objects as go
import plotly as plt
import numpy as np
import random as rnd


def rndata(a=-20, b=20):
    a = a
    b = b
    n = 1
    rslt = []
    for i in range(n):
        rslt.extend([rnd.randint(a, b), rnd.randint(a, b), None])

    return rslt


fig = go.Figure()

for i in range(10):
    x = rndata(0, 100)
    y = rndata(-10, 10)
    z = rndata(0, 40)

    size = ((x[1] - x[0]) ** 2 + (y[1] - y[0]) ** 2 + (z[1] - z[0]) ** 2) ** 0.5
    axis = [(x[1] - x[0]) / size, (y[1] - y[0]) / size, (z[1] - z[0]) / size]
    np.linalg.norm(axis)
    fig.add_scatter3d(x=x, y=y, z=z, mode="lines")

    u = [axis[0], None]
    v = [axis[1], None]
    w = [axis[2], None]
    xx = [x[1], None]
    yy = [y[1], None]
    zz = [z[1], None]

    cl = rnd.choice(plt.colors.DEFAULT_PLOTLY_COLORS)
    sizes = 10
    fig = fig.add_cone(
        opacity=0.5,
        sizemode="absolute",
        sizeref=sizes,
        showscale=False,
        anchor="tip",  # ['tip', 'tail', 'cm', 'center']
        x=xx,
        y=yy,
        z=zz,
        u=u,
        v=v,
        w=w,
        text=str(sizes),
    )

fig.update_layout(
    scene_aspectmode="data",
)
fig.show()
