#!/usr/bin/python
#coding:utf-8
#get line number: inspect.stack()[0][2]

import sys
import os
import logging

sys.path.append(os.path.abspath(os.path.join(sys.path[0], "util")))

import git_opt
import file_operator
from git_opt import Git_operator
from pj_info import Pj_path_info
from file_operator import File_operator


def print_usage():
    """print usage msg"""
    l_usage = ["usage:\n", \
        "    " + G_SYS_ARGV[0] + "\t\"the name what do you want to name for your modify\""]
    l_usages = [G_SYS_ARGV[:], l_usage]
    l_usages[0][0] = "    " + l_usages[0][0]
    l_usages[0].insert(0, "your input:\n")
    l_usages[0].append("\n")
    for mlist in l_usages:
        for mtext in mlist:
            print mtext, #python 3.x print(mtext, end = '')


def process_args(args_line):
    ''' deal with input parameter '''
    if len(args_line) > 2 or len(args_line) <= 1:
        print_usage()
    else:
        g_pj_info = Pj_path_info(key_dir="kernel", key_file="Makefile")
        g_pj_info.print_pj_info()
        g_pj_fops = File_operator(args_line=args_line)
        g_pj_fops.back_up_files(g_pj_info.get_root_dir(), str(), \
            g_pj_info.get_git_dir(), g_pj_info.get_cmd_dir())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, \
        format='%(levelname)s:%(filename)s[line:%(lineno)d,func:%(funcName)s]$ %(message)s')
    G_SYS_ARGV = (sys.argv[:])
    logging.info("len:%s args:%s ", len(G_SYS_ARGV), G_SYS_ARGV)
    process_args(G_SYS_ARGV)
