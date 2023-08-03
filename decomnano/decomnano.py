"""Main module."""

from wolframclient.evaluation import WolframLanguageSession
from wolframclient.language import wl, wlexpr
import re
import pandas as pd
import os

current_dir = os.path.dirname(os.path.abspath(__file__))


class DecomNano(object):
    r"""DecomNano class for solving the heterogeneity analysis of bimetallic nanoparticles using coordination numbers obtained from XAS analysis.

    Args:
        wolfram_kernel (str): Path to the Wolfram kernel. Defaults to None, which searches system default.
        input (dict): Input dictionary for the heterogeneity analysis. Defaults are {"dP": 2.77, "dA": 2.88, "fA": 0.2, "nAA": 6.5, "nPP": 9.9, "nAP": 0.6, "nPA": 1.13, "DA": 0, "DAP": 18, "DP": 5}.

    Attributes:
        session (WolframLanguageSession): Wolfram Language session
        input (dict): Input dictionary for the heterogeneity analysis. Defaults are {"dP": 2.77, "dA": 2.88, "fA": 0.2, "nAA": 6.5, "nPP": 9.9, "nAP": 0.6, "nPA": 1.13, "DA": 0, "DAP": 18, "DP": 5}.
        results (pd.DataFrame): Results of the heterogeneity analysis
        column (list): Column names of the results
        dict_regex (re.Pattern): Regular expression for converting the mathematica results to a dictionary

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

    """Template for the function call in Mathematica"""
    decomnano_equation = (
        "DecomNano[{dP}, {dA}, {fA}, {nAA}, {nPP}, {nAP}, {nPA}, {DA}, {DAP}, {DP}]"
    )

    decomnano_equation_hollow = "DecomNanoh[{dP}, {dA}, {fA}, {nAA}, {nPP}, {nAP}, {nPA}, {DA}, {DAP}, {DP}, {DAPh}]"

    column = [
        "dP",
        "dA",
        "fA",
        "nAA",
        "nPP",
        "nAP",
        "nPA",
        "DA",
        "DAP",
        "DP",
        "nAM_AP",
        "nPM_AP",
        "nAA_AP",
        "nAP_AP",
        "nPA_AP",
        "nPP_AP",
        "XAP",
        "XA",
        "XP",
        "y",
    ]

    column_hollow = [
        "dP",
        "dA",
        "fA",
        "nAA",
        "nPP",
        "nAP",
        "nPA",
        "DA",
        "DAP",
        "DP",
        "DAPh",
        "nAM_AP",
        "nPM_AP",
        "nAA_AP",
        "nAP_AP",
        "nPA_AP",
        "nPP_AP",
        "XAP",
        "XA",
        "XP",
        "y",
    ]

    def __init__(
        self,
        wolfram_kernel=None,
        input=None,
        fix_bulk_fraction=False,
        hollow_shell=False,
    ):
        self.wolfram_kernel = wolfram_kernel
        self.session = WolframLanguageSession(kernel=self.wolfram_kernel)
        self.fix_bulk_fraction = fix_bulk_fraction
        self.hollow_shell = hollow_shell

        if self.fix_bulk_fraction:
            if self.hollow_shell:
                self.session.evaluate(
                    wl.Get(
                        os.path.join(
                            current_dir, "decomnano_fix_bulk_fraction_hollow_shell.wl"
                        )
                    )
                )
            else:
                self.session.evaluate(
                    wl.Get(os.path.join(current_dir, "decomnano_fix_bulk_fraction.wl"))
                )
        else:
            self.session.evaluate(wl.Get(os.path.join(current_dir, "decomnano.wl")))
        self.results = pd.DataFrame()
        self.dict_regex = re.compile(r"Rule\[Global`(.*?), (.*?)]")

        if self.hollow_shell:
            self.column = self.column_hollow
        else:
            self.column = self.column

        self.input = dict(
            dP=2.77,
            dA=2.88,
            fA=0.2,
            nAA=6.5,
            nPP=9.9,
            nAP=0.6,
            nPA=1.13,
            DA=0,
            DAP=18,
            DP=5,
        )

        if input is not None:
            self.input.update(input)

    def respawn_kernel(self):
        if self.session is not None:
            self.session.terminate()

        self.session = WolframLanguageSession(kernel=self.wolfram_kernel)

        if self.fix_bulk_fraction:
            if self.hollow_shell:
                self.session.evaluate(
                    wl.Get(
                        os.path.join(
                            current_dir, "decomnano_fix_bulk_fraction_hollow_shell.wl"
                        )
                    )
                )
            else:
                self.session.evaluate(
                    wl.Get(os.path.join(current_dir, "decomnano_fix_bulk_fraction.wl"))
                )
        else:
            self.session.evaluate(wl.Get(os.path.join(current_dir, "decomnano.wl")))

    def init_input(self, **kwargs):
        """Initialize the input dictionary of DecomNano class.

        Args:
            **kwargs: Keyword arguments for the input dictionary. Defaults are {"dP": 2.77, "dA": 2.88, "fA": 0.2, "nAA": 6.5, "nPP": 9.9, "nAP": 0.6, "nPA": 1.13, "DA": 0, "DAP": 18, "DP": 5}.

        Examples:
            >>> dn = DecomNano()
            >>> dn.init_input(RPt=2.77, RAu=2.88, fAu=0.2, nAuAu=6.5, nPtPt=9.9, nAuPt=0.6, nPtAu=1.13, DA=0, DAP=18, DP=5)
        """
        self.input = dict(
            dP=2.77,
            dA=2.88,
            fA=0.2,
            nAA=6.5,
            nPP=9.9,
            nAP=0.6,
            nPA=1.13,
            DA=0,
            DAP=18,
            DP=5,
            DAPh=0,
        )

        self.input.update(kwargs)

    def calc_decomnano(self, **kwargs):
        """Initialize and solve the heterogeneity analysis of bimetallic nanoparticles using coordination numbers obtained from XAS analysis.

        Args:
            **kwargs: Keyword arguments for the input dictionary. Defaults are {"dP": 2.77, "dA": 2.88, "fA": 0.2, "nAA": 6.5, "nPP": 9.9, "nAP": 0.6, "nPA": 1.13, "DA": 0, "DAP": 18, "DP": 5}.

        Examples:
            >>> dn = DecomNano()
            >>> dn.calc_decomnano(RPt=2.77, RAu=2.88, fAu=0.2, nAuAu=6.5, nPtPt=9.9, nAuPt=0.6, nPtAu=1.13, DA=0, DAP=18, DP=5)
        """
        self.input.update(**kwargs)
        # if self.check_duplicate_input():
        #     return

        self.solve_decomnano()

    def print_input(self):
        """Prints the input dictionary of DecomNano class."""
        print(self.input)

    def solve_decomnano(self):
        """Solves the heterogeneity analysis of bimetallic nanoparticles using coordination numbers obtained from XAS analysis."""

        if self.hollow_shell:
            result = self.session.evaluate(
                wlexpr(self.decomnano_equation_hollow.format(**self.input))
            )
        else:
            result = self.session.evaluate(
                wlexpr(self.decomnano_equation.format(**self.input))
            )

        print(result)

        df = pd.DataFrame(result, columns=self.column)
        self.results = pd.concat([self.results, df])

        return df

    def check_duplicate_input(self):
        """Checks if the input dictionary is already solved.

        Returns:
            bool: True if the input dictionary is already solved, False otherwise.
        """

        if len(self.results) == 0:
            return False

        input_df = pd.Series(self.input)
        input_columns = input_df.index

        df = self.results[input_columns] == input_df
        df = df.all(axis=1)
        df = df.any()

        if df:
            return True
        else:
            return False

    def convert_dict(self, result):
        """Helper function to convert the result of WolframLanguageSession.evaluate() to a dictionary.

        Returns:
            dict: Dictionary of the result.
        """
        dict_result = re.findall(self.dict_regex, str(result))
        dict_result = dict(dict_result)
        return dict_result

    def print_results(self):
        """Prints the results of the heterogeneity analysis of bimetallic nanoparticles using coordination numbers obtained from XAS analysis."""
        print(self.results)

    def save_results(self, filename="results.csv"):
        """Saves the results of the heterogeneity analysis of bimetallic nanoparticles using coordination numbers obtained from XAS analysis.

        Args:
            filename (str): Filename of the results. Defaults to "results.csv".
        """
        self.results.to_csv(filename, index=False)

    def load_results(self, filename="results.csv"):
        """Loads the results to the DecomNano class.

        Args:
            filename (str): Filename of the results. Defaults to "results.csv".
        """

        if not os.path.exists(filename):
            return
        self.results = pd.read_csv(filename)

    def terminate(self):
        """Terminates the WolframLanguageSession."""
        self.session.terminate()

    def __del__(self):
        """Destructor of DecomNano class. Makes sure that the WolframLanguageSession is terminated."""
        self.terminate()
