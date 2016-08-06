# map/reduce/filter

##map/reduce
```python
# 把list中的每一个元素传入给func，将结果放到一个list中
map(func, list)

>>> list(map(str, [1, 2, 3, 4, 5, 6, 7, 8, 9]))
['1', '2', '3', '4', '5', '6', '7', '8', '9']

# func接收两个参数，并将产生的结果与list中的下一个元素继续传入给func
reduce(func, list)
# 相当于
reduce(f, [x1, x2, x3, x4]) = f(f(f(x1, x2), x3), x4)
```

##filter

```python
# 将list中每个元素传入到func中，如果func的结果是true则将该元素放到要filter返回的list，如果是false则不返回该元素。
filter(func,list)
```


