# -*- coding:utf-8 -*-

from ansible import constants as C
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager

## 用来加载解析yaml文件或JSON内容,并且支持vault的解密
loader = DataLoader()

# 管理变量的类，包括主机，组，扩展等变量，之前版本是在 inventory中的
variable_manager = VariableManager()

# 初始化需要的对象
Options = namedtuple('Options', [
    'connection',
    'remote_user',
    'ask_sudo_pass',
    'verbosity',
    'ack_pass',
    'module_path',
    'forks',
    'become',
    'become_method',
    'become_user',
    'check',
    'listhosts',
    'listtasks',
    'listtags',
    'syntax',
    'sudo_user',
    'sudo'
])

options = Options(connection='smart',
                  remote_user='root',
                  ack_pass=False,
                  sudo_user='root',
                  forks=10,
                  sudo='yes',
                  ask_sudo_pass=False,
                  verbosity=5,
                  module_path=None,
                  become=True,
                  become_method='sudo',
                  become_user='root',
                  check=None,
                  listhosts=None,
                  listtasks=None,
                  listtags=None,
                  syntax=None
                  )

passwords = dict(vault_pass='')