from molsysmt._private.digestion import digest

@digest(form='pdbfixer.PDBFixer')
def to_molsysmt_MolSys(item, atom_indices='all', structure_indices='all'):

    from molsysmt.native.molsys import MolSys
    from . import to_molsysmt_Topology
    from . import to_molsysmt_Structures as pdbfixer_PDBFixer_to_molsysmt_Structures

    tmp_item = MolSys()

    tmp_item.topology = to_molsysmt_Topology(item, atom_indices=atom_indices)
    tmp_item.structures = pdbfixer_PDBFixer_to_molsysmt_Structures(item, atom_indices=atom_indices)

    return tmp_item

