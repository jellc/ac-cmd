import subprocess
from colors import pycolor
import sys
import os
from logging import getLogger, basicConfig, INFO
logger = getLogger(__name__)

import gen
import tester
import colors


def main(args):
    if len(args) < 2:
        logger.error(pycolor.BRIGHT_RED + " enter two solutions.")
        exit(1)
    src1 = args[0]
    src2 = args[1]
    tmp1 = './tmp1.exe'
    tmp2 = './tmp2.exe'
    subprocess.call(["g++", src1, "-o", tmp1] + tester.options)
    subprocess.call(["g++", src2, "-o", tmp2] + tester.options)
    gencmd = 'python3.8 ' + gen.generator
    subprocess.call(["oj", "g/i", "-c", tmp2, "--hack", tmp1, gencmd])
    logger.critical(pycolor.RED + " " + src1 + " hacked by " + src2 + " !")
    os.remove(tmp1)
    os.remove(tmp2)
