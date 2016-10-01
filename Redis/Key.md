# Key
##DEL key [key ...]
删除给定的一个或多个 key 。不存在的 key 会被忽略。

##DUMP key
序列化给定 key的值，并返回被序列化的值，使用`RESTORE`命令可以将这个值反序列化为 Redis 键。

##RESTORE key ttl serialized-value
反序列化给定的序列化值，并将它和给定的 key 关联。
参数 ttl 以毫秒为单位为 key 设置生存时间；如果 ttl 为 0 ，那么不设置生存时间。
RESTORE 在执行反序列化之前会先对序列化值的 RDB 版本和数据校验和进行检查，如果 RDB 版本不相同或者数据不完整的话，那么 RESTORE 会拒绝进行反序列化，并返回一个错误。

```shell
redis> SET greeting "hello, dumping world!"
OK

# 输出指定key的值序列
redis> DUMP greeting
"\x00\x15hello, dumping world!\x06\x00E\xa0Z\x82\xd8r\xc1\xde"

redis> RESTORE greeting-again 0 "\x00\x15hello, dumping world!\x06\x00E\xa0Z\x82\xd8r\xc1\xde"
OK

# 获取存储了序列化值的key的反序列化的值
redis> GET greeting-again
"hello, dumping world!"

redis> RESTORE fake-message 0 "hello moto moto blah blah"   ; 使用错误的值进行反序列化
(error) ERR DUMP payload version or checksum are wrong
```

##EXISTS key
检查给定 key 是否存在。

##EXPIRE key seconds
为给定 key 设置生存时间，当 key 过期时(生存时间为 0 )，它会被自动删除。
改变生存时间的命令：`DEL`、`SET`、`GETSET`。前者彻底删除key，后面两个可以带生存时间的参数。

##PEXPIRE key milliseconds
以毫秒单位设置key的生存时间

##EXPIREAT key timestamp
设置过期时间，值为以秒为单位的时间戳。

##PEXPIREAT key milliseconds-timestamp
以毫秒为单位的时间戳设置key的过期时间

##TTL key
以秒为单位，返回key的剩余生存时间(TTL, time to live)。
key不存在时返回-2，key存在但没有设置过期时间返回-1。

##PTTL key
以毫秒为单位返回 key 的剩余生存时间。

##RANDOMKEY
从当前数据库中随机返回(不删除)一个 key 

##RENAME key newkey
将 key 改名为 newkey 。
当 key 和 newkey 相同，或者 key 不存在时，返回一个错误
当 newkey 已经存在时， RENAME 命令将覆盖旧值。

##RENAMENX key newkey
当且仅当 newkey 不存在时，将 key 改名为 newkey 。
当 key 不存在时，返回一个错误。

##TYPE key
返回 key 所储存的值的类型

##KEYS pattern
返回符合匹配模式的所有key
KEYS * 匹配数据库中所有 key 。
KEYS h?llo 匹配 hello ， hallo 和 hxllo 等。
KEYS h*llo 匹配 hllo 和 heeeeello 等。
KEYS h[ae]llo 匹配 hello 和 hallo ，但不匹配 hillo 。
特殊符号用 \ 隔开

##SORT key [BY pattern] [LIMIT offset count] [GET pattern [GET pattern ...]] [ASC | DESC] [ALPHA] [STORE destination]
返回或保存给定列表、集合、有序集合 key 中经过排序的元素。
排序默认以数字作为对象，值被解释为双精度浮点数，然后进行比较。


http://doc.redisfans.com/key/sort.html

```sh
redis> LPUSH today_cost 30 1.5 10 8
(integer) 4

# 排序
redis> SORT today_cost
1) "1.5"
2) "8"
3) "10"
4) "30"

# 逆序排序
redis 127.0.0.1:6379> SORT today_cost DESC
1) "30"
2) "10"
3) "8"
4) "1.5"

# 按数字或按字母
redis> LPUSH website "www.reddit.com"
(integer) 1
redis> LPUSH website "www.slashdot.com"
(integer) 2
redis> LPUSH website "www.infoq.com"
(integer) 3
```

###ALPHA选项，按字母排序

```sh
# 默认（按数字）排序
redis> SORT website
1) "www.infoq.com"
2) "www.slashdot.com"
3) "www.reddit.com"

# 按字符排序
redis> SORT website ALPHA
1) "www.infoq.com"
2) "www.reddit.com"
3) "www.slashdot.com"
```

