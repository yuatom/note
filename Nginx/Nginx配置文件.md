# Nginx配置文件

##1、例子

```shell
user nobody;

worker_processes    8;
error_log   /var/log/nginx/error.log    error;

#pid    logs/nginx.pid;

events {
    use epoll;
    worker_connections  50000;
}

http {
    
    include         mime.types;
    default_type    application/octet-stream;
    
    log_format  main    '$remote_add [$time_local] "$request" '
                        '$status $bytes_sent "$http_referer" '
                        '"$http_user_agent" "$http_x_forwarded_for"';
                        
    access_log  logs/access.log     main buffer=32k;
}
```

##2、语法
###2.1、块配置
Nginx中的块配置项有：`events`、`http`、`server`、`location`、`upstream`，通过`{}`将块配置项的配置包括起来。块配置项可以嵌套，当内部和外部存在同一配置项时，对于内部的处理模块中，内部的配置会覆盖外部的。

```shell
events {
...
}

http {
    upstream backend {
        server 127.0,0.1:8080;
    }
    
    gzip on;
    server {
        ...
        location /webstatic {
                gzip off;
        }
    }
}
```

###2.2、配置项语法

```shell
item    value1  value2  ...;
```
如果配置项值中包括语法符号，比如空格符，那么需要使用单引号或双引号括住该值：

```
log_format  main    '$remote_add [$time_local] "$request" '
```

##3、配置项讲解
>* 用于调试、定位问题的配置项
>* 正常运行的必备配置项
>* 优化性能的配置项
>* 事件类配置项

###3.1、用于调试、定位问题的配置项
####3.1.1、deamon，是否以守护进程方式运行

```shell
# 格式
deamon  on|off;
# 默认
deamon on;
```
守护进程，即启动后脱离终端并在后台运行，运行过程中的信息不会输出到终端上。

####3.1.2、master_process，是否以master/worker方式工作

```shell
# 格式
master_process  on|off;
# 默认
master_process  on;
```
如果该选项取值为`off`，关闭了master/worker工作方式，则不会fork出worker子进程来处理请求。

####3.1.3、error_log，日志路径及级别

```shell
# 格式
error_log   /path/file  level;
# 默认
error_log   logs/error.log  error;
```
`/path/file`最好放在一个磁盘空间比较大位置；当取值为`/dev/null`时为不输出日志，这是关闭error日志的唯一方式；当取值为`stderr`时日志会输出到标准错误文件中。
`level`的取值范围是：`debug`、`info`、`notice`、`warn`、`error`、`crit`、`alert`、`emerg`。从左到右级别一次增大。
> 设置以上配置时，必须在`configure`时加入`--with-debug`选项。

####3.1.4、debug_points，处理调试点的方式

```shell
# 格式
debug_points stop|abort
```
Nginx中在一些关键的错误逻辑中设置了调试点。当`debug_points = stop`时，遇到这些调试点时会发出`SIGSTOP`信号以用于调试；当`debug_points = abort`时，则会产生一个`coredump`文件。
> 通常不会使用这个配置项。

####3.1.5、debug_connection，仅对指定的客户端输出debug日志

```shell
# 格式
debug_connection [IP|CIDR]
```
该配置属于事件类配置，需要在`events {}`块中配置才生效。

```shell
events {
    debug_connection 10.224.66.14;
    debug_connection 10.224.66.0/24;
}
```
> 设置以上配置时，必须在`configure`时加入`--with-debug`选项。

####3.1.6、worker_rlimit_core，限制coredump核心转储文件大小

```shell
# 格式
worker_rlimit_core  size;
```
`核心转储`：Linux系统中如果进程发生错误或受到信号而终止，会将该进程执行时的内存内容（核心映像）写入到一个文件（core文件）。
当Nginx进行出现一些非法操作导致进程被操作系统强制关闭时，会生成核心转储core文件，可以从该文件中获取当时的堆栈和寄存器等信息。
core文件中通常有很多用户不一定需要的信息，如果不加以限制一个core文件可能会达到几GB，因此有需要时可以使用该配置限制大小。

####3.1.7、working_directory，coredump文件目录

```shell
# 格式
working_directory path;
```
需保证worker进程有权限向设置的目录写入文件。

###3.2、正常运行的必备配置项
####3.2.1、env，定义环境变量

```shell
# 格式
env VAR|VAR=VALUE
```
可设置操作系统上的环境变量。

####3.2.2、include，潜入其他文件

```shell
# 格式
include /path/file;
```
将其他配置文件引入到当前的配置文件中。
参数的值可以是一个明确的文件名也可以是一个含有通配符的文件名。

