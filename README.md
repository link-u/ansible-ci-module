# ansible role 用のインフラ CI

## 概要

このツールは tox と molecule によるインフラ CI の共通部分をサブモジュールとして切り分けるためのもの.

主に以下のことができるようになる

* ansible-lint による linting (デフォルト)
* ansible role の流し込み CI (デフォルト)
* testinfra によるテスト (設定の必要あり)

## 前提

* LXD/LXC 環境の用意
* tox のインストール (pip などでインストール)

## サブモジュールとして role に追加

role ディレクトリにこのサブモジュールを追加する

```
$ git submodule add https://github.com/link-u/infra-ci_for_role.git
```

## 使い方 (基本編)

role ディレクトリ内で以下を実行できる.

```
## CI する環境の確認
$ tox -c infra-ci_for_role/tox.ini --listenvs
ubuntu1804-ansible28
ubuntu1804-ansible29
ubuntu2004-ansible28
ubuntu2004-ansible29

## ubuntu2004-ansible29 を CI する場合
$ tox -c infra-ci_for_role/tox.ini -e ubuntu2004-ansible29

## 全環境で CI する場合
$ tox -c infra-ci_for_role/tox.ini
```

これにより以下の CI を確認できる

* ansible-lint による linting
* ansible の流し込み

## 使い方 (応用編)

### テストの自作

一般的に, role 毎にテスト方法は違う. そのため role のテストまで CI したい場合は以下のようにする.

まず必要なディレクトリと testinfra 用のファイルを用意する.

```
## role ディレクトリ内に以下のパスでテスト用のディレクトリを作成する
$ mkdir -p molecule/common/tests
$ touch molecule/common/tests/test_role.py
```

そして以下の testinfra 用テスト test_role.py を編集する.<br>
※ 名前が `test_` で始まる関数が必要<br>
※ `test_` で始まれば何個あっても良い

以下に test_role.py の一例を用意する.
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


### molecule のシナリオの自作

CI したい role によっては, デフォルトで用意しているシナリオ ([molecule/default/molecule.yml](molecule/default/molecule.yml)) では満足できない場合がある.

その場合は role ディレクトリ内に `molecule/default/molecule.yml` を作ることで自作シナリオを用意できる.

まず, 以下のように必要なファイルとディレクトリを用意する.
```
## role ディレクトリ内にシナリオを用意
$ mkdir -p molecule/default/
$ touch molecule/default/molecule.yml

## group_vars が必要な場合 (test で必要な場合もあるので用意したほうが良い)
$ mkdir -p molecule/default/group_vars/all/
$ ln -s ../../../../defaults/main.yml \
        molecule/default/group_vars/all/00-defaults.yml
```

そして, 自作 molecule.yml 編集する.
例えば, 仮想化インスタンスを3台建てたいなら以下のように編集する.
```yaml
---
platforms:
  - name: ${MOLECULE_DISTRO}-${ANSIBLE_VER}-1
    alias: ubuntu/${MOLECULE_DISTRO}/amd64

  - name: ${MOLECULE_DISTRO}-${ANSIBLE_VER}-2
    alias: ubuntu/${MOLECULE_DISTRO}/amd64

  - name: ${MOLECULE_DISTRO}-${ANSIBLE_VER}-3
    alias: ubuntu/${MOLECULE_DISTRO}/amd64
```

またこの molecule.yml は [molecule/common/base.yml](molecule/common/base.yml) にマージされることで molecule に読み込まれる.

## Licence
MIT
