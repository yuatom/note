# Postfix+Dovecot+MySQL

## 安装需要的软件

```s
yum --enablerepo=centosplus install postfix
yum install dovecot dovecot-mysql
# centos 6
yum install mysql-server 
# centos 7
rpm -Uvh http://dev.mysql.com/get/mysql-community-release-el7-5.noarch.rpm
yum repolist enabled | grep "mysql.*-community.*"
yum -y install mysql-community-server
```

## 配置MySQL

### 初始化MySQL
```sh
## 启动服务
## centos 6
chkconfig mysqld on
service mysqld start

## centos 7
systemctl start mysqld

## 初始化mysql配置，输入后提示设置root密码，是否删除匿名用户，是否禁止root远程登录，是否删除test数据库，是否刷新权限等
mysql_secure_installation
```

### 创建mail用到的数据库及用户等

```sql
CREATE DATABASE d_mail;
use d_mail;

GRANT SELECT, INSERT, UPDATE, DELETE ON d_mail.* TO 'mail_admin'@'localhost' IDENTIFIED BY 'mail_admin_pass';
GRANT SELECT, INSERT, UPDATE, DELETE ON d_mail.* TO 'mail_admin'@'localhost.localdomain' IDENTIFIED BY 'mail_admin_pass';
FLUSH PRIVILEGES;

CREATE TABLE t_domains (
    `id` INT(11) NOT NULL AUTO_INCREMENT,
    `domain` VARCHAR(50) NOT NULL DEFAULT '',
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE t_forwardings (
    `id` INT(11) NOT NULL AUTO_INCREMENT,
    `source` varchar(80) NOT NULL, 
    `destination` TEXT NOT NULL, 
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE t_users (
    `id` INT(11) NOT NULL AUTO_INCREMENT,
    `email` varchar(80) NOT NULL, 
    `password` varchar(32) NOT NULL, 
    UNIQUE KEY `unq_email` (`email`),
    PRIMARY KEY (`id`) 
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE t_transport (
    `id` INT(11) NOT NULL AUTO_INCREMENT,
    `domain` varchar(128) NOT NULL default '', 
    `transport` varchar(128) NOT NULL default '', 
    UNIQUE KEY `unq_domain` (`domain`),
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```

### 绑定MySQL IP只能本地登录
编辑文件`/etc/my.conf`，在`[mysqld]`节中编辑以下内容

```txt
bind-address=127.0.0.1
```

### 重启mysqld
```sh
## centos 6
service mysqld restart

## centos 7
systemctl restart mysqld
```


## 配置Postfix
### 1. 配置Postfix从Mysql获取数据需要的配置
编辑文件：`/etc/postfix/mysql-virtual_domains.cf`
```txt
user = mail_admin
password = mail_admin_pass
dbname = d_mail
query = SELECT domain AS virtual FROM t_domains WHERE domain='%s'
hosts = 127.0.0.1
```

编辑文件：`/etc/postfix/mysql-virtual_forwardings.cf`
```txt
user = mail_admin
password = mail_admin_pass
dbname = d_mail
query = SELECT destination AS virtual FROM t_forwardings WHERE source='%s'
hosts = 127.0.0.1
```

编辑文件：`/etc/postfix/mysql-virtual_mailboxes.cf`
```txt
user = mail_admin
password = mail_admin_pass
dbname = d_mail
query = SELECT CONCAT(SUBSTRING_INDEX(email,<'@'>,-1),'/',SUBSTRING_INDEX(email,<'@'>,1),'/') FROM t_users WHERE email='%s'
hosts = 127.0.0.1
```

编辑文件：`/etc/postfix/mysql-virtual_email2email.cf`
```txt
user = mail_admin
password = mail_admin_pass
dbname = d_mail
query = SELECT email FROM t_users WHERE email='%s'
hosts = 127.0.0.1
```

修改上述配置文件的权限
```sh
chmod o= /etc/postfix/mysql-virtual_*.cf
chgrp postfix /etc/postfix/mysql-virtual_*.cf
```

### 2.为postfix添加用户组

```sh
groupadd -g 5000 vmail
useradd -g vmail -u 5000 vmail -d /home/vmail -m
```

### 3. 修改postfix的配置

编辑文件：`/etc/postfix/main.cf`

