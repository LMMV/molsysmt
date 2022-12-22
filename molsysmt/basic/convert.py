from molsysmt._private.exceptions import NotImplementedConversionError
from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all


@digest(output=True)
def convert(molecular_system,
            to_form='molsysmt.MolSys',
            selection='all',
            structure_indices='all',
            syntax='MolSysMT',
            digest=True,
            **kwargs):
    """convert(item, to_form='molsysmt.MolSys', selection='all', structure_indices='all', syntax='MolSysMT', **kwargs)

    Convert an input form of a molecular system into other form.

    A molecular model in a given accepted form can be converted into any other supported form
    by MolSysMt. The list of supported forms can be found in the section 'XXX'.

    Parameters
    ----------

    molecular_system: molecular model
        Molecular model in any supported form by MolSysMT (see: XXX).

    selection: str, list, tuple or np.ndarray, defaul='all'
       Atoms selection over which this method applies. The selection can be given by a
       list, tuple or numpy array of integers (0-based), or by means of a string following any of
       the selection syntax parsable by MolSysMT (see: :func:`molsysmt.select`).

    to_form: str, default='molsysmt.MolSys'
        The output object will take the form specified here. This form supported form by MolSysMt
        for the output object.

    syntax: str, default='MolSysMT'
       Syntaxis used in the argument `selection` (in case it is a string). The
       current options supported by MolSysMt can be found in section XXX (see: :func:`molsysmt.select`).

    Returns
    -------

       item: molecular model

       A new object is returned with the form specified by the argument `to_form`.

    Examples
    --------

    See Also
    --------

    :func:`molsysmt.basic.select`

    Notes
    -----

    """

    from . import select, get_form
    from molsysmt.form import is_item, is_file
    from molsysmt.api_forms import dict_convert, dict_extract

    if to_form is None:
        to_form = get_form(molecular_system)

    if isinstance(to_form, (list, tuple)):
        tmp_item=[]
        for item_out in to_form:
            tmp_item.append(
                convert(molecular_system, to_form=item_out, selection=selection, structure_indices=structure_indices,
                        syntax=syntax, digest=True))
        return tmp_item

    if not is_all(selection):
        atom_indices = select(molecular_system, selection=selection, syntax=syntax, digest=False)
    else:
        atom_indices = 'all'

    conversion_arguments={}
    output_is_file=False

    if is_item(to_form):
        if is_file(to_form):
            output_is_file=True
            conversion_arguments['output_filename'] = to_form
            to_form = get_form(to_form)

    tmp_item = None

    if not isinstance(molecular_system, (list, tuple)):
        molecular_system = [molecular_system]

    for item in molecular_system:

        from_form = get_form(item)

        if from_form == to_form:
            tmp_item = dict_extract[from_form](item,
                                               atom_indices=atom_indices,
                                               structure_indices=structure_indices,
                                               copy_if_all=False,
                                               digest=False,
                                               **conversion_arguments, **kwargs)
        else:
            if from_form in dict_convert:
                if to_form in dict_convert[from_form]:
                    tmp_item = dict_convert[from_form][to_form](item,
                                                                molecular_system=molecular_system,
                                                                atom_indices=atom_indices,
                                                                structure_indices=structure_indices,
                                                                digest=False,
                                                                **conversion_arguments, **kwargs)
        if tmp_item is not None:
            break

    if tmp_item is None:

        from_form = get_form(molecular_system)
        if len(from_form)==1:
            from_form=from_form[0]
        raise NotImplementedConversionError(from_form, to_form)

    return tmp_item
