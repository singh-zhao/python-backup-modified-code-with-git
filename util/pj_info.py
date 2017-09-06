#!/usr/bin/python
#coding:utf-8

import os
import re
import sys
import inspect
import logging
from re import findall


class Pj_path_info:
    __root_dir = str()
    __git_dir = str()
    __cmd_path = str()
    __cmd_path_deep = int()
    __search_path_deep = int()
    __the_info_to_judge_root_dir = {}
    def __init__(self, search_path_deep_limit=4, \
        key_dir="kernel", key_file="Makefile", git_dir=".git"):
        self.__cmd_path = os.getcwd()
        self.__cmd_path_deep = len(findall("/", self.__cmd_path))
        self.__search_path_deep = search_path_deep_limit
        self.__the_info_to_judge_root_dir["key_dir"] = key_dir
        self.__the_info_to_judge_root_dir["key_file"] = key_file
        self.__the_info_to_judge_root_dir["git_dir"] = git_dir
        logging.info("cmd path:%s, search deep:%s",\
            self.__cmd_path, str(self.__search_path_deep))

    def __is_empty_str__(self, variable):
        return variable == ''

    def __is_match__(self, m_path):
        if os.path.exists(os.path.join(os.path.dirname(m_path), \
                self.__the_info_to_judge_root_dir["key_file"])):
            if os.path.isdir(os.path.join(\
                m_path, self.__the_info_to_judge_root_dir["git_dir"])):
                self.__git_dir = m_path
                self.__root_dir = os.path.dirname(m_path)
            elif  os.path.isdir(os.path.join( \
                m_path, "../" + self.__the_info_to_judge_root_dir["git_dir"])):
                self.__git_dir = os.path.dirname(m_path)
                self.__root_dir = os.path.dirname(m_path)
            else:
                return False
        else:
            return False
        return True

    def __find_root_dir_condition(self, m_path):
        m_path = m_path + "/"
        #logging.info("m_path:" + m_path)
        if not os.path.isdir(m_path):
            return False
        ret_l = findall("(/.*?/" + self.__the_info_to_judge_root_dir["key_dir"] + ".*?)/", m_path)
        #ret_l = findall("(/.*?/" + self.__the_info_to_judge_root_dir["key_dir"] + ")/", m_path)
        if not ret_l:
            ret = False
        else:
            ret = ret_l[0]

        #logging.debug(ret)

        if not ret:
            l_find_root = False
            if (len(findall("/", m_path)) - self.__cmd_path_deep) \
                >= self.__search_path_deep:
                #logging.info("The path is too deep")
                return False
            for t_dir in os.listdir(m_path):
                #logging.info(t_dir, self.__the_info_to_judge_root_dir["key_dir"], m_path)
                if os.path.isdir(m_path + t_dir):
                    l_find_root = self.__find_root_dir_condition(m_path + t_dir)
                    if l_find_root:
                        break
            return l_find_root
        elif self.__is_match__(ret) != False:
            return True
        else:
            '''
            logging.info("%s not exists" %
                (ret + self.__the_info_to_judge_root_dir["git_dir"]))
            '''
            return False

    def __get_root_path(self):
        if os.path.isdir(self.__cmd_path):
            return self.__find_root_dir_condition(self.__cmd_path)
        else:
            logging.error(self.get_cmd_dir() + "not exists!!")
            return False

    def get_cmd_dir(self):
        if self.__is_empty_str__(self.__cmd_path) is True:
            logging.error("__cmd_path is NULL")
            quit()
        return self.__cmd_path

    def get_root_dir(self):
        if self.__is_empty_str__(self.__root_dir) is True:
            if False == self.__get_root_path():
                logging.error("root_dir is NULL")
                quit()
            else:
                if not os.path.isdir(self.__root_dir):
                    logging.error("root_dir:%s not exist",\
                        self.__root_dir)
                    quit()
        return self.__root_dir

    def get_git_dir(self):
        if self.__is_empty_str__(self.__git_dir) is True:
            logging.error("kern_dir is NULL")
            return False
        return self.__git_dir

    def print_pj_info(self):
        logging.warn("\n\tcmd_path:\t%s\n" \
            "\troot_path:\t%s\n" \
            "\tgit_path:\t%s", \
            self.get_cmd_dir(), \
            self.get_root_dir(), \
            self.get_git_dir())

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, \
        format='%(levelname)s:%(filename)s[line:%(lineno)d,func:%(funcName)s]->%(message)s')
    logging.warn("main info")
    sample_pj = Pj_path_info(key_dir="kernel", key_file="Makefile")
    sample_pj.print_pj_info()
    logging.info("%s %s " "%s", "ad", "fdsf", sample_pj.get_cmd_dir())
