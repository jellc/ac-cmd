import subprocess
from colors import pycolor
import sys
import os
from logging import getLogger, basicConfig, INFO
logger = getLogger(__name__)

import gen
import tester
import colors

gencmd = 'python3.8 ' + gen.generator


def main(args):
    if len(args) == 0:
        exit(1)

    if len(args) == 1:
        logger.info(" Assert debugging...")
        src1 = args[0]
        tmp1 = './tmp1.exe'

        subprocess.call(["g++", src1, "-o", tmp1] + tester.options)

        # TODO
        # if subprocess.call(["oj", "g/i", "--width=2", "-c", tmp1, "--hack", tmp1, gencmd]):
        #     exit(1)

        logger.critical(pycolor.BRIGHT_RED + " " + src1 + " is hacked!")

        os.remove(tmp1)

    else:
        src1 = args[0]
        src2 = args[1]
        tmp1 = './tmp1.exe'
        tmp2 = './tmp2.exe'

        subprocess.call(["g++", src1, "-o", tmp1] + tester.options)
        subprocess.call(["g++", src2, "-o", tmp2] + tester.options)

        if subprocess.call(["oj", "g/i", "--width=2", "-c", tmp2, "--hack", tmp1, gencmd]):
            exit(1)

        logger.critical(pycolor.BRIGHT_RED + " " + src1 + " hacked by " + src2 + " !")

        os.remove(tmp1)
        os.remove(tmp2)
