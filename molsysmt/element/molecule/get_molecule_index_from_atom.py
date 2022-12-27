from molsysmt._private.digestion import digest
import numpy as np

@digest()
def get_molecule_index_from_atom(molecular_system, indices='all'):

    from molsysmt.basic import get

    output = get(molecular_system, element='atom', indices=indices, component_index=True)

    return output

