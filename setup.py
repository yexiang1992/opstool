from setuptools import find_packages, setup

from src.opstool import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='opstool',
    version=__version__,
    description='opensees toolbox',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Yexiang Yan',
    author_email='yexiang_yan@outlook.com',
    url='https://github.com/yexiang1992',
    license='GPL Licence',
    keywords='OpenSees seismic visualization',
    platforms='any',
    python_requires='>=3.9.*',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    install_requires=[
        'matplotlib',
        'numpy',
        'openseespy',
        'plotly',
        'pyvista',
        'sectionproperties',
        'shapely>=2.0.0',
        'h5py',
        'rich'
    ],
)
