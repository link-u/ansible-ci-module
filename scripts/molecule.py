#!/usr/bin/python3
if __name__ == "__main__":
    import os
    import subprocess
    import sys
    import glob


    ## python script path and repo dir
    script_path   = os.path.abspath(__file__)
    repo_root_dir = os.path.abspath(os.path.join(os.path.dirname(script_path), ".."))


    ## Execute dir
    __molecule_yml_files = [
        p for p in glob.glob(os.path.join(repo_root_dir, "..", "molecule", "*", "molecule.yml"))
        if os.path.isfile(p)]
    if len(__molecule_yml_files) >= 1:
        execute_dir = os.path.abspath(os.path.join(repo_root_dir, ".."))
    else:
        execute_dir = repo_root_dir


    ## Verify tests dir
    __tests_py_files = [
        p for p in glob.glob(os.path.join(repo_root_dir, "..", "molecule", "common", "tests", "test_*.py"))
        if os.path.isfile(p)]
    if len(__tests_py_files) >= 1:
        tests_dir = os.path.abspath(os.path.join(repo_root_dir, "..", "molecule", "common", "tests"))
    else:
        tests_dir = os.path.join(repo_root_dir, "molecule", "common", "tests")


    ## group_vars
    __group_vars_dir = os.path.join(repo_root_dir, "..", "molecule", "common", "group_vars")
    if os.path.exists(__group_vars_dir) and os.path.isdir(__group_vars_dir):
        group_vars_dir = os.path.abspath(__group_vars_dir)
    else:
        group_vars_dir = os.path.join(repo_root_dir, "molecule", "common", "group_vars")


    ## Add env
    env = os.environ
    env["CREATE_YML"]    = os.path.join(repo_root_dir, "molecule", "common", "playbooks", "create.yml")
    env["DESTROY_YML"]   = os.path.join(repo_root_dir, "molecule", "common", "playbooks", "destroy.yml")
    env["CONVERGE_YML"]  = os.path.join(repo_root_dir, "molecule", "common", "playbooks", "converge.yml")
    env["HOST_VARS"]     = os.path.join(repo_root_dir, "molecule", "common", "cache", "host_vars")
    env["GROUP_VARS"]    = group_vars_dir
    env["TESTINFRA_DIR"] = tests_dir
    env["ROLE_DIR"]      = os.path.abspath(os.path.join(repo_root_dir, ".."))


    ## Specify base.yml for molecule
    base_yml_path = os.path.join(repo_root_dir, "molecule", "common", "base.yml")
    args = sys.argv
    args[0] = "molecule"
    if (not "--base-config" in args) and (not "-c" in args):
        args.insert(1, "--base-config")
        args.insert(2, base_yml_path)


    ## Execute molecule
    proc = subprocess.run(args, cwd = execute_dir, env = env)
    sys.exit(proc.returncode)
