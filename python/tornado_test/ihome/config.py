# coding:utf-8

'''
    tornado各项配置
'''

import os

# Application配置参数
# cookie_secret以及passwd_hash_key采用uuid4()生成，并用base64()进行压缩
settings= dict(
    static_path = os.path.join(os.path.dirname(__file__),"static"),
    #cookie_secret = "8Lu2611ZRxmJQgp7Pa/EStiA83I11UyEp6f7uBZ+J4w=",
    #xsrf_cookies = True,
    debug = True
)

#mysql配置参数
mysql_options = dict(
    host = "127.0.0.1",
    database = "ihome",
    user = "root",
    password = "root"
)

# redis配置参数
redis_options = dict(
    host = "127.0.0.1",
    port = 6379
)


# 日志配置
# 日志打印可以通过import logging
# 调用logging.debug()/logging.info()/logging.warnning()/loging.error()打印各等级日志
log_path = os.path.join(os.path.dirname(__file__),"logs/ihome_log")
log_level = "debug"
'''
logging.debug()可打印dubug,info,warnning,error的日志
logging.info()打印info,warnning,error的日志
logging.error只打印error的日志
'''

#密码加密密钥
passwd_hash_key = "R72CIewfS4iJ1ccTY+Ala7Y+dC2UQk1+i5lID5VRxyg="

'''
UUID是128位的全局唯一标识符，通常由32字节的字符串表示。
它可以保证时间和空间的唯一性，也称为GUID，全称为：
UUID —— Universally Unique IDentifier      Python 中叫 UUID
GUID —— Globally Unique IDentifier          C#  中叫 GUID

它通过MAC地址、时间戳、命名空间、随机数、伪随机数来保证生成ID的唯一性。
UUID主要有五个算法，也就是五种方法来实现：

1、uuid1()——基于时间戳

由MAC地址、当前时间戳、随机数生成。可以保证全球范围内的唯一性，
但MAC的使用同时带来安全性问题，局域网中可以使用IP来代替MAC。

2、uuid2()——基于分布式计算环境DCE（Python中没有这个函数）

算法与uuid1相同，不同的是把时间戳的前4位置换为POSIX的UID。
实际中很少用到该方法。

3、uuid3()——基于名字的MD5散列值

通过计算名字和命名空间的MD5散列值得到，保证了同一命名空间中不同名字的唯一性，
和不同命名空间的唯一性，但同一命名空间的同一名字生成相同的uuid。    

4、uuid4()——基于随机数

由伪随机数得到，有一定的重复概率，该概率可以计算出来。

5、uuid5()——基于名字的SHA-1散列值

算法与uuid3相同，不同的是使用 Secure Hash Algorithm 1 算法

使用方面：

首先，Python中没有基于DCE的，所以uuid2可以忽略；
其次，uuid4存在概率性重复，由无映射性，最好不用；
再次，若在Global的分布式计算环境下，最好用uuid1；
最后，若有名字的唯一性要求，最好用uuid3或uuid5。
'''
