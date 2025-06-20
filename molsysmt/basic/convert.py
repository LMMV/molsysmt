from molsysmt._private.exceptions import NotImplementedConversionError
from molsysmt._private.exceptions import NotCompatibleConversionError
from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
from molsysmt.config import default_attribute
import inspect
import numpy as np

def _convert_one_to_one(molecular_system,
                        from_form,
                        to_form='molsysmt.MolSys',
                        selection='all',
                        structure_indices='all',
                        syntax='MolSysMT',
                        **kwargs):

    from . import select, get_form
    from molsysmt.form import is_item, is_file, _dict_modules
    from molsysmt.element import _element_indices, _element_index
    from molsysmt.basic import has_attribute
    from molsysmt.attribute import attributes as _attributes

    output = None

    # Conversion arguments

    conversion_arguments={}

    # If to_form is a file

    output_is_file=False

    if is_item(to_form):
        if is_file(to_form):
            output_is_file=True
            conversion_arguments['output_filename'] = to_form
            to_form = get_form(to_form)

    # Straight conversion

    if to_form in _dict_modules[from_form]._convert_to:

        function = _dict_modules[from_form]._convert_to[to_form]

        input_arguments = set(inspect.signature(function).parameters)

        if 'structure_indices' in input_arguments:
            conversion_arguments['structure_indices']=structure_indices

        for element, element_index in _element_index.items():
            if _element_indices[element] in input_arguments:
                if not is_all(selection):
                    conversion_arguments[_element_indices[element]] = select(molecular_system, element=element,
                                                                             selection=selection, syntax=syntax,
                                                                             skip_digestion=True)
                else:
                    conversion_arguments[_element_indices[element]] = 'all'
                break

        kwargs['skip_digestion']=True

        missing_arguments = input_arguments - (set(conversion_arguments) | set(kwargs) | {'item',
            'copy_if_all'})

        for missing_argument in missing_arguments:
            if missing_argument in default_attribute:
                kwargs[missing_argument]=default_attribute[missing_argument]

        missing_arguments = input_arguments - (set(conversion_arguments) | set(kwargs) | {'item',
        'copy_if_all'})

        if 'get_missing_bonds' in kwargs and 'get_missing_bonds' not in input_arguments:
            del kwargs['get_missing_bonds']

        if len(missing_arguments)>0:

            missing_arguments.discard('compression')
            missing_arguments.discard('compression_opts')
            missing_arguments.discard('int_precision')
            missing_arguments.discard('float_precision')
            missing_arguments.discard('get_missing_bonds')

            if len(missing_arguments)>0:
                raise NotCompatibleConversionError(from_form, to_form, missing_arguments)

        output = function(molecular_system, **conversion_arguments, **kwargs)

    elif ('molsysmt.MolSys' in _dict_modules[from_form]._convert_to) and (to_form in _dict_modules['molsysmt.MolSys']._convert_to):

        output = _convert_one_to_one(molecular_system, from_form, to_form='molsysmt.MolSys', selection=selection,
                structure_indices=structure_indices, syntax=syntax, **kwargs)
        output = _convert_one_to_one(output, 'molsysmt.MolSys', to_form=to_form)

    return output


def _convert_multiple_to_one_with_shortcuts(molecular_system,
                                            from_forms,
                                            to_form='molsysmt.MolSys',
                                            selection='all',
                                            structure_indices='all',
                                            syntax='MolSysMT',
                                            **kwargs):

    from . import select, get_form
    from molsysmt.form import is_item, is_file, _dict_modules
    from molsysmt.element import _element_indices, _element_index
    from molsysmt._private import _multiple_conversion_shortcuts
    from molsysmt.basic import has_attribute
    from molsysmt.attribute import attributes as _attributes

    output = None

    n_items = len(from_forms)

    # Conversion arguments

    conversion_arguments={}

    # If to_form is a file

    output_is_file=False

    if is_item(to_form):
        if is_file(to_form):
            output_is_file=True
            conversion_arguments['output_filename'] = to_form
            to_form = get_form(to_form)

    # Conversion 
    sorted_forms = tuple(sorted(from_forms))

    if to_form in _multiple_conversion_shortcuts[sorted_forms]:
        function = _multiple_conversion_shortcuts[sorted_forms][to_form]

        input_arguments = set(inspect.signature(function).parameters)

        if 'structure_indices' in input_arguments:
            conversion_arguments['structure_indices']=structure_indices

        if 'get_missing_bonds' in kwargs and 'get_missing_bonds' not in input_arguments:
            del kwargs['get_missing_bonds']

        for element, element_index in _element_index.items():
            if _element_indices[element] in input_arguments:
                if not is_all(selection):
                    conversion_arguments[_element_indices[element]] = select(molecular_system, element=element,
                                                                             selection=selection, syntax=syntax,
                                                                             skip_digestion=True)
                else:
                    conversion_arguments[_element_indices[element]] = 'all'
                break

        output = function(molecular_system, **conversion_arguments, **kwargs)

    elif ('molsysmt.MolSys' in _multiple_conversion_shortcuts[sorted_forms]) and (to_form in _dict_modules['molsysmt.MolSys']._convert_to):
        output = _convert_multiple_to_one_with_shortcuts(molecular_system, sorted_forms, to_form='molsysmt.MolSys', selection=selection,
                structure_indices=structure_indices, syntax=syntax, **kwargs)
        output = _convert_one_to_one(output, 'molsysmt.MolSys', to_form=to_form)

    return output

