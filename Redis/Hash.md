# # Hash
##HDEL key field [field ...]
删除哈希表key中的一个或多个域，返回成功移除的域的个数。

##HEXISTS key field
哈希表key中是否存在field

##HGET key field
获取哈希表key中的field的值

```shell
redis> HSET site redis redis.com
(integer) 1

redis> HGET site redis
"redis.com"
```

##HGETALL key
返回哈希表 key 中，所有的域和值。

```shell
redis> HSET people jack "Jack Sparrow"
(integer) 1

redis> HSET people gump "Forrest Gump"
(integer) 1

redis> HGETALL people
1) "jack"          # 域
2) "Jack Sparrow"  # 值
3) "gump"
4) "Forrest Gump"
```

##HINCRBY key field increment
对哈希表key中的field的值增加increment，可为正负。
如果表中没有field这个域，则先创建该域名初始化为0，在增加increment。
如果field的值是字符串，则返回执行失败，原值不变。

```
# increment 为正数
redis> HEXISTS counter page_view    # 对空域进行设置
(integer) 0
redis> HINCRBY counter page_view 200
(integer) 200
redis> HGET counter page_view
"200"


# increment 为负数
redis> HGET counter page_view
"200"
redis> HINCRBY counter page_view -50
(integer) 150
redis> HGET counter page_view
"150"


# 尝试对字符串值的域执行HINCRBY命令
redis> HSET myhash string hello,world       # 设定一个字符串值
(integer) 1
redis> HGET myhash string
"hello,world"
redis> HINCRBY myhash string 1              # 命令执行失败，错误。
(error) ERR hash value is not an integer
redis> HGET myhash string                   # 原值不变
"hello,world"
```

##HINCRBYFLOAT key field increment
为哈希表 key 中的域 field 加上浮点数增量 increment。
如果表中没有field这个域，则先创建该域名初始化为0，在增加increment。

##HKEYS key
返回哈希表 key 中的所有域

##HLEN key
返回哈希表 key 中域的数量

##HMGET key field [field ...]
获取哈希表key中一个或过个域的值；
如果给定的field不存，返回nil

##HMSET key field value [field value ...]
一次性设置哈希表key中多个域。

##HSET key field value
设置哈希表中一个域

##HSETNX key field value
如果哈希表中field不存在，则增加该域并设置为value；
如果该域存在，则不操作。

##HVALS key
返回哈希表key中所有的指。

```
redis> HMSET website google www.google.com yahoo www.yahoo.com
OK
redis> HVALS website
1) "www.google.com"
2) "www.yahoo.com"
```

##HSCAN key cursor [MATCH pattern] [COUNT count]
用于迭代哈希键中的键值对，返回的每个元素都是一个键值对，一个键值对由一个键和一个值组成。

```
127.0.0.1:6379> HSCAN user_1 0
1) "0"
2) 1) "id"
   2) "1"
   3) "username"
   4) "tony"
   5) "password"
   6) "111222"
```


