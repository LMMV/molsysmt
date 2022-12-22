from molsysmt._private.digestion import digest
from molsysmt._private.exceptions import NotImplementedMethodError
import numpy as np

@digest()
def compare(molecular_system_A, molecular_system_B, selection_A='all', structure_indices_A='all',
        selection_B='all', structure_indices_B='all', rule='equal', elements=True, coordinates=False,
        box=False, form=False, syntax='MolSysMT', report=False, digest=False):

    from molsysmt.basic import select, get, get_form

    report_dict = {}

    if rule == 'equal':

        if elements:

            # Number of atoms, groups, molecules, chains, entities

            n_atoms_A, n_groups_A, n_molecules_A, n_chains_A, n_entities_A, n_bonds_A = get(molecular_system_A, element='atom',
                                                                                            selection=selection_A, n_atoms=True,
                                                                                            n_groups=True, n_molecules=True,
                                                                                            n_chains=True, n_entities=True,
                                                                                            n_inner_bonds=True,
                                                                                            digest=False)

            n_atoms_B, n_groups_B, n_molecules_B, n_chains_B, n_entities_B, n_bonds_B = get(molecular_system_B, element='atom',
                                                                                            selection=selection_B, n_atoms=True,
                                                                                            n_groups=True, n_molecules=True,
                                                                                            n_chains=True, n_entities=True,
                                                                                            n_inner_bonds=True,
                                                                                            digest=False)


            report_dict['n_atoms'] = (n_atoms_A == n_atoms_B)
            report_dict['n_groups'] = (n_groups_A == n_groups_B)
            report_dict['n_molecules'] = (n_molecules_A == n_molecules_B)
            report_dict['n_chains'] = (n_chains_A == n_chains_B)
            report_dict['n_entities'] = (n_entities_A == n_entities_B)
            report_dict['n_bonds'] = (n_bonds_A == n_bonds_B)

            # atoms

            if report_dict['n_atoms']:

                atom_names_A, atom_types_A, atom_ids_A = get(molecular_system_A, element='atom', selection=selection_A,
                                                             atom_name=True, atom_type=True,
                                                             atom_id=True, digest=False)

                atom_names_B, atom_types_B, atom_ids_B = get(molecular_system_B, element='atom', selection=selection_B,
                                                             atom_name=True, atom_type=True,
                                                             atom_id=True, digest=False)

                report_dict['atom_names'] = np.all(atom_names_A == atom_names_B)
                report_dict['atom_types'] = np.all(atom_types_A == atom_types_B)
                report_dict['atom_ids'] = np.all(atom_ids_A == atom_ids_B)

            else:

                report_dict['atom_names'] = False
                report_dict['atom_types'] = False
                report_dict['atom_ids'] = False

            # groups

            if report_dict['n_groups']:

                group_names_A, group_types_A, group_ids_A = get(molecular_system_A, element='group', selection=selection_A,
                                                                group_name=True, group_type=True,
                                                                group_id=True, digest=False)

                group_names_B, group_types_B, group_ids_B = get(molecular_system_B, element='group', selection=selection_B,
                                                                group_name=True, group_type=True,
                                                                group_id=True, digest=False)

                report_dict['group_names'] = np.all(group_names_A == group_names_B)
                report_dict['group_types'] = np.all(group_types_A == group_types_B)
                report_dict['group_ids'] = np.all(group_ids_A == group_ids_B)

            else:

                report_dict['group_names'] = False
                report_dict['group_types'] = False
                report_dict['group_ids'] = False

            # molecules

            if report_dict['n_molecules']:

                molecule_names_A, molecule_types_A, molecule_ids_A = get(molecular_system_A, element='molecule',
                                                                         selection=selection_A, molecule_name=True,
                                                                         molecule_type=True,
                                                                         molecule_id=True,
                                                                         digest=False)

                molecule_names_B, molecule_types_B, molecule_ids_B = get(molecular_system_B, element='molecule',
                                                                         selection=selection_B, molecule_name=True,
                                                                         molecule_type=True,
                                                                         molecule_id=True,
                                                                         digest=False)

                report_dict['molecule_names'] = np.all(molecule_names_A == molecule_names_B)
                report_dict['molecule_types'] = np.all(molecule_types_A == molecule_types_B)
                report_dict['molecule_ids'] = np.all(molecule_ids_A == molecule_ids_B)

            else:

                report_dict['molecule_names'] = False
                report_dict['molecule_types'] = False
                report_dict['molecule_ids'] = False

            # chains

            if report_dict['n_chains']:

                chain_names_A, chain_types_A, chain_ids_A = get(molecular_system_A, element='chain', selection=selection_A,
                                                                chain_name=True, chain_type=True,
                                                                chain_id=True, digest=False)

                chain_names_B, chain_types_B, chain_ids_B = get(molecular_system_B, element='chain', selection=selection_B,
                                                                chain_name=True, chain_type=True,
                                                                chain_id=True, digest=False)

                report_dict['chain_names'] = np.all(chain_names_A == chain_names_B)
                report_dict['chain_types'] = np.all(chain_types_A == chain_types_B)
                report_dict['chain_ids'] = np.all(chain_ids_A == chain_ids_B)

            else:

                report_dict['chain_names'] = False
                report_dict['chain_types'] = False
                report_dict['chain_ids'] = False

            # entities

            if report_dict['n_entities']:

                entity_names_A, entity_types_A, entity_ids_A = get(molecular_system_A, element='entity', selection=selection_A,
                                                                   entity_name=True,
                                                                   entity_type=True,
                                                                   entity_id=True, digest=False)

                entity_names_B, entity_types_B, entity_ids_B = get(molecular_system_B, element='entity', selection=selection_B,
                                                                   entity_name=True,
                                                                   entity_type=True,
                                                                   entity_id=True, digest=False)

                report_dict['entity_names'] = np.all(entity_names_A == entity_names_B)
                report_dict['entity_types'] = np.all(entity_types_A == entity_types_B)
                report_dict['entity_ids'] = np.all(entity_ids_A == entity_ids_B)

            else:

                report_dict['entity_names'] = False
                report_dict['entity_types'] = False
                report_dict['entity_ids'] = False

            # bonds

            if report_dict['n_bonds']:

                bonded_atoms_A, bond_order_A, bond_type_A = get(molecular_system_A, element='bond', selection=selection_A,
                                                                atom_index=True, bond_order=True,
                                                                bond_type=True, digest=False)

                bonded_atoms_B, bond_order_B, bond_type_B = get(molecular_system_B, element='bond', selection=selection_A,
                                                                atom_index=True, bond_order=True,
                                                                bond_type=True, digest=False)

                report_dict['bonded_atoms'] = np.all(bonded_atoms_A == bonded_atoms_B)
                report_dict['bond_order'] = np.all(bond_order_A == bond_order_B)
                report_dict['bond_type'] = np.all(bond_type_A == bond_type_B)

            else:

                report_dict['bonded_atoms'] = False
                report_dict['bond_order'] = False
                report_dict['bond_type'] = False

        if coordinates:

            if report_dict['n_atoms']:

                coordinates_A = get(molecular_system_A, element='atom', selection=selection_A,
                                    structure_indices=structure_indices_A, coordinates=True,
                                    digest=False)

                coordinates_B = get(molecular_system_B, element='atom', selection=selection_B,
                                    structure_indices=structure_indices_B, coordinates=True,
                                    digest=False)

                if coordinates_A is None:
                    if coordinates_B is None:
                        report_dict['coordinates'] = True
                    else:
                        report_dict['coordinates'] = False
                else:
                    if coordinates_B is None:
                        report_dict['coordinates'] = False
                    else:
                        report_dict['coordinates'] = np.allclose(coordinates_A, coordinates_B)

            else:

                report_dict['coordinates'] = False

        if box:

            box_A = get(molecular_system_A, element='system', selection=selection_A, structure_indices=structure_indices_A,
                        box=True, digest=False)

            box_B = get(molecular_system_B, element='system', selection=selection_B, structure_indices=structure_indices_B,
                        box=True, digest=False)

            if box_A is None:
                if box_B is None:
                    report_dict['box'] = True
                else:
                    report_dict['box'] = False
            else:
                if box_B is None:
                    report_dict['box'] = False
                else:
                    report_dict['box'] = np.allclose(box_A, box_B)

        if form:

            form_A = get_form(molecular_system_A)

            form_B = get_form(molecular_system_B)

            report_dict['form'] = (form_A == form_B)

        # Result

        result = np.all(list(report_dict.values()))

    elif rule == 'in':

        raise NotImplementedMethodError()

    if report:

        return result, report_dict

    else:

        return result


