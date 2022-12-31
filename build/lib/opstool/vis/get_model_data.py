import os
import h5py
import numpy as np
import openseespy.opensees as ops
from typing import Union
from numpy.typing import ArrayLike

from ..utils import (ELE_TAG_Beam, ELE_TAG_Link,
                     ELE_TAG_Tetrahedron, ELE_TAG_Truss)
from ..utils import check_file


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
        if not os.path.exists(self.out_dir):
            os.makedirs(self.out_dir)

        self.model_info = dict()
        self.get_model_data_finished = False

        # Initialize cell connection data
        self.cells = dict()

        # Initialize eigenvalue data
        self.eigen = None

        # Analysis step model update data
        self.model_info_steps = dict()
        # Ele connection update data
        self.cells_steps = dict()
        # Update node response data
        self.node_resp_names = ("disp", "vel", "accel")
        self.node_resp_steps = dict()
        self.step_node_track = 0

        self.beam_infos = dict()
        self.beam_resp_names = ['localForces']
        # 'basicDeformations'
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
        for name in self.model_info.keys():
            self.model_info[name] = None
        for name in self.cells.keys():
            self.cells[name] = None

    def reset_eigen_state(self):
        """Reset the state of results extract of eigen data."""
        self.eigen = dict()
        for name in self.eigen.keys():
            self.eigen[name] = None

    def _reset_model_step(self):
        for name in self.model_info.keys():
            self.model_info_steps[name] = []
        for name in self.cells.keys():
            self.cells_steps[name] = []
        self.model_info_steps['step_track'] = 0
        self.cells_steps['step_track'] = 0

    def _reset_node_resp(self):
        self.step_node_track = 0
        for name in self.node_resp_names:
            self.node_resp_steps[name] = []

    def _reset_beam_step(self):
        self.step_beam_track = 0
        for name in self.beam_infos.keys():
            self.beam_infos[name] = None
        for name in self.beam_resp_names:
            self.beam_resp_step[name] = []

    def _reset_fiber_step(self):
        self.step_fiber_track = 0
        self.fiber_sec_step_data = dict()

    def reset_steps_state(self):
        """Reset the state of results extract in analysis step.

        .. important::
            As the data is saved in the loop analysis using the list append method,
            it is important to clear the data from previous analysis case before each analysis loop.
        """

        self._reset_model_step()
        self._reset_node_resp()
        self._reset_beam_step()
        self._reset_fiber_step()

        # Truss Element Analysis Step Response Data

        # Beam Element Analysis Step Response Data

    def get_model_data(self, save_file: Union[str, bool] = "ModelData.hdf5"):
        """Get data from the current model domain.
        The data will saved to file ``results_dir`` + ``save_file``.

        Parameters
        -----------
        save_file: str, default="ModelData.hdf5"
            The file name that data saved.
            If None of False, the data will not be saved.

            .. warning::
                Be careful not to include any path, only filename,
                the file will be saved to the directory ``results_dir``.

        """
        if save_file:
            check_file(save_file, ['.hdf5', '.h5', '.he5'])
        # --------------------------------
        node_tags = ops.getNodeTags()
        # node_tags.sort()
        num_node = len(node_tags)
        # Get all the ele tags
        ele_tags = ops.getEleTags()
        # ele_tags.sort()
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
            node_coords[i] = coord
            node_index[Tag] = i
        points = node_coords

        fixed_nodes = ops.getFixedNodes()
        fixed_dofs = []
        for tag in fixed_nodes:
            fixeddofs = ops.getFixedDOFs(tag)
            fixities = [0] * 6
            for dof in fixeddofs:
                fixities[dof - 1] = -1
            fixed_dofs.append(fixities)
        fixed_dofs = np.array(fixed_dofs)

        # lines and faces
        # How the ele is connected，node number n-node tag 1-node tag 2-...-node tag n
        # -----------------
        truss_cells = []
        truss_cells_tags = []
        # -----------------
        link_cells = []
        link_cells_tags = []
        link_midpoints = []
        link_xlocal = []
        link_ylocal = []
        link_zlocal = []
        # ------------------
        beam_cells = []
        beam_cells_tags = []
        beam_midpoints = []
        beam_xlocal = []
        beam_ylocal = []
        beam_zlocal = []
        # -----------------------
        other_line_cells = []
        other_line_cells_tags = []
        all_lines_cells = []
        all_lines_cells_tags = []
        # --------------------
        plane_cells = []
        plane_cells_tags = []
        # ------------------------
        tetrahedron_cells = []
        tetrahedron_cells_tags = []
        # -----------------------------
        brick_cells = []
        brick_cells_tags = []
        # -----------------------------
        all_faces_cells = []
        all_faces_cells_tags = []
        # ------------------------------
        ele_midpoints = []  # the coordinates of the ele's midpoint
        for i, ele in enumerate(ele_tags):
            ele_nodes = ops.eleNodes(ele)
            # Determine the element type based on the number of element nodes
            if len(ele_nodes) == 2:
                node_i, node_j = ele_nodes
                idx_i, idx_j = node_index[node_i], node_index[node_j]
                all_lines_cells.extend([2, idx_i, idx_j])
                all_lines_cells_tags.append(ele)
                if ops.getEleClassTags(ele)[0] in ELE_TAG_Truss:
                    truss_cells.extend([2, idx_i, idx_j])
                    truss_cells_tags.append(ele)
                elif ops.getEleClassTags(ele)[0] in ELE_TAG_Link:
                    link_cells.extend([2, idx_i, idx_j])
                    link_cells_tags.append(ele)
                    link_midpoints.append((node_coords[idx_i] + node_coords[idx_j]) / 2)
                    xlocal = ops.eleResponse(ele, "xlocal")
                    ylocal = ops.eleResponse(ele, "ylocal")
                    zlocal = ops.eleResponse(ele, "zlocal")
                    link_xlocal.append(np.array(xlocal) / np.linalg.norm(xlocal))
                    link_ylocal.append(np.array(ylocal) / np.linalg.norm(ylocal))
                    link_zlocal.append(np.array(zlocal) / np.linalg.norm(zlocal))
                elif ops.getEleClassTags(ele)[0] in ELE_TAG_Beam:
                    beam_cells.extend([2, idx_i, idx_j])
                    beam_cells_tags.append(ele)
                    beam_midpoints.append((node_coords[idx_i] + node_coords[idx_j]) / 2)
                    xlocal = ops.eleResponse(ele, "xlocal")
                    ylocal = ops.eleResponse(ele, "ylocal")
                    zlocal = ops.eleResponse(ele, "zlocal")
                    beam_xlocal.append(np.array(xlocal) / np.linalg.norm(xlocal))
                    beam_ylocal.append(np.array(ylocal) / np.linalg.norm(ylocal))
                    beam_zlocal.append(np.array(zlocal) / np.linalg.norm(zlocal))
                else:
                    other_line_cells.extend([2, idx_i, idx_j])
                    other_line_cells_tags.append(ele)
                ele_midpoints.append((node_coords[idx_i] + node_coords[idx_j]) / 2)

            elif len(ele_nodes) == 3 or len(ele_nodes) == 6:
                if len(ele_nodes) == 3:
                    node_i, node_j, node_k = ops.eleNodes(ele)
                else:
                    node_i, node_j, node_k = ops.eleNodes(ele)[1], ops.eleNodes(ele)[3], ops.eleNodes(ele)[5]
                idx_i, idx_j, idx_k = (
                    node_index[node_i],
                    node_index[node_j],
                    node_index[node_k],
                )
                all_faces_cells.extend([3, idx_i, idx_j, idx_k])
                all_faces_cells_tags.append(ele)
                plane_cells.extend([3, idx_i, idx_j, idx_k])
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
                    tetrahedron_cells.extend([3, idx_i, idx_j, idx_k])
                    tetrahedron_cells.extend([3, idx_i, idx_j, idx_l])
                    tetrahedron_cells.extend([3, idx_i, idx_k, idx_l])
                    tetrahedron_cells.extend([3, idx_j, idx_k, idx_l])
                    tetrahedron_cells_tags.append(ele)
                    all_faces_cells.extend([3, idx_i, idx_j, idx_k])
                    all_faces_cells.extend([3, idx_i, idx_j, idx_l])
                    all_faces_cells.extend([3, idx_i, idx_k, idx_l])
                    all_faces_cells.extend([3, idx_j, idx_k, idx_l])
                    all_faces_cells_tags.append(ele)
                else:
                    plane_cells.extend([4, idx_i, idx_j, idx_k, idx_l])
                    plane_cells_tags.append(ele)
                    all_faces_cells.extend([4, idx_i, idx_j, idx_k, idx_l])
                    all_faces_cells_tags.append(ele)
                ele_midpoints.append(np.mean(node_coords[[idx_i, idx_j, idx_k, idx_l]], axis=0))

            elif len(ele_nodes) == 8 or len(ele_nodes) == 20:
                eleNodes = ops.eleNodes(ele)[0:8]
                tag_list = [node_index[node_] for node_ in eleNodes]
                temp_points = np.array([node_coords[i] for i in tag_list])
                idxxx = np.argsort(temp_points[:, -1])
                temp_points = temp_points[idxxx]
                tag_list = np.array(tag_list)[idxxx]
                temp_points = [tuple(i) for i in temp_points]
                tag_list = list(tag_list)
                tag_counter1 = counter_clockwise(temp_points[:4], tag_list[:4])
                tag_counter2 = counter_clockwise(temp_points[4:], tag_list[4:])
                tag_counts = tag_counter1 + tag_counter2
                idx1, idx2, idx3, idx4, idx5, idx6, idx7, idx8 = tag_counts
                brick_cells.extend([4, idx1, idx4, idx3, idx2])
                brick_cells.extend([4, idx5, idx6, idx7, idx8])
                brick_cells.extend([4, idx1, idx5, idx8, idx4])
                brick_cells.extend([4, idx2, idx3, idx7, idx6])
                brick_cells.extend([4, idx1, idx2, idx6, idx5])
                brick_cells.extend([4, idx3, idx4, idx8, idx7])
                brick_cells_tags.append(ele)
                all_faces_cells.extend([4, idx1, idx4, idx3, idx2])
                all_faces_cells.extend([4, idx5, idx6, idx7, idx8])
                all_faces_cells.extend([4, idx1, idx5, idx8, idx4])
                all_faces_cells.extend([4, idx2, idx3, idx7, idx6])
                all_faces_cells.extend([4, idx1, idx2, idx6, idx5])
                all_faces_cells.extend([4, idx3, idx4, idx8, idx7])
                all_faces_cells_tags.append(ele)
                idxs1_8 = [idx1, idx2, idx3, idx4, idx5, idx6, idx7, idx8]
                ele_midpoints.append(np.mean(node_coords[idxs1_8], axis=0))
        ele_midpoints = np.array(ele_midpoints)
        beam_midpoints = np.array(beam_midpoints)
        beam_xlocal = np.array(beam_xlocal)
        beam_ylocal = np.array(beam_ylocal)
        beam_zlocal = np.array(beam_zlocal)
        link_midpoints = np.array(link_midpoints)
        link_xlocal = np.array(link_xlocal)
        link_ylocal = np.array(link_ylocal)
        link_zlocal = np.array(link_zlocal)

        # Automatically determine the coordinate axis boundary
        # according to the model node coordinates
        min_node = np.min(points, axis=0)
        max_node = np.max(points, axis=0)
        space = (max_node - min_node) / 10
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

        # FEM data
        model_info = dict()
        model_info["coord_no_deform"] = points
        model_info["coord_ele_midpoints"] = ele_midpoints
        model_info["bound"] = bounds
        model_info["max_bound"] = max_bound
        model_info["num_node"] = num_node
        model_info["num_ele"] = num_ele
        model_info["NodeTags"] = node_tags
        model_info["FixNodeTags"] = fixed_nodes
        model_info["FixNodeDofs"] = fixed_dofs
        model_info["EleTags"] = ele_tags
        model_info["model_dims"] = model_dims
        model_info["coord_ele_midpoints"] = ele_midpoints
        model_info["beam_midpoints"] = beam_midpoints
        model_info["beam_xlocal"] = beam_xlocal
        model_info["beam_ylocal"] = beam_ylocal
        model_info["beam_zlocal"] = beam_zlocal
        model_info["link_midpoints"] = link_midpoints
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

        self.model_info.update(model_info)
        self.cells.update(cells)

        self.get_model_data_finished = True

        # if save_file:
        #     output_filename = self.out_dir + '/ModelData'
        #     with shelve.open(output_filename) as db:
        #         db["ModelInfo"] = self.model_info
        #         db["Cell"] = self.cells
        #     print(f"Model data saved in {output_filename}!")
        if save_file:
            output_filename = self.out_dir + '/' + save_file
            with h5py.File(output_filename, "w") as f:
                grp1 = f.create_group("ModelInfo")
                for name, value in self.model_info.items():
                    grp1.create_dataset(name, data=value)
                grp2 = f.create_group("Cell")
                for name, value in self.cells.items():
                    grp2.create_dataset(name, data=value)
            print(f"Model data saved in {output_filename} !")

    def get_eigen_data(
        self,
        mode_tag: int = 1,
        solver: str = "-genBandArpack",
        save_file: str = 'EigenData.hdf5',
    ):
        """Get eigenvalue Analysis Data.
        The data will saved to file ``results_dir`` + ``save_file``.

        Parameters
        ----------
        mode_tag: int
            mode tag.
        solver: str, default '-genBandArpack'
            type of solver, optional '-genBandArpack', '-fullGenLapack',
            see https://openseespydoc.readthedocs.io/en/latest/src/eigen.html.
        save_file: str, default='EigenData.hdf5'
            The file name that data saved.
            If None of False, the data will not be saved.

            .. warning::
                Be careful not to include any path, only filename,
                the file will be saved to the directory ``results_dir``.

        Returns
        -------
        None
        """
        # ----------------------------------
        if save_file:
            check_file(save_file, ['.hdf5', '.h5', '.he5'])
        self.get_model_data(save_file=False)
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
                    if len(eigen) == 3 or len(eigen) == 2:
                        eigen = eigen[:2]
                        eigen.extend([0])
                    elif len(eigen) == 1:
                        eigen.extend([0, 0])
                else:
                    eigen = eigen[:3]
                eigen_vector[i] = np.array(eigen)
            eigenvectors.append(eigen_vector)
        self.eigen["eigenvector"] = eigenvectors

        self.eigen.update(self.model_info)
        self.eigen.update(self.cells)
        # ----------------------------------------------------------------
        # output_filename = self.out_dir + '/EigenData'
        # with shelve.open(output_filename) as db:
        #     db["EigenInfo"] = self.eigen
        if save_file:
            output_filename = self.out_dir + '/' + save_file
            with h5py.File(output_filename, "w") as f:
                grp = f.create_group("EigenInfo")
                for name, value in self.eigen.items():
                    grp.create_dataset(name, data=value)
            print(f"Eigen data saved in {output_filename} !")

    def get_node_resp_step(self,
                           num_steps: int = 100000000000,
                           total_time: float = 100000000000,
                           stop_cond: bool = False,
                           save_file: str = "NodeRespStepData-1.hdf5",
                           model_update: bool = False):
        """Get the node response data step by step.

        .. note::
            You need to call this function at each analysis step in OpenSees.
            The advantage is that you can modify the iterative algorithm at
            each analysis step to facilitate convergence.

        Parameters
        -----------------
        num_steps: int, default=100000000000
            Total number of steps, set to determine when to save data.
        total_time: float, default=100000000000
            Total analysis time, set to determine when to save data.
            You can specify one of the parameters *num_steps* and `total_time`.
            If both are used, it depends on which one arrives first.
        stop_cond: bool, default = False
            Condition used to determine when data is saved
            if ``num_steps`` and ``total_time`` unavailable.
            For example, stop_cond = ops.nodeDisp(nodeTag, 1) >= 0.1, i.e., once the displacement of node
            with tag nodeTag and dof 1 is greater than 0.1, the loop is terminated to save the data.
        save_file: str, default='NodeRespStepData-1.hdf5'
            The file name that data saved.
            If None of False, the data will not be saved.

            .. warning::
                Be careful not to include any path, only filename,
                the file will be saved to the directory ``results_dir``.
                You need to specify different suffixes to distinguish between the different analysis cases.
                Such as "NodeRespStepData-1.hdf5", "NodeRespStepData-2.hdf5", etc.

        model_update: bool, default False
            whether to update the model domain data at each analysis step,
            this will be useful if model data has changed.
            For example, some elements and nodes were removed.

        Returns
        -------
        None
        """
        if save_file:
            check_file(save_file, ['.hdf5', '.h5', '.he5'])
        if model_update:
            self.get_model_data(save_file=False)
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

        self.node_resp_steps["disp"].append(node_disp)
        self.node_resp_steps["vel"].append(node_vel)
        self.node_resp_steps["accel"].append(node_accel)
        if model_update:
            if self.step_node_track == self.model_info_steps['step_track']:
                for name in self.model_info.keys():
                    self.model_info_steps[name].append(self.model_info[name])
                self.model_info_steps['step_track'] += 1
            if self.step_node_track == self.cells_steps['step_track']:
                for name in self.cells.keys():
                    self.cells_steps[name].append(self.cells[name])
                self.cells_steps['step_track'] += 1
        else:
            if self.step_node_track == 0:
                self.model_info_steps.update(self.model_info)
                self.cells_steps.update(self.cells)
        # --------------------------------
        self.model_update = model_update
        self.step_node_track += 1
        # --------------------------------
        if save_file:
            if self.step_node_track >= num_steps or ops.getTime() >= total_time or stop_cond:
                output_filename = self.out_dir + '/' + save_file
                with h5py.File(output_filename, "w") as f:
                    n = len(self.node_resp_steps['disp'])
                    f.create_dataset("Nsteps", data=n)
                    grp1 = f.create_group("ModelInfoSteps")
                    grp2 = f.create_group("CellSteps")
                    grp3 = f.create_group("NodeRespSteps")
                    for name, value in self.model_info_steps.items():
                        if name not in ['step_track']:
                            if model_update:
                                subgrp = grp1.create_group(name)
                                for i in range(n):
                                    subgrp.create_dataset(f"step{i + 1}", data=value[i])
                            else:
                                grp1.create_dataset(name, data=value)
                    for name, value in self.cells_steps.items():
                        if name not in ['step_track']:
                            if model_update:
                                subgrp = grp2.create_group(name)
                                for i in range(n):
                                    subgrp.create_dataset(f"step{i + 1}", data=value[i])
                            else:
                                grp2.create_dataset(name, data=value)
                    for name, value in self.node_resp_steps.items():
                        subgrp = grp3.create_group(name)
                        for i in range(n):
                            subgrp.create_dataset(f"step{i + 1}", data=value[i])
                print(f"Node response data saved in {output_filename}!")

    def get_frame_resp_step(self,
                            num_steps: int = 100000000000,
                            total_time: float = 100000000000,
                            stop_cond: bool = False,
                            save_file: str = "BeamRespStepData-1.hdf5"
                            ):
        """Get the response data step by step.
        .. note::
            You need to call this function at each analysis step in OpenSees.
            The advantage is that you can modify the iterative algorithm at
            each analysis step to facilitate convergence.

        Parameters
        ----------
        num_steps: int, default=100000000000
            Total number of steps, set to determine when to save data.
        total_time: float, default=100000000000
            Total analysis time, set to determine when to save data.
            You can specify one of the parameters *num_steps* and `total_time`.
            If both are used, it depends on which one arrives first.
        stop_cond: bool, default = False
            Condition used to determine when data is saved
            if ``num_steps`` and ``total_time`` unavailable.
            For example, stop_cond = ops.nodeDisp(nodeTag, 1) >= 0.1, i.e., once the displacement of node
            with tag nodeTag and dof 1 is greater than 0.1, the loop is terminated to save the data.
        save_file: str, default='BeamRespStepData-1.hdf5'
            The file name that data saved.
            If None of False, the data will not be saved.

            .. warning::
                Be careful not to include any path, only filename,
                the file will be saved to the directory ``results_dir``.
                You need to specify different suffixes to distinguish between the different analysis cases.
                Such as "BeamRespStepData-1.hdf5", "BeamRespStepData-2.hdf5", etc.

        Returns
        -------
        None
        """
        if save_file:
            check_file(save_file, ['.hdf5', '.h5', '.he5'])
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

        self.beam_infos['beam_tags'] = beam_tags
        self.beam_infos['beam_node_coords'] = beam_node_coords
        self.beam_infos['beam_cells'] = beam_cells
        self.beam_infos['xlocal'] = xlocals
        self.beam_infos['ylocal'] = ylocals
        self.beam_infos['zlocal'] = zlocals
        self.beam_infos['bounds'] = bounds

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
        self.beam_resp_step['localForces'].append(beam_resp_steps)
        # ----------------------------------------------------------------
        self.step_beam_track += 1
        # ------------------------------------------
        if save_file:
            if self.step_beam_track >= num_steps or ops.getTime() >= total_time or stop_cond:
                output_filename = self.out_dir + '/' + save_file
                with h5py.File(output_filename, "w") as f:
                    n = len(self.beam_resp_step['localForces'])
                    f.create_dataset("Nsteps", data=n)
                    grp1 = f.create_group("BeamInfos")
                    grp2 = f.create_group("BeamRespSteps")
                    for name, value in self.beam_infos.items():
                        grp1.create_dataset(name, data=value)
                    for name, value in self.beam_resp_step.items():
                        subgrp = grp2.create_group(name)
                        for i in range(n):
                            subgrp.create_dataset(f"step{i + 1}", data=value[i])
                print(f"Frame elements response data saved in {output_filename}!")

    def get_fiber_data(self, ele_sec: list[tuple[int, int]], save_file: str = 'FiberData.hdf5'):
        """Get data from the section assigned by parameter ele_sec.

        Parameters
        ----------
        ele_sec: list[tuple[int, int]]
            A list or tuple composed of element tag and sectag.
            e.g., [(ele1, sec1), (ele2, sec2), ... , (elen, secn)],
            The section is attached to an element in the order from end i to end j of that element.
        save_file: str, default='FiberData.hdf5'
            The file name that data saved.
            If None of False, the data will not be saved.

            .. warning::
                Be careful not to include any path, only filename,
                the file will be saved to the directory ``results_dir``.

        Returns
        -------
        None
        """
        if save_file:
            check_file(save_file, ['.hdf5', '.h5', '.he5'])
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
        # ---------------------------------------------
        if save_file:
            output_filename = self.out_dir + '/' + save_file
            with h5py.File(output_filename, "w") as f:
                for name, value in self.fiber_sec_data.items():
                    f.create_dataset(name, data=value)
            print(f"Fiber section data saved in {output_filename}!")

    def get_fiber_resp_step(self,
                            num_steps: int = 100000000000,
                            total_time: float = 100000000000,
                            stop_cond: bool = False,
                            save_file: str = "FiberRespStepData-1.hdf5"):
        """Get analysis step data for fiber section.

        Parameters
        ----------
        num_steps: int, default=100000000000
            Total number of steps, set to determine when to save data.
        total_time: float, default=100000000000
            Total analysis time, set to determine when to save data.
            You can specify one of the parameters *num_steps* and `total_time`.
            If both are used, it depends on which one arrives first.
        stop_cond: bool, default = False
            Condition used to determine when data is saved
            if ``num_steps`` and ``total_time`` unavailable.
            For example, stop_cond = ops.nodeDisp(nodeTag, 1) >= 0.1, i.e., once the displacement of node
            with tag nodeTag and dof 1 is greater than 0.1, the loop is terminated to save the data.
        save_file: str, default='FiberRespStepData-1.hdf5'
            The file name that data saved.
            If None of False, the data will not be saved.

            .. warning::
                Be careful not to include any path, only filename,
                the file will be saved to the directory ``results_dir``.
                You need to specify different suffixes to distinguish between the different analysis cases.
                Such as "FiberRespStepData-1.hdf5", "FiberRespStepData-2.hdf5", etc.

        Returns
        -------
        None
        """
        if save_file:
            check_file(save_file, ['.hdf5', '.h5', '.he5'])
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
        # ------------------------
        self.step_fiber_track += 1
        # ------------------------
        if save_file:
            if self.step_fiber_track >= num_steps or ops.getTime() >= total_time or stop_cond:
                output_filename = self.out_dir + '/' + save_file
                with h5py.File(output_filename, "w") as f:
                    f.create_dataset("Nsteps", data=self.step_fiber_track)
                    grp = f.create_group("FiberRespSteps")
                    for name, value in self.fiber_sec_step_data.items():
                        subgrp = grp.create_group(name)
                        for i in range(self.step_fiber_track):
                            subgrp.create_dataset(f"step{i + 1}", data=value[i])
                print(f"Fiber section responses data saved in {output_filename}!")


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


def _lines_angle(v1, v2):
    # return np.arctan2(np.linalg.norm(np.cross(v1, v2)), np.dot(v1, v2))
    x = np.array(v1)
    y = np.array(v2)
    l_x = np.sqrt(x.dot(x))
    l_y = np.sqrt(y.dot(y))
    cos_ = x.dot(y) / (l_x * l_y)
    angle_r = np.arccos(cos_)
    return angle_r
