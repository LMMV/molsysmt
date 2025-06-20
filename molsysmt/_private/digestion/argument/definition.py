import numpy as np
from ...exceptions import ArgumentError

definitions = {
    'get_mass': ['OpenMM', 'physical'],
    'get_hydrophobicity': ['eisenberg', 'rao', 'sweet', 'kyte', 'abraham', 'bull', 'guy', 'miyazawa', 'roseman',
                         'wolfenden', 'chothia', 'hopp', 'manavalan', 'black', 'fauchere'],
    'get_volume': ['grantham'],
    'get_charge': ['physical_pH7', 'collantes', 'OpenMM'],
    'get_surface_area': ['collantes'],
    'get_polarity': ['grantham', 'zimmerman'],
    'get_area_buried': ['rose'],
    'get_buried_fraction': ['janin'],
    'get_atomic_radius': ['vdw'],
    'get_transmembrane_tendency': ['zhao', 'senes'],
}

def digest_definition(definition, caller=None):

    if caller=='molsysmt.physchem.get_mass.get_mass':
        if isinstance(definition, str):
            if definition in ['OpenMM', 'physical']:
                return definition

    elif caller=='molsysmt.physchem.get_mass.get_mass':
        if isinstance(definition, str):
            if definition in definitions['get_mass']:
                return definition

    elif caller=='molsysmt.physchem.get_hydrophobicity.get_hydrophobicity':
        if isinstance(definition, str):
            if definition in definitions['get_hydrophobicity']:
                return definition

    elif caller=='molsysmt.physchem.get_volume.get_volume':
        if isinstance(definition, str):
            if definition in definitions['get_volume']:
                return definition

    elif caller=='molsysmt.physchem.get_charge.get_charge':
        if isinstance(definition, str):
            if definition in definitions['get_charge']:
                return definition

    elif caller=='molsysmt.physchem.get_surface_area.get_surface_area':
        if isinstance(definition, str):
            if definition in definitions['get_surface_area']:
                return definition

    elif caller=='molsysmt.physchem.get_polarity.get_polarity':
        if isinstance(definition, str):
            if definition in definitions['get_polarity']:
                return definition

    elif caller=='molsysmt.physchem.get_area_buried.get_area_buried':
        if isinstance(definition, str):
            if definition in definitions['get_area_buried']:
                return definition

    elif caller=='molsysmt.physchem.get_buried_fraction.get_buried_fraction':
        if isinstance(definition, str):
            if definition in definitions['get_buried_fraction']:
                return definition

    elif caller=='molsysmt.physchem.get_atomic_radius.get_atomic_radius':
        if isinstance(definition, str):
            if definition in definitions['get_atomic_radius']:
                return definition

    elif caller=='molsysmt.physchem.get_transmembrane_tendency.get_transmembrane_tendency':
        if isinstance(definition, str):
            if definition in definitions['get_transmembrane_tendency']:
                return definition

    return ArgumentError('definition', value=definition, caller=caller, message=None)

