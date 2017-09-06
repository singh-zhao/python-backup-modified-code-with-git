#!/usr/bin/python
#coding:utf-8

import os

import time
import shutil
import inspect
import logging

import git_opt
from git_opt import Git_operator

class File_operator(object):
    """ file backup and create git list file and patch  """
    __git_opt = Git_operator()
    __custom_inited = False
    __args_line = []
    __src_root_path = str()
    __cmd_path = str()
    __dest_dir = str()
    __git_path = str()
    def __init__(self, args_line="", git_opt=Git_operator()):
        self.__custom_inited = False
        self.__git_opt = git_opt
        self.__args_line = args_line
        pass

    def custom_init(self, cmd_dir, src_root_dir, dest_dir, git_path):
        self.__custom_inited = True
        self.__cmd_path = cmd_dir
        self.__src_root_path = src_root_dir
        self.__dest_dir = dest_dir
        self.__git_path = git_path
        return

    def get_backup_dir_with_timestamp_under_rootdir(self, \
        backup_root_path, backup_name=""):
        if not os.path.exists(backup_root_path):
            print("%s: %s not exists!!" % \
                (inspect.stack()[0][2], backup_root_path))
            return
        time_stamp = time.strftime("%04Y-%02m-%02d-%02H-%02M-%02S", time.localtime())
        m_backup_path = os.path.join(os.path.dirname(backup_root_path), backup_name) \
            + "-" + time_stamp
        if not os.path.exists(m_backup_path):
            os.makedirs(m_backup_path)
        return m_backup_path

    def write_backuplist_to_file(self, m_path, m_content, m_file_name="file_list.txt"):
        if not os.path.exists(m_path):
            logging.info("%s not exists!!", m_path)
            return
        #backup file list
        m_file_list_fd = os.open(os.path.join(m_path, m_file_name), os.O_RDWR|os.O_CREAT)
        m_bytes_writen = os.write(m_file_list_fd, m_content)
        return m_bytes_writen

    def clean_useless_files(self, clean_path, \
        file_suffix=[".o", ".ko", ".o.cmd", ".order", ".builtin", ".mod.c"]):
        if not os.path.exists(clean_path):
            logging.info("%s not exists!", clean_path)
        for mfile in os.listdir(clean_path):
            if os.path.isdir(os.path.join(clean_path, mfile)) is True:
                self.clean_useless_files(os.path.join(clean_path, mfile))
            elif os.path.exists(os.path.join(clean_path, mfile)) is True:
                for rm_file in file_suffix:
                    if mfile.endswith(rm_file):
                        os.remove(os.path.join(clean_path, mfile))
                        #fie removed
                        logging.info("%s was removed!!", os.path.join(clean_path, mfile))
            else:
                logging.info("%s not exists!!", mfile)
        return

    def cp_file_list_to_back_dir(self, file_list, dest_dir, src_dir=__git_path):
        logging.info("src_dir:\n\t%s\nfile_list:", src_dir)
        dest_dir = os.path.join(dest_dir, os.path.basename(src_dir))
        for mlist in file_list:
            print "\t%s" % mlist
            if os.path.isdir(os.path.join(src_dir, mlist)):
                if not os.path.exists(os.path.join(dest_dir, mlist)):
                    os.makedirs(os.path.join(dest_dir, mlist))
                shutil.copytree(os.path.join(src_dir, mlist), \
                    os.path.join(dest_dir, os.path.dirname(mlist)))
            elif os.path.exists(os.path.join(src_dir, mlist)):
                if not os.path.exists(os.path.join(dest_dir, os.path.dirname(mlist))):
                    os.makedirs(os.path.join(dest_dir, os.path.dirname(mlist)))
                shutil.copy(os.path.join(src_dir, mlist), \
                    os.path.join(dest_dir, os.path.dirname(mlist)))
            else:
                logging.error("%s not exist!!", mlist)
        return

    def back_up_files(self, src_root_path, dest_path, git_path, cmd_path=os.getcwd()):
        if self.__custom_inited is False:
            self.custom_init(cmd_path, src_root_path, dest_path, git_path)
        #in the future, consider that displaying the modify status(M-modify A-add D-delete)
        back_up_str = self.__git_opt.convert_file_list_to_str(\
            self.__git_opt.generate_git_status_file_list(git_path, True))
        if not back_up_str:
            logging.warn("there is no change!!")
            quit()
        #get backup dir
        backup_to_path = self.get_backup_dir_with_timestamp_under_rootdir( \
            self.__src_root_path, self.__args_line[1])
        logging.info("backup to: %s", backup_to_path)
        #write backup list to file
        self.write_backuplist_to_file(backup_to_path, back_up_str)
        self.__git_opt.generator_git_patch_with_untracked(backup_path=backup_to_path, \
            backup_name=self.__args_line[1], git_path=git_path)
        file_list = self.__git_opt.generate_git_status_file_list(git_path)
        #logging.info("file_list: %s" file_list)
        # if the file status get from git is D ,we should remove it from file_list
        # if many file in same dir, filter them and copy dir
        self.cp_file_list_to_back_dir(file_list, backup_to_path, git_path)
        #generator commit format
        self.__git_opt.generator_git_commit_files(backup_path=backup_to_path, \
            backup_name=self.__args_line[1], git_path=git_path)
        self.clean_useless_files(backup_to_path)
