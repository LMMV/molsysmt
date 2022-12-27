from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='mmtf.MMTFDecoder', to_form='mmtf.MMTFDecoder')
def add(to_item, item):

    raise NotImplementedMethodError()