```txt
myhostname = mail.yuatom.com
mydomain = yuatom.com
myorigin = yuatom.com
inet_interfaces = all
mynetworks = 127.0.0.0/8
#mydestination = $myhostname, localhost, localhost.localdomain, $mydomain
message_size_limit = 30720000
virtual_alias_domains =
virtual_alias_maps = proxy:mysql:/etc/postfix/mysql-virtual_forwardings.cf, mysql:/etc/postfix/mysql-virtual_email2email.cf
virtual_mailbox_domains = proxy:mysql:/etc/postfix/mysql-virtual_domains.cf
virtual_mailbox_maps = proxy:mysql:/etc/postfix/mysql-virtual_mailboxes.cf
virtual_mailbox_base = /home/vmail
virtual_uid_maps = static:5000
virtual_gid_maps = static:5000
smtpd_sasl_type = dovecot
smtpd_sasl_path = private/auth
smtpd_sasl_auth_enable = yes
broken_sasl_auth_clients = yes
smtpd_sasl_authenticated_header = yes
smtpd_recipient_restrictions = permit_mynetworks, permit_sasl_authenticated, reject_unauth_destination
smtpd_use_tls = yes
smtpd_tls_cert_file = /etc/pki/dovecot/certs/dovecot.pem
smtpd_tls_key_file = /etc/pki/dovecot/private/dovecot.pem
virtual_create_maildirsize = yes
virtual_maildir_extended = yes
proxy_read_maps = $local_recipient_maps $mydestination $virtual_alias_maps $virtual_alias_domains $virtual_mailbox_maps $virtual_mailbox_domains $relay_recipient_maps $relay_domains $canonical_maps $sender_canonical_maps $recipient_canonical_maps $relocated_maps $transport_maps $mynetworks $virtual_mailbox_limit_maps
virtual_transport = dovecot
dovecot_destination_recipient_limit = 1
```

### 4. 配置postfix调用devecot

编辑文件：`/etc/postfix/master/cf`

```txt
dovecot   unix  -       n       n       -       -       pipe
    flags=DRhu user=vmail:vmail argv=/usr/libexec/dovecot/deliver -f ${sender} -d ${recipient}
```

### 5. 启动postfix

```sh
# centos 6
chkconfig postfix on
service postfix start
```

## 配置Dovecot
### 1. 备份配置文件

```sh
mv /etc/dovecot/dovecot.conf /etc/dovecot/dovecot.conf-backup
```

### 2. 修改配置文件中postmaser_address为自己的域名

```txt
    postmaster_address = postmaster@yuatom.com
```

### 3. 配置dovecot读取mysql

编辑文件：`/etc/dovecot/dovecot-sql.conf.ext`

```txt
driver = mysql
connect = host=127.0.0.1 dbname=d_mail user=mail_admin password=mail_admin_pass
default_pass_scheme = CRYPT
password_query = SELECT email as user, password FROM t_users WHERE email='%u';
```

### 4. 修改配置文件的权限

```sh
chgrp dovecot /etc/dovecot/dovecot-sql.conf.ext
chmod o= /etc/dovecot/dovecot-sql.conf.ext
```

### 5. 启动服务

```sh
# centos 6
chkconfig dovecot on
service dovecot start
```

启动后查看日志

```sh
cat /var/log/maillog
# 输出
Mar 18 15:21:59 sothoryos postfix/postfix-script[3069]: starting the Postfix mail system
Mar 18 15:22:00 sothoryos postfix/master[3070]: daemon started -- version 2.6.6, configuration /etc/postfix
Mar 18 15:32:03 sothoryos dovecot: master: Dovecot v2.0.9 starting up (core dumps disabled)
```

### 6. 测试POP3服务

```sh
yum install telnet
telnet localhost pop3
# 输出
Trying 127.0.0.1...
Connected to localhost.localdomain.
Escape character is '^]'.
+OK Dovecot ready.
```


## 配置邮件接收别名
配置后所有发送到root的邮件都会转发到my@yuatom.com。
编辑文件：/etc/aliases
```txt
postmaster: root
root: my@yuatom.com
```

更新别名并重启服务

```sh
newaliases
# centos 6
service postfix restart
```

## 测试Postfix服务

