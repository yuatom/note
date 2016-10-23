#ps&top&kill

##ps
该命令可以查看正在运行的进程以及运行的状态，进程是否结束，进程有没有僵死，哪些进程占用了过多的资源。

###选项

* -e，所有的process均显示出来；
* -A，与-e具有同样的效果；
* -a，显示和终端下的所有程序；
* -u，指定用户的所有进程，不提供用户列表时默认是当前登录用户；
* -x，显示无控制终端的进程；
* -au，显示较详细的信息；
* -aux，显示所有，包含其他使用者；
* -f，显示完整列表，以树状形式；
* -l，显示前台运行的进程



#### -aux

USER，进程所有者；
PID，进程ID；
%CPU，占用率；
%MEM，占用率；
VSZ，占用虚拟内存大小；
RSS，占用内存大小；
TTY，使用哪个tty；
STAT，进程状态；
START，启动进程的时间，
TIME，进程消耗CPU的时间；
COMMAND，进程的启动命令；


```sh
# 启动了nginx后台，有一个man在查看
[root@6224a0586831 nginx]# ps
  PID TTY          TIME CMD
   30 ?        00:00:00 bash
 8579 ?        00:00:00 ps

[root@6224a0586831 nginx]# ps -a
  PID TTY          TIME CMD
 8559 ?        00:00:00 man
 8569 ?        00:00:00 less
 8580 ?        00:00:00 ps


[root@6224a0586831 nginx]# ps -u
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.0  0.1 115392  3320 ?        Ss+  13:49   0:00 /bin/bash
root        30  0.0  0.1 115392  3416 ?        Ss   14:17   0:00 /bin/bash
root      7572  0.0  0.1 115392  3400 ?        Ss   15:02   0:00 /bin/bash
root      8559  0.0  0.1 119252  3208 ?        S+   15:07   0:00 man ps
root      8569  0.0  0.1 110260  2224 ?        S+   15:07   0:00 less -s
root      8585  0.0  0.1 151040  3824 ?        R+   15:11   0:00 ps -u


[root@6224a0586831 nginx]# ps -x
  PID TTY      STAT   TIME COMMAND
    1 ?        Ss+    0:00 /bin/bash
   30 ?        Ss     0:00 /bin/bash
 7572 ?        Ss     0:00 /bin/bash
 8545 ?        Ss     0:00 nginx: master process /usr/local/openresty/nginx/sbin/nginx -p /usr/local/openresty/nginx/
 8559 ?        S+     0:00 man ps
 8569 ?        S+     0:00 less -s
 8584 ?        R+     0:00 ps -x


[root@6224a0586831 nginx]# ps -au
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.0  0.1 115392  3320 ?        Ss+  13:49   0:00 /bin/bash
root        30  0.0  0.1 115392  3416 ?        Ss   14:17   0:00 /bin/bash
root      7572  0.0  0.1 115392  3400 ?        Ss   15:02   0:00 /bin/bash
root      8559  0.0  0.1 119252  3208 ?        S+   15:07   0:00 man ps
root      8569  0.0  0.1 110260  2224 ?        S+   15:07   0:00 less -s
root      8581  0.0  0.1 151040  3764 ?        R+   15:09   0:00 ps -au


[root@6224a0586831 nginx]# ps -ax
  PID TTY      STAT   TIME COMMAND
    1 ?        Ss+    0:00 /bin/bash
   30 ?        Ss     0:00 /bin/bash
 7572 ?        Ss     0:00 /bin/bash
 8545 ?        Ss     0:00 nginx: master process /usr/local/openresty/nginx/sbin/nginx -p /usr/local/openresty/nginx/
 8546 ?        S      0:00 nginx: worker process
 8559 ?        S+     0:00 man ps
 8569 ?        S+     0:00 less -s
 8586 ?        R+     0:00 ps -ax


[root@6224a0586831 nginx]# ps -ux
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.0  0.1 115392  3320 ?        Ss+  13:49   0:00 /bin/bash
root        30  0.0  0.1 115392  3416 ?        Ss   14:17   0:00 /bin/bash
root      7572  0.0  0.1 115392  3400 ?        Ss   15:02   0:00 /bin/bash
root      8545  0.0  0.0  55804  1044 ?        Ss   15:05   0:00 nginx: master process /usr/local/openresty/nginx/sbin/nginx -p /usr/local/openresty/nginx/
root      8559  0.0  0.1 119252  3208 ?        S+   15:07   0:00 man ps
root      8569  0.0  0.1 110260  2224 ?        S+   15:07   0:00 less -s
root      8587  0.0  0.1 151040  3828 ?        R+   15:13   0:00 ps -ux


[root@6224a0586831 nginx]# ps -aux
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.0  0.1 115392  3320 ?        Ss+  13:49   0:00 /bin/bash
root        30  0.0  0.1 115392  3416 ?        Ss   14:17   0:00 /bin/bash
root      7572  0.0  0.1 115392  3400 ?        Ss   15:02   0:00 /bin/bash
root      8545  0.0  0.0  55804  1044 ?        Ss   15:05   0:00 nginx: master process /usr/local/openresty/nginx/sbin/nginx -p /usr/local/openresty/nginx/
nobody    8546  0.0  0.1  56156  3076 ?        S    15:05   0:00 nginx: worker process
root      8559  0.0  0.1 119252  3208 ?        S+   15:07   0:00 man ps
root      8569  0.0  0.1 110260  2224 ?        S+   15:07   0:00 less -s
root      8582  0.0  0.1 151040  3800 ?        R+   15:09   0:00 ps -aux
```


##top
显示系统当前的进程和其他状态。和ps的区别是，top是一个动态的显示过程。

