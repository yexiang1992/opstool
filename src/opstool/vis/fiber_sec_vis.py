"""
Visualizing OpenSeesPy Fiber Section.
"""

import h5py
import numpy as np
import matplotlib
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from ..utils import shape_dict


class FiberSecVis:
    """
    A class to vis the fiber section responses in OpenSeesPy.

    .. warning::
        This class is currently only available for 3D models,
        as fiber coordinates cannot be extracted for 2D models.

    Parameters
    -------------
    results_dir: str, default="opstool_output"
        The dir that results saved.
    input_file: str, default='FiberRespStepData-1.hdf5'
        The file name that fiber section responses saved.
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

    def __init__(self,
                 results_dir: str = "opstool_output",
                 input_file: str = "FiberRespStepData-1.hdf5",
                 line_width: float = 0.75, line_color: str = 'k',
                 colormap: str = "viridis", opacity: float = 0.75):
        self.lw = line_width
        self.lc = line_color
        self.cmap = colormap
        self.opacity = opacity
        self.out_dir = results_dir

        filename = self.out_dir + '/' + input_file
        self.fiber_sec_step_data = dict()
        with h5py.File(filename, "r") as f:
            n = f["Nsteps"][...]
            grp = f["FiberRespSteps"]
            for name in grp.keys():
                temp = []
                for i in range(n):
                    temp.append(grp[name][f"step{i + 1}"][...])
                self.fiber_sec_step_data[name] = temp
        self.key_names = self.fiber_sec_step_data.keys()

    def sec_vis(self,
                ele_tag: int, sec_tag: int,
                mat_color: dict = None,
                ):
        """plot the fiber section.

        Parameters
        ------------
        ele_tag: int
            The element tag to which the section is to be displayed.
        sec_tag: int
            Which integration point section is displayed, tag from 1 from segment i to j.
        mat_color: dict
            Dict for assign color by matTag, {matTag1:color1,matTag2:color2, and so on}
            matTag is the material tag defined in openseespy, bu it must in the section.

        Returns
        ----------
        None
        """
        key = f"{ele_tag}-{sec_tag}"
        if key not in self.key_names:
            raise ValueError("ele_tag and sec_tag not in set_fiber_secs()!")
        fiber_data = self.fiber_sec_step_data[key][0][:, :6]

        plt.style.use("seaborn")
        # plt.style.use('ggplot')
        fig, ax = plt.subplots(figsize=(6, 6))
        txt = f"ele--sec: {ele_tag}--{sec_tag}\n"
        _plot_fiber_sec(ax, fiber_data, txt, self.lc,
                        self.lw, self.cmap, self.opacity, mat_color)
        plt.show()

    def _get_fiber_data(self,
                        key: str,
                        step: int = None,
                        show_variable: str = "strain",
                        show_mats=None,
                        ):

        if key not in self.key_names:
            raise ValueError("ele_tag and sec_tag not in set_fiber_secs()!")
        fiber_step_data = self.fiber_sec_step_data[key]
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
                 ele_tag: int, sec_tag: int,
                 step: int = None,
                 show_variable: str = "strain",
                 show_mats=None,
                 ):
        """fiber section response vis.

        Parameters
        -----------
        ele_tag: int
            The element tag to which the section is to be displayed.
        sec_tag: int
            Which integration point section is displayed, tag from 1 from segment i to j.
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
        key = f"{ele_tag}-{sec_tag}"
        if key not in self.key_names:
            raise ValueError("ele_tag and sec_tag not in set_fiber_secs()!")
        # fiber_step_data = fiber_sec_step_data[self.key]
        # fiber_step_data = np.array(fiber_step_data)

        fiber_data, step_, matidx, vmin, vmax, ylocs, zlocs, areas = self._get_fiber_data(
            key, step, show_variable, show_mats)
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
        my = fiber_data[0, 12]
        mz = fiber_data[0, 11]
        p = fiber_data[0, 10]
        ey = fiber_data[0, 8]
        ez = fiber_data[0, 7]
        eps = fiber_data[0, 6]
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
        txt = (f"ele--sec: {ele_tag}--{sec_tag} | step: {step_ + 1}\n"
               f"$\\rm M_z$={mz:.2E} | $\\rm M_y$={my:.2E} | $\\rm P$={p:.2E} \n"
               f"$\\rm \\phi_z$={ez:.2E} | $\\rm \\phi_y$={ey:.2E} | $\\rm \\epsilon$={eps:.2E}")
        ax.set_title(txt, fontsize=12)
        plt.tight_layout()
        plt.show()

    def animation(self,
                  output_file: str,
                  ele_tag: int, sec_tag: int,
                  show_variable: str = "strain",
                  show_mats=None,
                  framerate: int = 24,
                  ):
        """fiber section response animation.

        Parameters
        ----------
        output_file: str
            The output file name, must end with .gif.
        ele_tag: int
            The element tag to which the section is to be displayed.
        sec_tag: int
            Which integration point section is displayed, tag from 1 from segment i to j.
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
        key = f"{ele_tag}-{sec_tag}"
        if key not in self.key_names:
            raise ValueError("ele_tag and sec_tag not in set_fiber_secs()!")
        fiber_step_data = self.fiber_sec_step_data[key]

        fiber_data, step_max, matidx, vmin, vmax, ylocs, zlocs, areas = self._get_fiber_data(
            key, None, show_variable, show_mats)
        fiber_data, step0, matidx, vmin0, vmax0, ylocs, zlocs, areas = self._get_fiber_data(
            key, 1, show_variable, show_mats)
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
        txt = (f"ele--sec: {ele_tag}--{sec_tag} | step: {1}\n"
               f"$\\rm M_z$={mz:.2E} | $\\rm M_y$={my:.2E} | $\\rm P$={p:.2E} \n"
               f"$\\rm \\phi_z$={ez:.2E} | $\\rm \\phi_y$={ey:.2E} | $\\rm \\epsilon$={eps:.2E}")
        title = ax.set_title(txt, fontsize=12)

        # --------------------------------------------
        def animate(step):
            fiber_data_i = np.array(fiber_step_data[step])
            mat_tagsi = np.array(fiber_data_i[:, 3], dtype=int)
            if show_mats is not None:
                matidx_i = []
                for mat_ in show_mats:
                    matidx_i.append(np.argwhere(
                        np.abs(mat_tagsi - mat_) < 1e-8))
                matidx_i = np.vstack(matidx_i)
            else:
                matidx_i = np.argwhere(np.abs(mat_tagsi - mat_tagsi) < 1e-8)

            # if show_variable == "stress":
            #     vmini = np.min(fiber_data_i[matidx_i, 4])
            #     vmaxi = np.max(fiber_data_i[matidx_i, 4])
            # elif show_variable == "strain":
            #     vmini = np.min(fiber_data_i[matidx_i, 5])
            #     vmaxi = np.max(fiber_data_i[matidx_i, 5])
            # else:
            #     raise ValueError("")

            stressi, straini = fiber_data_i[matidx_i, 4].ravel(), fiber_data_i[matidx_i, 5].ravel()
            myi = fiber_data_i[0, 12]
            mzi = fiber_data_i[0, 11]
            pi = fiber_data_i[0, 10]
            eyi = fiber_data_i[0, 8]
            ezi = fiber_data_i[0, 7]
            epsi = fiber_data_i[0, 6]
            colors = stressi if show_variable == "stress" else straini
            coll.set_array(colors)
            coll.set_clim(vmin, vmax)
            txti = (f"ele--sec: {ele_tag}--{sec_tag} | step: {step + 1}\n"
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

    def force_defo_vis(self,
                       ele_tag: int, sec_tag: int,
                       force_type: str = "Mz",
                       defo_type: str = "Phiz"):
        """fiber section response vis.

        Parameters
        -----------
        ele_tag: int
            The element tag to which the section is to be displayed.
        sec_tag: int
            Which integration point section is displayed, tag from 1 from segment i to j.
        force_type: str, default = "Mz"
            Force type to plot, optional ["P", "Mz", "My"].
        defo_type: str, default = "Phiz"
            Deformation type to plot, optional ["eps", "Phiz", "Phiy"].

        Returns
        --------
        (numpy.1D Array, numpy.1D Array)
            Deformation Array, Force Array.
        """
        key = f"{ele_tag}-{sec_tag}"
        if key not in self.key_names:
            raise ValueError("ele_tag and sec_tag not in set_fiber_secs()!")
        fiber_sec_step = self.fiber_sec_step_data[key]

        force_map = dict(p=10, mz=11, my=12)
        defo_map = dict(eps=6, phiz=7, phiy=8)
        foidx = force_map[force_type.lower()]
        defoidx = defo_map[defo_type.lower()]

        forces = []
        defos = []
        for fiber_data in fiber_sec_step:
            forces.append(fiber_data[0, foidx])
            defos.append(fiber_data[0, defoidx])

        force_label_map = dict(p="$\\rm P$", mz="$\\rm M_z$", my="$\\rm M_y$")
        defo_label_map = dict(eps="$\\rm \\epsilon$", phiz="$\\rm \\phi_z$", phiy="$\\rm \\phi_y$")
        fig, ax = plt.subplots(figsize=(6, 6 * 0.618))
        ax.plot(defos, forces, lw=1.75, c="blue", )
        ax.set_ylabel(force_label_map[force_type.lower()], fontsize=16)
        ax.set_xlabel(defo_label_map[defo_type.lower()], fontsize=16)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        txt = f"ele--sec: {ele_tag}--{sec_tag}\n"
        ax.set_title(txt, fontsize=15)
        plt.show()

        return np.array(defos), np.array(forces)


def plot_fiber_sec(ele_sec: list,
                   results_dir: str = "opstool_output",
                   input_file: str = 'FiberData.hdf5',
                   line_width: float = 0.75, line_color: str = 'k',
                   colormap: str = "viridis", opacity: float = 0.75,
                   mat_color: dict = None, ):
    """plot the fiber section geometry.

    Parameters
    ------------
    results_dir: str, default="opstool_output"
        The dir that results saved.
    input_file: str, default='FiberData.hdf5'
        The file name that fiber section data saved.
        .. warning::
            Be careful not to include any path, only filename,
            the file will be loaded from the directory ``results_dir``.
    ele_sec: list[tuple[int, int]]
            A list or tuple composed of element tag and sectag to plot.
            e.g., [(ele1, sec1), (ele2, sec2), ... , (elen, secn)],
            The section is attached to an element in the order from end i to end j of that element.
    line_width: float, default = 0.75
        The line width of mesh edges.
    line_color: str, default = "k"
        The color of mesh edges.
    colormap: str, default = "jet"
        Color map used to display the response.
    opacity: float, default=0.75
        Transparency of mesh.
    mat_color: dict
        Dict for assign color by matTag, {matTag1:color1,matTag2:color2, and so on}
        matTag is the material tag defined in openseespy, bu it must in the section.

    Returns
    ----------
    None

    """
    lw, lc = line_width, line_color
    filename = results_dir + '/' + input_file
    fiber_sec_data = {}
    with h5py.File(filename, "r") as f:
        for name, value in f.items():
            fiber_sec_data[name] = value[...]
    n_sec = len(ele_sec)
    shape = shape_dict[n_sec]
    figsize = 5 * shape[1], 4 * shape[0]

    plt.style.use("seaborn")
    fig, axs = plt.subplots(shape[0], shape[1], figsize=figsize)

    for i, elesec in enumerate(ele_sec):
        ele_tag, sec_tag = elesec
        if n_sec == 1:
            ax = axs
        else:
            idxi = int(np.ceil((i + 1) / shape[1]) - 1)
            idxj = int(i - idxi * shape[1])
            ax = axs[idxi, idxj]
        key = f"{ele_tag}-{sec_tag}"
        fiber_data = fiber_sec_data[key]
        txt = f"ele--sec: {ele_tag}--{sec_tag}\n"
        _plot_fiber_sec(ax, fiber_data, txt, lc, lw, colormap, opacity, mat_color)
    if shape[0] * shape[1] > n_sec:
        for i in range(n_sec, shape[0] * shape[1]):
            idxi = int(np.ceil((i + 1) / shape[1]) - 1)
            idxj = int(i - idxi * shape[1])
            ax = axs[idxi, idxj]
            with plt.style.context('classic'):
                ax.set_visible(False)

    plt.subplots_adjust(hspace=0.3)
    plt.show()


def _plot_fiber_sec(ax, fiber_data, title, lc, lw, cmap, opacity, mat_color):
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
    patches = [
        plt.Circle((yloc, zloc), np.sqrt(area / np.pi))
        for yloc, zloc, area in zip(ylocs, zlocs, areas)
    ]
    coll = matplotlib.collections.PatchCollection(
        patches, alpha=opacity)
    coll.set_array(scalars)
    coll.set_ec(lc)
    coll.set_lw(lw)
    coll.set_cmap(cmap)
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
                patches, color=color, alpha=opacity
            )
            coll.set_ec(lc)
            coll.set_lw(lw)
            ax.add_collection(coll)
    ax.set_aspect(aspect_ratio)
    ax.set_xlim(ymin - space_y, ymax + space_y)
    ax.set_ylim(zmin - space_z, zmax + space_z)
    ax.set_xlabel("y", fontsize=16)
    ax.set_ylabel("z", fontsize=16)
    ax.tick_params(labelsize=12)
    ax.text(0.5, 1.0, title, ha='center', fontsize=15,
            va='top', transform=ax.transAxes)
