# Redis & Memcache

##1.网络IO模型
###1.1.Memcache，多线程，非阻塞IO复用
Memcache的多线程，分为监听主线程和worker子线程。
监听线程监听网络连接，接收请求后，将连接传递给worker线程，进行读写IO，网络层使用了libevent封装的事件库。
多线程模型可以发挥多核作用，但也引入了cache coherency(缓存一致性)和锁的问题。比如memcache最常用的stat命令，memcache所有的操作都要对这全局变量加锁，在性能上会有一些损耗。

###1.2.Redis，单线程，非阻塞型IO复用
单线程，避免了不必要的上下文切换和竞争条件
Redis网络层使用的是自己封装的一个简单的AeEvent事件处理框架。
对于单纯只有IO操作来说，单线程可以将速度优势发挥到最大，但是Redis提供的一些排序/聚合等功能，单线程模型在CPU的计算过程中，整个IO调度被阻塞，因此会影响整体的吞吐量。
内部实现采用epoll，

##2.数据支持类型
###2.1.Memcache，仅支持key-value形式的存储和访问
Memcache在内存中维护一张巨大的HashTable，使得对数据查询的时间复杂度降低到了O(1)。

###2.2.Redis，支持多种数据类型
Redis除了支持key-value形式的数据，还支持Hash/Set/SortedSet/List等数据类型

##3.内存管理机制
应用程序在内存管理，在C语言中的`malloc`和`free`函数是最常用的分配和释放内存的方法。但是可能存在以下问题：
>* 对于开发人员来说不匹配的malloc和free容易造成内存泄露；
>* 频繁调用会造成大量内存碎片无法回收重新利用；
>* 作为系统调用，其系统开销远远大于一般函数调用。
由于以上问题的存在，高效的内存管理方案都不会直接使用malloc和free调用。

###3.1.Memcache，Slab Allocation机制，预分配内存
Memcache默认的Slab Allocation机制的主要思想是按照预先规定的大小，将分配的内存分割成特定长度的块来存储相应长度的key-value数据，以此来解决内存碎片的问题（因为程序所能分配到的内存都被分配成不同的块）。

Slab Allocation的原理：
首先向系统申请一大块内存，然后将该内存分割成各种尺寸的块Chunk（存储key-value的最小单位），然后多个尺寸相同的块组成一个Slab Class。每个Slab Class的大小可以在Memcache启动时指定`Growth Factor`参数控制。默认Growth Factor的值是1.25，即后面一个Slab Class是前面一个Slab Class的1.25倍，但在实际运行中有时会不止1.25倍，因为需要字节对齐，memcache是8字节对齐，因此chunk和slab的大小必须被8整除。
在Memcache保存数据时，会根据需要保存的数据大小选择一个最合适的Slab Class，然后在Slab上找到一个空闲的chunk来保存数据。当一个数据过期或者丢弃时，所占用的chunk就可以回收，重新添加到空闲列表。
以上可以看出Memcache内存管理的效率高，且`不会造成内存碎片`。但是会`导致内存浪费`，因为被保存的数据大小总是小于或等于保存它的chunk的大小。

###3.2.Redis的内存管理，采用封装过的malloc/free，现场申请内存
Redis在分配一块内存之后，会将这块内存的大小保存到这块内存块的头部。
在redis调用mallo后，会返回被分配的内存的`头部指针（real_ptr）`。redis将内存块的大小Size保存到该内存块的头部（头部占用的内存大小是已知的），然后返回头部之后的内存地址，即真正保存`数据的内存地址（ret_ptr）`。当钥匙房内存的时候，将ret_ptr传递给内存管理程序，通过`ret_ptr`，程序可以计算出`real_ptr`的值，然后将real_ptr传给free释放内存。

| Size | Memory Block |
| --- | --- |

Redis中通过定义一个数组来记录所有的内存分配情况。数组的下标为所分配的内存大小，下标对应的元素为该内存大小的内存块的个数。

Redis中不是所有的数据都一直存储在内存中，这是和Memcache相比最大的一个区别。当物理内存用完时，Redis将一些长时间没有用到的数据的value交换（swap）到磁盘中，Redis会继续缓存这数据的key。当Redis发现内存的使用超过某个阈值时，会触发swap操作，根据“swappability = age*log(size_in_memory)”计算出哪些key对应的value需要swap到磁盘。然后将这些key的value持久化到磁盘中，同时在内存中删除该value。因此Redis能保存超过内存大小的数据，但前提是内存的大小足够保存所有的key。

在Redis将内存中的数据swap到磁盘时，提供服务的主线程和进行swap操作的子线程会共享这部分内存，所以在更新需要swap的数据时，Redis会阻塞这个更新操作，直到子线程完成swap操作后才能继续更新。

当从Redis中读取数据时发现value在swap文件中，就需要去加载swap文件，然后再将数据返回。默认的情况下，读取swap时Redis会被阻塞，直到swap文件加载完成后才会响应，最会降低服务的并发能力。此时需要在Redis运行时设置I/O线程池的大小，对需要从swap文件中加载相应数据的读取请求进行并发操作，减少阻塞时间。

Redis现场申请内存的方式来存储数据，在一定程度会存在内存碎片。此外，Redis会根据存储命令的参数，将带有过期时间的数据单独放在一起，成为临时数据。非临时数据是永远不会被剔除的，当物理内存数据不足时，Redis会先尝试剔除临时数据。从这点上看Redis更适合作为存储而不是Cache。

##4.数据一致性
Memcached提供了cas命令，可以保证多个并发访问操作同一份数据的一致性问题。 Redis没有提供cas 命令，并不能保证这点，不过Redis提供了事务的功能，可以保证一串 命令的原子性，中间不会被任何操作打断。
>* check and save: Check And Set，是一个确保并发一致性的机制，属于乐观锁的范畴。在更新数据前，会获得数据当前的版本号，提交数据时，带上该版本号，memcache服务判断提交上的版本是否是最新的，如果是最新的，则给予更新，否则更新失败。
>* memcache中，除了显式的gets和cas操作为，incr/decr操作也会使用cas机制；append/prepend操作也会涉及到cas的相关操作；

##5.集群管理

###5.1.Memcache，不支持分布式，只能通过一致性哈希
客户端向Memcached集群发送数据之前，首先会通过内置的分布式算法计算出该条数据的目标节点，然后数据会直接发送到该节点上存储。但客户端查询数据时，同样要计算出查询数据所在的节点，然后直接向该节点发送查询请求以获取数据。

###5.2.Redis，支持分布式
Redis更偏向于在服务器端构建分布式存储。最新版本的Redis已经支持了分布式存储功能。

Redis Cluster是一个实现了分布式且允许单点故障的Redis高级版本，它没有中心节点，具有线性可伸缩的功能。Redis Cluster的分布式存储架构，节点与节点之间通过二进制协议进行通信，节点与客户端之间通过ascii协议进行通信。在数据的放置策略上，Redis Cluster将整个key的数值域分成4096个哈希槽，每个节点上可以存储一个或多个哈希槽，也就是说当前Redis Cluster支持的最大节点数就是4096。Redis Cluster使用的分布式算法也很简单：crc16( key ) % HASH_SLOTS_NUMBER。

为了保证单点故障下的数据可用性，Redis Cluster引入了Master节点和Slave节点。在Redis Cluster中，每个Master节点都会有对应的两个用于冗余的Slave节点。这样在整个集群中，任意两个节点的宕机都不会导致数据的不可用。当Master节点退出后，集群会自动选择一个Slave节点成为新的Master节点。

##参考
http://blog.jobbole.com/101496/


