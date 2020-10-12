import sys
import os
import subprocess
import glob
import time
import toml
from logging import getLogger, basicConfig, INFO
logger = getLogger(__name__)

from colors import pycolor
generator = 'gen.py'


def main(args):
    if not args:
        logger.error(pycolor.BRIGHT_RED + " no contest id specified.")
        sys.exit(1)
    contest_id = args[0]
    contest_url = "https://atcoder.jp/contests/" + contest_id

    subprocess.call(["msedge", contest_url + "/standings"])
    subprocess.call(["msedge", contest_url + "/tasks_print"])

    time.sleep(3)
    cfg = toml.load(os.path.expanduser('~/.atcodertools.toml'))
    workspace = os.path.expanduser(cfg['codestyle']['workspace_dir'])
    subprocess.call(["atcoder-tools", "gen"] + args)

    dire = os.path.join(workspace, contest_id)

    for d in os.listdir(dire):
        here = os.path.join(dire, d)
        try:
            os.rename(os.path.join(here, 'main.cpp'), os.path.join(here, d.lower() + '.cpp'))
        except Exception:
            pass
        os.rename(here, here.lower())

    for d in os.listdir(dire):
        here = os.path.join(dire, d)
        with open(os.path.join(here, generator), "w") as genf:
            subprocess.call(["oj-template", "-t", "generate.py", os.path.join(contest_url, 'tasks', contest_id + '_' + d)], cwd=here, stdout=genf)
