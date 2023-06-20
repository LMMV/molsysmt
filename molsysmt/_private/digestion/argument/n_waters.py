from molsysmt._private.exceptions import ArgumentError

def digest_n_waters(n_waters, caller=None):

    if caller=='molsysmt.basic.get.get':
        if isinstance(n_waters, bool):
            return n_waters
    elif caller=='molsysmt.basic.contains.contains':
        if isinstance(n_waters, (bool, int)):
            return n_waters
    elif caller=='molsysmt.basic.is_composed_of.is_composed_of':
        if isinstance(n_waters, (bool, int)):
            return n_waters

    raise ArgumentError('n_waters', value=n_waters, caller=caller, message=None)

