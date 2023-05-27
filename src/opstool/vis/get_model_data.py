from __future__ import annotations

import os
from itertools import cycle
from typing import Union

import h5py
import numpy as np
import openseespy.opensees as ops
from rich import print

from ..utils import check_file
from ._get_model_base import (
    get_beam_info2,
    get_beam_resp,
    get_model_info,
    get_node_coords,
    get_node_react,
    get_node_resp,
    get_fiber_sec_data,
)


class GetFEMdata:
    """
    Get the data in the ``openseespy`` current domain.

    Parameters
    ----------
    results_dir: str, default="opstool_output"
        The directory that results to save.
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
        self.eigen = dict()

        # Analysis step model update data
        self.model_info_steps = dict()
        # Ele connection update data
        self.cells_steps = dict()
        # Update node response data
        self.node_resp_names = ("disp", "vel", "accel")
        self.node_resp_steps = dict()
        self.step_node_track = 0
        # node reactions
        self.node_react_steps = []
        self.step_react_track = 0

        self.beam_infos = dict()
        self.beam_resp_names = ["localForces"]
        # 'basicDeformations'
        self.beam_resp_step = dict()
        # ["N_1", "Vy_1", "Vz_1", "T_1", "My_1", "Mz_1",
        #  "N_2", "Vy_2", "Vz_2", "T_2", "My_2", "Mz_2"]
        # ["eps", "thetaZ_1", "thetaZ_2", "thetaY_1", "thetaY_2", "thetaX"]
        self.step_beam_track = 0

        # On/Off and Tracking for Model Updates
        self.model_update = False
        self.resp_step_track = 0

        # self.reset_model_state()
        # self.reset_eigen_state()
        self.reset_steps_state()

        # fiber section data
        self.fiber_sec_tags = []
        self.fiber_sec_data = dict()
        self.fiber_sec_step_data = dict()
        self.step_fiber_track = 0

        # terminal print colors
        colors = [
            "#00aeff",
            "#3369e7",
            "#8e43e7",
            "#b84592",
            "#ff4f81",
            "#ff6c5f",
            "#ffc168",
            "#2dde98",
            "#1cc7d0",
            "#49a942",
        ]
        self.colors_cycle = cycle(colors)

    def reset_model_state(self):
        """Reset the state of results extract of model data."""
        for name in self.model_info.keys():
            self.model_info[name] = None
        for name in self.cells.keys():
            self.cells[name] = None

    def reset_eigen_state(self):
        """Reset the state of results extract of eigen data."""
        for name in self.eigen.keys():
            self.eigen[name] = None

    def _reset_model_step(self):
        for name in self.model_info.keys():
            self.model_info_steps[name] = []
        for name in self.cells.keys():
            self.cells_steps[name] = []
        self.model_info_steps["step_track"] = 0
        self.cells_steps["step_track"] = 0

    def _reset_node_react(self):
        self.step_react_track = 0
        self.node_react_steps = []

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
        self._reset_node_react()
        self._reset_node_resp()
        self._reset_beam_step()
        self._reset_fiber_step()
        self.resp_step_track = 0

        # Truss Element Analysis Step Response Data

        # Beam Element Analysis Step Response Data

    def get_model_data(
        self, beam_sec: dict = None, save_file: Union[str, bool] = "ModelData.hdf5"
    ):
        """Get data from the current model domain.
        The data will saved to file ``results_dir`` + ``save_file`` in hdf5 style.

        Parameters
        -----------
        beam_sec: dict, default=None
            Specifies the section geometry for some beam or truss elements for 3D rendering.
            Such as beam_sec={1: sec_mesh, 2: sec_mesh}, 1 and 2 are beam or truss tags,
            sec_mesh must be an instance of :py:class:`opstool.preprocessing.SecMesh`.
        save_file: str, default="ModelData.hdf5"
            The file name that data saved.
            If None of False, the data will not be saved.

            .. warning::
                Be careful not to include any path, only filename,
                the file will be saved to the directory ``results_dir``.

        """
        if save_file:
            check_file(save_file, [".hdf5", ".h5", ".he5"])
        # --------------------------------
        model_info, cells = get_model_info(sec_mesh=beam_sec)
        self.model_info.update(model_info)
        self.cells.update(cells)
        self.get_model_data_finished = True
        if save_file:
            output_filename = self.out_dir + "/" + save_file
            with h5py.File(output_filename, "w") as f:
                grp1 = f.create_group("ModelInfo")
                for name, value in self.model_info.items():
                    grp1.create_dataset(name, data=value)
                grp2 = f.create_group("Cell")
                for name, value in self.cells.items():
                    grp2.create_dataset(name, data=value)
            print(
                f"Model data saved in [bold {next(self.colors_cycle)}]{output_filename}[/]!"
            )

    def get_eigen_data(
        self,
        mode_tag: int = 1,
        solver: str = "-genBandArpack",
        save_file: str = "EigenData.hdf5",
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
            check_file(save_file, [".hdf5", ".h5", ".he5"])
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
        if save_file:
            output_filename = self.out_dir + "/" + save_file
            with h5py.File(output_filename, "w") as f:
                grp = f.create_group("EigenInfo")
                for name, value in self.eigen.items():
                    grp.create_dataset(name, data=value)
            print(
                f"Eigen data saved in [bold {next(self.colors_cycle)}]{output_filename}[/]!"
            )

    def get_node_react_step(
        self,
        dynamic: bool = False,
        rayleigh: bool = False,
        num_steps: int = 10000000000000,
        total_time: float = 10000000000000,
        stop_cond: bool = False,
        save_file: Union[str, bool] = "NodeReactionStepData-1.hdf5",
    ):
        """Get one step the node reactions data.

        Parameters
        ----------
        dynamic : bool, optional, by default False
            If True, include dynamic effects.
        rayleigh : bool, optional, by default False
            If True, iInclude rayleigh damping.
        num_steps: int, default=10000000000000
            Total number of steps, set to determine when to save data.
        total_time: float, default=10000000000000
            Total analysis time, set to determine when to save data.
            You can specify one of the parameters *num_steps* and `total_time`.
            If both are used, it depends on which one arrives first.
        stop_cond: bool, default = False
            Condition used to determine when data is saved
            if ``num_steps`` and ``total_time`` unavailable.
            For example, stop_cond = ops.nodeDisp(nodeTag, 1) >= 0.1, i.e., once the displacement of node
            with tag nodeTag and dof 1 is greater than 0.1, the loop is terminated to save the data.
        save_file: str, default='NodeReactionStepData-1.hdf5'
            The file name that data saved.
            If None of False, the data will not be saved.

            .. warning::
                Be careful not to include any path, only filename,
                the file will be saved to the directory ``results_dir``.
                You need to specify different suffixes to distinguish between the different analysis cases.
                Such as "NodeReactionStepData-1.hdf5", "NodeReactionStepData-2.hdf5", etc.
        """
        args = []
        if dynamic:
            args.append("-dynamic")
        if rayleigh:
            args.append("-rayleigh")
        ops.reactions(*args)
        fixed_nodes = ops.getFixedNodes()
        self.node_react_steps.append(get_node_react(fixed_nodes))
        self.step_react_track += 1
        # --------------------------------
        if save_file:
            if (
                self.step_node_track >= num_steps or
                ops.getTime() >= total_time or
                stop_cond
            ):
                output_filename = self.out_dir + "/" + save_file
                self._save_node_react_step(output_filename, "w")
                print(
                    f"Node reaction data saved in [bold {next(self.colors_cycle)}]{output_filename}[/]!"
                )

    def _save_node_react_step(self, filename: str, mode: str = "w"):
        _, _, model_dims, _ = get_node_coords()
        fixed_nodes = ops.getFixedNodes()
        node_coords = np.zeros((len(fixed_nodes), 3))
        for i, tag in enumerate(fixed_nodes):
            coord = ops.nodeCoord(tag)
            model_dim = len(coord)
            if model_dim == 1:
                coord.extend([0, 0])
            elif model_dim == 2:
                coord.extend([0])
            node_coords[i] = coord
        with h5py.File(filename, mode) as f:
            n = len(self.node_react_steps)
            if "Nsteps" not in f.keys():
                f.create_dataset("Nsteps", data=n)
            if "model_dims" not in f.keys():
                f.create_dataset("model_dims", data=model_dims)
            f.create_dataset("NodeReactCoords", data=node_coords)
            f.create_dataset("NodeReactTags", data=fixed_nodes)
            grp = f.create_group("NodeReactSteps")
            for i in range(n):
                grp.create_dataset(f"step{i + 1}", data=self.node_react_steps[i])

    def get_node_resp_step(
        self,
        num_steps: int = 10000000000000,
        total_time: float = 10000000000000,
        stop_cond: bool = False,
        save_file: Union[str, bool] = "NodeRespStepData-1.hdf5",
        model_update: bool = False,
    ):
        """Get the node response data one step.

        .. note::
            You need to call this function at each analysis step in OpenSees.
            The advantage is that you can modify the iterative algorithm at
            each analysis step to facilitate convergence.

        Parameters
        -----------------
        num_steps: int, default=10000000000000
            Total number of steps, set to determine when to save data.
        total_time: float, default=10000000000000
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
            check_file(save_file, [".hdf5", ".h5", ".he5"])
        if model_update:
            self.get_model_data(save_file=False)
        else:
            if not self.get_model_data_finished:
                self.get_model_data(save_file=False)

        node_tags = self.model_info["NodeTags"]
        (node_disp, node_vel, node_accel, node_deform_coord) = get_node_resp(node_tags)

        self.node_resp_steps["disp"].append(node_disp)
        self.node_resp_steps["vel"].append(node_vel)
        self.node_resp_steps["accel"].append(node_accel)

        if model_update:
            if self.step_node_track == 0:
                self._reset_model_step()
            if self.step_node_track == self.model_info_steps["step_track"]:
                for name in self.model_info.keys():
                    self.model_info_steps[name].append(self.model_info[name])
                self.model_info_steps["step_track"] += 1
            if self.step_node_track == self.cells_steps["step_track"]:
                for name in self.cells.keys():
                    self.cells_steps[name].append(self.cells[name])
                self.cells_steps["step_track"] += 1
        else:
            if self.step_node_track == 0:
                self.model_info_steps.update(self.model_info)
                self.cells_steps.update(self.cells)
        # --------------------------------
        self.model_update = model_update
        self.step_node_track += 1
        # --------------------------------
        if save_file:
            if (
                self.step_node_track >= num_steps or
                ops.getTime() >= total_time or
                stop_cond
            ):
                output_filename = self.out_dir + "/" + save_file
                self._save_node_resp_step(output_filename, "w")
                print(
                    f"Node response data saved in [bold {next(self.colors_cycle)}]{output_filename}[/]!"
                )

    def _save_node_resp_step(self, filename: str, mode: str = "w"):
        with h5py.File(filename, mode) as f:
            n = len(self.node_resp_steps["disp"])
            if "Nsteps" not in f.keys():
                f.create_dataset("Nsteps", data=n)
            grp1 = f.create_group("ModelInfoSteps")
            grp2 = f.create_group("CellSteps")
            grp3 = f.create_group("NodeRespSteps")
            for name, value in self.model_info_steps.items():
                if name not in ["step_track"]:
                    if self.model_update:
                        subgrp = grp1.create_group(name)
                        for i in range(n):
                            subgrp.create_dataset(f"step{i + 1}", data=value[i])
                    else:
                        grp1.create_dataset(name, data=value)
            for name, value in self.cells_steps.items():
                if name not in ["step_track"]:
                    if self.model_update:
                        subgrp = grp2.create_group(name)
                        for i in range(n):
                            subgrp.create_dataset(f"step{i + 1}", data=value[i])
                    else:
                        grp2.create_dataset(name, data=value)
            for name, value in self.node_resp_steps.items():
                subgrp = grp3.create_group(name)
                for i in range(n):
                    subgrp.create_dataset(f"step{i + 1}", data=value[i])

    def get_frame_resp_step(
        self,
        num_steps: int = 10000000000000,
        total_time: float = 10000000000000,
        stop_cond: bool = False,
        save_file: Union[str, bool] = "BeamRespStepData-1.hdf5",
    ):
        """Get the response data one step.

        .. note::
            You need to call this function at each analysis step in OpenSees.
            The advantage is that you can modify the iterative algorithm at
            each analysis step to facilitate convergence.

        Parameters
        ----------
        num_steps: int, default=10000000000000
            Total number of steps, set to determine when to save data.
        total_time: float, default=10000000000000
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
            check_file(save_file, [".hdf5", ".h5", ".he5"])

        (
            beam_tags,
            beam_node_coords,
            beam_cells,
            xlocals,
            ylocals,
            zlocals,
            bounds,
        ) = get_beam_info2()
        self.beam_infos["beam_tags"] = beam_tags
        self.beam_infos["beam_node_coords"] = beam_node_coords
        self.beam_infos["beam_cells"] = beam_cells
        self.beam_infos["xlocal"] = xlocals
        self.beam_infos["ylocal"] = ylocals
        self.beam_infos["zlocal"] = zlocals
        self.beam_infos["bounds"] = bounds

        beam_resp_steps = get_beam_resp(beam_tags)
        self.beam_resp_step["localForces"].append(beam_resp_steps)
        # ----------------------------------------------------------------
        self.step_beam_track += 1
        # ------------------------------------------
        if save_file:
            if (
                self.step_beam_track >= num_steps or
                ops.getTime() >= total_time or
                stop_cond
            ):
                output_filename = self.out_dir + "/" + save_file
                self._save_frame_resp_step(output_filename, "w")
                print(
                    f"Frame elements response data saved in [bold {next(self.colors_cycle)}]{output_filename}[/]!"
                )

    def _save_frame_resp_step(self, filename: str, mode: str = "w"):
        with h5py.File(filename, mode) as f:
            n = len(self.beam_resp_step["localForces"])
            if "Nsteps" not in f.keys():
                f.create_dataset("Nsteps", data=n)
            grp1 = f.create_group("BeamInfos")
            grp2 = f.create_group("BeamRespSteps")
            for name, value in self.beam_infos.items():
                grp1.create_dataset(name, data=value)
            for name, value in self.beam_resp_step.items():
                subgrp = grp2.create_group(name)
                for i in range(n):
                    subgrp.create_dataset(f"step{i + 1}", data=value[i])

    def get_fiber_data(
        self, ele_sec: list, save_file: Union[str, bool] = "FiberData.hdf5"
    ):
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
            check_file(save_file, [".hdf5", ".h5", ".he5"])
        self.fiber_sec_tags.extend(ele_sec)
        for ele_sec_i in self.fiber_sec_tags:
            key = f"{ele_sec_i[0]}-{ele_sec_i[1]}"
            self.fiber_sec_data[key] = []

        # get data
        for ele_sec_i in self.fiber_sec_tags:
            ele_tag = ele_sec_i[0]
            sec_tag = ele_sec_i[1]
            key = f"{ele_sec_i[0]}-{ele_sec_i[1]}"
            fiber_data = get_fiber_sec_data(ele_tag, sec_tag)
            self.fiber_sec_data[key] = fiber_data
        # ---------------------------------------------
        if save_file:
            output_filename = self.out_dir + "/" + save_file
            with h5py.File(output_filename, "w") as f:
                for name, value in self.fiber_sec_data.items():
                    f.create_dataset(name, data=value)
            print(
                f"Fiber section data saved in [bold {next(self.colors_cycle)}]{output_filename}[/]!"
            )

    def get_fiber_resp_step(
        self,
        num_steps: int = 10000000000000,
        total_time: float = 10000000000000,
        stop_cond: bool = False,
        save_file: Union[str, bool] = "FiberRespStepData-1.hdf5",
    ):
        """Get analysis results data for fiber section one step.

        Parameters
        ----------
        num_steps: int, default=10000000000000
            Total number of steps, set to determine when to save data.
        total_time: float, default=10000000000000
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
            check_file(save_file, [".hdf5", ".h5", ".he5"])

        if self.step_fiber_track == 0:
            for ele_sec_i in self.fiber_sec_tags:
                key = f"{ele_sec_i[0]}-{ele_sec_i[1]}"
                self.fiber_sec_step_data[key] = []

        for ele_sec_i in self.fiber_sec_tags:
            ele_tag = ele_sec_i[0]
            sec_tag = ele_sec_i[1]
            key = f"{ele_sec_i[0]}-{ele_sec_i[1]}"
            fiber_data = get_fiber_sec_data(ele_tag, sec_tag)
            defo_fo = ops.eleResponse(
                ele_tag, "section", sec_tag, "forceAndDeformation"
            )
            if len(defo_fo) == 4:
                defo_fo = [
                    defo_fo[0],
                    defo_fo[1],
                    0.0,
                    0.0,
                    defo_fo[2],
                    defo_fo[3],
                    0.0,
                    0.0,
                ]
            sec_defo_fo = np.array([defo_fo] * len(fiber_data), dtype=float)
            data = np.hstack([fiber_data, sec_defo_fo])
            self.fiber_sec_step_data[key].append(data)
        # ------------------------
        self.step_fiber_track += 1
        # ------------------------
        if save_file:
            if (
                self.step_fiber_track >= num_steps or
                ops.getTime() >= total_time or
                stop_cond
            ):
                output_filename = self.out_dir + "/" + save_file
                self._save_fiber_resp_step(output_filename, "w")
                print(
                    f"Fiber section responses data saved in [bold {next(self.colors_cycle)}]{output_filename}[/]!"
                )

    def _save_fiber_resp_step(self, filename: str, mode: str = "w"):
        with h5py.File(filename, mode) as f:
            if "Nsteps" not in f.keys():
                f.create_dataset("Nsteps", data=self.step_fiber_track)
            grp = f.create_group("FiberRespSteps")
            for name, value in self.fiber_sec_step_data.items():
                subgrp = grp.create_group(name)
                for i in range(self.step_fiber_track):
                    subgrp.create_dataset(f"step{i + 1}", data=value[i])

    def get_resp_step(
        self,
        dynamic: bool = False,
        rayleigh: bool = False,
        model_update: bool = False,
    ):
        """Get all currently supported responses in one step.

        .. note::
                This method needs to be used in conjunction with :meth:`opstool.vis.GetFEMdata.save_resp_all`.

        Parameters
        ----------
        dynamic : bool, optional, by default False
            If True, node reactions will include dynamic effects.
        rayleigh : bool, optional, by default False
            If True, node reactions will include rayleigh damping.
        model_update: bool, optional, by default False
            whether to update the model domain data at each analysis step,
            this will be useful if model data has changed.
            For example, some elements and nodes were removed.
            This parameter is currently only valid for getting node response data, i.e.,
            :meth:`opstool.vis.GetFEMdata.get_node_resp_step`.
        """
        self.get_node_resp_step(save_file=False, model_update=model_update)
        self.get_node_react_step(dynamic=dynamic, rayleigh=rayleigh, save_file=False)
        self.get_frame_resp_step(save_file=False)
        self.get_fiber_resp_step(save_file=False)

    def save_resp_all(
        self, save_file: str = "RespStepData-1.hdf5", reset_state: bool = True
    ):
        """Save all responses data for all analysis steps at once.
        This means you need to call it after the loop is over.

        Parameters
        ----------
        save_file : str, optional, by default "RespStepData-1.hdf5"
            The file name that data saved.
            If None of False, the data will not be saved.

            .. warning::
                Be careful not to include any path, only filename,
                the file will be saved to the directory ``results_dir``.
                You need to specify different suffixes to distinguish between the different analysis cases.
                Such as "RespStepData-1.hdf5", "RespStepData-2.hdf5", etc.

        reset_state : bool, optional, by default True
            If True, the response data from previous analysis cases will be cleared, otherwise it will be included.
        """
        filename = self.out_dir + "/" + save_file
        if os.path.isfile(filename):
            os.remove(filename)
        if self.node_resp_steps["disp"]:
            self._save_node_resp_step(filename, "w")
        if self.node_react_steps:
            self._save_node_react_step(filename, "a")
        if self.beam_resp_step["localForces"]:
            self._save_frame_resp_step(filename, "a")
        if self.fiber_sec_step_data:
            self._save_fiber_resp_step(filename, "a")
        if reset_state:
            self.reset_steps_state()
        print(
            f"All responses data saved in [bold {next(self.colors_cycle)}]{filename}[/]!"
        )
