import molsysmt as msm
from molsysmt import pyunitwizard as puw
import numpy as np
from pathlib import Path
import os
from pathlib import Path
import shutil

data_dir = Path('../../data/.')

# New xyznpy files

molecular_system = np.zeros([3,4,3], dtype='float64') * puw.unit('nm')
molecular_system[0,0,:] = [0, 2, -1] * puw.unit('nm')
molecular_system[1,0,:] = [1, 2, -1] * puw.unit('nm')
molecular_system[2,0,:] = [0, 2, -1] * puw.unit('nm')
molecular_system[0,1,:] = [-1, 1, 1] * puw.unit('nm')
molecular_system[1,1,:] = [-1, 0, 1] * puw.unit('nm')
molecular_system[2,1,:] = [0, 0, 1] * puw.unit('nm')
molecular_system[0,2,:] = [-2, 0, 1] * puw.unit('nm')
molecular_system[1,2,:] = [-2, 0, 0] * puw.unit('nm')
molecular_system[2,2,:] = [-1, 1, 0] * puw.unit('nm')
molecular_system[0,3,:] = [-2, -2, -2] * puw.unit('nm')
molecular_system[1,3,:] = [0, 0, 0] * puw.unit('nm')
molecular_system[2,3,:] = [2, 2, 2] * puw.unit('nm')
msm.convert(molecular_system, to_form='traj_particles_4.xyznpy')

shutil.move('traj_particles_4.xyznpy', Path(data_dir, 'xyznpy/traj_particles_4.xyznpy'))

