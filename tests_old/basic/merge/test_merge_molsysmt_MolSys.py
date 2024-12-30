"""
Unit and regression test for the merge module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems
import numpy as np

def test_merge_molsysmt_MolSys_1():
    molsys_1 = msm.convert(systems['proline dipeptide']['proline_dipeptide.h5msm'], to_form='molsysmt.MolSys')
    molsys_2 = msm.convert(systems['valine dipeptide']['valine_dipeptide.h5msm'], to_form='molsysmt.MolSys')
    molsys_3 = msm.convert(systems['lysine dipeptide']['lysine_dipeptide.h5msm'], to_form='molsysmt.MolSys')
    n_atoms_1 = msm.get(molsys_1, element='system', n_atoms=True)
    n_atoms_2 = msm.get(molsys_2, element='system', n_atoms=True)
    n_atoms_3 = msm.get(molsys_3, element='system', n_atoms=True)
    molsys = msm.merge([molsys_1, molsys_2, molsys_3])
    n_atoms, n_structures = msm.get(molsys, element='system', n_atoms=True, n_structures=True)
    check = ('molsysmt.MolSys'==msm.get_form(molsys))
    check_n_atoms = (n_atoms == n_atoms_1+n_atoms_2+n_atoms_3)
    check_n_structures = (n_structures == 1)
    assert check and check_n_atoms and check_n_structures

