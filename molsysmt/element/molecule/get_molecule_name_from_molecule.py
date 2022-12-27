from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
import numpy as np

@digest()
def get_molecule_name_from_molecule(molecular_system, indices='all'):

    from . import get_n_molecules_from_system

    if is_all(indices):
        n_molecules = get_n_molecules_from_system(molecular_system)
        output = np.full(n_molecules, None, dtype=object)
    else:
        output = np.full(indices.shape[0], None, dtype=object)

    return output

