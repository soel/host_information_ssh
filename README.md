host_informaiton_ssh
====================

## これは何?
host に ssh でログインして取得したい情報を自動で取得します

## 主な特徴
- パスワード入力はインターフェースに移行し、コマンドライン履歴に残らないようにしています
- 取得したい情報を簡単に追加できます

## インストール
1. 事前確認
  - 動作確認は python2.7 で行っています

1. paramico のインストール
  ```bash
  pip install paramiko
  ```

1. git clone
  ```bash
  git clone https://github.com/soel/host_information_ssh.git
  ```

## 使い方
  ```bash
  ./host_ssh.py <ip address> <option>
  ```
  - option にはデフォルトで取得される情報以外のコマンドを記述すると情報を取得できます

## 取得したい情報の追加/削除
- command_list の配列に追加するか、 option に記述

## その他情報
- デフォルトは root ユーザになっているので、別のユーザにしたい場合は username の変数を変更してください
- デフォルトで取得される情報は、 command_list の配列となります

## その他
- 業務で使用しているスクリプトのリバイズなので上記のユーザ名の指定等不便な部分があります
- 不便な部分は後々解消予定です

## ライセンス
- LICENSE.txt を御覧ください
- MIT ライセンスです
