from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='file:mmtf', to_form='file:mmtf')
def add(to_item, item):

    raise NotImplementedMethodError()

