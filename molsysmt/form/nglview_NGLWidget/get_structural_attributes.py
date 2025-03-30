#######################################################################################
########### THE FOLLOWING LINES NEED TO BE CUSTOMIZED FOR EVERY CLASS  ################
#######################################################################################

from molsysmt._private.exceptions import NotImplementedMethodError, NotWithThisFormError
from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np
import types


form='nglview.NGLWidget'

## From atom

@digest(form=form)
def get_coordinates_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):

    if is_all(structure_indices):
        n_structures = get_n_structures_from_system(item, skip_digestion=True)
        structure_indices = np.arange(n_structures)

    if hasattr(item[0], 'get_coordinates'):

        coordinates = []
        for ii in structure_indices:
            if is_all(indices):
                coordinates.append(item[0].get_coordinates(ii))
            else:
                coordinates.append(item[0].get_coordinates(ii)[indices,:])
        coordinates = np.array(coordinates)
        coordinates = puw.quantity(coordinates, unit='angstroms')
        coordinates = puw.standardize(coordinates)

    else:

        from . import to_molsysmt_Structures
        from ..molsysmt_Structures import get_coordinates_from_atom as aux_get

        tmp_item = to_molsysmt_Structures(item, skip_digestion=True)
        coordinates = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, skip_digestion=True)

    return coordinates


## From system


@digest(form=form)
def get_n_structures_from_system(item, structure_indices='all', skip_digestion=False):

    if is_all(structure_indices):
        n_structures = item.max_frame + 1
    else:
        n_structures = len(structure_indices)

    return n_structures

@digest(form=form)
def get_box_from_system(item, structure_indices='all', skip_digestion=False):

    from . import to_molsysmt_Structures
    from ..molsysmt_Structures import get_box_from_system as aux_get

    tmp_item = to_molsysmt_Structures(item, skip_digestion=True)
    output = aux_get(tmp_item, structure_indices=structure_indices, skip_digestion=True)

    return output

@digest(form=form)
def get_time_from_system(item, structure_indices='all', skip_digestion=False):

    from . import to_molsysmt_Structures
    from ..molsysmt_Structures import get_time_from_system as aux_get

    tmp_item = to_molsysmt_Structures(item, skip_digestion=True)
    output = aux_get(tmp_item, structure_indices=structure_indices, skip_digestion=True)

    return output

@digest(form=form)
def get_structure_id_from_system(item, structure_indices='all', skip_digestion=False):

    from . import to_molsysmt_Structures
    from ..molsysmt_Structures import get_structure_id_from_system as aux_get

    tmp_item = to_molsysmt_Structures(item, skip_digestion=True)
    output = aux_get(tmp_item, structure_indices=structure_indices, skip_digestion=True)

    return output

@digest(form=form)
def get_coordinates_from_system(item, structure_indices='all', skip_digestion=False):

    return get_coordinates_from_atom(item, indices='all', structure_indices=structure_indices,
                                     skip_digestion=True)

# List of functions to be imported

__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]

