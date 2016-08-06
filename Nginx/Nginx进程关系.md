# Nginx进程关系
##运行方式
>* 单进程（master）
>* 一个master进程与多个worker进程（数量和CPU核心数相等）

##一个master进程与多个worker进程
>* master进程不负责处理请求，而是负责管理工作，包括启动、停止、重载配置文件、平滑升级等命令行以及管理worker进程。当任意一个worker进程出现错误时，master进程可以重新启动新的worker进程。
>* worker进程是真正处理请求的，一个worker进程可同时处理多个请求（受内存大小限制）。

