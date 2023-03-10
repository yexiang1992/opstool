import numpy as np
import matplotlib.pyplot as plt
import openseespy.opensees as ops
from ._smart_analyze import SmartAnalyze


class MomentCurvature:
    """_summary_


    Examples
    ---------
        >>> import opstool as opst
        >>> import openseespy.opensees as ops

        >>> ops.wipe()
        >>> ops.model('basic', '-ndm', 3, '-ndf', 6)

        >>> Ec = 3.55E+7
        >>> Vc = 0.2
        >>> Gc = 0.5 * Ec / (1 + Vc)
        >>> fc = -32.4E+3
        >>> ec = -2000.0E-6
        >>> ecu = 2.1 * ec
        >>> ft = 2.64E+3
        >>> et = 107E-6
        >>> fccore = -40.6e+3
        >>> eccore = -4079e-6
        >>> ecucore = -0.0144

        >>> Fys = 400.E+3
        >>> Fus = 530.E+3
        >>> Es = 2.0E+8
        >>> eps_sh = 0.0074
        >>> eps_ult = 0.095
        >>> Esh = (Fus - Fys) / (eps_ult - eps_sh)
        >>> bs = 0.01

        >>> matTagC = 1
        >>> matTagCCore = 2
        >>> matTagS = 3
        >>> ops.uniaxialMaterial('Concrete04', matTagC, fc, ec, ecu, Ec, ft, et)
        >>> ops.uniaxialMaterial('Concrete04', matTagCCore, fccore,
        >>>                     eccore, ecucore, Ec, ft, et)  # for core
        >>> ops.uniaxialMaterial('ReinforcingSteel', matTagS, Fys,
        >>>                     Fus, Es, Esh, eps_sh, eps_ult)

        >>> # section mesh
        >>> outlines = [[0, 0], [2, 0], [2, 2], [0, 2]]
        >>> coverlines = opst.offset(outlines, d=0.05)
        >>> cover = opst.add_polygon(outlines, holes=[coverlines])
        >>> holelines = [[0.5, 0.5], [1.5, 0.5], [1.5, 1.5], [0.5, 1.5]]
        >>> core = opst.add_polygon(coverlines, holes=[holelines])
        >>> sec = opst.SecMesh()
        >>> sec.assign_group(dict(cover=cover, core=core))
        >>> sec.assign_mesh_size(dict(cover=0.02, core=0.05))
        >>> sec.assign_group_color(dict(cover="gray", core="green"))
        >>> sec.assign_ops_matTag(dict(cover=matTagC, core=matTagCCore))
        >>> sec.mesh()
        >>> # add rebars
        >>> rebars = opst.Rebars()
        >>> rebar_lines1 = opst.offset(outlines, d=0.05 + 0.032 / 2)
        >>> rebars.add_rebar_line(
        >>>     points=rebar_lines1, dia=0.02, gap=0.1, color="red",
        >>>     matTag=matTagS,
        >>> )
        >>> rebar_lines2 = opst.offset(holelines, d=-(0.05 + 0.02 / 2))
        >>> rebars.add_rebar_line(
        >>>     points=rebar_lines2, dia=0.020, gap=0.1, color="black",
        >>>     matTag=matTagS,
        >>> )
        >>> rebar_lines3 = [[0.3, 0.3], [1.7, 0.3], [1.7, 1.7], [0.3, 1.7]]
        >>> rebars.add_rebar_line(
        >>>     points=rebar_lines3, dia=0.02, gap=0.15, closure=True,
        >>>     matTag=matTagS,
        >>>     color="blue",
        >>> )
        >>> # add to the sec
        >>> sec.add_rebars(rebars)
        >>> # sec.get_sec_props(display_results=False, plot_centroids=False)
        >>> sec.centring()
        >>> # sec.rotate(45)
        >>> sec.view(fill=True, engine='matplotlib', save_html=None, on_notebook=True)
        >>> sec.opspy_cmds(secTag=1, GJ=100000)  # important

        >>> # Moment Curvature analysis
        >>> mc = opst.MomentCurvature(sec_tag=1, axial_force=-10000)
        >>> mc.analyze(axis='z')
        >>> mc.plot_M_phi()
        >>> mc.plot_fiber_responses()
        >>> phiy, my = mc.get_limit_state(matTag=matTagS,
        >>>                             threshold=2e-3,)
        >>> phiu, mu = mc.get_limit_state(matTag=1,
        >>>                             threshold=-0.0144,
        >>>                             use_peak_drop20=False
        >>>                             )
        >>> Phi_eq, M_eq = mc.bilinearize(phiy, my, phiu, plot=True)
    """

    def __init__(self,
                 sec_tag: int,
                 axial_force: float = 0,) -> None:
        self.P = axial_force
        self.sec_tag = sec_tag
        self.phi, self.M, self.FiberData = None, None, None

    def analyze(self,
                axis: str = "y",
                max_phi: float = 1.0,
                incr_phi: float = 1e-4,
                stop_ratio: float = 0.7,
                smart_analyze: bool = True):
        """_summary_

        Parameters
        ----------
        axis : str, optional
            _description_, by default "y"
        max_phi : float, optional
            _description_, by default 1.0
        incr_phi : float, optional
            _description_, by default 1e-4
        stop_ratio : float, optional
            _description_, by default 0.8
        smart_analyze : bool, optional
            _description_, by default True
        """
        self.phi, self.M, self.FiberData = _analyze(sec_tag=self.sec_tag,
                                                    P=self.P,
                                                    axis=axis,
                                                    max_phi=max_phi,
                                                    incr_phi=incr_phi,
                                                    stop_ratio=stop_ratio,
                                                    smart_analyze=smart_analyze)

    def plot_M_phi(self):
        """_summary_
        """
        _, ax = plt.subplots(1, 1, figsize=(10, 10 * 0.618))
        ax.plot(self.phi, self.M, lw=3, c="blue")
        ax.set_title("$M-\phi$", fontsize=28,)
        ax.set_xlabel("$\phi$", fontsize=25)
        ax.set_ylabel("$M$", fontsize=25)
        plt.xticks(fontsize=15)
        plt.yticks(fontsize=15)
        ax.spines["bottom"].set_linewidth(1.2)
        ax.spines["left"].set_linewidth(1.2)
        ax.spines["right"].set_linewidth(1.2)
        ax.spines["top"].set_linewidth(1.2)
        plt.gcf().subplots_adjust(bottom=0.15)
        plt.show()

    def plot_fiber_responses(self):
        fiber_data = self.FiberData
        matTags = np.unique(fiber_data[-1][:, 3])

        _, axs = plt.subplots(
            len(matTags), 1, figsize=(8, 3*len(matTags)))
        for mat, ax in zip(matTags, axs):
            idxs = np.argwhere(np.abs(fiber_data[-1][:, 3] - mat) < 1e-6)
            strain = fiber_data[:, idxs, -1]
            stress = fiber_data[:, idxs, -2]
            for i in range(len(idxs)):
                ax.plot(strain[:, i, :], stress[:, i, :], lw=1, )
            ax.set_title(f"matTag = {mat:.0f}", fontsize=15)
            ax.tick_params(labelsize=12)
            ax.set_ylabel("stress", fontsize=16)
        ax.set_xlabel("strain", fontsize=16)
        plt.subplots_adjust(wspace=0.02, hspace=0.4)
        plt.tight_layout()
        plt.show()

    def get_phi(self):
        """_summary_

        Returns
        -------
        _type_
            _description_
        """
        return self.phi

    def get_curvature(self):
        """_summary_

        Returns
        -------
        _type_
            _description_
        """
        return self.get_phi()

    def get_M(self):
        """_summary_

        Returns
        -------
        _type_
            _description_
        """
        return self.M

    def get_moment(self):
        """_summary_

        Returns
        -------
        _type_
            _description_
        """
        return self.get_M()

    def get_M_phi(self):
        """_summary_

        Returns
        -------
        _type_
            _description_
        """
        return self.phi, self.M

    def get_fiber_data(self):
        """_summary_

        Returns
        -------
        _type_
            _description_
        """
        return self.FiberData

    def get_limit_state(self,
                        matTag: int = 1,
                        threshold: float = 0,
                        use_peak_drop20: bool = False):
        """_summary_

        Parameters
        ----------
        matTag : int, optional
            _description_, by default 1
        threshold : float, optional
            _description_, by default 0
        use_peak_drop20 : bool, optional
            _description_, by default False

        Returns
        -------
        _type_
            _description_

        Raises
        ------
        RuntimeError
            _description_
        RuntimeError
            _description_
        """
        phi = self.phi
        M = self.M
        fiber_data = self.FiberData
        if use_peak_drop20:
            idx = np.argmax(M)
            au = np.argwhere(M[idx:] <= np.max(M) * 0.80)
            if au.size == 0:
                raise RuntimeError(
                    "Peak strength does not drop 20%, please increase target ductility ratio!")
            else:
                bu = np.min(au) + idx - 1
        else:
            idxu = np.argwhere(np.abs(fiber_data[-1][:, 3] - matTag) < 1e-6)
            eu = threshold
            if eu >= 0:
                strain = np.array([np.max(data[idxu, -1])
                                  for data in fiber_data])
                au = np.argwhere(strain >= eu)
            else:
                strain = np.array([np.min(data[idxu, -1])
                                  for data in fiber_data])
                au = np.argwhere(strain < eu)
            if len(au) == 0:
                raise RuntimeError(
                    "The ultimate strain is not reached, please increase target ductility ratio!")
            else:
                bu = np.min(au)
        Phi_u = phi[bu]
        M_u = M[bu]
        return Phi_u, M_u

    def bilinearize(self, phiy: float,
                    My: float,
                    phiu: float,
                    plot: bool = False):
        """_summary_

        Parameters
        ----------
        phiy : float
            _description_
        My : float
            _description_
        phiu : float
            _description_
        plot : bool, optional
            _description_, by default False

        Returns
        -------
        _type_
            _description_
        """

        phi = self.phi
        M = self.M
        bu = np.argmin(np.abs(phiu - phi))
        Q = np.trapz(M[: bu + 1], phi[: bu + 1])
        k = My / phiy
        Phi_eq = (k * phiu - np.sqrt((k * phiu) ** 2 - 2 * k * Q)) / k
        M_eq = k * Phi_eq

        M_new = np.insert(M[0: bu + 1], 0, 0, axis=None)
        Phi_new = np.insert(phi[0: bu + 1], 0, 0, axis=None)

        if plot:
            _, ax = plt.subplots(1, 1, figsize=(10, 10 * 0.618))
            ax.plot(Phi_new, M_new, lw=3, c="#2529d8")
            ax.plot([0, phiy, Phi_eq, phiu],
                    [0, My, M_eq, M_eq],
                    lw=3, c='#de0f17',)
            ax.plot(phiy, My, "o", ms=12, mec="black", mfc='red')
            ax.plot(Phi_eq, M_eq, "o", ms=12, mec="black", mfc='red')
            ax.set_title("$M-\phi$", fontsize=28,)
            ax.set_xlabel("$\phi$", fontsize=25)
            ax.set_ylabel("$M$", fontsize=25)
            plt.xticks(fontsize=15)
            plt.yticks(fontsize=15)
            ax.spines["bottom"].set_linewidth(1.2)
            ax.spines["left"].set_linewidth(1.2)
            ax.spines["right"].set_linewidth(1.2)
            ax.spines["top"].set_linewidth(1.2)
            plt.gcf().subplots_adjust(bottom=0.15)
            plt.show()
        return Phi_eq, M_eq


