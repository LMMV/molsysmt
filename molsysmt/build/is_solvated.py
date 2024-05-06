from molsysmt._private.digestion import digest
from molsysmt import pyunitwizard as puw

@digest()
def is_solvated(molecular_system, skip_digestion=False):
    """
    To be written soon...
    """

    from molsysmt.basic import get

    output = False

    n_waters, volume = get(molecular_system, element='system', n_waters=True, box_volume=True, skip_digestion=True)

    if (n_waters>0) and (volume is not None):

        density_number = puw.get_value((n_waters/volume), to_unit='1/nm**3')

        if (density_number)>15:

            output = True

    return output

