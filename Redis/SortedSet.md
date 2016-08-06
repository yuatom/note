# SortedSet
有序集合，通过诶外提供一个优先级参数来为成员排序，并且是插入有序。

##ZADD key score member [[score member] [score member] ...]
将一个或多个集合元素加入到有序集合key中；
如果某个元素已经存在，则更新该元素的score；
score可以是整数或双精度浮点数。

```shell
127.0.0.1:6379> ZADD page_rank 10 google.com
(integer) 1
127.0.0.1:6379> ZADD page_rank 9 baidu.com 8 bing.com
(integer) 2
```

##ZCARD key
返回有序集合的基数

```shell
127.0.0.1:6379> ZADD page_rank 10 google.com
(integer) 1
127.0.0.1:6379> ZADD page_rank 9 baidu.com 8 bing.com
(integer) 2
127.0.0.1:6379> ZCARD page_rank
```

##ZCOUNT key min max
返回有序集中scope在 min 和 max 之间(默认包括 score 值等于 min 或 max )的元素个数。

##ZINCRBY key increment member
将有序集合key中的元素member的score增加increment（可以为负数）

```shell
redis> ZSCORE salary tom
"2000"
redis> ZINCRBY salary 2000 tom   # tom 加薪啦！
"4000"
```

##ZRANGE key start stop [WITHSCORES]
返回有序集合中某个区间内的元素，顺序按score 值递增(从小到大)来排序。
下标参数 start 和 stop 都从0开始，当值小于0时，则为倒数，-1表示倒数第一个。
WITHSCORES：是否输出score值

```shell
127.0.0.1:6379> ZADD salary 2000 tom
(integer) 1
127.0.0.1:6379> ZADD salary 5000 jack
(integer) 1
# 显示所有
127.0.0.1:6379> ZRANGE salary 0 -1 WITHSCORES
1) "tom"
2) "2000"
3) "jack"
4) "5000"
```

##ZRANGEBYSCORE key min max [WITHSCORES] [LIMIT offset count]
返回score值在min和max之间的元素，可用括号表示开区间；
min 和 max 可以是 -inf 和 +inf，分别表示最小和最大。

```shell
redis> ZRANGEBYSCORE salary -inf +inf               # 显示整个有序集
1) "jack"
2) "tom"
3) "peter"

redis> ZRANGEBYSCORE salary -inf +inf WITHSCORES    # 显示整个有序集及成员的 score 值
1) "jack"
2) "2500"
3) "tom"
4) "5000"
5) "peter"
6) "12000"

redis> ZRANGEBYSCORE salary -inf 5000 WITHSCORES    # 显示工资 <=5000 的所有成员
1) "jack"
2) "2500"
3) "tom"
4) "5000"

redis> ZRANGEBYSCORE salary (5000 400000            # 显示工资大于 5000 小于等于 400000 的成员
1) "peter"
```

##ZRANK key member
显示有序集合key中，member在集合中按 score 值递增(从小到大)顺序排列时的排名。

```shell
redis> ZRANGE salary 0 -1 WITHSCORES        # 显示所有成员及其 score 值
1) "peter"
2) "3500"
3) "tom"
4) "4000"
5) "jack"
6) "5000"

redis> ZRANK salary tom                     # 显示 tom 的薪水排名，第二
(integer) 1
```

##ZREVRANK key member
返回集合中member在score从大到小排序的排名

##ZREM key member [member ...]
移除有序集合key中的一个或多个元素

##ZREMRANGEBYRANK key start stop
移除有序集合key中排名在start和stop之间的元素

##ZREMRANGEBYSCORE key min max
移除有序集合key中score在min和max之间的元素

##ZREVRANGE key start stop [WITHSCORES]
返回排名在start到stop中的元素并按score从大到小排序。

##ZREVRANGEBYSCORE key max min [WITHSCORES] [LIMIT offset count]
返回score在max到min中的元素并按score从大到小排序。

##ZSCORE key member
返回成员的score值

#ZUNIONSTORE destination numkeys key [key ...] [WEIGHTS weight [weight ...]] [AGGREGATE SUM|MIN|MAX]
计算多个有序集合的并集，集合的个数必须由numkeys指定，并将结果保存到destination中；
WEIGHTS：权重选项，默认为1，每个集合在进行AGGREGATE都要先乘以这个权重；
AGGREGATE：聚合方式，默认是SUM，可以将所有集合中某个成员的 score 值之 和 作为结果集中该成员的 score 值；使用参数 MIN ，可以将所有集合中某个成员的 最小 score 值作为结果集中该成员的 score 值；而参数 MAX 则是将所有集合中某个成员的 最大 score 值作为结果集中该成员的 score 值。

```
redis> ZRANGE programmer 0 -1 WITHSCORES
1) "peter"
2) "2000"
3) "jack"
4) "3500"
5) "tom"
6) "5000"

redis> ZRANGE manager 0 -1 WITHSCORES
1) "herry"
2) "2000"
3) "mary"
4) "3500"
5) "bob"
6) "4000"

# SUM聚合，第二个集合中的score在计算前先乘3
redis> ZUNIONSTORE salary 2 programmer manager WEIGHTS 1 3  
(integer) 6

redis> ZRANGE salary 0 -1 WITHSCORES
1) "peter"
2) "2000"
3) "jack"
4) "3500"
5) "tom"
6) "5000"
7) "herry"
8) "6000"
9) "mary"
10) "10500"
11) "bob"
12) "12000"
```

##ZINTERSTORE destination numkeys key [key ...] [WEIGHTS weight [weight ...]] [AGGREGATE SUM|MIN|MAX]
计算交集，参照ZUNIONSTORE。

##ZSCAN key cursor [MATCH pattern] [COUNT count]
命令用于迭代有序集合中的元素（包括元素成员和元素分值。
返回的每个元素都是一个有序集合元素，一个有序集合元素由一个成员（member）和一个分值（score）组成

```
127.0.0.1:6379> ZSCAN salary 0
1) "0"
2) 1) "tom"
   2) "2000"
   3) "jack"
   4) "5000"
   5) "peter"
   6) "12000"
```

