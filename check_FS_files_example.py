
import os

if __name__ == '__main__':

    fs_database_path='/hpc/scalp/data/PASTEUR_database/fs600_isotrope'

    subjects_list = list()
    subj_files_list=os.listdir(fs_database_path)
    for fil in subj_files_list:
        if fil.find('.') == -1:
            subjects_list.append(fil)

    sides=['lh','rh']
    bad_subj_gifti = list()
    bad_subj_sphere = list()
    for side in sides:
        for subj in subjects_list:
            if not os.path.exists(os.path.join(fs_database_path, subj,'surf',side+'.white.gii')):
                bad_subj_gifti.append(subj+'_'+side)
            if not os.path.exists(os.path.join(fs_database_path, subj, 'surf', side + '.sphere.reg.gii')):
                bad_subj_sphere.append(subj + '_' + side)

    print('number of no gifti subjects : '+str(len(bad_subj_gifti)))
    print(bad_subj_gifti)
    print('number of no sphere subjects : '+str(len(bad_subj_sphere)))
    print(bad_subj_sphere)