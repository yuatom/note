# Limit 优化

```SQL
SELECT ＊ FROM table LIMIT offset,szie;
```

##当offset比较小时
如：

```SQL
SELECT * FROM table LIMIT 10,10;
```
可直接使用单句执行。
##当offset比较大时
如：

```SQL
SELECT * FROM table LIMIT 10000,10;
```

可先从offset里取出id然后再根据这个id的条件取后面的size：

```SQL
SELECT * FROM table WHERE `id` >= (
	SELECT id FROM table ORDER BY id LIMIT 10000,1
) LIMIT 10;
```






