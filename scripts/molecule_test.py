#!/usr/bin/python3
if __name__ == "__main__":
    import os
    import subprocess
    import sys
    import shlex

    ## python script path and repo dir
    script_dir  = os.path.dirname(os.path.abspath(__file__))
    molecule_py = os.path.abspath(os.path.join(script_dir, "molecule.py"))

    ## 環境変数の取得
    env = os.environ
    molecule_scenario = env.get("MOLECULE_SCENARIO")

    ## molecule.py を実行する
    if molecule_scenario == None:
        args = [molecule_py, "test", "--all"]
    else:
        args = [molecule_py, "test", "-s", molecule_scenario]

    print(shlex.join(args))
    proc = subprocess.run(args, env = env)
    sys.exit(proc.returncode)
