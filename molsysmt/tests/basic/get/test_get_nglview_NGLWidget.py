"""
Unit and regression test for the get module of the molsysmt package on xtc file systems.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt.systems import tests as tests_systems
import numpy as np


#def test_get_nglview_NGLWidget_1():
#    molsys = msm.convert([msm.demo['nglview']['1u19.gro'], msm.demo['nglview']['1u19.xtc']], to_form='molsysmt.MolSys')
#    view = msm.convert(molsys, to_form='nglview.NGLWidget')
#    check_comparison = msm.compare(molsys, view, comparison='info_no_form', rule='A_eq_B')
#    assert check_comparison

