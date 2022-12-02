import os
import shelve
from typing import Union

import numpy as np
import openseespy.opensees as ops
from numpy.typing import ArrayLike

from ..utils import (ELE_TAG_Beam, ELE_TAG_Brick, ELE_TAG_Joint, ELE_TAG_Link,
                     ELE_TAG_Plane, ELE_TAG_Tetrahedron, ELE_TAG_Truss,
                     check_file, shape_dict)


class GetFEMdata:
    """
    Get the data in the openseespy model domain.

    Parameters
    ----------
    results_dir: str, default="opstool_output"
        The dir that results saved.
    """

    def __init__(self, results_dir: str = "opstool_output"):

        self.out_dir = results_dir

        self.model_info_names = [
            "coord_no_deform",
            "coord_ele_midpoints",
            "bound",
            "max_bound",
            "num_node",
            "num_ele",
            "NodeTags",
            "EleTags",
            "model_dims",
        ]
        self.model_info = dict()
        self.get_model_data_finished = False

        # Initialize cell connection data
        self.cells_names = [
            "truss",
            "link",
            "beam",
            "other_line",
            "all_lines",
            "plane",
            "tetrahedron",
            "brick",
            "all_faces",
        ]
        self.cells = dict()

        # Initialize eigenvalue data
        self.eigen_names = (
            ["f", "eigenvector"] + self.model_info_names + self.cells_names
        )
        self.eigen = None

        # Analysis step model update data
        self.model_info_steps = dict()
        # Ele connection update data
        self.cells_steps = dict()
        # Update node response data
        self.node_resp_names = ("disp", "vel", "accel")
        self.node_resp_steps = dict()
        self.step_node_track = 0

        self.beam_info_names = ['beam_tags', 'beam_node_coords', 'beam_cells', 'beam_cell_map',
                                'xlocal', 'ylocal', 'zlocal', 'bounds']
        self.beam_infos = dict()
        self.beam_resp_names = ['localForces', 'basicDeformations']
        self.beam_resp_step = dict()
        # ["N_1", "Vy_1", "Vz_1", "T_1", "My_1", "Mz_1",
        #  "N_2", "Vy_2", "Vz_2", "T_2", "My_2", "Mz_2"]
        # ["eps", "thetaZ_1", "thetaZ_2", "thetaY_1", "thetaY_2", "thetaX"]
        self.step_beam_track = 0

        # On/Off and Tracking for Model Updates
        self.model_update = False

        # self.reset_model_state()
        # self.reset_eigen_state()
        self.reset_steps_state()

        # fiber section data
        self.fiber_sec_tags = None
        self.fiber_sec_data = dict()
        self.fiber_sec_step_data = dict()
        self.step_fiber_track = 0

    def reset_model_state(self):
        """Reset the state of results extract of model data."""
        for name in self.model_info_names:
            self.model_info[name] = None
        for name in self.cells_names:
            self.cells[name] = None

    def reset_eigen_state(self):
        """Reset the state of results extract of eigen data."""
        self.eigen = dict()
        for name in self.eigen_names:
            self.eigen[name] = None

    def reset_steps_state(self):
        """Reset the state of results extract in analysis step"""

        self.step_node_track = 0
        self.step_beam_track = 0
        self.step_fiber_track = 0

        for name in self.model_info_names:
            self.model_info_steps[name] = []

        for name in self.cells_names:
            self.cells_steps[name] = []

        for name in self.node_resp_names:
            self.node_resp_steps[name] = []

        for name in self.beam_info_names:
            self.beam_infos[name] = None
        for name in self.beam_resp_names:
            self.beam_resp_step[name] = []

        self.fiber_sec_step_data = dict()

        # Truss Element Analysis Step Response Data

        # Beam Element Analysis Step Response Data

    def get_model_data(self):
        """Get data from the current model domain. The data will saved to file ``ModelData.da``.
        """
        # --------------------------------
        node_tags = ops.getNodeTags()
        node_tags.sort()
        num_node = len(node_tags)
        # Get all the ele tags
        ele_tags = ops.getEleTags()
        ele_tags.sort()
        num_ele = len(ele_tags)
        # Dict of node coordinates
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
            node_coords[i] = np.array(coord)
            node_index[Tag] = i
        points = node_coords

        # lines and faces
        # How the ele is connected，node number n-node tag 1-node tag 2-...-node tag n
        truss_cells = []
        truss_cells_tags = []
        link_cells = []
        link_cells_tags = []
        beam_cells = []
        beam_cells_tags = []
        beam_midpoints = []
        beam_xlocal = []
        beam_ylocal = []
        beam_zlocal = []
        other_line_cells = []
        other_line_cells_tags = []
        all_lines_cells = []
        all_lines_cells_tags = []
        plane_cells = []
        plane_cells_tags = []
        tetrahedron_cells = []
        tetrahedron_cells_tags = []
        brick_cells = []
        brick_cells_tags = []
        all_faces_cells = []
        all_faces_cells_tags = []
        ele_midpoints = []  # the coordinates of the ele's midpoint
        for i, ele in enumerate(ele_tags):
            ele_nodes = ops.eleNodes(ele)
            # Determine the element type based on the number of element nodes
            if len(ele_nodes) == 2:
                node_i, node_j = ele_nodes
                idx_i, idx_j = node_index[node_i], node_index[node_j]
                all_lines_cells.append([2, idx_i, idx_j])
                all_lines_cells_tags.append(ele)
                if ops.getEleClassTags(ele)[0] in ELE_TAG_Truss:
                    truss_cells.append([2, idx_i, idx_j])
                    truss_cells_tags.append(ele)
                elif ops.getEleClassTags(ele)[0] in ELE_TAG_Link:
                    link_cells.append([2, idx_i, idx_j])
                    link_cells_tags.append(ele)
                elif ops.getEleClassTags(ele)[0] in ELE_TAG_Beam:
                    beam_cells.append([2, idx_i, idx_j])
                    beam_cells_tags.append(ele)
                    beam_midpoints.append((node_coords[idx_i] + node_coords[idx_j]) / 2)
                    xlocal = ops.eleResponse(ele, "xlocal")
                    ylocal = ops.eleResponse(ele, "ylocal")
                    zlocal = ops.eleResponse(ele, "zlocal")
                    beam_xlocal.append(np.array(xlocal) / np.linalg.norm(xlocal))
                    beam_ylocal.append(np.array(ylocal) / np.linalg.norm(ylocal))
                    beam_zlocal.append(np.array(zlocal) / np.linalg.norm(zlocal))
                else:
                    other_line_cells.append([2, idx_i, idx_j])
                    other_line_cells_tags.append(ele)
                ele_midpoints.append((node_coords[idx_i] + node_coords[idx_j]) / 2)

            elif len(ele_nodes) == 3:
                node_i, node_j, node_k = ops.eleNodes(ele)
                idx_i, idx_j, idx_k = (
                    node_index[node_i],
                    node_index[node_j],
                    node_index[node_k],
                )
                all_faces_cells.append([3, idx_i, idx_j, idx_k])
                all_faces_cells_tags.append(ele)
                plane_cells.append([3, idx_i, idx_j, idx_k])
                plane_cells_tags.append(ele)
                ele_midpoints.append(
                    (node_coords[idx_i] + node_coords[idx_j] + node_coords[idx_k]) / 3
                )

            elif len(ele_nodes) == 4 or len(ele_nodes) == 9:
                if len(ele_nodes) == 4:
                    node_i, node_j, node_k, node_l = ops.eleNodes(ele)
                else:
                    node_i, node_j, node_k, node_l = ops.eleNodes(ele)[0:4]
                idx_i, idx_j = node_index[node_i], node_index[node_j]
                idx_k, idx_l = node_index[node_k], node_index[node_l]
                if ops.getEleClassTags(ele)[0] in ELE_TAG_Tetrahedron:  # tetrahedron
                    tetrahedron_cells.append([3, idx_i, idx_j, idx_k])
                    tetrahedron_cells.append([3, idx_i, idx_j, idx_l])
                    tetrahedron_cells.append([3, idx_i, idx_k, idx_l])
                    tetrahedron_cells.append([3, idx_j, idx_k, idx_l])
                    tetrahedron_cells_tags.append(ele)
                    all_faces_cells.append([3, idx_i, idx_j, idx_k])
                    all_faces_cells.append([3, idx_i, idx_j, idx_l])
                    all_faces_cells.append([3, idx_i, idx_k, idx_l])
                    all_faces_cells.append([3, idx_j, idx_k, idx_l])
                    all_faces_cells_tags.append(ele)
                else:
                    plane_cells.append([4, idx_i, idx_j, idx_k, idx_l])
                    plane_cells_tags.append(ele)
                    all_faces_cells.append([4, idx_i, idx_j, idx_k, idx_l])
                    all_faces_cells_tags.append(ele)
                ele_midpoints.append(np.mean(node_coords[[idx_i, idx_j, idx_k, idx_l]], axis=0))

            elif len(ele_nodes) == 8 or len(ele_nodes) == 20:
                if len(ele_nodes) == 8:
                    (
                        node1,
                        node2,
                        node3,
                        node4,
                        node5,
                        node6,
                        node7,
                        node8,
                    ) = ops.eleNodes(ele)
                else:
                    (
                        node1,
                        node2,
                        node3,
                        node4,
                        node5,
                        node6,
                        node7,
                        node8,
                    ) = ops.eleNodes(ele)[0:8]
                tag_list = [
                    node_index[node1],
                    node_index[node2],
                    node_index[node3],
                    node_index[node4],
                    node_index[node5],
                    node_index[node6],
                    node_index[node7],
                    node_index[node8],
                ]
                temp_points = np.array([node_coords[i] for i in tag_list])
                idxxx = np.argsort(temp_points[:, -1])
                temp_points = temp_points[idxxx]
                tag_list = np.array(tag_list)[idxxx]
                temp_points = [tuple(i) for i in temp_points]
                tag_list = list(tag_list)
                tag_counter1 = counter_clockwise(temp_points[:4], tag_list[:4])  # 逆时针排序
                tag_counter2 = counter_clockwise(temp_points[4:], tag_list[4:])  # 逆时针排序
                tag_counts = tag_counter1 + tag_counter2
                idx1, idx2, idx3, idx4, idx5, idx6, idx7, idx8 = tag_counts
                brick_cells.append([4, idx1, idx4, idx3, idx2])
                brick_cells.append([4, idx5, idx6, idx7, idx8])
                brick_cells.append([4, idx1, idx5, idx8, idx4])
                brick_cells.append([4, idx2, idx3, idx7, idx6])
                brick_cells.append([4, idx1, idx2, idx6, idx5])
                brick_cells.append([4, idx3, idx4, idx8, idx7])
                brick_cells_tags.append(ele)
                all_faces_cells.append([4, idx1, idx4, idx3, idx2])
                all_faces_cells.append([4, idx5, idx6, idx7, idx8])
                all_faces_cells.append([4, idx1, idx5, idx8, idx4])
                all_faces_cells.append([4, idx2, idx3, idx7, idx6])
                all_faces_cells.append([4, idx1, idx2, idx6, idx5])
                all_faces_cells.append([4, idx3, idx4, idx8, idx7])
                all_faces_cells_tags.append(ele)
                idxs1_8 = [idx1, idx2, idx3, idx4, idx5, idx6, idx7, idx8]
                ele_midpoints.append(np.mean(node_coords[idxs1_8], axis=0))
        ele_midpoints = np.array(ele_midpoints)
        beam_midpoints = np.array(beam_midpoints)
        beam_xlocal = np.array(beam_xlocal)
        beam_ylocal = np.array(beam_ylocal)
        beam_zlocal = np.array(beam_zlocal)

        # Automatically determine the coordinate axis boundary
        # according to the model node coordinates
        min_node = np.min(points, axis=0)
        max_node = np.max(points, axis=0)
        space = (max_node - min_node) / 15
        min_node = min_node - 2 * space
        max_node = max_node + 2 * space
        bounds = [
            min_node[0],
            max_node[0],
            min_node[1],
            max_node[1],
            min_node[2],
            max_node[2],
        ]
        max_bound = np.max(max_node - min_node)

        # FEM data, including link for points, lines, surfaces, solids
        model_info = dict()
        model_info["coord_no_deform"] = points
        model_info["coord_ele_midpoints"] = ele_midpoints
        model_info["bound"] = bounds
        model_info["max_bound"] = max_bound
        model_info["num_node"] = num_node
        model_info["num_ele"] = num_ele
        model_info["NodeTags"] = node_tags
        model_info["EleTags"] = ele_tags
        model_info["model_dims"] = model_dims
        model_info["coord_ele_midpoints"] = ele_midpoints
        model_info["beam_midpoints"] = beam_midpoints
        model_info["beam_xlocal"] = beam_xlocal
        model_info["beam_ylocal"] = beam_ylocal
        model_info["beam_zlocal"] = beam_zlocal

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

        self.model_info.update(model_info)
        self.cells.update(cells)

        self.get_model_data_finished = True

        if not os.path.exists(self.out_dir):
            os.makedirs(self.out_dir)
        output_filename = self.out_dir + '/ModelData'
        with shelve.open(output_filename) as db:
            db["ModelInfo"] = self.model_info
            db["Cell"] = self.cells

        # if output_file:
        #     with h5py.File(output_file, "w") as f:
        #         grp1 = f.create_group("ModelInfo")
        #         for name in self.model_info_names:
        #             grp1.create_dataset(name, data=self.model_info[name])
        #         grp2 = f.create_group("Cell")
        #         for name in self.cells_names:
        #             grp2.create_dataset(name, data=self.cells[name])

    def get_eigen_data(
            self,
            mode_tag: int = 1,
            solver: str = "-genBandArpack",
    ):
        """Get eigenvalue Analysis Data. The data will saved to file ``EigenData.dat``.

        Parameters
        ----------
        mode_tag: int
            mode tag.
        solver: str, default '-genBandArpack'
            type of solver, optional '-genBandArpack', '-fullGenLapack',
            see https://openseespydoc.readthedocs.io/en/latest/src/eigen.html.
        Returns
        -------
        None
        """
        # ----------------------------------
        self.get_model_data()
        self.reset_eigen_state()
        # ----------------------------------
        ops.wipeAnalysis()
        if mode_tag == 1:
            eigen_values = ops.eigen(solver, 2)[:1]
        else:
            eigen_values = ops.eigen(solver, mode_tag)
        omega = np.sqrt(eigen_values)
        f = omega / (2 * np.pi)
        self.eigen["f"] = f
        eigenvectors = []
        for mode_tag in range(1, mode_tag + 1):
            # ------------------------------------------
            eigen_vector = np.zeros((self.model_info["num_node"], 3))
            for i, Tag in enumerate(self.model_info["NodeTags"]):
                coord = ops.nodeCoord(Tag)
                eigen = ops.nodeEigenvector(Tag, mode_tag)
                if len(coord) == 1:
                    coord.extend([0, 0])
                    eigen.extend([0, 0])
                elif len(coord) == 2:
                    coord.extend([0])
                    eigen = eigen[:2]
                    eigen.extend([0])
                else:
                    eigen = eigen[:3]
                eigen_vector[i] = np.array(eigen)
            eigenvectors.append(eigen_vector)
        self.eigen["eigenvector"] = eigenvectors

        self.eigen.update(self.model_info)
        self.eigen.update(self.cells)
        # ----------------------------------------------------------------
        if not os.path.exists(self.out_dir):
            os.makedirs(self.out_dir)
        output_filename = self.out_dir + '/EigenData'
        with shelve.open(output_filename) as db:
            db["EigenInfo"] = self.eigen

    def get_node_resp_step(self, analysis_tag: int, num_steps: int, model_update: bool = False):
        """Get the response data step by step. The data will saved to file ``NodeRespStepData-{analysis_tag}.dat``.

        Parameters
        ----------
        analysis_tag: int
            Analysis tag used to assign the analysis data.

        num_steps: int
            Total number of steps, must be set to determine when to save data.
        model_update: bool, default False
            whether to update the model domain data at each analysis step,
            this will be useful if model data has changed.

        Returns
        -------
        None

        Note
        ----
        You need to call this function at each analysis step in OpenSees.
        The advantage is that you can modify the iterative algorithm at each analysis step to facilitate convergence.
        """

        if model_update:
            self.get_model_data()
        else:
            if not self.get_model_data_finished:
                self.get_model_data()

        num_node = self.model_info["num_node"]
        # num_ele = self.num_ele
        node_tags = self.model_info["NodeTags"]
        # EleTags = self.EleTags
        # Used to store the response data of each node at each time step,
        # the index is time step, node, coordinate dimension
        node_disp = np.zeros((num_node, 3))
        node_vel = np.zeros((num_node, 3))
        node_accel = np.zeros((num_node, 3))
        # Used to store the deformed coordinate data of each node at each time step,
        # the index is time step, node, coordinate dimension
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
                coord.extend([0])
                disp = disp[:2]
                disp.extend([0])
                vel = vel[:2]
                vel.extend([0])
                accel = accel[:2]
                accel.extend([0])
            else:
                disp = disp[:3]  # ignore the rotation
                vel = vel[:3]
                accel = disp[:3]
            node_disp[i] = disp
            node_vel[i] = vel
            node_accel[i] = accel
            node_deform_coord[i] = [disp[ii] + coord[ii] for ii in range(3)]

        self.node_resp_steps["disp"].append(node_disp)
        self.node_resp_steps["vel"].append(node_vel)
        self.node_resp_steps["accel"].append(node_accel)
        self.model_update = model_update
        if model_update:
            for name in self.model_info_names:
                self.model_info_steps[name].append(self.model_info[name])
            for name in self.cells_names:
                self.cells_steps[name].append(self.cells[name])
        else:
            if self.step_node_track == 0:
                self.model_info_steps.update(self.model_info)
                self.cells_steps.update(self.cells)

        # ----------------------------------------------------------------
        self.step_node_track += 1
        if self.step_node_track == num_steps:
            if not os.path.exists(self.out_dir):
                os.makedirs(self.out_dir)
            output_filename = self.out_dir + f'/NodeRespStepData-{analysis_tag}'
            with shelve.open(output_filename) as db:
                db["ModelInfoSteps"] = self.model_info_steps
                db["CellSteps"] = self.cells_steps
                db["NodeRespSteps"] = self.node_resp_steps

    def get_frame_resp_step(self, analysis_tag: int, num_steps: int):
        """Get the response data step by step. The data will saved to file ``BeamRespStepData-{analysis_tag}.dat``.

        Parameters
        ----------
        analysis_tag: int
            Analysis tag used to assign the analysis data.

        num_steps: int
            Total number of steps, must be set to determine when to save data.

        Returns
        -------
        None

        Note
        ----
        You need to call this function at each analysis step in OpenSees.
        The advantage is that you can modify the iterative algorithm at each analysis step to facilitate convergence.
        """
        ele_tags = ops.getEleTags()
        ele_tags.sort()

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
        beam_cell_map = dict()
        xlocal_map = dict()
        ylocal_map = dict()
        zlocal_map = dict()
        for i, eletag in enumerate(beam_tags):
            node1, node2 = beam_node_map[eletag]
            idx_i, idx_j = node_coord_map[node1], node_coord_map[node2]
            beam_cells.append([2, idx_i, idx_j])
            beam_cell_map[eletag] = i
            xlocal = ops.eleResponse(eletag, "xlocal")
            ylocal = ops.eleResponse(eletag, "ylocal")
            zlocal = ops.eleResponse(eletag, "zlocal")
            xlocal_map[eletag] = np.array(xlocal)
            ylocal_map[eletag] = np.array(ylocal)
            zlocal_map[eletag] = np.array(zlocal)
        beam_cells = np.array(beam_cells)

        bounds = np.array(ops.nodeBounds())

        self.beam_infos['beam_tags'] = beam_tags
        self.beam_infos['beam_node_coords'] = beam_node_coords
        self.beam_infos['beam_cells'] = beam_cells
        self.beam_infos['beam_cell_map'] = beam_cell_map
        self.beam_infos['xlocal'] = xlocal_map
        self.beam_infos['ylocal'] = ylocal_map
        self.beam_infos['zlocal'] = zlocal_map
        self.beam_infos['bounds'] = bounds

        beam_resp_steps = []
        for eletag in beam_tags:
            local_forces = ops.eleResponse(eletag, "localForce")
            if len(local_forces) == 6:
                local_forces = [local_forces[0], local_forces[1], 0, 0, 0, local_forces[2],
                                local_forces[3], local_forces[4], 0, 0, 0, local_forces[5]]
            beam_resp_steps.append(local_forces)
        beam_resp_steps = np.array(beam_resp_steps)
        self.beam_resp_step['localForces'].append(beam_resp_steps)

        # ----------------------------------------------------------------
        self.step_beam_track += 1
        if self.step_beam_track == num_steps:
            if not os.path.exists(self.out_dir):
                os.makedirs(self.out_dir)
            output_filename = self.out_dir + f'/BeamRespStepData-{analysis_tag}'
            with shelve.open(output_filename) as db:
                db["BeamInfos"] = self.beam_infos
                db["BeamRespSteps"] = self.beam_resp_step

    def get_fiber_data(self, ele_sec: list[tuple[int, int]]):
        """Get data from the section assigned by parameter ele_sec.
        The data will saved to file ``FiberData.dat``.

        Parameters
        ----------
        ele_sec: list[tuple[int, int]]
            A list or tuple composed of element tag and sectag.
            e.g., [(ele1, sec1), (ele2, sec2), ... , (elen, secn)],
            The section is attached to an element in the order from end i to end j of that element.

        Returns
        -------
        None
        """
        self.fiber_sec_tags = ele_sec
        for ele_sec_i in ele_sec:
            key = f"{ele_sec_i[0]}-{ele_sec_i[1]}"
            self.fiber_sec_data[key] = None

        # get data
        for ele_sec_i in self.fiber_sec_tags:
            ele_tag = ele_sec_i[0]
            sec_tag = ele_sec_i[1]
            key = f"{ele_sec_i[0]}-{ele_sec_i[1]}"
            fiber_data = _get_fiber_sec_data(ele_tag, sec_tag)
            self.fiber_sec_data[key] = fiber_data
        if not os.path.exists(self.out_dir):
            os.makedirs(self.out_dir)
        output_filename = self.out_dir + '/FiberData'
        with shelve.open(output_filename) as db:
            db["Fiber"] = self.fiber_sec_data
        return self.fiber_sec_data

    def get_fiber_resp_step(self, analysis_tag: int, num_steps: int):
        """Get analysis step data for fiber section.
        The data will saved to file ``FiberRespStepData-{analysis_tag}.dat``.

        Parameters
        ----------
        analysis_tag: int

        num_steps: int
            Total number of steps, must be set after output_file is set to determine when to save data.

        Returns
        -------
        None
        """
        if not self.fiber_sec_data:
            raise ValueError(
                "Run get_fiber_step_data must run get_fiber_data() in advance!"
            )
        if self.step_fiber_track == 0:
            for ele_sec_i in self.fiber_sec_tags:
                key = f"{ele_sec_i[0]}-{ele_sec_i[1]}"
                self.fiber_sec_step_data[key] = []

        for ele_sec_i in self.fiber_sec_tags:
            ele_tag = ele_sec_i[0]
            sec_tag = ele_sec_i[1]
            key = f"{ele_sec_i[0]}-{ele_sec_i[1]}"
            fiber_data = _get_fiber_sec_data(ele_tag, sec_tag)
            defo_fo = ops.eleResponse(ele_tag, "section", sec_tag, "forceAndDeformation")
            if len(defo_fo) == 6:
                defo_fo = [defo_fo[0], defo_fo[1], 0., defo_fo[2],
                           defo_fo[3], defo_fo[4], 0., defo_fo[5]]
            sec_defo_fo = np.array([defo_fo] * fiber_data.shape[0], dtype=float)
            data = np.hstack([fiber_data, sec_defo_fo])
            self.fiber_sec_step_data[key].append(data)
        # ----------------------------------------------------------------
        self.step_fiber_track += 1
        if self.step_fiber_track == num_steps:
            if not os.path.exists(self.out_dir):
                os.makedirs(self.out_dir)
            output_filename = self.out_dir + f'/FiberRespStepData-{analysis_tag}'
            with shelve.open(output_filename) as db:
                db["FiberRespSteps"] = self.fiber_sec_step_data


def _get_fiber_sec_data(ele_tag: int, sec_tag: int = 1) -> ArrayLike:
    """Get the fiber sec data for a beam element.

    Parameters
    ----------
    ele_tag: int
        The element tag to which the section is to be displayed.
    sec_tag: int
        Which integration point section is displayed, tag from 1 from segment i to j.

    Returns
    -------
    fiber_data: ArrayLike
    """
    # Extract fiber data using eleResponse() command
    fiber_data = ops.eleResponse(ele_tag, "section", sec_tag, "fiberData2")
    if len(fiber_data) == 0:
        fiber_data = ops.eleResponse(ele_tag, "section", "fiberData2")
    # From column 1 to 6: "yCoord", "zCoord", "area", 'mat', "stress", "strain"
    fiber_data = np.array(fiber_data).reshape((-1, 6))  # 变形为6列数组
    return fiber_data


def sort_xy(x, y):
    """
    Sort points counterclockwise
    """
    x0 = np.mean(x)
    y0 = np.mean(y)
    r = np.sqrt((x - x0) ** 2 + (y - y0) ** 2)
    angles = np.where(
        (y - y0) >= 0, np.arccos((x - x0) / r), 4 * np.pi - np.arccos((x - x0) / r)
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
