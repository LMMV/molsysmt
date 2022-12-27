from molsysmt._private.digestion import digest

@digest(form='openmm.PDBFile')
def to_openmm_Topology(item, atom_indices='all', structure_indices='all'):

    from molsysmt.form.openmm_Topology import extract as extract_openmm_Topology

    tmp_item = item.getTopology()
    tmp_item = extract_openmm_Topology(tmp_item, atom_indices=atom_indices,
            structure_indices=structure_indices, copy_if_all=False)

    return tmp_item

