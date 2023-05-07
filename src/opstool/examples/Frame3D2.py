import openseespy.opensees as ops


def Frame3D2():
    print(
        "The original Tcl file comes from http://www.dinochen.com/, "
        "and the Python version is converted by opstool.tcl2py()."
    )
    ops.wipe()
    ops.model("basic", "-ndm", 3, "-ndf", 6)
    ops.node(1, 4500.0, 5000.0, 10500.0)
    ops.node(2, 4500.0, 5000.0, 13500.0)
    ops.node(3, 4500.0, 0.0, 10500.0)
    ops.node(4, 4500.0, 0.0, 13500.0)
    ops.node(5, 0.0, 0.0, 10500.0)
    ops.node(6, 0.0, 0.0, 13500.0)
    ops.node(7, 0.0, 5000.0, 10500.0)
    ops.node(8, 0.0, 5000.0, 13500.0)
    ops.node(9, 4500.0, 0.0, 7500.0)
    ops.node(10, 4500.0, 5000.0, 7500.0)
    ops.node(11, 0.0, 0.0, 7500.0)
    ops.node(12, 0.0, 5000.0, 7500.0)
    ops.node(13, 9000.0, 0.0, 7500.0)
    ops.node(14, 9000.0, 0.0, 10500.0)
    ops.node(15, 9000.0, 5000.0, 7500.0)
    ops.node(16, 9000.0, 5000.0, 10500.0)
    ops.node(17, 4500.0, 0.0, 4500.0)
    ops.node(18, 4500.0, 5000.0, 4500.0)
    ops.node(19, 0.0, 0.0, 4500.0)
    ops.node(20, 0.0, 5000.0, 4500.0)
    ops.node(21, 9000.0, 0.0, 4500.0)
    ops.node(22, 9000.0, 5000.0, 4500.0)
    ops.node(23, 4500.0, 0.0, 0.0)
    ops.node(24, 4500.0, 5000.0, 0.0)
    ops.node(25, 0.0, 0.0, 0.0)
    ops.node(26, 0.0, 5000.0, 0.0)
    ops.node(27, 9000.0, 0.0, 0.0)
    ops.node(28, 9000.0, 5000.0, 0.0)
    ops.mass(1, 8.604, 8.604, 8.604, 0.0, 0.0, 0.0)
    ops.mass(2, 4.302, 4.302, 4.302, 0.0, 0.0, 0.0)
    ops.mass(3, 8.604, 8.604, 8.604, 0.0, 0.0, 0.0)
    ops.mass(4, 4.302, 4.302, 4.302, 0.0, 0.0, 0.0)
    ops.mass(5, 4.302, 4.302, 4.302, 0.0, 0.0, 0.0)
    ops.mass(6, 4.302, 4.302, 4.302, 0.0, 0.0, 0.0)
    ops.mass(7, 4.302, 4.302, 4.302, 0.0, 0.0, 0.0)
    ops.mass(8, 4.302, 4.302, 4.302, 0.0, 0.0, 0.0)
    ops.mass(9, 8.604, 8.604, 8.604, 0.0, 0.0, 0.0)
    ops.mass(10, 8.604, 8.604, 8.604, 0.0, 0.0, 0.0)
    ops.mass(11, 4.302, 4.302, 4.302, 0.0, 0.0, 0.0)
    ops.mass(12, 4.302, 4.302, 4.302, 0.0, 0.0, 0.0)
    ops.mass(13, 4.302, 4.302, 4.302, 0.0, 0.0, 0.0)
    ops.mass(14, 4.302, 4.302, 4.302, 0.0, 0.0, 0.0)
    ops.mass(15, 4.302, 4.302, 4.302, 0.0, 0.0, 0.0)
    ops.mass(16, 4.302, 4.302, 4.302, 0.0, 0.0, 0.0)
    ops.mass(17, 8.604, 8.604, 8.604, 0.0, 0.0, 0.0)
    ops.mass(18, 8.604, 8.604, 8.604, 0.0, 0.0, 0.0)
    ops.mass(19, 4.302, 4.302, 4.302, 0.0, 0.0, 0.0)
    ops.mass(20, 4.302, 4.302, 4.302, 0.0, 0.0, 0.0)
    ops.mass(21, 4.302, 4.302, 4.302, 0.0, 0.0, 0.0)
    ops.mass(22, 4.302, 4.302, 4.302, 0.0, 0.0, 0.0)
    ops.fix(23, 1, 1, 1, 1, 1, 1)
    ops.fix(24, 1, 1, 1, 1, 1, 1)
    ops.fix(25, 1, 1, 1, 1, 1, 1)
    ops.fix(26, 1, 1, 1, 1, 1, 1)
    ops.fix(27, 1, 1, 1, 1, 1, 1)
    ops.fix(28, 1, 1, 1, 1, 1, 1)
    ops.uniaxialMaterial("Elastic", 1, 199900.0)
    ops.uniaxialMaterial("Elastic", 2, 26800.0)
    ops.uniaxialMaterial("Elastic", 3, 199900.0)
    ops.geomTransf("Linear", 1, 1.0, 0.0, 0.0)
    ops.geomTransf("Linear", 2, 1.0, 0.0, 0.0)
    ops.geomTransf("Linear", 3, 1.0, 0.0, 0.0)
    ops.geomTransf("Linear", 4, 1.0, 0.0, 0.0)
    ops.geomTransf("Linear", 5, 0.0, 0.0, 1.0)
    ops.geomTransf("Linear", 6, 0.0, 0.0, 1.0)
    ops.geomTransf("Linear", 7, 0.0, 0.0, 1.0)
    ops.geomTransf("Linear", 8, 0.0, 0.0, 1.0)
    ops.geomTransf("Linear", 9, 1.0, 0.0, 0.0)
    ops.geomTransf("Linear", 10, 1.0, 0.0, 0.0)
    ops.geomTransf("Linear", 11, 1.0, 0.0, 0.0)
    ops.geomTransf("Linear", 12, 1.0, 0.0, 0.0)
    ops.geomTransf("Linear", 13, 1.0, 0.0, 0.0)
    ops.geomTransf("Linear", 14, 1.0, 0.0, 0.0)
    ops.geomTransf("Linear", 15, 0.0, 0.0, 1.0)
    ops.geomTransf("Linear", 16, 0.0, 0.0, 1.0)
    ops.geomTransf("Linear", 17, 0.0, 0.0, 1.0)
    ops.geomTransf("Linear", 18, 0.0, 0.0, 1.0)
    ops.geomTransf("Linear", 19, 0.0, 0.0, 1.0)
    ops.geomTransf("Linear", 20, 0.0, 0.0, 1.0)
    ops.geomTransf("Linear", 21, 0.0, 0.0, 1.0)
    ops.geomTransf("Linear", 22, 1.0, 0.0, 0.0)
    ops.geomTransf("Linear", 23, 1.0, 0.0, 0.0)
    ops.geomTransf("Linear", 24, 1.0, 0.0, 0.0)
    ops.geomTransf("Linear", 25, 1.0, 0.0, 0.0)
    ops.geomTransf("Linear", 26, 1.0, 0.0, 0.0)
    ops.geomTransf("Linear", 27, 1.0, 0.0, 0.0)
    ops.geomTransf("Linear", 28, 0.0, 0.0, 1.0)
    ops.geomTransf("Linear", 29, 0.0, 0.0, 1.0)
    ops.geomTransf("Linear", 30, 0.0, 0.0, 1.0)
    ops.geomTransf("Linear", 31, 0.0, 0.0, 1.0)
    ops.geomTransf("Linear", 32, 0.0, 0.0, 1.0)
    ops.geomTransf("Linear", 33, 0.0, 0.0, 1.0)
    ops.geomTransf("Linear", 34, 0.0, 0.0, 1.0)
    ops.geomTransf("Linear", 35, 1.0, 0.0, 0.0)
    ops.geomTransf("Linear", 36, 1.0, 0.0, 0.0)
    ops.geomTransf("Linear", 37, 1.0, 0.0, 0.0)
    ops.geomTransf("Linear", 38, 1.0, 0.0, 0.0)
    ops.geomTransf("Linear", 39, 1.0, 0.0, 0.0)
    ops.geomTransf("Linear", 40, 1.0, 0.0, 0.0)
    ops.geomTransf("Linear", 41, 0.0, 0.0, 1.0)
    ops.geomTransf("Linear", 42, 0.0, 0.0, 1.0)
    ops.geomTransf("Linear", 43, 0.0, 0.0, 1.0)
    ops.geomTransf("Linear", 44, 0.0, 0.0, 1.0)
    ops.geomTransf("Linear", 45, 0.0, 0.0, 1.0)
    ops.geomTransf("Linear", 46, 0.0, 0.0, 1.0)
    ops.geomTransf("Linear", 47, 0.0, 0.0, 1.0)
    ops.element(
        "elasticBeamColumn",
        1,
        1,
        2,
        160000,
        26800,
        11170,
        3605000000,
        2133000000,
        2133000000,
        1,
    )
    ops.element(
        "elasticBeamColumn",
        2,
        3,
        4,
        160000,
        26800,
        11170,
        3605000000,
        2133000000,
        2133000000,
        2,
    )
    ops.element(
        "elasticBeamColumn",
        3,
        5,
        6,
        160000,
        26800,
        11170,
        3605000000,
        2133000000,
        2133000000,
        3,
    )
    ops.element(
        "elasticBeamColumn",
        4,
        7,
        8,
        160000,
        26800,
        11170,
        3605000000,
        2133000000,
        2133000000,
        4,
    )
    ops.element(
        "elasticBeamColumn",
        5,
        6,
        8,
        180000,
        26800,
        11170,
        3708000000,
        5400000000,
        1350000000,
        5,
    )
    ops.element(
        "elasticBeamColumn",
        6,
        4,
        2,
        180000,
        26800,
        11170,
        3708000000,
        5400000000,
        1350000000,
        6,
    )
    ops.element(
        "elasticBeamColumn",
        7,
        8,
        2,
        150000,
        26800,
        11170,
        2817000000,
        3125000000,
        1125000000,
        7,
    )
    ops.element(
        "elasticBeamColumn",
        8,
        6,
        4,
        150000,
        26800,
        11170,
        2817000000,
        3125000000,
        1125000000,
        8,
    )
    ops.element(
        "elasticBeamColumn",
        9,
        9,
        3,
        160000,
        26800,
        11170,
        3605000000,
        2133000000,
        2133000000,
        9,
    )
    ops.element(
        "elasticBeamColumn",
        10,
        10,
        1,
        160000,
        26800,
        11170,
        3605000000,
        2133000000,
        2133000000,
        10,
    )
    ops.element(
        "elasticBeamColumn",
        11,
        11,
        5,
        240000,
        26800,
        11170,
        7512000000,
        7200000000,
        3200000000,
        11,
    )
    ops.element(
        "elasticBeamColumn",
        12,
        12,
        7,
        240000,
        26800,
        11170,
        7512000000,
        7200000000,
        3200000000,
        12,
    )
    ops.element(
        "elasticBeamColumn",
        13,
        13,
        14,
        240000,
        26800,
        11170,
        7512000000,
        7200000000,
        3200000000,
        13,
    )
    ops.element(
        "elasticBeamColumn",
        14,
        15,
        16,
        240000,
        26800,
        11170,
        7512000000,
        7200000000,
        3200000000,
        14,
    )
    ops.element(
        "elasticBeamColumn",
        15,
        7,
        1,
        150000,
        26800,
        11170,
        2817000000,
        3125000000,
        1125000000,
        15,
    )
    ops.element(
        "elasticBeamColumn",
        16,
        1,
        16,
        150000,
        26800,
        11170,
        2817000000,
        3125000000,
        1125000000,
        16,
    )
    ops.element(
        "elasticBeamColumn",
        17,
        3,
        14,
        150000,
        26800,
        11170,
        2817000000,
        3125000000,
        1125000000,
        17,
    )
    ops.element(
        "elasticBeamColumn",
        18,
        5,
        3,
        150000,
        26800,
        11170,
        2817000000,
        3125000000,
        1125000000,
        18,
    )
    ops.element(
        "elasticBeamColumn",
        19,
        3,
        1,
        180000,
        26800,
        11170,
        3708000000,
        5400000000,
        1350000000,
        19,
    )
    ops.element(
        "elasticBeamColumn",
        20,
        14,
        16,
        180000,
        26800,
        11170,
        3708000000,
        5400000000,
        1350000000,
        20,
    )
    ops.element(
        "elasticBeamColumn",
        21,
        5,
        7,
        180000,
        26800,
        11170,
        3708000000,
        5400000000,
        1350000000,
        21,
    )
    ops.element(
        "elasticBeamColumn",
        22,
        17,
        9,
        160000,
        26800,
        11170,
        3605000000,
        2133000000,
        2133000000,
        22,
    )
    ops.element(
        "elasticBeamColumn",
        23,
        18,
        10,
        160000,
        26800,
        11170,
        3605000000,
        2133000000,
        2133000000,
        23,
    )
    ops.element(
        "elasticBeamColumn",
        24,
        19,
        11,
        240000,
        26800,
        11170,
        7512000000,
        7200000000,
        3200000000,
        24,
    )
    ops.element(
        "elasticBeamColumn",
        25,
        20,
        12,
        240000,
        26800,
        11170,
        7512000000,
        7200000000,
        3200000000,
        25,
    )
    ops.element(
        "elasticBeamColumn",
        26,
        21,
        13,
        240000,
        26800,
        11170,
        7512000000,
        7200000000,
        3200000000,
        26,
    )
    ops.element(
        "elasticBeamColumn",
        27,
        22,
        15,
        240000,
        26800,
        11170,
        7512000000,
        7200000000,
        3200000000,
        27,
    )
    ops.element(
        "elasticBeamColumn",
        28,
        12,
        10,
        150000,
        26800,
        11170,
        2817000000,
        3125000000,
        1125000000,
        28,
    )
    ops.element(
        "elasticBeamColumn",
        29,
        10,
        15,
        150000,
        26800,
        11170,
        2817000000,
        3125000000,
        1125000000,
        29,
    )
    ops.element(
        "elasticBeamColumn",
        30,
        9,
        13,
        150000,
        26800,
        11170,
        2817000000,
        3125000000,
        1125000000,
        30,
    )
    ops.element(
        "elasticBeamColumn",
        31,
        11,
        9,
        150000,
        26800,
        11170,
        2817000000,
        3125000000,
        1125000000,
        31,
    )
    ops.element(
        "elasticBeamColumn",
        32,
        9,
        10,
        180000,
        26800,
        11170,
        3708000000,
        5400000000,
        1350000000,
        32,
    )
    ops.element(
        "elasticBeamColumn",
        33,
        13,
        15,
        180000,
        26800,
        11170,
        3708000000,
        5400000000,
        1350000000,
        33,
    )
    ops.element(
        "elasticBeamColumn",
        34,
        11,
        12,
        180000,
        26800,
        11170,
        3708000000,
        5400000000,
        1350000000,
        34,
    )
    ops.element(
        "elasticBeamColumn",
        35,
        23,
        17,
        160000,
        26800,
        11170,
        3605000000,
        2133000000,
        2133000000,
        35,
    )
    ops.element(
        "elasticBeamColumn",
        36,
        24,
        18,
        160000,
        26800,
        11170,
        3605000000,
        2133000000,
        2133000000,
        36,
    )
    ops.element(
        "elasticBeamColumn",
        37,
        25,
        19,
        240000,
        26800,
        11170,
        7512000000,
        7200000000,
        3200000000,
        37,
    )
    ops.element(
        "elasticBeamColumn",
        38,
        26,
        20,
        240000,
        26800,
        11170,
        7512000000,
        7200000000,
        3200000000,
        38,
    )
    ops.element(
        "elasticBeamColumn",
        39,
        27,
        21,
        240000,
        26800,
        11170,
        7512000000,
        7200000000,
        3200000000,
        39,
    )
    ops.element(
        "elasticBeamColumn",
        40,
        28,
        22,
        240000,
        26800,
        11170,
        7512000000,
        7200000000,
        3200000000,
        40,
    )
    ops.element(
        "elasticBeamColumn",
        41,
        20,
        18,
        150000,
        26800,
        11170,
        2817000000,
        3125000000,
        1125000000,
        41,
    )
    ops.element(
        "elasticBeamColumn",
        42,
        18,
        22,
        150000,
        26800,
        11170,
        2817000000,
        3125000000,
        1125000000,
        42,
    )
    ops.element(
        "elasticBeamColumn",
        43,
        17,
        21,
        150000,
        26800,
        11170,
        2817000000,
        3125000000,
        1125000000,
        43,
    )
    ops.element(
        "elasticBeamColumn",
        44,
        19,
        17,
        150000,
        26800,
        11170,
        2817000000,
        3125000000,
        1125000000,
        44,
    )
    ops.element(
        "elasticBeamColumn",
        45,
        17,
        18,
        180000,
        26800,
        11170,
        3708000000,
        5400000000,
        1350000000,
        45,
    )
    ops.element(
        "elasticBeamColumn",
        46,
        21,
        22,
        180000,
        26800,
        11170,
        3708000000,
        5400000000,
        1350000000,
        46,
    )
    ops.element(
        "elasticBeamColumn",
        47,
        19,
        20,
        180000,
        26800,
        11170,
        3708000000,
        5400000000,
        1350000000,
        47,
    )
