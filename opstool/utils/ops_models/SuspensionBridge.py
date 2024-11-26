# This document was created from CSiBridge version 24.0.0

# Units: KN, m, C

from collections import namedtuple
import openseespy.opensees as ops


def SuspensionBridge():
    # Destroy all constructed objects,
    # i.e. all components of the model, all components of the analysis and all recorders.
    ops.wipe()
    # Set the default model dimensions and number of dofs.
    ops.model('basic', '-ndm', 3, '-ndf', 6)

    # Construct a coordinate-transformation object.
    # For vertical elements.
    ops.geomTransf('Linear', 1, -1, 0, 0)
    ops.geomTransf('PDelta', 3, -1, 0, 0)
    ops.geomTransf('Corotational', 5, -1, 0, 0)
    # For other elements except vertical one.
    ops.geomTransf('Linear', 2, 0, 0, 1)
    ops.geomTransf('PDelta', 4, 0, 0, 1)
    ops.geomTransf('Corotational', 6, 0, 0, 1)
    # Specify the tag of transformation, which can be changed according to requirements
    transf_Ver = 1
    transf_Other = 2

    # Mechanical properties of material
    MatProp_df = dict()
    # UnitMass-Mass Density; E-Elastic Modulus; G-Shear Modulus; v-Poisson's ratio; rho-Thermal expansion coefficient
    MatProp = namedtuple('MatProp', ('UnitMass', 'E', 'G', 'v', 'rho'))
    MatProp_df["4000Psi"] = MatProp._make(
        (2.40276960558926, 24855578.0600518, 10356490.8583549, 0.2, 9.89999952793124e-06))
    MatProp_df["A709Gr50"] = MatProp._make(
        (7.84904737995992, 199947978.795958, 76903068.767676, 0.3, 1.16999994421006e-05))

    # Create OpenSees node.
    ops.node(1, *[-60.0, -1.5, 0.0])
    ops.node(2, *[-56.6666666666667, -1.5, 0.0])
    ops.node(3, *[-56.6666666666667, -1.5, 0.277777777777778])
    ops.node(4, *[-60.0, 1.5, 0.0])
    ops.node(5, *[-56.6666666666667, 1.5, 0.0])
    ops.node(6, *[-56.6666666666667, 1.5, 0.277777777777778])
    ops.node(7, *[-53.3333333333333, -1.5, 0.0])
    ops.node(8, *[-53.3333333333333, -1.5, 1.11111111111111])
    ops.node(9, *[-53.3333333333333, 1.5, 0.0])
    ops.node(10, *[-53.3333333333333, 1.5, 1.11111111111111])
    ops.node(11, *[-50.0, -1.5, 0.0])
    ops.node(12, *[-50.0, -1.5, 2.5])
    ops.node(13, *[-50.0, 1.5, 0.0])
    ops.node(14, *[-50.0, 1.5, 2.5])
    ops.node(15, *[-46.6666666666667, -1.5, 0.0])
    ops.node(16, *[-46.6666666666667, -1.5, 4.44444444444445])
    ops.node(17, *[-46.6666666666667, 1.5, 0.0])
    ops.node(18, *[-46.6666666666667, 1.5, 4.44444444444445])
    ops.node(19, *[-43.3333333333333, -1.5, 0.0])
    ops.node(20, *[-43.3333333333333, -1.5, 6.94444444444445])
    ops.node(21, *[-43.3333333333333, 1.5, 0.0])
    ops.node(22, *[-43.3333333333333, 1.5, 6.94444444444445])
    ops.node(23, *[-40.0, -1.5, 0.0])
    ops.node(24, *[-40.0, -1.5, 10.0])
    ops.node(25, *[-40.0, 1.5, 0.0])
    ops.node(26, *[-40.0, 1.5, 10.0])
    ops.node(27, *[-36.6666666666667, -1.5, 0.0])
    ops.node(28, *[-36.6666666666667, -1.5, 8.72222222222222])
    ops.node(29, *[-36.6666666666667, 1.5, 0.0])
    ops.node(30, *[-36.6666666666667, 1.5, 8.72222222222222])
    ops.node(31, *[-33.3333333333333, -1.5, 0.0])
    ops.node(32, *[-33.3333333333333, -1.5, 7.55555555555556])
    ops.node(33, *[-33.3333333333333, 1.5, 0.0])
    ops.node(34, *[-33.3333333333333, 1.5, 7.55555555555556])
    ops.node(35, *[-30.0, -1.5, 0.0])
    ops.node(36, *[-30.0, -1.5, 6.5])
    ops.node(37, *[-30.0, 1.5, 0.0])
    ops.node(38, *[-30.0, 1.5, 6.5])
    ops.node(39, *[-26.6666666666667, -1.5, 0.0])
    ops.node(40, *[-26.6666666666667, -1.5, 5.55555555555556])
    ops.node(41, *[-26.6666666666667, 1.5, 0.0])
    ops.node(42, *[-26.6666666666667, 1.5, 5.55555555555556])
    ops.node(43, *[-23.3333333333333, -1.5, 0.0])
    ops.node(44, *[-23.3333333333333, -1.5, 4.72222222222222])
    ops.node(45, *[-23.3333333333333, 1.5, 0.0])
    ops.node(46, *[-23.3333333333333, 1.5, 4.72222222222222])
    ops.node(47, *[-20.0, -1.5, 0.0])
    ops.node(48, *[-20.0, -1.5, 4.0])
    ops.node(49, *[-20.0, 1.5, 0.0])
    ops.node(50, *[-20.0, 1.5, 4.0])
    ops.node(51, *[-16.6666666666667, -1.5, 0.0])
    ops.node(52, *[-16.6666666666667, -1.5, 3.38888888888889])
    ops.node(53, *[-16.6666666666667, 1.5, 0.0])
    ops.node(54, *[-16.6666666666667, 1.5, 3.38888888888889])
    ops.node(55, *[-13.3333333333333, -1.5, 0.0])
    ops.node(56, *[-13.3333333333333, -1.5, 2.88888888888889])
    ops.node(57, *[-13.3333333333333, 1.5, 0.0])
    ops.node(58, *[-13.3333333333333, 1.5, 2.88888888888889])
    ops.node(59, *[-10.0, -1.5, 0.0])
    ops.node(60, *[-10.0, -1.5, 2.5])
    ops.node(61, *[-10.0, 1.5, 0.0])
    ops.node(62, *[-10.0, 1.5, 2.5])
    ops.node(63, *[-6.66666666666666, -1.5, 0.0])
    ops.node(64, *[-6.66666666666666, -1.5, 2.22222222222222])
    ops.node(65, *[-6.66666666666666, 1.5, 0.0])
    ops.node(66, *[-6.66666666666666, 1.5, 2.22222222222222])
    ops.node(67, *[-3.33333333333333, -1.5, 0.0])
    ops.node(68, *[-3.33333333333333, -1.5, 2.05555555555556])
    ops.node(69, *[-3.33333333333333, 1.5, 0.0])
    ops.node(70, *[-3.33333333333333, 1.5, 2.05555555555556])
    ops.node(71, *[0.0, -1.5, 0.0])
    ops.node(72, *[0.0, -1.5, 2.0])
    ops.node(73, *[0.0, 1.5, 0.0])
    ops.node(74, *[0.0, 1.5, 2.0])
    ops.node(75, *[3.33333333333334, -1.5, 0.0])
    ops.node(76, *[3.33333333333334, -1.5, 2.05555555555556])
    ops.node(77, *[3.33333333333334, 1.5, 0.0])
    ops.node(78, *[3.33333333333334, 1.5, 2.05555555555556])
    ops.node(79, *[6.66666666666667, -1.5, 0.0])
    ops.node(80, *[6.66666666666667, -1.5, 2.22222222222222])
    ops.node(81, *[6.66666666666667, 1.5, 0.0])
    ops.node(82, *[6.66666666666667, 1.5, 2.22222222222222])
    ops.node(83, *[10.0, -1.5, 0.0])
    ops.node(84, *[10.0, -1.5, 2.5])
    ops.node(85, *[10.0, 1.5, 0.0])
    ops.node(86, *[10.0, 1.5, 2.5])
    ops.node(87, *[13.3333333333333, -1.5, 0.0])
    ops.node(88, *[13.3333333333333, -1.5, 2.88888888888889])
    ops.node(89, *[13.3333333333333, 1.5, 0.0])
    ops.node(90, *[13.3333333333333, 1.5, 2.88888888888889])
    ops.node(91, *[16.6666666666667, -1.5, 0.0])
    ops.node(92, *[16.6666666666667, -1.5, 3.38888888888889])
    ops.node(93, *[16.6666666666667, 1.5, 0.0])
    ops.node(94, *[16.6666666666667, 1.5, 3.38888888888889])
    ops.node(95, *[20.0, -1.5, 0.0])
    ops.node(96, *[20.0, -1.5, 4.0])
    ops.node(97, *[20.0, 1.5, 0.0])
    ops.node(98, *[20.0, 1.5, 4.0])
    ops.node(99, *[23.3333333333333, -1.5, 0.0])
    ops.node(100, *[23.3333333333333, -1.5, 4.72222222222222])
    ops.node(101, *[23.3333333333333, 1.5, 0.0])
    ops.node(102, *[23.3333333333333, 1.5, 4.72222222222222])
    ops.node(103, *[26.6666666666667, -1.5, 0.0])
    ops.node(104, *[26.6666666666667, -1.5, 5.55555555555556])
    ops.node(105, *[26.6666666666667, 1.5, 0.0])
    ops.node(106, *[26.6666666666667, 1.5, 5.55555555555556])
    ops.node(107, *[30.0, -1.5, 0.0])
    ops.node(108, *[30.0, -1.5, 6.5])
    ops.node(109, *[30.0, 1.5, 0.0])
    ops.node(110, *[30.0, 1.5, 6.5])
    ops.node(111, *[33.3333333333333, -1.5, 0.0])
    ops.node(112, *[33.3333333333333, -1.5, 7.55555555555556])
    ops.node(113, *[33.3333333333333, 1.5, 0.0])
    ops.node(114, *[33.3333333333333, 1.5, 7.55555555555556])
    ops.node(115, *[36.6666666666667, -1.5, 0.0])
    ops.node(116, *[36.6666666666667, -1.5, 8.72222222222222])
    ops.node(117, *[36.6666666666667, 1.5, 0.0])
    ops.node(118, *[36.6666666666667, 1.5, 8.72222222222222])
    ops.node(119, *[40.0, -1.5, 0.0])
    ops.node(120, *[40.0, -1.5, 10.0])
    ops.node(121, *[40.0, 1.5, 0.0])
    ops.node(122, *[40.0, 1.5, 10.0])
    ops.node(123, *[43.3333333333333, -1.5, 0.0])
    ops.node(124, *[43.3333333333333, -1.5, 6.94444444444445])
    ops.node(125, *[43.3333333333333, 1.5, 0.0])
    ops.node(126, *[43.3333333333333, 1.5, 6.94444444444445])
    ops.node(127, *[46.6666666666667, -1.5, 0.0])
    ops.node(128, *[46.6666666666667, -1.5, 4.44444444444444])
    ops.node(129, *[46.6666666666667, 1.5, 0.0])
    ops.node(130, *[46.6666666666667, 1.5, 4.44444444444444])
    ops.node(131, *[50.0, -1.5, 0.0])
    ops.node(132, *[50.0, -1.5, 2.5])
    ops.node(133, *[50.0, 1.5, 0.0])
    ops.node(134, *[50.0, 1.5, 2.5])
    ops.node(135, *[53.3333333333333, -1.5, 0.0])
    ops.node(136, *[53.3333333333333, -1.5, 1.11111111111111])
    ops.node(137, *[53.3333333333333, 1.5, 0.0])
    ops.node(138, *[53.3333333333333, 1.5, 1.11111111111111])
    ops.node(139, *[56.6666666666667, -1.5, 0.0])
    ops.node(140, *[56.6666666666667, -1.5, 0.277777777777778])
    ops.node(141, *[56.6666666666667, 1.5, 0.0])
    ops.node(142, *[56.6666666666667, 1.5, 0.277777777777778])
    ops.node(143, *[60.0, -1.5, 0.0])
    ops.node(144, *[60.0, 1.5, 0.0])
    ops.node(145, *[-40.0, -1.5, -5.0])
    ops.node(146, *[-40.0, 1.5, -5.0])
    ops.node(147, *[40.0, -1.5, -5.0])
    ops.node(148, *[40.0, 1.5, -5.0])
    ops.node(149, *[-40.0, -1.5, -4.0])
    ops.node(150, *[-40.0, -1.5, -3.0])
    ops.node(151, *[-40.0, -1.5, -2.0])
    ops.node(152, *[-40.0, -1.5, -1.0])
    ops.node(153, *[-40.0, 1.5, -4.0])
    ops.node(154, *[-40.0, 1.5, -3.0])
    ops.node(155, *[-40.0, 1.5, -2.0])
    ops.node(156, *[-40.0, 1.5, -1.0])
    ops.node(157, *[40.0, -1.5, -4.0])
    ops.node(158, *[40.0, -1.5, -3.0])
    ops.node(159, *[40.0, -1.5, -2.0])
    ops.node(160, *[40.0, -1.5, -1.0])
    ops.node(161, *[40.0, 1.5, -4.0])
    ops.node(162, *[40.0, 1.5, -3.0])
    ops.node(163, *[40.0, 1.5, -2.0])
    ops.node(164, *[40.0, 1.5, -1.0])
    ops.node(165, *[-40.0, -1.5, 1.0])
    ops.node(166, *[-40.0, -1.5, 2.0])
    ops.node(167, *[-40.0, -1.5, 3.0])
    ops.node(168, *[-40.0, -1.5, 4.0])
    ops.node(169, *[-40.0, -1.5, 5.0])
    ops.node(170, *[-40.0, -1.5, 6.0])
    ops.node(171, *[-40.0, -1.5, 7.0])
    ops.node(172, *[-40.0, -1.5, 8.0])
    ops.node(173, *[-40.0, -1.5, 9.0])
    ops.node(174, *[-40.0, 1.5, 1.0])
    ops.node(175, *[-40.0, 1.5, 2.0])
    ops.node(176, *[-40.0, 1.5, 3.0])
    ops.node(177, *[-40.0, 1.5, 4.0])
    ops.node(178, *[-40.0, 1.5, 5.0])
    ops.node(179, *[-40.0, 1.5, 6.0])
    ops.node(180, *[-40.0, 1.5, 7.0])
    ops.node(181, *[-40.0, 1.5, 8.0])
    ops.node(182, *[-40.0, 1.5, 9.0])
    ops.node(183, *[40.0, -1.5, 1.0])
    ops.node(184, *[40.0, -1.5, 2.0])
    ops.node(185, *[40.0, -1.5, 3.0])
    ops.node(186, *[40.0, -1.5, 4.0])
    ops.node(187, *[40.0, -1.5, 5.0])
    ops.node(188, *[40.0, -1.5, 6.0])
    ops.node(189, *[40.0, -1.5, 7.0])
    ops.node(190, *[40.0, -1.5, 8.0])
    ops.node(191, *[40.0, -1.5, 9.0])
    ops.node(192, *[40.0, 1.5, 1.0])
    ops.node(193, *[40.0, 1.5, 2.0])
    ops.node(194, *[40.0, 1.5, 3.0])
    ops.node(195, *[40.0, 1.5, 4.0])
    ops.node(196, *[40.0, 1.5, 5.0])
    ops.node(197, *[40.0, 1.5, 6.0])
    ops.node(198, *[40.0, 1.5, 7.0])
    ops.node(199, *[40.0, 1.5, 8.0])
    ops.node(200, *[40.0, 1.5, 9.0])

    # Fix the node.
    ops.fix(1, *[1, 1, 1, 0, 0, 0])
    ops.fix(4, *[1, 1, 1, 0, 0, 0])
    ops.fix(143, *[1, 1, 1, 0, 0, 0])
    ops.fix(144, *[1, 1, 1, 0, 0, 0])
    ops.fix(145, *[1, 1, 1, 1, 1, 1])
    ops.fix(146, *[1, 1, 1, 1, 1, 1])
    ops.fix(147, *[1, 1, 1, 1, 1, 1])
    ops.fix(148, *[1, 1, 1, 1, 1, 1])

    # Mechanical properties DataFrame of sec
    FrameSecProp_df = dict()
    FrameSecProp = namedtuple(
        'FrameSecProp', ('matName', 'A', 'J', 'I33', 'I22', 'AS2', 'AS3'))
    FrameSecProp_df["FSEC1"] = FrameSecProp._make(
        ['A709Gr50', 0.0042645076, 9.65117678053953e-08, 6.5724174702235e-05, 3.30125717301008e-06, 0.00193548, 0.00204300666666667])

    # Create OpenSees elements.
    # element('elasticBeamColumn', eleTag, *eleNodes, Area, E_mod, G_mod, Jxx, Iy, Iz, transfTag, <'-mass', mass>, <'-cMass'>)
    ops.element('elasticBeamColumn', 1, *[1, 2], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 2, *[1, 3], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 3, *[2, 3], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 4, *[4, 5], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 5, *[4, 6], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 6, *[5, 6], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 7, *[4, 1], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 8, *[2, 7], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 9, *[3, 8], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 10, *[7, 8], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 11, *[5, 9], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 12, *[6, 10], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 13, *[9, 10], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 14, *[5, 2], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 15, *[7, 11], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 16, *[8, 12], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 17, *[11, 12], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 18, *[9, 13], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 19, *[10, 14], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 20, *[13, 14], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 21, *[9, 7], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 22, *[11, 15], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 23, *[12, 16], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 24, *[15, 16], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 25, *[13, 17], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 26, *[14, 18], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 27, *[17, 18], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 28, *[13, 11], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 29, *[15, 19], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 30, *[16, 20], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 31, *[19, 20], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 32, *[17, 21], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 33, *[18, 22], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 34, *[21, 22], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 35, *[17, 15], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 36, *[19, 23], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 37, *[20, 24], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 38, *[21, 25], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 39, *[22, 26], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 40, *[21, 19], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 41, *[23, 27], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 42, *[24, 28], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 43, *[27, 28], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 44, *[25, 29], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 45, *[26, 30], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 46, *[29, 30], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 47, *[25, 23], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 48, *[27, 31], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 49, *[28, 32], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 50, *[31, 32], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 51, *[29, 33], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 52, *[30, 34], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 53, *[33, 34], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 54, *[29, 27], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 55, *[31, 35], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 56, *[32, 36], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 57, *[35, 36], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 58, *[33, 37], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 59, *[34, 38], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 60, *[37, 38], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 61, *[33, 31], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 62, *[35, 39], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 63, *[36, 40], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 64, *[39, 40], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 65, *[37, 41], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 66, *[38, 42], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 67, *[41, 42], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 68, *[37, 35], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 69, *[39, 43], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 70, *[40, 44], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 71, *[43, 44], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 72, *[41, 45], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 73, *[42, 46], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 74, *[45, 46], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 75, *[41, 39], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 76, *[43, 47], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 77, *[44, 48], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 78, *[47, 48], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 79, *[45, 49], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 80, *[46, 50], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 81, *[49, 50], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 82, *[45, 43], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 83, *[47, 51], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 84, *[48, 52], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 85, *[51, 52], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 86, *[49, 53], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 87, *[50, 54], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 88, *[53, 54], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 89, *[49, 47], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 90, *[51, 55], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 91, *[52, 56], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 92, *[55, 56], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 93, *[53, 57], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 94, *[54, 58], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 95, *[57, 58], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 96, *[53, 51], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 97, *[55, 59], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 98, *[56, 60], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 99, *[59, 60], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 100, *[57, 61], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 101, *[58, 62], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 102, *[61, 62], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 103, *[57, 55], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 104, *[59, 63], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 105, *[60, 64], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 106, *[63, 64], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 107, *[61, 65], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 108, *[62, 66], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 109, *[65, 66], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 110, *[61, 59], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 111, *[63, 67], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 112, *[64, 68], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 113, *[67, 68], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 114, *[65, 69], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 115, *[66, 70], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 116, *[69, 70], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 117, *[65, 63], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 118, *[67, 71], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 119, *[68, 72], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 120, *[71, 72], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 121, *[69, 73], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 122, *[70, 74], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 123, *[73, 74], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 124, *[69, 67], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 125, *[71, 75], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 126, *[72, 76], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 127, *[75, 76], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 128, *[73, 77], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 129, *[74, 78], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 130, *[77, 78], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 131, *[73, 71], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 132, *[75, 79], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 133, *[76, 80], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 134, *[79, 80], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 135, *[77, 81], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 136, *[78, 82], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 137, *[81, 82], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 138, *[77, 75], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 139, *[79, 83], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 140, *[80, 84], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 141, *[83, 84], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 142, *[81, 85], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 143, *[82, 86], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 144, *[85, 86], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 145, *[81, 79], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 146, *[83, 87], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 147, *[84, 88], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 148, *[87, 88], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 149, *[85, 89], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 150, *[86, 90], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 151, *[89, 90], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 152, *[85, 83], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 153, *[87, 91], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 154, *[88, 92], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 155, *[91, 92], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 156, *[89, 93], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 157, *[90, 94], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 158, *[93, 94], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 159, *[89, 87], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 160, *[91, 95], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 161, *[92, 96], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 162, *[95, 96], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 163, *[93, 97], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 164, *[94, 98], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 165, *[97, 98], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 166, *[93, 91], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 167, *[95, 99], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 168, *[96, 100], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 169, *[99, 100], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E,
                MatProp_df['A709Gr50'].G, FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 170, *[97, 101], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 171, *[98, 102], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 172, *[101, 102], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E,
                MatProp_df['A709Gr50'].G, FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 173, *[97, 95], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 174, *[99, 103], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 175, *[100, 104], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 176, *[103, 104], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E,
                MatProp_df['A709Gr50'].G, FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 177, *[101, 105], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 178, *[102, 106], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 179, *[105, 106], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E,
                MatProp_df['A709Gr50'].G, FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 180, *[101, 99], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 181, *[103, 107], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 182, *[104, 108], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 183, *[107, 108], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E,
                MatProp_df['A709Gr50'].G, FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 184, *[105, 109], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 185, *[106, 110], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 186, *[109, 110], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E,
                MatProp_df['A709Gr50'].G, FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 187, *[105, 103], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 188, *[107, 111], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 189, *[108, 112], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 190, *[111, 112], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E,
                MatProp_df['A709Gr50'].G, FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 191, *[109, 113], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 192, *[110, 114], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 193, *[113, 114], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E,
                MatProp_df['A709Gr50'].G, FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 194, *[109, 107], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 195, *[111, 115], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 196, *[112, 116], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 197, *[115, 116], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E,
                MatProp_df['A709Gr50'].G, FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 198, *[113, 117], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 199, *[114, 118], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 200, *[117, 118], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E,
                MatProp_df['A709Gr50'].G, FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 201, *[113, 111], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 202, *[115, 119], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 203, *[116, 120], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 204, *[117, 121], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 205, *[118, 122], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 206, *[117, 115], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 207, *[119, 123], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 208, *[120, 124], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 209, *[123, 124], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E,
                MatProp_df['A709Gr50'].G, FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 210, *[121, 125], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 211, *[122, 126], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 212, *[125, 126], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E,
                MatProp_df['A709Gr50'].G, FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 213, *[121, 119], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 214, *[123, 127], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 215, *[124, 128], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 216, *[127, 128], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E,
                MatProp_df['A709Gr50'].G, FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 217, *[125, 129], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 218, *[126, 130], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 219, *[129, 130], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E,
                MatProp_df['A709Gr50'].G, FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 220, *[125, 123], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 221, *[127, 131], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 222, *[128, 132], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 223, *[131, 132], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E,
                MatProp_df['A709Gr50'].G, FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 224, *[129, 133], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 225, *[130, 134], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 226, *[133, 134], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E,
                MatProp_df['A709Gr50'].G, FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 227, *[129, 127], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 228, *[131, 135], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 229, *[132, 136], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 230, *[135, 136], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E,
                MatProp_df['A709Gr50'].G, FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 231, *[133, 137], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 232, *[134, 138], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 233, *[137, 138], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E,
                MatProp_df['A709Gr50'].G, FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 234, *[133, 131], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 235, *[135, 139], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 236, *[136, 140], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 237, *[139, 140], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E,
                MatProp_df['A709Gr50'].G, FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 238, *[137, 141], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 239, *[138, 142], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 240, *[141, 142], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E,
                MatProp_df['A709Gr50'].G, FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 241, *[137, 135], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 242, *[139, 143], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 243, *[140, 143], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 244, *[141, 144], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 245, *[142, 144], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 246, *[141, 139], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 247, *[143, 144], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E, MatProp_df['A709Gr50'].G,
                FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Other)
    ops.element('elasticBeamColumn', 248, *[145, 149], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E,
                MatProp_df['A709Gr50'].G, FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 249, *[149, 150], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E,
                MatProp_df['A709Gr50'].G, FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 250, *[150, 151], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E,
                MatProp_df['A709Gr50'].G, FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 251, *[151, 152], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E,
                MatProp_df['A709Gr50'].G, FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 252, *[152, 23], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E,
                MatProp_df['A709Gr50'].G, FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 253, *[146, 153], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E,
                MatProp_df['A709Gr50'].G, FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 254, *[153, 154], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E,
                MatProp_df['A709Gr50'].G, FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 255, *[154, 155], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E,
                MatProp_df['A709Gr50'].G, FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 256, *[155, 156], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E,
                MatProp_df['A709Gr50'].G, FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 257, *[156, 25], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E,
                MatProp_df['A709Gr50'].G, FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 258, *[147, 157], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E,
                MatProp_df['A709Gr50'].G, FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 259, *[157, 158], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E,
                MatProp_df['A709Gr50'].G, FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 260, *[158, 159], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E,
                MatProp_df['A709Gr50'].G, FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 261, *[159, 160], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E,
                MatProp_df['A709Gr50'].G, FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 262, *[160, 119], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E,
                MatProp_df['A709Gr50'].G, FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 263, *[148, 161], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E,
                MatProp_df['A709Gr50'].G, FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 264, *[161, 162], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E,
                MatProp_df['A709Gr50'].G, FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 265, *[162, 163], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E,
                MatProp_df['A709Gr50'].G, FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 266, *[163, 164], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E,
                MatProp_df['A709Gr50'].G, FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 267, *[164, 121], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E,
                MatProp_df['A709Gr50'].G, FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 268, *[23, 165], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E,
                MatProp_df['A709Gr50'].G, FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 269, *[165, 166], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E,
                MatProp_df['A709Gr50'].G, FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 270, *[166, 167], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E,
                MatProp_df['A709Gr50'].G, FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 271, *[167, 168], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E,
                MatProp_df['A709Gr50'].G, FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 272, *[168, 169], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E,
                MatProp_df['A709Gr50'].G, FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 273, *[169, 170], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E,
                MatProp_df['A709Gr50'].G, FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 274, *[170, 171], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E,
                MatProp_df['A709Gr50'].G, FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 275, *[171, 172], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E,
                MatProp_df['A709Gr50'].G, FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 276, *[172, 173], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E,
                MatProp_df['A709Gr50'].G, FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 277, *[173, 24], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E,
                MatProp_df['A709Gr50'].G, FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 278, *[25, 174], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E,
                MatProp_df['A709Gr50'].G, FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 279, *[174, 175], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E,
                MatProp_df['A709Gr50'].G, FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 280, *[175, 176], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E,
                MatProp_df['A709Gr50'].G, FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 281, *[176, 177], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E,
                MatProp_df['A709Gr50'].G, FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 282, *[177, 178], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E,
                MatProp_df['A709Gr50'].G, FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 283, *[178, 179], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E,
                MatProp_df['A709Gr50'].G, FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 284, *[179, 180], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E,
                MatProp_df['A709Gr50'].G, FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 285, *[180, 181], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E,
                MatProp_df['A709Gr50'].G, FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 286, *[181, 182], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E,
                MatProp_df['A709Gr50'].G, FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 287, *[182, 26], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E,
                MatProp_df['A709Gr50'].G, FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 288, *[119, 183], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E,
                MatProp_df['A709Gr50'].G, FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 289, *[183, 184], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E,
                MatProp_df['A709Gr50'].G, FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 290, *[184, 185], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E,
                MatProp_df['A709Gr50'].G, FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 291, *[185, 186], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E,
                MatProp_df['A709Gr50'].G, FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 292, *[186, 187], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E,
                MatProp_df['A709Gr50'].G, FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 293, *[187, 188], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E,
                MatProp_df['A709Gr50'].G, FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 294, *[188, 189], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E,
                MatProp_df['A709Gr50'].G, FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 295, *[189, 190], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E,
                MatProp_df['A709Gr50'].G, FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 296, *[190, 191], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E,
                MatProp_df['A709Gr50'].G, FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 297, *[191, 120], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E,
                MatProp_df['A709Gr50'].G, FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 298, *[121, 192], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E,
                MatProp_df['A709Gr50'].G, FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 299, *[192, 193], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E,
                MatProp_df['A709Gr50'].G, FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 300, *[193, 194], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E,
                MatProp_df['A709Gr50'].G, FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 301, *[194, 195], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E,
                MatProp_df['A709Gr50'].G, FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 302, *[195, 196], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E,
                MatProp_df['A709Gr50'].G, FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 303, *[196, 197], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E,
                MatProp_df['A709Gr50'].G, FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 304, *[197, 198], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E,
                MatProp_df['A709Gr50'].G, FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 305, *[198, 199], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E,
                MatProp_df['A709Gr50'].G, FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 306, *[199, 200], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E,
                MatProp_df['A709Gr50'].G, FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)
    ops.element('elasticBeamColumn', 307, *[200, 122], FrameSecProp_df['FSEC1'].A, MatProp_df['A709Gr50'].E,
                MatProp_df['A709Gr50'].G, FrameSecProp_df['FSEC1'].J, FrameSecProp_df['FSEC1'].I33, FrameSecProp_df['FSEC1'].I22, transf_Ver)

    # Plate_Shell element.
    ops.nDMaterial('ElasticIsotropic', 1, 24855578.0600518, 0.2)
    ops.nDMaterial('PlateFiber', 2, 1)
    ops.section('PlateFiber', 3, 2, 0.25)
    # Create Plate_Shell element.
    ops.element('ShellMITC4', 308, *[5, 4, 1, 2], 3)
    ops.element('ShellMITC4', 309, *[9, 5, 2, 7], 3)
    ops.element('ShellMITC4', 310, *[13, 9, 7, 11], 3)
    ops.element('ShellMITC4', 311, *[17, 13, 11, 15], 3)
    ops.element('ShellMITC4', 312, *[21, 17, 15, 19], 3)
    ops.element('ShellMITC4', 313, *[25, 21, 19, 23], 3)
    ops.element('ShellMITC4', 314, *[29, 25, 23, 27], 3)
    ops.element('ShellMITC4', 315, *[33, 29, 27, 31], 3)
    ops.element('ShellMITC4', 316, *[37, 33, 31, 35], 3)
    ops.element('ShellMITC4', 317, *[41, 37, 35, 39], 3)
    ops.element('ShellMITC4', 318, *[45, 41, 39, 43], 3)
    ops.element('ShellMITC4', 319, *[49, 45, 43, 47], 3)
    ops.element('ShellMITC4', 320, *[53, 49, 47, 51], 3)
    ops.element('ShellMITC4', 321, *[57, 53, 51, 55], 3)
    ops.element('ShellMITC4', 322, *[61, 57, 55, 59], 3)
    ops.element('ShellMITC4', 323, *[65, 61, 59, 63], 3)
    ops.element('ShellMITC4', 324, *[69, 65, 63, 67], 3)
    ops.element('ShellMITC4', 325, *[73, 69, 67, 71], 3)
    ops.element('ShellMITC4', 326, *[77, 73, 71, 75], 3)
    ops.element('ShellMITC4', 327, *[81, 77, 75, 79], 3)
    ops.element('ShellMITC4', 328, *[85, 81, 79, 83], 3)
    ops.element('ShellMITC4', 329, *[89, 85, 83, 87], 3)
    ops.element('ShellMITC4', 330, *[93, 89, 87, 91], 3)
    ops.element('ShellMITC4', 331, *[97, 93, 91, 95], 3)
    ops.element('ShellMITC4', 332, *[101, 97, 95, 99], 3)
    ops.element('ShellMITC4', 333, *[105, 101, 99, 103], 3)
    ops.element('ShellMITC4', 334, *[109, 105, 103, 107], 3)
    ops.element('ShellMITC4', 335, *[113, 109, 107, 111], 3)
    ops.element('ShellMITC4', 336, *[117, 113, 111, 115], 3)
    ops.element('ShellMITC4', 337, *[121, 117, 115, 119], 3)
    ops.element('ShellMITC4', 338, *[125, 121, 119, 123], 3)
    ops.element('ShellMITC4', 339, *[129, 125, 123, 127], 3)
    ops.element('ShellMITC4', 340, *[133, 129, 127, 131], 3)
    ops.element('ShellMITC4', 341, *[137, 133, 131, 135], 3)
    ops.element('ShellMITC4', 342, *[141, 137, 135, 139], 3)
    ops.element('ShellMITC4', 343, *[144, 141, 139, 143], 3)

    # Set the mass at a node.
    ops.mass(1, *[1.6637072645854196, 1.6637072645854196, 1.6637072645854196])
    ops.mass(2, *[3.1698938312816636, 3.1698938312816636, 3.1698938312816636])
    ops.mass(3, *[0.11813364107720811,
             0.11813364107720811, 0.11813364107720811])
    ops.mass(4, *[1.6637072645854196, 1.6637072645854196, 1.6637072645854196])
    ops.mass(5, *[3.1698938312816636, 3.1698938312816636, 3.1698938312816636])
    ops.mass(6, *[0.11813364107720811,
             0.11813364107720811, 0.11813364107720811])
    ops.mass(7, *[3.183840632200247, 3.183840632200247, 3.183840632200247])
    ops.mass(8, *[0.13653600519874923,
             0.13653600519874923, 0.13653600519874923])
    ops.mass(9, *[3.183840632200247, 3.183840632200247, 3.183840632200247])
    ops.mass(10, *[0.13653600519874923,
             0.13653600519874923, 0.13653600519874923])
    ops.mass(11, *[3.2070853003978863, 3.2070853003978863, 3.2070853003978863])
    ops.mass(12, *[0.1668615902674156, 0.1668615902674156, 0.1668615902674156])
    ops.mass(13, *[3.2070853003978863, 3.2070853003978863, 3.2070853003978863])
    ops.mass(14, *[0.1668615902674156, 0.1668615902674156, 0.1668615902674156])
    ops.mass(15, *[3.2396278358745803, 3.2396278358745803, 3.2396278358745803])
    ops.mass(16, *[0.2087019930231647, 0.2087019930231647, 0.2087019930231647])
    ops.mass(17, *[3.2396278358745803, 3.2396278358745803, 3.2396278358745803])
    ops.mass(18, *[0.2087019930231647, 0.2087019930231647, 0.2087019930231647])
    ops.mass(19, *[3.2814682386303273, 3.2814682386303273, 3.2814682386303273])
    ops.mass(20, *[0.2616365022621502, 0.2616365022621502, 0.2616365022621502])
    ops.mass(21, *[3.2814682386303273, 3.2814682386303273, 3.2814682386303273])
    ops.mass(22, *[0.2616365022621502, 0.2616365022621502, 0.2616365022621502])
    ops.mass(23, *[3.198717219846733, 3.198717219846733, 3.198717219846733])
    ops.mass(24, *[0.15216089812966097,
             0.15216089812966097, 0.15216089812966097])
    ops.mass(25, *[3.198717219846733, 3.198717219846733, 3.198717219846733])
    ops.mass(26, *[0.15216089812966097,
             0.15216089812966097, 0.15216089812966097])
    ops.mass(27, *[3.3112214139233043, 3.3112214139233043, 3.3112214139233043])
    ops.mass(28, *[0.2648275792436708, 0.2648275792436708, 0.2648275792436708])
    ops.mass(29, *[3.3112214139233043, 3.3112214139233043, 3.3112214139233043])
    ops.mass(30, *[0.2648275792436708, 0.2648275792436708, 0.2648275792436708])
    ops.mass(31, *[3.2916958926372883, 3.2916958926372883, 3.2916958926372883])
    ops.mass(32, *[0.2440739776138226, 0.2440739776138226, 0.2440739776138226])
    ops.mass(33, *[3.2916958926372883, 3.2916958926372883, 3.2916958926372883])
    ops.mass(34, *[0.2440739776138226, 0.2440739776138226, 0.2440739776138226])
    ops.mass(35, *[3.2740299448070833, 3.2740299448070833, 3.2740299448070833])
    ops.mass(36, *[0.2252857651245705, 0.2252857651245705, 0.2252857651245705])
    ops.mass(37, *[3.2740299448070833, 3.2740299448070833, 3.2740299448070833])
    ops.mass(38, *[0.2252857651245705, 0.2252857651245705, 0.2252857651245705])
    ops.mass(39, *[3.258223570432691, 3.258223570432691, 3.258223570432691])
    ops.mass(40, *[0.20846602407446996,
             0.20846602407446996, 0.20846602407446996])
    ops.mass(41, *[3.258223570432691, 3.258223570432691, 3.258223570432691])
    ops.mass(42, *[0.20846602407446996,
             0.20846602407446996, 0.20846602407446996])
    ops.mass(43, *[3.244276769514106, 3.244276769514106, 3.244276769514106])
    ops.mass(44, *[0.19361764113832441,
             0.19361764113832441, 0.19361764113832441])
    ops.mass(45, *[3.244276769514106, 3.244276769514106, 3.244276769514106])
    ops.mass(46, *[0.19361764113832441,
             0.19361764113832441, 0.19361764113832441])
    ops.mass(47, *[3.2321895420513345, 3.2321895420513345, 3.2321895420513345])
    ops.mass(48, *[0.18074327075101088,
             0.18074327075101088, 0.18074327075101088])
    ops.mass(49, *[3.2321895420513345, 3.2321895420513345, 3.2321895420513345])
    ops.mass(50, *[0.18074327075101088,
             0.18074327075101088, 0.18074327075101088])
    ops.mass(51, *[3.221961888044375, 3.221961888044375, 3.221961888044375])
    ops.mass(52, *[0.16984529940200416,
             0.16984529940200416, 0.16984529940200416])
    ops.mass(53, *[3.221961888044375, 3.221961888044375, 3.221961888044375])
    ops.mass(54, *[0.16984529940200416,
             0.16984529940200416, 0.16984529940200416])
    ops.mass(55, *[3.2135938074932238, 3.2135938074932238, 3.2135938074932238])
    ops.mass(56, *[0.16092581184638335,
             0.16092581184638335, 0.16092581184638335])
    ops.mass(57, *[3.2135938074932238, 3.2135938074932238, 3.2135938074932238])
    ops.mass(58, *[0.16092581184638335,
             0.16092581184638335, 0.16092581184638335])
    ops.mass(59, *[3.2070853003978845, 3.2070853003978845, 3.2070853003978845])
    ops.mass(60, *[0.15398656026441687,
             0.15398656026441687, 0.15398656026441687])
    ops.mass(61, *[3.2070853003978845, 3.2070853003978845, 3.2070853003978845])
    ops.mass(62, *[0.15398656026441687,
             0.15398656026441687, 0.15398656026441687])
    ops.mass(63, *[3.202436366758359, 3.202436366758359, 3.202436366758359])
    ops.mass(64, *[0.1490289373766895, 0.1490289373766895, 0.1490289373766895])
    ops.mass(65, *[3.202436366758359, 3.202436366758359, 3.202436366758359])
    ops.mass(66, *[0.1490289373766895, 0.1490289373766895, 0.1490289373766895])
    ops.mass(67, *[3.199647006574641, 3.199647006574641, 3.199647006574641])
    ops.mass(68, *[0.14605395444113967,
             0.14605395444113967, 0.14605395444113967])
    ops.mass(69, *[3.199647006574641, 3.199647006574641, 3.199647006574641])
    ops.mass(70, *[0.14605395444113967,
             0.14605395444113967, 0.14605395444113967])
    ops.mass(71, *[3.198717219846735, 3.198717219846735, 3.198717219846735])
    ops.mass(72, *[0.14506222492273554,
             0.14506222492273554, 0.14506222492273554])
    ops.mass(73, *[3.198717219846735, 3.198717219846735, 3.198717219846735])
    ops.mass(74, *[0.14506222492273554,
             0.14506222492273554, 0.14506222492273554])
    ops.mass(75, *[3.1996470065746423, 3.1996470065746423, 3.1996470065746423])
    ops.mass(76, *[0.14605395444113986,
             0.14605395444113986, 0.14605395444113986])
    ops.mass(77, *[3.1996470065746423, 3.1996470065746423, 3.1996470065746423])
    ops.mass(78, *[0.14605395444113986,
             0.14605395444113986, 0.14605395444113986])
    ops.mass(79, *[3.202436366758357, 3.202436366758357, 3.202436366758357])
    ops.mass(80, *[0.14902893737668935,
             0.14902893737668935, 0.14902893737668935])
    ops.mass(81, *[3.202436366758357, 3.202436366758357, 3.202436366758357])
    ops.mass(82, *[0.14902893737668935,
             0.14902893737668935, 0.14902893737668935])
    ops.mass(83, *[3.2070853003978845, 3.2070853003978845, 3.2070853003978845])
    ops.mass(84, *[0.15398656026441687,
             0.15398656026441687, 0.15398656026441687])
    ops.mass(85, *[3.2070853003978845, 3.2070853003978845, 3.2070853003978845])
    ops.mass(86, *[0.15398656026441687,
             0.15398656026441687, 0.15398656026441687])
    ops.mass(87, *[3.2135938074932238, 3.2135938074932238, 3.2135938074932238])
    ops.mass(88, *[0.16092581184638335,
             0.16092581184638335, 0.16092581184638335])
    ops.mass(89, *[3.2135938074932238, 3.2135938074932238, 3.2135938074932238])
    ops.mass(90, *[0.16092581184638335,
             0.16092581184638335, 0.16092581184638335])
    ops.mass(91, *[3.2219618880443717, 3.2219618880443717, 3.2219618880443717])
    ops.mass(92, *[0.16984529940200382,
             0.16984529940200382, 0.16984529940200382])
    ops.mass(93, *[3.2219618880443717, 3.2219618880443717, 3.2219618880443717])
    ops.mass(94, *[0.16984529940200382,
             0.16984529940200382, 0.16984529940200382])
    ops.mass(95, *[3.2321895420513345, 3.2321895420513345, 3.2321895420513345])
    ops.mass(96, *[0.18074327075101088,
             0.18074327075101088, 0.18074327075101088])
    ops.mass(97, *[3.2321895420513345, 3.2321895420513345, 3.2321895420513345])
    ops.mass(98, *[0.18074327075101088,
             0.18074327075101088, 0.18074327075101088])
    ops.mass(99, *[3.244276769514106, 3.244276769514106, 3.244276769514106])
    ops.mass(100, *[0.19361764113832441,
             0.19361764113832441, 0.19361764113832441])
    ops.mass(101, *[3.244276769514106, 3.244276769514106, 3.244276769514106])
    ops.mass(102, *[0.19361764113832441,
             0.19361764113832441, 0.19361764113832441])
    ops.mass(103, *[3.2582235704326874,
             3.2582235704326874, 3.2582235704326874])
    ops.mass(104, *[0.20846602407446965,
             0.20846602407446965, 0.20846602407446965])
    ops.mass(105, *[3.2582235704326874,
             3.2582235704326874, 3.2582235704326874])
    ops.mass(106, *[0.20846602407446965,
             0.20846602407446965, 0.20846602407446965])
    ops.mass(107, *[3.2740299448070833,
             3.2740299448070833, 3.2740299448070833])
    ops.mass(108, *[0.22528576512457066,
             0.22528576512457066, 0.22528576512457066])
    ops.mass(109, *[3.2740299448070833,
             3.2740299448070833, 3.2740299448070833])
    ops.mass(110, *[0.22528576512457066,
             0.22528576512457066, 0.22528576512457066])
    ops.mass(111, *[3.2916958926372883,
             3.2916958926372883, 3.2916958926372883])
    ops.mass(112, *[0.24407397761382277,
             0.24407397761382277, 0.24407397761382277])
    ops.mass(113, *[3.2916958926372883,
             3.2916958926372883, 3.2916958926372883])
    ops.mass(114, *[0.24407397761382277,
             0.24407397761382277, 0.24407397761382277])
    ops.mass(115, *[3.3112214139233025,
             3.3112214139233025, 3.3112214139233025])
    ops.mass(116, *[0.26482757924367056,
             0.26482757924367056, 0.26482757924367056])
    ops.mass(117, *[3.3112214139233025,
             3.3112214139233025, 3.3112214139233025])
    ops.mass(118, *[0.26482757924367056,
             0.26482757924367056, 0.26482757924367056])
    ops.mass(119, *[3.198717219846733, 3.198717219846733, 3.198717219846733])
    ops.mass(120, *[0.15216089812966097,
             0.15216089812966097, 0.15216089812966097])
    ops.mass(121, *[3.198717219846733, 3.198717219846733, 3.198717219846733])
    ops.mass(122, *[0.15216089812966097,
             0.15216089812966097, 0.15216089812966097])
    ops.mass(123, *[3.2814682386303273,
             3.2814682386303273, 3.2814682386303273])
    ops.mass(124, *[0.2616365022621504,
             0.2616365022621504, 0.2616365022621504])
    ops.mass(125, *[3.2814682386303273,
             3.2814682386303273, 3.2814682386303273])
    ops.mass(126, *[0.2616365022621504,
             0.2616365022621504, 0.2616365022621504])
    ops.mass(127, *[3.2396278358745785,
             3.2396278358745785, 3.2396278358745785])
    ops.mass(128, *[0.20870199302316472,
             0.20870199302316472, 0.20870199302316472])
    ops.mass(129, *[3.2396278358745785,
             3.2396278358745785, 3.2396278358745785])
    ops.mass(130, *[0.20870199302316472,
             0.20870199302316472, 0.20870199302316472])
    ops.mass(131, *[3.207085300397883, 3.207085300397883, 3.207085300397883])
    ops.mass(132, *[0.1668615902674156,
             0.1668615902674156, 0.1668615902674156])
    ops.mass(133, *[3.207085300397883, 3.207085300397883, 3.207085300397883])
    ops.mass(134, *[0.1668615902674156,
             0.1668615902674156, 0.1668615902674156])
    ops.mass(135, *[3.183840632200247, 3.183840632200247, 3.183840632200247])
    ops.mass(136, *[0.1365360051987494,
             0.1365360051987494, 0.1365360051987494])
    ops.mass(137, *[3.183840632200247, 3.183840632200247, 3.183840632200247])
    ops.mass(138, *[0.1365360051987494,
             0.1365360051987494, 0.1365360051987494])
    ops.mass(139, *[3.1698938312816636,
             3.1698938312816636, 3.1698938312816636])
    ops.mass(140, *[0.11813364107720811,
             0.11813364107720811, 0.11813364107720811])
    ops.mass(141, *[3.1698938312816636,
             3.1698938312816636, 3.1698938312816636])
    ops.mass(142, *[0.11813364107720811,
             0.11813364107720811, 0.11813364107720811])
    ops.mass(143, *[1.6637072645854176,
             1.6637072645854176, 1.6637072645854176])
    ops.mass(144, *[1.6637072645854176,
             1.6637072645854176, 1.6637072645854176])
    ops.mass(145, *[0.016736161102299585,
                    0.016736161102299585, 0.016736161102299585])
    ops.mass(146, *[0.016736161102299585,
                    0.016736161102299585, 0.016736161102299585])
    ops.mass(147, *[0.016736161102299585,
                    0.016736161102299585, 0.016736161102299585])
    ops.mass(148, *[0.016736161102299585,
                    0.016736161102299585, 0.016736161102299585])
    ops.mass(149, *[0.03347232220459917,
             0.03347232220459917, 0.03347232220459917])
    ops.mass(150, *[0.03347232220459917,
             0.03347232220459917, 0.03347232220459917])
    ops.mass(151, *[0.03347232220459917,
             0.03347232220459917, 0.03347232220459917])
    ops.mass(152, *[0.03347232220459917,
             0.03347232220459917, 0.03347232220459917])
    ops.mass(153, *[0.03347232220459917,
             0.03347232220459917, 0.03347232220459917])
    ops.mass(154, *[0.03347232220459917,
             0.03347232220459917, 0.03347232220459917])
    ops.mass(155, *[0.03347232220459917,
             0.03347232220459917, 0.03347232220459917])
    ops.mass(156, *[0.03347232220459917,
             0.03347232220459917, 0.03347232220459917])
    ops.mass(157, *[0.03347232220459917,
             0.03347232220459917, 0.03347232220459917])
    ops.mass(158, *[0.03347232220459917,
             0.03347232220459917, 0.03347232220459917])
    ops.mass(159, *[0.03347232220459917,
             0.03347232220459917, 0.03347232220459917])
    ops.mass(160, *[0.03347232220459917,
             0.03347232220459917, 0.03347232220459917])
    ops.mass(161, *[0.03347232220459917,
             0.03347232220459917, 0.03347232220459917])
    ops.mass(162, *[0.03347232220459917,
             0.03347232220459917, 0.03347232220459917])
    ops.mass(163, *[0.03347232220459917,
             0.03347232220459917, 0.03347232220459917])
    ops.mass(164, *[0.03347232220459917,
             0.03347232220459917, 0.03347232220459917])
    ops.mass(165, *[0.03347232220459917,
             0.03347232220459917, 0.03347232220459917])
    ops.mass(166, *[0.03347232220459917,
             0.03347232220459917, 0.03347232220459917])
    ops.mass(167, *[0.03347232220459917,
             0.03347232220459917, 0.03347232220459917])
    ops.mass(168, *[0.03347232220459917,
             0.03347232220459917, 0.03347232220459917])
    ops.mass(169, *[0.03347232220459917,
             0.03347232220459917, 0.03347232220459917])
    ops.mass(170, *[0.03347232220459917,
             0.03347232220459917, 0.03347232220459917])
    ops.mass(171, *[0.033472322204599156,
                    0.033472322204599156, 0.033472322204599156])
    ops.mass(172, *[0.033472322204599156,
                    0.033472322204599156, 0.033472322204599156])
    ops.mass(173, *[0.03347232220459917,
             0.03347232220459917, 0.03347232220459917])
    ops.mass(174, *[0.03347232220459917,
             0.03347232220459917, 0.03347232220459917])
    ops.mass(175, *[0.03347232220459917,
             0.03347232220459917, 0.03347232220459917])
    ops.mass(176, *[0.03347232220459917,
             0.03347232220459917, 0.03347232220459917])
    ops.mass(177, *[0.03347232220459917,
             0.03347232220459917, 0.03347232220459917])
    ops.mass(178, *[0.03347232220459917,
             0.03347232220459917, 0.03347232220459917])
    ops.mass(179, *[0.03347232220459917,
             0.03347232220459917, 0.03347232220459917])
    ops.mass(180, *[0.033472322204599156,
                    0.033472322204599156, 0.033472322204599156])
    ops.mass(181, *[0.033472322204599156,
                    0.033472322204599156, 0.033472322204599156])
    ops.mass(182, *[0.03347232220459917,
             0.03347232220459917, 0.03347232220459917])
    ops.mass(183, *[0.03347232220459917,
             0.03347232220459917, 0.03347232220459917])
    ops.mass(184, *[0.03347232220459917,
             0.03347232220459917, 0.03347232220459917])
    ops.mass(185, *[0.03347232220459917,
             0.03347232220459917, 0.03347232220459917])
    ops.mass(186, *[0.03347232220459917,
             0.03347232220459917, 0.03347232220459917])
    ops.mass(187, *[0.03347232220459917,
             0.03347232220459917, 0.03347232220459917])
    ops.mass(188, *[0.03347232220459917,
             0.03347232220459917, 0.03347232220459917])
    ops.mass(189, *[0.033472322204599156,
                    0.033472322204599156, 0.033472322204599156])
    ops.mass(190, *[0.033472322204599156,
                    0.033472322204599156, 0.033472322204599156])
    ops.mass(191, *[0.03347232220459917,
             0.03347232220459917, 0.03347232220459917])
    ops.mass(192, *[0.03347232220459917,
             0.03347232220459917, 0.03347232220459917])
    ops.mass(193, *[0.03347232220459917,
             0.03347232220459917, 0.03347232220459917])
    ops.mass(194, *[0.03347232220459917,
             0.03347232220459917, 0.03347232220459917])
    ops.mass(195, *[0.03347232220459917,
             0.03347232220459917, 0.03347232220459917])
    ops.mass(196, *[0.03347232220459917,
             0.03347232220459917, 0.03347232220459917])
    ops.mass(197, *[0.03347232220459917,
             0.03347232220459917, 0.03347232220459917])
    ops.mass(198, *[0.033472322204599156,
                    0.033472322204599156, 0.033472322204599156])
    ops.mass(199, *[0.033472322204599156,
                    0.033472322204599156, 0.033472322204599156])
    ops.mass(200, *[0.03347232220459917,
             0.03347232220459917, 0.03347232220459917])
