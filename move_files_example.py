# -*- coding: utf-8 -*-
# __author__ = 'guillaume auzias, guillaume.auzias@gmail.com'

import os
import shutil


FS_db_dir = '/riou/work/meca/data/FreeSurferDB/FS_database_OASIS'
pits_db_dir ='/riou/work/scalp/lucile/pits_database/oasis'
output_dir ='/riou/work/meca/hpc/users/auzias/OASIS_dib_dataset'

bad_subjects = ['OAS1_0129','OAS1_0198','OAS1_0444']
subjects = list()
subj_files_list=os.listdir(FS_db_dir)
for fil in subj_files_list:
    if fil.find('.')==-1:
        subjects.append(fil)
print 'subjects to be processed : ',subjects

for subject in subjects:
    print '-----------------------processing subject '+subject
    try:
        os.mkdir(os.path.join(output_dir,subject))

        shutil.copy(os.path.join(FS_db_dir,subject,'surf','lh.white.gii'), os.path.join(output_dir,subject,subject+'.lh.white.gii'))
        shutil.copy(os.path.join(FS_db_dir,subject,'surf','rh.white.gii'), os.path.join(output_dir,subject,subject+'.rh.white.gii'))
        shutil.copy(os.path.join(FS_db_dir,subject,'surf','lh.sphere.reg.gii'), os.path.join(output_dir,subject,subject+'.lh.sphere.reg.gii'))
        shutil.copy(os.path.join(FS_db_dir,subject,'surf','rh.sphere.reg.gii'), os.path.join(output_dir,subject,subject+'.rh.sphere.reg.gii'))
        print 'copy the freesurfer white and sphere.reg meshes'

        shutil.copy(os.path.join(pits_db_dir,subject,'dpfMap','L_dpf_0.03.gii'), os.path.join(output_dir,subject,subject+'.lh.depth.gii'))
        shutil.copy(os.path.join(pits_db_dir,subject,'dpfMap','R_dpf_0.03.gii'), os.path.join(output_dir,subject,subject+'.rh.depth.gii'))
        print 'copy the DPF'
        #print os.path.join(pits_db_dir,subject,'dpfMap','aplha_0.03','an0_dn20_r1.5','alpha0.03_an0_dn20_r1.5_L_area50FilteredTexturePits.gii')
        shutil.copy(os.path.join(pits_db_dir,subject,'dpfMap','alpha_0.03','an0_dn20_r1.5','alpha0.03_an0_dn20_r1.5_L_area50FilteredTexturePits.gii'), os.path.join(output_dir,subject,subject+'.lh.pits.gii'))
        shutil.copy(os.path.join(pits_db_dir,subject,'dpfMap','alpha_0.03','an0_dn20_r1.5','alpha0.03_an0_dn20_r1.5_R_area50FilteredTexturePits.gii'), os.path.join(output_dir,subject,subject+'.rh.pits.gii'))
        print 'copy the pits texture'
    except:
        print 'cannot be processed!'

