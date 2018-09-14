


import os
import commands

if __name__ == "__main__":
    files = ['lh.white', 'rh.white', 'lh.sphere.reg', 'rh.sphere.reg']
    db_directory = '/hpc/scalp/data/PASTEUR_database/fs600_isotrope'
    subj_files_list = os.listdir(db_directory)
    subj_list_processed = []
    for fil in subj_files_list:
        if not '.' in fil:
            subj_list_processed.append(fil)

    for subject in subj_list_processed:
        print(subject)
        for f in files:
            conv_file = os.path.join(db_directory,subject,'surf',f)
            cmd = "mris_convert %s %s" % (conv_file, conv_file+'.gii')
            #cmd = "frioul_batch 'export FREESURFER_HOME=/hpc/soft/freesurfer/freesurfer_6.0.0/; export SUBJECTS_DIR=/hpc/scalp/data/PASTEUR_database/fs600_isotrope; freesurfer_setup; mri_convert %s %s'" % (subject, imported_fname)
            print(cmd)
            a = commands.getoutput(cmd)
            print(a)


