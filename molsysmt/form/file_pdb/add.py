from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='file:pdb', to_form='file:pdb')
def add(to_item, item):

    raise NotImplementedMethodError()

