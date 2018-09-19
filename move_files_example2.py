# -*- coding: utf-8 -*-
# __author__ = 'guillaume auzias, guillaume.auzias@gmail.com'
#____a un tout petit KIKI

import os
import shutil
import sys

if __name__ == '__main__':
    centers = None# all centers found will be processed by default
    move_to_analysis = 'default_analysis'#None
    subjects_in = None# all subjects found will be processed by default
    print sys.argv
    if len(sys.argv) == 1:
        print 'mandatory input :: BV_directory [centers to process] [analysis where to move the data to] [subject to process]'
    if len(sys.argv) > 1:
        BV_db_dir = sys.argv[1]#'/mnt/data/work/BV_database/BV_disco_test'
    if len(sys.argv) > 2:
        centers = [sys.argv[2]]
    if len(sys.argv) > 3:
        move_to_analysis = sys.argv[3]
    if len(sys.argv) > 4:
        subjects_in = [sys.argv[4]]

    ## autodetect centers if not given as input
    if centers is None:
        centers = list()
        centers_files_list = os.listdir(BV_db_dir)
        for fil in centers_files_list:
            if fil.find('.') == -1:
                centers.append(fil)
    print 'centers to be processed : ',centers

    for center in centers:
        center_path = os.path.join(BV_db_dir,center)
        ## autodetect subjects if not given as input
        if subjects_in is None:
            subjects = list()
            subj_files_list=os.listdir(center_path)
            for fil in subj_files_list:
                if fil.find('.')==-1:
                    subjects.append(fil)
        else:
            subjects = subjects_in
        print 'subjects to be processed in center '+center+' : ',subjects

        for subject in subjects:
            print '-----------------------processing subject '+subject
            # search for the old 'surface' directory to move
            if os.path.exists(os.path.join(center_path, subject,'surface')):
               old_surface_dir = os.path.join(center_path, subject,'surface')
            else:
                old_surface_dir = None # print 'no surface analysis found for this subject, no file moved'


            # search for the appropriate new location
            new_surface_dir = None
            # autodetect analysis if not given as input
            if move_to_analysis is None:
                nb_analysis_found = 0
                for path, dirs, files in os.walk(os.path.join(center_path, subject)):
                    if os.path.join('segmentation','mesh') in path:
                        new_surface_dir = path
                        nb_analysis_found += 1
                if nb_analysis_found > 1:
                    print 'several analyses have been found for subject '+subject+' you must specify which one you want to move the surface directory to'
                    raise Exception('several analyses found')
            else:
                for path, dirs, files in os.walk(os.path.join(center_path, subject)):
                    if os.path.join(move_to_analysis,'segmentation','mesh') in path:
                        if 'surface_analysis' not in path:
                            new_surface_dir = os.path.join(path,'surface_analysis')

            ## now lets do the job needed
            if new_surface_dir is None:
                print 'not able to find the target location!'
            else:
                if os.path.exists(new_surface_dir) == 0:
                    if old_surface_dir is None:
                        print 'no old surface analysis found for this subject'
                    else:
                        print 'moving the files to '+new_surface_dir
                        shutil.move(old_surface_dir,new_surface_dir)
                if os.path.exists(new_surface_dir):
                    print 'updated directory already exists, checking for file name updates'
                    files_list = os.listdir(new_surface_dir)
                    for file in files_list:
                        if 'white_hippo' in file:
                            print 'updating file name *white_hippo -> *white_pole_cingular'
                            file_dest = file.replace('white_hippo','white_pole_cingular')
                            print file
                            print file_dest
                            shutil.move(os.path.join(new_surface_dir,file),os.path.join(new_surface_dir,file_dest))
                        if 'white_insula' in file:
                            print 'updating file name *white_insula -> *white_pole_insula'
                            file_dest = file.replace('white_insula','white_pole_insula')
                            print file
                            print file_dest
                            shutil.move(os.path.join(new_surface_dir,file),os.path.join(new_surface_dir,file_dest))
