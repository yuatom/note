# AOF & rewrite
##AOF，类似于Log机制，记录每次写操作，当系统崩溃时，可通过AOF来恢复数据。
由于每一次记录的时候都通过append文件操作，因此速度较快。

##rewrite，当AOF文件大小超过某个临近值时，rewrite会被执行。
该操作会fork一个子进程，创建扫描库中的键值，以redis命令的形式输出到一个临时文件中。为了减少文件大小，该操作也会将多个键值集合起来在一条redis命令中完成。在rewrite期间，写操作会被缓存到内存的rewrite buffer中，rewrite成功后将这些操作复制到临时文件中。最后用临时文件来替代AOF文件。
当AOF机制关闭时，可以使用`bgrewriteaof`命令来进行rewrite。

##Redis AOF流程
1、Redis Server启动，如果AOF机制打开那么初始化AOF状态，并且如果存在AOF文件，读取AOF文件。
2、随着Redis不断接受命令，每个写命令都被添加到AOF文件，AOF文件膨胀到需要rewrite时又或者接收到客户端的`bgrewriteaof`命令。
3、fork出一个子进程进行rewrite，而父进程继续接受命令，现在的写操作命令都会被额外添加到一个`aof_rewrite_buf_blocks`缓冲中。
4、当子进程rewrite结束后，父进程收到子进程退出信号，把`aof_rewrite_buf_blocks`的缓冲添加到rewrite后的文件中，然后切换AOF的文件fd。rewrite任务完成，继续第二个步骤。

##关键点
1、写操作缓存，使得AOF操作可能没有写到硬盘中。通过`fsync()`强制输出到硬盘中。频率可通过配置文件中flush策略制定，可以选择每次事件循环写操作都强制fsync或者每秒fsync至少运行一次。
2、rewrite时，是否要将此时的写操作继续添加到原来的AOF文件中。如果继续`fsync()`，可能影响IO性能。所以一般rewrite的时候禁止`fsync()`到旧的AOF文件，这策略可以在配置文件中修改。
3、`?`在rewrite结束后，在将新rewrite文件重命名为配置中指定的文件时，如果旧AOF存在，那么会unlink掉旧文件。这是就存在一个问题，处理rewrite文件迁移的是主线程，rename(oldpath, newpath)过程会覆盖旧文件，这是rename会unlink(oldfd)，而unlink操作会导致block主线程。这时，我们就需要类似libeio(http://software.schmorp.de/pkg/libeio.html) 这样的库去进行异步的底层IO。作者在bio.c有一个类似的机制，通过创建新线程来进行异步操作。


