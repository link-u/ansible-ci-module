#!/usr/bin/python3
import os
import subprocess
import glob

## python script path and repo dir
script_path   = os.path.abspath(__file__)
repo_root_dir = os.path.abspath(os.path.dirname(script_path) + "/..")

def matrix_tox_envs():
    ## Execute dir
    if os.path.isfile(repo_root_dir + "/../tox.ini"):
        execute_dir = os.path.abspath(repo_root_dir + "/..")
    else:
        execute_dir = repo_root_dir

    ## Echo TOX_ENV
    tox_args = ["tox", "-l", "-c", "tox.ini"]
    proc = subprocess.Popen(
        tox_args,
        cwd = execute_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL)
    tox_env_list = proc.communicate()[0].decode()[:-1].split("\n")
    return tox_env_list


def matrix_scenarios():
    ## シナリオのリスト (ansible role ディレクトリで定義されているもの)
    scenarios_defined_by_role = [
        os.path.basename(os.path.dirname(p)) for p
        in glob.glob(repo_root_dir + "/../molecule/*/molecule.yml")
        if os.path.isfile(p)
    ]

    ## シナリオのリスト (ansible-ci-module 内でデフォルトで定義してあるもの)
    scenarios_in_ansible_ci_modules = [
        os.path.basename(os.path.dirname(p)) for p
        in glob.glob(repo_root_dir + "/molecule/*/molecule.yml")
        if os.path.isfile(p)
    ]

    if len(scenarios_defined_by_role) >= 1:
        return scenarios_defined_by_role
    else:
        return scenarios_in_ansible_ci_modules


if __name__ == "__main__":
    print("{" +
        "\"tox_env\": [\"" + "\", \"".join(matrix_tox_envs()) + "\"], " +
        "\"scenario\": [\"" + "\", \"".join(matrix_scenarios()) + "\"]" +
        "}"
    )
