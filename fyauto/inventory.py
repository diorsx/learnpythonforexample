# -*- coding:utf-8 -*-
# 描述: V0.1 WOOD 2017-06-24 Inventory重写封装api基本功能

__auther__ = 'wood'
__verson__ = 'v0.1'

from ansible.compat.six import string_types, iteritems

from ansible import constants as C
from ansible.errors import AnsibleError

from ansible.inventory.dir import InventoryDirectory, get_file_parser
from ansible.inventory.group import Group
from ansible.inventory.host import Host

try:
    from __main__ import display
except ImportError:
    from ansible.utils.display import Display
    display = Display()

HOSTS_PATTERNS_CACHE = {}
from ansible.inventory import Inventory

class FyYunweiInventory(Inventory):

    def __init__(self, loader, variable_manager, group_name, group_ext_vars, host_list=C.DEFAULT_HOST_LIST):

        # the host file file, or script path, or list of hosts
        # if a list, inventory data will NOT be loaded
        # self.host_list = unfrackpath(host_list, follow=False)
        # 传入的hosts
        self._loader = loader
        self._variable_manager = variable_manager
        self.host_list  = host_list
        # 传入的项目名也是组名
        self._group_name = group_name
        self._group_ext_vars = group_ext_vars

        super(FyYunweiInventory, self).__init__(self._loader, self._variable_manager, self.host_list)
        self.add_zdy_group()

    def add_zdy_group(self):
        # 添加自定义的组
        if isinstance(self._group_name, str) and self._group_name:
            # 自定义组名
            zdy_group = Group(self._group_name)
            self.add_group(zdy_group)

            # 为主机组添加额外参数
            # 添加外部变量
            if self._group_ext_vars and isinstance(self._group_ext_vars, dict):
                    for k,v in self._group_ext_vars.items():
                        zdy_group.set_variable(k, v)
