# -*- coding:utf-8 -*-
# 描述:V0.1 WOOD 2018-06-11 task重写封装api基本功能

import json
from ansible import constants as C
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager

from .attr import loader
from .attr import variable_manager
from .attr import passwords
from .attr import options
from .inventory import FyYunweiInventory as Inventory

try:
    from __main__ import display
except ImportError:
    from ansible.utils.display import Display
    display = Display()

# 根据inventory加载对应变量
inventory = Inventory(loader, variable_manager, "新增测试group", dict(), host_list=[])

class FyYunweiTask(object):

    '''封装一个task接口, 提供给外部使用'''
    def __init__(self, inventory=inventory, task_name='测试task', hosts="test", module="shell", args="ls -lh", stdout_callback=None):
        ## 用来加载解析yaml文件或JSON内容,并且支持vault的解密
        self.loader = loader

        # 管理变量的类，包括主机，组，扩展等变量，之前版本是在 inventory中的
        self.variable_manager = variable_manager
        self.inventory = inventory
        self.variable_manager.set_inventory(inventory)

        self.task_name = task_name
        self.hosts = hosts
        self.module = module
        self.args = args
        self.stdout_callback = stdout_callback

    def _play_ds(self):
        if self.module in ('command', 'win_command', 'shell', 'win_shell', 'script', 'raw'):
            return dict( name = self.task_name if self.task_name else "Ansible Ad-Hoc",
                         hosts = self.hosts,
                         gather_facts = 'no',
                         tasks = [
                             dict(action=dict(module=self.module, args=self.args))
                         ]
                         )
        else:
            return dict()

    def run(self):
        #use Runner lib to do SSH things, create play with tasks'''
        play_source = self._play_ds()
        if play_source:
            play = Play().load(play_source, variable_manager=self.variable_manager, loader=self.loader)
        else:
            return
        # now create a task queue manager to execute the play
        self._tqm = None
        try:
            self._tqm = TaskQueueManager(
                    inventory=self.inventory,
                    variable_manager=self.variable_manager,
                    loader=self.loader,
                    options=options,
                    passwords=passwords,
                    stdout_callback=self.stdout_callback
                )
            result = self._tqm.run(play)
        finally:
            if self._tqm:
                self._tqm.cleanup()
            if self.loader:
                self.loader.cleanup_all_tmp_files()
        return result