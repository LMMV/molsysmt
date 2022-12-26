from molsysmt.form.mmtf_MMTFDecoder.is_mmtf_MMTFDecoder import is_mmtf_MMTFDecoder as is_form
from molsysmt.form.mmtf_MMTFDecoder.extract import extract
from molsysmt.form.mmtf_MMTFDecoder.add import add
from molsysmt.form.mmtf_MMTFDecoder.append_structures import append_structures
from molsysmt.form.mmtf_MMTFDecoder.get import *
from molsysmt.form.mmtf_MMTFDecoder.set import *
from molsysmt.form.mmtf_MMTFDecoder.iterators import StructuresIterator, TopologyIterator
from .form_attributes import form_attributes

form_name = 'mmtf.MMTFDecoder'
form_type = 'class'
form_info = ["", ""]

form_attributes = form_attributes()
form_attributes['atom_index'] = True
form_attributes['atom_id'] = True
form_attributes['atom_name'] = True
form_attributes['atom_type'] = True
form_attributes['bond_index'] = True
form_attributes['bond_id'] = True
form_attributes['bond_name'] = True
form_attributes['bond_type'] = True
form_attributes['bond_order'] = True
form_attributes['group_index'] = True
form_attributes['group_id'] = True
form_attributes['group_name'] = True
form_attributes['group_type'] = True
form_attributes['component_index'] = True
form_attributes['molecule_index'] = True
form_attributes['molecule_id'] = True
form_attributes['molecule_name'] = True
form_attributes['molecule_type'] = True
form_attributes['chain_index'] = True
form_attributes['chain_id'] = True
form_attributes['chain_name'] = True
form_attributes['chain_type'] = True
form_attributes['entity_index'] = True
form_attributes['entity_id'] = True
form_attributes['entity_name'] = True
form_attributes['entity_type'] = True
form_attributes['coordinates'] = True
form_attributes['box'] = True
form_attributes['bioassemblies'] = True
form_attributes['occupancy'] = True
form_attributes['alternate_location'] = True
form_attributes['b_factor'] = True
form_attributes['formal_charge'] = True
form_attributes['partial_charge'] = True


def to_file_mmtf(item, molecular_system, atom_indices='all', structure_indices='all', output_filename=None):
    from molsysmt.form.mmtf_MMTFDecoder import to_file_mmtf as mmtf_MMTFDecoder_to_file_mmtf

    return mmtf_MMTFDecoder_to_file_mmtf(item, atom_indices=atom_indices, structure_indices=structure_indices,
                                         output_filename=output_filename, digest=False)


def to_file_pdb(item, molecular_system, atom_indices='all', structure_indices='all', output_filename=None):
    from molsysmt.form.mmtf_MMTFDecoder import to_file_pdb as mmtf_MMTFDecoder_to_file_pdb

    return mmtf_MMTFDecoder_to_file_pdb(item, atom_indices=atom_indices, structure_indices=structure_indices,
                                        output_filename=output_filename, digest=False)

def to_string_pdb_text(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.mmtf_MMTFDecoder import to_string_pdb_text as mmtf_MMTFDecoder_to_string_pdb_text

    return mmtf_MMTFDecoder_to_string_pdb_text(item, atom_indices=atom_indices, structure_indices=structure_indices, digest=False)


def to_molsysmt_MolSys(item, molecular_system, atom_indices='all', structure_indices='all', bioassembly_name=None):
    from molsysmt.form.mmtf_MMTFDecoder import to_molsysmt_MolSys as mmtf_MMTFDecoder_to_molsysmt_MolSys

    return mmtf_MMTFDecoder_to_molsysmt_MolSys(item, atom_indices=atom_indices, structure_indices=structure_indices, bioassembly_name=None, digest=False)


def to_molsysmt_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.mmtf_MMTFDecoder import to_molsysmt_Topology as mmtf_MMTFDecoder_to_molsysmt_Topology

    return mmtf_MMTFDecoder_to_molsysmt_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices, digest=False)


def to_molsysmt_Structures(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.mmtf_MMTFDecoder import to_molsysmt_Structures as mmtf_MMTFDecoder_to_molsysmt_Structures

    return mmtf_MMTFDecoder_to_molsysmt_Structures(item, atom_indices=atom_indices, structure_indices=structure_indices, digest=False)


def to_mdtraj_Trajectory(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.mmtf_MMTFDecoder import to_mdtraj_Trajectory as mmtf_MMTFDecoder_to_mdtraj_Trajectory

    return mmtf_MMTFDecoder_to_molsysmt_Structures(item, atom_indices=atom_indices, structure_indices=structure_indices, digest=False)


def to_openmm_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.mmtf_MMTFDecoder import to_openmm_Topology as mmtf_MMTFDecoder_to_openmm_Topology

    return mmtf_MMTFDecoder_to_openmm_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices, digest=False)


def to_string_aminoacids1(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.mmtf_MMTFDecoder import to_string_aminoacids1 as mmtf_MMTFDecoder_to_string_aminoacids1

    from molsysmt.form.mmtf_MMTFDecoder import get_group_index_from_atom

    group_indices = get_group_index_from_atom(item, indices=atom_indices, digest=False)
    group_indices = np.unique(group_indices)
    return mmtf_MMTFDecoder_to_string_aminoacids1(item, group_indices=group_indices, digest=False)


def to_string_aminoacids3(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.mmtf_MMTFDecoder import to_string_aminoacids3 as mmtf_MMTFDecoder_to_string_aminoacids3

    from molsysmt.form.mmtf_MMTFDecoder import get_group_index_from_atom

    group_indices = get_group_index_from_atom(item, indices=atom_indices, digest=False)
    group_indices = np.unique(group_indices)
    return mmtf_MMTFDecoder_to_string_aminoacids3(item, group_indices=group_indices, digest=False)
