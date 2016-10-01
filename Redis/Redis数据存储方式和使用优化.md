# Redis数据存储方式和使用优化
##数据类型
###redisObject，保存数据的对象

```c
typedef struct redisObject {
    unsigned type:4;    // 占4字节，对外的数据类型，如String/Hash/Set等
    unsigned storage:2;     // 数据保存的位置，REDIS_VM_MEMORY or REDIS_VM_SWAPPING
    unsigned encoding:4;    // 内部实现的编码，raw/int/ht/zipmap/linkedlist/ziplist/intset等
    unsigned lru::REDIS_LRU_BITS;   // 对象最后一次被访问的时间
    int refcount;   // 引用计数
    void *ptr;  // 指向实际数据的指针
} robj;

```

###String
内部存储默认是一个字符串，被redisObject的ptr指针引用。遇到incr，decr等操作时，会转成数值型进行计算，此时redisObject的encoding字段为int。

###Hash
如果要将一个Map以Srting保存到Redis中，有种方式：
>* 将Map序列化保存，但是会增加序列化/反序列化的开销，而且在修改Map的key时，需要整个对象取出来操作，并且修改操作需要并发进行保护；
>* 将Map的的每个成员都作为一个String保存，由于每一个成员都需要一个key来维护，会造成内存浪费。

Redis中的Hash可以用来很好地维护一个Map数据，每一个Hash类型的数据有多个field-value对，field相当于Map中的key。
Hash的value内部实际上就是一个HashMap，但实际上会有两种实现，当Hash的成员较少时，为了节省内存会采用类似一维数组的方式来紧凑存储，而不采用真正的HashMap结构，对应的redisObject的encoding为zipmap。而当成员数量较多时，会使用真正的HashMap来存储，相应的encoding是ht。
>Redis提供了一个接口hgetall来获取一个Hash的全部属性数据，但是如果成员很多，需要遍历，由于Redis是单线程，该操作会阻塞。

###List
List可按数据保存的顺序来存储数据，允许重复的value。
List的实现在Redis中采用双向链表，支持反向查找和遍历，但也会带来部分额外的内存开销。
Redis很多内部的实现都会基于这个结构，比如队列。

###Set
Set是不可重复的、无序的集合。
Set的内部实现是其value都是null的HashMap（和Java中的set实现基本相同），这个HashMap的key，就是我们保存进Set的数据成员，通过计算hash的方式来快速排重。

###SortedSet
不可重复，有序的集合，通过每一个成员都有一个对应的优先级score来决定排序。
SortedSet实现，使用HashMap和跳跃表（SkipList)

##参数优化
###vm-enable，是否开启虚拟内存
当存储的数据大小超过物理内存大小时，redis可以将内存中的数据转换到磁盘中。但是这种策略的内存管理成本比较高，并且不太成熟，所以建议关闭该策略。

###maxmemory，允许的最大内存大小
当Redis使用了超过该配置的内存大小时，就不会在接受后续的写入请求，防止Redis使用了过多的物理内存后触发了swap，会引起线程阻塞，影响性能。

###不同数据类型的内存控制参数
前面提到Hash在Redis中有两种实现，当Hash的key比较少时，使用线性紧凑格式来存储；当Hash中的key比较多时，才会真正使用HashMap去保存数据。
HashMap中key的查找和操作的时间复杂度都是O(1)，而一维的存储则是O(n)的时间复杂。当n小的时候，影响不大，否则会严重影响性能。
相关配置参数:

```sh
hash-max-zipmap-entries 64
hash-max-zipmap-value 512
```
hash-max-zipmap-entries表示，key的数量低于该值的情况下，使用线性紧凑格式来存储，否则转化成真正的HashMap。
hash-max-zipmap-value表示，Hash中key的value长度小于该值时，使用线性紧凑格式，否则转化成真正的Map。

此外还有

```sh
# list数据类型多少节点以下会采用去指针的紧凑存储格式。
list-max-ziplist-entries 512

# list数据类型节点值大小小于多少字节会采用紧凑存储格式。
list-max-ziplist-value 64 

# set数据类型内部数据如果全部是数值型，且包含多少节点以下会采用紧凑格式存储。 
set-max-intset-entries 512 

```

