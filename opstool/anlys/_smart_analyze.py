# -*- coding: utf-8 -*-
import time

import numpy as np
import openseespy.opensees as ops
from rich import print
from typing import Union

from ..utils import get_random_color


class SmartAnalyze:
    """The SmartAnalyze is a class to provide OpenSeesPy users an easier
    way to conduct analyses.
    Original Tcl version Author: Dr. Dong Hanlin, see
    `here <https://github.com/Hanlin-Dong/SmartAnalyze/>`__.
    Here's the converted python version, with some modifications.

    Parameters
    ---------------------
    analysis_type: str, default="Transient"
        Assign the analysis type, "Transient" or "Static".

    Other Parameters that control convergence
    ----------------------------------------------

    TEST RELATED:
    ===============
    testType: str, default="EnergyIncr"
        Identical to the testType in OpenSees test command.
        Choices see `test command <https://opensees.berkeley.edu/wiki/index.php/Test_Command>`__
    testTol: float, default=1.0e-10
        The initial test tolerance set to the OpenSees test command.
        If tryLooseTestTol is set to True, the test tolerance can be loosened.
    testIterTimes: int, default=10
        The initial number of test iteration times.
        If tryAddTestTimes is set to True, the number of test times can be enlarged.
    testPrintFlag: int, default=0
        The test print flag in OpenSees ``test`` command.
    tryAddTestTimes: bool, default=False
        If True, the number of test times will be enlarged if the last test norm is smaller than `normTol`,
        the enlarged number is specified in `testIterTimesMore`.
        Otherwise, the number of test times will always be equal to `testIterTimes`.
    normTol: float, default=1.e3
        Only useful when tryAddTestTimes is True.
        If unconverged, the last norm of test will be compared to `normTol`.
        If the norm is smaller, the number of test times will be enlarged.
    testIterTimesMore: int, default=50
        Only useful when tryaddTestTimes is True.
        If unconverge and norm are ok, the test iteration times will be set to this number.
    tryLooseTestTol: bool, default=False
        If this is set to True, if unconverge at a minimum step,
        the test tolerance will be loosened to the number specified by `looseTestTolTo`.
        The step will be set back.
    looseTestTolTo: float, default= 100 * initial test tolerance
        Only useful if tryLooseTestTol is True.
        If unconvergance at the min step, the test tolerance will be set to this value.

    ALGORITHM RELATED:
    ===================
    tryAlterAlgoTypes: bool, default=False
        If True, different algorithm types specified
        in `algoTypes` will be tried during unconvergance.
        If False, the first algorithm type specified in `algoTypes`
        will be used.
    algoTypes: list[int], default=[40, 10, 20, 30, 50, 60, 70, 90]
        A list of flags of the algorithms to be used during unconvergance.
        The integer flag is documented in the following section.
        Only useful when tryAlterAlgoTypes is True.
        The first flag will be used by default when tryAlterAlgoTypes is False.
        The algorithm command in the model will be ignored.
        If you need another algorithm, try a user-defined algorithm. See the following section.
    UserAlgoArgs: list,
        User-defined algorithm parameters, 100 is required in algoTypes,
        and the parameters must be included in the list, for example:
        algoTypes = [10, 20, 100],
        UserAlgoArgs = ["KrylovNewton", "-iterate", "initial", "-maxDim", 20]

    **Algorithm type flag reference**

    .. list-table:: Algorithm type flag reference
       :widths: 30 30
       :header-rows: 1

       * - Flags
         - Algorithm
       * - 0
         - Linear
       * - 1
         - Linear -initial
       * - 2
         - Linear -secant
       * - 3
         - Linear -factorOnce
       * - 4
         - Linear -initial -factorOnce
       * - 5
         - Linear -secant -factorOnce
       * - 10
         - Newton
       * - 11
         - Newton -initial
       * - 12
         - Newton -initialThenCurrent
       * - 13
         - Newton -Secant
       * - 20
         - NewtonLineSearch
       * - 21
         - NewtonLineSearch -type Bisection
       * - 22
         - NewtonLineSearch -type Secant
       * - 23
         - NewtonLineSearch -type RegulaFalsi
       * - 24
         - NewtonLineSearch -type LinearInterpolated
       * - 25
         - NewtonLineSearch -type InitialInterpolated
       * - 30
         - ModifiedNewton
       * - 31
         - ModifiedNewton -initial
       * - 32
         - ModifiedNewton -secant
       * - 40
         - KrylovNewton
       * - 41
         - KrylovNewton -iterate initial
       * - 42
         - KrylovNewton -increment initial
       * - 43
         - KrylovNewton -iterate initial -increment initial
       * - 44
         - KrylovNewton -maxDim 10
       * - 45
         - KrylovNewton -iterate initial -increment initial -maxDim 10
       * - 50
         - SecantNewton
       * - 51
         - SecantNewton -iterate initial
       * - 52
         - SecantNewton -increment initial
       * - 53
         - SecantNewton -iterate initial -increment initial
       * - 60
         - BFGS
       * - 61
         - BFGS -initial
       * - 62
         - BFGS -secant
       * - 70
         - Broyden
       * - 71
         - Broyden -initial
       * - 72
         - Broyden -secant
       * - 80
         - PeriodicNewton
       * - 81
         -  PeriodicNewton -maxDim 10
       * - 90
         -  ExpressNewton
       * - 91
         - ExpressNewton -InitialTangent
       * - 100
         - User-defined0

    STEP SIZE RELATED:
    ===================
    initialStep: float, default=None
        Specifying the initial Step length to conduct analysis.
        If None, equal to `dt`.
    relaxation: float, between 0 and 1, default=0.5
        A factor that is multiplied by each time
        the step length is shortened.
    minStep: float, default=1.e-6
        The step tolerance when shortening the step length.
        If step length is smaller than minStep, special ways to converge the model will be used
        according to `try-` flags.

    LOGGING RELATED:
    ===================
    printPer: int, default=50
        Print to the console every several trials.
    debugMode: bool, default=False
        Print as much information as possible.

    Examples
    ---------
    The following example demonstrates how to use the SmartAnalyze class.

    .. Note::

        * ``test()`` and ``algorithm()`` will run automatically in ``SmartAnalyze``;
        * Static analysis only supports displacement control;
        * Commands such as ``integrator()`` must be defined outside ``SmartAnalyze`` for ransient analysis.

    Example 1: Basic usage for Transient

    >>> import opstool as opst
    >>> ops.constraints('Transformation')
    >>> ops.numberer('Plain')
    >>> ops.system('BandGeneral')
    >>> ops.integrator('Newmark', 0.5, 0.25)
    >>> analysis = opst.anlys.SmartAnalyze(analysis_type="Transient")
    >>> npts, dt = 1000, 0.01
    >>> segs = analysis.transient_split(npts)
    >>> for seg in segs:
    >>>     analysis.TransientAnalyze(dt)

    Example 2: Basic usage for Static

    >>> import opstool as opst
    >>> ops.constraints('Transformation')
    >>> ops.numberer('Plain')
    >>> ops.system('BandGeneral')
    >>> protocol=[1, -1, 1, -1, 0]
    >>> analysis = opst.anlys.SmartAnalyze(analysis_type="Static")
    >>> segs = analysis.static_split(protocol, 0.01)
    >>> print(segs)
    >>> for seg in segs:
    >>>     analysis.StaticAnalyze(node=1, dof=2, seg=seg)  # node tag 1, dof 2

    Example 3: change control parameters

    >>> analysis = opst.anlys.SmartAnalyze(
    >>>   analysis_type="Transient",
    >>>   tryAlterAlgoTypes=True,
    >>>   algoTypes=[40, 30, 20],
    >>>   printPer=20,
    >>>)
    """

    def __init__(self, analysis_type="Transient", **kargs):
        if analysis_type not in ("Transient", "Static"):
            raise ValueError("analysis_type must Transient or Static!")
        # default
        self.control_args = {
            "analysis": analysis_type,
            "testType": "EnergyIncr",
            "testTol": 1.0e-10,
            "testIterTimes": 10,
            "testPrintFlag": 0,
            "tryAddTestTimes": False,
            "normTol": 1000,
            "testIterTimesMore": 50,
            "tryLooseTestTol": False,
            "looseTestTolTo": 1e-3,
            "tryAlterAlgoTypes": False,
            "algoTypes": [40, 10, 20, 30, 50, 60, 70, 90],
            "UserAlgoArgs": None,
            "initialStep": None,
            "relaxation": 0.5,
            "minStep": 1.0e-6,
            "printPer": 50,
            "debugMode": False,
        }
        self.control_args["looseTestTolTo"] = 100 * self.control_args["testTol"]
        for name in kargs.keys():
            if name not in self.control_args.keys():
                raise ValueError(f"Arg {name} error, valid args are: {self.control_args.keys()}!")
        self.control_args.update(kargs)

        self.analysis_type = analysis_type
        self.eps = 1.0e-12
        self.logo = "[bold magenta]SmartAnalyze:[/bold magenta]"

        # initial test commands
        ops.test(
            self.control_args["testType"],
            self.control_args["testTol"],
            self.control_args["testIterTimes"],
            self.control_args["testPrintFlag"],
        )
        # initial algorithm
        self._setAlgorithm(self.control_args["algoTypes"][0], self.control_args["UserAlgoArgs"])

        # Since the intelligent static analysis may reset the integrator,
        # the sensitivity analysis algorithm needs to be reset
        self.sensitivity_algorithm = None

        self.current_args = {
            "startTime": time.time(),
            "algoIndex": 0,
            "testIterTimes": self.control_args["testIterTimes"],
            "testTol": self.control_args["testTol"],
            "counter": 0,
            "progress": 0,
            "segs": 0,
            "step": 0.0,
            "node": 0,
            "dof": 0,
        }

    def transient_split(self, npts: int):
        """Step Segmentation for Transient Analysis.
        The main purpose of this function is to tell the program the total number of analysis steps to show progress.
        However, this is not necessary.

        Parameters
        ----------
        npts : int
            Total steps for transient analysis.

        Returns
        -------
        A list to loop.
        """
        self.current_args["segs"] = npts
        return list(range(1, npts + 1))

    def static_split(self, targets: Union[list, tuple, np.ndarray], maxStep: float = None):
        """Returns a sequence of substeps for static analysis, for use in outer analysis loops.
        It is not necessary to use this method if you already have a load sequence.

        Parameters
        ----------
        targets:  Union[list, tuple, numpy.ndarray]
            A list of target displacements, the first element must be positive.
        maxStep: float, default=None
            The maximum step size in the displacement control.
            If None, targets[1] - targets[0].

        Returns
        -------
        segs: list
            A sequence of substeps for static analysis.

        """
        targets = np.atleast_1d(targets)
        if targets.ndim != 1:
            raise ValueError("targets must be 1D!")
        if len(targets) == 1 and maxStep is None:
            raise ValueError(
                "When targets has only one element, maxStep must be passed in!"
            )
        if targets[0] != 0.0:
            targets = np.insert(targets, 0, 0.0)
        if maxStep is None:
            maxStep = targets[1] - targets[0]
        # calcuate the whole distance; divide the whole process into segments.
        distance = 0
        segs = []
        for i in range(len(targets) - 1):
            section = targets[i + 1] - targets[i]
            if abs(section) < self.eps:
                continue
            elif section > 0:
                positive = True
            else:
                positive = False

            distance = distance + np.abs(section)

            if positive:
                j = 0
                while (section - j * maxStep) > maxStep + self.eps:
                    segs.append(maxStep)
                    j += 1
                segs.append(section - j * maxStep)
            else:
                j = 0
                while (-section - j * maxStep) > maxStep + self.eps:
                    segs.append(-maxStep)
                    j += 1
                segs.append(section + j * maxStep)
        self.current_args["segs"] = len(segs)
        return segs

    def _get_time(self):
        return time.time() - self.current_args["startTime"]

    def set_sensitivity_algorithm(self, algorithm: str = "-computeAtEachStep"):
        """Set analysis sensitivity algorithm. Since the Smart Static Analysis may reset the integrator,
        the sensitivity analysis algorithm will need to be reset afterwards.

        Parameters
        -----------
        algorithm: Sensitivity analysis algorithm, default: "-computeAtEachStep".
            Optional: "-computeAtEachStep" or "-computeByCommand".

        Return
        -------
        None
        """
        if algorithm not in ["-computeAtEachStep", "-computeByCommand"]:
            raise ValueError("algorithm must be '-computeAtEachStep' or '-computeByCommand'")
        self.sensitivity_algorithm = algorithm

    def _run_sensitivity_algorithm(self):
        if self.sensitivity_algorithm is not None:
            ops.sensitivityAlgorithm(self.sensitivity_algorithm)

    def TransientAnalyze(self, dt: float, print_info: bool = True):
        """Single Step Transient Analysis.

        Parameters
        ----------
        dt : float
            Time Step.
        print_info: bool, default=True
            If True, print info.

        Returns
        -------
        Return 0 if successful, otherwise returns a negative number.
        """
        if self.control_args["analysis"] != "Transient":
            raise ValueError("Transient! Please check parameter input!")
        self.control_args["initialStep"] = dt

        ops.analysis(self.control_args["analysis"])

        return self._analyze(print_info)

    def StaticAnalyze(self, node: int, dof: int, seg: float, print_info: bool = True):
        """Single step static analysis and applies to displacement control only.

        Parameters
        ----------
        node : int
            The node tag in the displacement control.
        dof : int
            The dof in the displacement control.
        seg : float
            Each load step, i.e., each element returned by static_split.
        print_info: bool, default=True
            If True, print info.

        Returns
        -------
        Return 0 if successful, otherwise returns a negative number.
        """
        if self.control_args["analysis"] != "Static":
            raise ValueError("Static! Please check parameter input!")
        self.control_args["initialStep"] = seg
        self.current_args["node"] = node
        self.current_args["dof"] = dof
        self.current_args["step"] = seg

        ops.integrator("DisplacementControl", node, dof, seg)
        ops.analysis(self.control_args["analysis"])

        # reset sensitivity analysis algorithm
        self._run_sensitivity_algorithm()

        return self._analyze(print_info)

    def _analyze(self, verbose):
        initial_step = self.control_args["initialStep"]
        ok = self._analyze_one_step(initial_step, verbose)
        if ok < 0:
            ok = self._try_add_test_times(initial_step, verbose)
        if ok < 0:
            ok = self._try_alter_algo_types(initial_step, verbose)
        if ok < 0:
            ok = self._try_relax_step(initial_step, verbose)
        if ok < 0:
            ok = self._try_loose_test_tol(initial_step, verbose)

        if ok < 0:
            color = get_random_color()
            value = f"[bold {color}]{self._get_time():.3f}[/bold {color}]"
            print(f">>> {self.logo} Analyze failed. Time consumption: {value} s.")
            return ok

        self.current_args["progress"] += 1
        self.current_args["counter"] += 1
        print_info = True if self.control_args["debugMode"] else verbose
        if print_info:
            if self.current_args["segs"] > 0:
                color = get_random_color()
                if self.control_args["debugMode"]:
                    value1 = f"[bold {color}]{100 * self.current_args['progress'] / self.current_args['segs']:.3f}[/bold {color}]"
                    value2 = f"[bold {color}]{self._get_time():.3f}[/bold {color}]"
                    print(
                        f"* {self.logo} progress {value1} %. Time consumption: {value2} s."
                    )
                elif self.current_args["counter"] >= self.control_args["printPer"]:
                    value1 = f"[bold {color}]{100 * self.current_args['progress'] / self.current_args['segs']:.3f}[/bold {color}]"
                    value2 = f"[bold {color}]{self._get_time():.3f}[/bold {color}]"
                    print(
                        f"* {self.logo} progress {value1} %. Time consumption: {value2} s."
                    )
                    self.current_args["counter"] = 0

        # Finally
        if (self.current_args["segs"] > 0) and (
                self.current_args["progress"] >= self.current_args["segs"]
        ):
            color = get_random_color()
            value = f"[bold {color}]{self._get_time():.3f}[/bold {color}]"
            print(
                f">>> {self.logo} [{color}]Successfully finished[/{color}]! Time consumption: {value} s."
            )
        return 0

    def _analyze_one_step(self, step: float, verbose: bool):
        if self.analysis_type == "Static":
            if verbose:
                color = get_random_color()
                print(
                    f">>> {self.logo} Setting step to [bold {color}]%.3e[/bold {color}]\n"
                    % step
                )
            ops.integrator(
                "DisplacementControl",
                self.current_args["node"],
                self.current_args["dof"],
                step
            )

            # reset sensitivity analysis algorithm
            self._run_sensitivity_algorithm()

            ok = ops.analyze(1)
        else:
            ok = ops.analyze(1, step)

        self.current_args["step"] = step

        return ok

    def _try_add_test_times(self, step, verbose):
        if not self.control_args["tryAddTestTimes"]:
            return -1
        norm = ops.testNorm()
        color = get_random_color()
        if norm[-1] < self.control_args["normTol"]:
            if verbose:
                print(
                    f">>> {self.logo} Adding test times to [bold {color}]%i[/bold {color}].\n"
                    % (self.control_args["testIterTimesMore"])
                )
            ops.test(
                self.control_args["testType"],
                self.control_args["testTol"],
                self.control_args["testIterTimesMore"],
                self.control_args["testPrintFlag"]
            )
            ok = self._analyze_one_step(step, verbose)
            if ok < 0:  # reback
                ops.test(
                    self.control_args["testType"],
                    self.control_args["testTol"],
                    self.control_args["testIterTimes"],
                    self.control_args["testPrintFlag"]
                )
            return ok
        else:
            if verbose:
                print(
                    f">>> {self.logo} Not adding test times for norm [bold {color}]%.3e[/bold {color}].\n"
                    % (norm[-1])
                )
            return -1

    def _try_alter_algo_types(self, step, verbose):
        if not self.control_args["tryAlterAlgoTypes"]:
            return -1

        if len(self.control_args["algoTypes"]) <= 1:
            return -1

        ok = -1
        for algo_flag in self.control_args["algoTypes"][1:]:
            color = get_random_color()
            if verbose:
                print(
                    f">>> {self.logo} Setting algorithm to "
                    f"[bold {color}]{algo_flag}[/bold {color}].\n"
                )
            self._setAlgorithm(
                algo_flag,
                self.control_args["UserAlgoArgs"]
            )
            ok = self._analyze_one_step(step, verbose)
            if ok == 0:
                break
        if ok < 0:  # reback
            self._setAlgorithm(
                self.control_args["algoTypes"][0],
                self.control_args["UserAlgoArgs"]
            )
        return ok

    def _try_relax_step(self, step, verbose):
        alpha = self.control_args["relaxation"]
        min_step = self.control_args["minStep"]
        step_try = step * alpha  # The current step size we're trying to use
        step_remaining = step  # How much of the time step is left to complete

        ok = -1
        while step_remaining > self.eps:
            if step_try < min_step:
                color = get_random_color()
                print(
                    f">>> {self.logo} current step [bold {color}]%.3e[/bold {color}] beyond the min step!\n"
                    % step_try
                )
                return -1

            if step_try > step_remaining:
                step_try = step_remaining  # avoid overshooting

            # Try to run one substep
            ok = self._analyze_one_step(step_try, verbose)

            if ok == 0:
                step_remaining -= step_try
                # Try to increase next step size by relaxing alpha
                step_try = step_remaining
            else:
                step_try *= alpha
                if verbose:
                    color = get_random_color()
                    print(
                        f">>> {self.logo} Dividing the current step [bold {color}]%.3e into %.3e and %.3e[/bold {color}]\n"
                        % (step, step_try, step_remaining)
                    )
        return ok

    def _try_loose_test_tol(self, step, verbose):
        if not self.control_args["tryLooseTestTol"]:
            return -1
        if verbose:
            color = get_random_color()
            print(
                f"!!! {self.logo} Warning: [bold {color}]Loosing test tolerance[/bold {color}]\n"
            )
        ops.test(
            self.control_args["testType"],
            self.control_args["looseTestTolTo"],
            self.control_args["testIterTimes"],
            self.control_args["testPrintFlag"]
        )
        return self._analyze_one_step(step, verbose)

    def _setAlgorithm(self, algotype, user_algo_args: list = None):
        color = get_random_color()

        def case0():
            print(
                f"> {self.logo} Setting algorithm to  [bold {color}]Linear ...[/bold {color}]"
            )
            ops.algorithm("Linear")

        def case1():
            print(
                f"> {self.logo} Setting algorithm to  [bold {color}]Linear -initial ...[/bold {color}]"
            )
            ops.algorithm("Linear", "-Initial")

        def case2():
            print(
                f"> {self.logo} Setting algorithm to  [bold {color}]Linear -secant ...[/bold {color}]"
            )
            ops.algorithm("Linear", "-Secant")

        def case3():
            print(
                f"> {self.logo} Setting algorithm to  [bold {color}]Linear -factorOnce ...[/bold {color}]"
            )
            ops.algorithm("Linear", "-FactorOnce")

        def case4():
            print(
                f"> {self.logo} Setting algorithm to  [bold {color}]Linear -initial -factorOnce ...[/bold {color}]"
            )
            ops.algorithm("Linear", "-Initial", "-FactorOnce")

        def case5():
            print(
                f"> {self.logo} Setting algorithm to  [bold {color}]Linear -secant -factorOnce ...[/bold {color}]"
            )
            ops.algorithm("Linear", "-Secant", "-FactorOnce")

        def case10():
            print(
                f"> {self.logo} Setting algorithm to  [bold {color}]Newton ...[/bold {color}]"
            )
            ops.algorithm("Newton")

        def case11():
            print(
                f"> {self.logo} Setting algorithm to  [bold {color}]Newton -initial ...[/bold {color}]"
            )
            ops.algorithm("Newton", "-Initial")

        def case12():
            print(
                f"> {self.logo} Setting algorithm to  [bold {color}]Newton -initialThenCurrent ...[/bold {color}]"
            )
            ops.algorithm("Newton", "-intialThenCurrent")

        def case13():
            print(
                f"> {self.logo} Setting algorithm to  [bold {color}]Newton -Secant ...[/bold {color}]"
            )
            ops.algorithm("Newton", "-Secant")

        def case20():
            print(
                f"> {self.logo} Setting algorithm to  [bold {color}]NewtonLineSearch ...[/bold {color}]"
            )
            ops.algorithm("NewtonLineSearch")

        def case21():
            print(
                f"> {self.logo} Setting algorithm to "
                f"[bold {color}]NewtonLineSearch -type Bisection ...[/bold {color}]"
            )
            ops.algorithm("NewtonLineSearch", "-type", "Bisection")

        def case22():
            print(
                f"> {self.logo} Setting algorithm to "
                f"[bold {color}]NewtonLineSearch -type Secant ...[/bold {color}]"
            )
            ops.algorithm("NewtonLineSearch", "-type", "Secant")

        def case23():
            print(
                f"> {self.logo} Setting algorithm to "
                f"[bold {color}]NewtonLineSearch -type RegulaFalsi ...[/bold {color}]"
            )
            ops.algorithm("NewtonLineSearch", "-type", "RegulaFalsi")

        def case24():
            print(
                f"> {self.logo} Setting algorithm to "
                f"[bold {color}]NewtonLineSearch -type LinearInterpolated ...[/bold {color}]"
            )
            ops.algorithm("NewtonLineSearch", "-type", "LinearInterpolated")

        def case25():
            print(
                f"> {self.logo} Setting algorithm to "
                f"[bold {color}]NewtonLineSearch -type InitialInterpolated ...[/bold {color}]"
            )
            ops.algorithm("NewtonLineSearch", "-type", "InitialInterpolated")

        def case30():
            print(
                f"> {self.logo} Setting algorithm to  [bold {color}]Modified Newton ...[/bold {color}]"
            )
            ops.algorithm("ModifiedNewton")

        def case31():
            print(
                f"> {self.logo} Setting algorithm to  [bold {color}]ModifiedNewton -initial ...[/bold {color}]"
            )
            ops.algorithm("ModifiedNewton", "-initial")

        def case32():
            print(
                f"> {self.logo} Setting algorithm to  [bold {color}]ModifiedNewton -secant ...[/bold {color}]"
            )
            ops.algorithm("ModifiedNewton", "-secant")

        def case40():
            print(
                f"> {self.logo} Setting algorithm to  [bold {color}]KrylovNewton ...[/bold {color}]"
            )
            ops.algorithm("KrylovNewton")

        def case41():
            print(
                f"> {self.logo} Setting algorithm to "
                f"[bold {color}]KrylovNewton -iterate initial ...[/bold {color}]"
            )
            ops.algorithm("KrylovNewton", "-iterate", "initial")

        def case42():
            print(
                f"> {self.logo} Setting algorithm to "
                f"[bold {color}]KrylovNewton -increment initial ...[/bold {color}]"
            )
            ops.algorithm("KrylovNewton", "-increment", "initial")

        def case43():
            print(
                f"> {self.logo} Setting algorithm to "
                f"[bold {color}]KrylovNewton -iterate initial -increment initial ...[/bold {color}]"
            )
            ops.algorithm(
                "KrylovNewton", "-iterate", "initial", "-increment", "initial"
            )

        def case44():
            print(
                f"> {self.logo} Setting algorithm to  [bold {color}]KrylovNewton -maxDim 10[/bold {color}]"
            )
            ops.algorithm("KrylovNewton", "-maxDim", 10)

        def case45():
            print(
                f"> {self.logo} Setting algorithm to "
                f"[bold {color}]KrylovNewton -iterate initial -increment initial -maxDim 10[/bold {color}]"
            )
            ops.algorithm(
                "KrylovNewton",
                "-iterate",
                "initial",
                "-increment",
                "initial",
                "-maxDim",
                10,
            )

        def case50():
            print(
                f"> {self.logo} Setting algorithm to  [bold {color}]SecantNewton ...[/bold {color}]"
            )
            ops.algorithm("SecantNewton")

        def case51():
            print(
                f"> {self.logo} Setting algorithm to "
                f"[bold {color}]SecantNewton -iterate initial ...[/bold {color}]"
            )
            ops.algorithm("SecantNewton", "-iterate", "initial")

        def case52():
            print(
                f"> {self.logo} Setting algorithm to "
                f"[bold {color}]SecantNewton -increment initial  ...[/bold {color}]"
            )
            ops.algorithm("SecantNewton", "-increment", "initial")

        def case53():
            print(
                f"> {self.logo} Setting algorithm to "
                f"[bold {color}]SecantNewton -iterate initial -increment initial ...[/bold {color}]"
            )
            ops.algorithm(
                "SecantNewton", "-iterate", "initial", "-increment", "initial"
            )

        def case60():
            print(
                f"> {self.logo} Setting algorithm to  [bold {color}]BFGS ...[/bold {color}]"
            )
            ops.algorithm("BFGS")

        def case61():
            print(
                f"> {self.logo} Setting algorithm to  [bold {color}]BFGS -initial...[/bold {color}]"
            )
            ops.algorithm("BFGS", "-initial")

        def case62():
            print(
                f"> {self.logo} Setting algorithm to  [bold {color}]BFGS -secant ...[/bold {color}]"
            )
            ops.algorithm("BFGS", "-secant")

        def case70():
            print(
                f"> {self.logo} Setting algorithm to  [bold {color}]Broyden ...[/bold {color}]"
            )
            ops.algorithm("Broyden")

        def case71():
            print(
                f"> {self.logo} Setting algorithm to  [bold {color}]Broyden -initial ...[/bold {color}]"
            )
            ops.algorithm("Broyden", "-initial")

        def case72():
            print(
                f"> {self.logo} Setting algorithm to  [bold {color}]Broyden -secant ...[/bold {color}]"
            )
            ops.algorithm("Broyden", "-secant")

        def case80():
            print(
                f"> {self.logo} Setting algorithm to  [bold {color}]PeriodicNewton ...[/bold {color}]"
            )
            ops.algorithm("PeriodicNewton")

        def case81():
            print(
                f"> {self.logo} Setting algorithm to  [bold {color}]PeriodicNewton -maxDim, 10 ...[/bold {color}]"
            )
            ops.algorithm("PeriodicNewton", "-maxDim", 10)

        def case90():
            print(
                f"> {self.logo} Setting algorithm to  [bold {color}]ExpressNewton ...[/bold {color}]"
            )
            ops.algorithm("ExpressNewton")

        def case91():
            print(
                f"> {self.logo} Setting algorithm to  [bold {color}]ExpressNewton -InitialTangent ...[/bold {color}]"
            )
            ops.algorithm("ExpressNewton", "-InitialTangent")

        def case100():
            # User algorithm0
            if user_algo_args is not None:
                ops.algorithm(*user_algo_args)

        def default():
            raise ValueError("!!! SmartAnalyze: ERROR! WRONG Algorithm Type!")

        switch = {
            0: case0,
            1: case1,
            2: case2,
            3: case3,
            4: case4,
            5: case5,
            10: case10,
            11: case11,
            12: case12,
            13: case13,
            20: case20,
            21: case21,
            22: case22,
            23: case23,
            24: case24,
            25: case25,
            30: case30,
            31: case31,
            32: case32,
            40: case40,
            41: case41,
            42: case42,
            43: case43,
            44: case44,
            45: case45,
            50: case50,
            51: case51,
            52: case52,
            53: case53,
            60: case60,
            61: case61,
            62: case62,
            70: case70,
            71: case71,
            72: case72,
            80: case80,
            81: case81,
            90: case90,
            91: case91,
            100: case100,
        }

        switch.get(algotype, default)()
