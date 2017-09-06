#!/usr/bin/python
#coding:utf-8

import os
import sys
import inspect
import logging

class Git_operator:
    __git_status_short_types_add_forbidden = False
    #you can git diff --help then look up --diff-filter
    __git_status_short_type = ['M', 'A', 'D', '??', 'R', 'T', 'U', 'X']
    __git_status_short_raw_data = str()
    __git_status_short_raw_fmt_data = {}
    __git_status_short_raw_fmt_data_init_key = str("init")
    __git_status_short_raw_fmt_data_untrack_key = str("??")
    #__git_status_file_list = []
    #__git_status_file_list_with_no_del = []
    __git_status_file_list_with_no_del_flag = 'D'
    def __init__(self):
        self.__git_status_short_raw_fmt_data[\
            self.__git_status_short_raw_fmt_data_init_key] = False

    def git_status_short_types_add(self, mtypes):
        if self.__git_status_short_types_add_forbidden is True:
            logging.info("you should add types first!!")
        self.__git_status_short_type.append(mtypes)
        return self.__git_status_short_type

    def __init_git_status_short_type_dict(self, dict_key_list):
        if not isinstance(dict_key_list, list):
            logging.info("you key list is not a type of list!!")
            return False
        if self.__git_status_short_types_add_forbidden is True:
            logging.info("dict aready inited!!")
            return False
        self.__git_status_short_types_add_forbidden = True
        for key_list in dict_key_list:
            self.__git_status_short_raw_fmt_data[key_list] = []
        #self.__git_status_short_raw_fmt_data = {}.fromkeys((dict_key_list), [-1]), all the key share the same value
        return self.__git_status_short_raw_fmt_data

    def __do_git_status_short_type_dict_init_stat(self):
        if not self.__git_status_short_types_add_forbidden:
            self.__init_git_status_short_type_dict(dict_key_list=self.__git_status_short_type)
        return self.__git_status_short_types_add_forbidden

    def __do_save_file(self, fname, content, fmode=os.O_RDWR|os.O_CREAT):
        if not fname:
            logging.info("fname is null!!")
        try:
            save_fd = os.open(fname, fmode)
        except OSError, excep:
            print "%s: error %s open failed" % \
                (inspect.stack()[0][2], excep.strerror)
            return False
        os.write(save_fd, content)
        os.close(save_fd)
        return True

    def execute_git_add(self, flist, git_path=os.getcwd()):
        if isinstance(flist, list) and flist != []:
            for mflist in flist:
                self.execute_git_cmd(git_path, "git {0} {1}".format("add", mflist))
        else:
            logging.info("flist is null")

    def execute_git_reset_soft(self, flist, git_path=os.getcwd()):
        if isinstance(flist, list) and flist != []:
            for mflist in flist:
                self.execute_git_cmd(git_path, "git {0} {1}".format("reset", mflist))
        else:
            logging.info("flist is null")

    def execute_git_cmd(self, cmd_path, git_cmd="git status -s"):
        output = os.popen("cd {0} && {1} && cd {2}".format(
            cmd_path,
            git_cmd,
            cmd_path))
        #print(output.__class__)
        #print(output.read())
        return output.read()

    def get_git_status_short_raw_data(self, git_path=os.getcwd()):
        self.__git_status_short_raw_data = self.execute_git_cmd(git_path, \
            "git status {0}".format("-s -uall"))
        return self.__git_status_short_raw_data

    def __get_git_status_short_raw_fmt_data(self, git_path=os.getcwd()):
        self.__do_git_status_short_type_dict_init_stat()
        m_raw_data = self.get_git_status_short_raw_data(git_path)
        m_raw_data = m_raw_data.split('\n')
        m_raw_data_index = 0
        for m_raw in m_raw_data:
            m_raw_data[m_raw_data_index] = m_raw.strip()
            if not m_raw_data[m_raw_data_index]:
                continue
            #print m_raw_data[m_raw_data_index]
            m_raw_data_key = m_raw_data[m_raw_data_index].split()[0]
            m_raw_data_keyvalue = m_raw_data[m_raw_data_index].split()[1]
            ##pay attention !! this code can't execut twice or more
            self.__git_status_short_raw_fmt_data[m_raw_data_key].append(m_raw_data_keyvalue)
            m_raw_data_index += 1

        #print("%s: file list: %s" % \
        #    (inspect.stack()[0][2], self.__git_status_short_raw_fmt_data.items()))
        self.__git_status_short_raw_fmt_data\
            [self.__git_status_short_raw_fmt_data_init_key] = True
        return self.__git_status_short_raw_fmt_data

    def get_git_status_short_rawfmtdata_once(self, git_path=os.getcwd()):
        if not self.__git_status_short_raw_fmt_data[self.__git_status_short_raw_fmt_data_init_key]:
            return self.__get_git_status_short_raw_fmt_data(git_path)
        return self.__git_status_short_raw_fmt_data

    def filter_git_status_short_raw_fmt_data(self, git_path=os.getcwd()):
        dict_data_base = self.get_git_status_short_rawfmtdata_once(git_path)
        mfilter_Dict = {}
        for mkey_list in self.__git_status_short_type:
            if dict_data_base.has_key(mkey_list):
                mfilter_Dict[mkey_list] = dict_data_base.get(mkey_list)
        return mfilter_Dict

    def filter_git_status_short_rawfmtdata_no_init(self, git_path=os.getcwd()):
        dict_data_base = self.get_git_status_short_rawfmtdata_once(git_path)
        mfilter_Dict = {}
        for mkey_list in dict_data_base:
            if mkey_list != self.__git_status_short_raw_fmt_data_init_key:
                mfilter_Dict[mkey_list] = dict_data_base.get(mkey_list)
        return mfilter_Dict

    def generate_git_status_file_list(self, git_path=os.getcwd(), with_del_status = False):
        dict_data_base = self.get_git_status_short_rawfmtdata_once(git_path)
        #print dict_data_base
        mgit_status_file_list = []
        mgit_status_file_list_with_no_del = []
        for mkey_list in self.__git_status_short_type:
            #print inspect.stack()[0][2], mkey_list, dict_data_base.get(mkey_list)
            if dict_data_base.has_key(mkey_list):
                mgit_status_file_list.extend(\
                    dict_data_base.get(mkey_list))
                if mkey_list != self.__git_status_file_list_with_no_del_flag:
                    mgit_status_file_list_with_no_del.extend(\
                        dict_data_base.get(mkey_list))
        if with_del_status is True:
            return mgit_status_file_list
        else:
            return mgit_status_file_list_with_no_del

    def convert_file_list_to_str(self, mfile_list=[]):
        if not isinstance(mfile_list, list) or (not mfile_list):
            print("%s: list=para is empty or not list: %s" % \
                (inspect.stack()[0][2], mfile_list))
        converted_str = ""
        for list_item in mfile_list:
            list_item += "\n"
            converted_str += list_item
        return converted_str

    def exec_shell_cmd_get_status_with_nostat(self, git_path=os.getcwd()):
        output = self.execute_git_cmd(git_path, \
            "git status {0} | {1}".format("-s -uall", "awk '{print $2}'"))
        return output

    def generator_git_patch_no_untracked(self,\
        backup_path, backup_name, git_path=os.getcwd()):
        if backup_name != "":
            output = self.execute_git_cmd(git_path, "git {0} {1} {2}".format( \
                "diff -p --raw --stat 1>", \
                os.path.join(backup_path, backup_name + ".patch"), "2>&1"))
        else:
            output = self.execute_git_cmd(git_path, "git {0} {1}".format( \
                "diff", "-p --raw --stat"))
        return output

    def generator_git_commit_files(self,\
        backup_path, backup_name="commit", git_path=os.getcwd()):
        commit_dict = self.filter_git_status_short_raw_fmt_data(git_path)

        commit_write = str()
        for mcommit_list in self.get_file_list_by_status_flag(\
            self.__git_status_file_list_with_no_del_flag, git_path):
            join_str = "git rm " + mcommit_list + "\n"
            commit_write += join_str
        for mcommit_list in self.generate_git_status_file_list(git_path):
            join_str = "git add " + mcommit_list + "\n"
            commit_write += join_str
        commit_write = commit_write + "\ngit commit -sm \"\n" + backup_name + "\n\"\n"
        commit_write = commit_write + \
            "git branch |grep \\*|awk '{print $2}'|xargs -I {} git push origin {}:refs/for/{}\n"
        self.__do_save_file(os.path.join(backup_path, backup_name+".commit"), commit_write)
        #os.chmod(os.path.join(backup_path, backup_name+".commit"), 0777)

    def get_file_list_by_status_flag(self, status_flags=[], git_path=os.getcwd()):
        if not status_flags:
            return self.generate_git_status_file_list(True, git_path)
        mfilter_Dict = self.filter_git_status_short_raw_fmt_data(git_path)
        mfilter_flist = []
        for mkey_list in self.__git_status_short_type:
            if mfilter_Dict.has_key(mkey_list):
                if mkey_list in status_flags:
                    mfilter_flist.extend(\
                        mfilter_Dict.get(mkey_list))
        return mfilter_flist

    def generator_git_patch_with_untracked(self, \
        backup_path, backup_name="patch", git_path=os.getcwd()):
        self.execute_git_add(self.get_file_list_by_status_flag(\
            self.__git_status_short_raw_fmt_data_untrack_key, git_path), git_path)
        output_untracked = self.execute_git_cmd(\
            git_path, "git {0} ".format("diff --cached"))
        output_tracked = self.generator_git_patch_no_untracked(\
            backup_path, "", git_path)
        self.execute_git_reset_soft(self.get_file_list_by_status_flag(\
            self.__git_status_short_raw_fmt_data_untrack_key, git_path), git_path)
        self.__do_save_file(os.path.join(backup_path, backup_name + ".patch"), \
            output_tracked + output_untracked)
        return output_tracked + output_untracked

if __name__ == "__main__":
    g_gitopt_test = Git_operator()
    #print("%s: file list: %s" % \
    #        (inspect.stack()[0][2], g_gitopt_test.filter_git_status_short_raw_fmt_data().items()))
    print(g_gitopt_test.filter_git_status_short_raw_fmt_data())
    print ">>>>>>>>>>>>>>>>>>>>>>>>>>"
    print(g_gitopt_test.generate_git_status_file_list())
    print ">>>>>>>>>>>>>>>>>>>>>>>>>>"
    print(g_gitopt_test.generate_git_status_file_list(with_del_status=True))

    print ">>>>>>>>>>>>>>>>>>>>>>>>>>"
    print(g_gitopt_test.get_file_list_by_status_flag(['M', 'A']))

    print ">>>>>>>>>>>>>>>>>>>>>>>>>>"
    print(g_gitopt_test.get_file_list_by_status_flag())

    print ">>>>>>>>>>>>>>>>>>>>>>>>>>"
    print(g_gitopt_test.generator_git_patch_with_untracked("../../test-2017-06-19-16-48-12"))
    
    #g_gitopt_test.get_git_status_short_raw_fmt_data()