```sh
telnet localhost 25
ehlo localhost
# 输出
250-hostname.example.com
250-PIPELINING
250-SIZE 30720000
250-VRFY
250-ETRN
250-STARTTLS
250-AUTH PLAIN
250-AUTH=PLAIN
250-ENHANCEDSTATUSCODES
250-8BITMIME
250 DSN
```

## 测试账号和域名

### 添加以下域名和账号

```sql
INSERT INTO t_domains (domain) VALUES ('yuatom.com');
INSERT INTO t_users (email, password) VALUES ('sales@yuatom.com', ENCRYPT('pass'));
INSERT INTO t_users (email, password) VALUES ('my@yuatom.com', ENCRYPT('word'));
```

### 发送邮件

```sh
# 如果没有安装mailx
yum install mailx
mailx sales@example.com
# 输入邮件标题和内容，Ctrl+D结束输入并发送
```

### 查看log

```sh
tailf /var/log/maillog
# 输出
Mar 18 15:39:07 server postfix/cleanup[3252]: 444E34055: message-id=<20150318153907.444E34055@server.example.com>
Mar 18 15:39:07 server postfix/qmgr[3218]: 444E34055: from=<root@server.example.com>, size=489, nrcpt=1 (queue active)
Mar 18 15:39:07 server postfix/pipe[3258]: 444E34055: to=<sales@example.com>, relay=dovecot, delay=0.09, delays=0.04/0.01/0/0.05, dsn=2.0.0, sta$
Mar 18 15:39:07 server postfix/qmgr[3218]: 444E34055: removed

tailf /home/vmail/dovecot-deliver.log
# 输出
deliver(<sales@example.com>): 2011-01-21 20:03:19 Info: msgid=\<<20110121200319.E1D148908@hostname.example.com>>: saved mail to INBOX
```

### 查看收件箱

```sh
cd /home/vmail/yuatom.com/{$user}/Maildir
find
# 输出
.
./dovecot-uidlist
./cur
./new
./new/1285609582.P6115Q0M368794.li172-137
./dovecot.index
./dovecot.index.log
./tmp

# GUI方式查看邮件
mutt -f .
```

## 验证imap登录
telnet yuatom.com 143
Trying 139.162.86.231...
Connected to yuatom.com.
Escape character is '^]'.
* OK [CAPABILITY IMAP4rev1 LITERAL+ SASL-IR LOGIN-REFERRALS ID ENABLE IDLE STARTTLS LOGINDISABLED] Dovecot ready.
a login my@yuatom.com word
* BAD [ALERT] Plaintext authentication not allowed without SSL/TLS, but your client did it anyway. If anyone was listening, the password was exposed.
a NO [PRIVACYREQUIRED] Plaintext authentication disallowed on non-secure (SSL/TLS) connections.

需要加密
openssl s_client -connect yuatom.com:143 -starttls imap
openssl s_client -connect yuatom.com:993

firewall-cmd --zone=public --add-port=995/tcp --permanent

openssl s_client -connect yuatom.com:993

## 验证smtp

```sh
telnet yuatom.com 25
Trying 139.162.86.231...
Connected to yuatom.com.
Escape character is '^]'.
220 mail.yuatom.com ESMTP Postfix
AUTH LOGIN
535 5.7.8 Error: authentication failed: Invalid authentication mechanism
```

出现以上错误，需要在在dovecot的配置中加上

```txt
disable_plaintext_auth = yes
auth_mechanisms = plain login
```

```sh
telnet yuatom.com 25
Trying 139.162.86.231...
Connected to yuatom.com.
Escape character is '^]'.
220 mail.yuatom.com ESMTP Postfix
AUTH LOGIN
334 VXNlcm5hbWU6
bXlAeXVhdG9tLmNvbQ==    # 用户名的base64
334 UGFzc3dvcmQ6
d29yZA==                            # 密码的base64
235 2.7.0 Authentication successful
```

## 添加foxmail
imap服务器 mail.yuatom.com:993
用户名 my@yuatom.com
安全连接 √

stmp服务器 mail.yuatom.com:25
用户名 my@yuatom.com
安全连接

https://www.ndchost.com//wiki/doku.php?id=mail/test-smtp-auth-telnet

firewall-cmd --zone=public --add-port=465/tcp --permanent
firewall-cmd reload