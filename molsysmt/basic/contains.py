from molsysmt._private.digestion import digest
import numpy as np

def _evaluation(condition, n_in_system):

    output = True

    if condition is not None:
        if type(condition)==bool:
            if condition==True and n_in_system==0:
                output = False
            elif condition==False and n_in_system>0:
                output = False
        elif type(condition)==int:
            if condition>n_in_system:
                output = False

    return output

@digest()
def contains(molecular_system, selection='all', syntax='MolSysMT',
        ions=None, waters=None, small_molecules=None, peptides=None, proteins=None,
        dnas=None, rnas=None, lipids=None, oligosaccharides=None, hydrogens=None):

    from . import get, select

    if ions is not None:

        n_in_system = get(molecular_system, selection=selection, n_ions=True)

        if not _evaluation(ions, n_in_system):
            return False

    if waters is not None:

        n_in_system = get(molecular_system, n_waters=True)

        if not _evaluation(waters, n_in_system):
            return False

    if small_molecules is not None:

        n_in_system = get(molecular_system, n_small_molecules=True)

        if not _evaluation(small_molecules, n_in_system):
            return False

    if peptides is not None:

        n_in_system = get(molecular_system, n_peptides=True)

        if not _evaluation(peptides, n_in_system):
            return False

    if proteins is not None:

        n_in_system = get(molecular_system, n_proteins=True)

        if not _evaluation(proteins, n_in_system):
            return False

    if dnas is not None:

        n_in_system = get(molecular_system, n_dnas=True)

        if not _evaluation(dnas, n_in_system):
            return False

    if rnas is not None:

        n_in_system = get(molecular_system, n_rnas=True)

        if not _evaluation(rnas, n_in_system):
            return False

    if lipids is not None:

        n_in_system = get(molecular_system, n_lipids=True)

        if not _evaluation(lipids, n_in_system):
            return False

    if oligosaccharides is not None:

        n_in_system = get(molecular_system, n_oligosaccharides=True)

        if not _evaluation(oligosaccharides, n_in_system):
            return False

    if hydrogens is not None:

        hydrogen_indices = select(molecular_system, selection='atom_type=="H"')
        selection_indices = select(molecular_system, selection=selection)

        intersection = np.intersect1d(hydrogen_indices, selection_indices)
        n_in_system = intersection.shape[0]

        if not _evaluation(hydrogens, n_in_system):
            return False

    return True

