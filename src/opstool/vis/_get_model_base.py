import numpy as np
import openseespy.opensees as ops

from ..utils import (ELE_TAG_Beam, ELE_TAG_Link, ELE_TAG_Plane, ELE_TAG_Brick,
                     ELE_TAG_Tetrahedron, ELE_TAG_Truss, ELE_TAG_PFEM)


def get_node_coords():
    node_tags = ops.getNodeTags()
    num_node = len(node_tags)
    node_coords = np.zeros((num_node, 3))
    node_index = dict()  # key: nodeTag, value: index in Node_Coords
    model_dims = []
    for i, Tag in enumerate(node_tags):
        coord = ops.nodeCoord(Tag)
        model_dim = len(coord)
        if model_dim == 1:
            coord.extend([0, 0])
        elif model_dim == 2:
            coord.extend([0])
        model_dims.append(model_dim)
        node_coords[i] = coord
        node_index[Tag] = i
    return node_coords, node_index, model_dims, node_tags


def get_node_fix(node_coords, node_index):
    fixed_nodes = ops.getFixedNodes()
    fixed_dofs = []
    fixed_coords = []
    for tag in fixed_nodes:
        fixed_coords.append(node_coords[node_index[tag]])
        fixeddofs = ops.getFixedDOFs(tag)
        fixities = [0] * 6
        for dof in fixeddofs:
            fixities[dof - 1] = -1
        fixed_dofs.append(fixities)
    fixed_coords = np.array(fixed_coords)
    fixed_dofs = np.array(fixed_dofs)
    return fixed_nodes, fixed_coords, fixed_dofs


def get_mp_constraint(node_coords, node_index):
    retained_nodes = ops.getRetainedNodes()
    points = []
    midpoints = []
    cells = []
    dofs = []
    for i, tag in enumerate(retained_nodes):
        constrained_nodes = ops.getConstrainedNodes(tag)
        for tag2 in constrained_nodes:
            points.append(node_coords[node_index[tag]])
            points.append(node_coords[node_index[tag2]])
            midpoints.append(
                (node_coords[node_index[tag]] + node_coords[node_index[tag2]]) / 2)
            cells.extend([2, 2 * i, 2 * i + 1])
            dof = ops.getRetainedDOFs(tag, tag2)
            dofs.append(dof)
    return np.array(points), np.array(midpoints), dofs, cells


def get_truss_info(ele_tags, node_index):
    truss_cells = []
    truss_cells_tags = []
    for i, ele in enumerate(ele_tags):
        ele_nodes = ops.eleNodes(ele)
        if len(ele_nodes) == 2 and ops.getEleClassTags(ele)[0] in ELE_TAG_Truss:
            node_i, node_j = ele_nodes
            idx_i, idx_j = node_index[node_i], node_index[node_j]
            truss_cells.extend([2, idx_i, idx_j])
            truss_cells_tags.append(ele)
    return truss_cells, truss_cells_tags


def get_link_info(ele_tags, node_coords, node_index):
    link_cells = []
    link_cells_tags = []
    link_midpoints = []
    link_lengths = []
    link_xlocal = []
    link_ylocal = []
    link_zlocal = []
    for i, ele in enumerate(ele_tags):
        ele_nodes = ops.eleNodes(ele)
        if len(ele_nodes) == 2 and ops.getEleClassTags(ele)[0] in ELE_TAG_Link:
            node_i, node_j = ele_nodes
            idx_i, idx_j = node_index[node_i], node_index[node_j]
            link_cells.extend([2, idx_i, idx_j])
            link_cells_tags.append(ele)
            link_midpoints.append(
                (node_coords[idx_i] + node_coords[idx_j]) / 2)
            link_lengths.append(
                np.sqrt(np.sum((node_coords[idx_i] - node_coords[idx_j])**2)))
            xlocal = ops.eleResponse(ele, "xaxis")
            ylocal = ops.eleResponse(ele, "yaxis")
            zlocal = ops.eleResponse(ele, "zaxis")
            if xlocal:
                link_xlocal.append(np.array(xlocal) / np.linalg.norm(xlocal))
            else:
                link_xlocal.append(np.array([0., 0., 0.]))
            if ylocal:
                link_ylocal.append(np.array(ylocal) / np.linalg.norm(ylocal))
            else:
                link_ylocal.append(np.array([0., 0., 0.]))
            if zlocal:
                link_zlocal.append(np.array(zlocal) / np.linalg.norm(zlocal))
            else:
                link_zlocal.append(np.array([0., 0., 0.]))
    link_midpoints = np.array(link_midpoints)
    link_lengths = np.array(link_lengths)
    link_xlocal = np.array(link_xlocal)
    link_ylocal = np.array(link_ylocal)
    link_zlocal = np.array(link_zlocal)
    return (link_cells, link_cells_tags, link_midpoints, link_lengths,
            link_xlocal, link_ylocal, link_zlocal)


