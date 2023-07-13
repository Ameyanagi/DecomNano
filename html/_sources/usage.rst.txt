=====
Usage
=====

Command Line Interface
~~~~~~~~~~~~~~~~~~~~~~

The decomnano package comes with a command line interface (CLI) that can be used to run the analysis. The configuration file can be found in the `examples`_ directory. Download the configuration file and run the following command.

.. _examples: https://github.com/Ameyanagi/DecomNano/tree/main/examples

.. code-block:: bash

    decomnano -c sweep_example.toml -o sweep_results.csv

The results will be saved in the `sweep_results.csv` file.

The configuration file is a TOML file. The following parameters can be set in the configuration file.

.. code-block:: toml

    # Example configuration file for DecomNano

    # Single run is done if sweep is false
    # Sweep is done if sweep is true
    sweep = true

    # You can specify the output file name. If not specified, the default name is "results.csv"
    output = "sweep_results.csv"

    [input]
    # input section is used for input of DecomNano if sweep is false
    # input section is used for input_default of SweepDecomNano if sweep is true
    dP=2.77
    dA=2.88
    fA=0.8
    nAA=6.2
    nPP=9.8
    nAP=0.5
    nPA=0.53
    DA=0
    DAP=18
    DP=0

    [input_config]
    # Input_config section is used for defining the sweep range of each parameter.
    # It is required if sweep is true.
    # It will be ignored if sweep is false.# Accepted types are number, list and dictionary.
    # A dictionary will require start, end and step, and will generate a list of range(start, end, step). end is not included as in range() function in python.
    nAA=0.1                                 
    DAP=[16, 17, 18]                        
    DA={start=0, end=2, step=1}           

The variables in the input dictionary different from the paper due to the naming rules of python. Following table shows the correspondence between the variables in the paper and the input dictionary.

        +-------------------------------------------+------------+-----------------------------------------------------------------------+
        | Notation in paper                         | Keys       | Descriptions                                                          |
        +===========================================+============+=======================================================================+
        |:math:`d_P`                                | dP         | Interatomic spacing of Pt nanoparticles                               |
        +-------------------------------------------+------------+-----------------------------------------------------------------------+
        |:math:`d_A`                                | dA         | Interatomic spacing of Au nanoparticles                               |
        +-------------------------------------------+------------+-----------------------------------------------------------------------+
        |:math:`\frac{M_A}{M_A + M_P}`              | fA         | Molar fraction of Au                                                  |
        +-------------------------------------------+------------+-----------------------------------------------------------------------+
        |:math:`n_{A-A}`                            | nAA        | Total first nearest neighbor coordination number of Au-Au bonds.      |
        +-------------------------------------------+------------+-----------------------------------------------------------------------+
        |:math:`n_{P-P}`                            | nPP        | Total first nearest neighbor coordination number of Pt-Pt bonds.      |
        +-------------------------------------------+------------+-----------------------------------------------------------------------+
        |:math:`n_{A-P}`                            | nAP        | Total first nearest neighbor coordination number of Au-Pt bonds.      |
        +-------------------------------------------+------------+-----------------------------------------------------------------------+
        |:math:`n_{P-A}`                            | nPA        | Total first nearest neighbor coordination number of Pt-Au bonds.      |
        +-------------------------------------------+------------+-----------------------------------------------------------------------+
        |:math:`D_A`                                | DA         | Diameter of Au nanoparticles                                          |
        +-------------------------------------------+------------+-----------------------------------------------------------------------+
        |:math:`D_{AP}`                             | DAP        | Diameter of PtAu nanoparticles                                        |
        +-------------------------------------------+------------+-----------------------------------------------------------------------+
        |:math:`D_P`                                | DP         | Diameter of Pt nanoparticles                                          |
        +-------------------------------------------+------------+-----------------------------------------------------------------------+
 

Python API
~~~~~~~~~~

The decomanano package can be imported and used in python scripts.
Please refer to the `API documentation`_ for details.

.. _API documentation: https://ameyanagi.github.io/DecomNano/modules.html