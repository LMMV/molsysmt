from molsysmt._private.digestion import digest

@digest(form='mdanalysis.Universe')
def to_file_pdb(item, atom_indices='all', structure_indices='all', output_filename=None,
        multiframe=True):

    tmp_item = extract(item, atom_indices=atom_indices, structure_indices=structure_indices)
    tmp_item.atoms.write(output_filename, multiframe=multiframe)
    tmp_item = output_filename

    return tmp_item

