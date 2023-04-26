from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
from molsysmt.basic import select, get
import numpy as np
from molsysmt.lib import rmsd as librmsd
from molsysmt import pyunitwizard as puw

@digest()
def get_least_rmsd (molecular_system=None, selection='backbone', structure_indices='all',
          reference_molecular_system=None, reference_selection=None, reference_structure_index=0,
          reference_coordinates=None, syntax='MolSysMT', engine='MolSysMT'):

    if engine=='MolSysMT':

        coordinates = get(molecular_system, element='atom', selection=selection, structure_indices='all',
                          syntax=syntax, coordinates=True)

        if reference_molecular_system is None:
            reference_molecular_system = molecular_system


        if reference_selection is None:
            reference_selection = selection

        reference_coordinates = get(reference_molecular_system, element='atom', selection=reference_selection,
                                    structure_indices=reference_structure_index, syntax=syntax, coordinates=True)

        coordinates = get(molecular_system, structure_indices='all', coordinates=True)
        units = puw.get_unit(coordinates)
        coordinates = np.asfortranarray(puw.get_value(coordinates), dtype='float64')
        reference_coordinates = np.asfortranarray(puw.get_value(reference_coordinates, to_unit=units), dtype='float64')

        if reference_coordinates.shape[1]!=n_atom_indices:
            raise ValueError("reference selection and selection needs to have the same number of atoms")

        rmsd_val = librmsd.least_rmsd(coordinates, atom_indices, reference_coordinates, structure_indices,
                                 n_atoms, n_structures, n_atom_indices, n_structure_indices)

        rmsd_val = puw.quantity(rmsd_val, units, standardized=True)

        del(coordinates, units)

        return rmsd_val

    else:
        raise NotImplementedMethodError()

