# Pub/Sub（发布/订阅）
##SUBSCRIBE channel [channel ...]
订阅一个或多个频道

##PUBLISH channel message
将消息发布到指定频道

```sh
# term1 订阅两个频道
27.0.0.1:6379> subscribe ch1 ch2
Reading messages... (press Ctrl-C to quit)
1) "subscribe"
2) "ch1"
3) (integer) 1
1) "subscribe"
2) "ch2"
3) (integer) 2

# term2 发布
127.0.0.1:6379> publish ch1 msg1
(integer) 1

#term1 实时接收
pu1) "message"
2) "ch1"
3) "msg1"

# term2 发布
127.0.0.1:6379> publish ch2 msg2
(integer) 1

#term1 实时接收
pu1) "message"      #第一次发布的
2) "ch1"            #第一次发布的
3) "msg1"           #第一次发布的
1) "message"
2) "ch2"
3) "msg2"
```

##UNSUBSCRIBE [channel [channel ...]]
退订频道

##PSUBSCRIBE pattern [pattern ...]
订阅一个或多个符合给定模式的频道

##PUNSUBSCRIBE [pattern [pattern ...]]
退订符合给定模式的频道

##PUBSUB <subcommand> [argument [argument ...]]
查看订阅相关的信息
###PUBSUB CHANNELS [pattern]
查看符合给出的匹配模式的频道

###PUBSUB NUMSUB [channel-1 ... channel-N]
查看频道的订阅数量

###PUBSUB NUMPAT
返回订阅模式（匹配的模式）的数量。
注意， 这个命令返回的不是订阅模式的客户端的数量， 而是客户端订阅的所有模式的数量总和。

```sh
# 模式1：ch*
127.0.0.1:6379> PSUBSCRIBE ch*
Reading messages... (press Ctrl-C to quit)
1) "psubscribe"
2) "ch*"
3) (integer) 1
1) "pmessage"
2) "ch*"
3) "ch1"
4) "message"

# 输出数量：1
127.0.0.1:6379> PUBSUB NUMPAT
(integer) 1

# 模式2：c*
127.0.0.1:6379> PSUBSCRIBE c*
Reading messages... (press Ctrl-C to quit)
1) "psubscribe"
2) "c*"
3) (integer) 1

# 输出数量：1
127.0.0.1:6379> PUBSUB NUMPAT
(integer) 2
```

