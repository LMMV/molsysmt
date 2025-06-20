import pandas as pd
import numpy as np
from molsysmt._private.variables import is_all
from molsysmt._private.digestion import digest
from molsysmt.lib.series import occurrence_order
import string

class Atoms_DataFrame(pd.DataFrame):

    def __init__(self, n_atoms=0):

        columns = ['atom_id', 'atom_name', 'atom_type', 'group_index', 'chain_index']

        super().__init__(index=range(n_atoms), columns=columns)

        self['atom_id'] = self['atom_id'].astype('Int64')
        self['atom_name'] = self['atom_name'].astype(str)
        self['atom_type'] = self['atom_type'].astype(str)
        self['group_index'] = self['group_index'].astype('Int64')
        self['chain_index'] = self['chain_index'].astype('Int64')

    def _fix_null_values(self):

        for column in self:
            self[column]=self[column].fillna(pd.NA)


class Groups_DataFrame(pd.DataFrame):

    def __init__(self, n_groups=0):

        columns = ['group_id', 'group_name', 'group_type', 'component_index']

        super().__init__(index=range(n_groups), columns=columns)

        self['group_id'] = self['group_id'].astype('Int64')
        self['group_name'] = self['group_name'].astype(str)
        self['group_type'] = self['group_type'].astype(str)
        self['component_index'] = self['component_index'].astype('Int64')

    def _fix_null_values(self):

        for column in self:
            self[column]=self[column].fillna(pd.NA)


class Components_DataFrame(pd.DataFrame):

    def __init__(self, n_components=0):

        columns = ['component_id', 'component_name', 'component_type', 'molecule_index']

        super().__init__(index=range(n_components), columns=columns)

        self['component_id'] = self['component_id'].astype('Int64')
        self['component_name'] = self['component_name'].astype(str)
        self['component_type'] = self['component_type'].astype(str)
        self['molecule_index'] = self['molecule_index'].astype('Int64')

    def _fix_null_values(self):

        for column in self:
            self[column]=self[column].fillna(pd.NA)


class Molecules_DataFrame(pd.DataFrame):

    def __init__(self, n_molecules=0):

        columns = ['molecule_id', 'molecule_name', 'molecule_type', 'entity_index']

        super().__init__(index=range(n_molecules), columns=columns)

        self['molecule_id'] = self['molecule_id'].astype('Int64')
        self['molecule_name'] = self['molecule_name'].astype(str)
        self['molecule_type'] = self['molecule_type'].astype(str)
        self['entity_index'] = self['entity_index'].astype('Int64')

    def _fix_null_values(self):

        for column in self:
            self[column]=self[column].fillna(pd.NA)


class Entities_DataFrame(pd.DataFrame):

    def __init__(self, n_entities=0):

        columns = ['entity_id', 'entity_name', 'entity_type']

        super().__init__(index=range(n_entities), columns=columns)

        self['entity_id'] = self['entity_id'].astype('Int64')
        self['entity_name'] = self['entity_name'].astype(str)
        self['entity_type'] = self['entity_type'].astype(str)

    def _fix_null_values(self):

        for column in self:
            self[column]=self[column].fillna(pd.NA)


class Chains_DataFrame(pd.DataFrame):

    def __init__(self, n_chains=0):

        columns = ['chain_id', 'chain_name', 'chain_type']

        super().__init__(index=range(n_chains), columns=columns)

        self['chain_id'] = self['chain_id'].astype('Int64')
        self['chain_name'] = self['chain_name'].astype(str)
        self['chain_type'] = self['chain_type'].astype(str)

    def _fix_null_values(self):

        for column in self:
            self[column]=self[column].fillna(pd.NA)


class Bonds_DataFrame(pd.DataFrame):

    def __init__(self, n_bonds=0):

        columns = ['atom1_index', 'atom2_index']
        columns += ['order', 'type'] # extra columns -not necessary-

        super().__init__(index=range(n_bonds), columns=columns)

        self['atom1_index'] = self['atom1_index'].astype('Int64')
        self['atom2_index'] = self['atom2_index'].astype('Int64')
        self['order'] = self['order'].astype(str)
        self['type'] = self['type'].astype(str)

    def _reset(self, n_bonds=0):

        columns = ['atom1_index', 'atom2_index']
        columns += ['order', 'type'] # extra columns -not necessary-

        super().__init__(index=range(n_bonds), columns=columns)

        self['atom1_index'] = self['atom1_index'].astype('Int64')
        self['atom2_index'] = self['atom2_index'].astype('Int64')
        self['order'] = self['order'].astype(str)
        self['type'] = self['type'].astype(str)

    def _fix_null_values(self):

        for column in self:
            self[column]=self[column].fillna(pd.NA)

    def _sort_bonds(self):

        mask = self['atom1_index'] > self['atom2_index']
        self.loc[mask, ['atom1_index', 'atom2_index']] = self.loc[mask, ['atom2_index', 'atom1_index']].values
        self.sort_values(by=['atom1_index', 'atom2_index'], inplace=True)
        self.reset_index(drop=True, inplace=True)

    def _remove_empty_columns(self):

        if (self['order']=='nan').all():
            del self['order']

        if (self['type']=='nan').all():
            del self['type']

