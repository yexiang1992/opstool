# -*- coding: utf-8 -*-
import time

import numpy as np
import openseespy.opensees as ops
from rich import print
from ..utils import _get_random_color


class SmartAnalyze:
    """
    The SmartAnalyze is a class to provide OpenSeesPy users a easier
    way to conduct analyses.
    Original Tcl version Author: Dr. Dong Hanlin
    (http://www.hanlindong.com/2019/opensees-converge/)
    Here's the converted python version, with some modifications.

    Parameters
    ---------------------
    analysis_type: str, default="Transient"
        Assign the analysis type, "Transient" or "Static".

    Other Parameters that control convergence
    ----------------------------------------------

    TEST RELATED:
    ++++++++++++++
    testType: str, default="EnergyIncr"
        Identical to the testType in OpenSees test command.
        Choices see http://opensees.berkeley.edu/wiki/index.php/Test_Command.
    testTol: float, default=1.0e-12
        The initial test tolerance set to the OpenSees test command.
        If tryLooseTestTol is set to True, the test tolerance can be loosen.
    testIterTimes: int, default=10
        The initial number of test iteration times.
        If tryAddTestTimes is set to True, the number of test times can be enlarged.
    testPrintFlag: int, default=0
        The test print flag in OpenSees Test command.
        Choices see http://opensees.berkeley.edu/wiki/index.php/Test_Command.
    tryAddTestTimes: bool, default=False
        If True,the number of test times will be enlarged if the last test norm is smaller than `normTol`,
        the enlarged number is specified in `testIterTimesMore`.
        Otherwise, the number of test times will always be equal to `testIterTimes`.
    normTol: float, default=1.e3
        Only useful when tryAddTestTimes is True.
        If unconverge, the last norm of test will be compared to `normTol`.
        If the norm is smaller, the number of test times will be enlarged.
    testIterTimesMore: int, default=50
        Only useful when tryaddTestTimes is True.
        If unconverge and norm is ok, the test iteration times will be set to this number.
    tryLooseTestTol: bool, default=False
        If this is set to True, if unconverge at minimum step,
        the test tolerance will be loosen to the number specified by `looseTestTolTo`.the step will be set back.
    looseTestTolTo: float, default=1.0
        Only useful if tryLooseTestTol is True.
        If unconvergance at the min step, the test tolerance will be set to this value.

    ALGORITHM RELATED:
    +++++++++++++++++++++++
    tryAlterAlgoTypes: bool, default=False
        If True, different algorithm types specified
        in `algoTypes` will be tried during unconvergance.
        If False, the first algorithm type specified in `algoTypes`
        will be used.
    algoTypes: list[int], default=[10, 20, 30, 40, 50]
        A list of flags of the algorithms to be used during unconvergance.
        The integer flag is documented in the following section.
        Only useful when tryAlterAlgoTypes is True.
        The first flag will be used by default.
        The algorithm command in the model will be ignored.
        If you need other algorithm, try a user-defined algorithm. See the following section.

    STEP RELATED:
    +++++++++++++++++++++++
    initialStep: float, default=None
        Specifying the initial Step length to conduct analysis.
        If None, equal to `dt`.
    relaxation: float, between 0 and 1, default=0.5
        A factor that is multiplied by each time
        the step length is shortened.
    minStep: float, default=1.e-6
        The step tolerance when shortening
        the step length.
        If step length is smaller than minStep, special ways to converge the model will be used
        according to `try-` flags.

    LOGGING RELATED:
    +++++++++++++++++++
    printPer: int, default=10
        Print to the console every several trials.
    debugMode: bool, default=False
        Print as much information as possible.

    .. tip::
        Algorithm type flag reference
        +++++++++++++++++++++++++++++++
        * 0:  Linear
        * 1:  Linear -initial
        * 2:  Linear -factorOnce
        * 10:  Newton
        * 11:  Newton -initial
        * 12:  Newton -initialThenCurrent
        * 20:  NewtonLineSearch
        * 21:  NewtonLineSearch -type Bisection
        * 22:  NewtonLineSearch -type Secant
        * 23:  NewtonLineSearch -type RegulaFalsi
        * 30:  ModifiedNewton
        * 31:  ModifiedNewton -initial
        * 40:  KrylovNewton
        * 41:  KrylovNewton -iterate initial
        * 42:  KrylovNewton -increment initial
        * 43:  KrylovNewton -iterate initial -increment initial
        * 44:  KrylovNewton -maxDim 6
        * 50:  SecantNewton
        * 51:  SecantNewton -iterate initial
        * 52:  SecantNewton -increment initial
        * 53:  SecantNewton -iterate initial -increment initial
        * 60:  BFGS
        * 70:  Broyden
        * 80:  PeriodicNewton
        * 90:  User-defined0

    Examples
    ---------
    .. note::
        ``test()`` and ``algorithm()`` will run automatically in ``SmartAnalyze``,
        but commands such as ``integrator()`` must be defined outside ``SmartAnalyze``.


    Example 1: Basic usage for Transient
    ++++++++++++++++++++++++++++++++++++++
    >>> import opstool as opst
    >>> ops.constraints('Transformation')
    >>> ops.numberer('Plain')
    >>> ops.system('BandGeneral')
    >>> ops.integrator('Newmark', 0.5, 0.25)
    >>> analysis = opst.SmartAnalyze(analysis_type="Transient")
    >>> npts, dt = 1000, 0.01
    >>> segs = analysis.transient_split(npts)
    >>> for seg in segs:
    >>>     analysis.TransientAnalyze(dt)

    Example 2: Basic usage for Static
    +++++++++++++++++++++++++++++++++++++
    >>> import opstool as opst
    >>> ops.constraints('Transformation')
    >>> ops.numberer('Plain')
    >>> ops.system('BandGeneral')
    >>> protocol=[1, -1, 1, -1, 0]
    >>> analysis = opst.SmartAnalyze(analysis_type="Static")
    >>> segs = analysis.static_split(protocol, 0.01)
    >>> for seg in segs:
    >>>     analysis.StaticAnalyze(1, 1, seg)

    Example 3: change control parameters
    ++++++++++++++++++++++++++++++++++++++
    >>> analysis = opst.SmartAnalyze(analysis_type="Transient",
    >>>                              algoTypes=[20, 30],
    >>>                              printPer=20,
    >>>                              tryAlterAlgoTypes=True,
    >>>                             )
    """

    def __init__(self, analysis_type="Transient", **kargs):
        if analysis_type not in ("Transient", "Static"):
            raise ValueError("analysis_type must Transient or Static!")
        # default
        self.control = {'analysis': analysis_type, 'testType': "EnergyIncr", 'testTol': 1.0e-12,
                        'testIterTimes': 10, 'testPrintFlag': 0, 'tryAddTestTimes': False,
                        'normTol': 1.0e3, 'testIterTimesMore': 50, 'tryLooseTestTol': False,
                        'looseTestTolTo': 1.0, 'tryAlterAlgoTypes': False, 'algoTypes': [10, 20, 30, 40, 50],
                        'initialStep': None, 'relaxation': 0.5, 'minStep': 1.0e-6,
                        'printPer': 10, 'debugMode': False}
        for name in kargs.keys():
            if name not in self.control.keys():
                raise ValueError(f"arg {name} error!")
        self.control.update(kargs)
        self.eps = 1.E-12
        self.logo = "[bold magenta]SmartAnalyze:[/bold magenta]"

        # initial test commands
        ops.test(self.control['testType'], self.control['testTol'],
                 self.control['testIterTimes'], self.control['testPrintFlag'])
        self._setAlgorithm(self.control['algoTypes'][0])

        self.current = {'startTime': time.time(), 'algoIndex': 0,
                        'testIterTimes': self.control['testIterTimes'],
                        'testTol': self.control['testTol'], 'counter': 0,
                        'progress': 0, 'segs': 0, 'step': 0.0,
                        'node': 0, 'dof': 0}

    def transient_split(self, npts: int):
        """Step Segmentation for Transient Analysis.

        Parameters
        ----------
        npts : int
            Total steps for transient analysis.

        Returns
        -------
        A list to loop.
        """
        self.current['segs'] = npts
        return list(range(1, npts + 1))

    def static_split(self, targets: list, maxStep: float = None):
        """Returns a sequence of substeps for static analysis, for use in outer analysis loops.

        Parameters
        ----------
        targets: list
            A list of target displacements, the first element must be positive.
        maxStep: float, default=None
            The maximum step length in the displacement control.
            If None, targets[1] - targets[0].

        Returns
        -------
        segs: list
            A sequence of substeps for static analysis.

        """
        targets = np.array(targets)
        if targets.ndim != 1:
            raise ValueError("targets must be 1D!")
        if len(targets) == 1 and maxStep is None:
            raise ValueError(
                "When targets has only one element, maxStep must be passed in!")
        if targets[0] != 0.0:
            targets = np.insert(targets, 0, 0)
        if maxStep is None:
            maxStep = targets[1] - targets[0]
        # calcuate whole distance; divide the whole process into segments.
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
        self.current['segs'] = len(segs)
        return segs

    def _get_time(self):
        return time.time() - self.current['startTime']

    def TransientAnalyze(self, dt: float):
        """Single Step Transient Analysis.

        Parameters
        ----------
        dt : float
            Time Step.

        Returns
        -------
        None
        """
        if self.control['analysis'] != "Transient":
            raise ValueError("Transient! Please check parameter set!")
        self.control['initialStep'] = dt

        ops.analysis(self.control['analysis'])

        ok = self._RecursiveAnalyze(self.control['initialStep'], 0, self.control['testIterTimes'],
                                    self.control['testTol'], self.control.copy(), self.current.copy())
        if ok < 0:
            color = _get_random_color()
            custime = f"[{color}]{self._get_time():.3f}[/{color}]"
            print(
                f">>> {self.logo} Analyze failed. Time consumption: {custime} s.")
            return ok

        self.current['progress'] += 1

        if self.control['debugMode']:
            if self.current['segs'] is not None:
                color = _get_random_color()
                custime = f"[{color}]{100 * self.current['progress'] / self.current['segs']:.3f}[/{color}]"
                print(f"*** {self.logo} progress {custime} %")

        if self.current['progress'] == self.current['segs']:
            color = _get_random_color()
            custime = f"[{color}]{self._get_time():.3f}[/{color}]"
            print(
                f">>> {self.logo} [{color}]Successfully finished[/{color}]! Time consumption: {custime} s.")
            return 0

    def StaticAnalyze(self, node: int, dof: int, seg: float):
        """Single Step Static Analysis.

        Parameters
        ----------
        node : int
            The node tag in the displacement control.
        dof : int
            The dof in the displacement control.
        seg : float
            Each load step, i.e. each element returned by static_split.

        Returns
        -------
        None
        """
        if self.control['analysis'] != "Static":
            raise ValueError("Static! Please check parameter set!")
        self.control['initialStep'] = seg
        self.current['node'] = node
        self.current['dof'] = dof
        self.current['step'] = seg

        ops.integrator('DisplacementControl', node, dof, seg)
        ops.analysis(self.control['analysis'])

        ok = self._RecursiveAnalyze(seg, 0, self.control['testIterTimes'], self.control['testTol'],
                                    self.control.copy(), self.current.copy())
        if ok < 0:
            color = _get_random_color()
            value = f"[bold {color}]{self._get_time():.3f}[/bold {color}]"
            print(
                f">>> {self.logo} Analyze failed. Time consumption: {value} s.")
            return ok
        self.current['progress'] += 1

        if self.control['debugMode']:
            color = _get_random_color()
            value = f"[bold {color}]{100 * self.current['progress'] / self.current['segs']:.2f}[/bold {color}]"
            print(f"*** {self.logo} progress {value} %")

        if self.current['progress'] == self.current['segs']:
            color = _get_random_color()
            value = f"[bold {color}]{self._get_time():.3f}[/bold {color}]"
            print(
                f">>> {self.logo} [{color}]Successfully finished[/{color}]! Time consumption: {value} s.")
            return 0

    def _RecursiveAnalyze(self, step: float, algoIndex: int,
                          testIterTimes: int, testTol: float,
                          vcontrol: dict, vcurrent: dict):
        """RecursiveAnalyze.

        Parameters
        ----------
        step : float
            step size, dynamic analysis is dt;
            static analysis is the displacement of small loading section, <=maxStep
        algoIndex : int
            The serial number of the initial iteration method list,
            generally starting from the first one, which is 0
        testIterTimes : int
            The number of iterations, the default is 7
        testTol : float
            iteration tolerance
        vcontrol : dict
            real-time control parameter dictionary
        vcurrent : dict
            real-time status parameter dictionary

        Returns
        -------
        int
            Analysis flag, if < 0, analysis failed; elsewise = 0 success.
        """

        if vcontrol['debugMode']:
            color = _get_random_color()
            values = f"[bold {color}]step=%.3e, algoI=%i, times=%i, tol=%.3e[/bold {color}]" % (
                step, algoIndex, testIterTimes, testTol)
            print(f"*** {self.logo} Run Recursive: {values}\n")

        if algoIndex != vcurrent['algoIndex']:
            color = _get_random_color()
            values = f"[bold {color}]%i[/bold {color}]" % (
                vcontrol['algoTypes'][algoIndex])
            print(f">>> {self.logo} Setting algorithm to {values}\n")
            self._setAlgorithm(vcontrol['algoTypes'][algoIndex])
            vcurrent['algoIndex'] = algoIndex

        if testIterTimes != vcurrent['testIterTimes'] or testTol != vcurrent['testTol']:
            if testIterTimes != vcurrent['testIterTimes']:
                color = _get_random_color()
                values = f"[bold {color}]%i[/bold {color}]" % testIterTimes
                print(
                    f">>> {self.logo} Setting test iteration times to {values}\n")
                vcurrent['testIterTimes'] = testIterTimes
            if testTol != vcurrent['testTol']:
                color = _get_random_color()
                print(
                    f">>> {self.logo} Setting test tolerance to [bold {color}]%f[/bold {color}]\n" % testTol)
                vcurrent['testTol'] = testTol

            ops.test(vcontrol['testType'], testTol,
                     testIterTimes, vcontrol['testPrintFlag'])
        # static step size
        if vcontrol['analysis'] == 'Static' and vcurrent['step'] != step:
            color = _get_random_color()
            print(
                f">>> {self.logo} Setting step to [bold {color}]%.3e[/bold {color}]\n" % step)
            ops.integrator('DisplacementControl',
                           vcurrent['node'], vcurrent['dof'], step)
            vcurrent['step'] = step
        # trial analyze once
        if vcontrol['analysis'] == 'Static':
            ok = ops.analyze(1)
        else:
            ok = ops.analyze(1, step)
        vcurrent['counter'] += 1
        if ok == 0:
            if vcurrent['counter'] >= vcontrol['printPer']:
                if vcurrent['segs'] is not None:
                    color = _get_random_color()
                    value1 = f"[bold {color}]{100 * vcurrent['progress'] / vcurrent['segs']:.2f}[/bold {color}]"
                    value2 = f"[bold {color}]{self._get_time():.3f}[/bold {color}]"
                    print(
                        f"* {self.logo} progress {value1} %. Time consumption: {value2} s.")
                vcurrent['counter'] = 0
            return 0
        # If not convergence, add test iteration times. Use current step, algorithm and test tolerance.
        if vcontrol['tryAddTestTimes'] and testIterTimes != vcontrol['testIterTimesMore']:
            norm = ops.testNorm()
            color = _get_random_color()
            if norm[-1] < vcontrol['normTol']:
                print(f">>> {self.logo} Adding test times to [bold {color}]%i[/bold {color}].\n" % (
                    vcontrol['testIterTimesMore']))
                return self._RecursiveAnalyze(step, algoIndex, vcontrol['testIterTimesMore'],
                                              testTol, vcontrol, vcurrent)
            else:
                print(f">>> {self.logo} Not adding test times for norm [bold {color}]%.3e[/bold {color}].\n" % (
                    norm[-1]))

        # Change algorithm. Set back test iteration times.
        if vcontrol['tryAlterAlgoTypes'] and (algoIndex + 1) < len(vcontrol['algoTypes']):
            algoIndex += 1
            color = _get_random_color()
            print(f">>> {self.logo} Setting algorithm to [bold {color}]%i[/bold {color}].\n" % (
                vcontrol['algoTypes'][algoIndex]))
            return self._RecursiveAnalyze(step, algoIndex, testIterTimes, testTol, vcontrol, vcurrent)

        # If step length is too small, try add test tolerance. set algorithm and test iteration times back.
        if np.abs(step) < 2 * vcontrol['minStep']:
            color = _get_random_color()
            print(
                f">>> {self.logo} current step [bold {color}]%.3e[/bold {color}] beyond the min step!\n" % step)
            if vcontrol['tryLooseTestTol'] and vcurrent['testTol'] != vcontrol['looseTestTolTo']:
                print(
                    f"!!! {self.logo} Warning: [bold {color}]Loosing test tolerance[/bold {color}]\n")
                return self._RecursiveAnalyze(step, 0, vcontrol['testIterTimes'],
                                              vcontrol['looseTestTolTo'], vcontrol, vcurrent)
            # Here, all methods have been tried. Return negative value.
            return -1

        # Split the current step into two steps.
        stepNew = step * vcontrol['relaxation']
        if 0 < stepNew < vcontrol['minStep']:
            stepNew = vcontrol['minStep']
        if 0 > stepNew > -vcontrol['minStep']:
            stepNew = -vcontrol['minStep']

        stepRest = step - stepNew
        color = _get_random_color()
        print(f">>> {self.logo} Dividing the current step [bold {color}]%.3e into %.3e and %.3e[/bold {color}]\n" % (
            step, stepNew, stepRest))
        ok = self._RecursiveAnalyze(
            stepNew, 0, testIterTimes, testTol, vcontrol, vcurrent)
        if ok < 0:
            return -1
        ok = self._RecursiveAnalyze(
            stepRest, 0, testIterTimes, testTol, vcontrol, vcurrent)
        if ok < 0:
            return -1
        return 0

    def _setAlgorithm(self, algotype):
        color = _get_random_color()

        def case0():
            print(
                f"> {self.logo} Setting algorithm to  [bold {color}]Linear ...[/bold {color}]")
            ops.algorithm('Linear')

        def case1():
            print(
                f"> {self.logo} Setting algorithm to  [bold {color}]Linear -initial ...[/bold {color}]")
            ops.algorithm('Linear', True, False)

        def case2():
            print(
                f"> {self.logo} Setting algorithm to  [bold {color}]Linear -factorOnce ...[/bold {color}]")
            ops.algorithm('Linear', False, True)

        def case10():
            print(
                f"> {self.logo} Setting algorithm to  [bold {color}]Newton ...[/bold {color}]")
            ops.algorithm('Newton')

        def case11():
            print(
                f"> {self.logo} Setting algorithm to  [bold {color}]Newton -initial ...[/bold {color}]")
            ops.algorithm('Newton', False, True, False)

        def case12():
            print(
                f"> {self.logo} Setting algorithm to  [bold {color}]Newton -initialThenCurrent ...[/bold {color}]")
            ops.algorithm('Newton', False, False, True)

        def case20():
            print(
                f"> {self.logo} Setting algorithm to  [bold {color}]NewtonLineSearch ...[/bold {color}]")
            ops.algorithm('NewtonLineSearch')

        def case21():
            print(f"> {self.logo} Setting algorithm to "
                  f"[bold {color}]NewtonLineSearch -type Bisection ...[/bold {color}]")
            ops.algorithm('NewtonLineSearch', True)

        def case22():
            print(f"> {self.logo} Setting algorithm to "
                  f"[bold {color}]NewtonLineSearch -type Secant ...[/bold {color}]")
            ops.algorithm('NewtonLineSearch', False, True)

        def case23():
            print(f"> {self.logo} Setting algorithm to "
                  f"[bold {color}]NewtonLineSearch -type RegulaFalsi ...[/bold {color}]")
            ops.algorithm('NewtonLineSearch', False, False, True)

        def case30():
            print(
                f"> {self.logo} Setting algorithm to  [bold {color}]Modified Newton ...[/bold {color}]")
            ops.algorithm('ModifiedNewton')

        def case31():
            print(
                f"> {self.logo} Setting algorithm to  [bold {color}]ModifiedNewton -initial ...[/bold {color}]")
            ops.algorithm('ModifiedNewton', False, True)

        def case40():
            print(
                f"> {self.logo} Setting algorithm to  [bold {color}]KrylovNewton ...[/bold {color}]")
            ops.algorithm('KrylovNewton')

        def case41():
            print(f"> {self.logo} Setting algorithm to "
                  f"[bold {color}]KrylovNewton -iterate initial ...[/bold {color}]")
            ops.algorithm('KrylovNewton', 'initial')

        def case42():
            print(f"> {self.logo} Setting algorithm to "
                  f"[bold {color}]KrylovNewton -increment initial ...[/bold {color}]")
            ops.algorithm('KrylovNewton', 'current', 'initial')

        def case43():
            print(f"> {self.logo} Setting algorithm to "
                  f"[bold {color}]KrylovNewton -iterate initial -increment initial ...[/bold {color}]")
            ops.algorithm('KrylovNewton', 'initial', 'initial')

        def case44():
            print(
                f"> {self.logo} Setting algorithm to  [bold {color}]KrylovNewton -maxDim 50[/bold {color}]")
            ops.algorithm('KrylovNewton', 'current', 'current', 50)

        def case45():
            print(f"> {self.logo} Setting algorithm to "
                  f"[bold {color}]KrylovNewton -iterate initial -increment initial -maxDim 50[/bold {color}]")
            ops.algorithm('KrylovNewton', 'initial', 'initial', 50)

        def case50():
            print(
                f"> {self.logo} Setting algorithm to  [bold {color}]SecantNewton ...[/bold {color}]")
            ops.algorithm('SecantNewton')

        def case51():
            print(f"> {self.logo} Setting algorithm to "
                  f"[bold {color}]SecantNewton -iterate initial ...[/bold {color}]")
            ops.algorithm('SecantNewton', 'initial')

        def case52():
            print(f"> {self.logo} Setting algorithm to "
                  f"[bold {color}]SecantNewton -increment initial  ...[/bold {color}]")
            ops.algorithm('SecantNewton', 'current', 'initial')

        def case53():
            print(f"> {self.logo} Setting algorithm to "
                  f"[bold {color}]SecantNewton -iterate initial -increment initial ...[/bold {color}]")
            ops.algorithm('SecantNewton', 'initial', 'initial')

        def case60():
            print(
                f"> {self.logo} Setting algorithm to  [bold {color}]BFGS ...[/bold {color}]")
            ops.algorithm('BFGS')

        def case70():
            print(
                f"> {self.logo} Setting algorithm to  [bold {color}]Broyden ...[/bold {color}]")
            ops.algorithm('Broyden')

        def case80():
            print(
                f"> {self.logo} Setting algorithm to  [bold {color}]PeriodicNewton ...[/bold {color}]")
            ops.algorithm('PeriodicNewton')

        def case90():
            # User algorithm0
            pass

        def default():
            raise ValueError("!!! SmartAnalyze: ERROR! WRONG Algorithm Type!")

        switch = {0: case0, 1: case1, 2: case2, 10: case10, 11: case11, 12: case12,
                  20: case20, 21: case21, 22: case22, 23: case23,
                  30: case30, 31: case31,
                  40: case40, 41: case41, 42: case42, 43: case43, 44: case44, 45: case45,
                  50: case50, 51: case51, 52: case52, 53: case53,
                  60: case60, 70: case70, 80: case80, 90: case90}

        switch.get(algotype, default)()
