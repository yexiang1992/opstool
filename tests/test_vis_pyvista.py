import opstool as opst
import opstool.vis.pyvista as opsvis
from pyvista.plotting.plotter import Plotter


def test_set_plot_props():
    assert opsvis.set_plot_props() is None


def test_set_plot_colors():
    assert opsvis.set_plot_colors() is None


def test_plot_model_link():
    opst.load_ops_examples("ArchBridge")
    output = opsvis.plot_model(
        show_node_numbering=True,
        show_ele_numbering=True,
        show_link=True,
        show_local_axes=True,
    )
    assert isinstance(output, Plotter)


def test_plot_model_shell():
    opst.load_ops_examples("Shell3D")
    output = opsvis.plot_model(
        show_node_numbering=True, show_ele_numbering=True, show_local_axes=True
    )
    assert isinstance(output, Plotter)


def test_plot_model_brick():
    opst.load_ops_examples("Pier-Brick")
    output = opsvis.plot_model(show_node_numbering=True, show_ele_numbering=True)
    assert isinstance(output, Plotter)


def test_plot_eigen_subplots():
    opst.load_ops_examples("ArchBridge-2")
    output = opsvis.plot_eigen(mode_tags=3, subplots=True)
    assert isinstance(output, Plotter)


def test_plot_eigen_slides():
    opst.load_ops_examples("Pier-Brick")
    output = opsvis.plot_eigen(mode_tags=3, subplots=False)
    assert isinstance(output, Plotter)
