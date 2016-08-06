# Http模块的基础配置

##1、例子
一个http中可以包含多个server块和location块。
http中的配置项大概可分为以下八种类型：
>* 虚拟主机与请求的分发
>* 文件路径的定义
>* 内存及磁盘资源的分配
>* 网络连接的设置
>* MIME类型的设置
>* 对客户端请求的限制
>* 文件操作的优化
>* 对客户端请求的特殊处理

```shell
http{
    gzip    on;
    
    upstream {
        ...
    }
    ...
    server {
        listen localhost:80;
        ...
        location /webstatic {
            if ... {
                ...
            }
            root    /opt/webresource;
            ...
        }
        
        location ~* .(jpg|jpeg|png|jpe|gif)$ {
            ...
        }
    }
    
    server{
        ...
    }
}
```

##2、虚拟主机与请求分发
###2.1、listen，监听端口
位置：server

```shell
# 格式
listen addredd:port [ default(deprecated in 0.8.21) | default_server |[ backlog=num | rcvbuf=size | sndbuf=size | accept_filter=filter | deferred |bind | ipv6only=[on|off] | ssl]];
# 默认
listen 80;
```
配置监听端口的方式，可以只加IP地址、端口或主机名。

```shell
listen 127.0.0.1:8080;
listen 127.0.0.1;   # 不加端口时默认监听80端口
listen 8000;
listen *:8000;
listen localhost:8000;

listen 443 defalut_server ssl;
listen 127.0.0.1 default_server accept_filter=dataready backlog=1024;
```

####参数定义
>* default，将所在的server作为web服务的默认server块，如果没设置则取配置文件中第一个server作为默认的server块；
>* default_server，同上；
>* backlog=num，TCP中backlog队列的大小，默认-1，即不设置。在TCP建立三次握手过程中，还没有被进程处理监听句柄的请求将被放到backlog队列中。当backlog队列已满，还有新的客户端视图通过三次握手建立TCP连接时，将会建立失败；
>* rcvbuf=size，设置监听句柄的SO_RCVBUF参数；
>* sndbuf=size，设置监听句柄的SO_SNDBUF参数；
>* accept_filter，设置accept过滤器，只对FreeBSD操作系统有效；
>* deferred，该参数使得在用户发起建立连接请求并且完了TCP三次握手时内核也不会为这个请求调度worker进程来处理，只有在用户真正发送请求数据时（内核已经在网卡中收到请求数据包）才唤醒worker进程来处理这个连接。适合在大并发的情况减轻worker进程的负担；
>* bind，绑定当前端口/地址对；
>* ssl，在当前监听的端口上建立的连接必须基于SSL协议。

###2.2、server_name，主机名
位置：server

```shell
# 格式
server_name name [...];
# 默认
server_name "";
```
该配置项后面可跟多个主机名：

```shell
server_name www.testweb.com download.testweb.com
```
在开始处理http请求时，会取出请求头header中的Host，拿这个Host与每个server块中的server_name进行匹配，以此决定由哪一个server块来处理这个请求。当Hos匹配到多个server块的server_name时，会根据匹配的优先级来决定处理的server。
优先级顺序：
1) 所有字符串完全匹配的server_name；
2) 通配符在前面的server_name，如：\*.testweb.com；
3) 通配符在后面的server_name，如：www.testweb.\*;
4) 通过正则匹配到的。

如果Host与所有的server_name匹配不上，则以下面的顺序来选择：
1) listen配置项后加入[default|default_server]的server块；
2) 匹配listen端口的第一个server块。

> 如果配置为`server_name ""`则表示匹配没有Host这个Http头部的请求。

###2.3、server_names_hash_bucket_size，散列存储server_name的大小
位置：http/server/location

```shell
# 格式
server_name_hash_bucket_size size;
# 默认
server_name_hash_bucket_size 32|64|128;
```
Nginx使用散列表存储server_name来寻找匹配的速度，该参数设置每个散列桶占用的内存大小。

###2.4、server_names_hash_max_size，散列server_name的最大值
位置：http/server/location

```shell
# 格式
server_names_hash_max_size size;
# 默认
server_names_hash_max_size 512;
```
该参数会影响到散列表的冲突率。该值越大，消耗的内存就越多，但散列key的冲突率则会减低；反之该值越小消耗内存越小冲突率会增加。

###2.5、server_name_in_redirect，重定向主机名的处理
位置：http/server/location

```shell
# 格式
server_name_in_redirect on|off;
# 默认
server_name_in_redirect on;
```
该配置需要配合server_name使用。
该配置打开后会使用server_name配置的第一个主机名代替原先请求中的Host头部。

###2.6、location，匹配处理location块
位置：server

```shell
# 格式
location [=|~|~*|^~|@] /uri/ {...}
```
第一个参数指定后面uri的匹配规则：
>* =，表示完全匹配，如`location = / {}`只处理请求是`/`的请求；
>* ~，字母大小写敏感；
>* ~*，忽略字母大小写；
>* ^~，只匹配前半部分，如`location ^~ /images/ {}`，以/images/开始的请求都会被该location处理；
>* @，仅对于Nginx内部请求直接的重定向，不直接处理用户请求；

第二参数是要匹配请求的uri，取值可以包括正则表达式

```shell
location ~* .(jpg|jpeg|png|jpe|gif)$ {
  ...
}
```

> 以上配置的规则是”如果匹配...则...“，如果要做到”如果不匹配...则...“就需要用到特殊的方式，配置最后一个location块并且使用/作为参数，这个参数会使得该location块匹配所有的请求。这样就能做到前面的所有location都匹配不到时，则由这个”/“来处理请求。

##3、文件路径的定义

###3.1、root

###3.2、alias

###3.3、index

###3.4、error_page

###3.5、recursive_error_page

###3.6、try_file


