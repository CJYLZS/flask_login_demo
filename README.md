## Flask登录示例程序



后端配置

mysql

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



前端采用react组件渲染页面



实现功能:

- 注册账户/注销账户
- 登录/登出
- 邮箱找回密码
- 登录失败超过6次强制进行人机验证后才能登录
- 注册和找回密码均使用captcha防止暴力反复注册

