"""
Visualizing OpenSeesPy Fiber Section.
"""

import h5py
import numpy as np
import matplotlib
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from typing import Union


class FiberSecVis:
    """
    A class to vis the fiber section in OpenSeesPy.

    Parameters
    -------------
    ele_tag: int
        The element tag to which the section is to be displayed.
    sec_tag: int
        Which integration point section is displayed, tag from 1 from segment i to j.
    results_dir: str, default="opstool_output"
        The dir that results saved.
    line_width: float, default = 0.75
        The line width of mesh edges.
    line_color: str, default = "k"
        The color of mesh edges.
    colormap: str, default = "jet"
        Color map used to display the response.
    opacity: float, default=0.75
        Transparency of mesh.

    Returns
    --------
    FiberSecVis instance.
    """

    def __init__(self, ele_tag: int, sec_tag: int,
                 results_dir: str = "opstool_output",
                 line_width: float = 0.75, line_color: str = 'k',
                 colormap: str = "viridis", opacity: float = 0.75):
        self.ele_tag = ele_tag
        self.sec_tag = sec_tag
        self.key = f"{self.ele_tag}-{self.sec_tag}"
        self.lw = line_width
        self.lc = line_color
        self.cmap = colormap
        self.opacity = opacity
        self.out_dir = results_dir

    def sec_vis(self,
                input_file: str = 'FiberData.hdf5',
                mat_color: dict = None,
                ):
        """plot the fiber section.

        Parameters
        ------------
        input_file: str, default='FiberData.hdf5'
            The file name that fiber section data saved.

            .. warning::
                Be careful not to include any path, only filename,
                the file will be saved to the directory ``results_dir``.

        mat_color: dict
            Dict for assign color by matTag, {matTag1:color1,matTag2:color2, and so on}
            matTag is the material tag defined in openseespy, bu it must in the section.

        Returns
        ----------
        None
        """
        filename = self.out_dir + '/' + input_file
        fiber_sec_data = {}
        with h5py.File(filename, "r") as f:
            for name, value in f.items():
                fiber_sec_data[name] = value[...]
        if self.key not in fiber_sec_data.keys():
            raise ValueError("ele_tag and sec_tag not in set_fiber_secs()!")
        fiber_data = fiber_sec_data[self.key]
        ylocs = fiber_data[:, 0]
        zlocs = fiber_data[:, 1]
        areas = fiber_data[:, 2]
        mat_tags = np.array(fiber_data[:, 3], dtype=int)
        # bounds and centers
        ymin, ymax = np.min(ylocs), np.max(ylocs)
        zmin, zmax = np.min(zlocs), np.max(zlocs)
        space_y = (ymax - ymin) / 10
        space_z = (zmax - zmin) / 10
        aspect_ratio = (zmax - zmin) / (ymax - ymin)
        yc = np.sum(ylocs * areas) / np.sum(areas)
        zc = np.sum(zlocs * areas) / np.sum(areas)
        # scalars
        scalars = np.sqrt((ylocs - yc) ** 2 + (zlocs - zc) ** 2)
        # rs = np.sqrt(areas / np.pi)
        # --------------------------------------------------------------
        # start plot
        # --------------------------------------------------------------
        plt.style.use("seaborn")
        # plt.style.use('ggplot')
        fig, ax = plt.subplots(figsize=(6, 6 * aspect_ratio))
        patches = [
            plt.Circle((yloc, zloc), np.sqrt(area / np.pi))
            for yloc, zloc, area in zip(ylocs, zlocs, areas)
        ]
        coll = matplotlib.collections.PatchCollection(
            patches, alpha=self.opacity)
        coll.set_array(scalars)
        coll.set_ec(self.lc)
        coll.set_lw(self.lw)
        coll.set_cmap(self.cmap)
        ax.add_collection(coll)

        # If mat_color
        if mat_color is not None:
            for mat, color in mat_color.items():
                idx = np.argwhere(np.abs(mat_tags - mat) < 1e-8)
                ys_ = ylocs[idx]
                zs_ = zlocs[idx]
                areas_ = areas[idx]
                patches = [
                    plt.Circle((yloc, zloc), np.sqrt(area / np.pi))
                    for yloc, zloc, area in zip(ys_, zs_, areas_)
                ]
                coll = matplotlib.collections.PatchCollection(
                    patches, color=color, alpha=self.opacity
                )
                coll.set_ec(self.lc)
                coll.set_lw(self.lw)
                ax.add_collection(coll)
        # ax.set_aspect("equal")
        ax.set_xlim(ymin - space_y, ymax + space_y)
        ax.set_ylim(zmin - space_z, zmax + space_z)
        ax.set_xlabel("y", fontsize=16)
        ax.set_ylabel("z", fontsize=16)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        txt = f"ele--sec: {self.ele_tag}--{self.sec_tag}\n"
        ax.set_title(txt, fontsize=15)
        plt.show()

    def _get_fiber_data(self,
                        input_file: str = "FiberRespStepData-1.hdf5",
                        step: int = None,
                        show_variable: str = "strain",
                        show_mats: Union[int, list[int], tuple[int]] = None,
                        ):
        filename = self.out_dir + '/' + input_file
        fiber_sec_step_data = dict()
        with h5py.File(filename, "r") as f:
            n = f["Nsteps"][...]
            grp = f["FiberRespSteps"]
            for name in grp.keys():
                temp = []
                for i in range(n):
                    temp.append(grp[name][f"step{i+1}"][...])
                fiber_sec_step_data[name] = temp

        if self.key not in fiber_sec_step_data.keys():
            raise ValueError("ele_tag and sec_tag not in set_fiber_secs()!")
        fiber_step_data = fiber_sec_step_data[self.key]
        fiber_step_data = np.array(fiber_step_data)

        if step is None:
            max_resp = []
            for data in fiber_step_data:
                mat_tags = np.array(data[:, 3], dtype=int)
                if show_mats is not None:
                    show_mats = np.atleast_1d(show_mats)
                    matidx = []
                    for mat in show_mats:
                        matidx.append(np.argwhere(
                            np.abs(mat_tags - mat) < 1e-8))
                    matidx = np.vstack(matidx)
                else:
                    matidx = np.argwhere(np.abs(mat_tags - mat_tags) < 1e-8)
                if show_variable.lower() == "stress":
                    max_resp.append(np.max(np.abs(data[matidx, 4])))
                elif show_variable.lower() == "strain":
                    max_resp.append(np.max(np.abs(data[matidx, 5])))
                else:
                    raise ValueError("")
            maxstep = np.argmax(max_resp)
            fiber_data = fiber_step_data[maxstep]
            step_ = maxstep
        elif step == -1:
            fiber_data = fiber_step_data[-1]
            step_ = len(fiber_step_data) - 1
        else:
            fiber_data = fiber_step_data[step - 1]
            step_ = step - 1

        mat_tags = np.array(fiber_data[:, 3], dtype=int)
        if show_mats is not None:
            show_mats = np.atleast_1d(show_mats)
            matidx = []
            for mat in show_mats:
                matidx.append(np.argwhere(np.abs(mat_tags - mat) < 1e-8))
            matidx = np.vstack(matidx)
        else:
            matidx = np.argwhere(np.abs(mat_tags - mat_tags) < 1e-8)

        if show_variable == "stress":
            vmin = np.min(fiber_data[matidx, 4])
            vmax = np.max(fiber_data[matidx, 4])
        elif show_variable == "strain":
            vmin = np.min(fiber_data[matidx, 5])
            vmax = np.max(fiber_data[matidx, 5])
        else:
            raise ValueError("show_variable must be 'stress' or 'strain'!")

        ylocs = fiber_data[:, 0]
        zlocs = fiber_data[:, 1]
        areas = fiber_data[:, 2]
        return fiber_data, step_, matidx, vmin, vmax, ylocs, zlocs, areas

    def resp_vis(self,
                 input_file: str = "FiberRespStepData-1.hdf5",
                 step: int = None,
                 show_variable: str = "strain",
                 show_mats: Union[int, list[int], tuple[int]] = None,
                 ):
        """fiber section response vis.

        Parameters
        -----------
        input_file: str, default='FiberRespStepData-1.hdf5'
            The file name that fiber section responses saved.
        step: int, default = None
            Analysis step to display. If None, the step that max response; If -1, the final step; Else, the other step.
        show_variable: str, default = 'srain'
            Response type to display, optional "stress" or "strain".
        show_mats: Union[int, list[int], tuple[int]]
            matTags to dispaly. matTag is the material tag defined in openseespy, bu it must in the section.
            If None, all tags will display.

        Returns
        --------
        None
        """
        filename = self.out_dir + '/' + input_file
        fiber_sec_step_data = dict()
        with h5py.File(filename, "r") as f:
            n = f["Nsteps"][...]
            grp = f["FiberRespSteps"]
            for name in grp.keys():
                temp = []
                for i in range(n):
                    temp.append(grp[name][f"step{i+1}"][...])
                fiber_sec_step_data[name] = temp

        if self.key not in fiber_sec_step_data.keys():
            raise ValueError("ele_tag and sec_tag not in set_fiber_secs()!")
        fiber_step_data = fiber_sec_step_data[self.key]
        fiber_step_data = np.array(fiber_step_data)

        fiber_data, step_, matidx, vmin, vmax, ylocs, zlocs, areas = self._get_fiber_data(
            input_file, step, show_variable, show_mats)
        ymin, ymax = np.min(ylocs), np.max(ylocs)
        zmin, zmax = np.min(zlocs), np.max(zlocs)
        space_y = (ymax - ymin) / 10
        space_z = (zmax - zmin) / 10
        aspect_ratio = (zmax - zmin) / (ymax - ymin)
        ys_ = ylocs[matidx].ravel()
        zs_ = zlocs[matidx].ravel()
        areas_ = areas[matidx].ravel()
        stress_ = fiber_data[matidx, 4].ravel()
        strain_ = fiber_data[matidx, 5].ravel()
        my = fiber_data[matidx, 12][0, 0]
        mz = fiber_data[matidx, 11][0, 0]
        p = fiber_data[matidx, 10][0, 0]
        ey = fiber_data[matidx, 8][0, 0]
        ez = fiber_data[matidx, 7][0, 0]
        eps = fiber_data[matidx, 6][0, 0]
        colors = stress_ if show_variable == "stress" else strain_
        # --------------------------------------------------------------
        # start plot
        # --------------------------------------------------------------
        # ------------------------------------------------------
        plt.style.use("seaborn")
        # plt.style.use('ggplot')
        fig, ax = plt.subplots(figsize=(6, 6 * aspect_ratio))
        patches = [
            plt.Circle((yloc, zloc), np.sqrt(area / np.pi))
            for yloc, zloc, area in zip(ys_, zs_, areas_)
        ]
        coll = matplotlib.collections.PatchCollection(
            patches, alpha=self.opacity)
        coll.set_ec(self.lc)
        coll.set_lw(self.lw)
        coll.set_cmap(self.cmap)
        coll.set_clim(vmin, vmax)
        coll.set_array(colors)
        ax.add_collection(coll)
        # -------------------------------------------
        #  color bar
        clb = fig.colorbar(coll, ax=ax, format="%.2E",
                           use_gridspec=True, location='bottom',
                           fraction=0.15, aspect=16)
        clb.set_label(show_variable, fontsize=12)
        clb.ax.tick_params(labelsize=9)
        # -----------------------------
        ax.set_aspect(aspect_ratio)
        ax.set_xlim(ymin - space_y, ymax + space_y)
        ax.set_ylim(zmin - space_z, zmax + space_z)
        ax.set_xlabel("y", fontsize=15)
        ax.set_ylabel("z", fontsize=15)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        txt = (f"ele--sec: {self.ele_tag}--{self.sec_tag} | step: {step_ + 1}\n"
               f"$\\rm M_z$={mz:.2E} | $\\rm M_y$={my:.2E} | $\\rm P$={p:.2E} \n"
               f"$\\rm \\phi_z$={ez:.2E} | $\\rm \\phi_y$={ey:.2E} | $\\rm \\epsilon$={eps:.2E}")
        ax.set_title(txt, fontsize=12)
        plt.tight_layout()
        plt.show()

    def animation(self,
                  output_file: str,
                  input_file: str = "FiberRespStepData-1.hdf5",
                  show_variable: str = "strain",
                  show_mats: Union[int, list[int], tuple[int]] = None,
                  framerate: int = 24,
                  ):
        """fiber section response animation.

        Parameters
        ----------
        output_file: str
            The output file name, must end with .gif.
        input_file: str, default='FiberRespStepData-1.hdf5'
            The file name that fiber section responses saved.
        show_variable: str, default='strain
            Response type to display, optional "stress" or "strain".
        show_mats: Union[int, list[int], tuple[int]], default=None
            Mat tag to dispaly. If None, all tags will display.
        framerate: int, default=24
            The number of frames per second.

        Returns
        -------
        None
        """
        filename = self.out_dir + '/' + input_file
        fiber_sec_step_data = dict()
        with h5py.File(filename, "r") as f:
            n = f["Nsteps"][...]
            grp = f["FiberRespSteps"]
            for name in grp.keys():
                temp = []
                for i in range(n):
                    temp.append(grp[name][f"step{i+1}"][...])
                fiber_sec_step_data[name] = temp
        if self.key not in fiber_sec_step_data.keys():
            raise ValueError("ele_tag and sec_tag not in set_fiber_secs()!")
        fiber_step_data = fiber_sec_step_data[self.key]
        fiber_step_data = np.array(fiber_step_data)

        fiber_data, step_max, matidx, vmin, vmax, ylocs, zlocs, areas = self._get_fiber_data(
            input_file, None, show_variable, show_mats)
        fiber_data, step0, matidx, vmin0, vmax0, ylocs, zlocs, areas = self._get_fiber_data(
            input_file, 1, show_variable, show_mats)
        ymin, ymax = np.min(ylocs), np.max(ylocs)
        zmin, zmax = np.min(zlocs), np.max(zlocs)
        space_y = (ymax - ymin) / 10
        space_z = (zmax - zmin) / 10
        aspect_ratio = (zmax - zmin) / (ymax - ymin)
        my = fiber_data[matidx, 12][0, 0]
        mz = fiber_data[matidx, 11][0, 0]
        p = fiber_data[matidx, 10][0, 0]
        ey = fiber_data[matidx, 8][0, 0]
        ez = fiber_data[matidx, 7][0, 0]
        eps = fiber_data[matidx, 6][0, 0]

        # ------------------------------------------------------
        plt.style.use("seaborn")
        # plt.style.use('ggplot')
        fig, ax = plt.subplots(figsize=(8, 8 * aspect_ratio))
        patches = [
            plt.Circle((yloc, zloc), np.sqrt(area / np.pi))
            for yloc, zloc, area in zip(ylocs[matidx], zlocs[matidx], areas[matidx])
        ]
        coll = matplotlib.collections.PatchCollection(
            patches, alpha=self.opacity)
        coll.set_ec(self.lc)
        coll.set_lw(self.lw)
        coll.set_cmap(self.cmap)
        coll.set_clim(vmin, vmax)
        ax.add_collection(coll)
        # -------------------------------------------
        #  color bar
        clb = fig.colorbar(coll, ax=ax, format="%.2E",
                           use_gridspec=True, location='bottom',
                           fraction=0.15, aspect=16)
        clb.set_label(show_variable, fontsize=12)
        clb.ax.tick_params(labelsize=9)
        # -----------------------------
        ax.set_aspect(aspect_ratio)
        ax.set_xlim(ymin - space_y, ymax + space_y)
        ax.set_ylim(zmin - space_z, zmax + space_z)
        ax.set_xlabel("y", fontsize=15)
        ax.set_ylabel("z", fontsize=15)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        txt = (f"ele--sec: {self.ele_tag}--{self.sec_tag} | step: {1}\n"
               f"$\\rm M_z$={mz:.2E} | $\\rm M_y$={my:.2E} | $\\rm P$={p:.2E} \n"
               f"$\\rm \\phi_z$={ez:.2E} | $\\rm \\phi_y$={ey:.2E} | $\\rm \\epsilon$={eps:.2E}")
        title = ax.set_title(txt, fontsize=12)

        # --------------------------------------------
        def animate(step):
            fiber_data_i = fiber_step_data[step]
            mat_tagsi = np.array(fiber_data_i[:, 3], dtype=int)
            if show_mats is not None:
                matidx_i = []
                for mat_ in show_mats:
                    matidx_i.append(np.argwhere(np.abs(mat_tagsi - mat_) < 1e-8))
                matidx_i = np.vstack(matidx_i)
            else:
                matidx_i = np.argwhere(np.abs(mat_tagsi - mat_tagsi) < 1e-8)

            if show_variable == "stress":
                vmini = np.min(fiber_data_i[matidx_i, 4])
                vmaxi = np.max(fiber_data_i[matidx_i, 4])
            elif show_variable == "strain":
                vmini = np.min(fiber_data_i[matidx_i, 5])
                vmaxi = np.max(fiber_data_i[matidx_i, 5])
            else:
                raise ValueError("")

            stressi, straini = fiber_data_i[matidx_i, 4].ravel(
            ), fiber_data_i[matidx_i, 5].ravel()
            myi = fiber_data_i[matidx_i, 12][0, 0]
            mzi = fiber_data_i[matidx_i, 11][0, 0]
            pi = fiber_data_i[matidx_i, 10][0, 0]
            eyi = fiber_data_i[matidx_i, 8][0, 0]
            ezi = fiber_data_i[matidx_i, 7][0, 0]
            epsi = fiber_data_i[matidx_i, 6][0, 0]
            colors = stressi if show_variable == "stress" else straini
            coll.set_array(colors)
            coll.set_clim(vmin, vmax)
            txti = (f"ele--sec: {self.ele_tag}--{self.sec_tag} | step: {i+1}\n"
                    f"$\\rm M_z$={mzi:.2E} | $\\rm M_y$={myi:.2E} | $\\rm P$={pi:.2E} \n"
                    f"$\\rm \\phi_z$={ezi:.2E} | $\\rm \\phi_y$={eyi:.2E} | $\\rm \\epsilon$={epsi:.2E}")
            title.set_text(txti)
            # clb.set_ticks(clb.get_ticks())
            # clb.set_ticklabels(
            #     [f"{label:.2E}" for label in clb.get_ticks()], fontsize=13)
            # clb.set_label(show_variable, fontsize=16)

        ani = animation.FuncAnimation(
            fig, animate, frames=len(fiber_step_data), blit=False
        )
        plt.show()
        ani.save(output_file, fps=framerate)  # need ffmpeg
