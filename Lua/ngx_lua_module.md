# ngx_lua_module

##执行顺序
###初始化阶段

####init_by_lua*
####init_worker_by_lua*

###处理请求阶段

####ssl_certificate_by_lua*
请求是https时有该过程
####set_by_lua*
设置变量

####rewrite_by_lua*
转发、重定向、缓存等功能

####access_by_lua*
IP准入、接口健全等情况集中处理，可以配合iptable完成简单的防火墙

###内容生成阶段，通过lua或者调用上游

####content_by_lua\*/balancer_by_lua*
* content_by_lua内容生成
* balancer_by_lua负载均衡处理

####header_filter_by_lua*
响应头过滤处理，增删改响应头

####body_filter_by_lua*
响应注意过滤处理

###日志记录阶段
####log_by_lua*
 会话完成后本地异步完成日志记录(日志可以记录在本地，还可以同步到其他机器)

##Tips
###不同阶段数据共享
在单个请求的不同阶段共享数据，可以使用ngx.ctx表。
该表的生命周期和请求的生命周期一直，贯穿该请求的rewrite，access，content等各处理阶段。

###不同worker进程的数据共享
使用`ngx.shared.DICT`系列方法操作的变量，是基于共享内存名为 `DICT` 的Lua字典对象，它是一个共享内存区块。
所有共享的内存区块均被当前nginx服务器实例的所有nginx worker进程。

###静态链接Lua模块到Nginx中
###cosocket在有些地方不可用