###使用外部 key 进行排序
|uid|user_name_{uid}|user_levle_{uid}|
|---|---|---|
|1	|admin	|9999|
|2	|jack	|10|
|3	|peter	|25|
|4	|mary	|70||

####输入数据
```sh
#添加数据
# admin

redis 127.0.0.1:6379> LPUSH uid 1
(integer) 1
redis 127.0.0.1:6379> SET user_name_1 admin
OK
redis 127.0.0.1:6379> SET user_level_1 9999
OK

# jack
redis 127.0.0.1:6379> LPUSH uid 2
(integer) 2
redis 127.0.0.1:6379> SET user_name_2 jack
OK
redis 127.0.0.1:6379> SET user_level_2 10
OK

# peter
redis 127.0.0.1:6379> LPUSH uid 3
(integer) 3
redis 127.0.0.1:6379> SET user_name_3 peter
OK
redis 127.0.0.1:6379> SET user_level_3 25
OK

# mary
redis 127.0.0.1:6379> LPUSH uid 4
(integer) 4
redis 127.0.0.1:6379> SET user_name_4 mary
OK
redis 127.0.0.1:6379> SET user_level_4 70

```

####排序查询

```sh
# 默认排序
redis 127.0.0.1:6379> SORT uid
1) "1"      # admin
2) "2"      # jack
3) "3"      # peter
4) "4"      # mary

# 通过BY按其他键的元素来排序
# 首先取出uid的值，与user_level_拼起来，分别为：
# user_level_1 、 user_level_2 、 user_level_3 和 user_level_4
# 然后根据上面这些键的值排序
redis 127.0.0.1:6379> SORT uid BY user_level_*
1) "2"      # jack , level = 10
2) "3"      # peter, level = 25
3) "4"      # mary, level = 70
4) "1"      # admin, level = 9999

# 通过GET来引用排序的键的值，来取其他键的值
# 通过排序后的uid的值，去取user_name_{uid}键的值，按照uid的顺序显示
redis 127.0.0.1:6379> SORT uid GET user_name_*
1) "admin"
2) "jack"
3) "peter"
4) "mary"

## 使用过个GET
redis 127.0.0.1:6379> SORT uid GET # GET user_level_* GET user_name_*
1) "1"          # uid
2) "9999"       # level
3) "admin"      # name
4) "2"
5) "10"
6) "jack"
7) "3"
8) "25"
9) "peter"
10) "4"
11) "70"
12) "mary"

# 组合使用BY和GET
redis 127.0.0.1:6379> SORT uid BY user_level_* GET user_name_*
```

####使用哈希表保存表格数据
sh
```shell
# 使用哈希表保存的情况
redis 127.0.0.1:6379> HMSET user_info_1 name admin level 9999
OK
redis 127.0.0.1:6379> HMSET user_info_2 name jack level 10
OK
redis 127.0.0.1:6379> HMSET user_info_3 name peter level 25
OK
redis 127.0.0.1:6379> HMSET user_info_4 name mary level 70
OK

```

####查询
```sh
redis 127.0.0.1:6379> SORT uid BY user_info_*->level
1) "2"
2) "3"
3) "4"
4) "1"

redis 127.0.0.1:6379> SORT uid BY user_info_*->level GET user_info_*->name
1) "jack"
2) "peter"
3) "mary"
4) "admin"
```

###查询后保存

```sh
# 测试数据
redis 127.0.0.1:6379> RPUSH numbers 1 3 5 7 9
(integer) 5
redis 127.0.0.1:6379> RPUSH numbers 2 4 6 8 10
(integer) 10
redis 127.0.0.1:6379> LRANGE numbers 0 -1
1) "1"
2) "3"
3) "5"
4) "7"
5) "9"
6) "2"
7) "4"
8) "6"
9) "8"
10) "10"

redis 127.0.0.1:6379> SORT numbers STORE sorted-numbers
(integer) 10

# 排序后的结果
redis 127.0.0.1:6379> LRANGE sorted-numbers 0 -1
1) "1"
2) "2"
3) "3"
4) "4"
5) "5"
6) "6"
7) "7"
8) "8"
9) "9"
10) "10"
```

##MIGRATE host port key destination-db timeout [COPY] [REPLACE]
将 key 原子性地从当前实例传送到目标实例的指定数据库上，一旦传送成功， key 保证会出现在目标实例上，而当前实例上的 key 会被删除。

