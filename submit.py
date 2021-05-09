import sys
import os
import subprocess
import glob
import json
import multiprocessing
from logging import getLogger

logger = getLogger(__name__)

from colors import pycolor


def bundle_and_submit(src, prob, dire=None):
    bdl = os.path.splitext(src)[0] + ".bdl"
    if subprocess.call(['python', 'my-bundle', os.path.abspath(src), os.path.abspath(bdl)], cwd=os.path.expanduser('~')):
        logger.error(" " + pycolor.BRIGHT_RED + src + ": bundle failed.")
        sys.exit(1)
    logger.info(" Submitting to " + pycolor.PURPLE + prob.upper() + pycolor.END + " ...")
    sub_args = ["atcoder-tools", "submit", "-u", "-f", "--code", bdl]
    subprocess.call(sub_args, cwd=dire)


def confirm(lst):
    logger.critical(" Are you sure to submit " + pycolor.PURPLE + ', '.join(lst) + pycolor.END + " ? (y/n)")
    if input() != "y":
        logger.info(pycolor.PURPLE + " Canceled.")
        sys.exit(1)


def each(prob):
    os.chdir(prob)
    src = glob.glob('*.cpp')
    if not src:
        logger.error(" " + pycolor.RED + prob.upper() + ": No source file found." + pycolor.END)
        exit(1)
    elif len(src) > 1:
        logger.error(" " + pycolor.RED + prob.upper() + ": Multiple sources exist." + pycolor.END)
        exit(1)
    else:
        prob = os.path.basename(os.getcwd())
        bundle_and_submit(src[0], prob, os.getcwd())
    os.chdir("..")


def main(argv):
    src = ""
    for e in argv:
        if e.endswith(".cpp"):
            src = e
            break
    if src:
        prob = os.path.basename(os.getcwd())
        confirm(prob.upper())
        bundle_and_submit(src, prob)

    elif argv:
        for i in range(len(argv)):
            argv[i] = argv[i].upper()
        confirm(argv)
        for i in range(len(argv)):
            argv[i] = argv[i].lower()

        pool = multiprocessing.Pool(processes=6)
        pool.map(each, argv)

    else:
        srcs = glob.glob('*.cpp')
        if not srcs:
            logger.error(pycolor.BRIGHT_RED + " No source file found." + pycolor.END)
            sys.exit(1)
        elif len(srcs) > 1:
            logger.error(pycolor.BRIGHT_RED + " Multiple sources exist." + pycolor.END)
            sys.exit(1)
        else:
            src = srcs[0]
            prob = os.path.basename(os.getcwd())
            confirm(prob.upper())
            bundle_and_submit(src, prob)

    with open('metadata.json') as f:
        url = 'https://atcoder.jp/contests/' + json.load(f)['problem']['contest']['contest_id'] + '/submissions'
        subprocess.call(['msedge', url])
