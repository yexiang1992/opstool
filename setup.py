from setuptools import find_packages, setup

from src.opstool import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='opstool',
    version=__version__,
    description='openseespy toolbox',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Yexiang Yan',
    author_email='yexiang_yan@outlook.com',
    url='https://github.com/yexiang1992',
    license='GPL Licence',
    keywords='OpenSees Visualization Seismic Simulation',
    platforms='any',
    python_requires='>=3.8.*',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    install_requires=[
        'matplotlib',
        'numpy',
        'openseespy>=3.4.0.1',
        'plotly',
        'pyvista>=0.38.2',
        'sectionproperties>=2.1.5',
        'shapely>=2.0.0',
        'h5py',
        'rich',
        "triangle"
    ],
)
