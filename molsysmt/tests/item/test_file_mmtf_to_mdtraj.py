import molsysmt as msm
from molsysmt.systems import tests as tests_systems
from molsysmt.form import file_mmtf
import mdtraj as mdt
import numpy as np
import pytest


@pytest.fixture()
def mmtf_file_paths():
    return [tests_systems["1SUX"]["1sux.mmtf"],
            tests_systems["5ZMZ"]["5zmz.mmtf"],
            ]


@pytest.fixture()
def pdb_file_paths():
    return [tests_systems["1SUX"]["1sux.pdb"],
            tests_systems["5ZMZ"]["5zmz.pdb"],
            ]


@pytest.fixture()
def positions_5zmz_in_nanometers():
    x_expected = np.array([1.0752, 0.9668, 0.8392, 0.8347, 1.003,
                           1.1347, 0.8941, 1.188, 0.7375, 0.6058,
                           0.5037, 0.4997, 0.5765, 0.6582, 0.6574,
                           0.6565, 0.659, 0.4233, 0.3232, 0.1914,
                           0.1869, 0.3622, 0.4984, 0.2547, 0.5566,
                           0.0853, -0.0445, -0.1372, -0.254, -0.096,
                           0.9657])
    y_expected = np.array([0.0036, 0.0212, -0.0442, -0.1652, -0.0385,
                           0.0208, -0.012, -0.0479, 0.0381, -0.0066,
                           0.0503, 0.1712, 0.0395, -0.035, 0.0288,
                           0.1507, -0.0542, -0.0374, 0.0025, -0.0634,
                           -0.1847, -0.0389, 0.0195, 0.0047, -0.0372,
                           0.0149, -0.0445, 0.0421, 0.0069, 0.1489,
                           0.2092])
    z_expected = np.array([0.5972, 0.5018, 0.5537, 0.5718, 0.3661,
                           0.3171, 0.2654, 0.1946, 0.5789, 0.622,
                           0.5249, 0.5036, 0.7656, 0.8684, 1.0055,
                           1.0189, 1.1083, 0.4655, 0.3675, 0.4035,
                           0.4188, 0.2234, 0.1851, 0.1265, 0.0555,
                           0.4188, 0.4467, 0.5287, 0.5528, 0.5732,
                           0.9206])
    return x_expected, y_expected, z_expected


def test_load_mmtf(mmtf_file_paths, positions_5zmz_in_nanometers):
    traj = file_mmtf.load_mmtf(mmtf_file_paths[0].absolute().__str__())
    assert traj.n_atoms == 4257
    assert traj.n_frames == 1
    assert traj.n_residues == 882

    traj_2 = file_mmtf.load_mmtf(mmtf_file_paths[1].absolute().__str__())
    assert traj_2.n_atoms == 31
    assert traj_2.n_frames == 1
    assert traj_2.n_residues == 5

    x_expected, y_expected, z_expected = positions_5zmz_in_nanometers

    x_actual = traj_2.xyz[0, :, 0]
    y_actual = traj_2.xyz[0, :, 1]
    z_actual = traj_2.xyz[0, :, 2]

    assert np.allclose(x_actual, x_expected)
    assert np.allclose(y_actual, y_expected)
    assert np.allclose(z_actual, z_expected)


# Tests for MMTFTrajectoryFile class


def test_mmtf_trajectory_file_load_name_replacement_tables():
    residue_replacements, atom_replacements = file_mmtf.MMTFTrajectoryFile._load_name_replacement_tables()
    assert isinstance(residue_replacements, dict)
    assert isinstance(atom_replacements, dict)
    assert len(residue_replacements) == 62
    assert len(atom_replacements) == 40


