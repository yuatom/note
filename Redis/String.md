# String
##SET key value [EX seconds] [PX milliseconds] [NX|XX]
设置一个key为value，如果key存在则覆盖；
EX seconds：过期时间，秒；
PX milliseconds：过期时间，毫秒；
NX：当键不存在时操作，相当于SETNX；
XX：只有键存在时才操作。

##GET key
获取key中的值

##SETNX key value
当键不存在时设置

##SETEX key seconds value
设置key的值并设置生存时间（秒），相当于：
SET key value
EXPIRE key seconds  # 设置生存时间

##PSETEX key milliseconds value
设置key的值并设置生存时间（豪秒）

##SETRANGE key offset value
从key中offset出开始，拿value覆盖

##GETRANGE key start end
返回key中start到end的字符串

##SETBIT key offset value
将key的值中offset位设置为0或1；
offset 参数必须大于或等于 0 ，小于 2^32 (bit 映射被限制在 512 MB 之内)

##GETBIT key offset
获取key的值中offset位的值

```shell
redis> SETBIT bit 10086 1
(integer) 0

redis> GETBIT bit 10086
(integer) 1
```

##MSET key value [key value ...]
一次性设置多个key/value

##MSETNX key value [key value ...]
一次性设置多个key/value，只有key不存在时才设置

##APPEND key value
在key的值后面追加value

##MGET key [key ...]
一次性获取多个key的值

```sh
redis> SET redis redis.com
OK

redis> SET mongodb mongodb.org
OK

redis> MGET redis mongodb
1) "redis.com"
2) "mongodb.org"

redis> MGET redis mongodb mysql     # 不存在的 mysql 返回 nil
1) "redis.com"
2) "mongodb.org"
3) (nil)
```

##GETSET key value
将给定的key设置为value，并返回其旧值。
当key不存在时报错。

##BITCOUNT key [start] [end]
计算key的值中start到end中值为1的位数。
http://doc.redisfans.com/string/bitcount.html

```sh
redis> BITCOUNT bits
(integer) 0

redis> SETBIT bits 0 1          # 0001
(integer) 0

redis> BITCOUNT bits
(integer) 1

redis> SETBIT bits 3 1          # 1001
(integer) 0

redis> BITCOUNT bits
(integer) 2
```

##STRLEN key
返回key的值的长度，key保存的不是字符串时报错

##INCR key
将 key 中储存的数字值增一；
key不存在时先初始化为0，再执行INCR操作；
key不能转换为数值时报错。

##DECR key
将 key 中储存的数字值减一；
key不存在时先初始化为0，再执行DECR操作；
key不能转换为数值时报错。

##INCRBY key increment
将 key 中储存的数字值增加increment；
key不存在时先初始化为0，再执行INCRBY操作；
key不能转换为数值时报错。

##DECRBY key decrement
将 key 中储存的数字值减少decrement；
key不存在时先初始化为0，再执行DECRBY操作；
key不能转换为数值时报错。

##INCRBYFLOAT key increment
增加的increment为浮点



