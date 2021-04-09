import subprocess
from colors import pycolor
import os
from logging import getLogger
logger = getLogger(__name__)

import gen
import tester

gencmd = 'python3.8 ' + gen.generator


def main(args):
    if len(args) == 0:
        exit(1)

    if len(args) == 1:
        logger.info(" Assert debugging...")
        src1 = args[0]
        exe1 = './exe1.exe'

        subprocess.call(["g++", src1, "-o", exe1] + tester.options)

        # TODO
        # Compare with itself
        # if subprocess.call(["oj", "g/i", "--width=2", "-c", exe1, "--hack", exe1, gencmd]):
        #     exit(1)

        logger.critical(pycolor.BRIGHT_RED + " " + src1 + " is hacked!")

        os.remove(exe1)

    else:
        src1 = args[0]
        src2 = args[1]
        exe1 = './exe1.exe'
        exe2 = './exe2.exe'

        logger.info(' Compiling {} ...'.format(src1))
        if subprocess.call(["g++", src1, "-o", exe1] + tester.options):
            logger.error(' Compilation error: {}', src1)
            exit(1)

        logger.info(' Compiling {} ...'.format(src2))
        if subprocess.call(["g++", src2, "-o", exe2] + tester.options):
            logger.error(' Compilation error: {}', src2)
            exit(1)

        if subprocess.call(["oj", "g/i", "--width=2", "-c", exe2, "--hack", exe1, gencmd]):
            exit(1)

        logger.critical(pycolor.BRIGHT_RED + " " + src1 + " hacked by " + src2 + " !")

        os.remove(exe1)
        os.remove(exe2)
