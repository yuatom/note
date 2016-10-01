# crontab
crontab -l|-r|-e|-i [username]
   -l 显示用户的crontab文件的内容
   -i 删除crontab文件时给出提示
   -r 从crontab目录中删除用户的crontab文件
   -e 编辑用户的crontab文件
  
##格式

```sh
 ~ *　　*　　*　　*　　*　　command
 # 分　 时　 日　 月　 周　 命令
```
>* 第1列表示分钟1～59 每分钟用*或者 */1表示
>* 第2列表示小时1～23(0表示0点)
>* 第3列表示日期1～31
>* 第4列表示月份1～12
>* 第5列标识号星期0～6(0表示星期天)
>* 第6列要运行的命令

其中`日月`和`月星期`是 `OR`关系，即上面的语句会在每一年的9月27日或者是每一年的9月的每一个周日触发。如果这条命令的目的是指执行一次，但由于后面参数的`OR`关系，如果不及时清除该命令，会导致后来的每一年的九月份的每一个周日都会触发该事件。

```sh
# 例子
30 21 * * * /usr/local/apache/bin/apachectl restart
#上面的例子表示每晚的21:30重启apache。
  
45 4 1,10,22 * * /usr/local/apache/bin/apachectl restart
#上面的例子表示每月1、10、22日的4 : 45重启apache。
  
10 1 * * 6,0 /usr/local/apache/bin/apachectl restart
#上面的例子表示每周六、周日的1 : 10重启apache。
  
0,30 18-23 * * * /usr/local/apache/bin/apachectl restart
#上面的例子表示在每天18 : 00至23 : 00之间每隔30分钟重启apache。
  
0 23 * * 6 /usr/local/apache/bin/apachectl restart
#上面的例子表示每星期六的11 : 00 pm重启apache。
  
* */1 * * * /usr/local/apache/bin/apachectl restart
#每一小时重启apache
  
* 23-7/1 * * * /usr/local/apache/bin/apachectl restart
#晚上11点到早上7点之间，每隔一小时重启apache
  
#每月每天每小时的第 0 分钟执行一次 /bin/ls :
0 * * * * /bin/ls

#在 12 月内, 每天的早上 6 点到 12 点中，每隔 20 分钟执行一次 /usr/bin/backup :
*/20 6-12 * 12 * /usr/bin/backup

#周一到周五每天下午 5:00 寄一封信给 ranger@domain.name :
0 17 * * 1-5 mail -s "hi" ranger@domain.name < /tmp/maildata

#每月每天的午夜 0 点 20 分, 2 点 20 分, 4 点 20 分....执行 echo "haha"
20 0-23/2 * * * echo "haha"

#晚上11点到早上8点之间每两个小时，早上8点
0 23-7/2，8 * * * date
```

##权限
控制可以创建crontab任务的用户，`/etc/cron.allow`和`/etc/cron.deny`文件。
先检查`/etc/cron.allow`，如果该文件有标识出哪些用户可以创建，则以该文件来控制可以创建的用户。
如果`/etc/cron.allow`不存在，则检查`/etc/cron.deny`文件，检查哪些用户不被允许。

##文件

###/etc/crontab
该文件保护部分配置及定时命令，cron会每分钟去读取一次该文件。
在crontab的脚本中可以指定部分配置。

* SHELL，使用哪种shell
* PATH，可执行文件的搜寻路径
* MAILTO，如果有stdout，将数据以邮件发送给该用户

```sh
root@scotchbox:~# cat /etc/crontab
# /etc/crontab: system-wide crontab
# Unlike any other crontab you don't have to run the `crontab'
# command to install the new version when you edit this file
# and files in /etc/cron.d. These files also have username fields,
# that none of the other crontabs do.

SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
MAILTO=root

# Example of job defintion:
# .---------------- minute	(0-59)
#

# m h dom mon dow user 	command
17 *   	* * *  	root    cd / && run-parts --report /etc/cron.hourly
25 6   	* * *  	root   	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.daily )
47 6   	* * 7  	root   	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.weekly )
52 6   	1 * *  	root   	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.monthly )
#
```

###/etc/cron.d/*
/etc/cron.d/放置crontab脚本，在这些脚本中，同样有可以指定部分配置和写入cron任务。

```sh
cat /etc/cron.d/0hourly
$ Run hourly jobs
SHELL=/bin/bash
PATH=/sbin:/bin:/usr/sbin:/usr/bin
MATILTO=root

# run-parts，一个可执行的脚本在五分钟内随机选一个时间去执行/etc/cron.hourly目录内所有的文件
01 * * * * root run-parts /etc/cron.hourly
```

如果自己有需要每小时执行一次的任务，可以直接将指令链接到/etc/cron.hourly/目录下，该指令就会被crond在每小时的1分开始后的五分钟内的一个随机时间点来执行。
此外，在`/etc/`目录下，还有`/etc/cron.daily/`，`/etc/cron.weekly`，`/etc/cron.monthly/`文件夹。


###/etc/spool/cron/*
用户添加cron任务时，会被添加到`/etc/spoll/cron/username`文件中，该文件每分钟被cron每分钟扫一次。
此外还可以通过`crontab -e`来编辑上述文件。














































