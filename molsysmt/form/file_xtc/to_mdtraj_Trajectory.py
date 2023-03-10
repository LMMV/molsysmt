from molsysmt._private.digestion import digest

@digest(form='file:xtc')
def to_mdtraj_Trajectory(item, atom_indices='all', structure_indices='all'):

    from . import to_mdtraj_XTCTrajectoryFile
    from ..mdtraj_XTCTrajectoryFile import to_mdtraj_Trajectory as mdtraj_XTCTrajectoryFile_to_mdtraj_Trajectory

    tmp_item = to_mdtraj_XTCTrajectoryFile(item)
    tmp_item = mdtraj_XTCTrajectoryFile_to_mdtraj_Trajectory(tmp_item, atom_indices=atom_indices,
            structure_indices=structure_indices)

    return tmp_item

