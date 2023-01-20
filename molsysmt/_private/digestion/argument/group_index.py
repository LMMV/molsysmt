from ...exceptions import ArgumentError
from ...variables import is_all

functions_with_boolean = (
        'molsysmt.basic.get.get',
        'molsysmt.basic.iterator.__init__',
        'iterators.__init__',
        )

def digest_group_index(group_index, caller=None):
    """Checks if `group_index` has the expected type and value.

    Parameters
    ----------
    group_index : Any
        The `group_index` argument for digestion.
    caller: str, optional
        Name of the function or method that is being digested.

    .. _PEP 484:
        https://www.python.org/dev/peps/pep-0484/#the-any-type

    Returns
    -------
    bool
        Either True or False when caller is `get`.

    Raises
    -------
    ArgumentError
        If the given `group_index` has not of the correct type or value.
    """

    if caller.endswith(functions_with_boolean):
        if isinstance(group_index, bool):
            return group_index

    raise ArgumentError('group_index', value=group_index, caller=caller, message=None)

