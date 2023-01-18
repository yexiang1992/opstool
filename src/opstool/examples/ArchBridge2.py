# This model is converted from
# http://www.dinochen.com/article.asp?id=179
# by DinoChen


import openseespy.opensees as ops


def ArchBridge2():
    ops.wipe()
    ops.model('basic', '-ndm', 3, '-ndf', 6)
    ops.node(1, 0.0, 0.0, 0.0)
    ops.node(2, 125000.0, 0.0, 0.0)
    ops.node(3, 0.0, 24000.0, 0.0)
    ops.node(4, 125000.0, 24000.0, 0.0)
    ops.node(5, 3000.0, 0.0, 8000.0)
    ops.node(6, 3000.0, 6000.0, 8000.0)
    ops.node(7, 3000.0, 12000.0, 8000.0)
    ops.node(8, 3000.0, 18000.0, 8000.0)
    ops.node(9, 3000.0, 24000.0, 8000.0)
    ops.node(10, 8100.0, 0.0, 8000.0)
    ops.node(11, 8100.0, 6000.0, 8000.0)
    ops.node(12, 8100.0, 12000.0, 8000.0)
    ops.node(13, 8100.0, 18000.0, 8000.0)
    ops.node(14, 8100.0, 24000.0, 8000.0)
    ops.node(15, 14900.0, 0.0, 8000.0)
    ops.node(16, 14900.0, 6000.0, 8000.0)
    ops.node(17, 14900.0, 12000.0, 8000.0)
    ops.node(18, 14900.0, 18000.0, 8000.0)
    ops.node(19, 14900.0, 24000.0, 8000.0)
    ops.node(20, 21700.0, 0.0, 8000.0)
    ops.node(21, 21700.0, 6000.0, 8000.0)
    ops.node(22, 21700.0, 12000.0, 8000.0)
    ops.node(23, 21700.0, 18000.0, 8000.0)
    ops.node(24, 21700.0, 24000.0, 8000.0)
    ops.node(25, 28500.0, 0.0, 8000.0)
    ops.node(26, 28500.0, 6000.0, 8000.0)
    ops.node(27, 28500.0, 12000.0, 8000.0)
    ops.node(28, 28500.0, 18000.0, 8000.0)
    ops.node(29, 28500.0, 24000.0, 8000.0)
    ops.node(30, 35300.0, 0.0, 8000.0)
    ops.node(31, 35300.0, 6000.0, 8000.0)
    ops.node(32, 35300.0, 12000.0, 8000.0)
    ops.node(33, 35300.0, 18000.0, 8000.0)
    ops.node(34, 35300.0, 24000.0, 8000.0)
    ops.node(35, 42100.0, 0.0, 8000.0)
    ops.node(36, 42100.0, 6000.0, 8000.0)
    ops.node(37, 42100.0, 12000.0, 8000.0)
    ops.node(38, 42100.0, 18000.0, 8000.0)
    ops.node(39, 42100.0, 24000.0, 8000.0)
    ops.node(40, 48900.0, 0.0, 8000.0)
    ops.node(41, 48900.0, 6000.0, 8000.0)
    ops.node(42, 48900.0, 12000.0, 8000.0)
    ops.node(43, 48900.0, 18000.0, 8000.0)
    ops.node(44, 48900.0, 24000.0, 8000.0)
    ops.node(45, 55700.0, 0.0, 8000.0)
    ops.node(46, 55700.0, 6000.0, 8000.0)
    ops.node(47, 55700.0, 12000.0, 8000.0)
    ops.node(48, 55700.0, 18000.0, 8000.0)
    ops.node(49, 55700.0, 24000.0, 8000.0)
    ops.node(50, 62500.0, 0.0, 8000.0)
    ops.node(51, 62500.0, 6000.0, 8000.0)
    ops.node(52, 62500.0, 12000.0, 8000.0)
    ops.node(53, 62500.0, 18000.0, 8000.0)
    ops.node(54, 62500.0, 24000.0, 8000.0)
    ops.node(55, 69300.0, 0.0, 8000.0)
    ops.node(56, 69300.0, 6000.0, 8000.0)
    ops.node(57, 69300.0, 12000.0, 8000.0)
    ops.node(58, 69300.0, 18000.0, 8000.0)
    ops.node(59, 69300.0, 24000.0, 8000.0)
    ops.node(60, 76100.0, 0.0, 8000.0)
    ops.node(61, 76100.0, 6000.0, 8000.0)
    ops.node(62, 76100.0, 12000.0, 8000.0)
    ops.node(63, 76100.0, 18000.0, 8000.0)
    ops.node(64, 76100.0, 24000.0, 8000.0)
    ops.node(65, 82900.0, 0.0, 8000.0)
    ops.node(66, 82900.0, 6000.0, 8000.0)
    ops.node(67, 82900.0, 12000.0, 8000.0)
    ops.node(68, 82900.0, 18000.0, 8000.0)
    ops.node(69, 82900.0, 24000.0, 8000.0)
    ops.node(70, 89700.0, 0.0, 8000.0)
    ops.node(71, 89700.0, 6000.0, 8000.0)
    ops.node(72, 89700.0, 12000.0, 8000.0)
    ops.node(73, 89700.0, 18000.0, 8000.0)
    ops.node(74, 89700.0, 24000.0, 8000.0)
    ops.node(75, 96500.0, 0.0, 8000.0)
    ops.node(76, 96500.0, 6000.0, 8000.0)
    ops.node(77, 96500.0, 12000.0, 8000.0)
    ops.node(78, 96500.0, 18000.0, 8000.0)
    ops.node(79, 96500.0, 24000.0, 8000.0)
    ops.node(80, 103300.0, 0.0, 8000.0)
    ops.node(81, 103300.0, 6000.0, 8000.0)
    ops.node(82, 103300.0, 12000.0, 8000.0)
    ops.node(83, 103300.0, 18000.0, 8000.0)
    ops.node(84, 103300.0, 24000.0, 8000.0)
    ops.node(85, 110100.0, 0.0, 8000.0)
    ops.node(86, 110100.0, 6000.0, 8000.0)
    ops.node(87, 110100.0, 12000.0, 8000.0)
    ops.node(88, 110100.0, 18000.0, 8000.0)
    ops.node(89, 110100.0, 24000.0, 8000.0)
    ops.node(90, 116900.0, 0.0, 8000.0)
    ops.node(91, 116900.0, 6000.0, 8000.0)
    ops.node(92, 116900.0, 12000.0, 8000.0)
    ops.node(93, 116900.0, 18000.0, 8000.0)
    ops.node(94, 116900.0, 24000.0, 8000.0)
    ops.node(95, 122000.0, 0.0, 8000.0)
    ops.node(96, 122000.0, 6000.0, 8000.0)
    ops.node(97, 122000.0, 12000.0, 8000.0)
    ops.node(98, 122000.0, 18000.0, 8000.0)
    ops.node(99, 122000.0, 24000.0, 8000.0)
    ops.node(100, 3000.0, 0.0, 9050.0)
    ops.node(101, 3000.0, 6000.0, 9050.0)
    ops.node(102, 3000.0, 12000.0, 9050.0)
    ops.node(103, 3000.0, 18000.0, 9050.0)
    ops.node(104, 3000.0, 24000.0, 9050.0)
    ops.node(105, 8100.0, 0.0, 9050.0)
    ops.node(106, 8100.0, 6000.0, 9050.0)
    ops.node(107, 8100.0, 12000.0, 9050.0)
    ops.node(108, 8100.0, 18000.0, 9050.0)
    ops.node(109, 8100.0, 24000.0, 9050.0)
    ops.node(110, 14900.0, 0.0, 9050.0)
    ops.node(111, 14900.0, 6000.0, 9050.0)
    ops.node(112, 14900.0, 12000.0, 9050.0)
    ops.node(113, 14900.0, 18000.0, 9050.0)
    ops.node(114, 14900.0, 24000.0, 9050.0)
    ops.node(115, 21700.0, 0.0, 9050.0)
    ops.node(116, 21700.0, 6000.0, 9050.0)
    ops.node(117, 21700.0, 12000.0, 9050.0)
    ops.node(118, 21700.0, 18000.0, 9050.0)
    ops.node(119, 21700.0, 24000.0, 9050.0)
    ops.node(120, 28500.0, 0.0, 9050.0)
    ops.node(121, 28500.0, 6000.0, 9050.0)
    ops.node(122, 28500.0, 12000.0, 9050.0)
    ops.node(123, 28500.0, 18000.0, 9050.0)
    ops.node(124, 28500.0, 24000.0, 9050.0)
    ops.node(125, 35300.0, 0.0, 9050.0)
    ops.node(126, 35300.0, 6000.0, 9050.0)
    ops.node(127, 35300.0, 12000.0, 9050.0)
    ops.node(128, 35300.0, 18000.0, 9050.0)
    ops.node(129, 35300.0, 24000.0, 9050.0)
    ops.node(130, 42100.0, 0.0, 9050.0)
    ops.node(131, 42100.0, 6000.0, 9050.0)
    ops.node(132, 42100.0, 12000.0, 9050.0)
    ops.node(133, 42100.0, 18000.0, 9050.0)
    ops.node(134, 42100.0, 24000.0, 9050.0)
    ops.node(135, 48900.0, 0.0, 9050.0)
    ops.node(136, 48900.0, 6000.0, 9050.0)
    ops.node(137, 48900.0, 12000.0, 9050.0)
    ops.node(138, 48900.0, 18000.0, 9050.0)
    ops.node(139, 48900.0, 24000.0, 9050.0)
    ops.node(140, 55700.0, 0.0, 9050.0)
    ops.node(141, 55700.0, 6000.0, 9050.0)
    ops.node(142, 55700.0, 12000.0, 9050.0)
    ops.node(143, 55700.0, 18000.0, 9050.0)
    ops.node(144, 55700.0, 24000.0, 9050.0)
    ops.node(145, 62500.0, 0.0, 9050.0)
    ops.node(146, 62500.0, 6000.0, 9050.0)
    ops.node(147, 62500.0, 12000.0, 9050.0)
    ops.node(148, 62500.0, 18000.0, 9050.0)
    ops.node(149, 62500.0, 24000.0, 9050.0)
    ops.node(150, 69300.0, 0.0, 9050.0)
    ops.node(151, 69300.0, 6000.0, 9050.0)
    ops.node(152, 69300.0, 12000.0, 9050.0)
    ops.node(153, 69300.0, 18000.0, 9050.0)
    ops.node(154, 69300.0, 24000.0, 9050.0)
    ops.node(155, 76100.0, 0.0, 9050.0)
    ops.node(156, 76100.0, 6000.0, 9050.0)
    ops.node(157, 76100.0, 12000.0, 9050.0)
    ops.node(158, 76100.0, 18000.0, 9050.0)
    ops.node(159, 76100.0, 24000.0, 9050.0)
    ops.node(160, 82900.0, 0.0, 9050.0)
    ops.node(161, 82900.0, 6000.0, 9050.0)
    ops.node(162, 82900.0, 12000.0, 9050.0)
    ops.node(163, 82900.0, 18000.0, 9050.0)
    ops.node(164, 82900.0, 24000.0, 9050.0)
    ops.node(165, 89700.0, 0.0, 9050.0)
    ops.node(166, 89700.0, 6000.0, 9050.0)
    ops.node(167, 89700.0, 12000.0, 9050.0)
    ops.node(168, 89700.0, 18000.0, 9050.0)
    ops.node(169, 89700.0, 24000.0, 9050.0)
    ops.node(170, 96500.0, 0.0, 9050.0)
    ops.node(171, 96500.0, 6000.0, 9050.0)
    ops.node(172, 96500.0, 12000.0, 9050.0)
    ops.node(173, 96500.0, 18000.0, 9050.0)
    ops.node(174, 96500.0, 24000.0, 9050.0)
    ops.node(175, 103300.0, 0.0, 9050.0)
    ops.node(176, 103300.0, 6000.0, 9050.0)
    ops.node(177, 103300.0, 12000.0, 9050.0)
    ops.node(178, 103300.0, 18000.0, 9050.0)
    ops.node(179, 103300.0, 24000.0, 9050.0)
    ops.node(180, 110100.0, 0.0, 9050.0)
    ops.node(181, 110100.0, 6000.0, 9050.0)
    ops.node(182, 110100.0, 12000.0, 9050.0)
    ops.node(183, 110100.0, 18000.0, 9050.0)
    ops.node(184, 110100.0, 24000.0, 9050.0)
    ops.node(185, 116900.0, 0.0, 9050.0)
    ops.node(186, 116900.0, 6000.0, 9050.0)
    ops.node(187, 116900.0, 12000.0, 9050.0)
    ops.node(188, 116900.0, 18000.0, 9050.0)
    ops.node(189, 116900.0, 24000.0, 9050.0)
    ops.node(190, 122000.0, 24000.0, 9050.0)
    ops.node(191, 122000.0, 18000.0, 9050.0)
    ops.node(192, 122000.0, 12000.0, 9050.0)
    ops.node(193, 122000.0, 6000.0, 9050.0)
    ops.node(194, 122000.0, 0.0, 9050.0)
    ops.node(195, 8100.0, 0.0, 13640.0)
    ops.node(196, 14900.0, 0.0, 18100.0)
    ops.node(197, 21700.0, 0.0, 21950.0)
    ops.node(198, 28500.0, 0.0, 25190.0)
    ops.node(199, 35300.0, 0.0, 27830.0)
    ops.node(200, 42100.0, 0.0, 29880.0)
    ops.node(201, 48900.0, 0.0, 31330.0)
    ops.node(202, 55700.0, 0.0, 32210.0)
    ops.node(203, 62500.0, 0.0, 32500.0)
    ops.node(204, 116900.0, 0.0, 13640.0)
    ops.node(205, 110100.0, 0.0, 18100.0)
    ops.node(206, 103300.0, 0.0, 21950.0)
    ops.node(207, 96500.0, 0.0, 25190.0)
    ops.node(208, 89700.0, 0.0, 27830.0)
    ops.node(209, 82900.0, 0.0, 29880.0)
    ops.node(210, 76100.0, 0.0, 31330.0)
    ops.node(211, 69300.0, 0.0, 32210.0)
    ops.node(212, 0.0, 0.0, 7425.0)
    ops.node(213, 125000.0, 0.0, 7425.0)
    ops.node(214, 8100.0, 24000.0, 13640.0)
    ops.node(215, 14900.0, 24000.0, 18100.0)
    ops.node(216, 21700.0, 24000.0, 21950.0)
    ops.node(217, 28500.0, 24000.0, 25190.0)
    ops.node(218, 35300.0, 24000.0, 27830.0)
    ops.node(219, 42100.0, 24000.0, 29880.0)
    ops.node(220, 48900.0, 24000.0, 31330.0)
    ops.node(221, 55700.0, 24000.0, 32210.0)
    ops.node(222, 62500.0, 24000.0, 32500.0)
    ops.node(223, 116900.0, 24000.0, 13640.0)
    ops.node(224, 110100.0, 24000.0, 18100.0)
    ops.node(225, 103300.0, 24000.0, 21950.0)
    ops.node(226, 96500.0, 24000.0, 25190.0)
    ops.node(227, 89700.0, 24000.0, 27830.0)
    ops.node(228, 82900.0, 24000.0, 29880.0)
    ops.node(229, 76100.0, 24000.0, 31330.0)
    ops.node(230, 69300.0, 24000.0, 32210.0)
    ops.node(231, 0.0, 24000.0, 7425.0)
    ops.node(232, 125000.0, 24000.0, 7425.0)
    ops.node(233, 0.0, 6000.0, 7425.0)
    ops.node(234, 125000.0, 6000.0, 7425.0)
    ops.node(235, 0.0, 12000.0, 7425.0)
    ops.node(236, 125000.0, 12000.0, 7425.0)
    ops.node(237, 0.0, 18000.0, 7425.0)
    ops.node(238, 125000.0, 18000.0, 7425.0)
    ops.node(239, 28500.0, 12000.0, 25190.0)
    ops.node(240, 62500.0, 12000.0, 32500.0)
    ops.node(241, 96500.0, 12000.0, 25190.0)
    ops.mass(1, 113.6, 113.6, 113.6, 0.0, 0.0, 0.0)
    ops.mass(2, 113.6, 113.6, 113.6, 0.0, 0.0, 0.0)
    ops.mass(3, 113.6, 113.6, 113.6, 0.0, 0.0, 0.0)
    ops.mass(4, 113.6, 113.6, 113.6, 0.0, 0.0, 0.0)
    ops.mass(5, 16.12, 16.12, 16.12, 0.0, 0.0, 0.0)
    ops.mass(6, 27.21, 27.21, 27.21, 0.0, 0.0, 0.0)
    ops.mass(7, 27.21, 27.21, 27.21, 0.0, 0.0, 0.0)
    ops.mass(8, 27.21, 27.21, 27.21, 0.0, 0.0, 0.0)
    ops.mass(9, 16.12, 16.12, 16.12, 0.0, 0.0, 0.0)
    ops.mass(10, 18.29, 18.29, 18.29, 0.0, 0.0, 0.0)
    ops.mass(11, 29.38, 29.38, 29.38, 0.0, 0.0, 0.0)
    ops.mass(12, 29.38, 29.38, 29.38, 0.0, 0.0, 0.0)
    ops.mass(13, 29.38, 29.38, 29.38, 0.0, 0.0, 0.0)
    ops.mass(14, 18.29, 18.29, 18.29, 0.0, 0.0, 0.0)
    ops.mass(15, 19.33, 19.33, 19.33, 0.0, 0.0, 0.0)
    ops.mass(16, 30.42, 30.42, 30.42, 0.0, 0.0, 0.0)
    ops.mass(17, 30.42, 30.42, 30.42, 0.0, 0.0, 0.0)
    ops.mass(18, 30.42, 30.42, 30.42, 0.0, 0.0, 0.0)
    ops.mass(19, 19.33, 19.33, 19.33, 0.0, 0.0, 0.0)
    ops.mass(20, 19.33, 19.33, 19.33, 0.0, 0.0, 0.0)
    ops.mass(21, 30.42, 30.42, 30.42, 0.0, 0.0, 0.0)
    ops.mass(22, 30.42, 30.42, 30.42, 0.0, 0.0, 0.0)
    ops.mass(23, 30.42, 30.42, 30.42, 0.0, 0.0, 0.0)
    ops.mass(24, 19.33, 19.33, 19.33, 0.0, 0.0, 0.0)
    ops.mass(25, 19.33, 19.33, 19.33, 0.0, 0.0, 0.0)
    ops.mass(26, 30.42, 30.42, 30.42, 0.0, 0.0, 0.0)
    ops.mass(27, 30.42, 30.42, 30.42, 0.0, 0.0, 0.0)
    ops.mass(28, 30.42, 30.42, 30.42, 0.0, 0.0, 0.0)
    ops.mass(29, 19.33, 19.33, 19.33, 0.0, 0.0, 0.0)
    ops.mass(30, 19.33, 19.33, 19.33, 0.0, 0.0, 0.0)
    ops.mass(31, 30.42, 30.42, 30.42, 0.0, 0.0, 0.0)
    ops.mass(32, 30.42, 30.42, 30.42, 0.0, 0.0, 0.0)
    ops.mass(33, 30.42, 30.42, 30.42, 0.0, 0.0, 0.0)
    ops.mass(34, 19.33, 19.33, 19.33, 0.0, 0.0, 0.0)
    ops.mass(35, 19.33, 19.33, 19.33, 0.0, 0.0, 0.0)
    ops.mass(36, 30.42, 30.42, 30.42, 0.0, 0.0, 0.0)
    ops.mass(37, 30.42, 30.42, 30.42, 0.0, 0.0, 0.0)
    ops.mass(38, 30.42, 30.42, 30.42, 0.0, 0.0, 0.0)
    ops.mass(39, 19.33, 19.33, 19.33, 0.0, 0.0, 0.0)
    ops.mass(40, 19.33, 19.33, 19.33, 0.0, 0.0, 0.0)
    ops.mass(41, 30.42, 30.42, 30.42, 0.0, 0.0, 0.0)
    ops.mass(42, 30.42, 30.42, 30.42, 0.0, 0.0, 0.0)
    ops.mass(43, 30.42, 30.42, 30.42, 0.0, 0.0, 0.0)
    ops.mass(44, 19.33, 19.33, 19.33, 0.0, 0.0, 0.0)
    ops.mass(45, 19.33, 19.33, 19.33, 0.0, 0.0, 0.0)
    ops.mass(46, 30.42, 30.42, 30.42, 0.0, 0.0, 0.0)
    ops.mass(47, 30.42, 30.42, 30.42, 0.0, 0.0, 0.0)
    ops.mass(48, 30.42, 30.42, 30.42, 0.0, 0.0, 0.0)
    ops.mass(49, 19.33, 19.33, 19.33, 0.0, 0.0, 0.0)
    ops.mass(50, 19.33, 19.33, 19.33, 0.0, 0.0, 0.0)
    ops.mass(51, 30.42, 30.42, 30.42, 0.0, 0.0, 0.0)
    ops.mass(52, 30.42, 30.42, 30.42, 0.0, 0.0, 0.0)
    ops.mass(53, 30.42, 30.42, 30.42, 0.0, 0.0, 0.0)
    ops.mass(54, 19.33, 19.33, 19.33, 0.0, 0.0, 0.0)
    ops.mass(55, 19.33, 19.33, 19.33, 0.0, 0.0, 0.0)
    ops.mass(56, 30.42, 30.42, 30.42, 0.0, 0.0, 0.0)
    ops.mass(57, 30.42, 30.42, 30.42, 0.0, 0.0, 0.0)
    ops.mass(58, 30.42, 30.42, 30.42, 0.0, 0.0, 0.0)
    ops.mass(59, 19.33, 19.33, 19.33, 0.0, 0.0, 0.0)
    ops.mass(60, 19.33, 19.33, 19.33, 0.0, 0.0, 0.0)
    ops.mass(61, 30.42, 30.42, 30.42, 0.0, 0.0, 0.0)
    ops.mass(62, 30.42, 30.42, 30.42, 0.0, 0.0, 0.0)
    ops.mass(63, 30.42, 30.42, 30.42, 0.0, 0.0, 0.0)
    ops.mass(64, 19.33, 19.33, 19.33, 0.0, 0.0, 0.0)
    ops.mass(65, 19.33, 19.33, 19.33, 0.0, 0.0, 0.0)
    ops.mass(66, 30.42, 30.42, 30.42, 0.0, 0.0, 0.0)
    ops.mass(67, 30.42, 30.42, 30.42, 0.0, 0.0, 0.0)
    ops.mass(68, 30.42, 30.42, 30.42, 0.0, 0.0, 0.0)
    ops.mass(69, 19.33, 19.33, 19.33, 0.0, 0.0, 0.0)
    ops.mass(70, 19.33, 19.33, 19.33, 0.0, 0.0, 0.0)
    ops.mass(71, 30.42, 30.42, 30.42, 0.0, 0.0, 0.0)
    ops.mass(72, 30.42, 30.42, 30.42, 0.0, 0.0, 0.0)
    ops.mass(73, 30.42, 30.42, 30.42, 0.0, 0.0, 0.0)
    ops.mass(74, 19.33, 19.33, 19.33, 0.0, 0.0, 0.0)
    ops.mass(75, 19.33, 19.33, 19.33, 0.0, 0.0, 0.0)
    ops.mass(76, 30.42, 30.42, 30.42, 0.0, 0.0, 0.0)
    ops.mass(77, 30.42, 30.42, 30.42, 0.0, 0.0, 0.0)
    ops.mass(78, 30.42, 30.42, 30.42, 0.0, 0.0, 0.0)
    ops.mass(79, 19.33, 19.33, 19.33, 0.0, 0.0, 0.0)
    ops.mass(80, 19.33, 19.33, 19.33, 0.0, 0.0, 0.0)
    ops.mass(81, 30.42, 30.42, 30.42, 0.0, 0.0, 0.0)
    ops.mass(82, 30.42, 30.42, 30.42, 0.0, 0.0, 0.0)
    ops.mass(83, 30.42, 30.42, 30.42, 0.0, 0.0, 0.0)
    ops.mass(84, 19.33, 19.33, 19.33, 0.0, 0.0, 0.0)
    ops.mass(85, 19.33, 19.33, 19.33, 0.0, 0.0, 0.0)
    ops.mass(86, 30.42, 30.42, 30.42, 0.0, 0.0, 0.0)
    ops.mass(87, 30.42, 30.42, 30.42, 0.0, 0.0, 0.0)
    ops.mass(88, 30.42, 30.42, 30.42, 0.0, 0.0, 0.0)
    ops.mass(89, 19.33, 19.33, 19.33, 0.0, 0.0, 0.0)
    ops.mass(90, 18.29, 18.29, 18.29, 0.0, 0.0, 0.0)
    ops.mass(91, 29.38, 29.38, 29.38, 0.0, 0.0, 0.0)
    ops.mass(92, 29.38, 29.38, 29.38, 0.0, 0.0, 0.0)
    ops.mass(93, 29.38, 29.38, 29.38, 0.0, 0.0, 0.0)
    ops.mass(94, 18.29, 18.29, 18.29, 0.0, 0.0, 0.0)
    ops.mass(95, 16.12, 16.12, 16.12, 0.0, 0.0, 0.0)
    ops.mass(96, 27.21, 27.21, 27.21, 0.0, 0.0, 0.0)
    ops.mass(97, 27.21, 27.21, 27.21, 0.0, 0.0, 0.0)
    ops.mass(98, 27.21, 27.21, 27.21, 0.0, 0.0, 0.0)
    ops.mass(99, 16.12, 16.12, 16.12, 0.0, 0.0, 0.0)
    ops.mass(100, 13.04, 13.04, 13.04, 0.0, 0.0, 0.0)
    ops.mass(101, 25.91, 25.91, 25.91, 0.0, 0.0, 0.0)
    ops.mass(102, 25.91, 25.91, 25.91, 0.0, 0.0, 0.0)
    ops.mass(103, 25.91, 25.91, 25.91, 0.0, 0.0, 0.0)
    ops.mass(104, 13.04, 13.04, 13.04, 0.0, 0.0, 0.0)
    ops.mass(105, 30.27, 30.27, 30.27, 0.0, 0.0, 0.0)
    ops.mass(106, 60.23, 60.23, 60.23, 0.0, 0.0, 0.0)
    ops.mass(107, 60.23, 60.23, 60.23, 0.0, 0.0, 0.0)
    ops.mass(108, 60.23, 60.23, 60.23, 0.0, 0.0, 0.0)
    ops.mass(109, 30.27, 30.27, 30.27, 0.0, 0.0, 0.0)
    ops.mass(110, 34.64, 34.64, 34.64, 0.0, 0.0, 0.0)
    ops.mass(111, 68.81, 68.81, 68.81, 0.0, 0.0, 0.0)
    ops.mass(112, 68.81, 68.81, 68.81, 0.0, 0.0, 0.0)
    ops.mass(113, 68.81, 68.81, 68.81, 0.0, 0.0, 0.0)
    ops.mass(114, 34.64, 34.64, 34.64, 0.0, 0.0, 0.0)
    ops.mass(115, 34.7, 34.7, 34.7, 0.0, 0.0, 0.0)
    ops.mass(116, 68.81, 68.81, 68.81, 0.0, 0.0, 0.0)
    ops.mass(117, 68.81, 68.81, 68.81, 0.0, 0.0, 0.0)
    ops.mass(118, 68.81, 68.81, 68.81, 0.0, 0.0, 0.0)
    ops.mass(119, 34.7, 34.7, 34.7, 0.0, 0.0, 0.0)
    ops.mass(120, 34.75, 34.75, 34.75, 0.0, 0.0, 0.0)
    ops.mass(121, 68.81, 68.81, 68.81, 0.0, 0.0, 0.0)
    ops.mass(122, 68.81, 68.81, 68.81, 0.0, 0.0, 0.0)
    ops.mass(123, 68.81, 68.81, 68.81, 0.0, 0.0, 0.0)
    ops.mass(124, 34.75, 34.75, 34.75, 0.0, 0.0, 0.0)
    ops.mass(125, 34.8, 34.8, 34.8, 0.0, 0.0, 0.0)
    ops.mass(126, 68.81, 68.81, 68.81, 0.0, 0.0, 0.0)
    ops.mass(127, 68.81, 68.81, 68.81, 0.0, 0.0, 0.0)
    ops.mass(128, 68.81, 68.81, 68.81, 0.0, 0.0, 0.0)
    ops.mass(129, 34.8, 34.8, 34.8, 0.0, 0.0, 0.0)
    ops.mass(130, 34.83, 34.83, 34.83, 0.0, 0.0, 0.0)
    ops.mass(131, 68.81, 68.81, 68.81, 0.0, 0.0, 0.0)
    ops.mass(132, 68.81, 68.81, 68.81, 0.0, 0.0, 0.0)
    ops.mass(133, 68.81, 68.81, 68.81, 0.0, 0.0, 0.0)
    ops.mass(134, 34.83, 34.83, 34.83, 0.0, 0.0, 0.0)
    ops.mass(135, 34.85, 34.85, 34.85, 0.0, 0.0, 0.0)
    ops.mass(136, 68.81, 68.81, 68.81, 0.0, 0.0, 0.0)
    ops.mass(137, 68.81, 68.81, 68.81, 0.0, 0.0, 0.0)
    ops.mass(138, 68.81, 68.81, 68.81, 0.0, 0.0, 0.0)
    ops.mass(139, 34.85, 34.85, 34.85, 0.0, 0.0, 0.0)
    ops.mass(140, 34.87, 34.87, 34.87, 0.0, 0.0, 0.0)
    ops.mass(141, 68.81, 68.81, 68.81, 0.0, 0.0, 0.0)
    ops.mass(142, 68.81, 68.81, 68.81, 0.0, 0.0, 0.0)
    ops.mass(143, 68.81, 68.81, 68.81, 0.0, 0.0, 0.0)
    ops.mass(144, 34.87, 34.87, 34.87, 0.0, 0.0, 0.0)
    ops.mass(145, 34.87, 34.87, 34.87, 0.0, 0.0, 0.0)
    ops.mass(146, 68.81, 68.81, 68.81, 0.0, 0.0, 0.0)
    ops.mass(147, 68.81, 68.81, 68.81, 0.0, 0.0, 0.0)
    ops.mass(148, 68.81, 68.81, 68.81, 0.0, 0.0, 0.0)
    ops.mass(149, 34.87, 34.87, 34.87, 0.0, 0.0, 0.0)
    ops.mass(150, 34.87, 34.87, 34.87, 0.0, 0.0, 0.0)
    ops.mass(151, 68.81, 68.81, 68.81, 0.0, 0.0, 0.0)
    ops.mass(152, 68.81, 68.81, 68.81, 0.0, 0.0, 0.0)
    ops.mass(153, 68.81, 68.81, 68.81, 0.0, 0.0, 0.0)
    ops.mass(154, 34.87, 34.87, 34.87, 0.0, 0.0, 0.0)
    ops.mass(155, 34.85, 34.85, 34.85, 0.0, 0.0, 0.0)
    ops.mass(156, 68.81, 68.81, 68.81, 0.0, 0.0, 0.0)
    ops.mass(157, 68.81, 68.81, 68.81, 0.0, 0.0, 0.0)
    ops.mass(158, 68.81, 68.81, 68.81, 0.0, 0.0, 0.0)
    ops.mass(159, 34.85, 34.85, 34.85, 0.0, 0.0, 0.0)
    ops.mass(160, 34.83, 34.83, 34.83, 0.0, 0.0, 0.0)
    ops.mass(161, 68.81, 68.81, 68.81, 0.0, 0.0, 0.0)
    ops.mass(162, 68.81, 68.81, 68.81, 0.0, 0.0, 0.0)
    ops.mass(163, 68.81, 68.81, 68.81, 0.0, 0.0, 0.0)
    ops.mass(164, 34.83, 34.83, 34.83, 0.0, 0.0, 0.0)
    ops.mass(165, 34.8, 34.8, 34.8, 0.0, 0.0, 0.0)
    ops.mass(166, 68.81, 68.81, 68.81, 0.0, 0.0, 0.0)
    ops.mass(167, 68.81, 68.81, 68.81, 0.0, 0.0, 0.0)
    ops.mass(168, 68.81, 68.81, 68.81, 0.0, 0.0, 0.0)
    ops.mass(169, 34.8, 34.8, 34.8, 0.0, 0.0, 0.0)
    ops.mass(170, 34.75, 34.75, 34.75, 0.0, 0.0, 0.0)
    ops.mass(171, 68.81, 68.81, 68.81, 0.0, 0.0, 0.0)
    ops.mass(172, 68.81, 68.81, 68.81, 0.0, 0.0, 0.0)
    ops.mass(173, 68.81, 68.81, 68.81, 0.0, 0.0, 0.0)
    ops.mass(174, 34.75, 34.75, 34.75, 0.0, 0.0, 0.0)
    ops.mass(175, 34.7, 34.7, 34.7, 0.0, 0.0, 0.0)
    ops.mass(176, 68.81, 68.81, 68.81, 0.0, 0.0, 0.0)
    ops.mass(177, 68.81, 68.81, 68.81, 0.0, 0.0, 0.0)
    ops.mass(178, 68.81, 68.81, 68.81, 0.0, 0.0, 0.0)
    ops.mass(179, 34.7, 34.7, 34.7, 0.0, 0.0, 0.0)
    ops.mass(180, 34.64, 34.64, 34.64, 0.0, 0.0, 0.0)
    ops.mass(181, 68.81, 68.81, 68.81, 0.0, 0.0, 0.0)
    ops.mass(182, 68.81, 68.81, 68.81, 0.0, 0.0, 0.0)
    ops.mass(183, 68.81, 68.81, 68.81, 0.0, 0.0, 0.0)
    ops.mass(184, 34.64, 34.64, 34.64, 0.0, 0.0, 0.0)
    ops.mass(185, 30.27, 30.27, 30.27, 0.0, 0.0, 0.0)
    ops.mass(186, 60.23, 60.23, 60.23, 0.0, 0.0, 0.0)
    ops.mass(187, 60.23, 60.23, 60.23, 0.0, 0.0, 0.0)
    ops.mass(188, 60.23, 60.23, 60.23, 0.0, 0.0, 0.0)
    ops.mass(189, 30.27, 30.27, 30.27, 0.0, 0.0, 0.0)
    ops.mass(190, 13.04, 13.04, 13.04, 0.0, 0.0, 0.0)
    ops.mass(191, 25.91, 25.91, 25.91, 0.0, 0.0, 0.0)
    ops.mass(192, 25.91, 25.91, 25.91, 0.0, 0.0, 0.0)
    ops.mass(193, 25.91, 25.91, 25.91, 0.0, 0.0, 0.0)
    ops.mass(194, 13.04, 13.04, 13.04, 0.0, 0.0, 0.0)
    ops.mass(195, 229.2, 229.2, 229.2, 0.0, 0.0, 0.0)
    ops.mass(196, 199.4, 199.4, 199.4, 0.0, 0.0, 0.0)
    ops.mass(197, 248.6, 248.6, 248.6, 0.0, 0.0, 0.0)
    ops.mass(198, 233.2, 233.2, 233.2, 0.0, 0.0, 0.0)
    ops.mass(199, 180.2, 180.2, 180.2, 0.0, 0.0, 0.0)
    ops.mass(200, 175.9, 175.9, 175.9, 0.0, 0.0, 0.0)
    ops.mass(201, 172.9, 172.9, 172.9, 0.0, 0.0, 0.0)
    ops.mass(202, 226.2, 226.2, 226.2, 0.0, 0.0, 0.0)
    ops.mass(203, 218.1, 218.1, 218.1, 0.0, 0.0, 0.0)
    ops.mass(204, 229.2, 229.2, 229.2, 0.0, 0.0, 0.0)
    ops.mass(205, 199.4, 199.4, 199.4, 0.0, 0.0, 0.0)
    ops.mass(206, 248.6, 248.6, 248.6, 0.0, 0.0, 0.0)
    ops.mass(207, 233.2, 233.2, 233.2, 0.0, 0.0, 0.0)
    ops.mass(208, 180.2, 180.2, 180.2, 0.0, 0.0, 0.0)
    ops.mass(209, 175.9, 175.9, 175.9, 0.0, 0.0, 0.0)
    ops.mass(210, 172.9, 172.9, 172.9, 0.0, 0.0, 0.0)
    ops.mass(211, 226.2, 226.2, 226.2, 0.0, 0.0, 0.0)
    ops.mass(212, 339.1, 339.1, 339.1, 0.0, 0.0, 0.0)
    ops.mass(213, 339.1, 339.1, 339.1, 0.0, 0.0, 0.0)
    ops.mass(214, 229.2, 229.2, 229.2, 0.0, 0.0, 0.0)
    ops.mass(215, 199.4, 199.4, 199.4, 0.0, 0.0, 0.0)
    ops.mass(216, 248.6, 248.6, 248.6, 0.0, 0.0, 0.0)
    ops.mass(217, 233.2, 233.2, 233.2, 0.0, 0.0, 0.0)
    ops.mass(218, 180.2, 180.2, 180.2, 0.0, 0.0, 0.0)
    ops.mass(219, 175.9, 175.9, 175.9, 0.0, 0.0, 0.0)
    ops.mass(220, 172.9, 172.9, 172.9, 0.0, 0.0, 0.0)
    ops.mass(221, 226.2, 226.2, 226.2, 0.0, 0.0, 0.0)
    ops.mass(222, 218.1, 218.1, 218.1, 0.0, 0.0, 0.0)
    ops.mass(223, 229.2, 229.2, 229.2, 0.0, 0.0, 0.0)
    ops.mass(224, 199.4, 199.4, 199.4, 0.0, 0.0, 0.0)
    ops.mass(225, 248.6, 248.6, 248.6, 0.0, 0.0, 0.0)
    ops.mass(226, 233.2, 233.2, 233.2, 0.0, 0.0, 0.0)
    ops.mass(227, 180.2, 180.2, 180.2, 0.0, 0.0, 0.0)
    ops.mass(228, 175.9, 175.9, 175.9, 0.0, 0.0, 0.0)
    ops.mass(229, 172.9, 172.9, 172.9, 0.0, 0.0, 0.0)
    ops.mass(230, 226.2, 226.2, 226.2, 0.0, 0.0, 0.0)
    ops.mass(231, 339.1, 339.1, 339.1, 0.0, 0.0, 0.0)
    ops.mass(232, 339.1, 339.1, 339.1, 0.0, 0.0, 0.0)
    ops.mass(233, 226.0, 226.0, 226.0, 0.0, 0.0, 0.0)
    ops.mass(234, 226.0, 226.0, 226.0, 0.0, 0.0, 0.0)
    ops.mass(235, 258.1, 258.1, 258.1, 0.0, 0.0, 0.0)
    ops.mass(236, 258.1, 258.1, 258.1, 0.0, 0.0, 0.0)
    ops.mass(237, 226.0, 226.0, 226.0, 0.0, 0.0, 0.0)
    ops.mass(238, 226.0, 226.0, 226.0, 0.0, 0.0, 0.0)
    ops.mass(239, 208.7, 208.7, 208.7, 0.0, 0.0, 0.0)
    ops.mass(240, 316.0, 316.0, 316.0, 0.0, 0.0, 0.0)
    ops.mass(241, 208.7, 208.7, 208.7, 0.0, 0.0, 0.0)
    ops.fix(1, 1, 1, 1, 1, 1, 1)
    ops.fix(2, 1, 1, 1, 1, 1, 1)
    ops.fix(3, 1, 1, 1, 1, 1, 1)
    ops.fix(4, 1, 1, 1, 1, 1, 1)
    ops.uniaxialMaterial('Elastic', 1, 206000.0)
    ops.uniaxialMaterial('Elastic', 2, 26000.0)
    ops.uniaxialMaterial('Elastic', 3, 199900.0)
    ops.nDMaterial('ElasticIsotropic', 4, 26000, 0.2)
    ops.nDMaterial('PlateFiber', 601, 4)
    ops.section('PlateFiber', 701, 601, 260.0)
    ops.geomTransf('Linear', 1, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 2, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 3, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 4, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 5, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 6, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 7, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 8, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 9, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 10, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 11, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 12, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 13, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 14, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 15, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 16, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 17, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 18, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 19, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 20, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 21, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 22, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 23, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 24, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 25, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 26, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 27, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 28, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 29, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 30, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 31, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 32, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 33, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 34, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 35, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 36, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 37, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 38, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 39, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 40, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 41, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 42, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 43, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 44, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 45, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 46, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 47, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 48, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 49, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 50, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 51, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 52, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 53, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 54, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 55, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 56, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 57, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 58, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 59, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 60, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 61, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 62, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 63, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 64, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 65, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 66, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 67, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 68, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 69, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 70, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 71, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 72, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 73, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 74, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 75, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 76, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 77, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 78, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 79, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 80, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 81, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 82, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 83, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 84, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 85, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 86, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 87, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 88, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 89, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 90, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 91, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 92, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 93, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 94, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 95, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 96, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 97, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 98, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 99, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 100, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 101, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 102, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 103, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 104, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 105, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 106, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 107, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 108, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 109, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 110, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 111, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 112, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 113, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 114, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 115, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 116, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 117, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 118, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 119, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 120, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 121, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 122, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 123, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 124, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 125, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 126, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 127, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 128, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 129, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 130, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 131, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 132, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 133, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 134, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 135, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 136, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 137, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 138, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 139, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 140, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 141, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 142, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 143, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 144, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 145, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 146, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 147, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 148, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 149, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 150, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 151, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 152, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 153, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 154, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 155, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 156, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 157, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 158, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 159, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 160, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 161, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 162, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 163, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 164, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 165, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 166, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 167, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 168, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 169, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 170, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 171, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 172, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 173, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 174, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 175, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 176, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 177, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 178, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 179, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 180, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 181, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 182, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 183, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 184, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 185, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 186, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 187, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 188, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 189, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 190, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 191, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 192, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 193, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 194, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 195, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 196, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 197, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 198, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 199, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 200, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 201, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 202, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 203, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 204, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 205, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 206, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 207, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 208, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 209, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 210, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 211, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 212, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 213, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 214, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 215, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 216, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 217, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 218, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 219, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 220, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 221, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 222, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 223, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 224, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 225, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 226, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 227, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 228, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 229, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 230, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 231, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 232, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 233, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 234, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 235, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 236, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 237, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 238, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 239, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 240, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 241, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 242, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 243, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 244, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 245, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 246, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 247, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 248, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 249, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 250, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 251, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 252, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 253, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 254, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 255, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 256, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 257, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 258, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 259, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 260, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 261, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 262, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 263, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 264, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 265, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 266, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 267, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 268, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 269, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 270, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 271, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 272, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 273, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 274, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 275, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 276, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 277, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 278, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 279, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 280, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 281, -0.188, 0.0, 0.982)
    ops.geomTransf('Linear', 282, 0.188, 0.0, 0.982)
    ops.geomTransf('Linear', 283, -0.609, 0.0, 0.793)
    ops.geomTransf('Linear', 284, -0.548, 0.0, 0.836)
    ops.geomTransf('Linear', 285, -0.493, 0.0, 0.87)
    ops.geomTransf('Linear', 286, -0.43, 0.0, 0.903)
    ops.geomTransf('Linear', 287, -0.362, 0.0, 0.932)
    ops.geomTransf('Linear', 288, -0.289, 0.0, 0.957)
    ops.geomTransf('Linear', 289, -0.209, 0.0, 0.978)
    ops.geomTransf('Linear', 290, -0.128, 0.0, 0.992)
    ops.geomTransf('Linear', 291, -0.043, 0.0, 0.999)
    ops.geomTransf('Linear', 292, 0.609, 0.0, 0.793)
    ops.geomTransf('Linear', 293, 0.548, 0.0, 0.836)
    ops.geomTransf('Linear', 294, 0.493, 0.0, 0.87)
    ops.geomTransf('Linear', 295, 0.43, 0.0, 0.903)
    ops.geomTransf('Linear', 296, 0.362, 0.0, 0.932)
    ops.geomTransf('Linear', 297, 0.289, 0.0, 0.957)
    ops.geomTransf('Linear', 298, 0.209, 0.0, 0.978)
    ops.geomTransf('Linear', 299, 0.128, 0.0, 0.992)
    ops.geomTransf('Linear', 300, 0.043, 0.0, 0.999)
    ops.geomTransf('Linear', 301, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 302, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 303, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 304, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 305, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 306, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 307, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 308, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 309, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 310, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 311, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 312, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 313, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 314, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 315, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 316, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 317, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 318, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 319, 1.0, 0.0, 0.0)
    ops.geomTransf('Linear', 320, -0.188, 0.0, 0.982)
    ops.geomTransf('Linear', 321, 0.188, 0.0, 0.982)
    ops.geomTransf('Linear', 322, -0.609, 0.0, 0.793)
    ops.geomTransf('Linear', 323, -0.548, 0.0, 0.836)
    ops.geomTransf('Linear', 324, -0.493, 0.0, 0.87)
    ops.geomTransf('Linear', 325, -0.43, 0.0, 0.903)
    ops.geomTransf('Linear', 326, -0.362, 0.0, 0.932)
    ops.geomTransf('Linear', 327, -0.289, 0.0, 0.957)
    ops.geomTransf('Linear', 328, -0.209, 0.0, 0.978)
    ops.geomTransf('Linear', 329, -0.128, 0.0, 0.992)
    ops.geomTransf('Linear', 330, -0.043, 0.0, 0.999)
    ops.geomTransf('Linear', 331, 0.609, 0.0, 0.793)
    ops.geomTransf('Linear', 332, 0.548, 0.0, 0.836)
    ops.geomTransf('Linear', 333, 0.493, 0.0, 0.87)
    ops.geomTransf('Linear', 334, 0.43, 0.0, 0.903)
    ops.geomTransf('Linear', 335, 0.362, 0.0, 0.932)
    ops.geomTransf('Linear', 336, 0.289, 0.0, 0.957)
    ops.geomTransf('Linear', 337, 0.209, 0.0, 0.978)
    ops.geomTransf('Linear', 338, 0.128, 0.0, 0.992)
    ops.geomTransf('Linear', 339, 0.043, 0.0, 0.999)
    ops.geomTransf('Linear', 340, -0.188, 0.0, 0.982)
    ops.geomTransf('Linear', 341, 0.188, 0.0, 0.982)
    ops.geomTransf('Linear', 342, -0.188, 0.0, 0.982)
    ops.geomTransf('Linear', 343, 0.188, 0.0, 0.982)
    ops.geomTransf('Linear', 344, -0.188, 0.0, 0.982)
    ops.geomTransf('Linear', 345, 0.188, 0.0, 0.982)
    ops.geomTransf('Linear', 346, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 347, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 348, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 349, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 350, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 351, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 352, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 353, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 354, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 355, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 356, -0.113, 0.199, 0.974)
    ops.geomTransf('Linear', 357, -0.113, -0.199, 0.974)
    ops.geomTransf('Linear', 358, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 359, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 360, -0.01, 0.018, 1.0)
    ops.geomTransf('Linear', 361, 0.01, 0.018, 1.0)
    ops.geomTransf('Linear', 362, -0.01, -0.018, 1.0)
    ops.geomTransf('Linear', 363, 0.01, -0.018, 1.0)
    ops.geomTransf('Linear', 364, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 365, 0.0, 0.0, 1.0)
    ops.geomTransf('Linear', 366, 0.113, 0.199, 0.974)
    ops.geomTransf('Linear', 367, 0.113, -0.199, 0.974)
    ops.element('elasticBeamColumn', 1, 5, 6, 1500000, 26000,
                10830, 293500000000, 281300000000, 125000000000, 1)
    ops.element('elasticBeamColumn', 2, 6, 7, 1500000, 26000,
                10830, 293500000000, 281300000000, 125000000000, 2)
    ops.element('elasticBeamColumn', 3, 7, 8, 1500000, 26000,
                10830, 293500000000, 281300000000, 125000000000, 3)
    ops.element('elasticBeamColumn', 4, 8, 9, 1500000, 26000,
                10830, 293500000000, 281300000000, 125000000000, 4)
    ops.element('elasticBeamColumn', 5, 10, 11, 1500000, 26000,
                10830, 293500000000, 281300000000, 125000000000, 5)
    ops.element('elasticBeamColumn', 6, 11, 12, 1500000, 26000,
                10830, 293500000000, 281300000000, 125000000000, 6)
    ops.element('elasticBeamColumn', 7, 12, 13, 1500000, 26000,
                10830, 293500000000, 281300000000, 125000000000, 7)
    ops.element('elasticBeamColumn', 8, 13, 14, 1500000, 26000,
                10830, 293500000000, 281300000000, 125000000000, 8)
    ops.element('elasticBeamColumn', 9, 15, 16, 1500000, 26000,
                10830, 293500000000, 281300000000, 125000000000, 9)
    ops.element('elasticBeamColumn', 10, 16, 17, 1500000, 26000,
                10830, 293500000000, 281300000000, 125000000000, 10)
    ops.element('elasticBeamColumn', 11, 17, 18, 1500000, 26000,
                10830, 293500000000, 281300000000, 125000000000, 11)
    ops.element('elasticBeamColumn', 12, 18, 19, 1500000, 26000,
                10830, 293500000000, 281300000000, 125000000000, 12)
    ops.element('elasticBeamColumn', 13, 20, 21, 1500000, 26000,
                10830, 293500000000, 281300000000, 125000000000, 13)
    ops.element('elasticBeamColumn', 14, 21, 22, 1500000, 26000,
                10830, 293500000000, 281300000000, 125000000000, 14)
    ops.element('elasticBeamColumn', 15, 22, 23, 1500000, 26000,
                10830, 293500000000, 281300000000, 125000000000, 15)
    ops.element('elasticBeamColumn', 16, 23, 24, 1500000, 26000,
                10830, 293500000000, 281300000000, 125000000000, 16)
    ops.element('elasticBeamColumn', 17, 25, 26, 1500000, 26000,
                10830, 293500000000, 281300000000, 125000000000, 17)
    ops.element('elasticBeamColumn', 18, 26, 27, 1500000, 26000,
                10830, 293500000000, 281300000000, 125000000000, 18)
    ops.element('elasticBeamColumn', 19, 27, 28, 1500000, 26000,
                10830, 293500000000, 281300000000, 125000000000, 19)
    ops.element('elasticBeamColumn', 20, 28, 29, 1500000, 26000,
                10830, 293500000000, 281300000000, 125000000000, 20)
    ops.element('elasticBeamColumn', 21, 30, 31, 1500000, 26000,
                10830, 293500000000, 281300000000, 125000000000, 21)
    ops.element('elasticBeamColumn', 22, 31, 32, 1500000, 26000,
                10830, 293500000000, 281300000000, 125000000000, 22)
    ops.element('elasticBeamColumn', 23, 32, 33, 1500000, 26000,
                10830, 293500000000, 281300000000, 125000000000, 23)
    ops.element('elasticBeamColumn', 24, 33, 34, 1500000, 26000,
                10830, 293500000000, 281300000000, 125000000000, 24)
    ops.element('elasticBeamColumn', 25, 35, 36, 1500000, 26000,
                10830, 293500000000, 281300000000, 125000000000, 25)
    ops.element('elasticBeamColumn', 26, 36, 37, 1500000, 26000,
                10830, 293500000000, 281300000000, 125000000000, 26)
    ops.element('elasticBeamColumn', 27, 37, 38, 1500000, 26000,
                10830, 293500000000, 281300000000, 125000000000, 27)
    ops.element('elasticBeamColumn', 28, 38, 39, 1500000, 26000,
                10830, 293500000000, 281300000000, 125000000000, 28)
    ops.element('elasticBeamColumn', 29, 40, 41, 1500000, 26000,
                10830, 293500000000, 281300000000, 125000000000, 29)
    ops.element('elasticBeamColumn', 30, 41, 42, 1500000, 26000,
                10830, 293500000000, 281300000000, 125000000000, 30)
    ops.element('elasticBeamColumn', 31, 42, 43, 1500000, 26000,
                10830, 293500000000, 281300000000, 125000000000, 31)
    ops.element('elasticBeamColumn', 32, 43, 44, 1500000, 26000,
                10830, 293500000000, 281300000000, 125000000000, 32)
    ops.element('elasticBeamColumn', 33, 45, 46, 1500000, 26000,
                10830, 293500000000, 281300000000, 125000000000, 33)
    ops.element('elasticBeamColumn', 34, 46, 47, 1500000, 26000,
                10830, 293500000000, 281300000000, 125000000000, 34)
    ops.element('elasticBeamColumn', 35, 47, 48, 1500000, 26000,
                10830, 293500000000, 281300000000, 125000000000, 35)
    ops.element('elasticBeamColumn', 36, 48, 49, 1500000, 26000,
                10830, 293500000000, 281300000000, 125000000000, 36)
    ops.element('elasticBeamColumn', 37, 50, 51, 1500000, 26000,
                10830, 293500000000, 281300000000, 125000000000, 37)
    ops.element('elasticBeamColumn', 38, 51, 52, 1500000, 26000,
                10830, 293500000000, 281300000000, 125000000000, 38)
    ops.element('elasticBeamColumn', 39, 52, 53, 1500000, 26000,
                10830, 293500000000, 281300000000, 125000000000, 39)
    ops.element('elasticBeamColumn', 40, 53, 54, 1500000, 26000,
                10830, 293500000000, 281300000000, 125000000000, 40)
    ops.element('elasticBeamColumn', 41, 55, 56, 1500000, 26000,
                10830, 293500000000, 281300000000, 125000000000, 41)
    ops.element('elasticBeamColumn', 42, 56, 57, 1500000, 26000,
                10830, 293500000000, 281300000000, 125000000000, 42)
    ops.element('elasticBeamColumn', 43, 57, 58, 1500000, 26000,
                10830, 293500000000, 281300000000, 125000000000, 43)
    ops.element('elasticBeamColumn', 44, 58, 59, 1500000, 26000,
                10830, 293500000000, 281300000000, 125000000000, 44)
    ops.element('elasticBeamColumn', 45, 60, 61, 1500000, 26000,
                10830, 293500000000, 281300000000, 125000000000, 45)
    ops.element('elasticBeamColumn', 46, 61, 62, 1500000, 26000,
                10830, 293500000000, 281300000000, 125000000000, 46)
    ops.element('elasticBeamColumn', 47, 62, 63, 1500000, 26000,
                10830, 293500000000, 281300000000, 125000000000, 47)
    ops.element('elasticBeamColumn', 48, 63, 64, 1500000, 26000,
                10830, 293500000000, 281300000000, 125000000000, 48)
    ops.element('elasticBeamColumn', 49, 65, 66, 1500000, 26000,
                10830, 293500000000, 281300000000, 125000000000, 49)
    ops.element('elasticBeamColumn', 50, 66, 67, 1500000, 26000,
                10830, 293500000000, 281300000000, 125000000000, 50)
    ops.element('elasticBeamColumn', 51, 67, 68, 1500000, 26000,
                10830, 293500000000, 281300000000, 125000000000, 51)
    ops.element('elasticBeamColumn', 52, 68, 69, 1500000, 26000,
                10830, 293500000000, 281300000000, 125000000000, 52)
    ops.element('elasticBeamColumn', 53, 70, 71, 1500000, 26000,
                10830, 293500000000, 281300000000, 125000000000, 53)
    ops.element('elasticBeamColumn', 54, 71, 72, 1500000, 26000,
                10830, 293500000000, 281300000000, 125000000000, 54)
    ops.element('elasticBeamColumn', 55, 72, 73, 1500000, 26000,
                10830, 293500000000, 281300000000, 125000000000, 55)
    ops.element('elasticBeamColumn', 56, 73, 74, 1500000, 26000,
                10830, 293500000000, 281300000000, 125000000000, 56)
    ops.element('elasticBeamColumn', 57, 75, 76, 1500000, 26000,
                10830, 293500000000, 281300000000, 125000000000, 57)
    ops.element('elasticBeamColumn', 58, 76, 77, 1500000, 26000,
                10830, 293500000000, 281300000000, 125000000000, 58)
    ops.element('elasticBeamColumn', 59, 77, 78, 1500000, 26000,
                10830, 293500000000, 281300000000, 125000000000, 59)
    ops.element('elasticBeamColumn', 60, 78, 79, 1500000, 26000,
                10830, 293500000000, 281300000000, 125000000000, 60)
    ops.element('elasticBeamColumn', 61, 80, 81, 1500000, 26000,
                10830, 293500000000, 281300000000, 125000000000, 61)
    ops.element('elasticBeamColumn', 62, 81, 82, 1500000, 26000,
                10830, 293500000000, 281300000000, 125000000000, 62)
    ops.element('elasticBeamColumn', 63, 82, 83, 1500000, 26000,
                10830, 293500000000, 281300000000, 125000000000, 63)
    ops.element('elasticBeamColumn', 64, 83, 84, 1500000, 26000,
                10830, 293500000000, 281300000000, 125000000000, 64)
    ops.element('elasticBeamColumn', 65, 85, 86, 1500000, 26000,
                10830, 293500000000, 281300000000, 125000000000, 65)
    ops.element('elasticBeamColumn', 66, 86, 87, 1500000, 26000,
                10830, 293500000000, 281300000000, 125000000000, 66)
    ops.element('elasticBeamColumn', 67, 87, 88, 1500000, 26000,
                10830, 293500000000, 281300000000, 125000000000, 67)
    ops.element('elasticBeamColumn', 68, 88, 89, 1500000, 26000,
                10830, 293500000000, 281300000000, 125000000000, 68)
    ops.element('elasticBeamColumn', 69, 90, 91, 1500000, 26000,
                10830, 293500000000, 281300000000, 125000000000, 69)
    ops.element('elasticBeamColumn', 70, 91, 92, 1500000, 26000,
                10830, 293500000000, 281300000000, 125000000000, 70)
    ops.element('elasticBeamColumn', 71, 92, 93, 1500000, 26000,
                10830, 293500000000, 281300000000, 125000000000, 71)
    ops.element('elasticBeamColumn', 72, 93, 94, 1500000, 26000,
                10830, 293500000000, 281300000000, 125000000000, 72)
    ops.element('elasticBeamColumn', 73, 95, 96, 1500000, 26000,
                10830, 293500000000, 281300000000, 125000000000, 73)
    ops.element('elasticBeamColumn', 74, 96, 97, 1500000, 26000,
                10830, 293500000000, 281300000000, 125000000000, 74)
    ops.element('elasticBeamColumn', 75, 97, 98, 1500000, 26000,
                10830, 293500000000, 281300000000, 125000000000, 75)
    ops.element('elasticBeamColumn', 76, 98, 99, 1500000, 26000,
                10830, 293500000000, 281300000000, 125000000000, 76)
    ops.element('elasticBeamColumn', 77, 9, 14, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 77)
    ops.element('elasticBeamColumn', 78, 14, 19, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 78)
    ops.element('elasticBeamColumn', 79, 19, 24, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 79)
    ops.element('elasticBeamColumn', 80, 24, 29, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 80)
    ops.element('elasticBeamColumn', 81, 29, 34, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 81)
    ops.element('elasticBeamColumn', 82, 34, 39, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 82)
    ops.element('elasticBeamColumn', 83, 39, 44, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 83)
    ops.element('elasticBeamColumn', 84, 44, 49, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 84)
    ops.element('elasticBeamColumn', 85, 49, 54, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 85)
    ops.element('elasticBeamColumn', 86, 54, 59, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 86)
    ops.element('elasticBeamColumn', 87, 59, 64, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 87)
    ops.element('elasticBeamColumn', 88, 64, 69, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 88)
    ops.element('elasticBeamColumn', 89, 69, 74, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 89)
    ops.element('elasticBeamColumn', 90, 74, 79, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 90)
    ops.element('elasticBeamColumn', 91, 79, 84, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 91)
    ops.element('elasticBeamColumn', 92, 84, 89, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 92)
    ops.element('elasticBeamColumn', 93, 89, 94, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 93)
    ops.element('elasticBeamColumn', 94, 94, 99, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 94)
    ops.element('elasticBeamColumn', 95, 8, 13, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 95)
    ops.element('elasticBeamColumn', 96, 13, 18, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 96)
    ops.element('elasticBeamColumn', 97, 18, 23, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 97)
    ops.element('elasticBeamColumn', 98, 23, 28, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 98)
    ops.element('elasticBeamColumn', 99, 28, 33, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 99)
    ops.element('elasticBeamColumn', 100, 33, 38, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 100)
    ops.element('elasticBeamColumn', 101, 38, 43, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 101)
    ops.element('elasticBeamColumn', 102, 43, 48, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 102)
    ops.element('elasticBeamColumn', 103, 48, 53, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 103)
    ops.element('elasticBeamColumn', 104, 53, 58, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 104)
    ops.element('elasticBeamColumn', 105, 58, 63, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 105)
    ops.element('elasticBeamColumn', 106, 63, 68, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 106)
    ops.element('elasticBeamColumn', 107, 68, 73, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 107)
    ops.element('elasticBeamColumn', 108, 73, 78, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 108)
    ops.element('elasticBeamColumn', 109, 78, 83, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 109)
    ops.element('elasticBeamColumn', 110, 83, 88, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 110)
    ops.element('elasticBeamColumn', 111, 88, 93, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 111)
    ops.element('elasticBeamColumn', 112, 93, 98, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 112)
    ops.element('elasticBeamColumn', 113, 7, 12, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 113)
    ops.element('elasticBeamColumn', 114, 12, 17, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 114)
    ops.element('elasticBeamColumn', 115, 17, 22, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 115)
    ops.element('elasticBeamColumn', 116, 22, 27, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 116)
    ops.element('elasticBeamColumn', 117, 27, 32, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 117)
    ops.element('elasticBeamColumn', 118, 32, 37, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 118)
    ops.element('elasticBeamColumn', 119, 37, 42, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 119)
    ops.element('elasticBeamColumn', 120, 42, 47, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 120)
    ops.element('elasticBeamColumn', 121, 47, 52, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 121)
    ops.element('elasticBeamColumn', 122, 52, 57, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 122)
    ops.element('elasticBeamColumn', 123, 57, 62, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 123)
    ops.element('elasticBeamColumn', 124, 62, 67, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 124)
    ops.element('elasticBeamColumn', 125, 67, 72, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 125)
    ops.element('elasticBeamColumn', 126, 72, 77, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 126)
    ops.element('elasticBeamColumn', 127, 77, 82, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 127)
    ops.element('elasticBeamColumn', 128, 82, 87, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 128)
    ops.element('elasticBeamColumn', 129, 87, 92, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 129)
    ops.element('elasticBeamColumn', 130, 92, 97, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 130)
    ops.element('elasticBeamColumn', 131, 6, 11, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 131)
    ops.element('elasticBeamColumn', 132, 11, 16, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 132)
    ops.element('elasticBeamColumn', 133, 16, 21, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 133)
    ops.element('elasticBeamColumn', 134, 21, 26, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 134)
    ops.element('elasticBeamColumn', 135, 26, 31, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 135)
    ops.element('elasticBeamColumn', 136, 31, 36, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 136)
    ops.element('elasticBeamColumn', 137, 36, 41, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 137)
    ops.element('elasticBeamColumn', 138, 41, 46, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 138)
    ops.element('elasticBeamColumn', 139, 46, 51, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 139)
    ops.element('elasticBeamColumn', 140, 51, 56, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 140)
    ops.element('elasticBeamColumn', 141, 56, 61, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 141)
    ops.element('elasticBeamColumn', 142, 61, 66, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 142)
    ops.element('elasticBeamColumn', 143, 66, 71, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 143)
    ops.element('elasticBeamColumn', 144, 71, 76, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 144)
    ops.element('elasticBeamColumn', 145, 76, 81, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 145)
    ops.element('elasticBeamColumn', 146, 81, 86, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 146)
    ops.element('elasticBeamColumn', 147, 86, 91, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 147)
    ops.element('elasticBeamColumn', 148, 91, 96, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 148)
    ops.element('elasticBeamColumn', 149, 5, 10, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 149)
    ops.element('elasticBeamColumn', 150, 10, 15, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 150)
    ops.element('elasticBeamColumn', 151, 15, 20, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 151)
    ops.element('elasticBeamColumn', 152, 20, 25, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 152)
    ops.element('elasticBeamColumn', 153, 25, 30, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 153)
    ops.element('elasticBeamColumn', 154, 30, 35, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 154)
    ops.element('elasticBeamColumn', 155, 35, 40, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 155)
    ops.element('elasticBeamColumn', 156, 40, 45, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 156)
    ops.element('elasticBeamColumn', 157, 45, 50, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 157)
    ops.element('elasticBeamColumn', 158, 50, 55, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 158)
    ops.element('elasticBeamColumn', 159, 55, 60, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 159)
    ops.element('elasticBeamColumn', 160, 60, 65, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 160)
    ops.element('elasticBeamColumn', 161, 65, 70, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 161)
    ops.element('elasticBeamColumn', 162, 70, 75, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 162)
    ops.element('elasticBeamColumn', 163, 75, 80, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 163)
    ops.element('elasticBeamColumn', 164, 80, 85, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 164)
    ops.element('elasticBeamColumn', 165, 85, 90, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 165)
    ops.element('elasticBeamColumn', 166, 90, 95, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 166)
    ops.element('elasticBeamColumn', 167, 5, 100, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 167)
    ops.element('elasticBeamColumn', 168, 6, 101, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 168)
    ops.element('elasticBeamColumn', 169, 7, 102, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 169)
    ops.element('elasticBeamColumn', 170, 8, 103, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 170)
    ops.element('elasticBeamColumn', 171, 9, 104, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 171)
    ops.element('elasticBeamColumn', 172, 10, 105, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 172)
    ops.element('elasticBeamColumn', 173, 11, 106, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 173)
    ops.element('elasticBeamColumn', 174, 12, 107, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 174)
    ops.element('elasticBeamColumn', 175, 13, 108, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 175)
    ops.element('elasticBeamColumn', 176, 14, 109, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 176)
    ops.element('elasticBeamColumn', 177, 15, 110, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 177)
    ops.element('elasticBeamColumn', 178, 16, 111, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 178)
    ops.element('elasticBeamColumn', 179, 17, 112, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 179)
    ops.element('elasticBeamColumn', 180, 18, 113, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 180)
    ops.element('elasticBeamColumn', 181, 19, 114, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 181)
    ops.element('elasticBeamColumn', 182, 20, 115, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 182)
    ops.element('elasticBeamColumn', 183, 21, 116, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 183)
    ops.element('elasticBeamColumn', 184, 22, 117, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 184)
    ops.element('elasticBeamColumn', 185, 23, 118, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 185)
    ops.element('elasticBeamColumn', 186, 24, 119, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 186)
    ops.element('elasticBeamColumn', 187, 25, 120, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 187)
    ops.element('elasticBeamColumn', 188, 26, 121, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 188)
    ops.element('elasticBeamColumn', 189, 27, 122, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 189)
    ops.element('elasticBeamColumn', 190, 28, 123, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 190)
    ops.element('elasticBeamColumn', 191, 29, 124, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 191)
    ops.element('elasticBeamColumn', 192, 30, 125, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 192)
    ops.element('elasticBeamColumn', 193, 31, 126, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 193)
    ops.element('elasticBeamColumn', 194, 32, 127, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 194)
    ops.element('elasticBeamColumn', 195, 33, 128, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 195)
    ops.element('elasticBeamColumn', 196, 34, 129, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 196)
    ops.element('elasticBeamColumn', 197, 35, 130, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 197)
    ops.element('elasticBeamColumn', 198, 36, 131, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 198)
    ops.element('elasticBeamColumn', 199, 37, 132, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 199)
    ops.element('elasticBeamColumn', 200, 38, 133, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 200)
    ops.element('elasticBeamColumn', 201, 39, 134, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 201)
    ops.element('elasticBeamColumn', 202, 40, 135, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 202)
    ops.element('elasticBeamColumn', 203, 41, 136, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 203)
    ops.element('elasticBeamColumn', 204, 42, 137, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 204)
    ops.element('elasticBeamColumn', 205, 43, 138, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 205)
    ops.element('elasticBeamColumn', 206, 44, 139, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 206)
    ops.element('elasticBeamColumn', 207, 45, 140, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 207)
    ops.element('elasticBeamColumn', 208, 46, 141, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 208)
    ops.element('elasticBeamColumn', 209, 47, 142, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 209)
    ops.element('elasticBeamColumn', 210, 48, 143, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 210)
    ops.element('elasticBeamColumn', 211, 49, 144, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 211)
    ops.element('elasticBeamColumn', 212, 50, 145, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 212)
    ops.element('elasticBeamColumn', 213, 51, 146, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 213)
    ops.element('elasticBeamColumn', 214, 52, 147, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 214)
    ops.element('elasticBeamColumn', 215, 53, 148, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 215)
    ops.element('elasticBeamColumn', 216, 54, 149, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 216)
    ops.element('elasticBeamColumn', 217, 55, 150, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 217)
    ops.element('elasticBeamColumn', 218, 56, 151, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 218)
    ops.element('elasticBeamColumn', 219, 57, 152, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 219)
    ops.element('elasticBeamColumn', 220, 58, 153, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 220)
    ops.element('elasticBeamColumn', 221, 59, 154, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 221)
    ops.element('elasticBeamColumn', 222, 60, 155, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 222)
    ops.element('elasticBeamColumn', 223, 61, 156, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 223)
    ops.element('elasticBeamColumn', 224, 62, 157, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 224)
    ops.element('elasticBeamColumn', 225, 63, 158, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 225)
    ops.element('elasticBeamColumn', 226, 64, 159, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 226)
    ops.element('elasticBeamColumn', 227, 65, 160, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 227)
    ops.element('elasticBeamColumn', 228, 66, 161, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 228)
    ops.element('elasticBeamColumn', 229, 67, 162, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 229)
    ops.element('elasticBeamColumn', 230, 68, 163, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 230)
    ops.element('elasticBeamColumn', 231, 69, 164, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 231)
    ops.element('elasticBeamColumn', 232, 70, 165, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 232)
    ops.element('elasticBeamColumn', 233, 71, 166, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 233)
    ops.element('elasticBeamColumn', 234, 72, 167, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 234)
    ops.element('elasticBeamColumn', 235, 73, 168, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 235)
    ops.element('elasticBeamColumn', 236, 74, 169, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 236)
    ops.element('elasticBeamColumn', 237, 75, 170, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 237)
    ops.element('elasticBeamColumn', 238, 76, 171, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 238)
    ops.element('elasticBeamColumn', 239, 77, 172, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 239)
    ops.element('elasticBeamColumn', 240, 78, 173, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 240)
    ops.element('elasticBeamColumn', 241, 79, 174, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 241)
    ops.element('elasticBeamColumn', 242, 80, 175, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 242)
    ops.element('elasticBeamColumn', 243, 81, 176, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 243)
    ops.element('elasticBeamColumn', 244, 82, 177, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 244)
    ops.element('elasticBeamColumn', 245, 83, 178, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 245)
    ops.element('elasticBeamColumn', 246, 84, 179, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 246)
    ops.element('elasticBeamColumn', 247, 85, 180, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 247)
    ops.element('elasticBeamColumn', 248, 86, 181, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 248)
    ops.element('elasticBeamColumn', 249, 87, 182, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 249)
    ops.element('elasticBeamColumn', 250, 88, 183, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 250)
    ops.element('elasticBeamColumn', 251, 89, 184, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 251)
    ops.element('elasticBeamColumn', 252, 90, 185, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 252)
    ops.element('elasticBeamColumn', 253, 91, 186, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 253)
    ops.element('elasticBeamColumn', 254, 92, 187, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 254)
    ops.element('elasticBeamColumn', 255, 93, 188, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 255)
    ops.element('elasticBeamColumn', 256, 94, 189, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 256)
    ops.element('elasticBeamColumn', 257, 99, 190, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 257)
    ops.element('elasticBeamColumn', 258, 98, 191, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 258)
    ops.element('elasticBeamColumn', 259, 97, 192, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 259)
    ops.element('elasticBeamColumn', 260, 96, 193, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 260)
    ops.element('elasticBeamColumn', 261, 95, 194, 40000, 206000,
                79230, 225300000, 133300000, 133300000, 261)
    ops.element('elasticBeamColumn', 262, 105, 195, 4084,
                206000, 79230, 17360000, 8679000, 8679000, 262)
    ops.element('elasticBeamColumn', 263, 110, 196, 4084,
                206000, 79230, 17360000, 8679000, 8679000, 263)
    ops.element('elasticBeamColumn', 264, 115, 197, 4084,
                206000, 79230, 17360000, 8679000, 8679000, 264)
    ops.element('elasticBeamColumn', 265, 120, 198, 4084,
                206000, 79230, 17360000, 8679000, 8679000, 265)
    ops.element('elasticBeamColumn', 266, 125, 199, 4084,
                206000, 79230, 17360000, 8679000, 8679000, 266)
    ops.element('elasticBeamColumn', 267, 130, 200, 4084,
                206000, 79230, 17360000, 8679000, 8679000, 267)
    ops.element('elasticBeamColumn', 268, 135, 201, 4084,
                206000, 79230, 17360000, 8679000, 8679000, 268)
    ops.element('elasticBeamColumn', 269, 140, 202, 4084,
                206000, 79230, 17360000, 8679000, 8679000, 269)
    ops.element('elasticBeamColumn', 270, 145, 203, 4084,
                206000, 79230, 17360000, 8679000, 8679000, 270)
    ops.element('elasticBeamColumn', 271, 185, 204, 4084,
                206000, 79230, 17360000, 8679000, 8679000, 271)
    ops.element('elasticBeamColumn', 272, 180, 205, 4084,
                206000, 79230, 17360000, 8679000, 8679000, 272)
    ops.element('elasticBeamColumn', 273, 175, 206, 4084,
                206000, 79230, 17360000, 8679000, 8679000, 273)
    ops.element('elasticBeamColumn', 274, 170, 207, 4084,
                206000, 79230, 17360000, 8679000, 8679000, 274)
    ops.element('elasticBeamColumn', 275, 165, 208, 4084,
                206000, 79230, 17360000, 8679000, 8679000, 275)
    ops.element('elasticBeamColumn', 276, 160, 209, 4084,
                206000, 79230, 17360000, 8679000, 8679000, 276)
    ops.element('elasticBeamColumn', 277, 155, 210, 4084,
                206000, 79230, 17360000, 8679000, 8679000, 277)
    ops.element('elasticBeamColumn', 278, 150, 211, 4084,
                206000, 79230, 17360000, 8679000, 8679000, 278)
    ops.element('elasticBeamColumn', 279, 1, 212, 12000000, 26000,
                10830, 19440000000000, 16000000000000, 9000000000000, 279)
    ops.element('elasticBeamColumn', 280, 2, 213, 12000000, 26000,
                10830, 19440000000000, 16000000000000, 9000000000000, 280)
    ops.element('elasticBeamColumn', 281, 212, 5, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 281)
    ops.element('elasticBeamColumn', 282, 213, 95, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 282)
    ops.element('elasticBeamColumn', 283, 212, 195, 3142000, 206000,
                79230, 3338000000000, 1669000000000, 1669000000000, 283)
    ops.element('elasticBeamColumn', 284, 195, 196, 3142000, 206000,
                79230, 3338000000000, 1669000000000, 1669000000000, 284)
    ops.element('elasticBeamColumn', 285, 196, 197, 3142000, 206000,
                79230, 3338000000000, 1669000000000, 1669000000000, 285)
    ops.element('elasticBeamColumn', 286, 197, 198, 3142000, 206000,
                79230, 3338000000000, 1669000000000, 1669000000000, 286)
    ops.element('elasticBeamColumn', 287, 198, 199, 3142000, 206000,
                79230, 3338000000000, 1669000000000, 1669000000000, 287)
    ops.element('elasticBeamColumn', 288, 199, 200, 3142000, 206000,
                79230, 3338000000000, 1669000000000, 1669000000000, 288)
    ops.element('elasticBeamColumn', 289, 200, 201, 3142000, 206000,
                79230, 3338000000000, 1669000000000, 1669000000000, 289)
    ops.element('elasticBeamColumn', 290, 201, 202, 3142000, 206000,
                79230, 3338000000000, 1669000000000, 1669000000000, 290)
    ops.element('elasticBeamColumn', 291, 202, 203, 3142000, 206000,
                79230, 3338000000000, 1669000000000, 1669000000000, 291)
    ops.element('elasticBeamColumn', 292, 213, 204, 3142000, 206000,
                79230, 3338000000000, 1669000000000, 1669000000000, 292)
    ops.element('elasticBeamColumn', 293, 204, 205, 3142000, 206000,
                79230, 3338000000000, 1669000000000, 1669000000000, 293)
    ops.element('elasticBeamColumn', 294, 205, 206, 3142000, 206000,
                79230, 3338000000000, 1669000000000, 1669000000000, 294)
    ops.element('elasticBeamColumn', 295, 206, 207, 3142000, 206000,
                79230, 3338000000000, 1669000000000, 1669000000000, 295)
    ops.element('elasticBeamColumn', 296, 207, 208, 3142000, 206000,
                79230, 3338000000000, 1669000000000, 1669000000000, 296)
    ops.element('elasticBeamColumn', 297, 208, 209, 3142000, 206000,
                79230, 3338000000000, 1669000000000, 1669000000000, 297)
    ops.element('elasticBeamColumn', 298, 209, 210, 3142000, 206000,
                79230, 3338000000000, 1669000000000, 1669000000000, 298)
    ops.element('elasticBeamColumn', 299, 210, 211, 3142000, 206000,
                79230, 3338000000000, 1669000000000, 1669000000000, 299)
    ops.element('elasticBeamColumn', 300, 211, 203, 3142000, 206000,
                79230, 3338000000000, 1669000000000, 1669000000000, 300)
    ops.element('elasticBeamColumn', 301, 109, 214, 4084,
                206000, 79230, 17360000, 8679000, 8679000, 301)
    ops.element('elasticBeamColumn', 302, 114, 215, 4084,
                206000, 79230, 17360000, 8679000, 8679000, 302)
    ops.element('elasticBeamColumn', 303, 119, 216, 4084,
                206000, 79230, 17360000, 8679000, 8679000, 303)
    ops.element('elasticBeamColumn', 304, 124, 217, 4084,
                206000, 79230, 17360000, 8679000, 8679000, 304)
    ops.element('elasticBeamColumn', 305, 129, 218, 4084,
                206000, 79230, 17360000, 8679000, 8679000, 305)
    ops.element('elasticBeamColumn', 306, 134, 219, 4084,
                206000, 79230, 17360000, 8679000, 8679000, 306)
    ops.element('elasticBeamColumn', 307, 139, 220, 4084,
                206000, 79230, 17360000, 8679000, 8679000, 307)
    ops.element('elasticBeamColumn', 308, 144, 221, 4084,
                206000, 79230, 17360000, 8679000, 8679000, 308)
    ops.element('elasticBeamColumn', 309, 149, 222, 4084,
                206000, 79230, 17360000, 8679000, 8679000, 309)
    ops.element('elasticBeamColumn', 310, 189, 223, 4084,
                206000, 79230, 17360000, 8679000, 8679000, 310)
    ops.element('elasticBeamColumn', 311, 184, 224, 4084,
                206000, 79230, 17360000, 8679000, 8679000, 311)
    ops.element('elasticBeamColumn', 312, 179, 225, 4084,
                206000, 79230, 17360000, 8679000, 8679000, 312)
    ops.element('elasticBeamColumn', 313, 174, 226, 4084,
                206000, 79230, 17360000, 8679000, 8679000, 313)
    ops.element('elasticBeamColumn', 314, 169, 227, 4084,
                206000, 79230, 17360000, 8679000, 8679000, 314)
    ops.element('elasticBeamColumn', 315, 164, 228, 4084,
                206000, 79230, 17360000, 8679000, 8679000, 315)
    ops.element('elasticBeamColumn', 316, 159, 229, 4084,
                206000, 79230, 17360000, 8679000, 8679000, 316)
    ops.element('elasticBeamColumn', 317, 154, 230, 4084,
                206000, 79230, 17360000, 8679000, 8679000, 317)
    ops.element('elasticBeamColumn', 318, 3, 231, 12000000, 26000,
                10830, 19440000000000, 16000000000000, 9000000000000, 318)
    ops.element('elasticBeamColumn', 319, 4, 232, 12000000, 26000,
                10830, 19440000000000, 16000000000000, 9000000000000, 319)
    ops.element('elasticBeamColumn', 320, 231, 9, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 320)
    ops.element('elasticBeamColumn', 321, 232, 99, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 321)
    ops.element('elasticBeamColumn', 322, 231, 214, 3142000, 206000,
                79230, 3338000000000, 1669000000000, 1669000000000, 322)
    ops.element('elasticBeamColumn', 323, 214, 215, 3142000, 206000,
                79230, 3338000000000, 1669000000000, 1669000000000, 323)
    ops.element('elasticBeamColumn', 324, 215, 216, 3142000, 206000,
                79230, 3338000000000, 1669000000000, 1669000000000, 324)
    ops.element('elasticBeamColumn', 325, 216, 217, 3142000, 206000,
                79230, 3338000000000, 1669000000000, 1669000000000, 325)
    ops.element('elasticBeamColumn', 326, 217, 218, 3142000, 206000,
                79230, 3338000000000, 1669000000000, 1669000000000, 326)
    ops.element('elasticBeamColumn', 327, 218, 219, 3142000, 206000,
                79230, 3338000000000, 1669000000000, 1669000000000, 327)
    ops.element('elasticBeamColumn', 328, 219, 220, 3142000, 206000,
                79230, 3338000000000, 1669000000000, 1669000000000, 328)
    ops.element('elasticBeamColumn', 329, 220, 221, 3142000, 206000,
                79230, 3338000000000, 1669000000000, 1669000000000, 329)
    ops.element('elasticBeamColumn', 330, 221, 222, 3142000, 206000,
                79230, 3338000000000, 1669000000000, 1669000000000, 330)
    ops.element('elasticBeamColumn', 331, 232, 223, 3142000, 206000,
                79230, 3338000000000, 1669000000000, 1669000000000, 331)
    ops.element('elasticBeamColumn', 332, 223, 224, 3142000, 206000,
                79230, 3338000000000, 1669000000000, 1669000000000, 332)
    ops.element('elasticBeamColumn', 333, 224, 225, 3142000, 206000,
                79230, 3338000000000, 1669000000000, 1669000000000, 333)
    ops.element('elasticBeamColumn', 334, 225, 226, 3142000, 206000,
                79230, 3338000000000, 1669000000000, 1669000000000, 334)
    ops.element('elasticBeamColumn', 335, 226, 227, 3142000, 206000,
                79230, 3338000000000, 1669000000000, 1669000000000, 335)
    ops.element('elasticBeamColumn', 336, 227, 228, 3142000, 206000,
                79230, 3338000000000, 1669000000000, 1669000000000, 336)
    ops.element('elasticBeamColumn', 337, 228, 229, 3142000, 206000,
                79230, 3338000000000, 1669000000000, 1669000000000, 337)
    ops.element('elasticBeamColumn', 338, 229, 230, 3142000, 206000,
                79230, 3338000000000, 1669000000000, 1669000000000, 338)
    ops.element('elasticBeamColumn', 339, 230, 222, 3142000, 206000,
                79230, 3338000000000, 1669000000000, 1669000000000, 339)
    ops.element('elasticBeamColumn', 340, 233, 6, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 340)
    ops.element('elasticBeamColumn', 341, 234, 96, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 341)
    ops.element('elasticBeamColumn', 342, 235, 7, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 342)
    ops.element('elasticBeamColumn', 343, 236, 97, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 343)
    ops.element('elasticBeamColumn', 344, 237, 8, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 344)
    ops.element('elasticBeamColumn', 345, 238, 98, 480000, 26000,
                10830, 20230000000, 57600000000, 6400000000, 345)
    ops.element('elasticBeamColumn', 346, 231, 237, 16750000, 26000,
                10830, 26710000000000, 8724000000000, 62660000000000, 346)
    ops.element('elasticBeamColumn', 347, 237, 235, 16750000, 26000,
                10830, 26710000000000, 8724000000000, 62660000000000, 347)
    ops.element('elasticBeamColumn', 348, 235, 233, 16750000, 26000,
                10830, 26710000000000, 8724000000000, 62660000000000, 348)
    ops.element('elasticBeamColumn', 349, 233, 212, 16750000, 26000,
                10830, 26710000000000, 8724000000000, 62660000000000, 349)
    ops.element('elasticBeamColumn', 350, 213, 234, 16750000, 26000,
                10830, 26710000000000, 8724000000000, 62660000000000, 350)
    ops.element('elasticBeamColumn', 351, 234, 236, 16750000, 26000,
                10830, 26710000000000, 8724000000000, 62660000000000, 351)
    ops.element('elasticBeamColumn', 352, 236, 238, 16750000, 26000,
                10830, 26710000000000, 8724000000000, 62660000000000, 352)
    ops.element('elasticBeamColumn', 353, 238, 232, 16750000, 26000,
                10830, 26710000000000, 8724000000000, 62660000000000, 353)
    ops.element('elasticBeamColumn', 354, 198, 239, 1005000, 206000,
                79230, 201100000000, 100500000000, 100500000000, 354)
    ops.element('elasticBeamColumn', 355, 239, 217, 1005000, 206000,
                79230, 201100000000, 100500000000, 100500000000, 355)
    ops.element('elasticBeamColumn', 356, 216, 239, 1005000, 206000,
                79230, 201100000000, 100500000000, 100500000000, 356)
    ops.element('elasticBeamColumn', 357, 197, 239, 1005000, 206000,
                79230, 201100000000, 100500000000, 100500000000, 357)
    ops.element('elasticBeamColumn', 358, 203, 240, 1005000, 206000,
                79230, 201100000000, 100500000000, 100500000000, 358)
    ops.element('elasticBeamColumn', 359, 240, 222, 1005000, 206000,
                79230, 201100000000, 100500000000, 100500000000, 359)
    ops.element('elasticBeamColumn', 360, 221, 240, 1005000, 206000,
                79230, 201100000000, 100500000000, 100500000000, 360)
    ops.element('elasticBeamColumn', 361, 230, 240, 1005000, 206000,
                79230, 201100000000, 100500000000, 100500000000, 361)
    ops.element('elasticBeamColumn', 362, 202, 240, 1005000, 206000,
                79230, 201100000000, 100500000000, 100500000000, 362)
    ops.element('elasticBeamColumn', 363, 211, 240, 1005000, 206000,
                79230, 201100000000, 100500000000, 100500000000, 363)
    ops.element('elasticBeamColumn', 364, 207, 241, 1005000, 206000,
                79230, 201100000000, 100500000000, 100500000000, 364)
    ops.element('elasticBeamColumn', 365, 241, 226, 1005000, 206000,
                79230, 201100000000, 100500000000, 100500000000, 365)
    ops.element('elasticBeamColumn', 366, 225, 241, 1005000, 206000,
                79230, 201100000000, 100500000000, 100500000000, 366)
    ops.element('elasticBeamColumn', 367, 206, 241, 1005000, 206000,
                79230, 201100000000, 100500000000, 100500000000, 367)
    ops.element('ShellMITC4', 368, 104, 109, 108, 103, 701)
    ops.element('ShellMITC4', 369, 103, 108, 107, 102, 701)
    ops.element('ShellMITC4', 370, 102, 107, 106, 101, 701)
    ops.element('ShellMITC4', 371, 101, 106, 105, 100, 701)
    ops.element('ShellMITC4', 372, 109, 114, 113, 108, 701)
    ops.element('ShellMITC4', 373, 108, 113, 112, 107, 701)
    ops.element('ShellMITC4', 374, 107, 112, 111, 106, 701)
    ops.element('ShellMITC4', 375, 106, 111, 110, 105, 701)
    ops.element('ShellMITC4', 376, 114, 119, 118, 113, 701)
    ops.element('ShellMITC4', 377, 113, 118, 117, 112, 701)
    ops.element('ShellMITC4', 378, 112, 117, 116, 111, 701)
    ops.element('ShellMITC4', 379, 111, 116, 115, 110, 701)
    ops.element('ShellMITC4', 380, 119, 124, 123, 118, 701)
    ops.element('ShellMITC4', 381, 118, 123, 122, 117, 701)
    ops.element('ShellMITC4', 382, 117, 122, 121, 116, 701)
    ops.element('ShellMITC4', 383, 116, 121, 120, 115, 701)
    ops.element('ShellMITC4', 384, 124, 129, 128, 123, 701)
    ops.element('ShellMITC4', 385, 123, 128, 127, 122, 701)
    ops.element('ShellMITC4', 386, 122, 127, 126, 121, 701)
    ops.element('ShellMITC4', 387, 121, 126, 125, 120, 701)
    ops.element('ShellMITC4', 388, 129, 134, 133, 128, 701)
    ops.element('ShellMITC4', 389, 128, 133, 132, 127, 701)
    ops.element('ShellMITC4', 390, 127, 132, 131, 126, 701)
    ops.element('ShellMITC4', 391, 126, 131, 130, 125, 701)
    ops.element('ShellMITC4', 392, 134, 139, 138, 133, 701)
    ops.element('ShellMITC4', 393, 133, 138, 137, 132, 701)
    ops.element('ShellMITC4', 394, 132, 137, 136, 131, 701)
    ops.element('ShellMITC4', 395, 131, 136, 135, 130, 701)
    ops.element('ShellMITC4', 396, 139, 144, 143, 138, 701)
    ops.element('ShellMITC4', 397, 138, 143, 142, 137, 701)
    ops.element('ShellMITC4', 398, 137, 142, 141, 136, 701)
    ops.element('ShellMITC4', 399, 136, 141, 140, 135, 701)
    ops.element('ShellMITC4', 400, 144, 149, 148, 143, 701)
    ops.element('ShellMITC4', 401, 143, 148, 147, 142, 701)
    ops.element('ShellMITC4', 402, 142, 147, 146, 141, 701)
    ops.element('ShellMITC4', 403, 141, 146, 145, 140, 701)
    ops.element('ShellMITC4', 404, 149, 154, 153, 148, 701)
    ops.element('ShellMITC4', 405, 148, 153, 152, 147, 701)
    ops.element('ShellMITC4', 406, 147, 152, 151, 146, 701)
    ops.element('ShellMITC4', 407, 146, 151, 150, 145, 701)
    ops.element('ShellMITC4', 408, 154, 159, 158, 153, 701)
    ops.element('ShellMITC4', 409, 153, 158, 157, 152, 701)
    ops.element('ShellMITC4', 410, 152, 157, 156, 151, 701)
    ops.element('ShellMITC4', 411, 151, 156, 155, 150, 701)
    ops.element('ShellMITC4', 412, 159, 164, 163, 158, 701)
    ops.element('ShellMITC4', 413, 158, 163, 162, 157, 701)
    ops.element('ShellMITC4', 414, 157, 162, 161, 156, 701)
    ops.element('ShellMITC4', 415, 156, 161, 160, 155, 701)
    ops.element('ShellMITC4', 416, 164, 169, 168, 163, 701)
    ops.element('ShellMITC4', 417, 163, 168, 167, 162, 701)
    ops.element('ShellMITC4', 418, 162, 167, 166, 161, 701)
    ops.element('ShellMITC4', 419, 161, 166, 165, 160, 701)
    ops.element('ShellMITC4', 420, 169, 174, 173, 168, 701)
    ops.element('ShellMITC4', 421, 168, 173, 172, 167, 701)
    ops.element('ShellMITC4', 422, 167, 172, 171, 166, 701)
    ops.element('ShellMITC4', 423, 166, 171, 170, 165, 701)
    ops.element('ShellMITC4', 424, 174, 179, 178, 173, 701)
    ops.element('ShellMITC4', 425, 173, 178, 177, 172, 701)
    ops.element('ShellMITC4', 426, 172, 177, 176, 171, 701)
    ops.element('ShellMITC4', 427, 171, 176, 175, 170, 701)
    ops.element('ShellMITC4', 428, 179, 184, 183, 178, 701)
    ops.element('ShellMITC4', 429, 178, 183, 182, 177, 701)
    ops.element('ShellMITC4', 430, 177, 182, 181, 176, 701)
    ops.element('ShellMITC4', 431, 176, 181, 180, 175, 701)
    ops.element('ShellMITC4', 432, 184, 189, 188, 183, 701)
    ops.element('ShellMITC4', 433, 183, 188, 187, 182, 701)
    ops.element('ShellMITC4', 434, 182, 187, 186, 181, 701)
    ops.element('ShellMITC4', 435, 181, 186, 185, 180, 701)
    ops.element('ShellMITC4', 436, 189, 190, 191, 188, 701)
    ops.element('ShellMITC4', 437, 188, 191, 192, 187, 701)
    ops.element('ShellMITC4', 438, 187, 192, 193, 186, 701)
    ops.element('ShellMITC4', 439, 186, 193, 194, 185, 701)
