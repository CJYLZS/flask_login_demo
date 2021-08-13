## Flask登录示例程序



后端配置

部署需要自己配置config.json

```json
{
    "MYSQL_CONFIG":{
        // mysql 的账户配置
        "host":"127.0.0.1",
        "port":3306,
        "user":"ylzs",
        "password":"123123",
        "database":"flask_db_0" // 数据库名
    },
    "EMAIL_CONFIG":{
        // 找回邮件采用stmp发送
        "smtp_url":"smtp.qq.com",
        "smtp_port":465,
        "email_account":"3531555795@qq.com",
        "email_passwd":"cviwjdvzzbxmcjih"// stmp的授权码
    },
    "WEB_CONFIG":{
        // 找回邮件的链接由这个配置生成 例如: http://127.0.0.1:5000/.....
        "protocol":"http",
        "domain":"127.0.0.1",
        "port":5000
    }
}
```



mysql数据表结构 数据表名: ==users==

```shell
+----------+--------------+------+-----+---------+----------------+
| Field    | Type         | Null | Key | Default | Extra          |
+----------+--------------+------+-----+---------+----------------+
| username | varchar(50)  | YES  |     | NULL    |                |
| passwd   | varchar(150) | YES  |     | NULL    |                |
| id       | bigint       | NO   | PRI | NULL    | auto_increment |
| email    | varchar(50)  | NO   |     | NULL    |                |
+----------+--------------+------+-----+---------+----------------+
4 rows in set (0.00 sec)
```



前端相关文件位于static和templates两个目录



实现功能:

- 注册账户/注销账户
- 登录/登出
- 邮箱找回密码
- 登录失败超过5次强制进行人机验证后才能登录
- 注册和找回密码均使用captcha防止暴力反复注册

