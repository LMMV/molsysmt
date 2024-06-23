
def from_openmm_Context(item, molecular_system=None, atom_indices='all', structure_indices='all'):

    from molsysmt.native.molsys import MolSys
    from molsysmt.native.io.topology import from_openmm_Context as molsysmt_Topology_from_openmm_Context
    from molsysmt.native.io.trajectory import from_openmm_Context as molsysmt_Structures_from_openmm_Context

    tmp_item = MolSys()
    tmp_item.topology, _ = molsysmt_Topology_from_openmm_Context(item, atom_indices=atom_indices, structure_indices=structure_indices)
    tmp_item.trajectory, _ = molsysmt_Structures_from_openmm_Context(item, atom_indices=atom_indices, structure_indices=structure_indices)
    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices)
    else:
        tmp_molecular_system = None

    return tmp_item

