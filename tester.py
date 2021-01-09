options = [
    "-I/home/euler/Library/",
    "-I/home/euler/ac-library/",
    "-D_GLIBCXX_DEBUG",
    "-D_LOCAL",
    "-D_buffer_check",
    "-std=c++17",
    "-O2",
    "-Wall",
    "-Wno-comment",
    "-Wno-unknown-pragmas",
    "-Wno-unused-function",
    "-Wl,--stack,0x10000000",
    "-fsanitize-undefined-trap-on-error",
    "-fsanitize=undefined",
    "-fno-sanitize-recover",
]

import sys
import os
import subprocess
import glob
from colors import pycolor
from pathlib import Path
from logging import getLogger, basicConfig, INFO
logger = getLogger(__name__)


def main(args):
    cmd = ["atcoder-tools", "test", "--exec", "", "-t", "2"]
    srcs = []

    for arg in args:
        if Path.is_file(Path(arg)):
            if os.path.splitext(arg)[1] == '.cpp':
                srcs.append(arg)
        else:
            cmd.append(arg)

    if not srcs:
        srcs = glob.glob('*.cpp')

    if not srcs:
        logger.error(pycolor.BRIGHT_RED + " No source code found.")

    first = True
    exit_stat = 0

    for f in srcs:
        if first:
            first = False
        else:
            print(pycolor.BLUE + "-" * 50 + pycolor.END)
        logger.info(" Compiling " + f + "...")
        ff = os.path.splitext(f)[0]
        ret = subprocess.call(["g++", f, "-o", ff] + options)
        if ret:
            logger.error(pycolor.BRIGHT_RED + " Compilation error.")
            exit_stat = 1
            continue
        cmd[3] = './' + ff
        logger.info(" Testing " + f + "...")
        ret = subprocess.call(cmd)

    sys.exit(exit_stat)
