import sys
import os
import subprocess
import glob
import time
import toml
import json
import logging

logger = logging.getLogger(__name__)

from colors import pycolor

generator = 'generate'


def main(args):
    tmpl = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'template')

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
        here = os.path.join(dire, d.lower())
        os.rename(os.path.join(dire, d), here)
        try:
            os.rename(os.path.join(here, 'main.cpp'), os.path.join(here, d.lower() + '.cpp'))
        except Exception:
            pass

    for d in os.listdir(dire):
        here = os.path.join(dire, d)
        subprocess.call(["code", d + ".cpp"], cwd=here)
        url = contest_url + '/tasks/' + contest_id + '_' + d

        with open(os.path.join(here, generator), "w") as genf:
            subprocess.call(["oj-template", "-t", tmpl, url], cwd=here, stdout=genf, stderr=subprocess.DEVNULL)

        subprocess.call(["chmod", "u+x", generator], cwd=here)

    info = {"problem": {"contest": {"contest_id": contest_id}}}
    with open(os.path.join(dire, 'metadata.json'), 'w') as f:
        json.dump(info, f)