top [-d 数字] 

###选项

* -d，后面接秒数，即页面刷新的时间间隔，默认是5；
* -p，制定某些PID

###指令

* ?/h，显示指令列表，按q或ESC退出；
* P，以CPU的使用资源排序显示；
* M，以Memory的使用资源排序显示；
* N，以PID排序；
* m，切换Memory的显示信息；

```sh
[root@6224a0586831 /]# top
top - 15:35:51 up  1:50,  0 users,  load average: 0.00, 0.00, 0.00
Tasks:   6 total,   1 running,   5 sleeping,   0 stopped,   0 zombie
%Cpu(s):  2.5 us,  0.6 sy,  0.0 ni, 96.7 id,  0.2 wa,  0.0 hi,  0.0 si,  0.0 st
KiB Mem :  2048660 total,   178560 free,    62212 used,  1807888 buff/cache
KiB Swap:   987960 total,   987960 free,        0 used.  1603668 avail Mem

  PID USER      PR  NI    VIRT    RES    SHR S  %CPU %MEM     TIME+ COMMAND
    1 root      20   0  115392   3320   3048 S   0.0  0.2   0:00.03 bash
   30 root      20   0  115392   3416   3000 S   0.0  0.2   0:00.35 bash
 7572 root      20   0  115392   3400   3016 S   0.0  0.2   0:00.03 bash
 8545 root      20   0   55804   1044     12 S   0.0  0.1   0:00.00 nginx
 8546 nobody    20   0   56156   3076   1812 S   0.0  0.2   0:00.00 nginx
 8601 root      20   0  155460   4152   3640 R   0.0  0.2   0:00.00 top


# M
top - 15:36:28 up  1:50,  0 users,  load average: 0.00, 0.00, 0.00
Tasks:   6 total,   1 running,   5 sleeping,   0 stopped,   0 zombie
%Cpu(s):  0.0 us,  0.0 sy,  0.0 ni,100.0 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st
KiB Mem :  2048660 total,   177908 free,    62812 used,  1807940 buff/cache
KiB Swap:   987960 total,   987960 free,        0 used.  1603016 avail Mem

  PID USER      PR  NI    VIRT    RES    SHR S  %CPU %MEM     TIME+ COMMAND
 8601 root      20   0  155464   4160   3640 R   0.0  0.2   0:00.01 top
   30 root      20   0  115392   3416   3000 S   0.0  0.2   0:00.35 bash
 7572 root      20   0  115392   3400   3016 S   0.0  0.2   0:00.03 bash
    1 root      20   0  115392   3320   3048 S   0.0  0.2   0:00.03 bash
 8546 nobody    20   0   56156   3076   1812 S   0.0  0.2   0:00.00 nginx
 8545 root      20   0   55804   1044     12 S   0.0  0.1   0:00.00 nginx


```

###显示信息

```sh
[root@6224a0586831 /]# top
# 	目前的时间	开机至今的时间		已经登录用户数		系统在1，5，15分钟的平均工作负载
top - 15:35:51 up  1:50,  0 users,  load average: 0.00, 0.00, 0.00
# 	进程的状态	进程总量		运行的进程	睡眠的进程	停止的进程	僵尸进程
Tasks:   6 total,   1 running,   5 sleeping,   0 stopped,   0 zombie
# 	CPU整理负载
%Cpu(s):  2.5 us,  0.6 sy,  0.0 ni, 96.7 id,  0.2 wa,  0.0 hi,  0.0 si,  0.0 st
# 	内存负载
KiB Mem :  2048660 total,   178560 free,    62212 used,  1807888 buff/cache
KiB Swap:   987960 total,   987960 free,        0 used.  1603668 avail Mem
  PID USER      PR  NI    VIRT    RES    SHR S  %CPU %MEM     TIME+ COMMAND
    1 root      20   0  115392   3320   3048 S   0.0  0.2   0:00.03 bash
   30 root      20   0  115392   3416   3000 S   0.0  0.2   0:00.35 bash
 7572 root      20   0  115392   3400   3016 S   0.0  0.2   0:00.03 bash
 8545 root      20   0   55804   1044     12 S   0.0  0.1   0:00.00 nginx
 8546 nobody    20   0   56156   3076   1812 S   0.0  0.2   0:00.00 nginx
 8601 root      20   0  155460   4152   3640 R   0.0  0.2   0:00.00 top


# PR，Priority缩写，优先级，越小越早被执行
# NI，Nice值，和优先级有关，越小越早被执行
# TIME+，CPU使用时间的叠加
```


##kill
用来终止指定进程的运行。
kill[参数][进程号]
其中进程号可以通过ps/pidof/pstree/top等命令获得。


###参数

* -l，显示信号列表；
* -a，当处理当前进程时，不限制命令名和进程号的对应关系；
* -s，发送指定信号，如：kill -s KILL PID；
* -信号名称，发送指定信号，如：kill -KILL PID；
* -信号数，发送指定信号，如：kill -9 PID；
* -u，指定用户；

不指定信号的情况下，默认发出终止（15）信号。


* HUP    1    终端断线
* INT     2    中断（同 Ctrl + C）
* QUIT    3    退出（同 Ctrl + \）
* TERM   15    终止
* KILL    9    强制终止
* CONT   18    继续（与STOP相反， fg/bg命令）
* STOP    19    暂停（同 Ctrl + Z）






pstree [-AUup]
-A ：各程序树之间的连接以 ASCII 字符来连接；
-U ：各程序树之间的连接以万国码的字符来连接。在某些终端接口下可能会有错误；
-p ：并同时列出每个 process 的 PID；
-u ：并同时列出每个 process 的所属帐号名称





































