def is_openmm_Context(item):


    item_fullname = item.__class__.__module__+'.'+item.__class__.__name__
    output = (item_fullname == 'openmm.openmm.Context')

    return output

