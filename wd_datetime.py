# -*- coding:utf-8 -*-
'''
Author: wood
Date: 2017-08-28
Desc: ʱ����ز���,������ʽ���ͱȽ�
'''


from datetime import datetime
from datetime import timedelta
import time

# timeģ���е�����ʱ����ʽ
now_stamp = time.time()
now_local_stamp = time.localtime()
now_utc_stamp = time.gmtime()
print '{0}: {1}\n'.format('ʱ���', now_stamp)
print '{0}: {1}\n'.format('struct_time���͵ı���ʱ��', now_local_stamp)
print '{0}: {1}\n'.format('struct_time���͵�utcʱ��', now_utc_stamp)

# timeģ���У�����ʱ����ʽ֮���ת��
now_stamp = time.time()                        # ʱ���
local_time = time.localtime(now_stamp)         # ʱ���תstruct_time���͵ı���ʱ��
utc_time = time.gmtime(now_stamp)              # ʱ���תstruct_time���͵�utcʱ��
time_stamp_1 = time.mktime(local_time)          # struct_time���͵ı���ʱ��תʱ���

# timeģ���У�����ʱ����ʽ���ַ���֮���ת��
print '{0} {1}\n'.format('ʱ���תĬ���ַ���:' ,  time.ctime(now_stamp)) # ʱ���ת�ַ���(����ʱ���ַ���)
print '{0} {1}\n'.format('struct_time���͵ı���ʱ��ת�ַ����Զ����ʽ: ', time.strftime("%Y-%m-%d %H:%M:%S", local_time)) # struct_time���͵ı���ʱ��ת�ַ������Զ����ʽ
print '{0} {1}\n'.format('struct_time���͵ı���ʱ��ת�ַ����Զ����ʽ: ', time.strftime("%Y-%m-%d %H:%M:%S", local_time)) # struct_time���͵ı���ʱ��ת�ַ������Զ����ʽ
struct_time = time.strptime("2017-08-28 16:10:00", "%Y-%m-%d %H:%M:%S")       # �ַ���תstruct_time����


'''
%Y: ��λ�����
%y: ��λ�����
%m: ��λ���·�
%d: ��λ������(��01-31����ʾ)
%H: Сʱ(��00-23����ʾ)
%M: ����(��00-59����ʾ)
%S: ����
'''
# ���������ʽ��: datetime ---> string
now = datetime.now() #ȡ�ñ���ʱ�䣬�˶���Ϊdatetime��ʵ��
print '��ǰʱ��: {0}'.format(now.strftime('%Y-%m-%d %H:%M:%S'))

# ���������ʽ��: string ---> datetime
t_str = '2017-08-28 16:00:00'
d = datetime.strptime(t_str, '%Y-%m-%d %H:%M:%S')

# ���ڱȽϲ���
delta = timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)
print '��ʼ��timedelta����: {0}'.format(delta)

#���ڸ�ʽ��
before_day = datetime.strptime('2017-08-28 15:05:30', '%Y-%m-%d %H:%M:%S')
after_day = datetime.strptime('2017-08-31 17:04:20', '%Y-%m-%d %H:%M:%S')

delta = after_day - before_day
print '�������: {0}'.format(delta.days)


