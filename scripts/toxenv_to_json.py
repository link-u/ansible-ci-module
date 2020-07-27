#!/usr/bin/python3
if __name__ == "__main__":
    import os
    import subprocess

    ## python script path and repo dir
    script_path   = os.path.abspath(__file__)
    repo_root_dir = os.path.abspath(os.path.dirname(script_path) + "/..")

    ## Execute dir
    execute_dir = repo_root_dir

    ## Echo TOX_ENV
    tox_args = ["tox", "-l", "-c", "tox.ini"]
    proc = subprocess.Popen(
        tox_args,
        cwd = execute_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL)
    tox_env_list = proc.communicate()[0].decode()[:-1].split("\n")
    print("\"" + "\", \"".join(tox_env_list) + "\"")
