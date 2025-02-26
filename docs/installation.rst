Installation
============

Using pip
---------

.. code-block:: bash

    pip install opstool

Or upgrade:

.. code-block:: bash

    pip install --upgrade opstool

.. note::

   Since version **1.0.1**, this package has undergone major updates, including numerous new features and changes to the API!


Some Tips
-----------

1. **Recommended Installation Environment**: To simplify package management and ensure compatibility, we strongly recommend using the Anaconda distribution. Anaconda provides a well-managed Python environment, making it easier to install compatible versions of OpenSeesPy and its dependencies. Users can set up a dedicated environment as follows:

.. code-block:: bash

    conda create -n opensees-workspace python=3.12
    conda activate opensees-workspace
    pip install openseespy
    pip install opstool


2. **OpenSeesPy Version Compatibility**: ``opstool`` does not impose a strict ``OpenSeesPy`` version requirement, but it utilizes some functionalities introduced in newer OpenSeesPy releases. Therefore, **for Windows and Linux users, we recommend using the latest OpenSeesPy version to ensure full compatibility**.

3. **Python Version Dependency on Windows**: *OpenSeesPy has a strong dependency on the Python version on Windows*, as it is compiled using specific Python headers. Users should ensure their Python version aligns with OpenSeesPy’s requirements to maintain compatibility. For instance, the latest OpenSeesPy 3.7.0 requires Python 3.12 on Windows.

4. **Python Version Requirement for opstool**: Since opstool uses Python 3.10+ syntax features, installation requires **Python 3.10 or later** to ensure compatibility.

5. **Mac Compatibility**: The OpenSeesPy Mac version is independently maintained, and based on `PyPI records <https://pypi.org/project/openseespymac/>`_, it has not been updated for a long time. Since opstool does not explicitly specify an OpenSeesPy version, Mac users encountering installation issues may try **upgrading to Python 3.10+**. *However, OpenSeesPy versions on Mac may lack functionalities introduced in OpenSees 3.4.0 later, which could lead to some features being unavailable.*