def _convert_multiple_to_one(molecular_system,
                             from_forms,
                             to_form='molsysmt.MolSys',
                             selection='all',
                             structure_indices='all',
                             syntax='MolSysMT',
                             **kwargs):

    from . import select, get_form
    from molsysmt.form import is_item, is_file, _dict_modules
    from molsysmt.element import _element_indices, _element_index
    from molsysmt._private import _multiple_conversion_shortcuts
    from molsysmt.basic import has_attribute
    from molsysmt.attribute import attributes as _attributes

    n_items = len(from_forms)

    # Conversion arguments

    conversion_arguments={}

    # If to_form is a file

    output_is_file=False

    if is_item(to_form):
        if is_file(to_form):
            output_is_file=True
            conversion_arguments['output_filename'] = to_form
            to_form = get_form(to_form)

    #### Checking attributes sets for straight and indirect conversion

    to_attributes = set([ii for ii,jj in _dict_modules[to_form].attributes.items() if jj])

    from_attributes = []
    for from_form, from_item in zip(from_forms, molecular_system):
        aux_set = set()
        for ii,jj in _dict_modules[from_form].attributes.items():
            if jj:
                if _dict_modules[from_form].has_attribute(from_item, ii):
                    aux_set.add(ii)
        from_attributes.append(aux_set)

    attributes_to_be_discarded = []
    for attribute in to_attributes:
        if attribute.startswith('n_'):
            attributes_to_be_discarded.append(attribute)
    for attributes in from_attributes:
        for attribute in attributes:
            if attribute.startswith('n_'):
                attributes_to_be_discarded.append(attribute)

    attributes_to_be_discarded += ['box_volume', 'box_shape', 'box_angles', 'box_lengths']
    attributes_to_be_discarded += ['atom_index', 'structure_index']

    for attribute in attributes_to_be_discarded:
        to_attributes.discard(attribute)
        for ii in from_attributes:
            ii.discard(attribute)

    all_from_attributes = set()
    all_from_attributes = all_from_attributes.union(*from_attributes)

    #### straight conversion

    straight_conversions = {}

    for item_index in range(n_items):
        from_form = from_forms[item_index]
        aux_set = from_attributes[item_index]
        if from_form in _dict_modules:
            if to_form in _dict_modules[from_form]._convert_to:

                input_arguments = set(inspect.signature(_dict_modules[from_form]._convert_to[to_form]).parameters)
                for ii in ['atom_indices', 'group_indices', 'component_indices', 'chain_indices',
                        'molecule_indices', 'entity_indices', 'structure_indices', 'molecular_system',
                        'copy_if_all']:
                    input_arguments.discard(ii)

                attributes_in_other_forms = {}

                for aux_attribute in (all_from_attributes - aux_set) & to_attributes:
                    for ii in range(n_items-1,-1,-1):
                        if aux_attribute in from_attributes[ii]:
                            attributes_in_other_forms[aux_attribute]=[molecular_system[ii], from_forms[ii]]
                            break

                repeated_attributes = {}
                for aux_attribute in aux_set:
                    for ii in range(n_items-1, item_index, -1):
                        if aux_attribute in from_attributes[ii]:
                            if has_attribute(molecular_system[ii], aux_attribute):
                                repeated_attributes[aux_attribute]=[molecular_system[ii], from_forms[ii]]
                                break

                input_attributes = {}
                set_attributes = {}

                for aux_attribute, aux_value in attributes_in_other_forms.items():
                    if _dict_modules[from_form].attributes[aux_attribute]:
                        set_attributes[aux_attribute]=aux_value
                    else:
                        if aux_attribute in input_arguments:
                            input_attributes[aux_attribute]=aux_value
                        else:
                            set_attributes[aux_attribute]=aux_value

                for aux_attribute, aux_value in repeated_attributes.items():
                    set_attributes[aux_attribute]=aux_value

                status_input_attributes = True
                status_set_attributes = True

                for aux_attribute in set_attributes:
                    set_to = _attributes[aux_attribute]['set_to']
                    if not hasattr(_dict_modules[to_form], f'set_{aux_attribute}_to_{set_to}'):
                        status_set_attributes = False
                        break


                straight_conversions[item_index] = {
                        'item' : molecular_system[item_index],
                        'form' : from_form,
                        'input_arguments' : input_arguments,
                        'attributes_in_form' : aux_set,
                        'attributes_in_other_forms': attributes_in_other_forms,
                        'repeated_attributes': repeated_attributes,
                        'input_attributes': input_attributes,
                        'set_attributes': set_attributes,
                        'status_set_attributes': status_set_attributes,
                        }

    if False:
        for ii in straight_conversions:
            print(ii, straight_conversions[ii])
            print('----')
        print('@@@@')

    basic_index = None
    n_set_attributes = np.inf

    for aux_index, aux_dict in straight_conversions.items():
        if aux_dict['status_set_attributes']:
            if n_set_attributes > len(aux_dict['set_attributes']):
                basic_index = aux_index
                n_set_attributes = len(aux_dict['set_attributes'])

    if basic_index is not None:

        aux_dict = straight_conversions[basic_index]

        for aux_attribute, aux_item_form in aux_dict['input_attributes'].items():
            aux_item = aux_item_form[0]
            aux_form = aux_item_form[1]
            get_from = _attributes[aux_attribute]['get_from'][0]
            get_function = getattr(_dict_modules[aux_form], f'get_{aux_attribute}_from_{get_from}')
            get_arguments = {}
            input_arguments = set(inspect.signature(get_function).parameters)
            if 'structure_indices' in input_arguments:
                get_arguments['structure_indices']=structure_indices
            if 'indices' in input_arguments:
                if not is_all(selection):
                    get_arguments['indices'] = select(molecular_system, element=get_from, selection=selection,
                                                      syntax=syntax, skip_digestion=True)
                else:
                    get_arguments['indices'] = 'all'
            conversion_arguments[aux_attribute] = get_function(aux_item, **get_arguments)
        conversion_function = _dict_modules[aux_dict['form']]._convert_to[to_form]
        input_arguments = set(inspect.signature(conversion_function).parameters)
        if 'structure_indices' in input_arguments:
            conversion_arguments['structure_indices']=structure_indices
        for element, element_index in _element_index.items():
            if _element_indices[element] in input_arguments:
                if not is_all(selection):
                    conversion_arguments[_element_indices[element]] = select(molecular_system, element=element,
                                                                             selection=selection, syntax=syntax,
                                                                             skip_digestion=True)
                else:
                    conversion_arguments[_element_indices[element]] = 'all'
                break
        output = conversion_function(aux_dict['item'], **conversion_arguments, **kwargs)

        for aux_attribute, aux_item_form in aux_dict['set_attributes'].items():
            aux_item = aux_item_form[0]
            aux_form = aux_item_form[1]
            get_from = _attributes[aux_attribute]['get_from'][0]
            get_function = getattr(_dict_modules[aux_form], f'get_{aux_attribute}_from_{get_from}')
            get_arguments = {}
            input_arguments = set(inspect.signature(get_function).parameters)
            if 'structure_indices' in input_arguments:
                get_arguments['structure_indices']=structure_indices
            if 'indices' in input_arguments:
                if not is_all(selection):
                    get_arguments['indices'] = select(molecular_system, element=get_from, selection=selection, syntax=syntax)
                else:
                    get_arguments['indices'] = 'all'
            value_to_set = get_function(aux_item, **get_arguments)
            set_to = _attributes[aux_attribute]['set_to']
            set_function = getattr(_dict_modules[to_form], f'set_{aux_attribute}_to_{set_to}')
            set_function(output, value=value_to_set)

    elif to_form=='molsysmt.MolSys' and basic_index is None:

        print('The conversion needs to include new set functions:')

        for aux_index, aux_dict in straight_conversions.items():
            print('   ')
            print('To ', aux_dict['form'], ':')
            print('   ')
            for att, mm in aux_dict['set_attributes'].items():
                set_to = _attributes[att]['set_to']
                if not hasattr(_dict_modules[to_form], f'set_{att}_to_{set_to}'):
                    print(att, 'from', mm[1], 'to', set_to)


            print('   ')

        raise ValueError()

    elif to_form!='molsysmt.MolSys':

        output = _convert_multiple_to_one(molecular_system, from_forms, to_form='molsysmt.MolSys', selection=selection,
                structure_indices=structure_indices, syntax=syntax, **kwargs)
        if output is not None:
            output = _convert_one_to_one(output, 'molsysmt.MolSys', to_form=to_form)

    return output