def test_mmtf_trajectory_file_read(mmtf_file_paths, positions_5zmz_in_nanometers):
    positions, topology, unit_lengths, unit_angles = file_mmtf.MMTFTrajectoryFile._read(mmtf_file_paths[0].absolute().__str__(), True)
    assert positions.shape == (1, 4257, 3)
    assert np.allclose([42.869998931884766, 75.58000183105469, 146.4499969482422],
                       unit_lengths)
    assert np.allclose([90.0, 90.0, 90.0], unit_angles)

    assert isinstance(topology, mdt.Topology)
    assert topology.n_atoms == 4257
    assert topology.n_residues == 882
    assert topology.n_chains == 12
    assert topology.n_bonds == 3949

    positions, topology, unit_lengths, unit_angles = file_mmtf.MMTFTrajectoryFile._read(mmtf_file_paths[1].absolute().__str__(), True)
    assert positions.shape == (1, 31, 3)

    # Here expected is in nanometers, we multiply by 10 to convert to angstroms
    x_expected, y_expected, z_expected = positions_5zmz_in_nanometers

    x_actual = positions[0, :, 0]
    y_actual = positions[0, :, 1]
    z_actual = positions[0, :, 2]

    assert np.allclose(x_actual, x_expected * 10)
    assert np.allclose(y_actual, y_expected * 10)
    assert np.allclose(z_actual, z_expected * 10)

    unit_lengths_expected = np.array([[2.944, 0.48, 1.894]])
    unit_angles_expected = np.array([[90., 107.97, 90.]])

    assert unit_lengths.shape == (1, 3)
    assert unit_angles.shape == (1, 3)
    assert np.allclose(unit_lengths_expected * 10, unit_lengths)
    assert np.allclose(unit_angles_expected, unit_angles)

    atom_names_expected = ['N', 'CA', 'C', 'O', 'CB',
                           'CG1', 'CG2', 'CD1', 'N',
                           'CA', 'C', 'O', 'CB', 'CG',
                           'CD', 'OE1', 'NE2', 'N', 'CA',
                           'C', 'O', 'CB', 'CG1', 'CG2',
                           'CD1', 'N', 'CA', 'C', 'O', 'OXT',
                           'O']
    residue_names_expected = ['ILE', 'GLN', 'ILE', 'GLY', 'HOH']

    atom_names_actual = [atom.name for atom in topology.atoms]
    residue_names_actual = [residue.name for residue in topology.residues]

    assert atom_names_actual == atom_names_expected
    assert residue_names_expected == residue_names_actual

    bonds_expected = [
        (1, 2), (2, 3), (1, 4), (0, 1), (4, 5), (4, 6), (5, 7),
        (2, 8), (9, 10), (10, 11), (9, 12), (8, 9), (12, 13),
        (13, 14), (14, 16), (14, 15), (10, 17), (18, 19),
        (19, 20), (18, 21), (17, 18), (21, 22), (21, 23),
        (22, 24), (19, 25), (26, 27), (27, 28), (27, 29), (25, 26)
    ]
    assert len(bonds_expected) == 29
    bonds_expected = sorted(bonds_expected)
    bonds_actual = [(bond.atom1.index, bond.atom2.index) for bond in topology.bonds]
    assert len(bonds_actual) == 29
    bonds_actual = sorted(bonds_actual)

    assert bonds_actual == bonds_expected