>* 这个命令是一个原子操作，它在执行的时候会阻塞进行迁移的两个实例，直到以下任意结果发生：迁移成功，迁移失败，等到超时。
>* 命令的内部实现是这样的：它在当前实例对给定 key 执行 DUMP 命令 ，将它序列化，然后传送到目标实例，目标实例再使用 RESTORE 对数据进行反序列化，并将反序列化所得的数据添加到数据库中；当前实例就像目标实例的客户端那样，只要看到 RESTORE 命令返回 OK ，它就会调用 DEL 删除自己数据库上的 key 。
>* timeout 参数以毫秒为格式，指定当前实例和目标实例进行沟通的最大间隔时间。这说明操作并不一定要在 timeout 毫秒内完成，只是说数据传送的时间不能超过这个 timeout 数。

##MOVE key db
将当前数据库的 key 移动到给定的数据库 db 当中。

##PERSIST key
将某个key设置永久化（不会过期

##


##SCAN cursor [MATCH pattern] [COUNT count]
用于迭代当前数据库中的数据库键，返回一个新的游标与键的集合。
#### cursor迭代开始
返回的游标将会用于下一次迭代的cursor参数。
当`cursor`设置为0时，服务器开始一次新的迭代，而当服务器返回的游标为0时，表示迭代结束。
####MATCH
用来匹配要迭代的键
####COUNT
SCAN命令本身不保证每次迭代返回的个数，可以用count选项来调整。

```sh
# 开始一次新的迭代
redis 127.0.0.1:6379> scan 0
1) "17"
2)  1) "key:12"
    2) "key:8"
    3) "key:4"
    4) "key:14"
    5) "key:16"
    6) "key:17"
    7) "key:15"
    8) "key:10"
    9) "key:3"
    10) "key:7"
    11) "key:1"
# 将上一次迭代返回的游标用于该迭代，表示继续之前的迭代过程
# 该次迭代返回0，表示迭代结束
redis 127.0.0.1:6379> scan 17
1) "0"
2) 1) "key:5"
   2) "key:18"
   3) "key:0"
   4) "key:2"
   5) "key:19"
   6) "key:13"
   7) "key:6"
   8) "key:9"
   9) "key:11"

# 匹配
redis 127.0.0.1:6379> sadd myset 1 2 3 foo foobar feelsgood
(integer) 6
redis 127.0.0.1:6379> sscan myset 0 match f*
1) "0"
2) 1) "foo"
   2) "feelsgood"
   3) "foobar"
```


##OBJECT subcommand [arguments [arguments]]

OBJECT 命令有多个子命令：
>* OBJECT REFCOUNT <key> 返回给定 key 引用所储存的值的次数。此命令主要用于除错。
>* OBJECT ENCODING <key> 返回给定 key 锁储存的值所使用的内部表示(representation)。
>* OBJECT IDLETIME <key> 返回给定 key 自储存以来的空转时间(idle， 没有被读取也没有被写入)，以秒为单位。

对象可以以多种方式编码：
>* 字符串可以被编码为 raw (一般字符串)或 int (用字符串表示64位数字是为了节约空间)。
>* 列表可以被编码为 ziplist 或 linkedlist 。 ziplist 是为节约大小较小的列表空间而作的特殊表示。
>* 集合可以被编码为 intset 或者 hashtable 。 intset 是只储存数字的小集合的特殊表示。
>* 哈希表可以编码为 zipmap 或者 hashtable 。 zipmap 是小哈希表的特殊表示。
>* 有序集合可以被编码为 ziplist 或者 skiplist 格式。 ziplist 用于表示小的有序集合，而 skiplist 则用于表示任何大小的有序集合。


```sh
redis> SET game "COD"           # 设置一个字符串
OK

redis> OBJECT REFCOUNT game     # 只有一个引用
(integer) 1

redis> OBJECT IDLETIME game     # 等待一阵。。。然后查看空转时间
(integer) 90

redis> GET game                 # 提取game， 让它处于活跃(active)状态
"COD"

redis> OBJECT IDLETIME game     # 不再处于空转
(integer) 0

redis> OBJECT ENCODING game     # 字符串的编码方式
"raw"

redis> SET phone 15820123123    # 大的数字也被编码为字符串
OK

redis> OBJECT ENCODING phone
"raw"

redis> SET age 20               # 短数字被编码为 int
OK

redis> OBJECT ENCODING age
"int"
```

