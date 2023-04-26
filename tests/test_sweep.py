#!/usr/bin/env python

"""Tests for `decomnano.sweep` module."""

from decomnano.sweep import SweepDecomNano
from decomnano import __DecomNano_TESTFILE_DIR__
import pandas as pd
import numpy as np
import os

test_input_default = dict(
    dP=2.77,
    dA=2.88,
    fA=0.8,
    nAA=6.2,
    nPP=9.8,
    nAP=0.5,
    nPA=0.53,
    DA=0,
    DAP=18,
    DP=0,
)

test_input_config = dict(
    nAA=0.1,
    DAP=list(range(16, 19, 2)),
    DA=np.arange(0, 3, 1),
)

test_input_range = dict(
    dP=np.array([2.77]),
    dA=np.array([2.88]),
    fA=np.array([0.8]),
    nAA=np.array([6.1, 6.2, 6.3]),
    nPP=np.array([9.8]),
    nAP=np.array([0.5]),
    nPA=np.array([0.53]),
    DA=np.array([0, 1, 2]),
    DAP=np.array([16, 18]),
    DP=np.array([0]),
)


def test_SweepDecomNano_arguments():
    """Test SweepDecomNano arguments"""

    sd = SweepDecomNano(
        input_default=test_input_default, input_config=test_input_config
    )

    for key, value in test_input_config.items():
        if type(value) == list or type(value) == np.ndarray:
            assert np.array_equal(sd.input_config[key], np.array(value))
        else:
            assert sd.input_default[key] == test_input_default[key]

    for key, value in test_input_config.items():
        if type(value) == list or type(value) == np.ndarray:
            assert np.array_equal(sd.input_config[key], np.array(value))
        else:
            assert sd.input_config[key] == test_input_config[key]


def test_SweepDecomNano_init_input():
    """Test SweepDecomNano init_input"""

    sd = SweepDecomNano()

    sd.init_input(input_default=test_input_default, input_config=test_input_config)

    for key, value in test_input_config.items():
        if type(value) == list or type(value) == np.ndarray:
            assert np.array_equal(sd.input_config[key], np.array(value))
        else:
            assert sd.input_default[key] == test_input_default[key]

    for key, value in test_input_config.items():
        if type(value) == list or type(value) == np.ndarray:
            assert np.array_equal(sd.input_config[key], np.array(value))
        else:
            assert sd.input_config[key] == test_input_config[key]


def test_SweepDecomNano_calc_input_range():
    """Test SweepDecomNano calc_input_range"""

    sd = SweepDecomNano()
    sd.init_input(input_default=test_input_default, input_config=test_input_config)
    sd.calc_input_range()

    for key, value in test_input_range.items():
        assert np.array_equal(sd.input_range[key], test_input_range[key])


def test_SweepDecomNano_calc_sweep():
    """Test SweepDecomNano calc_sweep"""

    sd = SweepDecomNano(
        input_default=test_input_default, input_config=test_input_config
    )

    save_path_tmp = os.path.join(
        __DecomNano_TESTFILE_DIR__, "tmp", "test_sweep_result_tmp.csv"
    )
    answer_path = os.path.join(__DecomNano_TESTFILE_DIR__, "test_sweep_result.csv")

    sd.calc_sweep(savepath=save_path_tmp)

    df = pd.read_csv(save_path_tmp, index_col=None)
    answer_df = pd.read_csv(answer_path, index_col=None)

    pd.testing.assert_frame_equal(df, answer_df, check_dtype=False)


def test_SweepDecomNano_calc_sweep_const_2param():
    """Test SweepDecomNano calc_sweep with constraining 2 parameters"""

    sd = SweepDecomNano(
        input_default=test_input_default, input_config=test_input_config
    )

    save_path_tmp = os.path.join(
        __DecomNano_TESTFILE_DIR__, "tmp", "test_sweep_const_2pram_result_tmp.csv"
    )
    answer_path = os.path.join(
        __DecomNano_TESTFILE_DIR__, "test_sweep_const_2pram_result.csv"
    )

    sd.calc_sweep_const_2param(savepath=save_path_tmp, parameters=["DA", "DP"])

    df = pd.read_csv(save_path_tmp, index_col=None)
    answer_df = pd.read_csv(answer_path, index_col=None)

    pd.testing.assert_frame_equal(df, answer_df, check_dtype=False)


# def test_DecomNano_solve_decomnano():
#     """Test DecomNano solve_decomnano solvable case"""

#     # Test for solvable case
#     answer_df = pd.read_csv(
#         os.path.join(decomnano.__DecomNano_TESTFILE_DIR__, "test_result.csv"),
#         index_col=0,
#     )

#     input_solvable = dict(
#         dP=2.77,
#         dA=2.88,
#         fA=0.8,
#         nAA=6.2,
#         nPP=9.8,
#         nAP=0.5,
#         nPA=0.53,
#         DA=0,
#         DAP=18,
#         DP=0,
#     )

#     dn = decomnano.DecomNano(input=input_solvable)
#     df = dn.solve_decomnano()

#     pd.testing.assert_frame_equal(df, answer_df)


# def test_DecomNano_solve_decomnano_insolvable():
#     """Test DecomNano solve_decomnano insolvable case"""

#     answer_df = pd.read_csv(
#         os.path.join(
#             decomnano.__DecomNano_TESTFILE_DIR__, "test_result_insolvable.csv"
#         ),
#         index_col=0,
#     )

#     input_insolvable = dict(
#         dP=2.77,
#         dA=2.88,
#         fA=0.8,
#         nAA=6.2,
#         nPP=9.8,
#         nAP=0.5,
#         nPA=0.33,
#         DA=18,
#         DAP=18,
#         DP=18,
#     )

#     dn = decomnano.DecomNano(input=input_insolvable)
#     df = dn.solve_decomnano()

#     pd.testing.assert_frame_equal(df, answer_df, check_dtype=False)


# def test_DecomNano_check_duplicate_input():
#     """Test DecomNano check_duplicate_input"""

#     dn = decomnano.DecomNano(input=test_input)

#     assert dn.check_duplicate_input() == False

#     dn.solve_decomnano()

#     assert dn.check_duplicate_input() == True


# @pytest.fixture
# def response():
#     """Sample pytest fixture.

#     See more at: http://doc.pytest.org/en/latest/fixture.html
#     """
#     # import requests
#     # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


# def test_content(response):
#     """Sample pytest test function with the pytest fixture as an argument."""
#     # from bs4 import BeautifulSoup
#     # assert 'GitHub' in BeautifulSoup(response.content).title.string


# def test_command_line_interface():
#     """Test the CLI."""
#     runner = CliRunner()
#     result = runner.invoke(cli.main)
#     assert result.exit_code == 0
#     assert "decomnano.cli.main" in result.output
#     help_result = runner.invoke(cli.main, ["--help"])
#     assert help_result.exit_code == 0
#     assert "--help  Show this message and exit." in help_result.output
