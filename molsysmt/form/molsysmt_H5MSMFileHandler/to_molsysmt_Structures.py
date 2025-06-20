from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np

@digest(form='molsysmt.H5MSMFileHandler')
def to_molsysmt_Structures(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from molsysmt.native import Structures

    length_unit = puw.unit(item.file.attrs['length_unit'])
    time_unit = puw.unit(item.file.attrs['time_unit'])
    energy_unit = puw.unit(item.file.attrs['energy_unit'])
    temperature_unit = puw.unit(item.file.attrs['temperature_unit'])

    standard_length_unit = puw.get_standard_units(length_unit)
    standard_time_unit = puw.get_standard_units(time_unit)
    standard_energy_unit = puw.get_standard_units(energy_unit)
    standard_temperature_unit = puw.get_standard_units(temperature_unit)

    structures_ds = item.file['structures']

    
    if is_all(atom_indices):
        n_atoms = structures_ds.attrs['n_atoms']
    else:
        n_atoms = len(atom_indices)

    if is_all(structure_indices):
        #n_structures = structures_ds.attrs['n_structures']
        n_structures = structures_ds.attrs['n_structures_written']
    else:
        n_structures = len(structure_indices)

    tmp_item = Structures()

    tmp_item.n_atoms = n_atoms
    tmp_item.n_structures = n_structures

    # Coordinates

    if structures_ds['coordinates'].shape[0]>0:
        tmp_item.coordinates = puw.quantity(np.zeros([n_structures, n_atoms, 3], dtype='float64'),
                standard_length_unit)
        if is_all(structure_indices):
            if is_all(atom_indices):
                tmp_item.coordinates[:,:,:] = puw.quantity(structures_ds['coordinates'][:,:,:],
                                                           length_unit)
            else:
                tmp_item.coordinates[:,:,:] = puw.quantity(structures_ds['coordinates'][:,atom_indices,:],
                                                           length_unit)
        else:
            if is_all(atom_indices):
                tmp_item.coordinates[:,:,:] = puw.quantity(structures_ds['coordinates'][structure_indices,:,:],
                                                           length_unit)
            else:
                tmp_item.coordinates[:,:,:] = puw.quantity(structures_ds['coordinates'][np.ix_(structure_indices, atom_indices)],
                                                           length_unit)
    else:
        tmp_item.coordinates = None

    # Velocities

    if structures_ds['velocities'].shape[0]>0:
        tmp_item.velocities = puw.quantity(np.zeros([n_structures, n_atoms, 3], dtype='float64'),
                standard_length_unit/standard_time_unit)
        if is_all(structure_indices):
            if is_all(atom_indices):
                tmp_item.velocities[:,:,:] = puw.quantity(structures_ds['velocities'][:,:,:],
                                                          length_unit/time_unit)
            else:
                tmp_item.velocities[:,:,:] = puw.quantity(structures_ds['velocities'][:,atom_indices,:],
                                                          length_unit/time_unit)
        else:
            if is_all(atom_indices):
                tmp_item.velocities[:,:,:] = puw.quantity(structures_ds['velocities'][structure_indices,:,:],
                                                           length_unit)
            else:
                tmp_item.velocities[:,:,:] = puw.quantity(structures_ds['velocities'][np.ix_(structure_indices, atom_indices)],
                                                           length_unit)
    else:
        tmp_item.velocities = None

    # Box

    if structures_ds['box'].shape[0]>0:
        tmp_item.box = puw.quantity(np.zeros([n_structures, 3, 3], dtype='float64'),
                standard_length_unit)
        if is_all(structure_indices):
            tmp_item.box[:,:,:] = puw.quantity(structures_ds['box'][:,:,:],
                    length_unit)
        else:
            tmp_item.box[:,:,:] = puw.quantity(structures_ds['box'][structure_indices,:,:],
                    length_unit)
    else:
        tmp_item.box = None

    # Kinetic Energy

    if structures_ds['kinetic_energy'].shape[0]>0:
        tmp_item.kinetic_energy = puw.quantity(np.zeros([n_structures], dtype='float64'),
                standard_energy_unit)
        if is_all(structure_indices):
            tmp_item.kinetic_energy[:] = puw.quantity(structures_ds['kinetic_energy'][:],
                                         energy_unit)
        else:
            tmp_item.kinetic_energy[:] = puw.quantity(structures_ds['kinetic_energy'][structure_indices],
                                         energy_unit)
    else:
        tmp_item.kinetic_energy = None

    # Potential Energy

    if structures_ds['potential_energy'].shape[0]>0:
        tmp_item.potential_energy = puw.quantity(np.zeros([n_structures], dtype='float64'),
                standard_energy_unit)
        if is_all(structure_indices):
            tmp_item.potential_energy[:] = puw.quantity(structures_ds['potential_energy'][:],
                                                        energy_unit)
        else:
            tmp_item.potential_energy[:] = puw.quantity(structures_ds['potential_energy'][structure_indices],
                                                        energy_unit)
    else:
        tmp_item.potential_energy = None

    # Temperature

    if structures_ds['temperature'].shape[0]>0:

        tmp_item.temperature = puw.quantity(np.zeros([n_structures], dtype='float64'),
                standard_temperature_unit)
        if is_all(structure_indices):
            tmp_item.temperature[:] = puw.quantity(structures_ds['temperature'][:],
                                      temperature_unit)
        else:
            tmp_item.temperature[:] = puw.quantity(structures_ds['temperature'][structure_indices],
                                      temperature_unit)
    else:
        tmp_item.temperature = None


    return tmp_item

