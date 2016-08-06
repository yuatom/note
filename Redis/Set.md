# Set
集合，集合内的元素不能重复

##SADD key member [member ...]
将一个/多个member添加到key中

```shell
127.0.0.1:6379> SADD bbs "tianya.cn" "groups.google.com"
(integer) 2
#重复元素
127.0.0.1:6379> SADD bbs "tianya.cn"
(integer) 0
```

##SCARD key
返回集合 key 的基数(集合中元素的数量)，空集合则返回0

```shell
127.0.0.1:6379> SADD bbs "tianya.cn" "groups.google.com"
(integer) 2

127.0.0.1:6379> SCARD bbs
(integer) 2
```

##SDIFF key [key ...]
返回一个集合的全部成员，或后面那些集合中没有的元素。
不存在的 key 被视为空集。

```shell
127.0.0.1:6379> smembers bbs
1) "tianya.cn"
2) "groups.google.com"

127.0.0.1:6379> smembers bbs1
1) "weibo.com"
2) "tianya.cn"
# 一个集合中的所有元素
127.0.0.1:6379> sdiff bbs
1) "tianya.cn"
2) "groups.google.com"

# 返回差集
127.0.0.1:6379> sdiff bbs bbs1
1) "groups.google.com"
127.0.0.1:6379> sdiff bbs1 bbs
1) "weibo.com"
```

#SDIFFSTORE destination key [key ...]
将给出集合的`SDIFF`结果保存到`destination`集合中。

##SINTER key [key ...]
返回一个集合的全部成员，或和后面集合的交集。
不存在的 key 被视为空集。

```shell
127.0.0.1:6379> smembers bbs
1) "tianya.cn"
2) "groups.google.com"
127.0.0.1:6379> smembers bbs1
1) "weibo.com"
2) "tianya.cn"
127.0.0.1:6379> SINTER bbs bbs1
1) "tianya.cn"
```

##SINTERSTORE destination key [key ...]
将给出集合的`SINTER`结果保存到`destination`中。

##SISMEMBER key member
判断member是否是key集合的成员

```shell
127.0.0.1:6379> smembers bbs
1) "tianya.cn"
2) "groups.google.com"
127.0.0.1:6379> sismember bbs tianya.cn
(integer) 1
127.0.0.1:6379> sismember bbs tianya
(integer) 0
```

##SMEMBERS key
返回集合 key 中的所有成员。

```shell
# key 不存在或集合为空
redis> EXISTS not_exists_key
(integer) 0
redis> SMEMBERS not_exists_key
(empty list or set)

# 非空集合
redis> SADD language Ruby Python Clojure
(integer) 3
redis> SMEMBERS language
1) "Python"
2) "Ruby"
3) "Clojure"
```

##SMOVE source destination member
将 member 元素从 source 集合移动到 destination 集合。

```shell
#第一个集合
127.0.0.1:6379> smembers bbs
1) "tianya.cn"
2) "groups.google.com"
#第二个鸡舍
127.0.0.1:6379> smembers bbs1
1) "weibo.com"
2) "tianya.cn"
#移动一个不存在的元素，返回0
127.0.0.1:6379> smove bbs bbs1 "group.google.com"
(integer) 0
#移动一个存在的元素，返回1
127.0.0.1:6379> smove bbs bbs1 "groups.google.com"
(integer) 1
#移动后的第一个集合
127.0.0.1:6379> smembers bbs
1) "tianya.cn"
#移动后的第二个集合
127.0.0.1:6379> smembers bbs1
1) "weibo.com"
2) "tianya.cn"
3) "groups.google.com"
```

##SPOP key
移除并返回集合中的一个随机元素

```shell
127.0.0.1:6379> smembers bbs1
1) "weibo.com"
2) "tianya.cn"
3) "groups.google.com"
127.0.0.1:6379> spop bbs1
"tianya.cn"
127.0.0.1:6379> smembers bbs1
1) "weibo.com"
2) "groups.google.com"
```

##SRANDMEMBER key [count]
count为空，随机返回key集合的一个元素；
count大于0，随机返回key集合中count个元素，如果count大于集合的基数，则返回整个集合的元素；
count小于0，返回长度为count绝对值的数组，**数组中的元素可能重复**。

```shell
127.0.0.1:6379> smembers bbs1
1) "renren.com"
2) "tianya.cn"
3) "weibo.com"
4) "groups.google.com"
127.0.0.1:6379> srandmember bbs1
"renren.com"
127.0.0.1:6379> srandmember bbs1 3
1) "renren.com"
2) "weibo.com"
3) "tianya.cn"
127.0.0.1:6379> srandmember bbs1 -3
1) "weibo.com"
2) "weibo.com"
3) "groups.google.com"
```

##SREM key member [member ...]
移除key集合中的一个或多个元素

```shell
27.0.0.1:6379> smembers bbs1
1) "renren.com"
2) "tianya.cn"
3) "weibo.com"
4) "groups.google.com"
127.0.0.1:6379> srem bbs1 weibo.com tianya.cn
(integer) 2
127.0.0.1:6379> smembers bbs1
1) "renren.com"
2) "groups.google.com"
```

##SUNION key [key ...]
返回一个集合的全部元素，或多个元素的并集。

```shell
127.0.0.1:6379> smembers bbs
1) "tianya.cn"
127.0.0.1:6379> smembers bbs1
1) "renren.com"
2) "groups.google.com"
127.0.0.1:6379> sunion bbs1
1) "renren.com"
2) "groups.google.com"
127.0.0.1:6379> sunion bbs1 bbs
1) "renren.com"
2) "tianya.cn"
3) "groups.google.com"
```

##SUNIONSTORE destination key [key ...]
将给出集合的`SUNION`结果保存到`destination`中。

##SSCAN key cursor [MATCH pattern] [COUNT count]
用于迭代集合键中的元素，返回的每个元素都是一个集合成员。


