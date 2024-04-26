#!/usr/bin/env python
# ##################################################
## Python 3.9
## Martin Iglesias
## Script for copy desired Media footage from external HDD to local folder.
##
###################################################


import os, sys, shutil, re
import logging
logging.basicConfig(level=logging.DEBUG)

# tocopy_path = os.path.normpath(r'D:\_temp\tierra_incognita')
tocopy_path = os.path.normpath(r'D:\Edicion_Reel\MEDIA_IN\DISCO_EXT\DRT24\tierra_incognita')
default_source_path = os.path.normpath(r"F:\tierra_incognita")
# source_path = os.path.normpath(input("Enter directory path for search footages: ") or default_source_path)
# os.path.isdir(source_path)
# logging.info(f" You has enter: {source_path}")
#
# try:
#     source_path = os.path.normalpath(input("Enter directory path for search footages: ") or default_source_path)
#     os.path.isdir(source_path)
#
# except:
#     pass
# else:
#     logging.info(f"{source_path} \nIs not a path or directory\n")
#     source_path = default_source_path

def copiar_footage(source_path, tocopy_path):

    def copy_folders(source_path, path_shot_name):
        ## check if folder exist , otherwise make it and copy files.
        if not os.path.exists(path_shot_name):
            # print(f"not exist {path_shot_name}")
        #     os.makedirs(path_shot_name)
        # else:
            ## make folders and copy files.
            print(f"\n... coping files from \nsource =={source_path} \nto\t   =={path_shot_name} \n")
            shutil.copytree(source_path, path_shot_name)
        # TO-DO: Evitar los preRenders

    for dir_path, dirs, file_names in os.walk(source_path):
        # logging.debug(f" dir_path = {dir_path}\n dirs = {dirs}\n file_names ={file_names}")
        for d in dirs:
            if "IN".upper() in str(d).upper():
                source_IN_path = os.path.join(dir_path, d)
                searching_IN = re.search('IN', str(dir_path), re.IGNORECASE) #.group(0)
                shot_folder_name = str(d).replace(searching_IN.group(0),'').removeprefix('-').removesuffix('_').replace('__', '_')
                # logging.debug(f" !!!\t base shot = {dir_path}")
                # print(f" d = {d}\n IN = {searching_IN} \nsource_IN_path = {source_IN_path} \n")
                # logging.debug(f" __ IN path old __ =  {source_IN_path}")
                path_shot_name = os.path.join(tocopy_path , source_IN_path.rsplit('\\in', 1)[0].rsplit('\\')[-1] , 'in')
                source_IN_path = os.path.join(source_IN_path.rsplit('\\in', 1)[0] , 'in')
                # print(f"path_shot_name {path_shot_name}")
                # logging.debug(f" __ IN path old __ =  {source_IN_path}")

                ## call copy function.
                copy_folders(source_IN_path, path_shot_name)
                """                if os.path.exists(source_IN_path):
                                    # logging.debug(f" __ IN path new __ =  {source_IN_path}")
                                    path_shot_name = os.path.join(tocopy_path, searching_IN)
                                    # logging.debug(f" __ SEARCHING IN  __ =  {path_shot_name}\n")
                                    ## call copy function.
                                    # copy_folders(source_IN_path, path_shot_name)
                                else:
                                    logging.debug(f" __ NO EXISTE IN path new __ =  {source_IN_path}")
                """


            if "FULLRES".upper() in str(d).upper():
                fullres_path = os.path.join(dir_path, d)
                # logging.debug(f"--> fullres is in path {fullres_path}")
                seaching_fullres = re.search('fullres', str(d) , re.IGNORECASE)
                # logging.debug(f"\t NAME to make a folder with fullres == {seaching_fullres.group(0) }")
                shot_folder_name = str(d).replace(seaching_fullres.group(0),'').removeprefix('-').removesuffix('_').replace('__', '_')
                # logging.debug(f"\t NAME to make a folder with fullres == { shot_folder_name}")
                path_shot_name = os.path.join(tocopy_path, os.path.join(shot_folder_name, 'Fullres'))
                ## call copy function.
                copy_folders(fullres_path, path_shot_name)

            """
                            ## check if folder exist , otherwise make it and copy files.
                            if not os.path.exists(path_shot_name):
                                print(f"not exist {path_shot_name}")
                                ## make folders and copy files.
                                # os.makedirs(path_shot_name)
                                # shutil.copytree(fullres_path, path_shot_name)
            """

        for file_name in file_names:
            # logging.debug(f" filenames = {file_name}")
            # logging.debug(f"--fullres is in path {dirs}" )
            if "FULLRES".upper() in str(file_name).upper():
                logging.debug(f"fullres is in path {dirs}" )
            # else:
            #     logging.debug(f"\nfullres is NOT in path {dir_path}")

if __name__ == '__main__':
    # directories()
    copiar_footage(default_source_path, tocopy_path)
