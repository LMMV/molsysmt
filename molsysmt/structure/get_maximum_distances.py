from molsysmt._private.digestion import digest
from molsysmt import pyunitwizard as puw
import numpy as np

@digest()
def get_maximum_distances(molecular_system, selection="all", groups_of_atoms=None, group_behavior=None, as_entity=True, structure_indices="all",
                     molecular_system_2=None, selection_2=None, groups_of_atoms_2=None, group_behavior_2=None, as_entity_2=True, structure_indices_2=None,
                     output_with_atom_indices=False, pairs=False, pbc=False, engine='MolSysMT', syntax='MolSysMT'):

    from .get_distances import get_distances

    if output_with_atom_indices:

        atom_indices_1, atom_indices_2, all_dists = get_distances(molecular_system=molecular_system, selection=selection,
                groups_of_atoms=groups_of_atoms, group_behavior=group_behavior, structure_indices=structure_indices,
                molecular_system_2=molecular_system_2, selection_2=selection_2, groups_of_atoms_2=groups_of_atoms_2,
                group_behavior_2=group_behavior_2, structure_indices_2=structure_indices_2,
                pairs=pairs, pbc=pbc, output_type='numpy.ndarray', output_with_atom_indices=True,
                engine=engine, syntax=syntax)

    else:

        all_dists = get_distances(molecular_system=molecular_system, selection=selection, groups_of_atoms=groups_of_atoms, group_behavior=group_behavior,
                structure_indices=structure_indices, molecular_system_2=molecular_system_2, selection_2=selection_2, groups_of_atoms_2=groups_of_atoms_2,
                group_behavior_2=group_behavior_2, structure_indices_2=structure_indices_2,
                pairs=pairs, pbc=pbc, output_type='numpy.ndarray',
                engine=engine, syntax=syntax)

    if pairs is False:

        nstructures, nelements_1, nelements_2 = all_dists.shape
        length_units = puw.get_unit(all_dists)
        all_dists = puw.get_value(all_dists)

        if (as_entity is True) and (as_entity_2 is True):

            pairs=np.empty((nstructures,2),dtype=int)
            dists=np.empty((nstructures),dtype=float)
            for indice_structure in range(nstructures):
                ii,jj = np.unravel_index(all_dists[indice_structure,:,:].argmax(), all_dists[indice_structure,:,:].shape)
                if output_with_atom_indices:
                    pairs[indice_structure,0] = atom_indices_1[ii]
                    pairs[indice_structure,1] = atom_indices_2[jj]
                else:
                    pairs[indice_structure,0] = ii
                    pairs[indice_structure,1] = jj
                dists[indice_structure] = all_dists[indice_structure,ii,jj]

            del(all_dists)

            dists=dists*length_units

            return pairs, dists

        elif (as_entity is False) and (as_entity_2 is True):

            pairs=np.empty((nstructures, nelements_1), dtype=int)
            dists=np.empty((nstructures, nelements_1), dtype=float)
            for indice_structure in range(nstructures):
                for ii in range(nelements_1):
                    jj = all_dists[indice_structure,ii,:].argmax()
                    if output_with_atom_indices:
                        pairs[indice_structure,ii]=atom_indices_2[jj]
                    else:
                        pairs[indice_structure,ii]=jj
                    dists[indice_structure,ii]=all_dists[indice_structure,ii,jj]

            del(all_dists)

            dists=dists*length_units

            return pairs, dists

        elif (as_entity is True) and (as_entity_2 is False):

            pairs=np.empty((nstructures, nelements_2), dtype=int)
            dists=np.empty((nstructures, nelements_2), dtype=float)
            for indice_structure in range(nstructures):
                for ii in range(nelements_2):
                    jj = all_dists[indice_structure,:,ii].argmax()
                    if output_with_atom_indices:
                        pairs[indice_structure,ii]=atom_indices_1[jj]
                    else:
                        pairs[indice_structure,ii]=jj
                    dists[indice_structure,ii]=all_dists[indice_structure,jj,ii]

            del(all_dists)

            dists=dists*length_units

            return pairs, dists

        else:
            raise ValueError("If both input arguments 'as_entity' and 'as_entity_2' are False, the\
                    method you are looking for is molsysmt.distance()")

    else:

        nstructures, nelements = all_dists.shape
        length_units = puw.get_unit(all_dists)
        all_dists = puw.get_value(all_dists)

        if (as_entity is True) and (as_entity_2 is True):

            pairs=np.empty((nstructures),dtype=int)
            dists=np.empty((nstructures),dtype=float)
            for indice_structure in range(nstructures):
                ii = all_dists[indice_structure,:].argmax()
                pairs[indice_structure] = ii
                dists[indice_structure] = all_dists[indice_structure,ii]

            del(all_dists)

            dists=dists*length_units

            return pairs, dists

        else:
            raise ValueError("If 'pairs=True' both input arguments 'as_entity' and 'as_entity_2' need to be True")

