#install

##安装
tar zxvf redis-x.x.x.tar.gz
cd redis-x.x.x
make
make install

##启动

###后台启动
./redis-server &

###指定配置文件启动
redis-server ./redis.conf

###使用redis启动脚本设置开机自启动
启动脚本，redis-x.x.x/utils/redis_init_script

```shell
#!/bin/sh
#
# Simple Redis init.d script conceived to work on Linux systems
# as it does use of the /proc filesystem.

# 服务开放端口
REDISPORT=6379
# 服务的启动命令
EXEC=/usr/local/bin/redis-server
# 客户端的启动命令
CLIEXEC=/usr/local/bin/redis-cli

# pid的保存文件
PIDFILE=/var/run/redis_${REDISPORT}.pid
# 开机启动时的配置文件地址
CONF="/etc/redis/${REDISPORT}.conf"

case "$1" in
    start)
        if [ -f $PIDFILE ]
        then
                echo "$PIDFILE exists, process is already running or crashed"
        else
                echo "Starting Redis server..."
                $EXEC $CONF
        fi
        ;;
    stop)
        if [ ! -f $PIDFILE ]
        then
                echo "$PIDFILE does not exist, process is not running"
        else
                PID=$(cat $PIDFILE)
                echo "Stopping ..."
                $CLIEXEC -p $REDISPORT shutdown
                while [ -x /proc/${PID} ]
                do
                    echo "Waiting for Redis to shutdown ..."
                    sleep 1
                done
                echo "Redis stopped"
        fi
        ;;
    *)
        echo "Please use start or stop as first argument"
        ;;
esac

```

> 由启动脚本的内容可知，启动脚本会从`/etc/redis/`目录中读取指定端口号的配置文件，因此需要创建配置文件；
> 再将启动文件复制到/etc/init.d/目录中；


```shell
# 创建配置目录
[root@a11adc88a32c redis-3.2.4]# mkdir /etc/redis
# 拷贝配置文件
[root@a11adc88a32c redis-3.2.4]# cp redis.conf /etc/redis/6379.conf

[root@a11adc88a32c redis-3.2.4]# chkconfig redisd on
service redisd does not support chkconfig
# 报错，需要在启动脚本中加入chkconfig的启动级别和启动退出的顺序
```

因为每个chkconfig启动脚本在启动脚本中加入两行或更多注释：

```shell
# chkconfig:   2345 90 10
# description:  .....
```
第一行告诉chkconfig缺省启动的运行级以及启动和停止优先级；
第二行对服务进行注释；

```shell
#!/bin/sh
# chkconfig:   2345 90 10
# description:  Redis is a persistent key-value database
# Simple Redis init.d script conceived to work on Linux systems
# as it does use of the /proc filesystem.
#
```

> 2345：表示在什么级别下回启动，默认是2345，可以用-表示；
>* 等级0表示：表示关机
>* 等级1表示：单用户模式
>* 等级2表示：无网络连接的多用户命令行模式
>* 等级3表示：有网络连接的多用户命令行模式
>* 等级4表示：不可用
>* 等级5表示：带图形界面的多用户模式
>* 等级6表示：重新启动

> 90：表示启动顺序，第90个启动
> 10：退出顺序，第10个退出


修改启动脚本后启动

```shell
# 启动服务
[root@a11adc88a32c ~]# chkconfig redisd on
[root@a11adc88a32c ~]# service redisd start
```
会发现此时redis server在前台运行，因此需要修改启动脚本：

```shell
# 在下面一行后面加上&
EXEC $CONF
# 即为下面这行
$EXEC $CONF &
```

再执行开始命令：

```shell
[root@a11adc88a32c ~]# chkconfig redisd on
[root@a11adc88a32c ~]# service redisd start
```






























