# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li
    :license: MIT, see LICENSE for more details.
"""

import os
from types import MethodDescriptorType, MethodType
import json
import traceback

from flask import Flask, render_template, redirect, url_for, request, session
from flask_wtf import CSRFProtect
from flask_login import login_required

from login import login_util

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'secret string')

app.config['CAPTCHA_ENABLE'] = True
app.config['CAPTCHA_LENGTH'] = 5
app.config['CAPTCHA_WIDTH'] = 160
app.config['CAPTCHA_HEIGHT'] = 60

app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True
CSRFProtect(app)


app_login_util = login_util(app,'login')

def result_str(result = True, msg = '', url = ''):
    return json.dumps({
        'result':result,
        'msg':msg,
        'url':url
    })

def update_login_failed_session(session):
    if 'failed_login_times' in session.keys():
        session['failed_login_times'] += 1
    else:
        session['failed_login_times'] = 0

def reset_login_failed_session(session):
    if 'failed_login_times' in session.keys():
        session['failed_login_times'] = 0
    else:
        session['failed_login_times'] = 0

def get_login_failed_times(session):
    return session.get('failed_login_times', 0)

def load_captcha(session):
    if 'vcode_filename' not in session.keys():
        result, err_msg, filename = app_login_util.get_new_captcha(session)
        if not result:
            raise(err_msg)

@app.route('/')
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        if get_login_failed_times(session) > 5:
            # 跳转到人机认证界面
            return result_str(False, '登录失败次数过多!', url_for('captcha'))
        try:
            login_data = json.loads(request.data)
        except:
            # login data is illegal
            return result_str(False, 'login_data illegal')

        result, err_msg = app_login_util.login(login_data)
        if result:
            # login success redirect to login page
            reset_login_failed_session(session) # login success reset failed login times
            return result_str(result, err_msg, request.args.get('next') or url_for('index'))
        else:
            # login failed return err_msg
            update_login_failed_session(session) # record login failed times ++
            return result_str(result, err_msg)
    load_captcha(session)
    print(session.get('vcode_filename'))
    return render_template('login.html', default_view = 'logIn', vcode = session.get('vcode_filename'))

@app.route('/logout')
@login_required
def logout():
    app_login_util.logout()
    return redirect(url_for('login'))

@app.route('/signup', methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        try:
            signup_data = json.loads(request.data)
        except:
            # signup data is illegal
            return result_str(False, 'signup_data illegal')
        result, err_msg = app_login_util.verify_vcode(session, signup_data)
        if not result:
            # check vcode
            return result_str(result, err_msg)
        result, err_msg = app_login_util.signup(signup_data)
        if result:
            # signup success redirect to login page
            return result_str(result, err_msg, url_for('login'))
        else:
            # signup failed return err_msg
            return result_str(result, err_msg)
    load_captcha(session)
    return render_template('login.html',default_view = 'signUp', vcode = session.get('vcode_filename', ''))

@app.route('/deleteuser', methods=['GET'])
@login_required
def deleteuser():
    result , err_msg = app_login_util.deleteuser()
    if result:
        return redirect(url_for('login'))
    else:
        return render_template('index.html', username = login_util.get_current_user().get_username(),err_msg = err_msg)

@app.route('/index')
@login_required
def index():
    return render_template('index.html', username = app_login_util.get_current_user().username)

@app.route('/pwreset', methods=['GET', 'POST'])
def pwreset():
    if request.method == 'POST':
        try:
            reset_data = json.loads(request.data)
        except:
            # signup data is illegal
            return result_str(False, 'reset_data illegal')
        result, err_msg = app_login_util.verify_vcode(session, reset_data)
        if not result:
            # check vcode
            return result_str(result, err_msg)
        result , err_msg = app_login_util.reset_passwd(reset_data)
        return result_str(result, err_msg)
    load_captcha(session)
    return render_template('login.html',default_view = 'PWReset', vcode = session.get('vcode_filename', ''))

@app.route('/pwset', methods=['GET', 'POST'])
def pwset():
    if request.method == 'POST':
        try:
            set_passwd_data = json.loads(request.data)
        except:
            # signup data is illegal
            return result_str(False, 'set_passwd_data illegal')
        result, err_msg = app_login_util.verify_vcode(session, set_passwd_data)
        if not result:
            # check vcode
            return result_str(result, err_msg)
        result, err_msg = app_login_util.set_passwd(set_passwd_data)
        if result:
            return result_str(result, err_msg, url_for('login'))
        else:
            return result_str(result, err_msg)
    else:
        # GET
        load_captcha(session)
        if app_login_util.get_current_user().is_authenticated:
            return render_template('login.html',default_view = 'PWSet', vcode = session.get('vcode_filename', ''))
        
        old_hash = request.args.get('old_hash')
        if app_login_util.verify_old_hash(old_hash):
            return render_template('login.html',default_view = 'PWSet', vcode = session.get('vcode_filename', ''))
        else:
            return render_template('login.html',default_view = 'logIn', err_msg = '请求参数非法不能修改密码!', vcode = session.get('vcode_filename', ''))

@app.route('/captcha', methods=['GET', 'POST'])
def captcha():
    if request.method == 'POST':
        try:
            vcode_verify_data = json.loads(request.data)
        except:
            # signup data is illegal
            return result_str(False, 'vcode_verify_data illegal')
        result, err_msg = app_login_util.verify_vcode(session, vcode_verify_data)
        if result:
            reset_login_failed_session(session) # 人机验证完成 重置失败登录次数
            return result_str(result, err_msg, url_for('login'))
        else:
            return result_str(result, err_msg)

    result, err_msg, filename = app_login_util.get_new_captcha(session)
    return render_template('login.html',default_view = 'Captcha', vcode = session.get('vcode_filename', ''))

@app.route('/newvcode', methods=['GET'])
def newvcode():
    result, err_msg, filename = app_login_util.get_new_captcha(session)
    return result_str(result, err_msg, filename)