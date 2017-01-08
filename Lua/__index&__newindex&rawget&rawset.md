#__index&__newindex&rawget&rawset

##__index
访问一个表中不存在的元素时，会触发__index元方法。
其值可以是function，也可以是table。

##__newindex
当给表中不存在的元素赋值时，会触发__newindex元方法。

##rawget
v = rawget(table, k)
不触发任何元方法来获取k的值。

##rawset
rawset(table, k, v)
不触发任何元方法来对k进行赋值。

