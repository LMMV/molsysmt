import molsysmt as msm
import numpy as np
from pathlib import Path
import os

# purge
print('Removing old files...')
files_to_be_purged = ['vacuum.pdb', 'vacuum.msmpk']
for filename in files_to_be_purged:
    if os.path.isfile(filename):
        os.remove(filename)

molsys = msm.build.build_peptide('TyrGlyGlyPheMet')
_ = msm.convert(molsys, to_form='vacuum.msmpk')
_ = msm.convert(molsys, to_form='vacuum.pdb')
del(molsys)