def get_beam_info(ele_tags, node_coords, node_index):
    beam_cells = []
    beam_cells_tags = []
    beam_midpoints = []
    beam_lengths = []
    beam_xlocal = []
    beam_ylocal = []
    beam_zlocal = []
    for i, ele in enumerate(ele_tags):
        ele_nodes = ops.eleNodes(ele)
        if len(ele_nodes) == 2 and ops.getEleClassTags(ele)[0] in ELE_TAG_Beam:
            node_i, node_j = ele_nodes
            idx_i, idx_j = node_index[node_i], node_index[node_j]
            beam_cells.extend([2, idx_i, idx_j])
            beam_cells_tags.append(ele)
            beam_midpoints.append(
                (node_coords[idx_i] + node_coords[idx_j]) / 2)
            beam_lengths.append(
                np.sqrt(np.sum((node_coords[idx_i] - node_coords[idx_j])**2)))
            xlocal = ops.eleResponse(ele, "xaxis")
            ylocal = ops.eleResponse(ele, "yaxis")
            zlocal = ops.eleResponse(ele, "zaxis")
            if xlocal:
                beam_xlocal.append(np.array(xlocal) / np.linalg.norm(xlocal))
            else:
                beam_xlocal.append(np.array([0., 0., 0.]))
            if xlocal:
                beam_ylocal.append(np.array(ylocal) / np.linalg.norm(ylocal))
            else:
                beam_ylocal.append(np.array([0., 0., 0.]))
            if zlocal:
                beam_zlocal.append(np.array(zlocal) / np.linalg.norm(zlocal))
            else:
                beam_zlocal.append(np.array([0., 0., 0.]))
    beam_midpoints = np.array(beam_midpoints)
    beam_lengths = np.array(beam_lengths)
    beam_xlocal = np.array(beam_xlocal)
    beam_ylocal = np.array(beam_ylocal)
    beam_zlocal = np.array(beam_zlocal)
    return (beam_cells, beam_cells_tags, beam_midpoints, beam_lengths,
            beam_xlocal, beam_ylocal, beam_zlocal)


def get_other_line_info(ele_tags, node_index):
    other_line_cells = []
    other_line_cells_tags = []
    for i, ele in enumerate(ele_tags):
        ele_nodes = ops.eleNodes(ele)
        if len(ele_nodes) == 2:
            class_tag = ops.getEleClassTags(ele)[0]
            if class_tag not in (ELE_TAG_Beam + ELE_TAG_Link + ELE_TAG_Truss):
                node_i, node_j = ele_nodes
                idx_i, idx_j = node_index[node_i], node_index[node_j]
                other_line_cells.extend([2, idx_i, idx_j])
                other_line_cells_tags.append(ele)
    return other_line_cells, other_line_cells_tags


def get_all_line_info(ele_tags, node_index):
    all_lines_cells = []
    all_lines_cells_tags = []
    for i, ele in enumerate(ele_tags):
        ele_nodes = ops.eleNodes(ele)
        if len(ele_nodes) == 2:
            node_i, node_j = ele_nodes
            idx_i, idx_j = node_index[node_i], node_index[node_j]
            all_lines_cells.extend([2, idx_i, idx_j])
            all_lines_cells_tags.append(ele)
    return all_lines_cells, all_lines_cells_tags


