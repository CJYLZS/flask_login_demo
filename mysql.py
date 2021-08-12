

import re
import pymysql
from werkzeug.security import generate_password_hash


class sql_util:
    def __init__(self):
        self._sql_config = {
            'host':'127.0.0.1',
            'port':3306,
            'user':'ylzs',
            'password':'123123',
            'database':'flask_db_0'
        }
        self.db = pymysql.connect(**self._sql_config)
        self.cursor = self.db.cursor()
    
    def find_user_by_(self, by_, value):
        if not by_ or not value:
            return ()
        sql = 'SELECT id, username, passwd, email FROM users WHERE '+ by_ +' = %s'
        self.cursor.execute(sql, [value])
        result = self.cursor.fetchall()
        return result
    
    def has_user(self, fetch_result):
        if len(fetch_result) == 0:
            return False
        return True
    

    def checkemail(self, email):
        reg="\w+[@][a-zA-Z0-9_]+(\.[a-zA-Z0-9_]+)+"
        result=re.findall(reg,email)
        if result:
            return True   #邮箱合法
        else:
            return False    #邮箱不合法
    def add_user(self, username, passwd, email):
        if len(username) < 5:
            return (False, '用户名长度过短!')
        if len(passwd) < 5:
            return (False, '密码过短!')
        if not self.checkemail(email):
            return (False, '邮箱格式不正确!')
        if self.has_user(self.find_user_by_('username', username)):
            return (False,'用户名已存在!')
        if self.has_user(self.find_user_by_('email', email)):
            return (False, '邮箱已存在!')
        
        sql = 'INSERT INTO users (username, passwd, email) VALUES (%s, %s, %s)'
        result = bool(self.cursor.execute(sql, [username, generate_password_hash(passwd), email]))
        self.db.commit()
        return (result, '')
    
    def delete_user(self, id):
        if not self.has_user(self.find_user_by_('id', id)):
            return (False, '用户不存在!')
        sql = 'DELETE FROM users where id = %s'
        result = bool(self.cursor.execute(sql, [id]))
        self.db.commit()
        return (result, '')
    
    def update_user_passwd_by_(self, by_, by_value, passwd):
        # value is origin passwd
        # 执行此函数应该保证用户存在
        if not by_ or not by_value:
            return (False, '后端参数不正确!')
        if len(passwd) < 5:
            return (False, '密码长度过短!')
        
        sql = 'UPDATE users SET passwd = %s WHERE '+by_+' = %s'
        if bool(self.cursor.execute(sql, [generate_password_hash(passwd), by_value])):
            self.db.commit()
            return (True, '修改完成!')
        else:
            return (False, '修改失败 可能是用户不存在!')


