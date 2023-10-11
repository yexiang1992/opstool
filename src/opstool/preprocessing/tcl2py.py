import tkinter

from rich import print


def tcl2py(input_file: str,
           output_file: str,
           prefix: str = "ops",
           encoding: str = "utf-8"):
    """Convert OpenSees Tcl code to OpenSeesPy format.

    .. tip::

        * This function supports Tcl syntax and will flatten your Tcl code, including loops,
          judgments, assignments, proc, etc,.
        * Do not use assignment statements for OpenSees commands, such as
          ``set ok [analyze 1]``, ``set lambdaN [eigen 10]``, it will trigger
          an error! This is because this function does not run the OpenSees command at all.
        * It is recommended to remove `analysis related tcl code` and keep only
          commands such as model building and load definition to avoid
          possible exceptions.
          The `analysis-related python code` you can add manually, although
          this function provides the ability to convert the analysis Tcl code.

    Parameters
    ----------
    input_file : str
        The name of input ``.tcl`` file.
    output_file : str
        The name of output ``.py`` file.
    prefix : str, optional
        Prefix name of openseespy, by default ``ops``.
        i.e., ``import openseespy.opensees as ops``.
        If None or void str '', the prefix is not used.
        i.e., ``from openseespy.opensees import *``.
    encoding: str, optional
        file encoding format, by default "utf-8".
    """
    if not input_file.endswith(".tcl"):
        input_file += ".tcl"
    if not output_file.endswith(".py"):
        output_file += ".py"
    if prefix:
        import_txt = f"import openseespy.opensees as {prefix}\n\n"
        prefix += "."
    else:
        import_txt = "from openseespy.opensees import *\n\n"
        prefix = ''
    with open(input_file, 'r', encoding=encoding) as f:
        tcl_src = f.read()
    tcl_src = tcl_src.replace("#", "commits___ ")
    tcl_src = tcl_src.replace("{", " { ")
    tcl_src = tcl_src.replace("}", " } ")
    interp, contents = _TclInterp(prefix)

    try:
        interp.eval(tcl_src)
    finally:
        with open(output_file, mode='w', encoding=encoding) as fw:
            fw.write("# This file is created by opstool.tcl2py(), author:: Yexiang Yan\n\n")
            fw.write(import_txt)
            for line in contents:
                fw.write(line + "\n")
    print(f"[bold #34bf49]OpenSeesPy[/bold #34bf49] file "
          f"[bold #d20962]{output_file}[/bold #d20962] has been created successfully!")