def test_mmtf_trajectory_file_encode_data_for_writing(pdb_file_paths):
    traj = mdt.load(pdb_file_paths[1])
    encoder = file_mmtf.MMTFTrajectoryFile._encode_data_for_writing(
        traj.xyz,
        traj.topology,
        traj.unitcell_lengths,
        traj.unitcell_angles,
    )

    assert encoder.num_atoms == 31
    assert encoder.num_chains == 2
    assert encoder.num_bonds == 29
    assert encoder.num_groups == 5

    assert np.allclose(encoder.unit_cell,
                       [2.944, 0.48, 1.894, 90.0, 107.97, 90.0])

    x_coords = traj.xyz[0, :, 0]
    y_coords = traj.xyz[0, :, 1]
    z_coords = traj.xyz[0, :, 2]

    assert np.allclose(encoder.x_coord_list, x_coords)
    assert np.allclose(encoder.y_coord_list, y_coords)
    assert np.allclose(encoder.z_coord_list, z_coords)

    assert encoder.chain_id_list == ["A", "B"]
    assert encoder.groups_per_chain == [4, 1]
    assert encoder.atom_id_list == list(range(1, 31)) + [32]

    assert len(encoder.group_list) == 4

    assert encoder.group_list[0] == {
        'groupName': 'ILE',
        'atomNameList': ['N', 'CA', 'C', 'O', 'CB', 'CG1', 'CG2', 'CD1'],
        'elementList': ['N', 'C', 'C', 'O', 'C', 'C', 'C', 'C'],
        'bondOrderList': [1, 1, 1, 1, 1, 1, 1],
        'bondAtomList': [1, 2, 2, 3, 1, 4, 0, 1, 4, 5, 4, 6, 5, 7],
        'formalChargeList': [0, 0, 0, 0, 0, 0, 0, 0],
        'singleLetterCode': 'I',
        'chemCompType': 'PEPTIDE LINKING'
    }

    assert encoder.group_list[1] == {
        'groupName': 'GLN',
        'atomNameList': ['N', 'CA', 'C', 'O', 'CB', 'CG', 'CD', 'OE1', 'NE2'],
        'elementList': ['N', 'C', 'C', 'O', 'C', 'C', 'C', 'O', 'N'],
        'bondOrderList': [1, 1, 1, 1, 1, 1, 1, 1],
        'bondAtomList': [1, 2, 2, 3, 1, 4, 0, 1, 4, 5, 5, 6, 6, 0, 6, 7],
        'formalChargeList': [0, 0, 0, 0, 0, 0, 0, 0, 0],
        'singleLetterCode': 'Q',
        'chemCompType': 'PEPTIDE LINKING'
    }

    assert encoder.group_list[2] == {
        'groupName': 'GLY',
        'atomNameList': ['N', 'CA', 'C', 'O', 'OXT'],
        'elementList': ['N', 'C', 'C', 'O', 'O'],
        'bondOrderList': [1, 1, 1, 1],
        'bondAtomList': [1, 2, 2, 3, 2, 4, 0, 1],
        'formalChargeList': [0, 0, 0, 0, 0],
        'singleLetterCode': 'G',
        'chemCompType': 'PEPTIDE LINKING'
    }

    assert encoder.group_list[3] == {
        'groupName': 'HOH',
        'atomNameList': ['O'],
        'elementList': ['O'],
        'bondOrderList': [],
        'bondAtomList': [],
        'formalChargeList': [0],
        'singleLetterCode': '?',
        'chemCompType': 'NON-POLYMER'
    }

    assert encoder.group_type_list == [0, 1, 0, 2, 3]
    assert encoder.group_id_list == [1, 2, 3, 4, 101]

    assert len(encoder.entity_list) == 2
    assert encoder.entity_list[0] == {
        'description': '',
        'type': 'polymer',
        'chainIndexList': [0],
        'sequence': 'IQIG'
    }
    assert encoder.entity_list[1] == {
        'description': 'water',
        'type': 'water',
        'chainIndexList': [1],
        'sequence': ''
    }


def test_write_1sux_mmtf_file(pdb_file_paths):

    traj = mdt.load(pdb_file_paths[0])
    encoder = file_mmtf.MMTFTrajectoryFile._encode_data_for_writing(
        traj.xyz,
        traj.topology,
        traj.unitcell_lengths,
        traj.unitcell_angles,
    )

    assert encoder.num_atoms == 4244
    assert encoder.num_groups == 882
    assert encoder.num_bonds == 3936
    assert encoder.num_chains == 6

    assert len(encoder.x_coord_list) == 4244
    assert len(encoder.y_coord_list) == 4244
    assert len(encoder.z_coord_list) == 4244
    assert len(encoder.group_list) == 28


def test_write_mmtf_file_and_load_it(pdb_file_paths):

    traj = mdt.load(pdb_file_paths[1])
    encoder = file_mmtf.MMTFTrajectoryFile._encode_data_for_writing(
        traj.xyz,
        traj.topology,
        traj.unitcell_lengths,
        traj.unitcell_angles,
    )

    temp_file_ptr = encoder.write_temp_file()
    traj_from_temp_file = file_mmtf.load_mmtf(temp_file_ptr.name)
    temp_file_ptr.close()

    assert traj_from_temp_file.n_atoms == 31
    assert traj_from_temp_file.n_chains == 2
    assert traj_from_temp_file.topology.n_bonds == 29
    assert traj_from_temp_file.n_residues == 5
