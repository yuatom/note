systemd, systemctl

systemctl [command] [unit]
command 主要有：
start ：立刻启动后面接的 unit
stop ：立刻关闭后面接的 unit
restart ：立刻关闭后启动后面接的 unit，亦即执行 stop 再 start 的意思
reload ：不关闭后面接的 unit 的情况下，重新载入配置文件，让设置生效
enable ：设置下次开机时，后面接的 unit 会被启动
disable ：设置下次开机时，后面接的 unit 不会被启动
status ：目前后面接的这个 unit 的状态，会列出有没有正在执行、开机默认执行否、登录等信息等！
is-active ：目前有没有正在运行中
is-enable ：开机时有没有默认要启用这个 unit

范例一：看看目前 atd 这个服务的状态为何？
[root@study ~]# systemctl status atd.service
atd.service - Job spooling tools
Loaded: loaded （ /usr/lib/systemd/system/atd.service; enabled）
Active: active （ running） since Mon 2015-08-10 19:17:09 CST; 5h 42min ago
Main PID: 1350 （ atd）
CGroup: /system.slice/atd.service
└─
1350 /usr/sbin/atd -f
Aug 10 19:17:09 study.centos.vbird systemd[1]: Started Job spooling tools.
# 重点在第二、三行喔～
# Loaded：这行在说明，开机的时候这个 unit 会不会启动，enabled 为开机启动，disabled 开机不会启动
# Active：现在这个 unit 的状态是正在执行 （ running） 或没有执行 （ dead）
# 后面几行则是说明这个 unit 程序的 PID 状态以及最后一行显示这个服务的登录文件信息！
# 登录文件信息格式为：“时间” “讯息发送主机” “哪一个服务的讯息” “实际讯息内容”
# 所以上面的显示讯息是：这个 atd 默认开机就启动，而且现在正在运行的意思！
范例二：正常关闭这个 atd 服务
[root@study ~]# systemctl stop atd.service
[root@study ~]# systemctl status atd.service
atd.service - Job spooling tools
Loaded: loaded （ /usr/lib/systemd/system/atd.service; enabled）
Active: inactive （ dead） since Tue 2015-08-11 01:04:55 CST; 4s ago
Process: 1350 ExecStart=/usr/sbin/atd -f $OPTS （ code=exited, status=0/SUCCESS）
Main PID: 1350 （ code=exited, status=0/SUCCESS）
Aug 10 19:17:09 study.centos.vbird systemd[1]: Started Job spooling tools.
Aug 11 01:04:55 study.centos.vbird systemd[1]: Stopping Job spooling tools...
Aug 11 01:04:55 study.centos.vbird systemd[1]: Stopped Job spooling tools.
# 目前这个 unit 下次开机还是会启动，但是现在是没在运行的状态中！同时，
# 最后两行为新增加的登录讯息，告诉我们目前的系统状态喔！



unit相关
[root@study ~]# systemctl [command] [--type=TYPE] [--all]
command:
list-units ：依据 unit 列出目前有启动的 unit。若加上 --all 才会列出没启动的。
list-unit-files ：依据 /usr/lib/systemd/system/ 内的文件，将所有文件列表说明。
--type=TYPE：就是之前提到的 unit type，主要有 service, socket, target 等


target相关
[root@study ~]# systemctl [command] [unit.target]
选项与参数：
command:
get-default ：取得目前的 target
set-default ：设置后面接的 target 成为默认的操作模式
isolate ：切换到后面接的模式
show  ：显示默认设置值

systemctl poweroff 系统关机
systemctl reboot 重新开机
systemctl suspend 进入暂停模式
systemctl hibernate 进入休眠模式
systemctl rescue 强制进入救援模式
systemctl emergency 强制进入紧急救援模式



查看服务依赖
systemctl list-dependencies [unit] [--reverse]
选项与参数：
--reverse ：表示谁在依赖这个unit，不带该参数时表示这个unit依赖谁



service类型服务配置相关
/usr/lib/systemd/system/vsftpd.service：官方释出的默认配置文件；
/etc/systemd/system/vsftpd.service.d/custom.conf：在 /etc/systemd/system 下面创建与
配置文件相同文件名的目录，但是要加上 .d 的扩展名。然后在该目录下创建配置文件即
可。另外，配置文件最好附文件名取名为 .conf 较佳！ 在这个目录下的文件会“累加其他
设置”进入 /usr/lib/systemd/system/vsftpd.service 内喔！
/etc/systemd/system/vsftpd.service.wants/*：此目录内的文件为链接文件，设置相依服
务的链接。意思是启动了 vsftpd.service 之后，最好再加上这目录下面建议的服务。
/etc/systemd/system/vsftpd.service.requires/*：此目录内的文件为链接文件，设置相依
服务的链接。意思是在启动 vsftpd.service 之前，需要事先启动哪些服务的意思。

余旭东  22:03:59
运行两个vsftpd

1 创建新的服务
创建/etc/vsftpd/vsftpd2.conf文件，修改监听字段；
创建/usr/lib/systemd/system/vsftpd2.service文件，修改加载的配置文件；
systemctl daemon-reload，重新加载systemd服务，读取刚刚创建的配置文件，读取新的服务；
systemctl restart vsftpd.service vsftpd2.service，重启服务；
systemctl enable vsftpd.service vsftpd2.service，启用服务，开机启动；

2 使用@服务语法
cat /usr/lib/systemd/system/vsftpd@.service，查看配置文件@的读取规则；
ExecStart=/usr/sbin/vsftpd /etc/vsftpd/%i.conf，%i.conf表示配置文件以@后面的字符串+.conf命名；
创建/etc/vsftpd/vsftpd2.conf文件，修改监听字段；
systemctl start vsftpd@vsftpd2.service，启动@服务，回去查找/etc/vsftpd/vsftpd2.conf文件；
systemctl status vsftpd@vsftpd2.service，查看服务状态；