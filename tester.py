import os

options = [
    "-D_GLIBCXX_DEBUG",
    "-D_LOCAL",
    "-D_buffer_check",
    "-std=c++17",
    "-O2",
    "-march=native",
    "-Wall",
    "-Wl,-stack,0x10000000",
    "-fsanitize-undefined-trap-on-error",
    "-fsanitize=undefined",
    "-fno-sanitize-recover",
    "-I",
    os.path.expanduser('~/Library'),
    "-I",
    os.path.expanduser('~/ac-library'),
]

exts = ['cpp', 'cc', 'c']

import sys
import subprocess
import glob
import logging
from colors import pycolor

logger = logging.getLogger(__name__)


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
            srcs.extend(glob.glob('*.' + e))

    if not srcs:
        logger.error(pycolor.BRIGHT_RED + " No source code found.")

    first = True
    exit_stat = 0

    for f in srcs:
        if first:
            first = False
        else:
            print(pycolor.BLUE + "-" * 40 + pycolor.END)
        logger.info(" Compiling " + f + " ...")
        ff = os.path.splitext(f)[0]
        ret = subprocess.call(["g++", f, "-o", ff] + options)
        if ret:
            logger.error(pycolor.BRIGHT_RED + " Compilation error.")
            exit_stat = 1
            continue
        cmd[3] = './' + ff
        logger.info(" Testing " + f + " ...")
        ret = subprocess.call(cmd)

    sys.exit(exit_stat)
