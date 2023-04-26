"""Top-level package for DecomNano."""

__author__ = """Ryuichi Shimogawa"""
__email__ = "ryuichi.shimogawa@stonybrook.edu"
__version__ = "0.1.0"

from .decomnano import DecomNano
from .sweep import SweepDecomNano

import os

__DecomNano_TOP_DIR__ = os.path.dirname(os.path.abspath(__file__))
__DecomNano_TESTFILE_DIR__ = os.path.join(
    __DecomNano_TOP_DIR__, "../", "tests", "testfiles"
)
