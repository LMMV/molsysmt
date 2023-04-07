MODULE MODULE_BOX

USE MODULE_PBC

CONTAINS

  !! This box is not used by gro, xtc and trr:
  
  !! box(1,1) = v1_x, box(1,2) = v1_y, box(1,3) = v1_z
  !! box(2,1) = v2_x, box(2,2) = v2_y, box(2,3) = v2_z
  !! box(3,1) = v3_x, box(3,2) = v3_y, box(3,3) = v3_z
  
  !! The gromacs box and cell are:
  !!
  !! box(1,1) = v1_x, box(1,2) = 0,    box(1,3) = 0
  !! box(2,1) = v2_x, box(2,2) = v2_y, box(2,3) = 0
  !! box(3,1) = v3_x, box(3,2) = v3_y, box(3,3) = v3_z
  !!
  !! cell(1,1)= v1_x, cell(1,2)= alpha cell(1,3)= beta
  !! cell(2,1)= 0,    cell(2,2)= v2_y, cell(2,3)= gamma
  !! cell(3,1)= 0,    cell(3,2)= 0,    cell(3,3)= v3_z
  
  SUBROUTINE BOX2INVBOX (box,invbox,nframes)
  
    IMPLICIT NONE
    INTEGER,INTENT(IN)::nframes
    DOUBLE PRECISION,DIMENSION(nframes,3,3),INTENT(IN)::box
    DOUBLE PRECISION,DIMENSION(nframes,3,3),INTENT(OUT)::invbox
  
    invbox=0.0d0
  
    invbox(:,1,1)=1.0d0/box(:,1,1)
    invbox(:,2,2)=1.0d0/box(:,2,2)
    invbox(:,3,3)=1.0d0/box(:,3,3)
  
    invbox(:,2,1)=-box(:,2,1)/(box(:,1,1)*box(:,2,2))
    invbox(:,3,1)=(box(:,2,1)*box(:,3,2)-box(:,3,1)*box(:,2,2))/(box(:,1,1)*box(:,2,2)*box(:,3,3))
    invbox(:,3,2)=-box(:,3,2)/(box(:,2,2)*box(:,3,3))
  
  END SUBROUTINE BOX2INVBOX

  FUNCTION LENGTH_EDGES_BOX(box, nframes) RESULT(lengths)

    IMPLICIT NONE
    INTEGER,INTENT(IN)::nframes
    DOUBLE PRECISION,DIMENSION(nframes,3,3),INTENT(IN)::box
    DOUBLE PRECISION,DIMENSION(nframes,3)::lengths
    INTEGER::ii

    lengths = 0.0d0

    DO ii=1,nframes

        lengths(ii,1) = sqrt(box(ii,1,1)**2 + box(ii,1,2)**2 + box(ii,1,3)**2)
        lengths(ii,2) = sqrt(box(ii,2,1)**2 + box(ii,2,2)**2 + box(ii,2,3)**2)
        lengths(ii,3) = sqrt(box(ii,3,1)**2 + box(ii,3,2)**2 + box(ii,3,3)**2)

    END DO

  END FUNCTION LENGTH_EDGES_BOX

  FUNCTION ANGLES_BOX(box, nframes) RESULT(angles)

    IMPLICIT NONE
    INTEGER,INTENT(IN)::nframes
    DOUBLE PRECISION,DIMENSION(nframes,3,3),INTENT(IN)::box
    DOUBLE PRECISION,DIMENSION(nframes,3)::angles
    DOUBLE PRECISION::x,y,z,a,b,c
    DOUBLE PRECISION,PARAMETER::fact_pi_div_180=1.745329251994329547437168059786927E-0002
    INTEGER::ii

    angles = 0.0d0

    DO ii=1,nframes

        x=sqrt(box(ii,1,1)**2+box(ii,1,2)**2+box(ii,1,3)**2)
        y=sqrt(box(ii,2,1)**2+box(ii,2,2)**2+box(ii,2,3)**2)
        z=sqrt(box(ii,3,1)**2+box(ii,3,2)**2+box(ii,3,3)**2)
        a=(acos(dot_product(box(ii,2,:),box(ii,3,:))/(y*z)))/fact_pi_div_180 ! alpha: v2 and v3
        b=(acos(dot_product(box(ii,3,:),box(ii,1,:))/(x*z)))/fact_pi_div_180 ! beta: v1 and v3
        c=(acos(dot_product(box(ii,2,:),box(ii,1,:))/(x*y)))/fact_pi_div_180 ! gamma: v1 and v2
        angles(ii,1) = a
        angles(ii,2) = b
        angles(ii,3) = c

    END DO

  END FUNCTION ANGLES_BOX

  FUNCTION LENGTHS_AND_ANGLES_TO_BOX (lengths, angles, nframes) RESULT(box)

    IMPLICIT NONE
    INTEGER,INTENT(IN)::nframes
    DOUBLE PRECISION,DIMENSION(nframes,3),INTENT(IN):: lengths, angles
    INTEGER::ii
    DOUBLE PRECISION,DIMENSION(nframes,3,3)::box
    DOUBLE PRECISION::alpha,beta,gamm,x,y,z
    DOUBLE PRECISION,PARAMETER::fact_pi_div_180=1.745329251994329547437168059786927E-0002
 
    box=0.0d0

    DO ii=1,nframes
  
      alpha=angles(ii,1)*fact_pi_div_180
      beta=angles(ii,2)*fact_pi_div_180
      gamm=angles(ii,3)*fact_pi_div_180
      x=lengths(ii,1)
      y=lengths(ii,2)
      z=lengths(ii,3)
      box(ii,1,1)=x
      box(ii,2,1)=y*cos(gamm)
      box(ii,2,2)=y*sin(gamm)
      box(ii,3,1)=z*cos(beta)
      box(ii,3,2)=z*(cos(alpha)-cos(beta)*cos(gamm))/sin(gamm) 
      box(ii,3,3)=sqrt(z*z-box(ii,3,1)**2-box(ii,3,2)**2)
  
    END DO

  END FUNCTION LENGTHS_AND_ANGLES_TO_BOX

  SUBROUTINE WRAP_PBC (coors,centers,box,ortho,natoms,nframes)
  
    INTEGER,INTENT(IN)::ortho,natoms,nframes
    double precision,DIMENSION(nframes,3,3),INTENT(IN)::box
    double precision,dimension(nframes,natoms,3),intent(INOUT)::coors
    double precision,dimension(nframes,1,3),intent(IN)::centers
  
    DOUBLE PRECISION,DIMENSION(nframes,3,3)::inv
    DOUBLE PRECISION,DIMENSION(3,3)::tmp_box,tmp_inv
    DOUBLE PRECISION,DIMENSION(3)::aux,center

    INTEGER::ii,jj

    inv=0.0d0
    CALL BOX2INVBOX (box, inv, nframes)

    DO ii=1,nframes
      tmp_box=box(ii,:,:)
      tmp_inv=inv(ii,:,:)
      center=centers(ii,1,:)
      DO jj=1,natoms
        aux=coors(ii,jj,:)-center
        CALL PBC(aux,tmp_box,tmp_inv,ortho)
        coors(ii,jj,:)=center+aux
      END DO
    END DO

  END SUBROUTINE WRAP_PBC
 
  SUBROUTINE WRAP_MIC (coors,centers,box,ortho,natoms,nframes)
  
    INTEGER,INTENT(IN)::ortho,natoms,nframes
    double precision,DIMENSION(nframes,3,3),INTENT(IN)::box
    double precision,dimension(nframes,natoms,3),intent(INOUT)::coors
    double precision,dimension(nframes,1,3),intent(IN)::centers
  
    DOUBLE PRECISION,DIMENSION(nframes,3,3)::inv
    DOUBLE PRECISION,DIMENSION(3,3)::tmp_box,tmp_inv
    DOUBLE PRECISION,DIMENSION(3)::aux,center

    INTEGER::ii,jj

    inv=0.0d0
    CALL BOX2INVBOX (box, inv, nframes)

    DO ii=1,nframes
      tmp_box=box(ii,:,:)
      tmp_inv=inv(ii,:,:)
      center=centers(ii,1,:)
      DO jj=1,natoms
        aux=coors(ii,jj,:)-center
        CALL MIC(aux,tmp_box,tmp_inv,ortho)
        coors(ii,jj,:)=center+aux
      END DO
    END DO

  END SUBROUTINE WRAP_MIC
 
  SUBROUTINE UNWRAP (coors,box,ortho,natoms,nframes)
  
    INTEGER,INTENT(IN)::ortho,natoms,nframes
    double precision,DIMENSION(nframes,3,3),INTENT(IN)::box
    double precision,dimension(nframes,natoms,3),intent(INOUT)::coors
  
    DOUBLE PRECISION,DIMENSION(nframes,3,3)::inv
    DOUBLE PRECISION,DIMENSION(3,3)::tmp_box,tmp_inv
    DOUBLE PRECISION,DIMENSION(3)::delta

    INTEGER::ii,jj

    inv=0.0d0
    CALL BOX2INVBOX (box, inv, nframes)

    DO ii=1,nframes-1
      tmp_box=box(ii,:,:)
      tmp_inv=inv(ii,:,:)
      DO jj=1,natoms
        delta(:) = coors(ii+1,jj,:)-coors(ii,jj,:)
        CALL MIC(delta,tmp_box,tmp_inv,ortho)
        coors(ii+1,jj,:)=coors(ii,jj,:)+delta(:)
      END DO
    END DO

  END SUBROUTINE UNWRAP