def get_plane_info(ele_tags, node_index):
    plane_cells = []
    plane_cells_tags = []
    for i, ele in enumerate(ele_tags):
        ele_nodes = ops.eleNodes(ele)
        class_tag = ops.getEleClassTags(ele)[0]
        if class_tag in ELE_TAG_Plane:
            if len(ele_nodes) in [6, 7]:
                if class_tag in ELE_TAG_PFEM:
                    ele_nodes = [ele_nodes[1], ele_nodes[3], ele_nodes[5]]
                else:
                    ele_nodes = [ele_nodes[0], ele_nodes[3], ele_nodes[1],
                                 ele_nodes[4], ele_nodes[2], ele_nodes[5]]
            elif len(ele_nodes) in [8, 9]:
                ele_nodes = [ele_nodes[0], ele_nodes[4], ele_nodes[1], ele_nodes[5],
                             ele_nodes[2], ele_nodes[6], ele_nodes[3], ele_nodes[7]]
            idxs = [node_index[tag_] for tag_ in ele_nodes]
            plane_cells.extend([len(idxs)] + idxs)
            plane_cells_tags.append(ele)
    return plane_cells, plane_cells_tags


def get_tet_info(ele_tags, node_index):
    tetrahedron_cells = []
    tetrahedron_cells_tags = []
    for i, ele in enumerate(ele_tags):
        ele_nodes = ops.eleNodes(ele)
        class_tag = ops.getEleClassTags(ele)[0]
        if class_tag in ELE_TAG_Tetrahedron:  # tetrahedron
            if len(ele_nodes) == 8:  # FEMBubble 3D
                ele_nodes = [ele_nodes[1], ele_nodes[3],
                             ele_nodes[5], ele_nodes[7]]
            if len(ele_nodes) == 4:
                node_i, node_j, node_k, node_l = ele_nodes
                idx_i, idx_j = node_index[node_i], node_index[node_j]
                idx_k, idx_l = node_index[node_k], node_index[node_l]
                tetrahedron_cells.extend([3, idx_i, idx_j, idx_k])
                tetrahedron_cells.extend([3, idx_i, idx_j, idx_l])
                tetrahedron_cells.extend([3, idx_i, idx_k, idx_l])
                tetrahedron_cells.extend([3, idx_j, idx_k, idx_l])
                tetrahedron_cells_tags.append(ele)
            elif len(ele_nodes) == 10:
                idxs = [node_index[tag_] for tag_ in ele_nodes]
                tetrahedron_cells.extend(
                    [6, idxs[0], idxs[4], idxs[1], idxs[5], idxs[2], idxs[6]])
                tetrahedron_cells.extend(
                    [6, idxs[0], idxs[4], idxs[1], idxs[8], idxs[3], idxs[7]])
                tetrahedron_cells.extend(
                    [6, idxs[2], idxs[5], idxs[1], idxs[8], idxs[3], idxs[9]])
                tetrahedron_cells.extend(
                    [6, idxs[2], idxs[6], idxs[0], idxs[7], idxs[3], idxs[9]])
                tetrahedron_cells_tags.append(ele)
    return tetrahedron_cells, tetrahedron_cells_tags


def get_bri_info(ele_tags, node_index):
    brick_cells = []
    brick_cells_tags = []
    for i, ele in enumerate(ele_tags):
        ele_nodes = ops.eleNodes(ele)
        idxs = [node_index[tag_] for tag_ in ele_nodes]
        class_tag = ops.getEleClassTags(ele)[0]
        if class_tag in ELE_TAG_Brick:  # Brick
            if len(ele_nodes) == 8:
                idx1, idx2, idx3, idx4, idx5, idx6, idx7, idx8 = idxs
                brick_cells.extend([4, idx1, idx2, idx3, idx4])
                brick_cells.extend([4, idx5, idx6, idx7, idx8])
                brick_cells.extend([4, idx1, idx5, idx8, idx4])
                brick_cells.extend([4, idx2, idx6, idx7, idx3])
                brick_cells.extend([4, idx1, idx2, idx6, idx5])
                brick_cells.extend([4, idx3, idx4, idx8, idx7])
                brick_cells_tags.append(ele)
            elif len(ele_nodes) == 20:
                idx1, idx2, idx3, idx4, idx5, idx6, idx7 = idxs[:7]
                idx8, idx9, idx10, idx11, idx12, idx13, idx14 = idxs[7:14]
                idx15, idx16, idx17, idx18, idx19, idx20 = idxs[14:]
                brick_cells.extend(
                    [8, idx1, idx9, idx2, idx10, idx3, idx11, idx4, idx12])
                brick_cells.extend(
                    [8, idx5, idx13, idx6, idx14, idx7, idx15, idx8, idx16])
                brick_cells.extend(
                    [8, idx5, idx13, idx6, idx18, idx2, idx9, idx1, idx17])
                brick_cells.extend(
                    [8, idx7, idx15, idx8, idx20, idx4, idx11, idx3, idx19])
                brick_cells.extend(
                    [8, idx1, idx17, idx5, idx16, idx8, idx20, idx4, idx12])
                brick_cells.extend(
                    [8, idx2, idx18, idx6, idx14, idx7, idx19, idx3, idx10])
                brick_cells_tags.append(ele)
    return brick_cells, brick_cells_tags


