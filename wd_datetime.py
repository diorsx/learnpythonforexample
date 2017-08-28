# -*- coding:utf-8 -*-
'''
Author: wood
Date: 2017-08-28
Desc: 时间相关操作,包括格式化和比较
'''


from datetime import datetime
from datetime import timedelta
import time

# time模块中的三种时间形式
now_stamp = time.time()
now_local_stamp = time.localtime()
now_utc_stamp = time.gmtime()
print '{0}: {1}\n'.format('时间戳', now_stamp)
print '{0}: {1}\n'.format('struct_time类型的本地时间', now_local_stamp)
print '{0}: {1}\n'.format('struct_time类型的utc时间', now_utc_stamp)

# time模块中，三种时间形式之间的转换
now_stamp = time.time()                        # 时间戳
local_time = time.localtime(now_stamp)         # 时间戳转struct_time类型的本地时间
utc_time = time.gmtime(now_stamp)              # 时间戳转struct_time类型的utc时间
time_stamp_1 = time.mktime(local_time)          # struct_time类型的本地时间转时间戳

# time模块中，三种时间形式和字符串之间的转换
print '{0} {1}\n'.format('时间戳转默认字符串:' ,  time.ctime(now_stamp)) # 时间戳转字符串(本地时间字符串)
print '{0} {1}\n'.format('struct_time类型的本地时间转字符串自定义格式: ', time.strftime("%Y-%m-%d %H:%M:%S", local_time)) # struct_time类型的本地时间转字符串：自定义格式
print '{0} {1}\n'.format('struct_time类型的本地时间转字符串自定义格式: ', time.strftime("%Y-%m-%d %H:%M:%S", local_time)) # struct_time类型的本地时间转字符串：自定义格式
struct_time = time.strptime("2017-08-28 16:10:00", "%Y-%m-%d %H:%M:%S")       # 字符串转struct_time类型


'''
%Y: 四位数年份
%y: 两位数年份
%m: 两位数月份
%d: 两位数日期(以01-31来表示)
%H: 小时(以00-23来表示)
%M: 分钟(以00-59来表示)
%S: 秒数
'''
# 日期输出格式化: datetime ---> string
now = datetime.now() #取得本地时间，此对象为datetime的实例
print '当前时间: {0}'.format(now.strftime('%Y-%m-%d %H:%M:%S'))

# 日期输出格式化: string ---> datetime
t_str = '2017-08-28 16:00:00'
d = datetime.strptime(t_str, '%Y-%m-%d %H:%M:%S')

# 日期比较操作
delta = timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)
print '初始化timedelta对象: {0}'.format(delta)

#日期格式化
before_day = datetime.strptime('2017-08-28 15:05:30', '%Y-%m-%d %H:%M:%S')
after_day = datetime.strptime('2017-08-31 17:04:20', '%Y-%m-%d %H:%M:%S')

delta = after_day - before_day
print '相差天数: {0}'.format(delta.days)


