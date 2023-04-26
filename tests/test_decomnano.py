#!/usr/bin/env python

"""Tests for `decomnano.decomnano` module."""

import decomnano
import pandas as pd
import os

test_input = dict(
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


def test_DecomNano_arguments():
    """Test DecomNano arguments"""

    dn = decomnano.DecomNano(input=test_input)

    for key, value in test_input.items():
        assert dn.input[key] == value


def test_DecomNano_init_input():
    """Test DecomNano init_input"""
    dn = decomnano.DecomNano()
    dn.init_input(**test_input)

    for key, value in test_input.items():
        assert dn.input[key] == value


def test_DecomNano_solve_decomnano():
    """Test DecomNano solve_decomnano solvable case"""

    # Test for solvable case
    answer_df = pd.read_csv(
        os.path.join(decomnano.__DecomNano_TESTFILE_DIR__, "test_result.csv"),
        index_col=0,
    )

    input_solvable = dict(
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

    dn = decomnano.DecomNano(input=input_solvable)
    df = dn.solve_decomnano()

    pd.testing.assert_frame_equal(df, answer_df)


def test_DecomNano_solve_decomnano_insolvable():
    """Test DecomNano solve_decomnano insolvable case"""

    answer_df = pd.read_csv(
        os.path.join(
            decomnano.__DecomNano_TESTFILE_DIR__, "test_result_insolvable.csv"
        ),
        index_col=0,
    )

    input_insolvable = dict(
        dP=2.77,
        dA=2.88,
        fA=0.8,
        nAA=6.2,
        nPP=9.8,
        nAP=0.5,
        nPA=0.33,
        DA=18,
        DAP=18,
        DP=18,
    )

    dn = decomnano.DecomNano(input=input_insolvable)
    df = dn.solve_decomnano()

    pd.testing.assert_frame_equal(df, answer_df, check_dtype=False)


def test_DecomNano_check_duplicate_input():
    """Test DecomNano check_duplicate_input"""

    dn = decomnano.DecomNano(input=test_input)

    assert dn.check_duplicate_input() == False

    dn.solve_decomnano()

    assert dn.check_duplicate_input() == True