!  SUBROUTINE COMPACT_MOLECULES (coors, molecules_indices, molecules_values, molecules_starts, &
!          & bonded_atoms_indices, bonded_atoms_values, bonded_atoms_starts, &
!          & structure_indices, box, ortho, n_structures, n_atoms, n_molecules_indices, &
!          & n_molecules_values, n_bonded_atoms_indices, n_bonded_atoms_values, &
!          & n_structure_indices)
!
!    IMPLICIT NONE
!
!    INTEGER,INTENT(IN):: n_structures, n_atoms, ortho, n_structure_indices
!    INTEGER,INTENT(IN):: n_molecules_indices, n_molecules_values
!    INTEGER,INTENT(IN):: n_bonded_atoms_indices, n_bonded_atoms_values
!    DOUBLE PRECISION,DIMENSION(n_structures,n_atoms,3),INTENT(INOUT)::coors
!    INTEGER,DIMENSION(n_molecules_indices),INTENT(IN)::molecules_indices
!    INTEGER,DIMENSION(n_molecules_indices+1),INTENT(IN)::molecules_starts
!    INTEGER,DIMENSION(n_molecules_values),INTENT(IN)::molecules_values
!    INTEGER,DIMENSION(n_bonded_atoms_indices),INTENT(IN)::bonded_atoms_indices
!    INTEGER,DIMENSION(n_bonded_atoms_indices+1),INTENT(IN)::bonded_atoms_starts
!    INTEGER,DIMENSION(n_bonded_atoms_values),INTENT(IN)::bonded_atoms_values
!    INTEGER,DIMENSION(n_structure_indices),INTENT(IN)::structure_indices
!    DOUBLE PRECISION,DIMENSION(n_structures,3,3),INTENT(IN)::box
!    DOUBLE PRECISION,DIMENSION(n_structures,3,3)::inv
!
!    INTEGER:: ii, jj, kk, ll
!    INTEGER:: molecule_start, molecule_end, molecule_natoms
!    INTEGER:: n_left, n_storage
!    INTEGER:: atom_id, atom_id1, atom_id2, atom_pos1
!    LOGICAL,DIMENSION(n_atoms)::aux_filter
!    DOUBLE PRECISION,DIMENSION(3)::vect_aux
!    INTEGER,DIMENSION(:),ALLOCATABLE::left,storage
!    INTEGER,DIMENSION(n_atoms)::atom_id_to_position_in_bonds
!    INTEGER::frame_index
!    
!    CALL BOX2INVBOX (box, inv, n_structures)
!
!    aux_filter(:)=.FALSE.
!
!    atom_id_to_position_in_bonds(:)=0
!    DO ii=1, n_bonded_atoms_indices
!        atom_id = bonded_atoms_indices(ii)+1
!        atom_id_to_position_in_bonds(atom_id)=ii
!    END DO 
!
!    DO ii=1, n_molecules_indices
!
!        molecule_start=molecules_starts(ii)+1
!        molecule_end=molecules_starts(ii+1)
!        molecule_natoms=molecule_end-molecule_start+1
!
!        n_left=1
!        ALLOCATE(left(n_left),storage(molecule_natoms))
!        jj=molecules_values(molecule_start)+1
!        left(1)=jj
!        aux_filter(jj)=.TRUE.
!
!        DO WHILE (n_left>0)
!            n_storage=0
!            DO jj=1,n_left
!                atom_id1 = left(jj)
!                atom_pos1 = atom_id_to_position_in_bonds(atom_id1)
!                DO kk=bonded_atoms_starts(atom_pos1)+1,bonded_atoms_starts(atom_pos1+1)
!                    atom_id2=bonded_atoms_values(kk)+1
!                    IF (aux_filter(atom_id2).eqv..FALSE.) THEN
!                        DO ll=1,n_structure_indices
!                            frame_index=structure_indices(ll)+1
!                            vect_aux(:)=coors(frame_index,atom_id2,:)-coors(frame_index,atom_id1,:)
!                            CALL PBC(vect_aux,box(frame_index,:,:),inv(frame_index,:,:),ortho)
!                            coors(frame_index,atom_id2,:)=coors(frame_index,atom_id1,:)+vect_aux(:)
!                        END DO
!                        aux_filter(atom_id2)=.TRUE.
!                        n_storage=n_storage+1
!                        storage(n_storage)=atom_id2
!                    END IF
!                END DO
!            END DO
!            n_left=n_storage
!            IF (n_left>0) THEN
!                DEALLOCATE(left)
!                ALLOCATE(left(n_left))
!                left(:)=storage(1:n_left)
!            END IF
!        END DO
!
!        DEALLOCATE(left,storage)
!
!    END DO
!
!  END SUBROUTINE COMPACT_MOLECULES
!
!  SUBROUTINE MINIMUM_IMAGE_CONVENTION(coors, reference_coors, center_groups, groups_indices, groups_atoms_indices, groups_starts, &
!          structure_indices, box, ortho, n_structures, n_atoms, n_groups, n_groups_atoms, n_structure_indices)
!
!    IMPLICIT NONE
!
!    INTEGER,INTENT(IN):: n_structures, n_atoms, n_groups, n_groups_atoms, n_structure_indices, ortho
!    DOUBLE PRECISION,DIMENSION(n_structures,n_atoms,3),INTENT(INOUT)::coors
!    DOUBLE PRECISION,DIMENSION(n_structure_indices,1,3),INTENT(IN)::reference_coors
!    DOUBLE PRECISION,DIMENSION(n_structure_indices,n_groups,3),INTENT(IN)::center_groups
!    INTEGER,DIMENSION(n_groups),INTENT(IN)::groups_indices ! Molecules in this case
!    INTEGER,DIMENSION(n_groups+1),INTENT(IN)::groups_starts
!    INTEGER,DIMENSION(n_groups_atoms),INTENT(IN)::groups_atoms_indices
!    INTEGER,DIMENSION(n_structure_indices),INTENT(IN)::structure_indices
!    DOUBLE PRECISION,DIMENSION(n_structures,3,3),INTENT(IN)::box
!
!    INTEGER::ii,jj,ll
!    INTEGER::atom_index, frame_index
!    DOUBLE PRECISION,DIMENSION(n_structure_indices,3,3)::box_frames, inv_frames
!    DOUBLE PRECISION,DIMENSION(n_structure_indices,1,3)::vect_aux
!
!    DO ll=1,n_structure_indices
!        frame_index=structure_indices(ll)+1
!        box_frames(ll,:,:)=box(frame_index,:,:)
!    END DO
!
!    CALL BOX2INVBOX (box_frames, inv_frames, n_structure_indices)
!
!    DO ii=1, n_groups
!
!        vect_aux(:,1,:) = center_groups(:,ii,:) - reference_coors(:,1,:)
!
!        CALL PBC_TENSOR(vect_aux, box_frames, inv_frames, ortho, n_structure_indices, 1)
!
!        DO jj=groups_starts(ii)+1, groups_starts(ii+1)
!            atom_index = groups_atoms_indices(jj)+1
!            DO ll=1,n_structure_indices
!                frame_index=structure_indices(ll)+1
!                coors(frame_index, atom_index, :) = coors(frame_index, atom_index, :) - center_groups(ll, ii, :) +&
!                & vect_aux(ll, 1, :) + reference_coors(ll, 1, :)
!            END DO
!        END DO
!    END DO
!
!  END SUBROUTINE MINIMUM_IMAGE_CONVENTION

END MODULE MODULE_BOX

