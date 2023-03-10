from molsysmt._private.digestion import digest

@digest(form='openmm.Modeller')
def to_pdbfixer_PDBFixer(item, atom_indices='all', structure_indices='all'):

    from . import to_openmm_Topology
    from . import get_coordinates_from_atom
    from ..openmm_Topology import to_pdbfixer_PDBFixer as openmm_Topology_to_pdbfixer_PDBFixer

    tmp_item = to_openmm_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices)
    coordinates = get_coordinates_from_atom(item, atom_indices=atom_indices, structure_indices=structure_indices)
    tmp_item = openmm_Topology_to_pdbfixer_PDBFixer(tmp_item, coordinates=coordinates)

    return tmp_item

