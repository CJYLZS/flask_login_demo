from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from captcha.image import ImageCaptcha
import random
import uuid
import os

from mysql import sql_util

import smtplib
from email.mime.text import MIMEText

def sendMail(body, email):
    try:
        """发送邮件"""
        msg = MIMEText(body)
        msg["Subject"] = "密码重置"
        msg["From"] = "YLZS的登录网页"  # from
        msg["To"] = "你的qq邮箱"  # to

        s = smtplib.SMTP_SSL("smtp.qq.com", 465)
        s.login("3531555795@qq.com", "cviwjdvzzbxmcjih")  # 这里的第二个参数为qq邮箱授权码，不要填你的密码
        s.sendmail("3531555795@qq.com", [email, ], msg.as_string())  # from，to，msg
        s.quit()
    except Exception as e:
        print("邮件发送失败~~" + e.message)

class User(UserMixin):
    def __init__(self, user):
        self.id = user.get('id')
        self.username = user.get('username')
        self.passwd_hash = user.get('passwd')
    
    def verify_password(self, passwd):
        if self.passwd_hash is None:
            return False
        return check_password_hash(self.passwd_hash, passwd)

    def get_id(self):
        return self.id

    def get_username(self):
        return self.username

class login_util:
    def __init__(self, app, login_view):
        login_manager = LoginManager()
        login_manager.init_app(app)
        login_manager.login_view = login_view
        login_manager.user_loader(self.load_user)
        self._sql_util = sql_util()

    def load_user(self, user_id):
        result = self._sql_util.find_user_by_('id', user_id)
        if len(result) == 0:
            return None
        result = result[0]
        return User({
            'id':result[0],
            'username':result[1],
            'passwd':result[2]
        })

    def get_user(self, username):
        result = self._sql_util.find_user_by_('username', username)
        if len(result) == 0:
            return None
        result = result[0]
        return User({
            'id':result[0],
            'username':result[1],
            'passwd':result[2]
        })
    
    def get_current_user(self):
        return current_user

    def login(self, login_data):
        # get username passwd
        username = login_data.get('username')
        passwd = login_data.get('password')
        user = self.get_user(username) # get user_info
        if user:
            login_user(user)
            if user.verify_password(passwd):
                return (True, '')
        return (False, '用户名或密码错误!')
    
    def logout(self):
        logout_user()
    
    def signup(self, signup_data):
        email = signup_data.get('email')
        username = signup_data.get('username')
        passwd = signup_data.get('password')
        return self._sql_util.add_user(username, passwd, email)

    def deleteuser(self):
        return self._sql_util.delete_user(current_user.get_id())

    def send_reset_mail(self, username, passwd_hash, email):
        mail_data = ("%s reset password link: http://127.0.0.1:5000/pwset?old_hash=%s") \
            % (username,passwd_hash)
        sendMail(mail_data, email)


    def reset_passwd(self, reset_data):
        email = reset_data.get('email')
        user_data = self._sql_util.find_user_by_('email', email)
        if len(user_data) == 0:
            return (False, '邮箱未注册账户!')
        elif len(user_data) > 1:
            print('ERROR! email has mutiple user!')
        user_data = user_data[0]
        self.send_reset_mail(user_data[1], user_data[2], user_data[3])
        return (True, '已发送!')
    
    def set_passwd(self, set_passwd_data):
        new_passwd = set_passwd_data.get('password')
        if current_user.is_authenticated:
            return self._sql_util.update_user_passwd_by_('id',current_user.get_id(), new_passwd)

        old_hash = set_passwd_data.get('old_hash')
        return self._sql_util.update_user_passwd_by_('passwd', old_hash, new_passwd)

    def verify_old_hash(self, old_hash):
        result = self._sql_util.find_user_by_('passwd', old_hash)
        if len(result) == 0:
            return False
        return True

    
    def remove_old_captcha(self, filename):
        try:
            os.remove(filename)
        except FileNotFoundError:
            pass

    def get_new_captcha(self, session):
        self.remove_old_captcha(session.get('vcode_filename',''))
        image = ImageCaptcha()
        v_str = str(random.randint(10000,99999))
        v_filename = 'static/vcode/'+str(uuid.uuid4())+'.png'
        image.write(v_str, v_filename)
        session['vcode_result'] = v_str
        session['vcode_filename'] = v_filename
        return (True, '', v_filename)

    def verify_vcode(self, session, verify_data):
        type_vcode = verify_data.get('vcode','')
        if type_vcode == session['vcode_result']:
            self.remove_old_captcha(session.get('vcode_filename',''))
            return (True, '')
        else:
            return (False, '验证码错误!')

        

        
