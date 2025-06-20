"""
Unit and regression test for the compare module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems
import numpy as np

def test_compare_all_eq_1():
    molsys_A = msm.convert(systems['T4 lysozyme L99A']['t4_lysozyme_L99A.h5msm'], to_form='molsysmt.MolSys')
    molsys_B = msm.convert(systems['T4 lysozyme L99A']['t4_lysozyme_L99A.h5msm'], to_form='molsysmt.MolSys')
    output = msm.compare(molsys_A, molsys_B, attributes_type='topological', coordinates=True, box=True)
    assert output == True

def test_compare_all_eq_2():
    molsys_A = msm.convert(systems['T4 lysozyme L99A']['t4_lysozyme_L99A.h5msm'], to_form='molsysmt.MolSys')
    molsys_B = msm.convert(systems['chicken villin HP35']['chicken_villin_HP35.h5msm'], to_form='molsysmt.MolSys')
    output = msm.compare(molsys_A, molsys_B, attributes_type='topological', coordinates=True, box=True)
    assert output == False

def test_compare_all_eq_3():
    molsys_A = msm.convert(systems['T4 lysozyme L99A']['181l.h5msm'], to_form='openmm.Modeller')
    molsys_B = msm.convert(molsys_A, to_form='molsysmt.MolSys')
    comparison = msm.compare(molsys_A, molsys_B, output_type='dictionary')

    output = True

    if comparison['atom_index']!=True:
        output = False
    if comparison['atom_name']!=True:
        output = False
    if comparison['atom_id']!=True:
        output = False
    if comparison['atom_type']!=True:
        output = False

    if comparison['group_index']!=True:
        output = False
    if comparison['group_name']!=True:
        output = False
    if comparison['group_id']!=True:
        output = False
    if comparison['group_type']!=True:
        output = False

    if comparison['component_index']!=True:
        output = False
    if comparison['component_type']!=True:
        output = False

    if comparison['chain_index']!=True:
        output = False
    if comparison['chain_name']!=True:
        output = False
    if comparison['chain_id']!=True:
        output = False
    if comparison['chain_type']!=True:
        output = False

    if comparison['molecule_index']!=True:
        output = False
    if comparison['molecule_type']!=True:
        output = True

    if comparison['bonded_atom_pairs']!=True:
        output = False

    if comparison['n_atoms']!=True:
        output = False
    if comparison['n_groups']!=True:
        output = False
    if comparison['n_components']!=True:
        output = False
    if comparison['n_chains']!=True:
        output = False
    if comparison['n_molecules']!=True:
        output = False
    if comparison['n_bonds']!=True:
        output = False

    assert output == True

def test_compare_all_eq_4():

    molsys_A = msm.convert('pdb_id:181L', to_form='openmm.Modeller')
    molsys_B = msm.convert(molsys_A, to_form='molsysmt.MolSys')
    molsys_C = msm.extract(molsys_B, selection='molecule_type=="protein"')


    assert True == msm.compare(molsys_A, molsys_B)
    assert False == msm.compare(molsys_A, molsys_C)
    assert True == msm.compare(molsys_A, molsys_B, coordinates=True, box=True, n_groups=True)
    assert False == msm.compare(molsys_B, molsys_C, coordinates=True, box=True, n_groups=True)
    assert True == msm.compare(molsys_B, molsys_C, coordinates=False, box=True, n_groups=False)


