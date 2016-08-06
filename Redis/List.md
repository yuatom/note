# List
##LINDEX key index
返回列表key中下标为index的元素，index从0开始

##LINSERT key BEFORE|AFTER pivot value
在值为pivot的元素之前/之后插入value；
如果pivot不存在，不做任何操作；
如果key不存在，不做任何操作

##LLEN key
返回列表 key 的长度

##LPOP key
移除并返回列表 key 的头元素

##LPUSH key value [value ...]
将一个或多个值 value 插入到列表 key 的表头；
key不存在则创建；

##LPUSHX key value
将value插入到表头，key不存在则不操作。

##LRANGE key start stop
返回key中start到stop之间的元素

##LREM key count value
移除count个与value相等的元素；
count=0，移除key中所有与value相等的元素；
count>0，从表头开始，删除count个；
count<0，从表尾开始，删除count个。

##LSET key index value
设置下标为index的元素为value，如果index超出范围，返回一个错误。

##LTRIM key start stop
只保留key中start到stop的元素

##RPOP key
移除并返回列表 key 的尾元素

##RPOPLPUSH source destination
将source最后一个元素弹出返回给客户端，并将该元素插入到destination的头部。

##RPUSH key value [value ...]
将一个或多个元素添加到表尾。

##RPUSHX key value
在尾部插入value，key不存在时不做任何操作。

##BLPOP key [key ...] timeout
`LPOP`命令的阻塞版本。
当给定列表内没有任何元素可供弹出的时候，连接将被 BLPOP 命令阻塞，直到等待超时或发现可弹出元素。
当给定多个 key 参数时，按参数 key 的先后顺序依次检查各个列表，弹出第一个非空列表的头元素

##BRPOP key [key ...] timeout
`RPOP`命令的阻塞版本。
当给定的key中没有可以弹出的元素时，连接会被`BRPOP`阻塞，直到等到超时或发现有可以弹出的元素。
当给定多个 key 参数时，按参数 key 的先后顺序依次检查各个列表，弹出第一个非空列表的尾部元素

##BRPOPLPUSH source destination timeout
`RPOPLPUSH`的阻塞版本.

