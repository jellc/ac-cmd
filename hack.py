# Use oj g/i
# Require ./generate
cmd = 'python ./generate'

import os
import subprocess
from colors import pycolor
from logging import getLogger
import multiprocessing
import tester

logger = getLogger(__name__)


def main(args):
    if len(args) == 0:
        exit(1)

    pool = multiprocessing.Pool(processes=2)
    pool.map(tester.build, args)

    if len(args) == 1:  # Assert Debug
        n = 0
        tmp = '.tmp'

        while True:
            n += 1
            subprocess.call(cmd, stdout=open(tmp, 'w'))

            if subprocess.call(args[0], stdin=open(tmp, 'r'), stdout=subprocess.DEVNULL):
                logger.critical(' RE on {} th attempt!'.format(n))
                subprocess.call(['cat', tmp])
                break

            if n == 100:
                logger.info(pycolor.GREEN + ' No RE detected!')
                break

        os.remove(tmp)

    else:
        if subprocess.call(["oj", "g/i", "-c", args[1], "--hack", args[0], cmd], shell=True):
            exit(1)
        logger.critical(pycolor.BRIGHT_RED + " " + args[0] + " is hacked!")
