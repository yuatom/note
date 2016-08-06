# list/tuple/dict/set
##list有序列表
```shell
# 初始化
>>> classmates = ['Michael', 'Bob', 'Tracy']
>>> classmates
['Michael', 'Bob', 'Tracy']
```
>* 使用`[]`初始化；
>* 元素索引从0开始；
>* 最后一个元素索引为-1；

```shell
# 定义空的list
>>> list = [];

# 赋值
>>> list[0] = 'test';

# 追加
>>> classmates.append('Adam')
>>> classmates
['Michael', 'Bob', 'Tracy', 'Adam']

# 插入到指定位置
>>> classmates.insert(1, 'Jack')
>>> classmates
['Michael', 'Jack', 'Bob', 'Tracy', 'Adam']

# 返回并删除最后的元素
>>> classmates.pop();
'Adam'
>>> classmates
['Michael', 'Jack', 'Bob', 'Tracy']

# 返回并删除指定元素
>>> classmates.pop(1)
'Jack'
>>> classmates
['Michael', 'Bob', 'Tracy']
```

##tuple有序列表

```shell
# 初始化
>>> classmates = ('Michael', 'Bob', 'Tracy')
```
>* 一旦初始化就不能修改；
>* 使用`()`初始化；
>* tuple不可变指的是其中元素指定的变量地址不可变；
>* 元素不可变使得代码更安全；

```shell
# 定义空的tuple
>>> t = ()
>>> t
()

# 定义一个元素的tuple
>>> t = (1) # 错误！定义的是一个int！
>>> t
1
>>> t = (1,) # 定义一个元素的tuple
>>> t
(1,) 

# ”可变“的tuple
>>> t = ('a', 'b', ['A', 'B'])
>>> t[2][0] = 'X'
>>> t[2][1] = 'Y'
>>> t
('a', 'b', ['X', 'Y'])  # 第三个元素仍然指向list的地址，但list里的指向改变了
```

##dict字典

```shell
# 定义并初始化
>>> d = {'Michael': 95, 'Bob': 75, 'Tracy': 85}
>>> d['Michael']
95

# 返回并删除一个元素
>>> d.pop('Michael')
95
```

>* 通过key-value形式哈希key来保存；
>* 可通过[key]形式获取元素，获取不到会报错；
>* 可通过get(key[,default])获取，获取不到时返回一个值；

与list相比：
>* dict查找和插入的速度极快，不会随着key的增加而变慢；
>* dict需要占用大量的内存，内存浪费多；
>*	list查找和插入的时间随着元素的增加而增加；
>* list占用空间小，浪费内存很少。


##set集合，无序，无重复

```shell
# 定义，需要传入一个list
>>> s = set([1, 2, 3])
>>> s
{1, 2, 3}

# 重复的会被过滤掉
>>> s = set([1, 1, 2, 2, 3, 3])
>>> s
{1, 2, 3}

# 添加key
>>> s.add(4)
>>> s
{1, 2, 3, 4}
>>> s.add(4)
>>> s
{1, 2, 3, 4}

# 删除key
>>> s.remove(4)
>>> s
{1, 2, 3}
```


