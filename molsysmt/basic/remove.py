from molsysmt._private.digestion import digest
from molsysmt._private.structure_indices import complementary_structure_indices
from molsysmt._private.atom_indices import complementary_atom_indices
from molsysmt._private.variables import is_all

@digest()
def remove(molecular_system, selection=None, structure_indices=None, to_form=None, syntax='MolSysMT'):

    """remove(item, selection=None, structure_indices=None, syntax='MolSysMT')

    Remove atoms or frames from the molecular model.

    Paragraph with detailed explanation.

    Parameters
    ----------

    item: molecular model
        Molecular model in any of the supported forms by MolSysMT. (See: XXX)

    selection: str, list, tuple or np.ndarray, default=None
       Atoms selection over which this method applies. The selection can be given by a
       list, tuple or numpy array of integers (0-based), or by means of a string following any of
       the selection syntax parsable by MolSysMT (see: :func:`molsysmt.select`).

    structure_indices: str, list, tuple or np.ndarray, default=None
        XXX

    syntax: str, default='MolSysMT'
       Syntaxis used in the argument `selection` (in case it is a string). The
       current options supported by MolSysMt can be found in section XXX (see: :func:`molsysmt.select`).

    Returns
    -------
    item: molecular model
        The result is a new molecular model with the same form as the input item.

    Examples
    --------
    Remove chains 0 and 1 from the pdb: 1B3T.
    >>> import molsysmt as m3t
    >>> system = m3t.load('pdb:1B3T')
    Check the number of chains
    >>> m3t.get(system,n_chains=True)
    8
    Remove chains 0 and 1
    >>> new_system = m3t.remove(system,'chainid 0 1')
    Check the number of chains of the new molecular model
    >>> m3t.get(new_system,n_chains=True)
    6

    See Also
    --------

    :func:`molsysmt.select`

    Notes
    -----
    There is a specific method to remove solvent atoms: molsysmt.remove_solvent and another one to
    remove hydrogens: molsysmt.remove_hydrogens.

    """

    from . import select, extract, get

    atom_indices_to_be_kept = 'all'
    structure_indices_to_be_kept = 'all'

    if selection is not None:
        atom_indices_to_be_removed = select(molecular_system, selection=selection, syntax=syntax)
        atom_indices_to_be_kept = complementary_atom_indices(molecular_system, atom_indices_to_be_removed)

    if structure_indices is not None:
        if is_all(structure_indices):
            n_structures = get(molecular_system, element='system', n_structures=True)
            structure_indices= list(range(n_structures))
        structure_indices_to_be_kept = complementary_structure_indices(molecular_system, structure_indices)

    tmp_item = extract(molecular_system, selection=atom_indices_to_be_kept,
                       structure_indices=structure_indices_to_be_kept, to_form=to_form, copy_if_all=False)

    if isinstance(tmp_item, (list, tuple)):
        if len(tmp_item) == 1:
            tmp_item = tmp_item[0]

    return tmp_item

