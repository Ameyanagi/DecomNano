from decomnano import DecomNano
import numpy as np
import itertools
from tqdm import tqdm


class SweepDecomNano(object):
    r"""SweepDecomNano class for calculating decomnano with various input parameters.

    Args:
        wolfam_kernel (str): Path to the Wolfram kernel. Defaults to None, which uses the default kernel.

    Attributes:
        dn (DecomNano): DecomNano class for calculating decomnano.
        input (dict): Current input parameters used for calculating DecomNano solver.
        input_default (dict): Default input parameters used for calculating DecomNano solver. input will be generated by updating input_default with input_config.
        input_config (dict): Configuration of input range parameters used for calculating DecomNano solver. input_default will be generated by updating input_default with range specified in input_config. The range of input parameters can be specified by list or numpy array. If the range is specified by list or numpy array, the input parameters varies from the minimum value to the maximum value with the step size of the difference between the maximum value and the minimum value divided by the number of elements in the list or numpy array minus 1. If the range is specified by a single value, the input parameters will be varied from range(input_default-value, input_default+value, resolution). The resolution is set to 0.1 by default.

    Examples:
        >>> from decomnano import SweepDecomNano
        >>> sd = SweepDecomNano()
        >>> sd.calc_sweep("sweep_results")
        >>> Pt40Au60BP1_input_default = dict(
                RPt = 2.77,
                RAu = 2.88,
                fAu = 0.6,
                nAuAu = 4.2,
                nPtPt = 10.0,
                nAuPt = 2.8,
                nPtAu = 0.71,
                DA = 10,
                DAP = 17,
                DP = 17,
            )
        >>> Pt40Au60BP1_input_config = dict(
                nAuAu = 0.6,
                nPtPt = 0.7,
                nAuPt = 0.5,
                nPtAu = 0.8,
                DP = list(range(0, 18, 2)),
                DA = list(range(0, 18, 2))
                )
        >>> sd.update_input_default(Pt40Ag60BP1_input_default)
        >>> sd.update_input_config(Pt40Ag60BP1_input_config)
        >>> sd.calc_sweep("sweep_results.csv")

    Note:
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
        |:math:`n_{A-M,AP}`                         | nAM_AP     | First nearest neighbor coordination number of Au-metal bonds          |
        +-------------------------------------------+------------+-----------------------------------------------------------------------+
        |:math:`n_{P-M,AP}`                         | nPM_AP     | First nearest neighbor coordination number of Pt-metal bonds          |
        +-------------------------------------------+------------+-----------------------------------------------------------------------+
        |:math:`n_{A-A,AP}`                         | nAA_AP     | First nearest neighbor coordination number of Au-Au bonds             |
        +-------------------------------------------+------------+-----------------------------------------------------------------------+
        |:math:`n_{A-P,AP}`                         | nAP_AP     | First nearest neighbor coordination number of Au-Pt bonds             |
        +-------------------------------------------+------------+-----------------------------------------------------------------------+
        |:math:`n_{P-A,AP}`                         | nPA_AP     | First nearest neighbor coordination number of Pt-Au bonds             |
        +-------------------------------------------+------------+-----------------------------------------------------------------------+
        |:math:`n_{P-P,AP}`                         | nPP_AP     | First nearest neighbor coordination number of Pt-Pt bonds             |
        +-------------------------------------------+------------+-----------------------------------------------------------------------+
        |:math:`X_A`                                | XA         | Molar ratio of Au nanoparticles                                       |
        +-------------------------------------------+------------+-----------------------------------------------------------------------+
        |:math:`X_{AP}`                             | XAP        | Molar ratio of PtAu nanoparticles                                     |
        +-------------------------------------------+------------+-----------------------------------------------------------------------+
        |:math:`X_P`                                | XP         | Molar ratio of Pt nanoparticles                                       |
        +-------------------------------------------+------------+-----------------------------------------------------------------------+
        |:math:`y`                                  | y          | Molar fraction of Au in PtAu nanoparticles                            |
        +-------------------------------------------+------------+-----------------------------------------------------------------------+
    """

    def __init__(
        self,
        wolfram_kernel=None,
        input_default=None,
        input_config=None,
        fix_bulk_fraction=False,
        respawn_interval=10000,
        hollow_shell=False,
    ):
        self.respawn_interval = respawn_interval
        self.fix_bulk_fraction = fix_bulk_fraction
        self.hollow_shell = hollow_shell

        self.dn = DecomNano(
            wolfram_kernel=wolfram_kernel,
            fix_bulk_fraction=fix_bulk_fraction,
            hollow_shell=hollow_shell,
        )
        self.init_input(input_default=input_default, input_config=input_config)
        self.calc_input_range()

    def init_input(self, input_default=None, input_config=None):
        """Initialize input parameters for calculating DecomNano solver. Called in __init__()."""
        self.input = dict(
            dP=2.77,
            dA=2.88,
            fA=0.8,
            nAA=6.5,
            nPP=9.9,
            nAP=0.6,
            nPA=1.13,
            DA=0,
            DAP=18,
            DP=5,
        )

        self.input_default = dict(
            dP=2.77,
            dA=2.88,
            fA=0.8,
            nAA=6.5,
            nPP=9.9,
            nAP=0.6,
            nPA=1.13,
            DA=10,
            DAP=18,
            DP=18,
        )

        if input_default is not None:
            self.input_default.update(input_default)

        if input_config is None:
            self.input_config = dict(
                nAA=0.5,
                nPP=0.7,
                nAP=0.5,
                nPA=0.8,
                DA=list(range(11)),
            )
        else:
            self.input_config = input_config

    def update_input_default(self, input_default, resolution=0.1):
        """Update input_default and calculate input_range. Copies input_default to self.input_default and calculates input_range.

        Args:
            input_default (dict): Dictionary to replace input_default.
            resolution (float): Resolution of input_range. Defaults to 0.1. input_default will be generated by updating input_default with range specified in input_config. The range of input parameters can be specified by list or numpy array. If the range is specified by list or numpy array, the input parameters varies from the minimum value to the maximum value with the step size of the difference between the maximum value and the minimum value divided by the number of elements in the list or numpy array minus 1. If the range is specified by a single value, the input parameters will be varied from range(input_default-value, input_default+value, resolution). The resolution is set to 0.1 by default.
        """
        self.input_default = input_default.copy()
        self.calc_input_range(resolution=resolution)

    def update_input_config(self, input_config, resolution=0.1):
        """Update input_config and calculate input_range. Copies input_config to self.input_config and calculates input_range.

        Args:
            input_config (dict): Dictionary to replace input_config.
            resolution (float): Resolution of input_range. Defaults to 0.1. input_default will be generated by updating input_default with range specified in input_config. The range of input parameters can be specified by list or numpy array. If the range is specified by list or numpy array, the input parameters varies from the minimum value to the maximum value with the step size of the difference between the maximum value and the minimum value divided by the number of elements in the list or numpy array minus 1. If the range is specified by a single value, the input parameters will be varied from range(input_default-value, input_default+value, resolution). The resolution is set to 0.1 by default.
        """
        self.input_config = input_config.copy()
        self.calc_input_range(resolution=resolution)

    def update_input_from_list(self, input_list, label=None):
        """Update input from list.

        Args:
            input_list (list): List of input parameters.
            label (list): List of labels for input parameters. Defaults to None. If label is None, the order of input parameters should be the same as the order of input parameters in self.input. If label is not None, the order of input parameters should be the same as the order of labels.
        """

        if label is not None:
            for i in range(len(input_list)):
                self.input[label[i]] = input_list[i]
        else:
            keys = list(self.input.keys())
            for i in range(len(self.input)):
                self.input[keys[i]] = input_list[i]

    def update_input(self, input_dict):
        """Update input from dictionary.

        Args:
            input_dict (dict): Dictionary of input parameters.
        """
        self.input.update(input_dict)

    def calc_input_range(self, resolution=0.1):
        """Calculate input_range from input_default and input_config.

        Args:
            resolution (float): Resolution of input_range. Defaults to 0.1. input_default will be generated by updating input_default with range specified in input_config. The range of input parameters can be specified by list or numpy array. If the range is specified by list or numpy array, the input parameters varies from the minimum value to the maximum value with the step size of the difference between the maximum value and the minimum value divided by the number of elements in the list or numpy array minus 1. If the range is specified by a single value, the input parameters will be varied from range(input_default-value, input_default+value, resolution). The resolution is set to 0.1 by default.
        """

        input_range = {}

        for key in self.input_default:
            input_range[key] = np.array([self.input_default[key]])

        for key in self.input_config:
            if type(self.input_config[key]) == list:
                input_range[key] = self.input_config[key]
            elif type(self.input_config[key]) == np.ndarray:
                input_range[key] = self.input_config[key]
            elif type(self.input_config[key]) == float:
                input_range[key] = np.round(
                    np.arange(
                        max(0.0, self.input_default[key] - self.input_config[key]),
                        self.input_default[key] + self.input_config[key] + 0.1,
                        resolution,
                    ),
                    decimals=2,
                )
            elif type(self.input_config[key]) == int:
                input_range[key] = np.arange(
                    max(0, self.input_default[key] - self.input_config[key]),
                    self.input_default[key] + self.input_config[key] + 1,
                )
            else:
                pass

        self.input_range = input_range.copy()

    def print_input_range(self):
        """Print input_range."""
        print(self.input_range)

    def calc_sweep(self, savepath="result.csv", save_interval=100):
        """Calculate DecomNano solver with sweep of input parameters.

        Args:
            savepath (str): Path to save results. Defaults to "result.csv".
            save_interval (int): Interval of saving results. The results will be saved after each save_interval. Defaults to 100.
        """

        labels = list(self.input_range.keys())

        input_range_list = []

        for key in labels:
            input_range_list.append(self.input_range[key])

        input_iteration = itertools.product(*input_range_list)

        num = 0
        for input in tqdm(input_iteration):
            self.update_input_from_list(input, labels)
            self.dn.calc_decomnano(**self.input)

            # num = num % save_interval

            if num % save_interval == 0:
                self.dn.print_input()
                self.dn.save_results(savepath)

            if num % self.respawn_interval == 0:
                self.dn.respawn_kernel()

            num = num + 1

        self.dn.print_input()
        self.dn.save_results(savepath)

    def calc_sweep_const_2param(
        self, parameters=["DA", "DP"], savepath="result.csv", save_interval=100
    ):
        """Calculate DecomNano solver with sweep of input parameters with constraining two parameters to be the same.

        Args:
            parameters (list): List of two parameters to be constrained to be the same. Defaults to ["DA", "DP"]. Input config of the first parameter will be applied to the second parameter.
            savepath (str): Path to save results. Defaults to "result.csv".
            save_interval (int): Interval of saving results. The results will be saved after each save_interval. Defaults to 100.

        Examples:
            >>> # To constrain DA = DP, run
            >>> sd.calc_sweep_const_2param(["DA", "DP"], savepath, save_interval=100)
        """

        if len(parameters) != 2:
            raise ValueError("parameters should be a list of two strings")

        labels = list(self.input_range.keys())

        # remove parameter[1] from labels
        labels.remove(parameters[1])
        index_param0 = labels.index(parameters[0])

        input_range_list = []

        for key in labels:
            input_range_list.append(self.input_range[key])

        input_iteration = itertools.product(*input_range_list)

        num = 0
        for input in tqdm(input_iteration):
            self.update_input_from_list(input, labels)

            # update input to constrain parameters[1] to be the same as parameters[0]
            self.update_input({parameters[1]: input[index_param0]})
            self.dn.calc_decomnano(**self.input)

            # num = num % save_interval

            if num % save_interval == 0:
                self.dn.print_input()
                self.dn.save_results(savepath)

            if num % self.respawn_interval == 0:
                self.dn.respawn_kernel()

            num = num + 1

        self.dn.print_input()
        self.dn.save_results(savepath)

    def terminate(self):
        """Terminate DecomNano solver."""
        self.dn.terminate()

    def __del__(self):
        """Terminate DecomNano solver."""
        self.terminate()
