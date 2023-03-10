from molsysmt._private.digestion import digest

@digest(form='file:prmtop')
def to_molsysmt_MolSys(item, atom_indices='all', coordinates=None):

    from molsysmt.native import MolSys, Structures
    from .to_molsysmt_Topology import to_molsysmt_Topology
    tmp_item = MolSys()
    tmp_item.topology = to_molsysmt_Topology(item, atom_indices=atom_indices)
    tmp_item.structures = Structures()
    tmp_item.structures.append_structures(coordinates=coordinates)

    return tmp_item

