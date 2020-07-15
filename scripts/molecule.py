#!/usr/bin/python3
import os
import subprocess
import sys
import glob


## python script path and dir
script_path   = os.path.abspath(__file__)
scripts_dir   = os.path.dirname(script_path)
repo_root_dir = os.path.abspath(scripts_dir + "/..")


## Execute dir
__molecule_yml_files = [
    p for p in glob.glob(repo_root_dir + "/../molecule/*/molecule.yml")
    if os.path.isfile(p)]
if len(__molecule_yml_files) >= 1:
    execute_dir = os.path.abspath(repo_root_dir + "/..")
else:
    execute_dir = repo_root_dir


## Verify tests dir
__tests_py_files = [
    p for p in glob.glob(repo_root_dir + "/../molecule/common/tests/test_*.py")
    if os.path.isfile(p)]
if len(__tests_py_files) >= 1:
    tests_dir = os.path.abspath(repo_root_dir + "/../molecule/common/tests")
else:
    tests_dir = repo_root_dir + "/molecule/common/tests"

## Add env
env = os.environ
env["CREATE_YML"]    = repo_root_dir + "/molecule/common/playbooks/create.yml"
env["DESTROY_YML"]   = repo_root_dir + "/molecule/common/playbooks/destroy.yml"
env["CONVERGE_YML"]  = repo_root_dir + "/molecule/common/playbooks/converge.yml"
env["TESTINFRA_DIR"] = tests_dir
env["ROLE_DIR"]      = os.path.abspath(repo_root_dir + "/..")


## Specify base.yml for molecule
base_yml_path = repo_root_dir + "/molecule/common/base.yml"
args = sys.argv
args[0] = "molecule"
if (not "--base-config" in args) and (not "-c" in args):
    args.insert(1, "--base-config")
    args.insert(2, base_yml_path)


## Execute molecule
subprocess.run(args, cwd = execute_dir, env = env)
