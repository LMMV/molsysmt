from molsysmt._private.digestion import digest
import numpy as np

@digest(form='nglview.NGLWidget')
def to_string_amino_acids_3(item, group_indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import to_string_amino_acids_3 as molsysmt_Topology_to_string_amino_acids_3
    from . import get_atom_index_from_group

    atom_indices = get_atom_index_from_group(item, indices=group_indices, skip_digestion=True)
    atom_indices = np.concatenate(atom_indices)
    tmp_item = to_molsysmt_Topology(item, atom_indices=atom_indices, skip_digestion=True)
    tmp_item = molsysmt_Topology_to_string_amino_acids_3(tmp_item, skip_digestion=True)

    return tmp_item

