# configure执行过程
##执行./auto/options文件，判断执行configure的参数

##执行./auto/init文件，初始化configure命令后续将产生的文件路径，一般在./objs路径

##执行./auto/sources文件，分析Nginx源码，构造Makefile文件

##创建编译过程中所有要生成的文件路径，该路径由--builddir参数指定

##准备创建必要的编译文件，如ngx_auto_headers.h、autoconf.err等

##向objs/gx_auto_headers.h写入命令行带的参数

##判断DEBUG标志

##检查操作系统参数是否支持后续编译

##输出操作系统信息

##执行./auto/cc/conf检查并设置GCC编译器

##执行./auto/headers定义非Windows系统的一些必要头文件

##执行./auto/os/conf定义当前操作系统相关的方法并检查环境是否支持

##执行./auto/unix定义UNIX系统中通用的头文件和系统调用

##执行./auto/modules，读取模块数组，生产ngx_modules.c文件，该文件会被编译进Nginx

##执行./auto/lib/conf检查第三方库

##处理Nginx安装后的路径

##处理Nginx安装后conf文件的路径

##处理Nginx安装后，二进制文件、pid、lock等其他文件的路径

##执行./auto/make创建编译时使用的objs/Makefile文件

##执行./auto/lib/make，为objs/Makefile加入需要的第三库

##执行./auto/install，为objs/Makefile加入install功能

##执行./auto/stubs

##在ngx_auto_config.h中指定Nginx服务的用户和用户组

##执行./auto/summary


