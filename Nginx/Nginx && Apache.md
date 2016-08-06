# Nginx && Apache

##Apache和Nginx比较 功能对比
Nginx和Apache一样，都是HTTP服务器软件，在功能实现上都采用模块化结构设计，都支持通用的语言接口，如PHP、Perl、Python等，同时还支持正向和反向代理、虚拟主机、URL重写、压缩传输、SSL加密传输等。
在功能实现上，Apache的所有模块都支持动、静态编译，而Nginx模块都是静态编译的，
对FastCGI的支持，Apache对Fcgi的支持不好，而Nginx对Fcgi的支持非常好；
在处理连接方式上，Nginx支持epoll，而Apache却不支持；
在空间使用上，Nginx安装包仅仅只有几百K，和Nginx比起来Apache绝对是庞然大物。

##Nginx相对apache的优点
轻量级，同样起web 服务，比apache 占用更少的内存及资源
静态处理，Nginx 静态处理性能比 Apache 高 3倍以上
抗并发，nginx 处理请求是异步非阻塞的，而apache则是阻塞型的，在高并发下nginx 能保持低资源低消耗高性能。在Apache+PHP（prefork）模式下，如果PHP处理慢或者前端压力很大的情况下，很容易出现Apache进程数飙升，从而拒绝服务的现象。
高度模块化的设计，编写模块相对简单
社区活跃，各种高性能模块出品迅速啊

##apache相对nginx的优点
rewrite，比nginx 的rewrite 强大
模块超多，基本想到的都可以找到
少bug，nginx的bug相对较多
超稳定
Apache对PHP支持比较简单，Nginx需要配合其他后端用


##选择Nginx的优势所在
作为Web服务器: Nginx处理静态文件、索引文件，自动索引的效率非常高。
作为代理服务器，Nginx可以实现无缓存的反向代理加速，提高网站运行速度。
作为负载均衡服务器，Nginx既可以在内部直接支持Rails和PHP，也可以支持HTTP代理服务器对外进行服务，同时还支持简单的容错和利用算法进行负载均衡。
在性能方面，Nginx是专门为性能优化而开发的，在实现上非常注重效率。它采用内核Poll模型(epoll and kqueue )，可以支持更多的并发连接，最大可以支持对50 000个并发连接数的响应，而且只占用很低的内存资源。
在稳定性方面，Nginx采取了分阶段资源分配技术，使得CPU与内存的占用率非常低。Nginx官方表示，Nginx保持10 000个没有活动的连接，而这些连接只占用2.5MB内存，因此，类似DOS这样的攻击对Nginx来说基本上是没有任何作用的。
在高可用性方面，Nginx支持热部署，启动速度特别迅速，因此可以在不间断服务的情况下，对软件版本或者配置进行升级，即使运行数月也无需重新启动，几乎可以做到7×24小时不间断地运行。

##同时使用Nginx和Apache
由于Nginx和Apache各自的优势，现在很多人选择了让两者在服务器中共存。在服务器端让Nginx在前，Apache在后。由Nginx做负载均衡和反向代理，并且处理静态文件，讲动态请求（如PHP应用）交给Apache去处理。