# def get_all_face_info(ele_tags, node_coords, node_index):
#     pass


def get_ele_mid(ele_tags, node_coords, node_index):
    ele_midpoints = []
    for i, ele in enumerate(ele_tags):
        ele_nodes = ops.eleNodes(ele)
        idxs = [node_index[tag_] for tag_ in ele_nodes]
        ele_midpoints.append(np.mean(node_coords[idxs], axis=0))
    return np.array(ele_midpoints)


def get_bounds(node_coords):
    min_node = np.min(node_coords, axis=0)
    max_node = np.max(node_coords, axis=0)
    space = (max_node - min_node) / 5
    min_node = min_node - space
    max_node = max_node + space
    bounds = [
        min_node[0],
        max_node[0],
        min_node[1],
        max_node[1],
        min_node[2],
        max_node[2],
    ]
    max_bound = np.max(max_node - min_node)
    min_bound = np.min(max_node - min_node)
    return bounds, max_bound, min_bound


def get_model_info():
    # print(ops.constrainedDOFs())   constrainedDOFs
    node_coords, node_index, model_dims, node_tags = get_node_coords()
    fixed_nodes, fixed_coords, fixed_dofs = get_node_fix(
        node_coords, node_index)
    ctra_coords, ctra_midcoords, ctra_dofs, ctra_cells = get_mp_constraint(
        node_coords, node_index)
    ele_tags = ops.getEleTags()
    num_ele = len(ele_tags)
    truss_cells, truss_cells_tags = get_truss_info(ele_tags, node_index)
    (link_cells, link_cells_tags, link_midpoints, link_lengths,
     link_xlocal, link_ylocal, link_zlocal) = get_link_info(ele_tags, node_coords, node_index)
    (beam_cells, beam_cells_tags, beam_midpoints, beam_lengths,
     beam_xlocal, beam_ylocal, beam_zlocal) = get_beam_info(ele_tags, node_coords, node_index)
    other_line_cells, other_line_cells_tags = get_other_line_info(
        ele_tags, node_index)
    all_lines_cells, all_lines_cells_tags = get_all_line_info(
        ele_tags, node_index)
    plane_cells, plane_cells_tags = get_plane_info(ele_tags, node_index)
    tetrahedron_cells, tetrahedron_cells_tags = get_tet_info(
        ele_tags, node_index)
    brick_cells, brick_cells_tags = get_bri_info(ele_tags, node_index)
    all_faces_cells = plane_cells + tetrahedron_cells + brick_cells
    all_faces_cells_tags = plane_cells_tags + \
        tetrahedron_cells_tags + brick_cells_tags
    ele_midpoints = get_ele_mid(ele_tags, node_coords, node_index)
    bounds, max_bound, min_bound = get_bounds(node_coords)
    model_info = dict()
    model_info["coord_no_deform"] = node_coords
    model_info["coord_ele_midpoints"] = ele_midpoints
    model_info["bound"] = bounds
    model_info["max_bound"] = max_bound
    model_info["min_bound"] = min_bound
    model_info["num_ele"] = num_ele
    model_info["NodeTags"] = node_tags
    model_info["num_node"] = len(node_tags)
    model_info["FixNodeTags"] = fixed_nodes
    model_info["FixNodeDofs"] = fixed_dofs
    model_info["FixNodeCoords"] = fixed_coords
    model_info["ConstrainedCoords"] = ctra_coords
    model_info["ConstrainedMidCoords"] = ctra_midcoords
    model_info["ConstrainedDofs"] = ctra_dofs
    model_info["ConstrainedCells"] = ctra_cells
    model_info["EleTags"] = ele_tags
    model_info["model_dims"] = model_dims
    model_info["coord_ele_midpoints"] = ele_midpoints
    model_info["beam_midpoints"] = beam_midpoints
    model_info["beam_lengths"] = beam_lengths
    model_info["beam_xlocal"] = beam_xlocal
    model_info["beam_ylocal"] = beam_ylocal
    model_info["beam_zlocal"] = beam_zlocal
    model_info["link_midpoints"] = link_midpoints
    model_info["link_lengths"] = link_lengths
    model_info["link_xlocal"] = link_xlocal
    model_info["link_ylocal"] = link_ylocal
    model_info["link_zlocal"] = link_zlocal
    cells = dict()
    cells["all_lines"] = all_lines_cells
    cells['all_lines_tags'] = all_lines_cells_tags
    cells["all_faces"] = all_faces_cells
    cells["all_faces_tags"] = all_faces_cells_tags
    cells["plane"] = plane_cells
    cells["plane_tags"] = plane_cells_tags
    cells["tetrahedron"] = tetrahedron_cells
    cells["tetrahedron_tags"] = tetrahedron_cells_tags
    cells["brick"] = brick_cells
    cells["brick_tags"] = brick_cells_tags
    cells["truss"] = truss_cells
    cells["truss_tags"] = truss_cells_tags
    cells["link"] = link_cells
    cells["link_tags"] = link_cells_tags
    cells["beam"] = beam_cells
    cells["beam_tags"] = beam_cells_tags
    cells["other_line"] = other_line_cells
    cells["other_line_tags"] = other_line_cells_tags
    for key, value in cells.items():
        cells[key] = np.array(value)
    return model_info, cells


