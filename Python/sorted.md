# sorted
对list进行排序

```python
>>> sorted([36, 5, -12, 9, -21])
[-21, -12, 5, 9, 36]
# key参数，可排序前操作，如取绝对值再排序
>>> sorted([36, 5, -12, 9, -21], key=abs)
[5, 9, -12, -21, 36]

# 默认情况下，对字符串排序，是按照ASCII的大小比较的，即'Z' < 'a'
>>> sorted(['bob', 'about', 'Zoo', 'Credit'])
['Credit', 'Zoo', 'about', 'bob']
# 可先转换为全部小写或全部大写
>>> sorted(['bob', 'about', 'Zoo', 'Credit'], key=str.lower)
['about', 'bob', 'Credit', 'Zoo']
# reverse，反序
>>> sorted(['bob', 'about', 'Zoo', 'Credit'], key=str.lower, reverse=True)
['Zoo', 'Credit', 'bob', 'about']
```

