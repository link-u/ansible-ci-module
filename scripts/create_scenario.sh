#!/bin/bash

set -eu
set -o pipefail

## 引数チェック
if [ $# -le 0 ]; then
    echo "一つ以上のシナリオ名を引数に設定してください" >&2
    exit 1
fi

## シナリオ名の配列をコマンドライン引数から取得
SCENARIOS=( "${@}" )

## role ディレクトリパスの取得
SCRIPT_DIR="$(cd "$(dirname .)" && pwd)"
ROLE_DIR="$(cd "${SCRIPT_DIR}/../../" && pwd)"

## 各シンボリックリンク
cd "${ROLE_DIR}"
for SCENARIO_NAME in "${SCENARIOS[@]}"; do
    SCENARIO_DIR="molecule/${SCENARIO_NAME}"
    mkdir -p "${SCENARIO_DIR}/group_vars/all"
    ln -sf "../../../../defaults/main.yml" "${SCENARIO_DIR}/group_vars/all/00-defaults.yml"

    if [ ! -f "${SCENARIO_DIR}/group_vars/all/99-molecule.yml" ] && [ "${SCENARIO_NAME}" != "default" ]; then
        touch "${SCENARIO_DIR}/group_vars/all/99-molecule.yml"
    fi
    if [ ! -f "${SCENARIO_DIR}/molecule.yml" ]; then
        cp "${SCRIPT_DIR}/template_molecule.yml" "${SCENARIO_DIR}/molecule.yml"
    fi
done
