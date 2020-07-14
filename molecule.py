#!/usr/bin/python3
import os
import subprocess
import sys


## python script path and dir
script_path   = os.path.abspath(__file__)
script_dir    = os.path.dirname(script_path)


## Execute dir
if os.path.exists(script_dir + "/../molecule"):
    execute_dir = os.path.abspath(script_dir + "/..")
else:
    execute_dir = script_dir


## Add env
env = os.environ
env["CREATE_YML"]    = script_dir + "/molecule/common/playbooks/create.yml"
env["DESTROY_YML"]   = script_dir + "/molecule/common/playbooks/destroy.yml"
env["CONVERGE_YML"]  = script_dir + "/molecule/common/playbooks/converge.yml"
env["TESTINFRA_DIR"] = script_dir + "/molecule/common/tests"
env["ROLE_DIR"]      = os.path.abspath(script_dir + "/..")


## Specify base.yml for molecule
base_yml_path = script_dir + "/molecule/common/base.yml"
args = sys.argv
args[0] = "molecule"
if (not "--base-config" in args) and (not "-c" in args):
    args.insert(1, "--base-config")
    args.insert(2, base_yml_path)


## Execute molecule
subprocess.run(args, cwd = execute_dir, env = env)
