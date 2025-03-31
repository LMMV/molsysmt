form_name = 'molsysmt.Topology'
form_type = 'class'
form_info = ["", ""]

piped_topological_attribute = None
piped_structural_attribute = None
piped_any_attribute = None
bonds_are_explicit = True
bonds_can_be_computed = False

from .is_form import is_form

from .attributes import attributes
from .has_attribute import has_attribute

from .extract import extract
from .copy import copy
from .add import add
from .merge import merge
from .append_structures import append_structures
from .get_topological_attributes import *
from .set import *
from .iterators import TopologyIterator

from .add_bonds import add_bonds
from .remove_bonds import remove_bonds

from .to_string_amino_acids_3 import to_string_amino_acids_3
from .to_string_amino_acids_1 import to_string_amino_acids_1
from .to_string_pdb_text import to_string_pdb_text
from .to_file_h5msm import to_file_h5msm, dump_topology_to_h5msm
from .to_file_pdb import to_file_pdb
from .to_file_psf import to_file_psf
from .to_mdtraj_Topology import to_mdtraj_Topology
from .to_networkx_Graph import to_networkx_Graph
from .to_openmm_Topology import to_openmm_Topology
from .to_parmed_Structure import to_parmed_Structure
from .to_pytraj_Topology import to_pytraj_Topology
from .to_nglview_NGLWidget import to_nglview_NGLWidget

_convert_to={
        'molsysmt.Topology': extract,
        'mdtraj.Topology': to_mdtraj_Topology,
        'string:amino_acids_1': to_string_amino_acids_1,
        'string:amino_acids_3': to_string_amino_acids_3,
        'string:pdb_text': to_string_pdb_text,
        'file:h5msm': to_file_h5msm,
        'file:pdb': to_file_pdb,
        'file:psf': to_file_psf,
        'networkx.Graph': to_networkx_Graph,
        'openmm.Topology': to_openmm_Topology,
        'parmed.Structure': to_parmed_Structure,
        'pytraj.Topology': to_pytraj_Topology,
        'nglview.NGLWidget': to_nglview_NGLWidget,
        }
