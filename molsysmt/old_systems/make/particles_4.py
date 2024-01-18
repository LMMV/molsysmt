import molsysmt as msm
from molsysmt import pyunitwizard as puw
import numpy as np
from pathlib import Path
import os

data_dir = Path('../../../data/.')

# Purge

files_to_be_purged = [
        'xyznpy/traj_particles_4.xyznpy',
        ]

for filename in files_to_be_purged:
    filepath = Path(data_dir, filename)
    if os.path.isfile(filepath):
        os.remove(filepath)


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
msm.convert(molecular_system, to_form=Path(data_dir,'xyznpy/traj_particles_4.xyznpy'))

