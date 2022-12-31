# !-*- coding:utf-8 -*-

# This document was created from Midas2OPS version 0.01
from collections import namedtuple
import openseespy.opensees as ops


def Frame3D():
    ops.wipe()
    # Set the default model dimensions and number of dofs.
    ops.model('basic', '-ndm', 3, '-ndf', 6)

    # Mechanical properties of material
    # E-Elastic Modulus; G-Shear Modulus; v-Poisson's ratio; rho-Mass Density;
    # gamma-unit weight; r: expansion coefficient
    mat_props = namedtuple(
        'mat_props', ['mat_name', 'E', 'v', 'G', 'r', 'gamma', 'rho'])
    MatProps = dict()
    MatProps[1] = mat_props._make(
        ('C40', 32500000.0, 0.2, 13541666.666666668, 5.5556e-06, 25.0, 2.5493))

    # Mechanical properties of Sections
    # A-Area; Asy-Shear area along y; Asz-Shear area along z;
    # Ixx-torsional; Iyy-inertia moment about y; Izz-inertia moment about z;
    sec_props = namedtuple(
        'sec_props', ['sec_name', 'A', 'Asy', 'Asz', 'Ixx', 'Iyy', 'Izz'])
    SecProps = dict()
    SecProps[1] = sec_props._make(
        ('yan', 0.25, 0.2083, 0.2083, 0.0088, 0.0052, 0.0052))

    # Create OpenSees node.
    ops.node(1, 0, 0, 0)
    ops.node(2, 5, 0, 0)
    ops.node(3, 10, 0, 0)
    ops.node(4, 15, 0, 0)
    ops.node(5, 20, 0, 0)
    ops.node(6, 25, 0, 0)
    ops.node(7, 0, 0, 5)
    ops.node(8, 5, 0, 5)
    ops.node(9, 10, 0, 5)
    ops.node(10, 15, 0, 5)
    ops.node(11, 20, 0, 5)
    ops.node(12, 25, 0, 5)
    ops.node(13, 0, 0, 10)
    ops.node(14, 5, 0, 10)
    ops.node(15, 10, 0, 10)
    ops.node(16, 15, 0, 10)
    ops.node(17, 20, 0, 10)
    ops.node(18, 25, 0, 10)
    ops.node(19, 0, 0, 15)
    ops.node(20, 5, 0, 15)
    ops.node(21, 10, 0, 15)
    ops.node(22, 15, 0, 15)
    ops.node(23, 20, 0, 15)
    ops.node(24, 25, 0, 15)
    ops.node(25, 0, 0, 20)
    ops.node(26, 5, 0, 20)
    ops.node(27, 10, 0, 20)
    ops.node(28, 15, 0, 20)
    ops.node(29, 20, 0, 20)
    ops.node(30, 25, 0, 20)
    ops.node(31, 0, 0, 25)
    ops.node(32, 5, 0, 25)
    ops.node(33, 10, 0, 25)
    ops.node(34, 15, 0, 25)
    ops.node(35, 20, 0, 25)
    ops.node(36, 25, 0, 25)
    ops.node(37, 0, 5, 0)
    ops.node(38, 5, 5, 0)
    ops.node(39, 10, 5, 0)
    ops.node(40, 15, 5, 0)
    ops.node(41, 20, 5, 0)
    ops.node(42, 25, 5, 0)
    ops.node(43, 0, 5, 5)
    ops.node(44, 5, 5, 5)
    ops.node(45, 10, 5, 5)
    ops.node(46, 15, 5, 5)
    ops.node(47, 20, 5, 5)
    ops.node(48, 25, 5, 5)
    ops.node(49, 0, 5, 10)
    ops.node(50, 5, 5, 10)
    ops.node(51, 10, 5, 10)
    ops.node(52, 15, 5, 10)
    ops.node(53, 20, 5, 10)
    ops.node(54, 25, 5, 10)
    ops.node(55, 0, 5, 15)
    ops.node(56, 5, 5, 15)
    ops.node(57, 10, 5, 15)
    ops.node(58, 15, 5, 15)
    ops.node(59, 20, 5, 15)
    ops.node(60, 25, 5, 15)
    ops.node(61, 0, 5, 20)
    ops.node(62, 5, 5, 20)
    ops.node(63, 10, 5, 20)
    ops.node(64, 15, 5, 20)
    ops.node(65, 20, 5, 20)
    ops.node(66, 25, 5, 20)
    ops.node(67, 0, 5, 25)
    ops.node(68, 5, 5, 25)
    ops.node(69, 10, 5, 25)
    ops.node(70, 15, 5, 25)
    ops.node(71, 20, 5, 25)
    ops.node(72, 25, 5, 25)
    ops.node(73, 0, 10, 0)
    ops.node(74, 5, 10, 0)
    ops.node(75, 10, 10, 0)
    ops.node(76, 15, 10, 0)
    ops.node(77, 20, 10, 0)
    ops.node(78, 25, 10, 0)
    ops.node(79, 0, 10, 5)
    ops.node(80, 5, 10, 5)
    ops.node(81, 10, 10, 5)
    ops.node(82, 15, 10, 5)
    ops.node(83, 20, 10, 5)
    ops.node(84, 25, 10, 5)
    ops.node(85, 0, 10, 10)
    ops.node(86, 5, 10, 10)
    ops.node(87, 10, 10, 10)
    ops.node(88, 15, 10, 10)
    ops.node(89, 20, 10, 10)
    ops.node(90, 25, 10, 10)
    ops.node(91, 0, 10, 15)
    ops.node(92, 5, 10, 15)
    ops.node(93, 10, 10, 15)
    ops.node(94, 15, 10, 15)
    ops.node(95, 20, 10, 15)
    ops.node(96, 25, 10, 15)
    ops.node(97, 0, 10, 20)
    ops.node(98, 5, 10, 20)
    ops.node(99, 10, 10, 20)
    ops.node(100, 15, 10, 20)
    ops.node(101, 20, 10, 20)
    ops.node(102, 25, 10, 20)
    ops.node(103, 0, 10, 25)
    ops.node(104, 5, 10, 25)
    ops.node(105, 10, 10, 25)
    ops.node(106, 15, 10, 25)
    ops.node(107, 20, 10, 25)
    ops.node(108, 25, 10, 25)
    ops.node(109, 0, 15, 0)
    ops.node(110, 5, 15, 0)
    ops.node(111, 10, 15, 0)
    ops.node(112, 15, 15, 0)
    ops.node(113, 20, 15, 0)
    ops.node(114, 25, 15, 0)
    ops.node(115, 0, 15, 5)
    ops.node(116, 5, 15, 5)
    ops.node(117, 10, 15, 5)
    ops.node(118, 15, 15, 5)
    ops.node(119, 20, 15, 5)
    ops.node(120, 25, 15, 5)
    ops.node(121, 0, 15, 10)
    ops.node(122, 5, 15, 10)
    ops.node(123, 10, 15, 10)
    ops.node(124, 15, 15, 10)
    ops.node(125, 20, 15, 10)
    ops.node(126, 25, 15, 10)
    ops.node(127, 0, 15, 15)
    ops.node(128, 5, 15, 15)
    ops.node(129, 10, 15, 15)
    ops.node(130, 15, 15, 15)
    ops.node(131, 20, 15, 15)
    ops.node(132, 25, 15, 15)
    ops.node(133, 0, 15, 20)
    ops.node(134, 5, 15, 20)
    ops.node(135, 10, 15, 20)
    ops.node(136, 15, 15, 20)
    ops.node(137, 20, 15, 20)
    ops.node(138, 25, 15, 20)
    ops.node(139, 0, 15, 25)
    ops.node(140, 5, 15, 25)
    ops.node(141, 10, 15, 25)
    ops.node(142, 15, 15, 25)
    ops.node(143, 20, 15, 25)
    ops.node(144, 25, 15, 25)
    ops.node(145, 0, 0, 30)
    ops.node(146, 5, 0, 30)
    ops.node(147, 10, 0, 30)
    ops.node(148, 15, 0, 30)
    ops.node(149, 20, 0, 30)
    ops.node(150, 25, 0, 30)
    ops.node(151, 0, 5, 30)
    ops.node(152, 5, 5, 30)
    ops.node(153, 10, 5, 30)
    ops.node(154, 15, 5, 30)
    ops.node(155, 20, 5, 30)
    ops.node(156, 25, 5, 30)
    ops.node(157, 0, 10, 30)
    ops.node(158, 5, 10, 30)
    ops.node(159, 10, 10, 30)
    ops.node(160, 15, 10, 30)
    ops.node(161, 20, 10, 30)
    ops.node(162, 25, 10, 30)
    ops.node(163, 0, 15, 30)
    ops.node(164, 5, 15, 30)
    ops.node(165, 10, 15, 30)
    ops.node(166, 15, 15, 30)
    ops.node(167, 20, 15, 30)
    ops.node(168, 25, 15, 30)
    ops.node(169, 0, 0, 35)
    ops.node(170, 5, 0, 35)
    ops.node(171, 10, 0, 35)
    ops.node(172, 15, 0, 35)
    ops.node(173, 20, 0, 35)
    ops.node(174, 25, 0, 35)
    ops.node(175, 0, 5, 35)
    ops.node(176, 5, 5, 35)
    ops.node(177, 10, 5, 35)
    ops.node(178, 15, 5, 35)
    ops.node(179, 20, 5, 35)
    ops.node(180, 25, 5, 35)
    ops.node(181, 0, 10, 35)
    ops.node(182, 5, 10, 35)
    ops.node(183, 10, 10, 35)
    ops.node(184, 15, 10, 35)
    ops.node(185, 20, 10, 35)
    ops.node(186, 25, 10, 35)
    ops.node(187, 0, 15, 35)
    ops.node(188, 5, 15, 35)
    ops.node(189, 10, 15, 35)
    ops.node(190, 15, 15, 35)
    ops.node(191, 20, 15, 35)
    ops.node(192, 25, 15, 35)
    ops.node(193, 0, 0, 40)
    ops.node(194, 5, 0, 40)
    ops.node(195, 10, 0, 40)
    ops.node(196, 15, 0, 40)
    ops.node(197, 20, 0, 40)
    ops.node(198, 25, 0, 40)
    ops.node(199, 0, 5, 40)
    ops.node(200, 5, 5, 40)
    ops.node(201, 10, 5, 40)
    ops.node(202, 15, 5, 40)
    ops.node(203, 20, 5, 40)
    ops.node(204, 25, 5, 40)
    ops.node(205, 0, 10, 40)
    ops.node(206, 5, 10, 40)
    ops.node(207, 10, 10, 40)
    ops.node(208, 15, 10, 40)
    ops.node(209, 20, 10, 40)
    ops.node(210, 25, 10, 40)
    ops.node(211, 0, 15, 40)
    ops.node(212, 5, 15, 40)
    ops.node(213, 10, 15, 40)
    ops.node(214, 15, 15, 40)
    ops.node(215, 20, 15, 40)
    ops.node(216, 25, 15, 40)
    ops.node(217, 0, 0, 45)
    ops.node(218, 5, 0, 45)
    ops.node(219, 10, 0, 45)
    ops.node(220, 15, 0, 45)
    ops.node(221, 20, 0, 45)
    ops.node(222, 25, 0, 45)
    ops.node(223, 0, 5, 45)
    ops.node(224, 5, 5, 45)
    ops.node(225, 10, 5, 45)
    ops.node(226, 15, 5, 45)
    ops.node(227, 20, 5, 45)
    ops.node(228, 25, 5, 45)
    ops.node(229, 0, 10, 45)
    ops.node(230, 5, 10, 45)
    ops.node(231, 10, 10, 45)
    ops.node(232, 15, 10, 45)
    ops.node(233, 20, 10, 45)
    ops.node(234, 25, 10, 45)
    ops.node(235, 0, 15, 45)
    ops.node(236, 5, 15, 45)
    ops.node(237, 10, 15, 45)
    ops.node(238, 15, 15, 45)
    ops.node(239, 20, 15, 45)
    ops.node(240, 25, 15, 45)
    ops.node(241, 0, 0, 50)
    ops.node(242, 5, 0, 50)
    ops.node(243, 10, 0, 50)
    ops.node(244, 15, 0, 50)
    ops.node(245, 20, 0, 50)
    ops.node(246, 25, 0, 50)
    ops.node(247, 0, 5, 50)
    ops.node(248, 5, 5, 50)
    ops.node(249, 10, 5, 50)
    ops.node(250, 15, 5, 50)
    ops.node(251, 20, 5, 50)
    ops.node(252, 25, 5, 50)
    ops.node(253, 0, 10, 50)
    ops.node(254, 5, 10, 50)
    ops.node(255, 10, 10, 50)
    ops.node(256, 15, 10, 50)
    ops.node(257, 20, 10, 50)
    ops.node(258, 25, 10, 50)
    ops.node(259, 0, 15, 50)
    ops.node(260, 5, 15, 50)
    ops.node(261, 10, 15, 50)
    ops.node(262, 15, 15, 50)
    ops.node(263, 20, 15, 50)
    ops.node(264, 25, 15, 50)
    ops.node(265, 0, 0, 55)
    ops.node(266, 5, 0, 55)
    ops.node(267, 10, 0, 55)
    ops.node(268, 15, 0, 55)
    ops.node(269, 20, 0, 55)
    ops.node(270, 25, 0, 55)
    ops.node(271, 0, 5, 55)
    ops.node(272, 5, 5, 55)
    ops.node(273, 10, 5, 55)
    ops.node(274, 15, 5, 55)
    ops.node(275, 20, 5, 55)
    ops.node(276, 25, 5, 55)
    ops.node(277, 0, 10, 55)
    ops.node(278, 5, 10, 55)
    ops.node(279, 10, 10, 55)
    ops.node(280, 15, 10, 55)
    ops.node(281, 20, 10, 55)
    ops.node(282, 25, 10, 55)
    ops.node(283, 0, 15, 55)
    ops.node(284, 5, 15, 55)
    ops.node(285, 10, 15, 55)
    ops.node(286, 15, 15, 55)
    ops.node(287, 20, 15, 55)
    ops.node(288, 25, 15, 55)
    ops.node(289, 0, 0, 60)
    ops.node(290, 5, 0, 60)
    ops.node(291, 10, 0, 60)
    ops.node(292, 15, 0, 60)
    ops.node(293, 20, 0, 60)
    ops.node(294, 25, 0, 60)
    ops.node(295, 0, 5, 60)
    ops.node(296, 5, 5, 60)
    ops.node(297, 10, 5, 60)
    ops.node(298, 15, 5, 60)
    ops.node(299, 20, 5, 60)
    ops.node(300, 25, 5, 60)
    ops.node(301, 0, 10, 60)
    ops.node(302, 5, 10, 60)
    ops.node(303, 10, 10, 60)
    ops.node(304, 15, 10, 60)
    ops.node(305, 20, 10, 60)
    ops.node(306, 25, 10, 60)
    ops.node(307, 0, 15, 60)
    ops.node(308, 5, 15, 60)
    ops.node(309, 10, 15, 60)
    ops.node(310, 15, 15, 60)
    ops.node(311, 20, 15, 60)
    ops.node(312, 25, 15, 60)
    ops.node(313, 0, 0, 65)
    ops.node(314, 5, 0, 65)
    ops.node(315, 10, 0, 65)
    ops.node(316, 15, 0, 65)
    ops.node(317, 20, 0, 65)
    ops.node(318, 25, 0, 65)
    ops.node(319, 0, 5, 65)
    ops.node(320, 5, 5, 65)
    ops.node(321, 10, 5, 65)
    ops.node(322, 15, 5, 65)
    ops.node(323, 20, 5, 65)
    ops.node(324, 25, 5, 65)
    ops.node(325, 0, 10, 65)
    ops.node(326, 5, 10, 65)
    ops.node(327, 10, 10, 65)
    ops.node(328, 15, 10, 65)
    ops.node(329, 20, 10, 65)
    ops.node(330, 25, 10, 65)
    ops.node(331, 0, 15, 65)
    ops.node(332, 5, 15, 65)
    ops.node(333, 10, 15, 65)
    ops.node(334, 15, 15, 65)
    ops.node(335, 20, 15, 65)
    ops.node(336, 25, 15, 65)
    ops.node(337, 0, 0, 70)
    ops.node(338, 5, 0, 70)
    ops.node(339, 10, 0, 70)
    ops.node(340, 15, 0, 70)
    ops.node(341, 20, 0, 70)
    ops.node(342, 25, 0, 70)
    ops.node(343, 0, 5, 70)
    ops.node(344, 5, 5, 70)
    ops.node(345, 10, 5, 70)
    ops.node(346, 15, 5, 70)
    ops.node(347, 20, 5, 70)
    ops.node(348, 25, 5, 70)
    ops.node(349, 0, 10, 70)
    ops.node(350, 5, 10, 70)
    ops.node(351, 10, 10, 70)
    ops.node(352, 15, 10, 70)
    ops.node(353, 20, 10, 70)
    ops.node(354, 25, 10, 70)
    ops.node(355, 0, 15, 70)
    ops.node(356, 5, 15, 70)
    ops.node(357, 10, 15, 70)
    ops.node(358, 15, 15, 70)
    ops.node(359, 20, 15, 70)
    ops.node(360, 25, 15, 70)
    ops.node(361, 0, 0, 75)
    ops.node(362, 5, 0, 75)
    ops.node(363, 10, 0, 75)
    ops.node(364, 15, 0, 75)
    ops.node(365, 20, 0, 75)
    ops.node(366, 25, 0, 75)
    ops.node(367, 0, 5, 75)
    ops.node(368, 5, 5, 75)
    ops.node(369, 10, 5, 75)
    ops.node(370, 15, 5, 75)
    ops.node(371, 20, 5, 75)
    ops.node(372, 25, 5, 75)
    ops.node(373, 0, 10, 75)
    ops.node(374, 5, 10, 75)
    ops.node(375, 10, 10, 75)
    ops.node(376, 15, 10, 75)
    ops.node(377, 20, 10, 75)
    ops.node(378, 25, 10, 75)
    ops.node(379, 0, 15, 75)
    ops.node(380, 5, 15, 75)
    ops.node(381, 10, 15, 75)
    ops.node(382, 15, 15, 75)
    ops.node(383, 20, 15, 75)
    ops.node(384, 25, 15, 75)

    # Create OpenSees elastic elements.
    ops.geomTransf('Linear', 1, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 6, *[7, 8], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 1)
    ops.geomTransf('Linear', 2, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 7, *[8, 9], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 2)
    ops.geomTransf('Linear', 3, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 8, *[9, 10], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 3)
    ops.geomTransf('Linear', 4, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 9, *[10, 11], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 4)
    ops.geomTransf('Linear', 5, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 10, *[11, 12], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 5)
    ops.geomTransf('Linear', 6, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 11, *[13, 14], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 6)
    ops.geomTransf('Linear', 7, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 12, *[14, 15], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 7)
    ops.geomTransf('Linear', 8, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 13, *[15, 16], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 8)
    ops.geomTransf('Linear', 9, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 14, *[16, 17], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 9)
    ops.geomTransf('Linear', 10, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 15, *[17, 18], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 10)
    ops.geomTransf('Linear', 11, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 16, *[19, 20], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 11)
    ops.geomTransf('Linear', 12, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 17, *[20, 21], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 12)
    ops.geomTransf('Linear', 13, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 18, *[21, 22], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 13)
    ops.geomTransf('Linear', 14, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 19, *[22, 23], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 14)
    ops.geomTransf('Linear', 15, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 20, *[23, 24], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 15)
    ops.geomTransf('Linear', 16, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 21, *[25, 26], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 16)
    ops.geomTransf('Linear', 17, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 22, *[26, 27], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 17)
    ops.geomTransf('Linear', 18, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 23, *[27, 28], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 18)
    ops.geomTransf('Linear', 19, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 24, *[28, 29], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 19)
    ops.geomTransf('Linear', 20, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 25, *[29, 30], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 20)
    ops.geomTransf('Linear', 21, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 26, *[31, 32], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 21)
    ops.geomTransf('Linear', 22, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 27, *[32, 33], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 22)
    ops.geomTransf('Linear', 23, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 28, *[33, 34], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 23)
    ops.geomTransf('Linear', 24, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 29, *[34, 35], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 24)
    ops.geomTransf('Linear', 25, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 30, *[35, 36], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 25)
    ops.geomTransf('Linear', 26, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 31, *[1, 7], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 26)
    ops.geomTransf('Linear', 27, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 32, *[7, 13], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 27)
    ops.geomTransf('Linear', 28, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 33, *[13, 19], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 28)
    ops.geomTransf('Linear', 29, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 34, *[19, 25], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 29)
    ops.geomTransf('Linear', 30, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 35, *[25, 31], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 30)
    ops.geomTransf('Linear', 31, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 36, *[2, 8], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 31)
    ops.geomTransf('Linear', 32, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 37, *[8, 14], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 32)
    ops.geomTransf('Linear', 33, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 38, *[14, 20], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 33)
    ops.geomTransf('Linear', 34, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 39, *[20, 26], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 34)
    ops.geomTransf('Linear', 35, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 40, *[26, 32], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 35)
    ops.geomTransf('Linear', 36, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 41, *[3, 9], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 36)
    ops.geomTransf('Linear', 37, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 42, *[9, 15], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 37)
    ops.geomTransf('Linear', 38, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 43, *[15, 21], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 38)
    ops.geomTransf('Linear', 39, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 44, *[21, 27], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 39)
    ops.geomTransf('Linear', 40, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 45, *[27, 33], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 40)
    ops.geomTransf('Linear', 41, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 46, *[4, 10], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 41)
    ops.geomTransf('Linear', 42, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 47, *[10, 16], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 42)
    ops.geomTransf('Linear', 43, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 48, *[16, 22], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 43)
    ops.geomTransf('Linear', 44, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 49, *[22, 28], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 44)
    ops.geomTransf('Linear', 45, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 50, *[28, 34], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 45)
    ops.geomTransf('Linear', 46, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 51, *[5, 11], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 46)
    ops.geomTransf('Linear', 47, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 52, *[11, 17], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 47)
    ops.geomTransf('Linear', 48, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 53, *[17, 23], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 48)
    ops.geomTransf('Linear', 49, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 54, *[23, 29], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 49)
    ops.geomTransf('Linear', 50, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 55, *[29, 35], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 50)
    ops.geomTransf('Linear', 51, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 56, *[6, 12], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 51)
    ops.geomTransf('Linear', 52, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 57, *[12, 18], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 52)
    ops.geomTransf('Linear', 53, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 58, *[18, 24], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 53)
    ops.geomTransf('Linear', 54, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 59, *[24, 30], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 54)
    ops.geomTransf('Linear', 55, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 60, *[30, 36], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 55)
    ops.geomTransf('Linear', 56, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 66, *[43, 44], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 56)
    ops.geomTransf('Linear', 57, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 67, *[44, 45], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 57)
    ops.geomTransf('Linear', 58, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 68, *[45, 46], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 58)
    ops.geomTransf('Linear', 59, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 69, *[46, 47], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 59)
    ops.geomTransf('Linear', 60, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 70, *[47, 48], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 60)
    ops.geomTransf('Linear', 61, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 71, *[49, 50], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 61)
    ops.geomTransf('Linear', 62, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 72, *[50, 51], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 62)
    ops.geomTransf('Linear', 63, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 73, *[51, 52], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 63)
    ops.geomTransf('Linear', 64, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 74, *[52, 53], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 64)
    ops.geomTransf('Linear', 65, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 75, *[53, 54], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 65)
    ops.geomTransf('Linear', 66, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 76, *[55, 56], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 66)
    ops.geomTransf('Linear', 67, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 77, *[56, 57], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 67)
    ops.geomTransf('Linear', 68, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 78, *[57, 58], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 68)
    ops.geomTransf('Linear', 69, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 79, *[58, 59], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 69)
    ops.geomTransf('Linear', 70, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 80, *[59, 60], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 70)
    ops.geomTransf('Linear', 71, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 81, *[61, 62], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 71)
    ops.geomTransf('Linear', 72, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 82, *[62, 63], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 72)
    ops.geomTransf('Linear', 73, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 83, *[63, 64], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 73)
    ops.geomTransf('Linear', 74, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 84, *[64, 65], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 74)
    ops.geomTransf('Linear', 75, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 85, *[65, 66], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 75)
    ops.geomTransf('Linear', 76, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 86, *[67, 68], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 76)
    ops.geomTransf('Linear', 77, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 87, *[68, 69], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 77)
    ops.geomTransf('Linear', 78, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 88, *[69, 70], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 78)
    ops.geomTransf('Linear', 79, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 89, *[70, 71], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 79)
    ops.geomTransf('Linear', 80, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 90, *[71, 72], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 80)
    ops.geomTransf('Linear', 81, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 91, *[37, 43], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 81)
    ops.geomTransf('Linear', 82, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 92, *[43, 49], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 82)
    ops.geomTransf('Linear', 83, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 93, *[49, 55], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 83)
    ops.geomTransf('Linear', 84, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 94, *[55, 61], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 84)
    ops.geomTransf('Linear', 85, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 95, *[61, 67], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 85)
    ops.geomTransf('Linear', 86, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 96, *[38, 44], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 86)
    ops.geomTransf('Linear', 87, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 97, *[44, 50], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 87)
    ops.geomTransf('Linear', 88, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 98, *[50, 56], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 88)
    ops.geomTransf('Linear', 89, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 99, *[56, 62], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 89)
    ops.geomTransf('Linear', 90, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 100, *[62, 68], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 90)
    ops.geomTransf('Linear', 91, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 101, *[39, 45], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 91)
    ops.geomTransf('Linear', 92, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 102, *[45, 51], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 92)
    ops.geomTransf('Linear', 93, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 103, *[51, 57], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 93)
    ops.geomTransf('Linear', 94, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 104, *[57, 63], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 94)
    ops.geomTransf('Linear', 95, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 105, *[63, 69], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 95)
    ops.geomTransf('Linear', 96, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 106, *[40, 46], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 96)
    ops.geomTransf('Linear', 97, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 107, *[46, 52], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 97)
    ops.geomTransf('Linear', 98, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 108, *[52, 58], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 98)
    ops.geomTransf('Linear', 99, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 109, *[58, 64], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 99)
    ops.geomTransf('Linear', 100, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 110, *[64, 70], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 100)
    ops.geomTransf('Linear', 101, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 111, *[41, 47], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 101)
    ops.geomTransf('Linear', 102, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 112, *[47, 53], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 102)
    ops.geomTransf('Linear', 103, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 113, *[53, 59], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 103)
    ops.geomTransf('Linear', 104, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 114, *[59, 65], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 104)
    ops.geomTransf('Linear', 105, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 115, *[65, 71], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 105)
    ops.geomTransf('Linear', 106, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 116, *[42, 48], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 106)
    ops.geomTransf('Linear', 107, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 117, *[48, 54], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 107)
    ops.geomTransf('Linear', 108, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 118, *[54, 60], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 108)
    ops.geomTransf('Linear', 109, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 119, *[60, 66], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 109)
    ops.geomTransf('Linear', 110, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 120, *[66, 72], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 110)
    ops.geomTransf('Linear', 111, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 126, *[79, 80], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 111)
    ops.geomTransf('Linear', 112, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 127, *[80, 81], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 112)
    ops.geomTransf('Linear', 113, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 128, *[81, 82], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 113)
    ops.geomTransf('Linear', 114, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 129, *[82, 83], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 114)
    ops.geomTransf('Linear', 115, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 130, *[83, 84], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 115)
    ops.geomTransf('Linear', 116, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 131, *[85, 86], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 116)
    ops.geomTransf('Linear', 117, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 132, *[86, 87], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 117)
    ops.geomTransf('Linear', 118, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 133, *[87, 88], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 118)
    ops.geomTransf('Linear', 119, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 134, *[88, 89], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 119)
    ops.geomTransf('Linear', 120, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 135, *[89, 90], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 120)
    ops.geomTransf('Linear', 121, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 136, *[91, 92], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 121)
    ops.geomTransf('Linear', 122, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 137, *[92, 93], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 122)
    ops.geomTransf('Linear', 123, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 138, *[93, 94], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 123)
    ops.geomTransf('Linear', 124, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 139, *[94, 95], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 124)
    ops.geomTransf('Linear', 125, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 140, *[95, 96], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 125)
    ops.geomTransf('Linear', 126, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 141, *[97, 98], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 126)
    ops.geomTransf('Linear', 127, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 142, *[98, 99], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 127)
    ops.geomTransf('Linear', 128, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 143, *[99, 100], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 128)
    ops.geomTransf('Linear', 129, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 144, *[100, 101], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 129)
    ops.geomTransf('Linear', 130, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 145, *[101, 102], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 130)
    ops.geomTransf('Linear', 131, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 146, *[103, 104], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 131)
    ops.geomTransf('Linear', 132, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 147, *[104, 105], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 132)
    ops.geomTransf('Linear', 133, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 148, *[105, 106], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 133)
    ops.geomTransf('Linear', 134, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 149, *[106, 107], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 134)
    ops.geomTransf('Linear', 135, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 150, *[107, 108], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 135)
    ops.geomTransf('Linear', 136, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 151, *[73, 79], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 136)
    ops.geomTransf('Linear', 137, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 152, *[79, 85], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 137)
    ops.geomTransf('Linear', 138, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 153, *[85, 91], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 138)
    ops.geomTransf('Linear', 139, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 154, *[91, 97], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 139)
    ops.geomTransf('Linear', 140, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 155, *[97, 103], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 140)
    ops.geomTransf('Linear', 141, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 156, *[74, 80], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 141)
    ops.geomTransf('Linear', 142, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 157, *[80, 86], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 142)
    ops.geomTransf('Linear', 143, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 158, *[86, 92], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 143)
    ops.geomTransf('Linear', 144, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 159, *[92, 98], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 144)
    ops.geomTransf('Linear', 145, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 160, *[98, 104], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 145)
    ops.geomTransf('Linear', 146, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 161, *[75, 81], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 146)
    ops.geomTransf('Linear', 147, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 162, *[81, 87], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 147)
    ops.geomTransf('Linear', 148, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 163, *[87, 93], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 148)
    ops.geomTransf('Linear', 149, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 164, *[93, 99], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 149)
    ops.geomTransf('Linear', 150, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 165, *[99, 105], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 150)
    ops.geomTransf('Linear', 151, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 166, *[76, 82], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 151)
    ops.geomTransf('Linear', 152, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 167, *[82, 88], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 152)
    ops.geomTransf('Linear', 153, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 168, *[88, 94], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 153)
    ops.geomTransf('Linear', 154, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 169, *[94, 100], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 154)
    ops.geomTransf('Linear', 155, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 170, *[100, 106], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 155)
    ops.geomTransf('Linear', 156, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 171, *[77, 83], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 156)
    ops.geomTransf('Linear', 157, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 172, *[83, 89], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 157)
    ops.geomTransf('Linear', 158, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 173, *[89, 95], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 158)
    ops.geomTransf('Linear', 159, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 174, *[95, 101], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 159)
    ops.geomTransf('Linear', 160, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 175, *[101, 107], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 160)
    ops.geomTransf('Linear', 161, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 176, *[78, 84], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 161)
    ops.geomTransf('Linear', 162, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 177, *[84, 90], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 162)
    ops.geomTransf('Linear', 163, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 178, *[90, 96], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 163)
    ops.geomTransf('Linear', 164, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 179, *[96, 102], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 164)
    ops.geomTransf('Linear', 165, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 180, *[102, 108], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 165)
    ops.geomTransf('Linear', 166, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 186, *[115, 116], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 166)
    ops.geomTransf('Linear', 167, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 187, *[116, 117], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 167)
    ops.geomTransf('Linear', 168, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 188, *[117, 118], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 168)
    ops.geomTransf('Linear', 169, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 189, *[118, 119], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 169)
    ops.geomTransf('Linear', 170, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 190, *[119, 120], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 170)
    ops.geomTransf('Linear', 171, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 191, *[121, 122], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 171)
    ops.geomTransf('Linear', 172, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 192, *[122, 123], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 172)
    ops.geomTransf('Linear', 173, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 193, *[123, 124], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 173)
    ops.geomTransf('Linear', 174, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 194, *[124, 125], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 174)
    ops.geomTransf('Linear', 175, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 195, *[125, 126], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 175)
    ops.geomTransf('Linear', 176, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 196, *[127, 128], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 176)
    ops.geomTransf('Linear', 177, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 197, *[128, 129], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 177)
    ops.geomTransf('Linear', 178, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 198, *[129, 130], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 178)
    ops.geomTransf('Linear', 179, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 199, *[130, 131], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 179)
    ops.geomTransf('Linear', 180, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 200, *[131, 132], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 180)
    ops.geomTransf('Linear', 181, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 201, *[133, 134], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 181)
    ops.geomTransf('Linear', 182, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 202, *[134, 135], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 182)
    ops.geomTransf('Linear', 183, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 203, *[135, 136], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 183)
    ops.geomTransf('Linear', 184, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 204, *[136, 137], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 184)
    ops.geomTransf('Linear', 185, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 205, *[137, 138], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 185)
    ops.geomTransf('Linear', 186, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 206, *[139, 140], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 186)
    ops.geomTransf('Linear', 187, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 207, *[140, 141], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 187)
    ops.geomTransf('Linear', 188, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 208, *[141, 142], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 188)
    ops.geomTransf('Linear', 189, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 209, *[142, 143], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 189)
    ops.geomTransf('Linear', 190, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 210, *[143, 144], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 190)
    ops.geomTransf('Linear', 191, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 211, *[109, 115], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 191)
    ops.geomTransf('Linear', 192, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 212, *[115, 121], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 192)
    ops.geomTransf('Linear', 193, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 213, *[121, 127], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 193)
    ops.geomTransf('Linear', 194, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 214, *[127, 133], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 194)
    ops.geomTransf('Linear', 195, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 215, *[133, 139], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 195)
    ops.geomTransf('Linear', 196, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 216, *[110, 116], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 196)
    ops.geomTransf('Linear', 197, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 217, *[116, 122], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 197)
    ops.geomTransf('Linear', 198, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 218, *[122, 128], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 198)
    ops.geomTransf('Linear', 199, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 219, *[128, 134], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 199)
    ops.geomTransf('Linear', 200, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 220, *[134, 140], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 200)
    ops.geomTransf('Linear', 201, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 221, *[111, 117], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 201)
    ops.geomTransf('Linear', 202, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 222, *[117, 123], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 202)
    ops.geomTransf('Linear', 203, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 223, *[123, 129], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 203)
    ops.geomTransf('Linear', 204, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 224, *[129, 135], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 204)
    ops.geomTransf('Linear', 205, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 225, *[135, 141], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 205)
    ops.geomTransf('Linear', 206, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 226, *[112, 118], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 206)
    ops.geomTransf('Linear', 207, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 227, *[118, 124], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 207)
    ops.geomTransf('Linear', 208, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 228, *[124, 130], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 208)
    ops.geomTransf('Linear', 209, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 229, *[130, 136], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 209)
    ops.geomTransf('Linear', 210, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 230, *[136, 142], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 210)
    ops.geomTransf('Linear', 211, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 231, *[113, 119], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 211)
    ops.geomTransf('Linear', 212, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 232, *[119, 125], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 212)
    ops.geomTransf('Linear', 213, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 233, *[125, 131], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 213)
    ops.geomTransf('Linear', 214, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 234, *[131, 137], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 214)
    ops.geomTransf('Linear', 215, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 235, *[137, 143], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 215)
    ops.geomTransf('Linear', 216, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 236, *[114, 120], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 216)
    ops.geomTransf('Linear', 217, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 237, *[120, 126], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 217)
    ops.geomTransf('Linear', 218, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 238, *[126, 132], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 218)
    ops.geomTransf('Linear', 219, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 239, *[132, 138], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 219)
    ops.geomTransf('Linear', 220, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 240, *[138, 144], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 220)
    ops.geomTransf('Linear', 221, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 241, *[144, 108], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 221)
    ops.geomTransf('Linear', 222, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 242, *[108, 72], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 222)
    ops.geomTransf('Linear', 223, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 243, *[72, 36], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 223)
    ops.geomTransf('Linear', 224, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 244, *[143, 107], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 224)
    ops.geomTransf('Linear', 225, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 245, *[107, 71], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 225)
    ops.geomTransf('Linear', 226, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 246, *[71, 35], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 226)
    ops.geomTransf('Linear', 227, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 247, *[142, 106], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 227)
    ops.geomTransf('Linear', 228, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 248, *[106, 70], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 228)
    ops.geomTransf('Linear', 229, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 249, *[70, 34], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 229)
    ops.geomTransf('Linear', 230, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 250, *[141, 105], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 230)
    ops.geomTransf('Linear', 231, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 251, *[105, 69], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 231)
    ops.geomTransf('Linear', 232, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 252, *[69, 33], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 232)
    ops.geomTransf('Linear', 233, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 253, *[140, 104], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 233)
    ops.geomTransf('Linear', 234, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 254, *[104, 68], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 234)
    ops.geomTransf('Linear', 235, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 255, *[68, 32], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 235)
    ops.geomTransf('Linear', 236, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 256, *[139, 103], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 236)
    ops.geomTransf('Linear', 237, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 257, *[103, 67], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 237)
    ops.geomTransf('Linear', 238, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 258, *[67, 31], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 238)
    ops.geomTransf('Linear', 239, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 259, *[138, 102], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 239)
    ops.geomTransf('Linear', 240, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 260, *[102, 66], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 240)
    ops.geomTransf('Linear', 241, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 261, *[66, 30], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 241)
    ops.geomTransf('Linear', 242, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 262, *[137, 101], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 242)
    ops.geomTransf('Linear', 243, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 263, *[101, 65], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 243)
    ops.geomTransf('Linear', 244, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 264, *[65, 29], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 244)
    ops.geomTransf('Linear', 245, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 265, *[136, 100], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 245)
    ops.geomTransf('Linear', 246, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 266, *[100, 64], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 246)
    ops.geomTransf('Linear', 247, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 267, *[64, 28], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 247)
    ops.geomTransf('Linear', 248, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 268, *[135, 99], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 248)
    ops.geomTransf('Linear', 249, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 269, *[99, 63], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 249)
    ops.geomTransf('Linear', 250, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 270, *[63, 27], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 250)
    ops.geomTransf('Linear', 251, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 271, *[134, 98], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 251)
    ops.geomTransf('Linear', 252, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 272, *[98, 62], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 252)
    ops.geomTransf('Linear', 253, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 273, *[62, 26], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 253)
    ops.geomTransf('Linear', 254, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 274, *[133, 97], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 254)
    ops.geomTransf('Linear', 255, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 275, *[97, 61], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 255)
    ops.geomTransf('Linear', 256, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 276, *[61, 25], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 256)
    ops.geomTransf('Linear', 257, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 277, *[132, 96], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 257)
    ops.geomTransf('Linear', 258, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 278, *[96, 60], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 258)
    ops.geomTransf('Linear', 259, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 279, *[60, 24], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 259)
    ops.geomTransf('Linear', 260, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 280, *[131, 95], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 260)
    ops.geomTransf('Linear', 261, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 281, *[95, 59], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 261)
    ops.geomTransf('Linear', 262, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 282, *[59, 23], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 262)
    ops.geomTransf('Linear', 263, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 283, *[130, 94], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 263)
    ops.geomTransf('Linear', 264, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 284, *[94, 58], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 264)
    ops.geomTransf('Linear', 265, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 285, *[58, 22], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 265)
    ops.geomTransf('Linear', 266, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 286, *[129, 93], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 266)
    ops.geomTransf('Linear', 267, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 287, *[93, 57], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 267)
    ops.geomTransf('Linear', 268, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 288, *[57, 21], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 268)
    ops.geomTransf('Linear', 269, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 289, *[128, 92], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 269)
    ops.geomTransf('Linear', 270, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 290, *[92, 56], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 270)
    ops.geomTransf('Linear', 271, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 291, *[56, 20], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 271)
    ops.geomTransf('Linear', 272, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 292, *[127, 91], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 272)
    ops.geomTransf('Linear', 273, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 293, *[91, 55], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 273)
    ops.geomTransf('Linear', 274, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 294, *[55, 19], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 274)
    ops.geomTransf('Linear', 275, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 295, *[126, 90], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 275)
    ops.geomTransf('Linear', 276, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 296, *[90, 54], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 276)
    ops.geomTransf('Linear', 277, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 297, *[54, 18], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 277)
    ops.geomTransf('Linear', 278, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 298, *[125, 89], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 278)
    ops.geomTransf('Linear', 279, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 299, *[89, 53], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 279)
    ops.geomTransf('Linear', 280, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 300, *[53, 17], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 280)
    ops.geomTransf('Linear', 281, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 301, *[124, 88], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 281)
    ops.geomTransf('Linear', 282, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 302, *[88, 52], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 282)
    ops.geomTransf('Linear', 283, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 303, *[52, 16], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 283)
    ops.geomTransf('Linear', 284, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 304, *[123, 87], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 284)
    ops.geomTransf('Linear', 285, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 305, *[87, 51], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 285)
    ops.geomTransf('Linear', 286, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 306, *[51, 15], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 286)
    ops.geomTransf('Linear', 287, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 307, *[122, 86], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 287)
    ops.geomTransf('Linear', 288, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 308, *[86, 50], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 288)
    ops.geomTransf('Linear', 289, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 309, *[50, 14], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 289)
    ops.geomTransf('Linear', 290, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 310, *[121, 85], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 290)
    ops.geomTransf('Linear', 291, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 311, *[85, 49], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 291)
    ops.geomTransf('Linear', 292, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 312, *[49, 13], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 292)
    ops.geomTransf('Linear', 293, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 313, *[120, 84], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 293)
    ops.geomTransf('Linear', 294, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 314, *[84, 48], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 294)
    ops.geomTransf('Linear', 295, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 315, *[48, 12], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 295)
    ops.geomTransf('Linear', 296, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 316, *[119, 83], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 296)
    ops.geomTransf('Linear', 297, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 317, *[83, 47], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 297)
    ops.geomTransf('Linear', 298, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 318, *[47, 11], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 298)
    ops.geomTransf('Linear', 299, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 319, *[118, 82], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 299)
    ops.geomTransf('Linear', 300, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 320, *[82, 46], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 300)
    ops.geomTransf('Linear', 301, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 321, *[46, 10], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 301)
    ops.geomTransf('Linear', 302, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 322, *[117, 81], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 302)
    ops.geomTransf('Linear', 303, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 323, *[81, 45], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 303)
    ops.geomTransf('Linear', 304, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 324, *[45, 9], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 304)
    ops.geomTransf('Linear', 305, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 325, *[116, 80], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 305)
    ops.geomTransf('Linear', 306, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 326, *[80, 44], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 306)
    ops.geomTransf('Linear', 307, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 327, *[44, 8], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 307)
    ops.geomTransf('Linear', 308, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 328, *[115, 79], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 308)
    ops.geomTransf('Linear', 309, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 329, *[79, 43], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 309)
    ops.geomTransf('Linear', 310, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 330, *[43, 7], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 310)
    ops.geomTransf('Linear', 311, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 331, *[145, 146], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 311)
    ops.geomTransf('Linear', 312, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 332, *[146, 147], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 312)
    ops.geomTransf('Linear', 313, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 333, *[147, 148], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 313)
    ops.geomTransf('Linear', 314, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 334, *[148, 149], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 314)
    ops.geomTransf('Linear', 315, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 335, *[149, 150], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 315)
    ops.geomTransf('Linear', 316, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 336, *[31, 145], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 316)
    ops.geomTransf('Linear', 317, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 337, *[32, 146], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 317)
    ops.geomTransf('Linear', 318, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 338, *[33, 147], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 318)
    ops.geomTransf('Linear', 319, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 339, *[34, 148], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 319)
    ops.geomTransf('Linear', 320, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 340, *[35, 149], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 320)
    ops.geomTransf('Linear', 321, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 341, *[36, 150], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 321)
    ops.geomTransf('Linear', 322, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 342, *[151, 152], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 322)
    ops.geomTransf('Linear', 323, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 343, *[152, 153], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 323)
    ops.geomTransf('Linear', 324, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 344, *[153, 154], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 324)
    ops.geomTransf('Linear', 325, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 345, *[154, 155], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 325)
    ops.geomTransf('Linear', 326, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 346, *[155, 156], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 326)
    ops.geomTransf('Linear', 327, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 347, *[67, 151], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 327)
    ops.geomTransf('Linear', 328, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 348, *[68, 152], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 328)
    ops.geomTransf('Linear', 329, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 349, *[69, 153], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 329)
    ops.geomTransf('Linear', 330, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 350, *[70, 154], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 330)
    ops.geomTransf('Linear', 331, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 351, *[71, 155], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 331)
    ops.geomTransf('Linear', 332, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 352, *[72, 156], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 332)
    ops.geomTransf('Linear', 333, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 353, *[157, 158], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 333)
    ops.geomTransf('Linear', 334, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 354, *[158, 159], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 334)
    ops.geomTransf('Linear', 335, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 355, *[159, 160], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 335)
    ops.geomTransf('Linear', 336, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 356, *[160, 161], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 336)
    ops.geomTransf('Linear', 337, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 357, *[161, 162], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 337)
    ops.geomTransf('Linear', 338, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 358, *[103, 157], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 338)
    ops.geomTransf('Linear', 339, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 359, *[104, 158], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 339)
    ops.geomTransf('Linear', 340, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 360, *[105, 159], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 340)
    ops.geomTransf('Linear', 341, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 361, *[106, 160], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 341)
    ops.geomTransf('Linear', 342, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 362, *[107, 161], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 342)
    ops.geomTransf('Linear', 343, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 363, *[108, 162], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 343)
    ops.geomTransf('Linear', 344, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 364, *[163, 164], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 344)
    ops.geomTransf('Linear', 345, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 365, *[164, 165], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 345)
    ops.geomTransf('Linear', 346, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 366, *[165, 166], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 346)
    ops.geomTransf('Linear', 347, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 367, *[166, 167], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 347)
    ops.geomTransf('Linear', 348, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 368, *[167, 168], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 348)
    ops.geomTransf('Linear', 349, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 369, *[139, 163], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 349)
    ops.geomTransf('Linear', 350, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 370, *[140, 164], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 350)
    ops.geomTransf('Linear', 351, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 371, *[141, 165], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 351)
    ops.geomTransf('Linear', 352, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 372, *[142, 166], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 352)
    ops.geomTransf('Linear', 353, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 373, *[143, 167], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 353)
    ops.geomTransf('Linear', 354, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 374, *[144, 168], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 354)
    ops.geomTransf('Linear', 355, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 375, *[168, 162], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 355)
    ops.geomTransf('Linear', 356, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 376, *[162, 156], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 356)
    ops.geomTransf('Linear', 357, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 377, *[156, 150], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 357)
    ops.geomTransf('Linear', 358, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 378, *[167, 161], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 358)
    ops.geomTransf('Linear', 359, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 379, *[161, 155], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 359)
    ops.geomTransf('Linear', 360, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 380, *[155, 149], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 360)
    ops.geomTransf('Linear', 361, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 381, *[166, 160], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 361)
    ops.geomTransf('Linear', 362, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 382, *[160, 154], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 362)
    ops.geomTransf('Linear', 363, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 383, *[154, 148], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 363)
    ops.geomTransf('Linear', 364, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 384, *[165, 159], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 364)
    ops.geomTransf('Linear', 365, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 385, *[159, 153], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 365)
    ops.geomTransf('Linear', 366, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 386, *[153, 147], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 366)
    ops.geomTransf('Linear', 367, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 387, *[164, 158], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 367)
    ops.geomTransf('Linear', 368, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 388, *[158, 152], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 368)
    ops.geomTransf('Linear', 369, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 389, *[152, 146], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 369)
    ops.geomTransf('Linear', 370, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 390, *[163, 157], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 370)
    ops.geomTransf('Linear', 371, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 391, *[157, 151], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 371)
    ops.geomTransf('Linear', 372, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 392, *[151, 145], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 372)
    ops.geomTransf('Linear', 373, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 393, *[169, 170], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 373)
    ops.geomTransf('Linear', 374, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 394, *[170, 171], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 374)
    ops.geomTransf('Linear', 375, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 395, *[171, 172], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 375)
    ops.geomTransf('Linear', 376, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 396, *[172, 173], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 376)
    ops.geomTransf('Linear', 377, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 397, *[173, 174], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 377)
    ops.geomTransf('Linear', 378, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 398, *[145, 169], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 378)
    ops.geomTransf('Linear', 379, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 399, *[146, 170], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 379)
    ops.geomTransf('Linear', 380, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 400, *[147, 171], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 380)
    ops.geomTransf('Linear', 381, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 401, *[148, 172], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 381)
    ops.geomTransf('Linear', 382, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 402, *[149, 173], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 382)
    ops.geomTransf('Linear', 383, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 403, *[150, 174], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 383)
    ops.geomTransf('Linear', 384, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 404, *[175, 176], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 384)
    ops.geomTransf('Linear', 385, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 405, *[176, 177], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 385)
    ops.geomTransf('Linear', 386, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 406, *[177, 178], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 386)
    ops.geomTransf('Linear', 387, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 407, *[178, 179], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 387)
    ops.geomTransf('Linear', 388, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 408, *[179, 180], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 388)
    ops.geomTransf('Linear', 389, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 409, *[151, 175], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 389)
    ops.geomTransf('Linear', 390, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 410, *[152, 176], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 390)
    ops.geomTransf('Linear', 391, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 411, *[153, 177], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 391)
    ops.geomTransf('Linear', 392, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 412, *[154, 178], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 392)
    ops.geomTransf('Linear', 393, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 413, *[155, 179], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 393)
    ops.geomTransf('Linear', 394, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 414, *[156, 180], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 394)
    ops.geomTransf('Linear', 395, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 415, *[181, 182], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 395)
    ops.geomTransf('Linear', 396, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 416, *[182, 183], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 396)
    ops.geomTransf('Linear', 397, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 417, *[183, 184], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 397)
    ops.geomTransf('Linear', 398, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 418, *[184, 185], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 398)
    ops.geomTransf('Linear', 399, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 419, *[185, 186], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 399)
    ops.geomTransf('Linear', 400, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 420, *[157, 181], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 400)
    ops.geomTransf('Linear', 401, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 421, *[158, 182], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 401)
    ops.geomTransf('Linear', 402, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 422, *[159, 183], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 402)
    ops.geomTransf('Linear', 403, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 423, *[160, 184], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 403)
    ops.geomTransf('Linear', 404, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 424, *[161, 185], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 404)
    ops.geomTransf('Linear', 405, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 425, *[162, 186], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 405)
    ops.geomTransf('Linear', 406, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 426, *[187, 188], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 406)
    ops.geomTransf('Linear', 407, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 427, *[188, 189], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 407)
    ops.geomTransf('Linear', 408, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 428, *[189, 190], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 408)
    ops.geomTransf('Linear', 409, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 429, *[190, 191], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 409)
    ops.geomTransf('Linear', 410, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 430, *[191, 192], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 410)
    ops.geomTransf('Linear', 411, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 431, *[163, 187], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 411)
    ops.geomTransf('Linear', 412, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 432, *[164, 188], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 412)
    ops.geomTransf('Linear', 413, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 433, *[165, 189], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 413)
    ops.geomTransf('Linear', 414, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 434, *[166, 190], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 414)
    ops.geomTransf('Linear', 415, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 435, *[167, 191], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 415)
    ops.geomTransf('Linear', 416, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 436, *[168, 192], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 416)
    ops.geomTransf('Linear', 417, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 437, *[192, 186], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 417)
    ops.geomTransf('Linear', 418, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 438, *[186, 180], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 418)
    ops.geomTransf('Linear', 419, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 439, *[180, 174], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 419)
    ops.geomTransf('Linear', 420, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 440, *[191, 185], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 420)
    ops.geomTransf('Linear', 421, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 441, *[185, 179], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 421)
    ops.geomTransf('Linear', 422, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 442, *[179, 173], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 422)
    ops.geomTransf('Linear', 423, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 443, *[190, 184], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 423)
    ops.geomTransf('Linear', 424, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 444, *[184, 178], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 424)
    ops.geomTransf('Linear', 425, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 445, *[178, 172], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 425)
    ops.geomTransf('Linear', 426, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 446, *[189, 183], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 426)
    ops.geomTransf('Linear', 427, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 447, *[183, 177], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 427)
    ops.geomTransf('Linear', 428, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 448, *[177, 171], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 428)
    ops.geomTransf('Linear', 429, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 449, *[188, 182], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 429)
    ops.geomTransf('Linear', 430, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 450, *[182, 176], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 430)
    ops.geomTransf('Linear', 431, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 451, *[176, 170], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 431)
    ops.geomTransf('Linear', 432, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 452, *[187, 181], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 432)
    ops.geomTransf('Linear', 433, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 453, *[181, 175], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 433)
    ops.geomTransf('Linear', 434, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 454, *[175, 169], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 434)
    ops.geomTransf('Linear', 435, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 455, *[193, 194], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 435)
    ops.geomTransf('Linear', 436, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 456, *[194, 195], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 436)
    ops.geomTransf('Linear', 437, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 457, *[195, 196], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 437)
    ops.geomTransf('Linear', 438, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 458, *[196, 197], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 438)
    ops.geomTransf('Linear', 439, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 459, *[197, 198], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 439)
    ops.geomTransf('Linear', 440, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 460, *[169, 193], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 440)
    ops.geomTransf('Linear', 441, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 461, *[170, 194], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 441)
    ops.geomTransf('Linear', 442, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 462, *[171, 195], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 442)
    ops.geomTransf('Linear', 443, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 463, *[172, 196], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 443)
    ops.geomTransf('Linear', 444, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 464, *[173, 197], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 444)
    ops.geomTransf('Linear', 445, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 465, *[174, 198], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 445)
    ops.geomTransf('Linear', 446, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 466, *[199, 200], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 446)
    ops.geomTransf('Linear', 447, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 467, *[200, 201], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 447)
    ops.geomTransf('Linear', 448, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 468, *[201, 202], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 448)
    ops.geomTransf('Linear', 449, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 469, *[202, 203], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 449)
    ops.geomTransf('Linear', 450, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 470, *[203, 204], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 450)
    ops.geomTransf('Linear', 451, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 471, *[175, 199], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 451)
    ops.geomTransf('Linear', 452, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 472, *[176, 200], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 452)
    ops.geomTransf('Linear', 453, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 473, *[177, 201], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 453)
    ops.geomTransf('Linear', 454, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 474, *[178, 202], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 454)
    ops.geomTransf('Linear', 455, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 475, *[179, 203], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 455)
    ops.geomTransf('Linear', 456, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 476, *[180, 204], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 456)
    ops.geomTransf('Linear', 457, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 477, *[205, 206], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 457)
    ops.geomTransf('Linear', 458, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 478, *[206, 207], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 458)
    ops.geomTransf('Linear', 459, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 479, *[207, 208], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 459)
    ops.geomTransf('Linear', 460, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 480, *[208, 209], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 460)
    ops.geomTransf('Linear', 461, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 481, *[209, 210], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 461)
    ops.geomTransf('Linear', 462, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 482, *[181, 205], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 462)
    ops.geomTransf('Linear', 463, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 483, *[182, 206], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 463)
    ops.geomTransf('Linear', 464, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 484, *[183, 207], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 464)
    ops.geomTransf('Linear', 465, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 485, *[184, 208], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 465)
    ops.geomTransf('Linear', 466, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 486, *[185, 209], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 466)
    ops.geomTransf('Linear', 467, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 487, *[186, 210], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 467)
    ops.geomTransf('Linear', 468, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 488, *[211, 212], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 468)
    ops.geomTransf('Linear', 469, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 489, *[212, 213], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 469)
    ops.geomTransf('Linear', 470, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 490, *[213, 214], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 470)
    ops.geomTransf('Linear', 471, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 491, *[214, 215], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 471)
    ops.geomTransf('Linear', 472, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 492, *[215, 216], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 472)
    ops.geomTransf('Linear', 473, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 493, *[187, 211], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 473)
    ops.geomTransf('Linear', 474, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 494, *[188, 212], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 474)
    ops.geomTransf('Linear', 475, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 495, *[189, 213], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 475)
    ops.geomTransf('Linear', 476, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 496, *[190, 214], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 476)
    ops.geomTransf('Linear', 477, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 497, *[191, 215], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 477)
    ops.geomTransf('Linear', 478, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 498, *[192, 216], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 478)
    ops.geomTransf('Linear', 479, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 499, *[216, 210], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 479)
    ops.geomTransf('Linear', 480, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 500, *[210, 204], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 480)
    ops.geomTransf('Linear', 481, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 501, *[204, 198], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 481)
    ops.geomTransf('Linear', 482, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 502, *[215, 209], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 482)
    ops.geomTransf('Linear', 483, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 503, *[209, 203], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 483)
    ops.geomTransf('Linear', 484, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 504, *[203, 197], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 484)
    ops.geomTransf('Linear', 485, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 505, *[214, 208], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 485)
    ops.geomTransf('Linear', 486, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 506, *[208, 202], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 486)
    ops.geomTransf('Linear', 487, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 507, *[202, 196], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 487)
    ops.geomTransf('Linear', 488, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 508, *[213, 207], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 488)
    ops.geomTransf('Linear', 489, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 509, *[207, 201], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 489)
    ops.geomTransf('Linear', 490, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 510, *[201, 195], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 490)
    ops.geomTransf('Linear', 491, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 511, *[212, 206], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 491)
    ops.geomTransf('Linear', 492, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 512, *[206, 200], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 492)
    ops.geomTransf('Linear', 493, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 513, *[200, 194], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 493)
    ops.geomTransf('Linear', 494, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 514, *[211, 205], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 494)
    ops.geomTransf('Linear', 495, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 515, *[205, 199], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 495)
    ops.geomTransf('Linear', 496, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 516, *[199, 193], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 496)
    ops.geomTransf('Linear', 497, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 517, *[217, 218], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 497)
    ops.geomTransf('Linear', 498, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 518, *[218, 219], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 498)
    ops.geomTransf('Linear', 499, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 519, *[219, 220], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 499)
    ops.geomTransf('Linear', 500, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 520, *[220, 221], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 500)
    ops.geomTransf('Linear', 501, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 521, *[221, 222], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 501)
    ops.geomTransf('Linear', 502, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 522, *[193, 217], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 502)
    ops.geomTransf('Linear', 503, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 523, *[194, 218], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 503)
    ops.geomTransf('Linear', 504, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 524, *[195, 219], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 504)
    ops.geomTransf('Linear', 505, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 525, *[196, 220], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 505)
    ops.geomTransf('Linear', 506, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 526, *[197, 221], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 506)
    ops.geomTransf('Linear', 507, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 527, *[198, 222], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 507)
    ops.geomTransf('Linear', 508, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 528, *[223, 224], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 508)
    ops.geomTransf('Linear', 509, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 529, *[224, 225], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 509)
    ops.geomTransf('Linear', 510, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 530, *[225, 226], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 510)
    ops.geomTransf('Linear', 511, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 531, *[226, 227], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 511)
    ops.geomTransf('Linear', 512, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 532, *[227, 228], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 512)
    ops.geomTransf('Linear', 513, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 533, *[199, 223], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 513)
    ops.geomTransf('Linear', 514, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 534, *[200, 224], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 514)
    ops.geomTransf('Linear', 515, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 535, *[201, 225], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 515)
    ops.geomTransf('Linear', 516, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 536, *[202, 226], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 516)
    ops.geomTransf('Linear', 517, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 537, *[203, 227], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 517)
    ops.geomTransf('Linear', 518, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 538, *[204, 228], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 518)
    ops.geomTransf('Linear', 519, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 539, *[229, 230], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 519)
    ops.geomTransf('Linear', 520, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 540, *[230, 231], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 520)
    ops.geomTransf('Linear', 521, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 541, *[231, 232], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 521)
    ops.geomTransf('Linear', 522, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 542, *[232, 233], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 522)
    ops.geomTransf('Linear', 523, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 543, *[233, 234], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 523)
    ops.geomTransf('Linear', 524, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 544, *[205, 229], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 524)
    ops.geomTransf('Linear', 525, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 545, *[206, 230], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 525)
    ops.geomTransf('Linear', 526, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 546, *[207, 231], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 526)
    ops.geomTransf('Linear', 527, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 547, *[208, 232], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 527)
    ops.geomTransf('Linear', 528, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 548, *[209, 233], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 528)
    ops.geomTransf('Linear', 529, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 549, *[210, 234], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 529)
    ops.geomTransf('Linear', 530, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 550, *[235, 236], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 530)
    ops.geomTransf('Linear', 531, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 551, *[236, 237], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 531)
    ops.geomTransf('Linear', 532, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 552, *[237, 238], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 532)
    ops.geomTransf('Linear', 533, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 553, *[238, 239], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 533)
    ops.geomTransf('Linear', 534, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 554, *[239, 240], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 534)
    ops.geomTransf('Linear', 535, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 555, *[211, 235], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 535)
    ops.geomTransf('Linear', 536, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 556, *[212, 236], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 536)
    ops.geomTransf('Linear', 537, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 557, *[213, 237], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 537)
    ops.geomTransf('Linear', 538, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 558, *[214, 238], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 538)
    ops.geomTransf('Linear', 539, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 559, *[215, 239], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 539)
    ops.geomTransf('Linear', 540, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 560, *[216, 240], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 540)
    ops.geomTransf('Linear', 541, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 561, *[240, 234], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 541)
    ops.geomTransf('Linear', 542, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 562, *[234, 228], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 542)
    ops.geomTransf('Linear', 543, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 563, *[228, 222], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 543)
    ops.geomTransf('Linear', 544, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 564, *[239, 233], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 544)
    ops.geomTransf('Linear', 545, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 565, *[233, 227], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 545)
    ops.geomTransf('Linear', 546, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 566, *[227, 221], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 546)
    ops.geomTransf('Linear', 547, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 567, *[238, 232], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 547)
    ops.geomTransf('Linear', 548, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 568, *[232, 226], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 548)
    ops.geomTransf('Linear', 549, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 569, *[226, 220], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 549)
    ops.geomTransf('Linear', 550, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 570, *[237, 231], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 550)
    ops.geomTransf('Linear', 551, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 571, *[231, 225], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 551)
    ops.geomTransf('Linear', 552, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 572, *[225, 219], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 552)
    ops.geomTransf('Linear', 553, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 573, *[236, 230], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 553)
    ops.geomTransf('Linear', 554, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 574, *[230, 224], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 554)
    ops.geomTransf('Linear', 555, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 575, *[224, 218], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 555)
    ops.geomTransf('Linear', 556, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 576, *[235, 229], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 556)
    ops.geomTransf('Linear', 557, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 577, *[229, 223], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 557)
    ops.geomTransf('Linear', 558, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 578, *[223, 217], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 558)
    ops.geomTransf('Linear', 559, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 579, *[241, 242], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 559)
    ops.geomTransf('Linear', 560, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 580, *[242, 243], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 560)
    ops.geomTransf('Linear', 561, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 581, *[243, 244], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 561)
    ops.geomTransf('Linear', 562, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 582, *[244, 245], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 562)
    ops.geomTransf('Linear', 563, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 583, *[245, 246], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 563)
    ops.geomTransf('Linear', 564, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 584, *[217, 241], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 564)
    ops.geomTransf('Linear', 565, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 585, *[218, 242], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 565)
    ops.geomTransf('Linear', 566, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 586, *[219, 243], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 566)
    ops.geomTransf('Linear', 567, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 587, *[220, 244], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 567)
    ops.geomTransf('Linear', 568, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 588, *[221, 245], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 568)
    ops.geomTransf('Linear', 569, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 589, *[222, 246], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 569)
    ops.geomTransf('Linear', 570, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 590, *[247, 248], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 570)
    ops.geomTransf('Linear', 571, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 591, *[248, 249], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 571)
    ops.geomTransf('Linear', 572, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 592, *[249, 250], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 572)
    ops.geomTransf('Linear', 573, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 593, *[250, 251], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 573)
    ops.geomTransf('Linear', 574, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 594, *[251, 252], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 574)
    ops.geomTransf('Linear', 575, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 595, *[223, 247], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 575)
    ops.geomTransf('Linear', 576, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 596, *[224, 248], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 576)
    ops.geomTransf('Linear', 577, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 597, *[225, 249], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 577)
    ops.geomTransf('Linear', 578, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 598, *[226, 250], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 578)
    ops.geomTransf('Linear', 579, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 599, *[227, 251], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 579)
    ops.geomTransf('Linear', 580, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 600, *[228, 252], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 580)
    ops.geomTransf('Linear', 581, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 601, *[253, 254], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 581)
    ops.geomTransf('Linear', 582, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 602, *[254, 255], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 582)
    ops.geomTransf('Linear', 583, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 603, *[255, 256], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 583)
    ops.geomTransf('Linear', 584, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 604, *[256, 257], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 584)
    ops.geomTransf('Linear', 585, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 605, *[257, 258], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 585)
    ops.geomTransf('Linear', 586, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 606, *[229, 253], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 586)
    ops.geomTransf('Linear', 587, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 607, *[230, 254], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 587)
    ops.geomTransf('Linear', 588, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 608, *[231, 255], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 588)
    ops.geomTransf('Linear', 589, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 609, *[232, 256], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 589)
    ops.geomTransf('Linear', 590, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 610, *[233, 257], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 590)
    ops.geomTransf('Linear', 591, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 611, *[234, 258], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 591)
    ops.geomTransf('Linear', 592, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 612, *[259, 260], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 592)
    ops.geomTransf('Linear', 593, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 613, *[260, 261], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 593)
    ops.geomTransf('Linear', 594, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 614, *[261, 262], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 594)
    ops.geomTransf('Linear', 595, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 615, *[262, 263], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 595)
    ops.geomTransf('Linear', 596, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 616, *[263, 264], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 596)
    ops.geomTransf('Linear', 597, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 617, *[235, 259], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 597)
    ops.geomTransf('Linear', 598, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 618, *[236, 260], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 598)
    ops.geomTransf('Linear', 599, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 619, *[237, 261], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 599)
    ops.geomTransf('Linear', 600, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 620, *[238, 262], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 600)
    ops.geomTransf('Linear', 601, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 621, *[239, 263], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 601)
    ops.geomTransf('Linear', 602, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 622, *[240, 264], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 602)
    ops.geomTransf('Linear', 603, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 623, *[264, 258], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 603)
    ops.geomTransf('Linear', 604, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 624, *[258, 252], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 604)
    ops.geomTransf('Linear', 605, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 625, *[252, 246], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 605)
    ops.geomTransf('Linear', 606, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 626, *[263, 257], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 606)
    ops.geomTransf('Linear', 607, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 627, *[257, 251], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 607)
    ops.geomTransf('Linear', 608, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 628, *[251, 245], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 608)
    ops.geomTransf('Linear', 609, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 629, *[262, 256], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 609)
    ops.geomTransf('Linear', 610, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 630, *[256, 250], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 610)
    ops.geomTransf('Linear', 611, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 631, *[250, 244], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 611)
    ops.geomTransf('Linear', 612, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 632, *[261, 255], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 612)
    ops.geomTransf('Linear', 613, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 633, *[255, 249], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 613)
    ops.geomTransf('Linear', 614, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 634, *[249, 243], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 614)
    ops.geomTransf('Linear', 615, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 635, *[260, 254], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 615)
    ops.geomTransf('Linear', 616, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 636, *[254, 248], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 616)
    ops.geomTransf('Linear', 617, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 637, *[248, 242], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 617)
    ops.geomTransf('Linear', 618, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 638, *[259, 253], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 618)
    ops.geomTransf('Linear', 619, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 639, *[253, 247], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 619)
    ops.geomTransf('Linear', 620, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 640, *[247, 241], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 620)
    ops.geomTransf('Linear', 621, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 641, *[265, 266], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 621)
    ops.geomTransf('Linear', 622, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 642, *[266, 267], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 622)
    ops.geomTransf('Linear', 623, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 643, *[267, 268], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 623)
    ops.geomTransf('Linear', 624, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 644, *[268, 269], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 624)
    ops.geomTransf('Linear', 625, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 645, *[269, 270], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 625)
    ops.geomTransf('Linear', 626, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 646, *[241, 265], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 626)
    ops.geomTransf('Linear', 627, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 647, *[242, 266], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 627)
    ops.geomTransf('Linear', 628, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 648, *[243, 267], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 628)
    ops.geomTransf('Linear', 629, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 649, *[244, 268], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 629)
    ops.geomTransf('Linear', 630, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 650, *[245, 269], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 630)
    ops.geomTransf('Linear', 631, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 651, *[246, 270], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 631)
    ops.geomTransf('Linear', 632, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 652, *[271, 272], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 632)
    ops.geomTransf('Linear', 633, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 653, *[272, 273], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 633)
    ops.geomTransf('Linear', 634, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 654, *[273, 274], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 634)
    ops.geomTransf('Linear', 635, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 655, *[274, 275], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 635)
    ops.geomTransf('Linear', 636, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 656, *[275, 276], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 636)
    ops.geomTransf('Linear', 637, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 657, *[247, 271], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 637)
    ops.geomTransf('Linear', 638, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 658, *[248, 272], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 638)
    ops.geomTransf('Linear', 639, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 659, *[249, 273], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 639)
    ops.geomTransf('Linear', 640, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 660, *[250, 274], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 640)
    ops.geomTransf('Linear', 641, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 661, *[251, 275], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 641)
    ops.geomTransf('Linear', 642, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 662, *[252, 276], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 642)
    ops.geomTransf('Linear', 643, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 663, *[277, 278], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 643)
    ops.geomTransf('Linear', 644, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 664, *[278, 279], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 644)
    ops.geomTransf('Linear', 645, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 665, *[279, 280], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 645)
    ops.geomTransf('Linear', 646, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 666, *[280, 281], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 646)
    ops.geomTransf('Linear', 647, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 667, *[281, 282], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 647)
    ops.geomTransf('Linear', 648, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 668, *[253, 277], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 648)
    ops.geomTransf('Linear', 649, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 669, *[254, 278], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 649)
    ops.geomTransf('Linear', 650, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 670, *[255, 279], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 650)
    ops.geomTransf('Linear', 651, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 671, *[256, 280], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 651)
    ops.geomTransf('Linear', 652, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 672, *[257, 281], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 652)
    ops.geomTransf('Linear', 653, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 673, *[258, 282], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 653)
    ops.geomTransf('Linear', 654, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 674, *[283, 284], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 654)
    ops.geomTransf('Linear', 655, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 675, *[284, 285], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 655)
    ops.geomTransf('Linear', 656, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 676, *[285, 286], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 656)
    ops.geomTransf('Linear', 657, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 677, *[286, 287], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 657)
    ops.geomTransf('Linear', 658, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 678, *[287, 288], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 658)
    ops.geomTransf('Linear', 659, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 679, *[259, 283], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 659)
    ops.geomTransf('Linear', 660, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 680, *[260, 284], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 660)
    ops.geomTransf('Linear', 661, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 681, *[261, 285], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 661)
    ops.geomTransf('Linear', 662, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 682, *[262, 286], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 662)
    ops.geomTransf('Linear', 663, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 683, *[263, 287], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 663)
    ops.geomTransf('Linear', 664, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 684, *[264, 288], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 664)
    ops.geomTransf('Linear', 665, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 685, *[288, 282], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 665)
    ops.geomTransf('Linear', 666, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 686, *[282, 276], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 666)
    ops.geomTransf('Linear', 667, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 687, *[276, 270], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 667)
    ops.geomTransf('Linear', 668, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 688, *[287, 281], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 668)
    ops.geomTransf('Linear', 669, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 689, *[281, 275], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 669)
    ops.geomTransf('Linear', 670, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 690, *[275, 269], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 670)
    ops.geomTransf('Linear', 671, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 691, *[286, 280], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 671)
    ops.geomTransf('Linear', 672, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 692, *[280, 274], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 672)
    ops.geomTransf('Linear', 673, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 693, *[274, 268], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 673)
    ops.geomTransf('Linear', 674, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 694, *[285, 279], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 674)
    ops.geomTransf('Linear', 675, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 695, *[279, 273], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 675)
    ops.geomTransf('Linear', 676, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 696, *[273, 267], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 676)
    ops.geomTransf('Linear', 677, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 697, *[284, 278], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 677)
    ops.geomTransf('Linear', 678, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 698, *[278, 272], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 678)
    ops.geomTransf('Linear', 679, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 699, *[272, 266], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 679)
    ops.geomTransf('Linear', 680, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 700, *[283, 277], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 680)
    ops.geomTransf('Linear', 681, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 701, *[277, 271], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 681)
    ops.geomTransf('Linear', 682, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 702, *[271, 265], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 682)
    ops.geomTransf('Linear', 683, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 703, *[289, 290], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 683)
    ops.geomTransf('Linear', 684, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 704, *[290, 291], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 684)
    ops.geomTransf('Linear', 685, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 705, *[291, 292], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 685)
    ops.geomTransf('Linear', 686, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 706, *[292, 293], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 686)
    ops.geomTransf('Linear', 687, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 707, *[293, 294], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 687)
    ops.geomTransf('Linear', 688, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 708, *[265, 289], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 688)
    ops.geomTransf('Linear', 689, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 709, *[266, 290], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 689)
    ops.geomTransf('Linear', 690, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 710, *[267, 291], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 690)
    ops.geomTransf('Linear', 691, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 711, *[268, 292], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 691)
    ops.geomTransf('Linear', 692, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 712, *[269, 293], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 692)
    ops.geomTransf('Linear', 693, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 713, *[270, 294], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 693)
    ops.geomTransf('Linear', 694, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 714, *[295, 296], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 694)
    ops.geomTransf('Linear', 695, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 715, *[296, 297], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 695)
    ops.geomTransf('Linear', 696, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 716, *[297, 298], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 696)
    ops.geomTransf('Linear', 697, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 717, *[298, 299], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 697)
    ops.geomTransf('Linear', 698, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 718, *[299, 300], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 698)
    ops.geomTransf('Linear', 699, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 719, *[271, 295], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 699)
    ops.geomTransf('Linear', 700, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 720, *[272, 296], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 700)
    ops.geomTransf('Linear', 701, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 721, *[273, 297], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 701)
    ops.geomTransf('Linear', 702, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 722, *[274, 298], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 702)
    ops.geomTransf('Linear', 703, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 723, *[275, 299], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 703)
    ops.geomTransf('Linear', 704, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 724, *[276, 300], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 704)
    ops.geomTransf('Linear', 705, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 725, *[301, 302], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 705)
    ops.geomTransf('Linear', 706, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 726, *[302, 303], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 706)
    ops.geomTransf('Linear', 707, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 727, *[303, 304], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 707)
    ops.geomTransf('Linear', 708, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 728, *[304, 305], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 708)
    ops.geomTransf('Linear', 709, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 729, *[305, 306], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 709)
    ops.geomTransf('Linear', 710, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 730, *[277, 301], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 710)
    ops.geomTransf('Linear', 711, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 731, *[278, 302], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 711)
    ops.geomTransf('Linear', 712, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 732, *[279, 303], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 712)
    ops.geomTransf('Linear', 713, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 733, *[280, 304], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 713)
    ops.geomTransf('Linear', 714, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 734, *[281, 305], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 714)
    ops.geomTransf('Linear', 715, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 735, *[282, 306], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 715)
    ops.geomTransf('Linear', 716, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 736, *[307, 308], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 716)
    ops.geomTransf('Linear', 717, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 737, *[308, 309], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 717)
    ops.geomTransf('Linear', 718, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 738, *[309, 310], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 718)
    ops.geomTransf('Linear', 719, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 739, *[310, 311], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 719)
    ops.geomTransf('Linear', 720, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 740, *[311, 312], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 720)
    ops.geomTransf('Linear', 721, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 741, *[283, 307], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 721)
    ops.geomTransf('Linear', 722, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 742, *[284, 308], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 722)
    ops.geomTransf('Linear', 723, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 743, *[285, 309], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 723)
    ops.geomTransf('Linear', 724, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 744, *[286, 310], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 724)
    ops.geomTransf('Linear', 725, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 745, *[287, 311], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 725)
    ops.geomTransf('Linear', 726, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 746, *[288, 312], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 726)
    ops.geomTransf('Linear', 727, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 747, *[312, 306], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 727)
    ops.geomTransf('Linear', 728, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 748, *[306, 300], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 728)
    ops.geomTransf('Linear', 729, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 749, *[300, 294], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 729)
    ops.geomTransf('Linear', 730, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 750, *[311, 305], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 730)
    ops.geomTransf('Linear', 731, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 751, *[305, 299], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 731)
    ops.geomTransf('Linear', 732, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 752, *[299, 293], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 732)
    ops.geomTransf('Linear', 733, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 753, *[310, 304], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 733)
    ops.geomTransf('Linear', 734, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 754, *[304, 298], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 734)
    ops.geomTransf('Linear', 735, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 755, *[298, 292], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 735)
    ops.geomTransf('Linear', 736, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 756, *[309, 303], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 736)
    ops.geomTransf('Linear', 737, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 757, *[303, 297], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 737)
    ops.geomTransf('Linear', 738, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 758, *[297, 291], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 738)
    ops.geomTransf('Linear', 739, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 759, *[308, 302], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 739)
    ops.geomTransf('Linear', 740, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 760, *[302, 296], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 740)
    ops.geomTransf('Linear', 741, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 761, *[296, 290], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 741)
    ops.geomTransf('Linear', 742, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 762, *[307, 301], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 742)
    ops.geomTransf('Linear', 743, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 763, *[301, 295], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 743)
    ops.geomTransf('Linear', 744, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 764, *[295, 289], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 744)
    ops.geomTransf('Linear', 745, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 765, *[313, 314], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 745)
    ops.geomTransf('Linear', 746, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 766, *[314, 315], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 746)
    ops.geomTransf('Linear', 747, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 767, *[315, 316], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 747)
    ops.geomTransf('Linear', 748, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 768, *[316, 317], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 748)
    ops.geomTransf('Linear', 749, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 769, *[317, 318], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 749)
    ops.geomTransf('Linear', 750, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 770, *[289, 313], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 750)
    ops.geomTransf('Linear', 751, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 771, *[290, 314], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 751)
    ops.geomTransf('Linear', 752, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 772, *[291, 315], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 752)
    ops.geomTransf('Linear', 753, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 773, *[292, 316], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 753)
    ops.geomTransf('Linear', 754, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 774, *[293, 317], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 754)
    ops.geomTransf('Linear', 755, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 775, *[294, 318], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 755)
    ops.geomTransf('Linear', 756, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 776, *[319, 320], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 756)
    ops.geomTransf('Linear', 757, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 777, *[320, 321], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 757)
    ops.geomTransf('Linear', 758, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 778, *[321, 322], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 758)
    ops.geomTransf('Linear', 759, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 779, *[322, 323], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 759)
    ops.geomTransf('Linear', 760, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 780, *[323, 324], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 760)
    ops.geomTransf('Linear', 761, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 781, *[295, 319], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 761)
    ops.geomTransf('Linear', 762, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 782, *[296, 320], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 762)
    ops.geomTransf('Linear', 763, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 783, *[297, 321], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 763)
    ops.geomTransf('Linear', 764, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 784, *[298, 322], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 764)
    ops.geomTransf('Linear', 765, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 785, *[299, 323], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 765)
    ops.geomTransf('Linear', 766, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 786, *[300, 324], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 766)
    ops.geomTransf('Linear', 767, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 787, *[325, 326], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 767)
    ops.geomTransf('Linear', 768, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 788, *[326, 327], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 768)
    ops.geomTransf('Linear', 769, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 789, *[327, 328], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 769)
    ops.geomTransf('Linear', 770, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 790, *[328, 329], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 770)
    ops.geomTransf('Linear', 771, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 791, *[329, 330], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 771)
    ops.geomTransf('Linear', 772, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 792, *[301, 325], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 772)
    ops.geomTransf('Linear', 773, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 793, *[302, 326], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 773)
    ops.geomTransf('Linear', 774, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 794, *[303, 327], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 774)
    ops.geomTransf('Linear', 775, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 795, *[304, 328], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 775)
    ops.geomTransf('Linear', 776, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 796, *[305, 329], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 776)
    ops.geomTransf('Linear', 777, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 797, *[306, 330], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 777)
    ops.geomTransf('Linear', 778, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 798, *[331, 332], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 778)
    ops.geomTransf('Linear', 779, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 799, *[332, 333], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 779)
    ops.geomTransf('Linear', 780, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 800, *[333, 334], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 780)
    ops.geomTransf('Linear', 781, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 801, *[334, 335], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 781)
    ops.geomTransf('Linear', 782, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 802, *[335, 336], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 782)
    ops.geomTransf('Linear', 783, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 803, *[307, 331], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 783)
    ops.geomTransf('Linear', 784, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 804, *[308, 332], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 784)
    ops.geomTransf('Linear', 785, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 805, *[309, 333], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 785)
    ops.geomTransf('Linear', 786, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 806, *[310, 334], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 786)
    ops.geomTransf('Linear', 787, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 807, *[311, 335], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 787)
    ops.geomTransf('Linear', 788, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 808, *[312, 336], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 788)
    ops.geomTransf('Linear', 789, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 809, *[336, 330], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 789)
    ops.geomTransf('Linear', 790, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 810, *[330, 324], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 790)
    ops.geomTransf('Linear', 791, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 811, *[324, 318], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 791)
    ops.geomTransf('Linear', 792, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 812, *[335, 329], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 792)
    ops.geomTransf('Linear', 793, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 813, *[329, 323], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 793)
    ops.geomTransf('Linear', 794, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 814, *[323, 317], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 794)
    ops.geomTransf('Linear', 795, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 815, *[334, 328], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 795)
    ops.geomTransf('Linear', 796, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 816, *[328, 322], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 796)
    ops.geomTransf('Linear', 797, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 817, *[322, 316], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 797)
    ops.geomTransf('Linear', 798, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 818, *[333, 327], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 798)
    ops.geomTransf('Linear', 799, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 819, *[327, 321], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 799)
    ops.geomTransf('Linear', 800, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 820, *[321, 315], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 800)
    ops.geomTransf('Linear', 801, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 821, *[332, 326], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 801)
    ops.geomTransf('Linear', 802, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 822, *[326, 320], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 802)
    ops.geomTransf('Linear', 803, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 823, *[320, 314], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 803)
    ops.geomTransf('Linear', 804, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 824, *[331, 325], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 804)
    ops.geomTransf('Linear', 805, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 825, *[325, 319], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 805)
    ops.geomTransf('Linear', 806, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 826, *[319, 313], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 806)
    ops.geomTransf('Linear', 807, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 827, *[337, 338], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 807)
    ops.geomTransf('Linear', 808, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 828, *[338, 339], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 808)
    ops.geomTransf('Linear', 809, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 829, *[339, 340], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 809)
    ops.geomTransf('Linear', 810, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 830, *[340, 341], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 810)
    ops.geomTransf('Linear', 811, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 831, *[341, 342], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 811)
    ops.geomTransf('Linear', 812, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 832, *[313, 337], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 812)
    ops.geomTransf('Linear', 813, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 833, *[314, 338], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 813)
    ops.geomTransf('Linear', 814, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 834, *[315, 339], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 814)
    ops.geomTransf('Linear', 815, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 835, *[316, 340], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 815)
    ops.geomTransf('Linear', 816, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 836, *[317, 341], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 816)
    ops.geomTransf('Linear', 817, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 837, *[318, 342], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 817)
    ops.geomTransf('Linear', 818, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 838, *[343, 344], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 818)
    ops.geomTransf('Linear', 819, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 839, *[344, 345], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 819)
    ops.geomTransf('Linear', 820, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 840, *[345, 346], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 820)
    ops.geomTransf('Linear', 821, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 841, *[346, 347], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 821)
    ops.geomTransf('Linear', 822, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 842, *[347, 348], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 822)
    ops.geomTransf('Linear', 823, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 843, *[319, 343], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 823)
    ops.geomTransf('Linear', 824, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 844, *[320, 344], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 824)
    ops.geomTransf('Linear', 825, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 845, *[321, 345], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 825)
    ops.geomTransf('Linear', 826, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 846, *[322, 346], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 826)
    ops.geomTransf('Linear', 827, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 847, *[323, 347], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 827)
    ops.geomTransf('Linear', 828, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 848, *[324, 348], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 828)
    ops.geomTransf('Linear', 829, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 849, *[349, 350], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 829)
    ops.geomTransf('Linear', 830, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 850, *[350, 351], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 830)
    ops.geomTransf('Linear', 831, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 851, *[351, 352], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 831)
    ops.geomTransf('Linear', 832, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 852, *[352, 353], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 832)
    ops.geomTransf('Linear', 833, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 853, *[353, 354], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 833)
    ops.geomTransf('Linear', 834, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 854, *[325, 349], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 834)
    ops.geomTransf('Linear', 835, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 855, *[326, 350], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 835)
    ops.geomTransf('Linear', 836, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 856, *[327, 351], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 836)
    ops.geomTransf('Linear', 837, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 857, *[328, 352], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 837)
    ops.geomTransf('Linear', 838, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 858, *[329, 353], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 838)
    ops.geomTransf('Linear', 839, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 859, *[330, 354], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 839)
    ops.geomTransf('Linear', 840, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 860, *[355, 356], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 840)
    ops.geomTransf('Linear', 841, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 861, *[356, 357], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 841)
    ops.geomTransf('Linear', 842, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 862, *[357, 358], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 842)
    ops.geomTransf('Linear', 843, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 863, *[358, 359], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 843)
    ops.geomTransf('Linear', 844, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 864, *[359, 360], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 844)
    ops.geomTransf('Linear', 845, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 865, *[331, 355], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 845)
    ops.geomTransf('Linear', 846, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 866, *[332, 356], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 846)
    ops.geomTransf('Linear', 847, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 867, *[333, 357], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 847)
    ops.geomTransf('Linear', 848, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 868, *[334, 358], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 848)
    ops.geomTransf('Linear', 849, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 869, *[335, 359], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 849)
    ops.geomTransf('Linear', 850, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 870, *[336, 360], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 850)
    ops.geomTransf('Linear', 851, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 871, *[360, 354], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 851)
    ops.geomTransf('Linear', 852, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 872, *[354, 348], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 852)
    ops.geomTransf('Linear', 853, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 873, *[348, 342], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 853)
    ops.geomTransf('Linear', 854, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 874, *[359, 353], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 854)
    ops.geomTransf('Linear', 855, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 875, *[353, 347], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 855)
    ops.geomTransf('Linear', 856, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 876, *[347, 341], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 856)
    ops.geomTransf('Linear', 857, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 877, *[358, 352], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 857)
    ops.geomTransf('Linear', 858, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 878, *[352, 346], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 858)
    ops.geomTransf('Linear', 859, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 879, *[346, 340], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 859)
    ops.geomTransf('Linear', 860, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 880, *[357, 351], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 860)
    ops.geomTransf('Linear', 861, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 881, *[351, 345], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 861)
    ops.geomTransf('Linear', 862, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 882, *[345, 339], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 862)
    ops.geomTransf('Linear', 863, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 883, *[356, 350], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 863)
    ops.geomTransf('Linear', 864, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 884, *[350, 344], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 864)
    ops.geomTransf('Linear', 865, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 885, *[344, 338], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 865)
    ops.geomTransf('Linear', 866, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 886, *[355, 349], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 866)
    ops.geomTransf('Linear', 867, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 887, *[349, 343], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 867)
    ops.geomTransf('Linear', 868, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 888, *[343, 337], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 868)
    ops.geomTransf('Linear', 869, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 889, *[361, 362], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 869)
    ops.geomTransf('Linear', 870, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 890, *[362, 363], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 870)
    ops.geomTransf('Linear', 871, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 891, *[363, 364], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 871)
    ops.geomTransf('Linear', 872, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 892, *[364, 365], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 872)
    ops.geomTransf('Linear', 873, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 893, *[365, 366], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 873)
    ops.geomTransf('Linear', 874, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 894, *[337, 361], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 874)
    ops.geomTransf('Linear', 875, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 895, *[338, 362], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 875)
    ops.geomTransf('Linear', 876, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 896, *[339, 363], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 876)
    ops.geomTransf('Linear', 877, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 897, *[340, 364], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 877)
    ops.geomTransf('Linear', 878, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 898, *[341, 365], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 878)
    ops.geomTransf('Linear', 879, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 899, *[342, 366], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 879)
    ops.geomTransf('Linear', 880, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 900, *[367, 368], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 880)
    ops.geomTransf('Linear', 881, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 901, *[368, 369], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 881)
    ops.geomTransf('Linear', 882, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 902, *[369, 370], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 882)
    ops.geomTransf('Linear', 883, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 903, *[370, 371], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 883)
    ops.geomTransf('Linear', 884, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 904, *[371, 372], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 884)
    ops.geomTransf('Linear', 885, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 905, *[343, 367], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 885)
    ops.geomTransf('Linear', 886, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 906, *[344, 368], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 886)
    ops.geomTransf('Linear', 887, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 907, *[345, 369], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 887)
    ops.geomTransf('Linear', 888, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 908, *[346, 370], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 888)
    ops.geomTransf('Linear', 889, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 909, *[347, 371], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 889)
    ops.geomTransf('Linear', 890, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 910, *[348, 372], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 890)
    ops.geomTransf('Linear', 891, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 911, *[373, 374], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 891)
    ops.geomTransf('Linear', 892, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 912, *[374, 375], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 892)
    ops.geomTransf('Linear', 893, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 913, *[375, 376], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 893)
    ops.geomTransf('Linear', 894, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 914, *[376, 377], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 894)
    ops.geomTransf('Linear', 895, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 915, *[377, 378], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 895)
    ops.geomTransf('Linear', 896, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 916, *[349, 373], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 896)
    ops.geomTransf('Linear', 897, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 917, *[350, 374], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 897)
    ops.geomTransf('Linear', 898, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 918, *[351, 375], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 898)
    ops.geomTransf('Linear', 899, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 919, *[352, 376], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 899)
    ops.geomTransf('Linear', 900, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 920, *[353, 377], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 900)
    ops.geomTransf('Linear', 901, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 921, *[354, 378], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 901)
    ops.geomTransf('Linear', 902, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 922, *[379, 380], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 902)
    ops.geomTransf('Linear', 903, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 923, *[380, 381], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 903)
    ops.geomTransf('Linear', 904, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 924, *[381, 382], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 904)
    ops.geomTransf('Linear', 905, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 925, *[382, 383], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 905)
    ops.geomTransf('Linear', 906, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 926, *[383, 384], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 906)
    ops.geomTransf('Linear', 907, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 927, *[355, 379], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 907)
    ops.geomTransf('Linear', 908, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 928, *[356, 380], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 908)
    ops.geomTransf('Linear', 909, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 929, *[357, 381], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 909)
    ops.geomTransf('Linear', 910, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 930, *[358, 382], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 910)
    ops.geomTransf('Linear', 911, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 931, *[359, 383], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 911)
    ops.geomTransf('Linear', 912, *[1.0, 0.0, 0.0])
    ops.element('elasticBeamColumn', 932, *[360, 384], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 912)
    ops.geomTransf('Linear', 913, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 933, *[384, 378], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 913)
    ops.geomTransf('Linear', 914, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 934, *[378, 372], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 914)
    ops.geomTransf('Linear', 915, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 935, *[372, 366], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 915)
    ops.geomTransf('Linear', 916, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 936, *[383, 377], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 916)
    ops.geomTransf('Linear', 917, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 937, *[377, 371], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 917)
    ops.geomTransf('Linear', 918, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 938, *[371, 365], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 918)
    ops.geomTransf('Linear', 919, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 939, *[382, 376], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 919)
    ops.geomTransf('Linear', 920, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 940, *[376, 370], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 920)
    ops.geomTransf('Linear', 921, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 941, *[370, 364], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 921)
    ops.geomTransf('Linear', 922, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 942, *[381, 375], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 922)
    ops.geomTransf('Linear', 923, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 943, *[375, 369], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 923)
    ops.geomTransf('Linear', 924, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 944, *[369, 363], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 924)
    ops.geomTransf('Linear', 925, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 945, *[380, 374], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 925)
    ops.geomTransf('Linear', 926, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 946, *[374, 368], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 926)
    ops.geomTransf('Linear', 927, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 947, *[368, 362], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 927)
    ops.geomTransf('Linear', 928, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 948, *[379, 373], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 928)
    ops.geomTransf('Linear', 929, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 949, *[373, 367], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 929)
    ops.geomTransf('Linear', 930, *[0.0, 0.0, 1.0])
    ops.element('elasticBeamColumn', 950, *[367, 361], SecProps[1].A, MatProps[1].E,
                MatProps[1].G, SecProps[1].Ixx, SecProps[1].Iyy, SecProps[1].Izz, 930)

    # Fix the node.
    ops.fix(1, *[1, 1, 1, 1, 1, 1])
    ops.fix(2, *[1, 1, 1, 1, 1, 1])
    ops.fix(3, *[1, 1, 1, 1, 1, 1])
    ops.fix(4, *[1, 1, 1, 1, 1, 1])
    ops.fix(5, *[1, 1, 1, 1, 1, 1])
    ops.fix(6, *[1, 1, 1, 1, 1, 1])
    ops.fix(37, *[1, 1, 1, 1, 1, 1])
    ops.fix(38, *[1, 1, 1, 1, 1, 1])
    ops.fix(39, *[1, 1, 1, 1, 1, 1])
    ops.fix(40, *[1, 1, 1, 1, 1, 1])
    ops.fix(41, *[1, 1, 1, 1, 1, 1])
    ops.fix(42, *[1, 1, 1, 1, 1, 1])
    ops.fix(73, *[1, 1, 1, 1, 1, 1])
    ops.fix(74, *[1, 1, 1, 1, 1, 1])
    ops.fix(75, *[1, 1, 1, 1, 1, 1])
    ops.fix(76, *[1, 1, 1, 1, 1, 1])
    ops.fix(77, *[1, 1, 1, 1, 1, 1])
    ops.fix(78, *[1, 1, 1, 1, 1, 1])
    ops.fix(109, *[1, 1, 1, 1, 1, 1])
    ops.fix(110, *[1, 1, 1, 1, 1, 1])
    ops.fix(111, *[1, 1, 1, 1, 1, 1])
    ops.fix(112, *[1, 1, 1, 1, 1, 1])
    ops.fix(113, *[1, 1, 1, 1, 1, 1])
    ops.fix(114, *[1, 1, 1, 1, 1, 1])

    # Set the mass at a node.
    ops.mass(1, *[1.5934, 1.5934, 1.5934])
    ops.mass(2, *[1.5934, 1.5934, 1.5934])
    ops.mass(3, *[1.5934, 1.5934, 1.5934])
    ops.mass(4, *[1.5934, 1.5934, 1.5934])
    ops.mass(5, *[1.5934, 1.5934, 1.5934])
    ops.mass(6, *[1.5934, 1.5934, 1.5934])
    ops.mass(7, *[6.3736, 6.3736, 6.3736])
    ops.mass(8, *[7.9671, 7.9671, 7.9671])
    ops.mass(9, *[7.9671, 7.9671, 7.9671])
    ops.mass(10, *[7.9671, 7.9671, 7.9671])
    ops.mass(11, *[7.9671, 7.9671, 7.9671])
    ops.mass(12, *[6.3736, 6.3736, 6.3736])
    ops.mass(13, *[6.3736, 6.3736, 6.3736])
    ops.mass(14, *[7.9671, 7.9671, 7.9671])
    ops.mass(15, *[7.9671, 7.9671, 7.9671])
    ops.mass(16, *[7.9671, 7.9671, 7.9671])
    ops.mass(17, *[7.9671, 7.9671, 7.9671])
    ops.mass(18, *[6.3736, 6.3736, 6.3736])
    ops.mass(19, *[6.3736, 6.3736, 6.3736])
    ops.mass(20, *[7.9671, 7.9671, 7.9671])
    ops.mass(21, *[7.9671, 7.9671, 7.9671])
    ops.mass(22, *[7.9671, 7.9671, 7.9671])
    ops.mass(23, *[7.9671, 7.9671, 7.9671])
    ops.mass(24, *[6.3736, 6.3736, 6.3736])
    ops.mass(25, *[6.3736, 6.3736, 6.3736])
    ops.mass(26, *[7.9671, 7.9671, 7.9671])
    ops.mass(27, *[7.9671, 7.9671, 7.9671])
    ops.mass(28, *[7.9671, 7.9671, 7.9671])
    ops.mass(29, *[7.9671, 7.9671, 7.9671])
    ops.mass(30, *[6.3736, 6.3736, 6.3736])
    ops.mass(31, *[6.3736, 6.3736, 6.3736])
    ops.mass(32, *[7.9671, 7.9671, 7.9671])
    ops.mass(33, *[7.9671, 7.9671, 7.9671])
    ops.mass(34, *[7.9671, 7.9671, 7.9671])
    ops.mass(35, *[7.9671, 7.9671, 7.9671])
    ops.mass(36, *[6.3736, 6.3736, 6.3736])
    ops.mass(37, *[1.5934, 1.5934, 1.5934])
    ops.mass(38, *[1.5934, 1.5934, 1.5934])
    ops.mass(39, *[1.5934, 1.5934, 1.5934])
    ops.mass(40, *[1.5934, 1.5934, 1.5934])
    ops.mass(41, *[1.5934, 1.5934, 1.5934])
    ops.mass(42, *[1.5934, 1.5934, 1.5934])
    ops.mass(43, *[7.9671, 7.9671, 7.9671])
    ops.mass(44, *[9.5605, 9.5605, 9.5605])
    ops.mass(45, *[9.5605, 9.5605, 9.5605])
    ops.mass(46, *[9.5605, 9.5605, 9.5605])
    ops.mass(47, *[9.5605, 9.5605, 9.5605])
    ops.mass(48, *[7.9671, 7.9671, 7.9671])
    ops.mass(49, *[7.9671, 7.9671, 7.9671])
    ops.mass(50, *[9.5605, 9.5605, 9.5605])
    ops.mass(51, *[9.5605, 9.5605, 9.5605])
    ops.mass(52, *[9.5605, 9.5605, 9.5605])
    ops.mass(53, *[9.5605, 9.5605, 9.5605])
    ops.mass(54, *[7.9671, 7.9671, 7.9671])
    ops.mass(55, *[7.9671, 7.9671, 7.9671])
    ops.mass(56, *[9.5605, 9.5605, 9.5605])
    ops.mass(57, *[9.5605, 9.5605, 9.5605])
    ops.mass(58, *[9.5605, 9.5605, 9.5605])
    ops.mass(59, *[9.5605, 9.5605, 9.5605])
    ops.mass(60, *[7.9671, 7.9671, 7.9671])
    ops.mass(61, *[7.9671, 7.9671, 7.9671])
    ops.mass(62, *[9.5605, 9.5605, 9.5605])
    ops.mass(63, *[9.5605, 9.5605, 9.5605])
    ops.mass(64, *[9.5605, 9.5605, 9.5605])
    ops.mass(65, *[9.5605, 9.5605, 9.5605])
    ops.mass(66, *[7.9671, 7.9671, 7.9671])
    ops.mass(67, *[7.9671, 7.9671, 7.9671])
    ops.mass(68, *[9.5605, 9.5605, 9.5605])
    ops.mass(69, *[9.5605, 9.5605, 9.5605])
    ops.mass(70, *[9.5605, 9.5605, 9.5605])
    ops.mass(71, *[9.5605, 9.5605, 9.5605])
    ops.mass(72, *[7.9671, 7.9671, 7.9671])
    ops.mass(73, *[1.5934, 1.5934, 1.5934])
    ops.mass(74, *[1.5934, 1.5934, 1.5934])
    ops.mass(75, *[1.5934, 1.5934, 1.5934])
    ops.mass(76, *[1.5934, 1.5934, 1.5934])
    ops.mass(77, *[1.5934, 1.5934, 1.5934])
    ops.mass(78, *[1.5934, 1.5934, 1.5934])
    ops.mass(79, *[7.9671, 7.9671, 7.9671])
    ops.mass(80, *[9.5605, 9.5605, 9.5605])
    ops.mass(81, *[9.5605, 9.5605, 9.5605])
    ops.mass(82, *[9.5605, 9.5605, 9.5605])
    ops.mass(83, *[9.5605, 9.5605, 9.5605])
    ops.mass(84, *[7.9671, 7.9671, 7.9671])
    ops.mass(85, *[7.9671, 7.9671, 7.9671])
    ops.mass(86, *[9.5605, 9.5605, 9.5605])
    ops.mass(87, *[9.5605, 9.5605, 9.5605])
    ops.mass(88, *[9.5605, 9.5605, 9.5605])
    ops.mass(89, *[9.5605, 9.5605, 9.5605])
    ops.mass(90, *[7.9671, 7.9671, 7.9671])
    ops.mass(91, *[7.9671, 7.9671, 7.9671])
    ops.mass(92, *[9.5605, 9.5605, 9.5605])
    ops.mass(93, *[9.5605, 9.5605, 9.5605])
    ops.mass(94, *[9.5605, 9.5605, 9.5605])
    ops.mass(95, *[9.5605, 9.5605, 9.5605])
    ops.mass(96, *[7.9671, 7.9671, 7.9671])
    ops.mass(97, *[7.9671, 7.9671, 7.9671])
    ops.mass(98, *[9.5605, 9.5605, 9.5605])
    ops.mass(99, *[9.5605, 9.5605, 9.5605])
    ops.mass(100, *[9.5605, 9.5605, 9.5605])
    ops.mass(101, *[9.5605, 9.5605, 9.5605])
    ops.mass(102, *[7.9671, 7.9671, 7.9671])
    ops.mass(103, *[7.9671, 7.9671, 7.9671])
    ops.mass(104, *[9.5605, 9.5605, 9.5605])
    ops.mass(105, *[9.5605, 9.5605, 9.5605])
    ops.mass(106, *[9.5605, 9.5605, 9.5605])
    ops.mass(107, *[9.5605, 9.5605, 9.5605])
    ops.mass(108, *[7.9671, 7.9671, 7.9671])
    ops.mass(109, *[1.5934, 1.5934, 1.5934])
    ops.mass(110, *[1.5934, 1.5934, 1.5934])
    ops.mass(111, *[1.5934, 1.5934, 1.5934])
    ops.mass(112, *[1.5934, 1.5934, 1.5934])
    ops.mass(113, *[1.5934, 1.5934, 1.5934])
    ops.mass(114, *[1.5934, 1.5934, 1.5934])
    ops.mass(115, *[6.3736, 6.3736, 6.3736])
    ops.mass(116, *[7.9671, 7.9671, 7.9671])
    ops.mass(117, *[7.9671, 7.9671, 7.9671])
    ops.mass(118, *[7.9671, 7.9671, 7.9671])
    ops.mass(119, *[7.9671, 7.9671, 7.9671])
    ops.mass(120, *[6.3736, 6.3736, 6.3736])
    ops.mass(121, *[6.3736, 6.3736, 6.3736])
    ops.mass(122, *[7.9671, 7.9671, 7.9671])
    ops.mass(123, *[7.9671, 7.9671, 7.9671])
    ops.mass(124, *[7.9671, 7.9671, 7.9671])
    ops.mass(125, *[7.9671, 7.9671, 7.9671])
    ops.mass(126, *[6.3736, 6.3736, 6.3736])
    ops.mass(127, *[6.3736, 6.3736, 6.3736])
    ops.mass(128, *[7.9671, 7.9671, 7.9671])
    ops.mass(129, *[7.9671, 7.9671, 7.9671])
    ops.mass(130, *[7.9671, 7.9671, 7.9671])
    ops.mass(131, *[7.9671, 7.9671, 7.9671])
    ops.mass(132, *[6.3736, 6.3736, 6.3736])
    ops.mass(133, *[6.3736, 6.3736, 6.3736])
    ops.mass(134, *[7.9671, 7.9671, 7.9671])
    ops.mass(135, *[7.9671, 7.9671, 7.9671])
    ops.mass(136, *[7.9671, 7.9671, 7.9671])
    ops.mass(137, *[7.9671, 7.9671, 7.9671])
    ops.mass(138, *[6.3736, 6.3736, 6.3736])
    ops.mass(139, *[6.3736, 6.3736, 6.3736])
    ops.mass(140, *[7.9671, 7.9671, 7.9671])
    ops.mass(141, *[7.9671, 7.9671, 7.9671])
    ops.mass(142, *[7.9671, 7.9671, 7.9671])
    ops.mass(143, *[7.9671, 7.9671, 7.9671])
    ops.mass(144, *[6.3736, 6.3736, 6.3736])
    ops.mass(145, *[6.3736, 6.3736, 6.3736])
    ops.mass(146, *[7.9671, 7.9671, 7.9671])
    ops.mass(147, *[7.9671, 7.9671, 7.9671])
    ops.mass(148, *[7.9671, 7.9671, 7.9671])
    ops.mass(149, *[7.9671, 7.9671, 7.9671])
    ops.mass(150, *[6.3736, 6.3736, 6.3736])
    ops.mass(151, *[7.9671, 7.9671, 7.9671])
    ops.mass(152, *[9.5605, 9.5605, 9.5605])
    ops.mass(153, *[9.5605, 9.5605, 9.5605])
    ops.mass(154, *[9.5605, 9.5605, 9.5605])
    ops.mass(155, *[9.5605, 9.5605, 9.5605])
    ops.mass(156, *[7.9671, 7.9671, 7.9671])
    ops.mass(157, *[7.9671, 7.9671, 7.9671])
    ops.mass(158, *[9.5605, 9.5605, 9.5605])
    ops.mass(159, *[9.5605, 9.5605, 9.5605])
    ops.mass(160, *[9.5605, 9.5605, 9.5605])
    ops.mass(161, *[9.5605, 9.5605, 9.5605])
    ops.mass(162, *[7.9671, 7.9671, 7.9671])
    ops.mass(163, *[6.3736, 6.3736, 6.3736])
    ops.mass(164, *[7.9671, 7.9671, 7.9671])
    ops.mass(165, *[7.9671, 7.9671, 7.9671])
    ops.mass(166, *[7.9671, 7.9671, 7.9671])
    ops.mass(167, *[7.9671, 7.9671, 7.9671])
    ops.mass(168, *[6.3736, 6.3736, 6.3736])
    ops.mass(169, *[6.3736, 6.3736, 6.3736])
    ops.mass(170, *[7.9671, 7.9671, 7.9671])
    ops.mass(171, *[7.9671, 7.9671, 7.9671])
    ops.mass(172, *[7.9671, 7.9671, 7.9671])
    ops.mass(173, *[7.9671, 7.9671, 7.9671])
    ops.mass(174, *[6.3736, 6.3736, 6.3736])
    ops.mass(175, *[7.9671, 7.9671, 7.9671])
    ops.mass(176, *[9.5605, 9.5605, 9.5605])
    ops.mass(177, *[9.5605, 9.5605, 9.5605])
    ops.mass(178, *[9.5605, 9.5605, 9.5605])
    ops.mass(179, *[9.5605, 9.5605, 9.5605])
    ops.mass(180, *[7.9671, 7.9671, 7.9671])
    ops.mass(181, *[7.9671, 7.9671, 7.9671])
    ops.mass(182, *[9.5605, 9.5605, 9.5605])
    ops.mass(183, *[9.5605, 9.5605, 9.5605])
    ops.mass(184, *[9.5605, 9.5605, 9.5605])
    ops.mass(185, *[9.5605, 9.5605, 9.5605])
    ops.mass(186, *[7.9671, 7.9671, 7.9671])
    ops.mass(187, *[6.3736, 6.3736, 6.3736])
    ops.mass(188, *[7.9671, 7.9671, 7.9671])
    ops.mass(189, *[7.9671, 7.9671, 7.9671])
    ops.mass(190, *[7.9671, 7.9671, 7.9671])
    ops.mass(191, *[7.9671, 7.9671, 7.9671])
    ops.mass(192, *[6.3736, 6.3736, 6.3736])
    ops.mass(193, *[6.3736, 6.3736, 6.3736])
    ops.mass(194, *[7.9671, 7.9671, 7.9671])
    ops.mass(195, *[7.9671, 7.9671, 7.9671])
    ops.mass(196, *[7.9671, 7.9671, 7.9671])
    ops.mass(197, *[7.9671, 7.9671, 7.9671])
    ops.mass(198, *[6.3736, 6.3736, 6.3736])
    ops.mass(199, *[7.9671, 7.9671, 7.9671])
    ops.mass(200, *[9.5605, 9.5605, 9.5605])
    ops.mass(201, *[9.5605, 9.5605, 9.5605])
    ops.mass(202, *[9.5605, 9.5605, 9.5605])
    ops.mass(203, *[9.5605, 9.5605, 9.5605])
    ops.mass(204, *[7.9671, 7.9671, 7.9671])
    ops.mass(205, *[7.9671, 7.9671, 7.9671])
    ops.mass(206, *[9.5605, 9.5605, 9.5605])
    ops.mass(207, *[9.5605, 9.5605, 9.5605])
    ops.mass(208, *[9.5605, 9.5605, 9.5605])
    ops.mass(209, *[9.5605, 9.5605, 9.5605])
    ops.mass(210, *[7.9671, 7.9671, 7.9671])
    ops.mass(211, *[6.3736, 6.3736, 6.3736])
    ops.mass(212, *[7.9671, 7.9671, 7.9671])
    ops.mass(213, *[7.9671, 7.9671, 7.9671])
    ops.mass(214, *[7.9671, 7.9671, 7.9671])
    ops.mass(215, *[7.9671, 7.9671, 7.9671])
    ops.mass(216, *[6.3736, 6.3736, 6.3736])
    ops.mass(217, *[6.3736, 6.3736, 6.3736])
    ops.mass(218, *[7.9671, 7.9671, 7.9671])
    ops.mass(219, *[7.9671, 7.9671, 7.9671])
    ops.mass(220, *[7.9671, 7.9671, 7.9671])
    ops.mass(221, *[7.9671, 7.9671, 7.9671])
    ops.mass(222, *[6.3736, 6.3736, 6.3736])
    ops.mass(223, *[7.9671, 7.9671, 7.9671])
    ops.mass(224, *[9.5605, 9.5605, 9.5605])
    ops.mass(225, *[9.5605, 9.5605, 9.5605])
    ops.mass(226, *[9.5605, 9.5605, 9.5605])
    ops.mass(227, *[9.5605, 9.5605, 9.5605])
    ops.mass(228, *[7.9671, 7.9671, 7.9671])
    ops.mass(229, *[7.9671, 7.9671, 7.9671])
    ops.mass(230, *[9.5605, 9.5605, 9.5605])
    ops.mass(231, *[9.5605, 9.5605, 9.5605])
    ops.mass(232, *[9.5605, 9.5605, 9.5605])
    ops.mass(233, *[9.5605, 9.5605, 9.5605])
    ops.mass(234, *[7.9671, 7.9671, 7.9671])
    ops.mass(235, *[6.3736, 6.3736, 6.3736])
    ops.mass(236, *[7.9671, 7.9671, 7.9671])
    ops.mass(237, *[7.9671, 7.9671, 7.9671])
    ops.mass(238, *[7.9671, 7.9671, 7.9671])
    ops.mass(239, *[7.9671, 7.9671, 7.9671])
    ops.mass(240, *[6.3736, 6.3736, 6.3736])
    ops.mass(241, *[6.3736, 6.3736, 6.3736])
    ops.mass(242, *[7.9671, 7.9671, 7.9671])
    ops.mass(243, *[7.9671, 7.9671, 7.9671])
    ops.mass(244, *[7.9671, 7.9671, 7.9671])
    ops.mass(245, *[7.9671, 7.9671, 7.9671])
    ops.mass(246, *[6.3736, 6.3736, 6.3736])
    ops.mass(247, *[7.9671, 7.9671, 7.9671])
    ops.mass(248, *[9.5605, 9.5605, 9.5605])
    ops.mass(249, *[9.5605, 9.5605, 9.5605])
    ops.mass(250, *[9.5605, 9.5605, 9.5605])
    ops.mass(251, *[9.5605, 9.5605, 9.5605])
    ops.mass(252, *[7.9671, 7.9671, 7.9671])
    ops.mass(253, *[7.9671, 7.9671, 7.9671])
    ops.mass(254, *[9.5605, 9.5605, 9.5605])
    ops.mass(255, *[9.5605, 9.5605, 9.5605])
    ops.mass(256, *[9.5605, 9.5605, 9.5605])
    ops.mass(257, *[9.5605, 9.5605, 9.5605])
    ops.mass(258, *[7.9671, 7.9671, 7.9671])
    ops.mass(259, *[6.3736, 6.3736, 6.3736])
    ops.mass(260, *[7.9671, 7.9671, 7.9671])
    ops.mass(261, *[7.9671, 7.9671, 7.9671])
    ops.mass(262, *[7.9671, 7.9671, 7.9671])
    ops.mass(263, *[7.9671, 7.9671, 7.9671])
    ops.mass(264, *[6.3736, 6.3736, 6.3736])
    ops.mass(265, *[6.3736, 6.3736, 6.3736])
    ops.mass(266, *[7.9671, 7.9671, 7.9671])
    ops.mass(267, *[7.9671, 7.9671, 7.9671])
    ops.mass(268, *[7.9671, 7.9671, 7.9671])
    ops.mass(269, *[7.9671, 7.9671, 7.9671])
    ops.mass(270, *[6.3736, 6.3736, 6.3736])
    ops.mass(271, *[7.9671, 7.9671, 7.9671])
    ops.mass(272, *[9.5605, 9.5605, 9.5605])
    ops.mass(273, *[9.5605, 9.5605, 9.5605])
    ops.mass(274, *[9.5605, 9.5605, 9.5605])
    ops.mass(275, *[9.5605, 9.5605, 9.5605])
    ops.mass(276, *[7.9671, 7.9671, 7.9671])
    ops.mass(277, *[7.9671, 7.9671, 7.9671])
    ops.mass(278, *[9.5605, 9.5605, 9.5605])
    ops.mass(279, *[9.5605, 9.5605, 9.5605])
    ops.mass(280, *[9.5605, 9.5605, 9.5605])
    ops.mass(281, *[9.5605, 9.5605, 9.5605])
    ops.mass(282, *[7.9671, 7.9671, 7.9671])
    ops.mass(283, *[6.3736, 6.3736, 6.3736])
    ops.mass(284, *[7.9671, 7.9671, 7.9671])
    ops.mass(285, *[7.9671, 7.9671, 7.9671])
    ops.mass(286, *[7.9671, 7.9671, 7.9671])
    ops.mass(287, *[7.9671, 7.9671, 7.9671])
    ops.mass(288, *[6.3736, 6.3736, 6.3736])
    ops.mass(289, *[6.3736, 6.3736, 6.3736])
    ops.mass(290, *[7.9671, 7.9671, 7.9671])
    ops.mass(291, *[7.9671, 7.9671, 7.9671])
    ops.mass(292, *[7.9671, 7.9671, 7.9671])
    ops.mass(293, *[7.9671, 7.9671, 7.9671])
    ops.mass(294, *[6.3736, 6.3736, 6.3736])
    ops.mass(295, *[7.9671, 7.9671, 7.9671])
    ops.mass(296, *[9.5605, 9.5605, 9.5605])
    ops.mass(297, *[9.5605, 9.5605, 9.5605])
    ops.mass(298, *[9.5605, 9.5605, 9.5605])
    ops.mass(299, *[9.5605, 9.5605, 9.5605])
    ops.mass(300, *[7.9671, 7.9671, 7.9671])
    ops.mass(301, *[7.9671, 7.9671, 7.9671])
    ops.mass(302, *[9.5605, 9.5605, 9.5605])
    ops.mass(303, *[9.5605, 9.5605, 9.5605])
    ops.mass(304, *[9.5605, 9.5605, 9.5605])
    ops.mass(305, *[9.5605, 9.5605, 9.5605])
    ops.mass(306, *[7.9671, 7.9671, 7.9671])
    ops.mass(307, *[6.3736, 6.3736, 6.3736])
    ops.mass(308, *[7.9671, 7.9671, 7.9671])
    ops.mass(309, *[7.9671, 7.9671, 7.9671])
    ops.mass(310, *[7.9671, 7.9671, 7.9671])
    ops.mass(311, *[7.9671, 7.9671, 7.9671])
    ops.mass(312, *[6.3736, 6.3736, 6.3736])
    ops.mass(313, *[6.3736, 6.3736, 6.3736])
    ops.mass(314, *[7.9671, 7.9671, 7.9671])
    ops.mass(315, *[7.9671, 7.9671, 7.9671])
    ops.mass(316, *[7.9671, 7.9671, 7.9671])
    ops.mass(317, *[7.9671, 7.9671, 7.9671])
    ops.mass(318, *[6.3736, 6.3736, 6.3736])
    ops.mass(319, *[7.9671, 7.9671, 7.9671])
    ops.mass(320, *[9.5605, 9.5605, 9.5605])
    ops.mass(321, *[9.5605, 9.5605, 9.5605])
    ops.mass(322, *[9.5605, 9.5605, 9.5605])
    ops.mass(323, *[9.5605, 9.5605, 9.5605])
    ops.mass(324, *[7.9671, 7.9671, 7.9671])
    ops.mass(325, *[7.9671, 7.9671, 7.9671])
    ops.mass(326, *[9.5605, 9.5605, 9.5605])
    ops.mass(327, *[9.5605, 9.5605, 9.5605])
    ops.mass(328, *[9.5605, 9.5605, 9.5605])
    ops.mass(329, *[9.5605, 9.5605, 9.5605])
    ops.mass(330, *[7.9671, 7.9671, 7.9671])
    ops.mass(331, *[6.3736, 6.3736, 6.3736])
    ops.mass(332, *[7.9671, 7.9671, 7.9671])
    ops.mass(333, *[7.9671, 7.9671, 7.9671])
    ops.mass(334, *[7.9671, 7.9671, 7.9671])
    ops.mass(335, *[7.9671, 7.9671, 7.9671])
    ops.mass(336, *[6.3736, 6.3736, 6.3736])
    ops.mass(337, *[6.3736, 6.3736, 6.3736])
    ops.mass(338, *[7.9671, 7.9671, 7.9671])
    ops.mass(339, *[7.9671, 7.9671, 7.9671])
    ops.mass(340, *[7.9671, 7.9671, 7.9671])
    ops.mass(341, *[7.9671, 7.9671, 7.9671])
    ops.mass(342, *[6.3736, 6.3736, 6.3736])
    ops.mass(343, *[7.9671, 7.9671, 7.9671])
    ops.mass(344, *[9.5605, 9.5605, 9.5605])
    ops.mass(345, *[9.5605, 9.5605, 9.5605])
    ops.mass(346, *[9.5605, 9.5605, 9.5605])
    ops.mass(347, *[9.5605, 9.5605, 9.5605])
    ops.mass(348, *[7.9671, 7.9671, 7.9671])
    ops.mass(349, *[7.9671, 7.9671, 7.9671])
    ops.mass(350, *[9.5605, 9.5605, 9.5605])
    ops.mass(351, *[9.5605, 9.5605, 9.5605])
    ops.mass(352, *[9.5605, 9.5605, 9.5605])
    ops.mass(353, *[9.5605, 9.5605, 9.5605])
    ops.mass(354, *[7.9671, 7.9671, 7.9671])
    ops.mass(355, *[6.3736, 6.3736, 6.3736])
    ops.mass(356, *[7.9671, 7.9671, 7.9671])
    ops.mass(357, *[7.9671, 7.9671, 7.9671])
    ops.mass(358, *[7.9671, 7.9671, 7.9671])
    ops.mass(359, *[7.9671, 7.9671, 7.9671])
    ops.mass(360, *[6.3736, 6.3736, 6.3736])
    ops.mass(361, *[4.7802, 4.7802, 4.7802])
    ops.mass(362, *[6.3736, 6.3736, 6.3736])
    ops.mass(363, *[6.3736, 6.3736, 6.3736])
    ops.mass(364, *[6.3736, 6.3736, 6.3736])
    ops.mass(365, *[6.3736, 6.3736, 6.3736])
    ops.mass(366, *[4.7802, 4.7802, 4.7802])
    ops.mass(367, *[6.3736, 6.3736, 6.3736])
    ops.mass(368, *[7.9671, 7.9671, 7.9671])
    ops.mass(369, *[7.9671, 7.9671, 7.9671])
    ops.mass(370, *[7.9671, 7.9671, 7.9671])
    ops.mass(371, *[7.9671, 7.9671, 7.9671])
    ops.mass(372, *[6.3736, 6.3736, 6.3736])
    ops.mass(373, *[6.3736, 6.3736, 6.3736])
    ops.mass(374, *[7.9671, 7.9671, 7.9671])
    ops.mass(375, *[7.9671, 7.9671, 7.9671])
    ops.mass(376, *[7.9671, 7.9671, 7.9671])
    ops.mass(377, *[7.9671, 7.9671, 7.9671])
    ops.mass(378, *[6.3736, 6.3736, 6.3736])
    ops.mass(379, *[4.7802, 4.7802, 4.7802])
    ops.mass(380, *[6.3736, 6.3736, 6.3736])
    ops.mass(381, *[6.3736, 6.3736, 6.3736])
    ops.mass(382, *[6.3736, 6.3736, 6.3736])
    ops.mass(383, *[6.3736, 6.3736, 6.3736])
    ops.mass(384, *[4.7802, 4.7802, 4.7802])