def get_node_react(fixed_nodes):
    reacts = []
    for tag in fixed_nodes:
        fixeddofs = ops.getFixedDOFs(tag)
        forces = [0] * 6
        for dof in fixeddofs:
            forces[dof - 1] = ops.nodeReaction(tag, dof)
        reacts.append(forces)
    return np.array(reacts)


def get_node_resp(node_tags):
    num_node = len(node_tags)
    node_disp = np.zeros((num_node, 3))
    node_vel = np.zeros((num_node, 3))
    node_accel = np.zeros((num_node, 3))
    node_deform_coord = np.zeros((num_node, 3))

    for i, Tag in enumerate(node_tags):
        coord = ops.nodeCoord(Tag)
        disp = ops.nodeDisp(Tag)
        vel = ops.nodeVel(Tag)
        accel = ops.nodeAccel(Tag)
        if len(coord) == 1:
            coord.extend([0, 0])
            disp.extend([0, 0])
            vel.extend([0, 0])
            accel.extend([0, 0])
        elif len(coord) == 2:
            if len(disp) in [2, 3]:
                coord.extend([0])
                disp = disp[:2]
                disp.extend([0])
                vel = vel[:2]
                vel.extend([0])
                accel = accel[:2]
                accel.extend([0])
            else:
                coord.extend([0])
                disp = disp[:2]
                disp.extend([0, 0])
                vel = vel[:2]
                vel.extend([0, 0])
                accel = accel[:2]
                accel.extend([0, 0])
        else:
            disp = disp[:3]  # ignore the rotation
            vel = vel[:3]
            accel = accel[:3]
        node_disp[i] = disp
        node_vel[i] = vel
        node_accel[i] = accel
        node_deform_coord[i] = [disp[ii] + coord[ii] for ii in range(3)]
    return node_disp, node_vel, node_accel, node_deform_coord


