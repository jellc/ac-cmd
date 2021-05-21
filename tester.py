exts = ['.cpp', '.cc', '.c']

import os
import sys
import subprocess
import glob
import logging
from colors import pycolor

logger = logging.getLogger(__name__)


def build(src):
    logger.info(' Compiling {} ...'.format(src))
    if subprocess.call(["bash", "--login", "-c", "make " + src], stdout=subprocess.DEVNULL, shell=True):
        logger.error(' Compilation error: {}', src)
        exit(1)


def main(args):
    cmd = ["atcoder-tools", "test", "--exec", "", "-t", "2"]
    srcs = []

    for arg in args:
        if os.path.isfile(arg):
            if os.path.splitext(arg)[1] in exts:
                srcs.append(arg)
        else:
            cmd.append(arg)

    if not srcs:
        for e in exts:
            srcs.extend(glob.glob('*' + e))

    if not srcs:
        logger.error(pycolor.BRIGHT_RED + " No source code found.")

    first = True
    exit_stat = 0

    for f in srcs:
        if first:
            first = False
        else:
            print(pycolor.BLUE + "-" * 30 + pycolor.END)
        ff = os.path.splitext(f)[0]
        build(ff)
        logger.info(" Testing {} ...".format(ff))
        ret = subprocess.call(["atcoder-tools", "test", "--exec", ff, "-t", "2"])