class Topology():

    @digest()
    def __init__(self, n_atoms=0, n_groups=0, n_components=0, n_molecules=0, n_entities=0, n_chains=0, n_bonds=0,
                skip_digestion=False):

        self.reset_atoms(n_atoms=n_atoms)
        self.reset_groups(n_groups=n_groups)
        self.reset_components(n_components=n_components)
        self.reset_molecules(n_molecules=n_molecules)
        self.reset_entities(n_entities=n_entities)
        self.reset_chains(n_chains=n_chains)
        self.reset_bonds(n_bonds=n_bonds)

    def reset_atoms(self, n_atoms=0):

        self.atoms = Atoms_DataFrame(n_atoms=n_atoms)

    def reset_groups(self, n_groups=0):

        self.groups = Groups_DataFrame(n_groups=n_groups)

    def reset_components(self, n_components=0):

        self.components = Components_DataFrame(n_components=n_components)

    def reset_molecules(self, n_molecules=0):

        self.molecules = Molecules_DataFrame(n_molecules=n_molecules)

    def reset_entities(self, n_entities=0):

        self.entities = Entities_DataFrame(n_entities=n_entities)

    def reset_chains(self, n_chains=0):

        self.chains = Chains_DataFrame(n_chains=n_chains)

    def reset_bonds(self, n_bonds=0):

        self.bonds = Bonds_DataFrame(n_bonds=n_bonds)

    @digest()
    def extract(self, atom_indices='all', keep_ids=True, copy_if_all=False, skip_digestion=False):

        if is_all(atom_indices):

            if copy_if_all:
                return self.copy()
            else:
                return self

        elif len(atom_indices) == self.atoms.shape[0]:

            if copy_if_all:
                return self.copy()
            else:
                return self

        else:

            atom_indices = np.sort(atom_indices)

            tmp_item = Topology(skip_digestion=True)
            tmp_item.atoms = self.atoms.iloc[atom_indices].copy()
            tmp_item.atoms.reset_index(drop=True, inplace=True)

            old_group_indices = tmp_item.atoms['group_index'].unique()
            tmp_item.groups = self.groups.iloc[old_group_indices].copy()
            tmp_item.groups.reset_index(drop=True, inplace=True)
            del old_group_indices

            old_component_indices = tmp_item.groups['component_index'].unique()
            tmp_item.components = self.components.iloc[old_component_indices].copy()
            tmp_item.components.reset_index(drop=True, inplace=True)
            del old_component_indices

            old_molecule_indices = tmp_item.components['molecule_index'].unique()
            tmp_item.molecules = self.molecules.iloc[old_molecule_indices].copy()
            tmp_item.molecules.reset_index(drop=True, inplace=True)
            del old_molecule_indices

            old_entity_indices = tmp_item.molecules['entity_index'].unique()
            tmp_item.entities = self.entities.iloc[old_entity_indices].copy()
            tmp_item.entities.reset_index(drop=True, inplace=True)
            del old_entity_indices

            old_chain_indices = tmp_item.atoms['chain_index'].unique()
            tmp_item.chains = self.chains.iloc[old_chain_indices].copy()
            tmp_item.chains.reset_index(drop=True, inplace=True)
            del old_chain_indices

            tmp_item.atoms['group_index'] = occurrence_order(tmp_item.atoms['group_index'].to_numpy(dtype=int))
            tmp_item.groups['component_index'] = occurrence_order(tmp_item.groups['component_index'].to_numpy(dtype=int))
            tmp_item.components['molecule_index'] = occurrence_order(tmp_item.components['molecule_index'].to_numpy(dtype=int))
            tmp_item.molecules['entity_index'] = occurrence_order(tmp_item.molecules['entity_index'].to_numpy(dtype=int))
            tmp_item.atoms['chain_index'] = occurrence_order(tmp_item.atoms['chain_index'].to_numpy(dtype=int))

            if self.bonds.shape[0]:

                mask_atom1 = np.in1d(self.bonds['atom1_index'], atom_indices)
                mask_atom2 = np.in1d(self.bonds['atom2_index'], atom_indices)
                mask = mask_atom1*mask_atom2
                tmp_item.bonds = self.bonds[mask].copy()
                tmp_item.bonds.reset_index(drop=True, inplace=True)
                del(mask_atom1, mask_atom2)

                if tmp_item.bonds.shape[0]:
                    aux_dict = {jj: ii for ii, jj in enumerate(atom_indices)}
                    vaux_dict = np.vectorize(aux_dict.__getitem__)
                    tmp_item.bonds['atom1_index']=vaux_dict(tmp_item.bonds['atom1_index'].to_numpy())
                    tmp_item.bonds['atom2_index']=vaux_dict(tmp_item.bonds['atom2_index'].to_numpy())
                    del aux_dict, vaux_dict

            tmp_item.rebuild_components(redefine_indices=False, redefine_ids=(not keep_ids), redefine_names=False,
                                        redefine_types=True)
            tmp_item.rebuild_molecules(redefine_indices=False, redefine_ids=(not keep_ids), redefine_names=False,
                                       redefine_types=True)
            tmp_item.rebuild_chains(redefine_ids=(not keep_ids), redefine_types=True, redefine_names=False)
            tmp_item.rebuild_entities(redefine_indices=False, redefine_ids=(not keep_ids), redefine_names=False,
                                      redefine_types=True)

            return tmp_item

    @digest()
    def remove(self, atom_indices=None, copy_if_None=False, skip_digestion=False):

        if atom_indices is None:

            if copy_if_None:
                return self.copy()
            else:
                return self

        else:

            atom_indices_to_be_kept = np.setdiff1d(np.arange(self.n_atoms), atom_indices)

            tmp_item = self.extract(atom_indices=atom_indices_to_be_kept, skip_digestion=True)

            return tmp_item


    @digest(form='molsysmt.Topology')
    def add(self, item, atom_indices='all', keep_ids=True, skip_digestion=False):

        if is_all(atom_indices):
            tmp_item = item.copy()
        else:
            tmp_item = item.extract(atom_indices=atom_indices, skip_digestion=True)

        n_atoms = self.atoms.shape[0]
        n_groups = self.groups.shape[0]
        n_components = self.components.shape[0]
        n_molecules = self.molecules.shape[0]
        n_chains = self.chains.shape[0]

        tmp_item.atoms['group_index'] += n_groups
        tmp_item.groups['component_index'] += n_components
        tmp_item.components['molecule_index'] += n_molecules
        tmp_item.atoms['chain_index'] += n_chains
        tmp_item.bonds['atom1_index'] += n_atoms
        tmp_item.bonds['atom2_index'] += n_atoms

        self.atoms = pd.concat([self.atoms, tmp_item.atoms], ignore_index=True, copy=False)
        self.groups = pd.concat([self.groups, tmp_item.groups], ignore_index=True, copy=False)
        self.components = pd.concat([self.components, tmp_item.components], ignore_index=True, copy=False)
        self.molecules = pd.concat([self.molecules, tmp_item.molecules], ignore_index=True, copy=False)
        self.chains = pd.concat([self.chains, tmp_item.chains], ignore_index=True, copy=False)
        self.bonds = pd.concat([self.bonds, tmp_item.bonds], ignore_index=True, copy=False)

        if not keep_ids:
            self.rebuild_atoms(redefine_ids=True, redefine_types=False)
            self.rebuild_groups(redefine_ids=True, redefine_types=False)

        self.rebuild_components(redefine_indices=False, redefine_ids=(not keep_ids), redefine_names=True,
                                    redefine_types=False)
        self.rebuild_molecules(redefine_indices=False, redefine_ids=(not keep_ids), redefine_types=False,
                                   redefine_names=True)
        self.rebuild_chains(redefine_ids=(not keep_ids), redefine_types=True)

        self.rebuild_entities(redefine_indices=True, redefine_ids=True, redefine_names=True, redefine_types=True)

        del tmp_item

    def copy(self):

        tmp_item = Topology()

        tmp_item.atoms = self.atoms.copy()
        tmp_item.groups = self.groups.copy()
        tmp_item.components = self.components.copy()
        tmp_item.molecules = self.molecules.copy()
        tmp_item.entities = self.entities.copy()
        tmp_item.chains = self.chains.copy()
        tmp_item.bonds = self.bonds.copy()

        return tmp_item

    def add_bonds(self, bonded_atom_pairs, skip_digestion=False):

        bonded_atom_pairs = np.array(bonded_atom_pairs)        
        n_bonds = bonded_atom_pairs.shape[0]

        aux_bonds_dataframe = Bonds_DataFrame(n_bonds=n_bonds)
        aux_bonds_dataframe.atom1_index=bonded_atom_pairs[:,0]
        aux_bonds_dataframe.atom2_index=bonded_atom_pairs[:,1]

        df_concatenado = pd.concat([self.bonds, aux_bonds_dataframe], ignore_index=True)

        self.bonds = Bonds_DataFrame(n_bonds=df_concatenado.shape[0])
        self.bonds['atom1_index'] = df_concatenado['atom1_index']
        self.bonds['atom2_index'] = df_concatenado['atom2_index']
        self.bonds['order'] = df_concatenado['order']
        self.bonds['type'] = df_concatenado['type']

        self.bonds._sort_bonds()
        self.bonds._remove_empty_columns()

        self.rebuild_components()
        self.rebuild_molecules()
        self.rebuild_entities()

        del(df_concatenado, aux_bonds_dataframe)

    def remove_bonds(self, bond_indices='all', skip_digestion=False):

        if is_all(bond_indices):

            self.bonds = Bonds_DataFrame(n_bonds=0)

        else:

            self.bonds.drop(bond_indices, inplace=True)
            self.bonds.reset_index(drop=True, inplace=True)

            #n_bonds = tmp_dataframe.shape[0]


            #self.bonds = Bonds_DataFrame(n_bonds=n_bonds)
            #self.bonds.atom1_index=tmp_dataframe.atom1_index
            #self.bonds.atom2_index=tmp_dataframe.atom2_index

            #if 'order' in tmp_dataframe:
            #    self.bonds['order'] = tmp_dataframe['order']
            #else:
            #    del self.bonds['order']

            #if 'type' in tmp_dataframe:
            #    self.bonds['type'] = tmp_dataframe['type']
            #else:
            #    del self.bonds['type']

            #self.bonds._sort_bonds()

            #del(tmp_dataframe)

        self.rebuild_components(redefine_indices=True, redefine_ids=False, redefine_names=False, redefine_types=False)
        self.rebuild_molecules()
        self.rebuild_entities()


    def add_missing_bonds(self, selection='all', syntax='MolSysMT', skip_digestion=False):

        from molsysmt.build import get_missing_bonds as _get_missing_bonds

        bonds = _get_missing_bonds(self, selection=selection, syntax=syntax,
                                   engine='MolSysMT', with_templates=True, with_distances=False,
                                   skip_digestion=True)

        self.add_bonds(bonds, skip_digestion=True)

        self.rebuild_components()
        self.rebuild_molecules()
        self.rebuild_entities()

    def rebuild_atoms(self, redefine_ids=True, redefine_types=True):

        if redefine_ids:

            self.atoms['atom_id']=np.arange(self.atoms.shape[0], dtype=int)

        if redefine_types:

            from molsysmt.element.atom import get_atom_type_from_atom_name

            aux_dict = {}

            atom_types = []

            for atom_name in self.atoms['atom_name'].values:
                if atom_name not in aux_dict:
                    atom_type=get_atom_type_from_atom_name(atom_name)
                    aux_dict[atom_name]=atom_type
                    atom_types.append(atom_type)
                else:
                    atom_types.append(aux_dict[atom_name])

            self.atoms.atom_type = np.array(atom_types, dtype=object)

            del aux_dict, atom_types

    def rebuild_groups(self, redefine_ids=True, redefine_types=True):

        if redefine_ids:

            self.groups['group_id']=np.arange(self.groups.shape[0], dtype=int)

        if redefine_types:

            from molsysmt.element.group import get_group_type_from_group_name
            from molsysmt.element.group.small_molecule import small_molecule_is_amino_acid

            aux_dict = {}

            group_types = []

            for group_name in self.groups['group_name'].values:
                if group_name not in aux_dict:
                    group_type = get_group_type_from_group_name(group_name)
                    if group_type == 'small molecule':
                        if small_molecule_is_amino_acid(self, group_name):
                            group_type = 'amino acid'
                    aux_dict[group_name]= group_type
                    group_types.append(group_type)
                else:
                    group_types.append(aux_dict[group_name])

            self.groups.group_type = np.array(group_types, dtype=object)

            del aux_dict, group_types

    def rebuild_components(self, redefine_indices=True, redefine_ids=True, redefine_names=True, redefine_types=True):

        if redefine_indices:

            import networkx as nx
            from molsysmt.form.molsysmt_Topology import to_networkx_Graph

            g = to_networkx_Graph(self, skip_digestion=True)
            components = list(nx.connected_components(g))
            n_components = len(components)

            component_index_of_groups = np.zeros(self.groups.shape[0], dtype=int)

            series_aux = self.atoms['group_index']

            group_indices_per_component = [series_aux.iloc[list(indices)].unique() for indices in components]
            for component_index, group_indices in enumerate(group_indices_per_component):
                component_index_of_groups[group_indices]=component_index

            #component_index_of_atoms = np.empty((g.number_of_nodes()), dtype=int)
            #for component_index, component in enumerate(components):
            #    component_index_of_atoms[list(component)] = component_index
            #component_index_of_atoms = occurrence_order(component_index_of_atoms)

            #group_index, first_atom_indices = np.unique(self.atoms['group_index'], return_index=True)
            #component_index_of_groups = component_index_of_atoms[first_atom_indices]

            component_index_of_groups = occurrence_order(component_index_of_groups)
            self.groups["component_index"] = component_index_of_groups
            self.components = Components_DataFrame(n_components=n_components)

            del g, components, component_index_of_groups, group_indices_per_component, series_aux

        if redefine_ids:

            self.components["component_id"] = np.arange(self.components.shape[0], dtype=int)

        if redefine_types:

            from molsysmt.element.component.get_component_type import _get_component_type_from_group_names_and_types

            aux_df = self.groups.groupby('component_index').agg(group_name=('group_name', list),
                                                                group_type=('group_type', list))
            for row in aux_df.itertuples(index=True):
                component_type = _get_component_type_from_group_names_and_types(row.group_name, row.group_type)
                self.components.iloc[row.Index,2] = component_type

        if redefine_names:

            from molsysmt.element.group.small_molecule import group_names as small_molecule_names
            from molsysmt.element.group.saccharide import group_names as saccharide_names

            aux_df = self.groups.groupby('component_index').agg(group_name=('group_name', list),
                                                                group_type=('group_type', list))

            component_types = self.components['component_type'].to_numpy()

            counter = {'peptide':0, 'protein':0, 'small molecule':0, 'saccharide':0, 'unknown':0}

            peptides = {}
            proteins = {}
            small_molecules = {}
            saccharides = {}

            for component_type, row in zip(component_types, aux_df.itertuples(index=True)):
            
                if component_type == 'peptide':

                    string_peptide = ','.join(row.group_name)

                    if string_peptide in peptides:
                        component_name = peptides[string_peptide]
                    else:
                        component_name = component_type+' '+str(counter[component_type])
                        peptides[string_peptide] = component_name
                        counter[component_type] += 1
 
                elif component_type == 'protein':

                    string_protein = ','.join(row.group_name)

                    if string_protein in proteins:
                        component_name = proteins[string_protein]
                    else:
                        component_name = component_type+' '+str(counter[component_type])
                        proteins[string_protein] = component_name
                        counter[component_type] += 1

                elif component_type == 'small molecule':

                    group_name = row.group_name[0]

                    if group_name in small_molecules:
                        component_name = small_molecules[group_name]
                    else:
                        if group_name in small_molecule_names:
                            component_name = group_name
                        else:
                            component_name = group_name
                        small_molecules[component_name] = component_name

                elif component_type == 'saccharide':

                    group_name = row.group_name[0]

                    if group_name in saccharides:
                        component_name = saccharides[group_name]
                    else:
                        if group_name in saccharide_names:
                            component_name = group_name
                        else:
                            component_name = group_name
                        saccharides[component_name] = component_name

                elif component_type in ['ion', 'lipid']:

                    component_name = row.group_name[0]

                elif component_type in ['water']:

                    component_name = 'water'

                else:

                    component_name = 'unknown '+str(counter['unknown'])
                    counter['unknown']+=1

                self.components.iloc[row.Index,1] = component_name
            
        #    component_name = get_component_name(self, element='component', redefine_names=True, skip_digestion=True)
        #    self.components["component_name"] = np.array(component_name, dtype=object)
        #    del component_name


    def rebuild_molecules(self, redefine_indices=True, redefine_ids=True, redefine_names=True, redefine_types=True):

        if redefine_indices:

            component_indices_from_component = np.arange(self.components.shape[0])
            molecule_indices_from_component = component_indices_from_component

            self.components["molecule_index"] = molecule_indices_from_component
            self.reset_molecules(n_molecules = len(molecule_indices_from_component))

        if redefine_ids:

            self.molecules["molecule_id"]=np.arange(self.molecules.shape[0], dtype=int)

        if redefine_names:

            self.molecules['molecule_name']=self.components.groupby('molecule_index')['component_name'].first().to_numpy()

        if redefine_types:

            from molsysmt.config import min_length_protein

            aux_groups = self.components.groupby('molecule_index')['component_type']
            aux_dict = aux_groups.apply(list).to_dict()
            aux_dict_2 = self.components.groupby('molecule_index').indices

            for molecule_index, component_types in aux_dict.items():
                if len(component_types)==1:
                    self.molecules.iat[molecule_index,2]=component_types[0]
                else:
                    if 'protein' in component_types:
                        self.molecules.iat[molecule_index,2]='protein'
                    elif 'peptide' in component_types:
                        aux_components = aux_dict_2[molecule_index] 
                        aux_groups = self.groups.index[self.groups['component_index'].isin(aux_components)].tolist()
                        group_types = self.groups.iloc[aux_groups, 2]
                        n_amino_acids = np.sum(group_types=='amino acid')
                        if n_amino_acids >= min_length_protein:
                            self.molecules.iat[molecule_index,2]='protein'
                        else:
                            self.molecules.iat[molecule_index,2]='peptide'
                    else:
                        raise NotImplementedError

            del aux_groups, aux_dict, aux_dict_2


    def rebuild_chains(self, redefine_ids=True, redefine_types=True, redefine_names=True):

        from molsysmt.element.molecule import _singular_molecule_type_to_plural
        from molsysmt.element.chain import all_chain_names

        if redefine_ids:

            self.chains["chain_id"]=np.arange(self.chains.shape[0], dtype=int)

        if redefine_types:

            atom_indices = [ii.tolist() for ii in self.atoms.groupby('chain_index').groups.values()]

            if len(atom_indices)==1 and len(atom_indices[0])==self.atoms.shape[0]:

                chain_types_from_chain = ['system']

                del(atom_indices)

            else:

                group_indices = []
                for aux_atom_indices in atom_indices:
                    group_indices.append(np.unique(self.atoms.iloc[aux_atom_indices,3]))

                component_indices = []
                for aux_group_indices in group_indices:
                    component_indices.append(np.unique(self.groups.iloc[aux_group_indices,3]))

                molecule_indices = []
                for aux_component_indices in component_indices:
                    molecule_indices.append(np.unique(self.components.iloc[aux_component_indices,3]))

                molecule_types = []
                for aux_molecule_indices in molecule_indices:
                    molecule_types.append(self.molecules.iloc[aux_molecule_indices,2].tolist())

                chain_types_from_chain = []

                for aux_molecule_types in molecule_types:
                    aux = []
                    array_molecule_types = np.array(aux_molecule_types)
                    for aux_type in ['protein', 'peptide', 'dna', 'rna', 'oligosaccharide', 'saccharide',
                                     'small molecule', 'lipid', 'ion', 'water']:
                        if aux_type in aux_molecule_types:
                            counter = np.sum(array_molecule_types == aux_type)
                            if counter == 1:
                                aux.append(aux_type)
                            elif aux_type=='water':
                                aux.append(aux_type)
                            else:
                                aux.append(_singular_molecule_type_to_plural[aux_type])
                    chain_types_from_chain.append(' + '.join(aux))

                del(atom_indices, group_indices, component_indices, molecule_indices, molecule_types)

            self.chains["chain_type"] = np.array(chain_types_from_chain, dtype=object)

        if redefine_names:

            self.chains["chain_name"]=np.array(all_chain_names[:self.chains.shape[0]], dtype=object)


    def rebuild_entities(self, redefine_indices=True, redefine_ids=True, redefine_names=True, redefine_types=True):

        if redefine_indices:

            molecule_names = self.molecules['molecule_name'].to_numpy()
            molecule_types = self.molecules['molecule_type'].to_numpy()

            count = 0
            entity_indices = []
            aux_dict = {}

            for molecule_name, molecule_type in zip(molecule_names, molecule_types):
                if molecule_type == 'water':
                    if 'water' not in aux_dict:
                        aux_dict['water'] = count
                        entity_index = count
                        count += 1
                    else:
                        entity_index = aux_dict['water']
                elif molecule_type == 'ion':
                    if molecule_name not in aux_dict:
                        aux_dict[molecule_name] = count
                        entity_index = count
                        count += 1
                    else:
                        entity_index = aux_dict[molecule_name]
                elif molecule_type == 'lipid':
                    if molecule_name not in aux_dict:
                        aux_dict[molecule_name] = count
                        entity_index = count
                        count += 1
                    else:
                        entity_index = aux_dict[molecule_name]
                elif molecule_type == 'small molecule':
                    if molecule_name not in aux_dict:
                        aux_dict[molecule_name] = count
                        entity_index = count
                        count += 1
                    else:
                        entity_index = aux_dict[molecule_name]
                elif molecule_type == 'saccharide':
                    if molecule_name not in aux_dict:
                        aux_dict[molecule_name] = count
                        entity_index = count
                        count += 1
                    else:
                        entity_index = aux_dict[molecule_name]
                elif molecule_type == 'peptide':
                    if molecule_name not in aux_dict:
                        aux_dict[molecule_name] = count
                        entity_index = count
                        count += 1
                    else:
                        entity_index = aux_dict[molecule_name]
                elif molecule_type == 'protein':
                    if molecule_name not in aux_dict:
                        aux_dict[molecule_name] = count
                        entity_index = count
                        count += 1
                    else:
                        entity_index = aux_dict[molecule_name]
                else:
                    if 'unknown' not in aux_dict:
                        aux_dict['unknown'] = count
                        entity_index = count
                        count += 1
                    else:
                        entity_index = aux_dict['unknown']

                entity_indices.append(entity_index)

            del molecule_names, molecule_types

            n_entities = count

            self.molecules['entity_index']=np.array(entity_indices, dtype=int)

            self.reset_entities(n_entities=n_entities)

        if redefine_ids:

            self.entities['entity_id']=np.arange(self.entities.shape[0], dtype=int)

        if redefine_names:

            self.entities['entity_name']=self.molecules.groupby('entity_index')['molecule_name'].first().to_numpy()

        if redefine_types:

            self.entities['entity_type']=self.molecules.groupby('entity_index')['molecule_type'].first().to_numpy()

    def _join_molecules(self, indices=None):

        raise NotImplementedError

    def _fix_null_values(self):

        self.atoms._fix_null_values()
        self.groups._fix_null_values()
        self.components._fix_null_values()
        self.molecules._fix_null_values()
        self.entities._fix_null_values()
        self.chains._fix_null_values()
        self.bonds._fix_null_values()

    def _sort_bonds(self):

        self.bonds._sort_bonds()

    @digest()
    def compare(self, item, rule='equal', output_type='boolean', skip_digestion=False, **kwargs):

        if rule == 'equal':

            output = {}

            if 'n_atoms' in kwargs:

                tmp_output = (self.atoms.shape[0]==item.atoms.shape[0])
                output['n_atoms'] = (kwargs['n_atoms'] == tmp_output)

            if 'atom_index' in kwargs:

                tmp_output = (self.atoms.shape[0]==item.atoms.shape[0])
                output['atom_index'] = (kwargs['atom_index'] == tmp_output)

            if 'atom_id' in kwargs:

                tmp_output = (self.atoms['atom_id'].values==item.atoms['atom_id'].values).all()
                output['atom_id'] = (kwargs['atom_id'] == tmp_output)

            if 'atom_name' in kwargs:

                tmp_output = (self.atoms['atom_name'].values==item.atoms['atom_name'].values).all()
                output['atom_name'] = (kwargs['atom_name'] == tmp_output)

            if 'atom_type' in kwargs:

                tmp_output = (self.atoms['atom_type'].values==item.atoms['atom_type'].values).all()
                output['atom_type'] = (kwargs['atom_type'] == tmp_output)

            if 'n_groups' in kwargs:

                tmp_output = (self.groups.shape[0]==item.groups.shape[0])
                output['n_groups'] = (kwargs['n_groups'] == tmp_output)

            if 'group_index' in kwargs:

                tmp_output = (self.atoms['group_index'].values==item.atoms['group_index'].values).all()
                output['group_index'] = (kwargs['group_index'] == tmp_output)

            if 'group_id' in kwargs:

                tmp_output = (self.groups['group_id'].values==item.groups['group_id'].values).all()
                output['group_id'] = (kwargs['group_id'] == tmp_output)

            if 'group_name' in kwargs:

                tmp_output = (self.groups['group_name'].values==item.groups['group_name'].values).all()
                output['group_name'] = (kwargs['group_name'] == tmp_output)

            if 'group_type' in kwargs:

                tmp_output = (self.groups['group_type'].values==item.groups['group_type'].values).all()
                output['group_type'] = (kwargs['group_type'] == tmp_output)

            if 'component_index' in kwargs:

                tmp_output = (self.groups['component_index'].values==item.groups['component_index'].values).all()
                output['component_index'] = (kwargs['component_index'] == tmp_output)

            if 'component_id' in kwargs:

                tmp_output = (self.components['component_id'].values==item.components['component_id'].values).all()
                output['component_id'] = (kwargs['component_id'] == tmp_output)

            if 'component_name' in kwargs:

                tmp_output = (self.components['component_name'].values==item.components['component_name'].values).all()
                output['component_name'] = (kwargs['component_name'] == tmp_output)

            if 'component_type' in kwargs:

                tmp_output = (self.components['component_type'].values==item.components['component_type'].values).all()
                output['component_type'] = (kwargs['component_type'] == tmp_output)

            if 'molecule_index' in kwargs:

                tmp_output = (self.components['molecule_index'].values==item.components['molecule_index'].values).all()
                output['molecule_index'] = (kwargs['molecule_index'] == tmp_output)

            if 'molecule_id' in kwargs:

                tmp_output = (self.molecules['molecule_id'].values==item.molecules['molecule_id'].values).all()
                output['molecule_id'] = (kwargs['molecule_id'] == tmp_output)

            if 'molecule_name' in kwargs:

                tmp_output = (self.molecules['molecule_name'].values==item.molecules['molecule_name'].values).all()
                output['molecule_name'] = (kwargs['molecule_name'] == tmp_output)

            if 'molecule_type' in kwargs:

                tmp_output = (self.molecules['molecule_type'].values==item.molecules['molecule_type'].values).all()
                output['molecule_type'] = (kwargs['molecule_type'] == tmp_output)

            if 'entity_index' in kwargs:

                tmp_output = (self.molecules['entity_index'].values==item.molecules['entity_index'].values).all()
                output['entity_index'] = (kwargs['entity_index'] == tmp_output)

            if 'entity_id' in kwargs:

                tmp_output = (self.entities['entity_id'].values==item.entities['entity_id'].values).all()
                output['entity_id'] = (kwargs['entity_id'] == tmp_output)

            if 'entity_name' in kwargs:

                tmp_output = (self.entities['entity_name'].values==item.entities['entity_name'].values).all()
                output['entity_name'] = (kwargs['entity_name'] == tmp_output)

            if 'entity_type' in kwargs:

                tmp_output = (self.entities['entity_type'].values==item.entities['entity_type'].values).all()
                output['entity_type'] = (kwargs['entity_type'] == tmp_output)

            if 'chain_index' in kwargs:

                tmp_output = (self.atoms['chain_index'].values==item.atoms['chain_index'].values).all()
                output['chain_index'] = (kwargs['chain_index'] == tmp_output)

            if 'chain_id' in kwargs:

                tmp_output = (self.chains['chain_id'].values==item.chains['chain_id'].values).all()
                output['chain_id'] = (kwargs['chain_id'] == tmp_output)

            if 'chain_name' in kwargs:

                tmp_output = (self.chains['chain_name'].values==item.chains['chain_name'].values).all()
                output['chain_name'] = (kwargs['chain_name'] == tmp_output)

            if 'chain_type' in kwargs:

                tmp_output = (self.chains['chain_type'].values==item.chains['chain_type'].values).all()
                output['chain_type'] = (kwargs['chain_type'] == tmp_output)

            if 'n_bonds' in kwargs:

                tmp_output = (self.bonds.shape[0]==item.bonds.shape[0]).all()
                output['n_bonds'] = (kwargs['n_bonds'] == tmp_output)

            if 'bonded_atom_pairs' in kwargs:

                tmp_output1 = (self.bonds['atom1_index'] == item.bonds['atom1_index']).all()
                tmp_output2 = (self.bonds['atom2_index'] == item.bonds['atom2_index']).all()
                tmp_output = tmp_output1*tmp_output2
                output['bonded_atom_pairs'] = (kwargs['bonded_atom_pairs'] == tmp_output)

        if output_type=='boolean':
            output = all(list(output.values()))

        return output

