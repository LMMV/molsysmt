#######################################################################################
########### THE FOLLOWING LINES NEED TO BE CUSTOMIZED FOR EVERY CLASS  ################
#######################################################################################

from molsysmt._private.execfile import execfile
from molsysmt._private.exceptions import NotImplementedMethodError, NotWithThisFormError
from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np

form='mdtraj.DCDTrajectoryFile'


## From atom

@digest(form=form)
def get_atom_id_from_atom(item, indices='all'):

    raise NotWithThisFormError()

@digest(form=form)
def get_atom_name_from_atom(item, indices='all'):

    raise NotWithThisFormError()

@digest(form=form)
def get_atom_type_from_atom(item, indices='all'):

    raise NotWithThisFormError()

@digest(form=form)
def get_group_index_from_atom(item, indices='all'):

    raise NotWithThisFormError()

@digest(form=form)
def get_component_index_from_atom(item, indices='all'):

    raise NotWithThisFormError()

@digest(form=form)
def get_chain_index_from_atom(item, indices='all'):

    raise NotWithThisFormError()

@digest(form=form)
def get_molecule_index_from_atom(item, indices='all'):

    raise NotWithThisFormError()

@digest(form=form)
def get_entity_index_from_atom(item, indices='all'):

    raise NotWithThisFormError()

@digest(form=form)
def get_inner_bonded_atoms_from_atom(item, indices='all'):

    raise NotWithThisFormError()

@digest(form=form)
def get_n_inner_bonds_from_atom(item, indices='all'):

    raise NotWithThisFormError()

@digest(form=form)
def get_coordinates_from_atom(item, indices='all', structure_indices='all'):

    from molsysmt._private.math import serie_to_chunks

    if is_all(structure_indices):

        n_structures= get_n_structures_from_system(item)
        structure_indices = np.arange(n_structures)

    starts_serie_frames, size_serie_frames = serie_to_chunks(structure_indices)

    xyz_list = []

    for start, size in zip(starts_serie_frames, size_serie_frames):
        item.seek(start)
        if is_all(indices):
            xyz, _, _ = item.read(n_frames=size)
        else:
            xyz, _, _ = item.read(n_frames=size, atom_indices=indices)
        xyz_list.append(xyz)

    xyz = np.concatenate(xyz_list)
    del(xyz_list)

    xyz = xyz.astype('float64')

    xyz = xyz*puw.unit(item.distance_unit)
    xyz = puw.standardize(xyz)

    return xyz


## From group

@digest(form=form)
def get_group_id_from_group(item, indices='all'):

    raise NotImplementedMethodError()

@digest(form=form)
def get_group_name_from_group(item, indices='all'):

    raise NotImplementedMethodError()

@digest(form=form)
def get_group_type_from_group(item, indices='all'):

    raise NotImplementedMethodError()


## From component

@digest(form=form)
def get_component_id_from_group(item, indices='all'):

    raise NotWithThisFormError()

@digest(form=form)
def get_component_name_from_group(item, indices='all'):

    raise NotWithThisFormError()

@digest(form=form)
def get_component_type_from_group(item, indices='all'):

    raise NotWithThisFormError()


## From molecule

@digest(form=form)
def get_molecule_id_from_group(item, indices='all'):

    raise NotWithThisFormError()

@digest(form=form)
def get_molecule_name_from_group(item, indices='all'):

    raise NotWithThisFormError()

@digest(form=form)
def get_molecule_type_from_group(item, indices='all'):

    raise NotWithThisFormError()


## From chain

@digest(form=form)
def get_chain_id_from_group(item, indices='all'):

    raise NotWithThisFormError()

@digest(form=form)
def get_chain_name_from_group(item, indices='all'):

    raise NotWithThisFormError()

@digest(form=form)
def get_chain_type_from_group(item, indices='all'):

    raise NotWithThisFormError()


## From entity

@digest(form=form)
def get_entity_id_from_group(item, indices='all'):

    raise NotWithThisFormError()

@digest(form=form)
def get_entity_name_from_group(item, indices='all'):

    raise NotWithThisFormError()

@digest(form=form)
def get_entity_type_from_group(item, indices='all'):

    raise NotWithThisFormError()



## system

@digest(form=form)
def get_n_atoms_from_system(item):

    position = item.tell()
    xyz, _, _ = item.read(n_frames=1)
    n_atoms = xyz.shape[1]
    del(xyz)
    item.seek(position)
    return n_atoms

@digest(form=form)
def get_n_groups_from_system(item):

    return len(item)

@digest(form=form)
def get_n_components_from_system(item):

    raise NotWithThisFormError()

@digest(form=form)
def get_n_chains_from_system(item):

    raise NotWithThisFormError()

@digest(form=form)
def get_n_molecules_from_system(item):

    raise NotWithThisFormError()

@digest(form=form)
def get_n_entities_from_system(item):

    raise NotWithThisFormError()
@digest(form=form)
def get_n_bonds_from_system(item):

    raise NotWithThisFormError()

@digest(form=form)
def get_n_structures_from_system(item):

    lim = 1000
    aux_val = 1000

    while aux_val==lim:
        lim=lim*10
        item.seek(lim)
        aux_val = item.tell()

    return aux_val

@digest(form=form)
def get_box_from_system(item, structure_indices='all'):

    from molsysmt._private.math import serie_to_chunks

    if is_all(structure_indices):

        n_structures= get_n_structures_from_system(item)
        structure_indices = np.arange(n_structures)

    starts_serie_frames, size_serie_frames = serie_to_chunks(structure_indices)

    cell_lengths = []
    cell_angles = []

    for start, size in zip(starts_serie_frames, size_serie_frames):
        item.seek(start)
        _, aux_cell_lengths, aux_cell_angles = item.read(n_frames=size)
        cell_lengths.append(aux_cell_lengths)
        cell_angles.append(aux_cell_angles)

    cell_lengths = np.concatente(cell_lengths)
    cell_angles = np.concatente(cell_angles)

    cell_lengths = cell_lengths.astype('float64')
    cell_angles = cell_angles.astype('float64')

    cell_lengths = puw.quantity(cell_lengths, item.distance_unit)
    cell_angles = puw.quantity(cell_angles, 'degrees')

    box = box_from_box_lengths_and_angles(cell_lengths, cell_angles)
    box = puw.standardize(box)

    del(cell_lengths, cell_angles)

    return box

@digest(form=form)
def get_time_from_system(item, structure_indices='all'):

    return None

@digest(form=form)
def get_step_from_system(item, structure_indices='all'):

    return None


#######################################################################################
######### DO NOT TOUCH THE FOLLOWING LINES, JUST INCLUDE THEM AS THEY ARE #############
#######################################################################################

from os import path
this_folder = path.dirname(path.abspath(__file__))
common_get = path.join(this_folder, '../../_private/common_get.py')
execfile(common_get, globals(), locals())
del(path, this_folder, common_get)

