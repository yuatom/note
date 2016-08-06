# 匿名函数 use
从父作用域继承变量

```php
$message = 'hello';

// 没有 "use"
$example = function () {
    var_dump($message); // Notice: Undefined variable: message in /example.php on line 6
};
echo $example();    // NULL

// 继承 $message
$example = function () use ($message) {
    var_dump($message); // hello
};
echo $example();
```

