from molsysmt._private.digestion import digest


@digest()
def is_composed_of(molecular_system, selection='all', syntax='MolSysMT', ions=False, waters=False,
                   small_molecules=False, peptides=False, proteins=False, dnas=False, rnas=False,
                   lipids=False, oligosaccharides=False):

    from . import get

    n_ions_in, n_waters_in, n_small_molecules_in, n_peptides_in, n_proteins_in, \
    n_dnas_in, n_rnas_in, n_lipids_in, n_oligosaccharides_in = get(molecular_system, element="system",
                                            selection=selection, syntax=syntax,
                                            n_ions=True, n_waters=True, n_small_molecules=True,
                                            n_peptides=True, n_proteins=True, n_dnas=True, n_rnas=True,
                                            n_lipids=True, n_oligosaccharides=True)

    aux_list = [[ions, n_ions_in], [waters, n_waters_in],
                [small_molecules, n_small_molecules_in], [peptides, n_peptides_in], [proteins,
                                                                                     n_proteins_in], [dnas, n_dnas_in],
                [rnas, n_rnas_in], [lipids, n_lipids_in], [oligosaccharides, n_oligosaccharides_in]]

    output = True

    for condition, in_system in aux_list:

        if type(condition) == int:
            if condition != in_system:
                output = False
                break

        elif type(condition) == bool:
            if condition == True:
                if in_system == 0:
                    output = False
                    break
            else:
                if in_system > 0:
                    output = False
                    break

    return output