def _TclInterp(prefix):
    interp = tkinter.Tcl()
    contents = []

    def _commits(*args):
        args = [src.replace("commits___", "#") for src in args]
        if args:
            args = " ".join(args).replace("# ", "#")
            contents.append(f"# {args}")
        else:
            contents.append("#")

    def _puts(*args):
        if len(args) == 1:
            contents.append(f"print('{args[0]}')")
        else:
            contents.append(f"print{args}")

    def _wipe(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}wipe{args}")

    def _model(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}model{args}")

    def _node(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}node{args}")

    def _fix(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}fix{args}")

    def _fixX(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}fixX{args}")

    def _fixY(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}fixY{args}")

    def _fixZ(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}fixZ{args}")

    def _equalDOF(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}equalDOF{args}")

    def _equalDOF_Mixed(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}equalDOF_Mixed{args}")

    def _rigidDiaphragm(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}rigidDiaphragm{args}")

    def _rigidLink(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}rigidLink{args}")

    def _uniaxialMaterial(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}uniaxialMaterial{args}")

    def _nDMaterial(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}nDMaterial{args}")

    def _beamIntegration(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}beamIntegration{args}")

    def _section(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        if args[0].lower() in ('ndfiber', 'fiber'):
            if args[0].lower() == "fiber" and ('-GJ' not in args or '-torsion' not in args):
                print("[bold #d20962]Warning[/bold #d20962]: "
                      "-GJ or -torsion not used for fiber section, GJ=10000 is assumed!")
                new_args = (args[0], args[1], '-GJ', 1.E4)
            else:
                new_args = args[:-1]
            contents.append(f"{prefix}section{new_args}")
            txt = args[-1]
            txt.replace("\\n", '')
            interp.eval(txt)
        else:
            contents.append(f"{prefix}section{args}")

    def _fiber(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}fiber{args}")

    def _patch(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}patch{args}")

    def _layer(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}layer{args}")

    def _element(*args):
        args = _remove_commit(args)
        args = [_type_convert(i) for i in args]
        if args[0] not in ['nonlinearBeamColumn',
                           'forceBeamColumn', 'dispBeamColumn']:
            args = tuple([_type_convert(i) for i in args])
            contents.append(f"{prefix}element{args}")
        else:
            eleTag = args[1]
            secTag = args[5]
            if isinstance(secTag, int):
                Np = args[4]
                transfTag = args[6]
                if args[0] == 'dispBeamColumn':
                    contents.append(
                        f"{prefix}beamIntegration"
                        f"('Legendre', {eleTag}, {secTag}, {Np})")
                else:
                    contents.append(
                        f"{prefix}beamIntegration"
                        f"('Lobatto', {eleTag}, {secTag}, {Np})")
                idx = 7
            else:
                transfTag = args[4]
                interp_paras = []
                idx = 6
                for i, arg in enumerate(args[6:]):
                    if not isinstance(arg, str):
                        interp_paras.append(arg)
                    else:
                        idx += i
                        break
                contents.append(
                    f"{prefix}beamIntegration"
                    f"('{args[5]}', {eleTag}, *{interp_paras})")
            if args[0] == 'nonlinearBeamColumn':
                args[0] = 'forceBeamColumn'
            if '-mass' not in args and '-iter' not in args:
                contents.append(
                    f"{prefix}element('{args[0]}', {eleTag}, {args[2]}, "
                    f"{args[3]}, {transfTag}, {eleTag})")
            else:
                contents.append(
                    f"{prefix}element('{args[0]}', {eleTag}, {args[2]}, "
                    f"{args[3]}, {transfTag}, {eleTag}, *{args[idx:]})")

    def _timeSeries(*args):
        args = _remove_commit(args)
        args = [_type_convert(i) for i in args]
        if args[0] in ['Path', 'Series']:
            if ('-time' in args) or ('-values' in args):
                time, values = None, None
                if '-time' in args:
                    idx = args.index('-time')
                    time = list(args[idx + 1].split())
                    time = [float(i) for i in time]
                    args.pop(idx)
                    args.pop(idx)
                if '-values' in args:
                    idx = args.index('-values')
                    values = list(args[idx + 1].split())
                    values = [float(i) for i in values]
                    args.pop(idx)
                    args.pop(idx)
                if time and values:
                    args = args[:2] + ['-time', *time,
                                       '-values', *values] + args[2:]
                elif values is None:
                    args = args[:2] + ['-time', *time] + args[2:]
                else:
                    args = args[:2] + ['-values', *values] + args[2:]
                txt = f"{prefix}timeSeries('Path', {args[1]}, *{args[2:]})"
                contents.append(txt)
            else:
                contents.append(f"{prefix}timeSeries{tuple(args)}")
        else:
            contents.append(f"{prefix}timeSeries{tuple(args)}")

    def _pattern(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        if args[0].lower() != "uniformexcitation":
            if args[0].lower() == "plain" and isinstance(args[2], str):
                print(
                    f"[bold #d20962]Warning[/bold #d20962]: OpenSeesPy not support a str "
                    f"[bold #0099e5]{args[2]}[/bold #0099e5] "
                    f"followed [bold #ff4c4c]plain[/bold #ff4c4c], "
                    f"and a new [bold #f47721]timeSeries[/bold #f47721] is created with tag "
                    f"[bold #34bf49]{args[1]}[/bold #34bf49], "
                    f"please check this [bold #34bf49]pattern tag={args[1]}[/bold #34bf49]!")
                tsargs = list(args[2].split())
                if len(tsargs) == 1:
                    contents.append(f"{prefix}timeSeries('{tsargs[0]}', {args[1]})")
                else:
                    contents.append(f"{prefix}timeSeries('{tsargs[0]}', {args[1]}, *{tsargs[1:]})")
                args = list(args)
                args[2] = args[1]
                args = tuple(args)
                contents.append(f"{prefix}pattern{args[:-1]}")
            else:
                contents.append(f"{prefix}pattern{args[:-1]}")
            txt = args[-1]
            txt.replace("\\n", '')
            interp.eval(txt)
        else:
            contents.append(f"{prefix}pattern{args}")

    def _load(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}load{args}")

    def _eleLoad(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}eleLoad{args}")

    def _sp(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}sp{args}")

    def _groundMotion(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}groundMotion{args}")

    def _imposedMotion(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}imposedMotion{args}")

    def _mass(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}mass{args}")

    def _frictionModel(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}frictionModel{args}")

    def _geomTransf(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}geomTransf{args}")

    def _region(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}region{args}")

    def _rayleigh(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}rayleigh{args}")

    def _block2D(*args):
        args = _remove_commit(args)
        args = [_type_convert(i) for i in args]
        txt = args[-1]
        txt = txt.replace("\n", "").replace("\t", " ")
        crds = txt.split()
        crds = [_type_convert(i) for i in crds]
        contents.append(f"crds = {crds}")
        if isinstance(args[-2], str):
            eleargs = args[-2].split()
            eleargs = [_type_convert(i) for i in eleargs]
            args = args[:-2] + eleargs
            args = [f"'{i}'" if isinstance(i, str) else str(i)
                    for i in args]
            args.append("*crds")
        else:
            args = [f"'{i}'" if isinstance(i, str) else str(i)
                    for i in args[:-1]]
            args.append("*crds")
        txt = f"{prefix}block2D(" + ", ".join(args) + ")"
        contents.append(txt)

    def _block3D(*args):
        args = _remove_commit(args)
        args = [_type_convert(i) for i in args]
        txt = args[-1]
        txt = txt.replace("\n", "").replace("\t", " ")
        crds = txt.split()
        crds = [_type_convert(i) for i in crds]
        contents.append(f"crds = {crds}")
        if isinstance(args[-2], str):
            eleargs = args[-2].split()
            eleargs = [_type_convert(i) for i in eleargs]
            args = args[:-2] + eleargs
            args = [f"'{i}'" if isinstance(i, str) else str(i)
                    for i in args]
            args.append("*crds")
        else:
            args = [f"'{i}'" if isinstance(i, str) else str(i)
                    for i in args[:-1]]
            args.append("*crds")
        txt = f"{prefix}block3D(" + ", ".join(args) + ")"
        contents.append(txt)

    def _ShallowFoundationGen(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}ShallowFoundationGen{args}")

    def _constraints(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}constraints{args}")

    def _numberer(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}numberer{args}")

    def _system(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}system{args}")

    def _test(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}test{args}")

    def _algorithm(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}algorithm{args}")

    def _integrator(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}integrator{args}")

    def _analysis(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}analysis{args}")

    def _eigen(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}eigen{args}")
        return 0

    def _analyze(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}analyze{args}")
        return 0

    def _modalProperties(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}modalProperties{args}")

    def _responseSpectrumAnalysis(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}responseSpectrumAnalysis{args}")

    def _recorder(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}recorder{args}")

    def _record(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}record{args}")

    def _print(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}printModel{args}")

    def _printA(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}printA{args}")

    def _logFile(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}logFile{args}")

    def _remove(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}remove{args}")

    def _loadConst(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}loadConst{args}")

    def _wipeAnalysis(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}wipeAnalysis{args}")

    def _modalDamping(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}modalDamping{args}")

    def _database(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}database{args}")

    def _getTime(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}getTime{args}")

    def _setTime(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}setTime{args}")

    def _testUniaxialMaterial(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}testUniaxialMaterial{args}")

    def _setStrain(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}setStrain{args}")

    def _getStrain(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}getStrain{args}")

    def _getStress(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}getStress{args}")

    def _getTangent(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}getTangent{args}")

    def _getDampTangent(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}getDampTangent{args}")

    def _reactions(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}reactions{args}")

    def _nodeReaction(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}nodeReaction{args}")

    def _nodeEigenvector(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}nodeEigenvector{args}")

    def _setCreep(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}setCreep{args}")

    def _eleResponse(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}eleResponse{args}")

    def _reset(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}reset{args}")

    def _initialize(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}initialize{args}")

    def _getLoadFactor(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}getLoadFactor{args}")

    def _build(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}build{args}")

    def _printGID(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}printGID{args}")

    def _getCTestNorms(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}getCTestNorms{args}")

    def _getCTestIter(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}getCTestIter{args}")

    def _save(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}save{args}")

    def _restore(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}restore{args}")

    def _eleForce(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}eleForce{args}")

    def _eleDynamicalForce(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}eleDynamicalForce{args}")

    def _nodeUnbalance(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}nodeUnbalance{args}")

    def _nodeDisp(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}nodeDisp{args}")

    def _setNodeDisp(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}setNodeDisp{args}")

    def _nodeVel(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}nodeVel{args}")

    def _setNodeVel(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}setNodeVel{args}")

    def _nodeAccel(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}nodeAccel{args}")

    def _setNodeAccel(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}setNodeAccel{args}")

    def _nodeResponse(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}nodeResponse{args}")

    def _nodeCoord(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}nodeCoord{args}")

    def _setNodeCoord(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}setNodeCoord{args}")

    def _updateElementDomain(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}updateElementDomain{args}")

    def _getNDMM(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}getNDM{args}")

    def _getNDFF(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}getNDF{args}")

    def _eleNodes(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}eleNodes{args}")

    def _eleType(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}eleType{args}")

    def _nodeDOFs(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}nodeDOFs{args}")

    def _nodeMass(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}nodeMass{args}")

    def _nodePressure(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}nodePressure{args}")

    def _setNodePressure(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}setNodePressure{args}")

    def _nodeBounds(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}nodeBounds{args}")

    def _startTimer(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}start{args}")

    def _stopTimer(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}stop{args}")

    def _modalDampingQ(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}modalDampingQ{args}")

    def _setElementRayleighDampingFactors(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}setElementRayleighDampingFactors{args}")

    def _setPrecision(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}setPrecision{args}")

    def _searchPeerNGA(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}searchPeerNGA{args}")

    def _domainChange(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}domainChange{args}")

    def _defaultUnits(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}defaultUnits{args}")

    def _stripXML(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}stripXML{args}")

    def _convertBinaryToText(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}convertBinaryToText{args}")

    def _convertTextToBinary(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}convertTextToBinary{args}")

    def _getEleTags(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}getEleTags{args}")

    def _getCrdTransfTags(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}getCrdTransfTags{args}")

    def _getNodeTags(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}getNodeTags{args}")

    def _getParamTags(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}getParamTags{args}")

    def _getParamValue(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}getParamValue{args}")

    def _sectionForce(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}sectionForce{args}")

    def _sectionDeformation(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}sectionDeformation{args}")

    def _sectionStiffness(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}sectionStiffness{args}")

    def _sectionFlexibility(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}sectionFlexibility{args}")

    def _sectionLocation(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}sectionLocation{args}")

    def _sectionWeight(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}sectionWeight{args}")

    def _sectionTag(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}sectionTag{args}")

    def _sectionDisplacement(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}sectionDisplacement{args}")

    def _cbdiDisplacement(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}cbdiDisplacement{args}")

    def _basicDeformation(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}basicDeformation{args}")

    def _basicForce(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}basicForce{args}")

    def _basicStiffness(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}basicStiffness{args}")

    def _InitialStateAnalysis(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}InitialStateAnalysis{args}")

    def _totalCPU(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}totalCPU{args}")

    def _solveCPU(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}solveCPU{args}")

    def _accelCPU(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}accelCPU{args}")

    def _numFact(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}numFact{args}")

    def _numIter(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}numIter{args}")

    def _systemSize(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}systemSize{args}")

    def _version(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}version{args}")

    def _setMaxOpenFiles(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}setMaxOpenFiles{args}")

    def _limitCurve(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}limitCurve{args}")

    def _setElementRayleighFactors(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}setElementRayleighFactors{args}")

    def _mesh(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}mesh{args}")

    def _remesh(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}remesh{args}")

    def _parameter(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}parameter{args}")

    def _addToParameter(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}addToParameter{args}")

    def _updateParameter(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}updateParameter{args}")

    def _setParameter(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}setParameter{args}")

    def _getPID(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}getPID{args}")

    def _getNP(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}getNP{args}")

    def _barrier(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}barrier{args}")

    def _send(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}send{args}")

    def _recv(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}recv{args}")

    def _Bcast(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}Bcast{args}")

    def _computeGradients(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}computeGradients{args}")

    def _sensitivityAlgorithm(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}sensitivityAlgorithm{args}")

    def _sensNodeDisp(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}sensNodeDisp{args}")

    def _sensNodeVel(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}sensNodeVel{args}")

    def _sensNodeAccel(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}sensNodeAccel{args}")

    def _sensLambda(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}sensLambda{args}")

    def _sensSectionForce(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}sensSectionForce{args}")

    def _sensNodePressure(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}sensNodePressure{args}")

    def _getNumElements(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}getNumElements{args}")

    def _getEleClassTags(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}getEleClassTags{args}")

    def _getEleLoadClassTags(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}getEleLoadClassTags{args}")

    def _getEleLoadTags(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}getEleLoadTags{args}")

    def _getEleLoadData(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}getEleLoadData{args}")

    def _getNodeLoadTags(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}getNodeLoadTags{args}")

    def _getNodeLoadData(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}getNodeLoadData{args}")

    def _randomVariable(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}randomVariable{args}")

    def _getRVTags(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}getRVTags{args}")

    def _getRVMean(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}getRVMean{args}")

    def _getRVStdv(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}getRVStdv{args}")

    def _getRVPDF(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}getRVPDF{args}")

    def _getRVCDF(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}getRVCDF{args}")

    def _getRVInverseCDF(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}getRVInverseCDF{args}")

    def _addCorrelate(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}addCorrelate{args}")

    def _correlate(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}correlate{args}")

    def _performanceFunction(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}performanceFunction{args}")

    def _gradPerformanceFunction(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}gradPerformanceFunction{args}")

    def _transformUtoX(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}transformUtoX{args}")

    def _wipeReliability(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}wipeReliability{args}")

    def _updateMaterialStage(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}updateMaterialStage{args}")

    def _sdfResponse(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}sdfResponse{args}")

    def _probabilityTransformation(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}probabilityTransformation{args}")

    def _startPoint(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}startPoint{args}")

    def _randomNumberGenerator(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}randomNumberGenerator{args}")

    def _reliabilityConvergenceCheck(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}reliabilityConvergenceCheck{args}")

    def _searchDirection(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}searchDirection{args}")

    def _meritFunctionCheck(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}meritFunctionCheck{args}")

    def _stepSizeRule(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}stepSizeRule{args}")

    def _rootFinding(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}rootFinding{args}")

    def _functionEvaluator(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}functionEvaluator{args}")

    def _gradientEvaluator(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}gradientEvaluator{args}")

    def _runFOSMAnalysis(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}runFOSMAnalysis{args}")

    def _findDesignPoint(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}findDesignPoint{args}")

    def _runFORMAnalysis(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}runFORMAnalysis{args}")

    def _getLSFTags(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}getLSFTags{args}")

    def _runImportanceSamplingAnalysis(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}runImportanceSamplingAnalysis{args}")

    def _IGA(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}IGA{args}")

    def _NDTest(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}NDTest{args}")

    def _getNumThreads(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}getNumThreads{args}")

    def _setNumThreads(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}setNumThreads{args}")

    def _setStartNodeTag(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}setStartNodeTag{args}")

    def _hystereticBackbone(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}hystereticBackbone{args}")

    def _stiffnessDegradation(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}stiffnessDegradation{args}")

    def _strengthDegradation(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}strengthDegradation{args}")

    def _unloadingRule(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}unloadingRule{args}")

    def _partition(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}partition{args}")

    def _pc(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}pressureConstraint{args}")

    def _domainCommitTag(*args):
        args = _remove_commit(args)
        args = tuple([_type_convert(i) for i in args])
        contents.append(f"{prefix}domainCommitTag{args}")

    interp.createcommand('commits___', _commits)
    interp.createcommand('puts', _puts)
    interp.createcommand('wipe', _wipe)
    interp.createcommand('model', _model)
    interp.createcommand('node', _node)
    interp.createcommand('fix', _fix)
    interp.createcommand('fixX', _fixX)
    interp.createcommand('fixY', _fixY)
    interp.createcommand('fixZ', _fixZ)
    interp.createcommand('equalDOF', _equalDOF)
    interp.createcommand('equalDOF_Mixed', _equalDOF_Mixed)
    interp.createcommand('rigidDiaphragm', _rigidDiaphragm)
    interp.createcommand('rigidLink', _rigidLink)
    interp.createcommand('element', _element)
    interp.createcommand('timeSeries', _timeSeries)
    # interp.createcommand('Series', _timeSeries)
    interp.createcommand('pattern', _pattern)
    interp.createcommand('load', _load)
    interp.createcommand('eleLoad', _eleLoad)
    interp.createcommand('sp', _sp)
    interp.createcommand('groundMotion', _groundMotion)
    interp.createcommand('imposedMotion', _imposedMotion)
    interp.createcommand("imposedSupportMotion", _imposedMotion)
    interp.createcommand('mass', _mass)
    interp.createcommand('uniaxialMaterial', _uniaxialMaterial)
    interp.createcommand('nDMaterial', _nDMaterial)
    interp.createcommand("beamIntegration", _beamIntegration)
    interp.createcommand('section', _section)
    interp.createcommand('fiber', _fiber)
    interp.createcommand('patch', _patch)
    interp.createcommand('layer', _layer)
    interp.createcommand('frictionModel', _frictionModel)
    interp.createcommand('geomTransf', _geomTransf)
    interp.createcommand('region', _region)
    interp.createcommand('rayleigh', _rayleigh)
    interp.createcommand('block2D', _block2D)
    interp.createcommand('block2d', _block2D)
    interp.createcommand('block3D', _block3D)
    interp.createcommand('block3d', _block3D)
    interp.createcommand('ShallowFoundationGen', _ShallowFoundationGen)
    interp.createcommand('constraints', _constraints)
    interp.createcommand('numberer', _numberer)
    interp.createcommand('system', _system)
    interp.createcommand('test', _test)
    interp.createcommand('algorithm', _algorithm)
    interp.createcommand('integrator', _integrator)
    interp.createcommand('analysis', _analysis)
    interp.createcommand('eigen', _eigen)
    interp.createcommand('analyze', _analyze)
    interp.createcommand('modalProperties', _modalProperties)
    interp.createcommand('responseSpectrumAnalysis', _responseSpectrumAnalysis)
    interp.createcommand('record', _record)
    interp.createcommand('recorder', _recorder)
    interp.createcommand('print', _print)
    interp.createcommand('printA', _printA)
    interp.createcommand('logFile', _logFile)
    interp.createcommand('remove', _remove)
    interp.createcommand('loadConst', _loadConst)
    interp.createcommand('wipeAnalysis', _wipeAnalysis)
    interp.createcommand('modalDamping', _modalDamping)
    interp.createcommand('database', _database)
    interp.createcommand('getTime', _getTime)
    interp.createcommand("setTime", _setTime)
    interp.createcommand("testUniaxialMaterial", _testUniaxialMaterial)
    interp.createcommand("setStrain", _setStrain)
    interp.createcommand("getStrain", _getStrain)
    interp.createcommand("getStress", _getStress)
    interp.createcommand("getTangent", _getTangent)
    interp.createcommand("getDampTangent", _getDampTangent)
    interp.createcommand("reactions", _reactions)
    interp.createcommand("nodeReaction", _nodeReaction)
    interp.createcommand("remove", _remove)
    interp.createcommand("nodeEigenvector", _nodeEigenvector)
    interp.createcommand("setCreep", _setCreep)
    interp.createcommand("eleResponse", _eleResponse)
    interp.createcommand("reset", _reset)
    interp.createcommand("initialize", _initialize)
    interp.createcommand("getLoadFactor", _getLoadFactor)
    interp.createcommand("build", _build)
    interp.createcommand("printGID", _printGID)
    interp.createcommand("testNorm", _getCTestNorms)
    interp.createcommand("testIter", _getCTestIter)
    interp.createcommand("save", _save)
    interp.createcommand("restore", _restore)
    interp.createcommand("eleForce", _eleForce)
    interp.createcommand("eleDynamicalForce", _eleDynamicalForce)
    interp.createcommand("nodeUnbalance", _nodeUnbalance)
    interp.createcommand("nodeDisp", _nodeDisp)
    interp.createcommand("setNodeDisp", _setNodeDisp)
    interp.createcommand("nodeVel", _nodeVel)
    interp.createcommand("setNodeVel", _setNodeVel)
    interp.createcommand("nodeAccel", _nodeAccel)
    interp.createcommand("setNodeAccel", _setNodeAccel)
    interp.createcommand("nodeResponse", _nodeResponse)
    interp.createcommand("nodeCoord", _nodeCoord)
    interp.createcommand("setNodeCoord", _setNodeCoord)
    interp.createcommand("updateElementDomain", _updateElementDomain)
    interp.createcommand("getNDM", _getNDMM)
    interp.createcommand("getNDF", _getNDFF)
    interp.createcommand("eleNodes", _eleNodes)
    interp.createcommand("eleType", _eleType)
    interp.createcommand("nodeDOFs", _nodeDOFs)
    interp.createcommand("nodeMass", _nodeMass)
    interp.createcommand("nodePressure", _nodePressure)
    interp.createcommand("setNodePressure", _setNodePressure)
    interp.createcommand("nodeBounds", _nodeBounds)
    interp.createcommand("start", _startTimer)
    interp.createcommand("stop", _stopTimer)
    interp.createcommand("modalDampingQ", _modalDampingQ)
    interp.createcommand("setElementRayleighDampingFactors",
                         _setElementRayleighDampingFactors)
    interp.createcommand("setPrecision", _setPrecision)
    interp.createcommand("searchPeerNGA", _searchPeerNGA)
    interp.createcommand("domainChange", _domainChange)
    interp.createcommand("defaultUnits", _defaultUnits)
    interp.createcommand("stripXML", _stripXML)
    interp.createcommand("convertBinaryToText", _convertBinaryToText)
    interp.createcommand("convertTextToBinary", _convertTextToBinary)
    interp.createcommand("getEleTags", _getEleTags)
    interp.createcommand("getCrdTransfTags", _getCrdTransfTags)
    interp.createcommand("getNodeTags", _getNodeTags)
    interp.createcommand("getParamTags", _getParamTags)
    interp.createcommand("getParamValue", _getParamValue)
    interp.createcommand("sectionForce", _sectionForce)
    interp.createcommand("sectionDeformation", _sectionDeformation)
    interp.createcommand("sectionStiffness", _sectionStiffness)
    interp.createcommand("sectionFlexibility", _sectionFlexibility)
    interp.createcommand("sectionLocation", _sectionLocation)
    interp.createcommand("sectionWeight", _sectionWeight)
    interp.createcommand("sectionTag", _sectionTag)
    interp.createcommand("sectionDisplacement", _sectionDisplacement)
    interp.createcommand("cbdiDisplacement", _cbdiDisplacement)
    interp.createcommand("basicDeformation", _basicDeformation)
    interp.createcommand("basicForce", _basicForce)
    interp.createcommand("basicStiffness", _basicStiffness)
    interp.createcommand("InitialStateAnalysis", _InitialStateAnalysis)
    interp.createcommand("totalCPU", _totalCPU)
    interp.createcommand("solveCPU", _solveCPU)
    interp.createcommand("accelCPU", _accelCPU)
    interp.createcommand("numFact", _numFact)
    interp.createcommand("numIter", _numIter)
    interp.createcommand("systemSize", _systemSize)
    interp.createcommand("version", _version)
    interp.createcommand("setMaxOpenFiles", _setMaxOpenFiles)
    interp.createcommand("limitCurve", _limitCurve)

    interp.createcommand("equalDOF_Mixed", _equalDOF_Mixed)
    interp.createcommand("setElementRayleighFactors",
                         _setElementRayleighFactors)
    interp.createcommand("mesh", _mesh)
    interp.createcommand("remesh", _remesh)
    interp.createcommand("parameter", _parameter)
    interp.createcommand("addToParameter", _addToParameter)
    interp.createcommand("updateParameter", _updateParameter)
    interp.createcommand("setParameter", _setParameter)
    interp.createcommand("getPID", _getPID)
    interp.createcommand("getNP", _getNP)
    interp.createcommand("barrier", _barrier)
    interp.createcommand("send", _send)
    interp.createcommand("recv", _recv)
    interp.createcommand("Bcast", _Bcast)
    interp.createcommand("computeGradients", _computeGradients)
    interp.createcommand("sensitivityAlgorithm", _sensitivityAlgorithm)
    interp.createcommand("sensNodeDisp", _sensNodeDisp)
    interp.createcommand("sensNodeVel", _sensNodeVel)
    interp.createcommand("sensNodeAccel", _sensNodeAccel)
    interp.createcommand("sensLambda", _sensLambda)
    interp.createcommand("sensSectionForce", _sensSectionForce)
    interp.createcommand("sensNodePressure", _sensNodePressure)
    interp.createcommand("getNumElements", _getNumElements)
    interp.createcommand("getEleClassTags", _getEleClassTags)
    interp.createcommand("getEleLoadClassTags", _getEleLoadClassTags)
    interp.createcommand("getEleLoadTags", _getEleLoadTags)
    interp.createcommand("getEleLoadData", _getEleLoadData)
    interp.createcommand("getNodeLoadTags", _getNodeLoadTags)
    interp.createcommand("getNodeLoadData", _getNodeLoadData)
    interp.createcommand("randomVariable", _randomVariable)
    interp.createcommand("getRVTags", _getRVTags)
    interp.createcommand("getMean", _getRVMean)
    interp.createcommand("getStdv", _getRVStdv)
    interp.createcommand("getPDF", _getRVPDF)
    interp.createcommand("getCDF", _getRVCDF)
    interp.createcommand("getInverseCDF", _getRVInverseCDF)
    interp.createcommand("correlate", _correlate)
    interp.createcommand("performanceFunction", _performanceFunction)
    interp.createcommand("gradPerformanceFunction", _gradPerformanceFunction)
    interp.createcommand("transformUtoX", _transformUtoX)
    interp.createcommand("wipeReliability", _wipeReliability)
    interp.createcommand("updateMaterialStage", _updateMaterialStage)
    interp.createcommand("sdfResponse", _sdfResponse)
    interp.createcommand("probabilityTransformation",
                         _probabilityTransformation)
    interp.createcommand("startPoint", _startPoint)
    interp.createcommand("randomNumberGenerator", _randomNumberGenerator)
    interp.createcommand("reliabilityConvergenceCheck", _reliabilityConvergenceCheck)
    interp.createcommand("searchDirection", _searchDirection)
    interp.createcommand("meritFunctionCheck", _meritFunctionCheck)
    interp.createcommand("stepSizeRule", _stepSizeRule)
    interp.createcommand("rootFinding", _rootFinding)
    interp.createcommand("functionEvaluator", _functionEvaluator)
    interp.createcommand("gradientEvaluator", _gradientEvaluator)
    interp.createcommand("runFOSMAnalysis", _runFOSMAnalysis)
    interp.createcommand("findDesignPoint", _findDesignPoint)
    interp.createcommand("runFORMAnalysis", _runFORMAnalysis)
    interp.createcommand("getLSFTags", _getLSFTags)
    interp.createcommand("runImportanceSamplingAnalysis", _runImportanceSamplingAnalysis)
    interp.createcommand("IGA", _IGA)
    interp.createcommand("NDTest", _NDTest)
    interp.createcommand("getNumThreads", _getNumThreads)
    interp.createcommand("setNumThreads", _setNumThreads)
    interp.createcommand("setStartNodeTag", _setStartNodeTag)
    interp.createcommand("hystereticBackbone", _hystereticBackbone)
    interp.createcommand("stiffnessDegradation", _stiffnessDegradation)
    interp.createcommand("strengthDegradation", _strengthDegradation)
    interp.createcommand("unloadingRule", _unloadingRule)
    interp.createcommand("partition", _partition)
    interp.createcommand("pressureConstraint", _pc)
    interp.createcommand("domainCommitTag", _domainCommitTag)
    return interp, contents


def _type_convert(a):
    try:
        a = int(a)
    except ValueError:
        try:
            a = float(a)
        except ValueError:
            a = str(a)
    return a


def _remove_commit(args, obj="#"):
    if "#" in args:
        idx = args.index(obj)
        args = args[:idx]
    return args
