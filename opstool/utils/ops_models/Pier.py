import numpy as np
import openseespy.opensees as ops


def Pier():
    ops.wipe()
    ops.model('basic', '-ndm', 3, '-ndf', 3)
    matTag, E, nu, rho = 1, 3.E7, 0.2, 2.55
    ops.nDMaterial('ElasticIsotropic', matTag, E, nu)

    ele_mass = {}
    node_mass = {}

    B = 1
    L = 1
    H = 8
    nB, nL, nH = (6, 6, 41)
    dB, dL, dH = (B / (nB - 1), L / (nL - 1), H / (nH - 1))
    xs = np.linspace(0, B, nB)
    ys = np.linspace(0, L, nL)
    zs = np.linspace(0, H, nH)

    tag = 0
    for k in range(nH):
        for j in range(nL):
            for i in range(nB):
                x = xs[i]
                y = ys[j]
                z = zs[k]
                tag += 1
                ops.node(tag, x, y, z)
    ops.fixZ(0, *[1, 1, 1])

    nodeTags = np.arange(1, nB * nL * nH + 1).reshape((nH, nL, nB))
    tag = 0
    for k in range(nH - 1):
        for j in range(nL - 1):
            for i in range(nB - 1):
                node1, node2 = int(nodeTags[k][j][i]), int(
                    nodeTags[k][j][i + 1])
                node3, node4 = int(nodeTags[k][j + 1]
                                   [i + 1]), int(nodeTags[k][j + 1][i])
                node5, node6 = int(nodeTags[k + 1][j][i]
                                   ), int(nodeTags[k + 1][j][i + 1])
                node7, node8 = int(nodeTags[k + 1][j + 1]
                                   [i + 1]), int(nodeTags[k + 1][j + 1][i])
                eleNodes = [node1, node2, node3,
                            node4, node5, node6, node7, node8]
                tag += 1
                ops.element('stdBrick', tag, *eleNodes, matTag)
                ele_mass[tag] = (dB * dL * dH) * rho

    for tag in ele_mass.keys():
        nodeTags = ops.eleNodes(tag)
        mass = ele_mass[tag]
        for tag_ in nodeTags:
            if tag_ in node_mass.keys():
                node_mass[tag_] += mass / 8
            else:
                node_mass[tag_] = mass / 8
    for tag in node_mass.keys():
        ops.mass(tag, node_mass[tag], node_mass[tag], node_mass[tag])
