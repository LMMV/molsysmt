from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='openmm.System', to_form='openmm.System')
def add(to_item, item):

    raise NotImplementedMethodError()

