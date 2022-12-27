from molsysmt._private.digestion import digest

@digest(form='molsysmt.Topology')
def to_string_aminoacids3(item, group_indices='all'):

    from . import get_group_name_from_group

    group_names = get_group_name_from_group(item, indices=group_indices)
    tmp_item = ''.join([ii.title() for ii in group_names])

    return tmp_item

