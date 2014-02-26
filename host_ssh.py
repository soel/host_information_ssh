#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
import ssh を使用するために
/u/user/local/lib/python2.7/site-packages/ssh.py
を作成しています
また、paramiko という外部パッケージが必要です

このスクリプトの対象となる機器は
redhat系 のみです
"""
import ssh
import sys
import re

class HostSsh:

    def __init__(self, host, username, password, command_list):
        self.host = host
        self.username = username
        self.password = password
        self.command_list = command_list

    def ssh_connect(self):
        try:
            self.connection = ssh.Connection(
                    self.host,
                    username = self.username,
                    password = self.password
                    )
        except:
            print "ホスト名,ユーザ名,パスワードいずれかが正しくないので接続できませんでした"
            sys.exit()

    def ssh_close(self):
        self.connection.close()

    def command(self):
        #self.command_list からコマンドを取り出して実行
        #例外処理は if で分岐してそれぞれの関数で処理する
        result_list = []
        for command in self.command_list:
            if command == "eth":
                result_list.append(self.ether())
                continue
            if command == "route":
                result_list.append(self.route())
                continue
            if command == "cpu":
                result_list.append(self.cpu())
                continue
            if command == "memory":
                result_list.append(self.memory())
                continue
            result = "".join(self.connection.execute(command))
            result_list.append(self.result_format(command, result))

        return result_list

    def ether(self):
        #/etc/sysconfig/network-scripts/ifcfg-* を検索して
        #該当するファイルの内容をすべて表示する
        eth = self.connection.execute(
            "ls /etc/sysconfig/network-scripts/ifcfg-*")
        eth_result = ""
        for item in eth:
            item = item.rstrip("\n")
            eth_com = "cat " + item
            eth_result += "".join(self.connection.execute(eth_com)) +"\n"
        #最後の改行が余計なので削除
        eth_result = eth_result[:-1]

        return self.result_format("/etc/sysconfig/network-scripts/ifcfg-*", eth_result)

    def route(self):
        #/etc/sysconfig/network-scripts/route-* を検索して
        #該当するファイルの内容をすべて表示する
        route = self.connection.execute(
                "LANG=C ls /etc/sysconfig/network-scripts/route-*")
        route_result = ""
        for item in route:
            item = item.rstrip("\n")
            i = re.match('^ls\: cannot access.+', item)
            j = re.match(
                    '^ls\: \/etc\/sysconfig\/network-scripts\/route-\*\: No such file or directory', item)
            if i or j:
                route_result += item + "\n"
                break
            route_com = "cat" + item
            route_result += "".join(self.connection.execute(route_com)) +"\n"

        return self.result_format("/etc/sysconfig/network-scripts/route-*",
                route_result)

    def cpu(self):
        #cat /proc/cpuinfo の中の processor と model name を表示
        cpu = self.connection.execute(
                "cat /proc/cpuinfo")
        cpu_result = ""
        for item in cpu:
            if re.match('^processor', item):
                cpu_result += item
            if re.match('^model name', item):
                cpu_result += item

        return self.result_format("cat /proc/cpuinfo", cpu_result)

    def memory(self):
        #cat /proc/meminfo の中の MemTotal のみを表示
        memory = self.connection.execute(
                "cat /proc/meminfo")
        memory_result = ""
        for item in memory:
            if re.match('^MemTotal', item):
                memory_result += item

        return self.result_format("cat /proc/meminfo", memory_result)

    def result_format(self, command, result):
        #表示の整形を行う
        result_print = ""
        result_print += "----------\n"
        result_print += command + ":\n\n"
        result_print += result + "\n"

        return result_print

    def result_print(self, result_list):
        #結果の表示を行う
        arr = [str(i) for i in result_list]
        result = "".join(arr)
        print result

def argv_check():
    #引数が足りない場合、使用例を提示してスクリプト終了
    if len(sys.argv) < 2:
        print 'Usage : ./host_ssh.py <IP address> <"option_command"(Comma Separated Value)>'
        sys.exit()

def option():
    #option で入力された文字列を分割して command_list に追加
    #ただし、特定のコマンドは command_list に追加させない
    if len(sys.argv) == 3:
        option_list = sys.argv[2].split(",")
        com_list = []
        for com in option_list:
            com = com.strip()
            if re.match('^shutdown', com):
                break
            if re.match('^reboot', com):
                break
            if re.match('^rm', com):
                break
            com_list.append(com)
        return com_list
    return None

if __name__ == '__main__':
    """
    リストに書かれた順番にコマンドの実行結果が表示されます
    ただし、以下の情報を所得する際はコマンドを書かずに
    指定された文字を書いてください

    インターフェース情報 : "eth"
    /etc/sysconfig/network-scripts/ifcfg-*
    の情報を出力します

    route 情報 : "route"
    /etc/sysconfig/network-scripts/route-*
    の情報を出力します

    cpu 情報 : "cpu"
    cat /proc/cpuinfo 内の processor と model name のみを表示します

    memory 情報 : "memory"
    cat /proc/meminfo 内の MemTotal のみを表示します
    """
    command_list = [
            "hostname",
            "cat /etc/hosts",
            "cat /etc/redhat-release",
            "uname -a",
            "cat /etc/sysctl.conf",
            "eth",
            "route",
            "route -n",
            "cat /etc/sysconfig/network",
            "cat /etc/resolv.conf",
            "cat /etc/ntp.conf",
            "ntpq -p",
            "cpu",
            "memory",
            "df -h",
            "cat /etc/fstab",
            "cat /etc/snmp/snmpd.conf",
            "cat /etc/inittab",
            "cat /etc/init/control-alt-delete.conf",
            "cat /home/bbt-adm/ks-post.log",
            "cat /home/bbt-adm/installcheck/service_off_check",
            "cat /home/bbt-adm/installcheck/service_on_check",
            "grep -i error /var/log/messages",
            "grep -i fail /var/log/messages",
            "dmesg | grep -i error",
            "dmesg | grep -i fail",
            ]

    argv_check()
    option_list = option()
    if option_list:
        command_list.extend(option_list)

    #root のパスワード確認とパラメータの取得
    username_root = 'root'
    print 'user name: '+ username_root + '\n'
    password_root = raw_input('password:')
    host_ssh3 = HostSsh(sys.argv[1], username_root, password_root, command_list)
    host_ssh3.ssh_connect()
    result_list = host_ssh3.command()
    host_ssh3.ssh_close()
    host_ssh3.result_print(result_list)
