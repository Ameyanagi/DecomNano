=========
DecomNano
=========


.. image:: https://img.shields.io/pypi/v/decomnano.svg
        :target: https://pypi.python.org/pypi/decomnano

.. image:: https://img.shields.io/travis/Ameyanagi/decomnano.svg
        :target: https://travis-ci.com/Ameyanagi/decomnano

.. image:: https://ameyanagi.github.io/DecomNano/index.html
        :target: https://github.com/Ameyanagi/DecomNano/actions/workflows/documentation.yaml/badge.svg
        :alt: Documentation Status

DecomNano is a heterogeneity analysis of bimetallic nanoparticles using coordination numbers obtained from XAS analysis.


* Free software: MIT license
* Documentation: https://ameyanagi.github.io/DecomNano/index.html.

Requirements
------------

DecomNano requires Mathematica_ for solving non-liner equations. Please install Mathematica_ or `Wolfram Engine`_.\n
Other requirements for python can be installed by pip command.

.. _Mathematica: https://www.wolfram.com/mathematica/
.. _Wolfram Engine: https://www.wolfram.com/engine/

.. code-block:: bash

    pip install -r requirements.txt

Installation
------------

Detailed instructions for installation are available in the `installation documentation`_.

.. _installation documentation: https://ameyanagi.github.io/DecomNano/installation.html

Installation from PyPI
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    pip install decomnano

Installation from source
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    pip install git+https://github.com/Ameyanagi/DecomNano

or clone the repository and install from local source.

.. code-block:: bash

    git clone https://github.com/Ameyanagi/DecomNano
    cd DecomNano
    pip install .

Usage
-----

Command Line Interface
~~~~~~~~~~~~~~~~~~~~~~

Detailed instructions for usage are available in the `usage documentation`_.

.. _usage documentation: https://ameyanagi.github.io/DecomNano/usage.html

The decomnano package comes with a command line interface (CLI) that can be used to run the analysis. The configuration file can be found in the `examples`_ directory. Download the configuration file and run the following command.

.. _examples: https://github.com/Ameyanagi/DecomNano/tree/main/examples

.. code-block:: bash

    decomnano -c sweep_example.toml -o sweep_results.csv

The results will be saved in the `sweep_results.csv` file.

Python API
~~~~~~~~~~

Detailed instructions for usage are available in the `API documentation`_.
The decomanano package can be imported and used in python scripts.

.. _API documentation: https://ameyanagi.github.io/DecomNano/modules.html

Citation
--------

If you use DecomNano in your research, please cite the following paper: to be submitted.
