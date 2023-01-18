# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
from pathlib import Path

import plotly.io as pio

# import pyvista as pv
# pv.set_jupyter_backend('pythreejs')
# pio.renderers = 'jupyterlab'
pio.renderers = 'notebook'

# from unittest.mock import MagicMock


# class Mock(MagicMock):
#     @classmethod
#     def __getattr__(cls, name):
#         return MagicMock()


# MOCK_MODULES = [
#     'numpy',
#     # 'scipy',
#     # 'sklearn',
#     'matplotlib',
#     'shapely',
#     'Sphinx',
#     'sphinx-rtd-theme',
#     'sphinx-gallery',
#     'sphinxcontrib-napoleon',
#     'sphinx-autodoc-typehints',
#     'nbsphinx',
#     'cad_to_shapely',
#     'openseespy',
#     'plotly',
#     'sectionproperties',
# ]
# sys.modules.update((mod_name, Mock()) for mod_name in MOCK_MODULES)

this_dir = Path(__file__).resolve().parent.parent.parent
about = {}
with open(this_dir / "src" / "opstool" / "__about__.py") as f:
    d = exec(f.read(), about)
__version__ = about["__version__"]

sys.path.insert(0, os.path.abspath('../../src'))


# -- Project information -----------------------------------------------------

project = 'opstool'
copyright = '2022, Yexiang Yan'
author = 'Yexiang Yan'

# The full version, including alpha/beta/rc tags
release = __version__


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.mathjax",
    "sphinx.ext.viewcode",
    # "sphinx_gallery.gen_gallery",
    'nbsphinx',
    "jupyter_sphinx",
    'sphinx_copybutton',
]

# The master toctree document.
master_doc = "index"

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['../../src/opstool/examples', 'opstool.examples.rst']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# html_theme = 'alabaster'
# html_theme = 'sphinx_rtd_theme'
html_theme = 'pydata_sphinx_theme'
html_static_path = ["_static"]
html_theme_options = {
    "show_prev_next": False,
    # "google_analytics_id": 'UA-141840477-1',
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/yexiang1992/opstool",
            "icon": "fab fa-github",
            "type": "fontawesome",
        },
        {
            "name": "PyPi",
            "url": "https://pypi.org/project/opstool/",
            "icon": "fas fa-box-open",
            "type": "fontawesome",
        }
    ],
    "logo": {
        "image_light": "logo_white.png",
        "image_dark": "logo_dark.png",
    }
}

html_sidebars = {
    "index": ["search-field", "sidebar_index"],
    # "gallery/*": []
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Output file base name for HTML help builder.
htmlhelp_basename = "opstooldoc"

# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',
    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',
    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',
    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (
        master_doc,
        "opstool.tex",
        "opstool Documentation",
        "Yexiang Yan",
        "manual",
    ),
]

# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, "opstool",
     "opstool Documentation", [author], 1)
]

# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (
        master_doc,
        "opstool",
        "opstool Documentation",
        author,
        "opstool",
        "One line description of project.",
        "Miscellaneous",
    ),
]
