import argparse
import sys
import os
import subprocess
from logging import getLogger, basicConfig, INFO

logger = getLogger(__name__)

import gen
import tester
import submit
import hack
from colors import pycolor


def main(args):
    if args:
        cmd = args[0]
        args = args[1:]
        if cmd in ['test', 't']:
            tester.main(args)
        elif cmd in ['gen', 'g']:
            gen.main(args)
        elif cmd in ['submit', 's']:
            submit.main(args)
        elif cmd in ['hack', 'h']:
            hack.main(args)
        else:
            subprocess.call("atcoder-tools" + cmd + args)
    else:
        logger.error(pycolor.BRIGHT_RED + " arg empty.")
