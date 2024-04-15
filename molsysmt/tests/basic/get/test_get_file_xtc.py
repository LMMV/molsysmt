"""
Unit and regression test for the get module of the molsysmt package on xtc file systems.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems
import numpy as np


def test_get_file_xtc_1():
    molsys = systems['nglview']['md_1u19.xtc']
    n_atoms, n_structures = msm.get(molsys, element='system', n_atoms=True, n_structures=True)
    assert (n_atoms==5547) and (n_structures==51)