```shell
include     mime.types;
include     vhost/*.conf;
```

####3.2.3、pid，pid文件路径

```shell
# 格式
pid path/file;
# 默认
pid logs/nginx.pid;
```
保存master进程ID的pid文件存放路径。默认与`configure`执行时的参数`--pid-path`所指定的路径相同，也可以随时改。要确保Nginx有权在相应的目标中创建pid文件。

####3.3.4、user，worker进程运行的用户及用户组

```shell
# 格式
user username [groupname];
# 默认
user nobody nobody;
```
用于设置master进程启动后，fork出的worker进程在哪个用户和用户组下。
如果在`configure`时指定了`--user=username`和`--group=groupname`，则此时配置文件中将使用这两个参数的值。

####3.3.5、worker_rlimit_nofile，worker可以打开的最大文件句柄数

```shell
# 格式
worker_rlimit_nofile    limit;
```
设置一个worker进程可以打开的最大文件句柄数。

####3.3.6、worker_rlimit_sigpending，限制信号队列

```shell
# 格式
worker_rlimit_sigpending    limit;
```
用户发往Nginx的信号队列的大小，当队列满了，用户再发送的信号会被丢弃。

###3.3、优化性能的配置项

####3.3.1、worker_processes，worker进程数

```shell
# 格式
worker_processes    number;
# 默认
worker_processes    1;
```
设置master/worker方式下worker进程的个数。
每个worker进程都是单线程的进程。多worker进程可以充分利用多核系统架构。但若worker进程的数量多于CPU内核数，那么会增大进程间切换带来的消耗。

####3.3.2、worker_cpu_affinity，绑定worker进程到指定cpu内核

```shell
# 格式
worker_cpu_affinity cpumask [cpumask...]
```
将worker进程和cpu内核绑定能够避免多个worker进程争抢同一个CPU而出现的同步问题。

```shell
worker_processes    4;
worker_cpu_affinity 1000 0100 0010 0001;
```

####3.3.3、worker_priority，worker进程优先级

```shell
# 格式
worker_priority nice;
# 默认
worker_priority 0;
```
Linux系统中当多个进程处于可执行状态时，将按照进程的优先级来决定本次内核选择哪一个进程执行。

####3.3.4、timer_resolution，gettimeofday执行频率

```shell
# 格式
timer_resolution    t;
```
gettimeofday：每次内核的事件调用（epoll、select、poll、kqueue等）返回时，会执行一次gettimeofday来实现用内核的时钟来更新Nginx中的缓存时钟。
早期的Linux内核执行gettimeofday的代价不小，所以当需要调低调用频率时，可使用该配置。

###3.4、事件类配置项

####3.4.1、accept_mutex，是否打开accept锁

```shell
# 格式
accept_mutex [on|off];
# 默认
accept_mutex on;
```
accept_mutex是Nginx的负载均衡锁，能够让多个worker进程轮流地、序列化地与新的客户端建立TCP连接。当一个worker进程上的连接达到`worker_connections`的7/8时，新的TCP连接到该进程的机会将大大减小。
关闭该锁时会减少TCP连接建立的耗时，但会使得worker进程之间负载不均衡。

####3.4.2、lock_file，lock文件路径

```shell
# 格式
lock_file path/file;
# 默认
lock_file logs/nginx.lock;
```
当编译程序、操作系统架构等因素导致Nginx不支持院子锁，会通过文件锁来实现accept锁。

####3.4.3、accept_mutex_delay，使用accept锁后到真正建立连接之间的延迟时间

```shell
# 格式
accept_mutex_delay Nms;
# 默认
accept_mutex_delay 500ms;
```
启用accept锁后，同一个时间只有一个worker进程能够取到accept锁，如果取不到会立刻返回，然后至少等accept_mutex_delay定义的时间间隔后才能再次试图取锁。

####3.4.4、multi_accept，批量建立新连接

```shell
# 格式
multi_accept [on|off];
# 默认
multi_accept off;
```
当事件模型通知有新连接时，尽可能地对本次调度中客户端发起的所有TCP请求都建立连接。

####3.4.5、use，选择事件模型

```shell
# 格式
use [kqueue|rtsing|epoll|/dev/poll|select|poll|eventport];
# 默认
Nginx会自动使用最适合的事件模型
```
Linux系统中可选择的有epoll、select、poll三种。

####3.4.6、worker_connections，每个worker进程可以同时处理的最大连接数

```shell
# 格式
worker_connections number;
```




