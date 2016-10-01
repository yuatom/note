# docker网络
##外部网络
容器公开端口并绑定到本地网络接口（通过run时的p/P选项），比如将容器的80端口绑定到本地其他端口。

##内部网络
在安装Docker时，会创建一个新的网络接口，docker0。每个Docker容器都会在这个接口上分配一个IP地址。
查看docker0接口信息（OS X系统需要进到虚拟机中查看）：

```sh
docker@default:~$ ip a show docker0
5: docker0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default
    link/ether 02:42:ea:0a:34:70 brd ff:ff:ff:ff:ff:ff
    inet 172.17.0.1/16 scope global docker0
       valid_lft forever preferred_lft forever
    inet6 fe80::42:eaff:fe0a:3470/64 scope link
       valid_lft forever preferred_lft forever
```
`172.17.0.1`为该网卡接口的网关。此外，还能看到其他一系列以`veth`开头的接口，这些是容器的接口，连接容器到主机。容器要进行网络连接时，先通过这些接口与主机的docker0连接。

```sh
veth4b0ad02 Link encap:Ethernet  HWaddr C6:1D:A5:60:DA:55
          inet6 addr: fe80::c41d:a5ff:fe60:da55/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:19 errors:0 dropped:0 overruns:0 frame:0
          TX packets:162 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:1989 (1.9 KiB)  TX bytes:11416 (11.1 KiB)        
```

可通过以下方法追踪容器的网络连接：

```sh
# 在容器内部，安装工具 traceroute
root@1b857d5f2e6a:/# apt-get -yqq update && apt-get install -yqq traceroute
# 追踪网络连接
root@1b857d5f2e6a:/# traceroute google.com
traceroute to google.com (159.106.121.75), 30 hops max, 60 byte packets
 1  172.17.0.1 (172.17.0.1)  0.032 ms  0.008 ms  0.007 ms
 2  10.0.2.2 (10.0.2.2)  0.141 ms  0.145 ms  0.154 ms
 3  * * *
 4  * * *
 5  * * *
 6  * * *
 7  * * *
 8  * * *
 9  221.179.54.145 (221.179.54.145)  110.378 ms  110.298 ms  110.210 ms
10  183.235.224.245 (183.235.224.245)  110.741 ms 183.235.225.1 (183.235.225.1)  110.500 ms 183.235.224.245 (183.235.224.245)  110.461 ms
11  * * *
12  * * *
13  * * *
...
```

容器地址的下一条是Docker主机的网关`172.17.0.1`。
容器要和外部网络进行通信，还需要配置Docker主机上的防火墙规则和NAT配置。

```sh
root@default:/home/docker# iptables -t nat -L -n
Chain PREROUTING (policy ACCEPT)
target     prot opt source               destination
DOCKER     all  --  0.0.0.0/0            0.0.0.0/0            ADDRTYPE match dst-type LOCAL

Chain INPUT (policy ACCEPT)
target     prot opt source               destination

Chain OUTPUT (policy ACCEPT)
target     prot opt source               destination
DOCKER     all  --  0.0.0.0/0           !127.0.0.0/8          ADDRTYPE match dst-type LOCAL

Chain POSTROUTING (policy ACCEPT)
target     prot opt source               destination
MASQUERADE  all  --  172.17.0.0/16        0.0.0.0/0
MASQUERADE  tcp  --  172.17.0.2           172.17.0.2           tcp dpt:80
MASQUERADE  tcp  --  172.17.0.3           172.17.0.3           tcp dpt:4567
MASQUERADE  tcp  --  172.17.0.4           172.17.0.4           tcp dpt:6379

Chain DOCKER (2 references)
target     prot opt source               destination
RETURN     all  --  0.0.0.0/0            0.0.0.0/0
DNAT       tcp  --  0.0.0.0/0            0.0.0.0/0            tcp dpt:32768 to:172.17.0.2:80
DNAT       tcp  --  0.0.0.0/0            0.0.0.0/0            tcp dpt:32769 to:172.17.0.3:4567
DNAT       tcp  --  0.0.0.0/0            0.0.0.0/0            tcp dpt:32770 to:172.17.0.4:6379
```
容器默认是无法访问的，需要打开端口将容器里的访问路由到Docker主机的端口上，即DNAT规则。如下，将Docker主机的32770端口映射到容器的6379。`172.17.0.4`为容器的的地址。

```sh
DNAT       tcp  --  0.0.0.0/0            0.0.0.0/0            tcp dpt:32770 to:172.17.0.4:6379
```


##run命令的--link选项，容器互联
容器间的连接，假设容器A中的程序要要访问容器B的某端口，可通过连接Docker主机分配给容器B的地址来连接，比如

```sh
DNAT       tcp  --  0.0.0.0/0            0.0.0.0/0            tcp dpt:32770 to:172.17.0.4:6379
```
中的172.17.0.4。此种方式需要将容器B的地址硬编码在A容器的配置中。但是每次容器启动时分配的地址都是不一样的，如果采用这种方式连接，需要在每次B容器启动时修改A容器的配置。

###创建容器连接
Docker提供了连接（link）功能，使得同个Docker中的容器可以连接起来。
`--link <containner name>:<alias>`，建立Docker内部连接，containner name所在容器作为子容器，子容器在启动（docker run）时无须对外部主机暴露端口，父容器（当前run的容器）可以直接访问子容器开放的端口（Dockerfile中EXPOSE的端口）。当Docker的守护进程启动时加上`--icc=false`时，容器之间的连接功能将被关闭。
下面使用连接功能与redis通信，其中redis容器在启动时并没有对外暴露端口。webapp容器通过连接功能与redis容器通信，并取别名为db。之后查看webapp中hosts文件的配置以及相应的环境变量，包括
>* 子容器的名字
>* 容器里运行的服务所使用的协议、IP和端口号
>* 容器里运行的不同服务所指定的协议、IP和端口号
>* 容器里由Docker设置的环境变量的值

```sh
# 启动redis容器，没有开放端口给外部
docker run -d --name redis jamtur01/redis

# 启动客户端容器，使用--link选项连接redis，别名为db；启动后直接进入到容器内部，而不是以daemon进程
docker run -p 4567 \
--name webapp --link redis:db -t -i \
-v $PWD/webapp:/opt/webapp jamtur01/sinatra \
/bin/bash
# 查看容器中hosts配置，redis、bd及redis容器的id都被动态映射到容器的地址上
root@178f7b424b0f:/# cat /etc/hosts
127.0.0.1	localhost
::1	localhost ip6-localhost ip6-loopback
fe00::0	ip6-localnet
ff00::0	ip6-mcastprefix
ff02::1	ip6-allnodes
ff02::2	ip6-allrouters
172.17.0.4	db ead67ec82269 redis
172.17.0.3	178f7b424b0f
# 查看环境变量，里面包含一些DB开头的子容器相关的环境变量
root@178f7b424b0f:/# env
HOSTNAME=178f7b424b0f
DB_NAME=/webapp/db
DB_PORT_6379_TCP_PORT=6379
TERM=xterm
DB_PORT=tcp://172.17.0.4:6379
DB_PORT_6379_TCP=tcp://172.17.0.4:6379
...
DB_PORT_6379_TCP_ADDR=172.17.0.4
DB_PORT_6379_TCP_PROTO=tcp
...
```

###在容器中使用连接