def _create_model(sec_tag):
    ops.model('basic', '-ndm', 3, '-ndf', 6)
    ops.node(1, 0.0, 0.0, 0.0)
    ops.node(2, 0.0, 0.0, 0.0)
    ops.fix(1, 1, 1, 1, 1, 1, 1)
    ops.fix(2, 0, 1, 1, 1, 0, 0)
    ops.element('zeroLengthSection', 1, 1, 2, sec_tag)


def _create_axial_resp(p):
    ops.timeSeries('Constant', 1)
    ops.pattern('Plain', 1, 1)
    ops.load(2, p, 0, 0, 0, 0, 0)    # nd  FX,  FY, Fz, MX, MY, MZ
    ops.wipeAnalysis()
    ops.system('SparseGeneral', '-piv')
    ops.constraints('Plain')
    ops.numberer('Plain')
    ops.test('NormDispIncr', 1.0e-12, 10, 3)
    ops.algorithm('Newton')
    ops.integrator('LoadControl', 1 / 10)
    ops.analysis('Static')
    ops.analyze(10)
    ops.loadConst('-time', 0.0)


def _analyze(sec_tag,
             P=0,
             axis="y",
             max_phi=1,
             incr_phi=1e-4,
             stop_ratio=0.7,
             smart_analyze=True):
    _create_model(sec_tag=sec_tag)
    if P != 0:
        _create_axial_resp(P)
    ops.timeSeries('Linear', 2)
    ops.pattern('Plain', 2, 2)
    if axis.lower() == "y":
        dof = 5
        ops.load(2, 0, 0, 0, 0, 1, 0)
    elif axis.lower() == "z":
        dof = 6
        ops.load(2, 0, 0, 0, 0, 0, 1)
    else:
        raise ValueError("Only supported axis = y or z!")
    M = [0]
    PHI = [0]
    FIBER_RESPONSES = [0]
    if smart_analyze:
        protocol = [max_phi]
        userControl = {
            "analysis": "Static",
            "testType": "NormDispIncr",
            "testTol": 1.0e-10,
            "relaxation": 0.5,
            "minStep": 1.0e-8,
            "printPer": 10,
            "debugMode": False,
        }
        analysis = SmartAnalyze(analysis_type="Static", **userControl)
        segs = analysis.static_split(protocol, maxStep=incr_phi)
        ii = 0
        while True:
            seg = segs[ii]
            ii += 1
            analysis.StaticAnalyze(2, dof, seg)
            curr_M = ops.getLoadFactor(2)
            curr_Phi = ops.nodeDisp(2, dof)
            cond1 = np.abs(curr_M) < np.max(np.abs(M)) * (stop_ratio - 0.02)
            cond2 = np.abs(curr_Phi) > max_phi
            if cond1 or cond2:
                break
            PHI.append(ops.nodeDisp(2, dof))
            M.append(curr_M)
            FIBER_RESPONSES.append(_get_fiber_sec_data(ele_tag=1))

    else:
        ops.integrator('DisplacementControl', 2, dof, incr_phi)
        while True:
            ops.analyze(1)
            curr_M = ops.getLoadFactor(2)
            curr_Phi = ops.nodeDisp(2, dof)
            cond1 = np.abs(curr_M) < np.max(np.abs(M)) * (stop_ratio - 0.02)
            cond2 = np.abs(curr_Phi) > max_phi
            if cond1 or cond2:
                break
            PHI.append(ops.nodeDisp(2, dof))
            M.append(curr_M)
            FIBER_RESPONSES.append(_get_fiber_sec_data(ele_tag=1))
    FIBER_RESPONSES[0] = FIBER_RESPONSES[1] * 0
    return np.abs(PHI), np.abs(M), np.array(FIBER_RESPONSES)


def _get_fiber_sec_data(ele_tag: int):
    fiber_data = ops.eleResponse(ele_tag, "section", "fiberData2")
    # From column 1 to 6: "yCoord", "zCoord", "area", 'mat', "stress", "strain"
    fiber_data = np.array(fiber_data).reshape((-1, 6))
    return fiber_data
