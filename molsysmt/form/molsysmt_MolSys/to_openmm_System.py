from molsysmt._private.digestion import digest

@digest(form='molsysmt.MolSys')
def to_openmm_System(item, atom_indices='all', structure_indices='all'):

    from . import to_openmm_Topology
    from ..openmm_Topology import to_openmm_System as openmm_Topology_to_openmm_System

    tmp_item = to_openmm_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices)
    tmp_item = openmm_Topology_to_openmm_System(tmp_item)

    return tmp_item

