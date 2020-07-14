#!/usr/bin/python3
import os
import subprocess
import sys
import glob


## python script path and dir
script_path = os.path.abspath(__file__)
script_dir  = os.path.dirname(script_path)


## Execute dir
if len(glob.glob(script_dir + "/../molecule/*/molecule.yml")) >= 1:
    execute_dir = os.path.abspath(script_dir + "/..")
else:
    execute_dir = script_dir


## Verify tests dir
__tests_dir = script_dir + "/../molecule/common/tests"
if os.path.exists(__tests_dir) and os.path.isdir(__tests_dir):
    tests_dir = os.path.abspath(__tests_dir)
else:
    tests_dir = script_dir + "/molecule/common/tests"


## Add env
env = os.environ
env["CREATE_YML"]    = script_dir + "/molecule/common/playbooks/create.yml"
env["DESTROY_YML"]   = script_dir + "/molecule/common/playbooks/destroy.yml"
env["CONVERGE_YML"]  = script_dir + "/molecule/common/playbooks/converge.yml"
env["TESTINFRA_DIR"] = tests_dir
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