def get_beam_info2():
    ele_tags = ops.getEleTags()
    beam_tags = []
    beam_node_tags = []
    beam_node_map = dict()
    for i, eletag in enumerate(ele_tags):
        if ops.getEleClassTags(eletag)[0] in ELE_TAG_Beam:
            beam_tags.append(eletag)
            ele_nodes = ops.eleNodes(eletag)
            if ele_nodes[0] not in beam_node_tags:
                beam_node_tags.append(ele_nodes[0])
            if ele_nodes[1] not in beam_node_tags:
                beam_node_tags.append(ele_nodes[1])
            beam_node_map[eletag] = ele_nodes
    beam_node_coords = []
    node_coord_map = dict()
    for i, nodetag in enumerate(beam_node_tags):
        coord = ops.nodeCoord(nodetag)
        model_dim = len(coord)
        if model_dim == 1:
            coord.extend([0, 0])
        elif model_dim == 2:
            coord.extend([0])
        beam_node_coords.append(coord)
        node_coord_map[nodetag] = i
    beam_node_coords = np.array(beam_node_coords)
    beam_cells = []
    xlocals = []
    ylocals = []
    zlocals = []
    for i, eletag in enumerate(beam_tags):
        node1, node2 = beam_node_map[eletag]
        idx_i, idx_j = node_coord_map[node1], node_coord_map[node2]
        beam_cells.append([2, idx_i, idx_j])
        xlocal = ops.eleResponse(eletag, "xlocal")
        ylocal = ops.eleResponse(eletag, "ylocal")
        zlocal = ops.eleResponse(eletag, "zlocal")
        xlocals.append(np.array(xlocal) / np.linalg.norm(xlocal))
        ylocals.append(np.array(ylocal) / np.linalg.norm(ylocal))
        zlocals.append(np.array(zlocal) / np.linalg.norm(zlocal))
    xlocals = np.array(xlocals)
    ylocals = np.array(ylocals)
    zlocals = np.array(zlocals)
    beam_cells = np.array(beam_cells)
    bounds = np.array(ops.nodeBounds())
    return beam_tags, beam_node_coords, beam_cells, xlocals, ylocals, zlocals, bounds


def get_beam_resp(beam_tags):
    beam_resp_steps = []
    for eletag in beam_tags:
        local_forces = ops.eleResponse(eletag, "localForce")
        if len(local_forces) == 6:
            local_forces = [local_forces[0], local_forces[1], 0, 0, 0, local_forces[2],
                            local_forces[3], local_forces[4], 0, 0, 0, local_forces[5]]
        # for ii in range(6):
        #     local_forces[ii] = -local_forces[ii]
        beam_resp_steps.append(local_forces)
    beam_resp_steps = np.array(beam_resp_steps)
    return beam_resp_steps


def sort_xy(x, y):
    """
    Sort points counterclockwise
    """
    x0 = np.mean(x)
    y0 = np.mean(y)
    r = np.sqrt((x - x0) ** 2 + (y - y0) ** 2)
    angles = np.where(
        (y - y0) >= 0, np.arccos((x - x0) / r),
        4 * np.pi - np.arccos((x - x0) / r)
    )
    mask = np.argsort(angles)
    x_max = np.max(x)
    if x[mask][0] != x_max:
        mask = np.roll(mask, 1)
    return mask


def counter_clockwise(points, tag):
    """
    Used to sort the points on a face counterclockwise
    """
    x = np.array([point[0] for point in points])
    y = np.array([point[1] for point in points])
    z = np.array([point[2] for point in points])

    if all(np.abs(x - x[0]) < 1e-6):  # yz
        # def algo(point):
        #    return (math.atan2(point[2] - z_center, point[1] - y_center) + 2 * math.pi) % (2*math.pi)
        # sorted_points = sorted(points,key = algo )
        index = sort_xy(y, z)
        sorted_points = list(zip(x[index], y[index], z[index]))
        sorted_id = [points.index(i) for i in sorted_points]
        sorted_tag = [tag[i] for i in sorted_id]
    elif all(np.abs(y - y[0]) < 1e-6):  # xz
        # def algo(point):
        #    return (math.atan2(point[2] - z_center, point[0] - x_center) + 2 * math.pi) % (2*math.pi)
        # sorted_points = sorted(points,key = algo )
        index = sort_xy(x, z)
        sorted_points = list(zip(x[index], y[index], z[index]))
        sorted_id = [points.index(i) for i in sorted_points]
        sorted_tag = [tag[i] for i in sorted_id]
    else:
        # def algo(point):
        #    return (math.atan2(point[1] - y_center, point[0] - x_center) + 2 * math.pi) % (2*math.pi)
        # sorted_points = sorted(points,key = algo )
        index = sort_xy(x, y)
        sorted_points = list(zip(x[index], y[index], z[index]))
        sorted_id = [points.index(i) for i in sorted_points]
        sorted_tag = [tag[i] for i in sorted_id]
    return sorted_tag


def lines_angle(v1, v2):
    # return np.arctan2(np.linalg.norm(np.cross(v1, v2)), np.dot(v1, v2))
    x = np.array(v1)
    y = np.array(v2)
    l_x = np.sqrt(x.dot(x))
    l_y = np.sqrt(y.dot(y))
    cos_ = x.dot(y) / (l_x * l_y)
    angle_r = np.arccos(cos_)
    return angle_r
