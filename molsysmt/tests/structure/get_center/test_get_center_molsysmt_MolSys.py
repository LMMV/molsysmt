"""
Unit and regression test for the get_geometric_center module of the molsysmt package on molsysmt MolSys molecular
systems.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt.systems import tests as tests_systems
import numpy as np

# Distance between atoms in space and time

def test_get_center_molsysmt_MolSys_1():

    molsys = msm.convert(tests_systems['pentalanine']['traj_pentalanine.h5'], to_form='molsysmt.MolSys')
    list_CAs = msm.select(molsys, selection='atom_name=="CA"')
    n_atoms_CAs = list_CAs.shape[0]
    center = msm.structure.get_center(molsys, selection=list_CAs, weights=np.ones(n_atoms_CAs))
    n_structures = msm.get(molsys, element='system', n_structures=True)
    check_shape = np.all((n_structures,1,3)==center.shape)
    true_values = np.array([[[ 0.79670861,  1.07878454, -0.02861541]],
       [[ 0.83204994,  1.10665931, -0.06361365]],
       [[ 0.77414551,  0.99350907,  0.01043041]]])
    check_values = np.allclose(true_values, msm.pyunitwizard.get_value(center[1007:1010], to_unit='nm'))
    assert check_shape and check_values

