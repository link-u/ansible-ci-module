# ansible 用のインフラ CI モジュール

## 1. 目次

<!-- TOC depthFrom:2 -->

- [1. 目次](#1-目次)
- [2. 概要](#2-概要)
- [3. 前提](#3-前提)
- [4. インストール](#4-インストール)
- [5. 使い方 (基本編)](#5-使い方-基本編)
- [6. 使い方 (応用編)](#6-使い方-応用編)
    - [6.1. テストの自作](#61-テストの自作)
    - [6.2. molecule のシナリオの自作](#62-molecule-のシナリオの自作)
- [7. その他](#7-その他)
    - [7.1. ラッパースクリプト molecule.py について](#71-ラッパースクリプト-moleculepy-について)
- [8. Licence](#8-licence)

<!-- /TOC -->

<br>

## 2. 概要

CI したい role のリポジトリにこのリポジトリをサブモジュールとして追加することでインフラ CI を提供する.

主に以下のことができるようになる

* ansible-lint による linting (デフォルト)
* ansible role の流し込み CI (デフォルト)
* testinfra によるテスト (設定の必要あり)

<br>

## 3. 前提

* python (>= 3.6)
* LXD/LXC 環境の用意
* tox のインストール (pip などでインストール)

簡単なインストール方法を提示する. カスタマイズしたい場合は各々でやること.

```
## 必要な deb パッケージのインストール
$ sudo apt update
$ sudo apt install lxd lxd-tools qemu-block-extra python3 python3-pip python3-setuptools

## LXD の初期設定
$ sudo lxd init --auto
$ sudo usermod -aG lxd $(whoami)

## tox のインストール
$ pip3 install tox
```

<br>

## 4. インストール

role ディレクトリにこのリポジトリをサブモジュールとして追加する

```
$ git submodule add https://github.com/link-u/ansible-ci-module.git
```

role に追加後は以下のようなディレクトリ構成となる.

```
<role directory>/
├── defaults/...
├── tasks/...
├── ...
│
└── ansible-ci-module/  ## It is this repository as a submodule.
```

<br>

## 5. 使い方 (基本編)

特に何もカスタマイズしなくても以下の CI ができるようになる (前提は必要).

* ansible-lint による linting
* ansible の流し込み

作業ディレクトリは `<role directory>` とする.

```
## CI する環境の確認
$ tox -c ansible-ci-module/tox.ini --listenvs
ubuntu1804-ansible28
ubuntu1804-ansible29
ubuntu2004-ansible28
ubuntu2004-ansible29

## ubuntu2004-ansible29 を CI する場合
$ tox -c ansible-ci-module/tox.ini -e ubuntu2004-ansible29

## 全パターン CI する場合
$ tox -c ansible-ci-module/tox.ini
```

<br>

## 6. 使い方 (応用編)

### 6.1. テストの自作

一般的に, role 毎にテスト方法は違う. そのため role のテストまで CI したい場合は以下のようにする.

まず必要なディレクトリと testinfra 用のファイルを用意する.<br>
作業ディレクトリは `<role directory>` とする.

```
## role ディレクトリ内に以下のパスでテスト用のディレクトリを作成する
$ mkdir -p molecule/common/tests
$ touch molecule/common/tests/test_role.py  # テストファイルの名前は `test_*.py` という形式

## また以下の .gitignore の記述を <role directory> 直下に用意しておいたほうが良い.
$ echo "__pycache__/" >> <role directory>/.gitignore
```

この時のディレクトリ構成はこのようになる.

```
<role directory>/
├── defaults/...
├── tasks/...
├── ...
│
├── ansible-ci-module/  ## It is this repository as a submodule.
└── molecule/           ## user-defined molecule directory
    └── common/
        └── tests/
            ├── .gitignore
            └── test_role.py  ## user-defined test.
```

そして以下の testinfra 用テストである test_role.py を編集する.<br>
* 名前が `test_` で始まる関数が必要.
* `test_` で始まれば複数ファイルあっても良い.

以下に `test_role.py` の一例を用意する.

```python
import os
import testinfra.utils.ansible_runner

## molecule から呼び出した場合のインベントリファイルを読み込むために必要
testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')

## テスト用関数
def test_passwd_file(host):
    passwd = host.file("/etc/passwd")
    assert passwd.contains("root")
    assert passwd.user == "root"
    assert passwd.group == "root"
    assert passwd.mode == 0o644
```

<br>

### 6.2. molecule のシナリオの自作

CI したい role によっては, デフォルトで用意しているシナリオ ([./molecule/default/molecule.yml](molecule/default/molecule.yml)) では満足できない場合がある.

その場合は role ディレクトリ内に `molecule/default/molecule.yml` を作ることで自作シナリオを用意できる.

まず, 以下のように必要なファイルとディレクトリを用意する.<br>
作業ディレクトリは `<role directory>` とする.

```
## role ディレクトリ内にシナリオを用意
#  * molecule/<シナリオ名>/molecule.yml という命名規則で設置する.
#  * シナリオについては molecuel の公式ドキュメントを参照すること.
#
$ mkdir -p molecule/default/
$ touch molecule/default/molecule.yml


## group_vars が必要な場合
#  * testinfra からは group_vars を読み込めるが, role の defalts/main.yml は読み込めない.
#  * group_vars 内にシンボリックリンクを貼ることで解決できる.
#
$ mkdir -p molecule/default/group_vars/all/
$ ln -s ../../../../defaults/main.yml molecule/default/group_vars/all/00-defaults.yml
```

この時のディレクトリ構成はこのようになる.

```
<role directory>/
├── defaults/...
├── tasks/...
├── ...
│
├── ansible-ci-module/  ## It is this repository as a submodule.
└── molecule/           ## user-defined molecule directory
    └── default/        ## user-defined molecule scenario
        ├── group_vars/
        │   └── all/
        │       └── 00-defaults.yml -> ../../../../defaults/main.yml
        │
        └── molecule.yml
```

自作 `molecule.yml` は [molecule/common/base.yml](molecule/common/base.yml) をベースとして, 「変更したい」 or 「付け足したい」項目のみを編集する.

例えば, 仮想化インスタンスを3台建てたいなら以下のように編集する.

```yaml
---
platforms:
  - name: focal-instance-1
    alias: ubuntu/focal/amd64

  - name: focal-instance-2
    alias: ubuntu/focal/amd64

  - name: focal-instance-3
    alias: ubuntu/focal/amd64
```

`molecule.yml` では OS の環境変数も使うことができるので,

```yaml
platforms:
  - name: ${MOLECULE_DISTRO}-instance-1
    alias: ubuntu/${MOLECULE_DISTRO}/amd64

  - name: ${MOLECULE_DISTRO}-instance-2
    alias: ubuntu/${MOLECULE_DISTRO}/amd64

  - name: ${MOLECULE_DISTRO}-instance-3
    alias: ubuntu/${MOLECULE_DISTRO}/amd64
```

のような書き方もできる.

<br>

## 7. その他

### 7.1. ラッパースクリプト molecule.py について

[molecule.py](scripts/molecule.py) は `molecule` コマンドのラッパースクリプトである. <br>
基本的に `molecule` コマンドと同じオプションが使用できる.

このラッパースクリプトは以下の機能を提供する.

* [./molecule/common/base.yml](./molecule/common/base.yml) を自動で読み込む.

  `molecule.py` のコマンドライン引数に `-c` or `--base-config` が指定されていない場合, デフォルトでは以下のコマンドと等価になる.
  ```
  molecule -c ./molecule/common/base.yml <sub command>

  or

  molecule --base-config ./molecule/common/base.yml <sub command>
  ```

<br>

* 自作 molecule シナリオの有無で作業ディレクトリを変更

  `<role directory>` に molecule シナリオが存在するかどうかで `molecule` コマンドの作業ディレクトリが変わる.

  * `<role directory>/molecule/*/molecule.yml` が無い場合 (default)

    ```
    ## work directory
    <role directory>/ansible-ci-module/
    ```

  * `<role directory>/molecule/*/molecule.yml` が有る場合

    ```
    ## work directory
    <role directory>/
    ```

<br>

* 自作テストの有無で testinfra のディレクトリを変更

  * `<role directory>/molecule/common/tests/test_*.py` がない場合 (default)

    ```
    ## testinfra directory
    <role directory>/ansible-ci-module/molecule/common/tests/
    ```

  * `<role directory>/molecule/common/tests/test_*.py` がある場合

    ```
    ## testinfra directory
    <role directory>/molecule/common/tests/
    ```

<br>

## 8. Licence
MIT