@digest()
def convert(molecular_system,
            to_form='molsysmt.MolSys',
            selection='all',
            structure_indices='all',
            syntax='MolSysMT',
            skip_digestion=False,
            **kwargs):
    """
    Convert a molecular system into another form or set of forms.

    This function converts a molecular system from its current form to another supported form,
    or multiple forms. Optionally, a subset of atoms and/or structures can be selected using the
    `selection` and `structure_indices` arguments prior to conversion.

    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any of the :ref:`supported forms <Introduction_Forms>`.

    to_form : str or list of str, default='molsysmt.MolSys'
        Target form or list of forms for the conversion output.
        See :ref:`Supported conversions <Introduction_Supported>`.

    selection : str, tuple, list, or numpy.ndarray, default 'all'
        Atom selection to apply before conversion. Can be specified as a string using a
        supported selection syntax, or as indices (0-based). The default 'all' includes
        the entire system.

    structure_indices : int, tuple, list, or numpy.ndarray, default 'all'
        Indices of structures to include in the conversion (0-based). Use 'all' to include all structures.

    syntax : str, default 'MolSysMT'
        Syntax used to parse the `selection` string, if applicable.
        See :ref:`Introduction_Selection`.

    skip_digestion : bool, default False
        If True, bypass the standard validation and digestion of input. For advanced use only.

    **kwargs : dict, optional
        Additional arguments passed to specific conversion handlers if needed.

    Returns
    -------
    molecular_system : molecular system or list of molecular systems
        The converted system(s) in the form(s) specified by `to_form`.

    Raises
    ------
    NotSupportedFormError
        If the input or requested output form is not supported.

    ArgumentError
        If one or more input arguments are invalid.

    Notes
    -----
    For a list of all supported input/output forms, see:
    :ref:`User Guide > Introduction > Molecular systems > Forms <Introduction_Forms>`.

    For supported selection syntaxes, see:
    :ref:`User Guide > Introduction > Selection syntaxes <Introduction_Selection>`.

    See Also
    --------
    :func:`molsysmt.basic.select`
        Select elements of a molecular system.

    :func:`molsysmt.basic.get_form`
        Identify the current form of a molecular system.

    :func:`molsysmt.basic.extract`
        Extract a subset of a molecular system.

    Examples
    --------
    >>> import molsysmt as msm
    >>> molsys_A = '2LAO'
    >>> msm.get_form(molsys_A)
    'string:pdb_id'
    >>> molsys_B = msm.convert(molsys_A, to_form='openmm.Topology')
    >>> msm.get_form(molsys_B)
    'openmm.Topology'

    .. admonition:: User guide

       For a tutorial on using this function, see:
       :ref:`User Guide > Tools > Basic > Convert <Tutorial_Convert>`

    .. versionadded:: 1.0.0
    """

    from . import get_form
    from molsysmt._private import _multiple_conversion_shortcuts

    output = None

    from_form = get_form(molecular_system)

    if isinstance(from_form, (list, tuple)):
        if len(from_form)==1:
            molecular_system = molecular_system[0]
            from_form = from_form[0]

    # If to_form is a list, convert is invoked iteratively

    if isinstance(to_form, (list, tuple)):
        output=[]
        for item_out in to_form:
            output.append(
                convert(molecular_system, to_form=item_out, selection=selection, structure_indices=structure_indices,
                        syntax=syntax, skip_digestion=True, **kwargs))
        return output

    # If one to one
    if not isinstance(from_form, (list, tuple)):
        output = _convert_one_to_one(molecular_system, from_form, to_form=to_form, selection=selection, structure_indices=structure_indices,
                syntax=syntax, skip_digestion=True, **kwargs)

    # If multiple to one

    else:

        # conversions in private shortcuts
        if tuple(sorted(from_form)) in _multiple_conversion_shortcuts:
            output = _convert_multiple_to_one_with_shortcuts(molecular_system, from_form, to_form=to_form, selection=selection, structure_indices=structure_indices,
                syntax=syntax, skip_digestion=True, **kwargs)

        # general conversion
        if output is None:
            output = _convert_multiple_to_one(molecular_system, from_form, to_form=to_form, selection=selection, structure_indices=structure_indices,
                syntax=syntax, skip_digestion=True, **kwargs)

    # Returning the output

    if output is None:

        from_form = get_form(molecular_system)
        if len(from_form)==1:
            from_form=from_form[0]
        raise NotImplementedConversionError(from_form, to_form)

    if isinstance(output, (list, tuple)):
        if len(output) == 1:
            output = output[0]

    return output


