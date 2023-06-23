"""
Unit and regression test for the info module of the molsysmt package.
"""

import molsysmt as msm
from molsysmt.systems import tests as tests_systems
import numpy as np
from pandas import DataFrame

def test_info_1():
    molsys = msm.convert(tests_systems['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    df = msm.info(molsys, element='atom', selection=[9, 10, 11, 12])
    true_dict = {'index': {0: 9, 1: 10, 2: 11, 3: 12},
                 'id': {0: 10, 1: 11, 2: 12, 3: 13},
                 'name': {0: 'N', 1: 'CA', 2: 'C', 3: 'O'},
                 'type': {0: 'N', 1: 'C', 2: 'C', 3: 'O'},
                 'group index': {0: 1, 1: 1, 2: 1, 3: 1},
                 'group id': {0: 5, 1: 5, 2: 5, 3: 5},
                 'group name': {0: 'PRO', 1: 'PRO', 2: 'PRO', 3: 'PRO'},
                 'group type': {0: 'aminoacid',
                  1: 'aminoacid',
                  2: 'aminoacid',
                  3: 'aminoacid'},
                 'component index': {0: 0, 1: 0, 2: 0, 3: 0},
                 'chain index': {0: 0, 1: 0, 2: 0, 3: 0},
                 'molecule index': {0: 0, 1: 0, 2: 0, 3: 0},
                 'molecule type': {0: 'protein', 1: 'protein', 2: 'protein', 3: 'protein'},
                 'entity index': {0: 0, 1: 0, 2: 0, 3: 0},
                 'entity name': {0: 'Triosephosphate isomerase',
                  1: 'Triosephosphate isomerase',
                  2: 'Triosephosphate isomerase',
                  3: 'Triosephosphate isomerase'}}
    true_df = DataFrame(true_dict)
    assert df.data.equals(true_df)

def test_info_2():
    molsys = msm.convert(tests_systems['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    df = msm.info(molsys, element='atom', selection='group_index==6')
    true_dict = {'index': {0: 45, 1: 46, 2: 47, 3: 48, 4: 49},
                 'id': {0: 46, 1: 47, 2: 48, 3: 49, 4: 50},
                 'name': {0: 'N', 1: 'CA', 2: 'C', 3: 'O', 4: 'CB'},
                 'type': {0: 'N', 1: 'C', 2: 'C', 3: 'O', 4: 'C'},
                 'group index': {0: 6, 1: 6, 2: 6, 3: 6, 4: 6},
                 'group id': {0: 10, 1: 10, 2: 10, 3: 10, 4: 10},
                 'group name': {0: 'ALA', 1: 'ALA', 2: 'ALA', 3: 'ALA', 4: 'ALA'},
                 'group type': {0: 'aminoacid',
                  1: 'aminoacid',
                  2: 'aminoacid',
                  3: 'aminoacid',
                  4: 'aminoacid'},
                 'component index': {0: 0, 1: 0, 2: 0, 3: 0, 4: 0},
                 'chain index': {0: 0, 1: 0, 2: 0, 3: 0, 4: 0},
                 'molecule index': {0: 0, 1: 0, 2: 0, 3: 0, 4: 0},
                 'molecule type': {0: 'protein',
                  1: 'protein',
                  2: 'protein',
                  3: 'protein',
                  4: 'protein'},
                 'entity index': {0: 0, 1: 0, 2: 0, 3: 0, 4: 0},
                 'entity name': {0: 'Triosephosphate isomerase',
                  1: 'Triosephosphate isomerase',
                  2: 'Triosephosphate isomerase',
                  3: 'Triosephosphate isomerase',
                  4: 'Triosephosphate isomerase'}}
    true_df = DataFrame(true_dict)
    assert df.data.equals(true_df)

def test_info_3():
    molsys = msm.convert(tests_systems['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    df = msm.info(molsys, element='group', selection=[20, 21, 22, 23])
    true_dict ={'index': {0: 20, 1: 21, 2: 22, 3: 23},
                'id': {0: 24, 1: 25, 2: 26, 3: 27},
                'name': {0: 'PRO', 1: 'LEU', 2: 'ILE', 3: 'GLU'},
                'type': {0: 'aminoacid', 1: 'aminoacid', 2: 'aminoacid', 3: 'aminoacid'},
                'n atoms': {0: 7, 1: 8, 2: 8, 3: 9},
                'component index': {0: 0, 1: 0, 2: 0, 3: 0},
                'chain index': {0: 0, 1: 0, 2: 0, 3: 0},
                'molecule index': {0: 0, 1: 0, 2: 0, 3: 0},
                'molecule type': {0: 'protein', 1: 'protein', 2: 'protein', 3: 'protein'},
                'entity index': {0: 0, 1: 0, 2: 0, 3: 0},
                'entity name': {0: 'Triosephosphate isomerase',
                 1: 'Triosephosphate isomerase',
                 2: 'Triosephosphate isomerase',
                 3: 'Triosephosphate isomerase'}}
    true_df = DataFrame(true_dict)
    assert df.data.equals(true_df)

def test_info_4():
    molsys = msm.convert(tests_systems['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    df = msm.info(molsys, element='component', selection='molecule_type!="water"')
    true_dict = {'index': {0: 0, 1: 1},
                 'n atoms': {0: 1906, 1: 1912},
                 'n groups': {0: 248, 1: 249},
                 'chain index': {0: 0, 1: 1},
                 'molecule index': {0: 0, 1: 1},
                 'molecule type': {0: 'protein', 1: 'protein'},
                 'entity index': {0: 0, 1: 0},
                 'entity name': {0: 'Triosephosphate isomerase',
                     1: 'Triosephosphate isomerase'}}
    true_df = DataFrame(true_dict)
    assert df.data.equals(true_df)

def test_info_5():
    molsys = msm.convert(tests_systems['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    df = msm.info(molsys, element='molecule', selection='molecule_type!="water"')
    true_dict = {'index': {0: 0, 1: 1},
                 'name': {0: 'Triosephosphate isomerase', 1: 'Triosephosphate isomerase'},
                 'type': {0: 'protein', 1: 'protein'},
                 'n atoms': {0: 1906, 1: 1912},
                 'n groups': {0: 248, 1: 249},
                 'n components': {0: 1, 1: 1},
                 'chain index': {0: 0, 1: 1},
                 'entity index': {0: 0, 1: 0},
                 'entity name': {0: 'Triosephosphate isomerase',
                  1: 'Triosephosphate isomerase'}}
    assert df.data.to_dict()==true_dict

def test_info_6():
    molsys = msm.convert(tests_systems['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    df = msm.info(molsys, element='entity')
    true_dict = {'index': {0: 0, 1: 1},
                 'name': {0: 'Triosephosphate isomerase', 1: 'water'},
                 'type': {0: 'protein', 1: 'water'},
                 'n atoms': {0: 3818, 1: 165},
                 'n groups': {0: 497, 1: 165},
                 'n components': {0: 2, 1: 165},
                 'n chains': {0: 2, 1: 2},
                 'n molecules': {0: 2, 1: 165}}
    assert df.data.to_dict()==true_dict

def test_info_7():
    molsys = msm.convert(tests_systems['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    df = msm.info(molsys)
    true_dict = {'form': {0: 'molsysmt.MolSys'},
                 'n_atoms': {0: 3983},
                 'n_groups': {0: 662},
                 'n_components': {0: 167},
                 'n_chains': {0: 4},
                 'n_molecules': {0: 167},
                 'n_entities': {0: 2},
                 'n_waters': {0: 165},
                 'n_proteins': {0: 2},
                 'n_structures': {0: 1}}
    true_df = DataFrame(true_dict)
    assert df.data.equals(true_df)

def test_info_8():
    molsys = msm.convert(tests_systems['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    molsys = msm.convert(molsys, to_form='molsysmt.Topology')
    df = msm.info(molsys)
    true_dict = {'form': {0: 'molsysmt.Topology'},
                 'n_atoms': {0: 3983},
                 'n_groups': {0: 662},
                 'n_components': {0: 167},
                 'n_chains': {0: 4},
                 'n_molecules': {0: 167},
                 'n_entities': {0: 2},
                 'n_waters': {0: 165},
                 'n_proteins': {0: 2},
                 'n_structures': {0: None}}
    true_df = DataFrame(true_dict)
    assert df.data.equals(true_df)

def test_info_9():
    molsys = msm.convert(tests_systems['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    molsys = msm.convert(molsys, to_form='molsysmt.Structures')
    df = msm.info(molsys)
    true_dict = {'form': {0: 'molsysmt.Structures'},
                 'n_atoms': {0: 3983},
                 'n_groups': {0: None},
                 'n_components': {0: None},
                 'n_chains': {0: None},
                 'n_molecules': {0: None},
                 'n_entities': {0: None},
                 'n_structures': {0: 1}}
    true_df = DataFrame(true_dict)
    assert df.data.equals(true_df)

def test_info_10():
    molsys = msm.convert(tests_systems['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    molsys = msm.convert(molsys, to_form=['molsysmt.Topology', 'molsysmt.Structures'])
    df = msm.info(molsys)
    true_dict = {'form': {0: ['molsysmt.Topology', 'molsysmt.Structures']},
                 'n_atoms': {0: 3983},
                 'n_groups': {0: 662},
                 'n_components': {0: 167},
                 'n_chains': {0: 4},
                 'n_molecules': {0: 167},
                 'n_entities': {0: 2},
                 'n_waters': {0: 165},
                 'n_proteins': {0: 2},
                 'n_structures': {0: 1}}
    true_df = DataFrame(true_dict)
    assert df.data.equals(true_df)

def test_info_11():
    molsys = msm.convert(tests_systems['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    df = msm.info(molsys, element='component', selection='molecule_type=="protein"')
    true_dict = {'index': {0: 0, 1: 1},
        'n atoms': {0: 1906, 1: 1912},
        'n groups': {0: 248, 1: 249},
        'chain index': {0: 0, 1: 1},
        'molecule index': {0: 0, 1: 1},
        'molecule type': {0: 'protein', 1: 'protein'},
        'entity index': {0: 0, 1: 0},
        'entity name': {0: 'Triosephosphate isomerase',
         1: 'Triosephosphate isomerase'}}
    true_df = DataFrame(true_dict)
    assert df.data.equals(true_df)

def test_info_12():
    molsys = msm.convert(tests_systems['TcTIM']['1tcd.msmpk'], to_form='molsysmt.MolSys')
    group_index_in_component_0 = msm.get(molsys, element='group', selection='component_index==0', index=True)[69]
    group_index_in_component_1 = msm.get(molsys, element='group', selection='component_index==1', index=True)[12]
    df = msm.info(molsys, element='group', selection=[group_index_in_component_0,
                                                    group_index_in_component_1])
    true_dict = {'index': {0: 69, 1: 260},
        'id': {0: 73, 1: 15},
        'name': {0: 'GLY', 1: 'CYS'},
        'type': {0: 'aminoacid', 1: 'aminoacid'},
        'n atoms': {0: 4, 1: 6},
        'component index': {0: 0, 1: 1},
        'chain index': {0: 0, 1: 1},
        'molecule index': {0: 0, 1: 1},
        'molecule type': {0: 'protein', 1: 'protein'},
        'entity index': {0: 0, 1: 0},
        'entity name': {0: 'Triosephosphate isomerase',
         1: 'Triosephosphate isomerase'}}
    true_df = DataFrame(true_dict)
    assert df.data.equals(true_df)

