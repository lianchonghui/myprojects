# coding:utf-8

import logging
import hashlib
import config
import re

from handlers.BaseHandler import BaseHandler
from tornado.web import RequestHandler
from utils.response_code import RET
from utils.session import Session
from utils.commons import required_login

class RegisterHandler(BaseHandler):
    #注册
    def post(self):
        mobile = self.json_args.get('mobile')
        sms_code = self.json_args.get('phonecode')
        password = self.json_args.get('password')
        #检查参数
        # all(iterable)传入一个可迭代对象，判断是否所有元素为True，如果有False,则返回False
        if not all([mobile,sms_code,password]):
            return self.write(dict(errcode=RET.PARAMERR,errmsg='参数不完整'))

        if not re.match(r'1\d{10}$',mobile):
            return self.write(dict(errcode=RET.DATAERR,errmsg='手机好格式错误'))

        #如果对密码有限制则进行判断
        #if len(password)<6

        #判断短信验证码是否正确
        if '2468' != sms_code:
            '''
            try:
                real_sms_code = self.redis.get("sms_code_%s" % mobile)
            except Exception as e:
                logging.error(e)
                return self.write(dict(errcode=RET.DBERR,errmsg='查询验证码出错'))
            
            #判断短信验证码是否过期
            if not real_sms_code:
                return self.write(dict(errcode=RET.NODATA,errmsg='验证码过期'))

            # 对比用户填写的验证码与真实值
            if real_sms_code != sms_code:
                return self.write(dict(errcode=RET.DATAERR,errmsg='验证码错误'))

            try:
                self.redis.delete('sms_code_%s' % mobile)
            except Exception as e:
                logging.error(e)
'''
        # 保存数据，同时判断手机好是否存在，判断的依据是数据库中的mobile字段的唯一约束
        passwd = hashlib.sha256(password+config.passwd_hash_key).hexdigest()
        sql="insert into ih_user_profile(up_name,up_mobile,up_passwd) values (%(name)s,%(mobile)s,%(passwd)s);"
        try:
            user_id = self.db.execute(sql,name=mobile,mobile=mobile,passwd=passwd)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DATAEXIST,errmsg='手机好已存在'))

        #用session记录用户的登录状态
        session = Session(self)
        session.data['user_id'] = user_id
        session.data['mobile'] = mobile
        session.data['name'] = mobile
        try:
            session.save()
        except Exception as e:
            logging.error(e)

        self.write(dict(errcode=RET.OK,errmsg='注册成功'))

class LoginHandler(BaseHandler):
    def get(self):
        self.write('hello login')
    # 登录
    def post(self):
        # 获取参数
        mobile = self.json_args.get('mobile')
        password = self.json_args.get('password')

        # 检查参数
        if not all((mobile,password)):
            return self.write(dict(errcode=RET.PARAMERR, errmsg='参数错误'))
        if not re.match(r'^1\d{10}$',mobile):
            return self.write(ditc(errcode=RET.DATAERR,errmsg='手机号错误'))

        # 检查秘密是否正确
        res = self.db.get('select up_user_id,up_name,up_passwd from ih_user_profile where up_mobile=%(mobile)s',mobile=mobile)
        password = hashlib.sha256(password+config.passwd_hash_key).hexdigest()

        if res and res['up_passwd'] == unicode(password):
            # 生成session数据
            # 返回客户端
            try:
                self.session = Session(self)
                self.session.data['user_id'] = res['up_user_id']
                self.session.data['name'] = res['up_name']
                self.session.data['mobile'] = mobile
                self.session.save()
            except Exception as e:
                logging.error(e)
            return self.write(dict(errcode=RET.OK,errmsg='OK'))
        else:
            return self.write(dict(errcode=RET.DATAERR,errmsg='手机号或密码错误'))

class LogoutHandler(BaseHandler):
    # 退出登录
    @required_login
    def get(self):
        # 清除session数据
        self.session.clear()
        self.write(dict(errcode=RET.OK,errmsg='退出成功'))
