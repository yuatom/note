# PHP7
##1.标量类型声明
强制模式
严格模式

旧版本的函数参数声明只能是数组和类。

##2.返回类型声明

##3. ??运算符
如果变量存在且值不为NULL，它就会返回自身的值，否则返回第二个操作数。
旧版： isset($_GET[‘id']) ? $_GET[id] : err;

新版： $_GET['id'] ?? 'err';

##4.<=>太空船操作符
echo $a <=> $b;
当 $a 大于、等于或小于 $b 时它分别返回 -1 、 0 或 1

##5.define()定义常量数组

define('ANIMALS', ['dog', 'cat', 'bird']);
echo ANIMALS[1]; // outputs "cat"

##6.匿名类

```php
// define
$object = new class{

};

// demo
interface Logger {

public function log(string $msg);

}

class Application {

private $logger;

public function getLogger(): Logger {

return $this->logger;

}

public function setLogger(Logger $logger) {

$this->logger = $logger;

}

}

$app = new Application;

$app->setLogger(new class implements Logger {

public function log(string $msg) {

echo $msg;

}

});

var_dump($app->getLogger());
```

##7. Closure::call()

##8.unserialize()过滤

```php
// 将所有对象分为 __PHP_Incomplete_Class 对象

$data = unserialize($foo, ["allowed_classes" => false]);

// 将所有对象分为 __PHP_Incomplete_Class 对象 除了 ClassName1 和 ClassName2

$data = unserialize($foo, ["allowed_classes" => ["ClassName1", "ClassName2"]);

// 默认行为，和 unserialize($foo) 相同

$data = unserialize($foo, ["allowed_classes" => true]);

```

##9.assert()方法

##10.同一个namespace下的可以用一个use语句导入

```php
//PHP7 之前

use some\namespace\ClassA;

use some\namespace\ClassB;

use some\namespace\ClassC as C;

use function some\namespace\fn_a;

use function some\namespace\fn_b;

use function some\namespace\fn_c;

use const some\namespace\ConstA;

use const some\namespace\ConstB;

use const some\namespace\ConstC;

// PHP7 之后

use some\namespace\{ClassA, ClassB, ClassC as C};

use function some\namespace\{fn_a, fn_b, fn_c};

use const some\namespace\{ConstA, ConstB, ConstC};
```

##11.intdic()除

```php
var_dump(intdiv(7, 2)); // int(3)
```

##12.生成安全随机字符串的函数
random_bytes — 加密生存被保护的伪随机字符串
random_int — 加密生存被保护的伪随机整数

##13.session配置
session_start() 函数可以接收一个数组作为参数，可以覆盖 php.ini 中 session 的配置项。

##14.preg_replace_callback_array()
新增了一个函数 preg_replace_callback_array() ，使用该函数可以使得在使用 preg_replace_callback() 函数时代码变得更加优雅。在 PHP7 之前，回调函数会调用每一个正则表达式，回调函数在部分分支上是被污染了。

##15.生成器返回值
在 PHP5.5 引入生成器的概念。生成器函数每执行一次就得到一个 yield 标识的值。在 PHP7 中，当生成器迭代完成后，可以获取该生成器函数的返回值。通过 Generator::getReturn() 得到。

```php

function generator() {
    yield 1;
    yield 2;
    yield 3;
    return "a";
}

$generatorClass = ("generator")();
foreach ($generatorClass as $val) {
    echo $val.” “;
}

echo $generatorClass->getReturn();
```

##16.生成器中嵌入其他生成器
在生成器中可以引入另一个或几个生成器，只需要写 yield from functionName1

```php
function generator1(){
    yield 1;
    yield 2;
    yield from generator2();
    yield from generator3();
}

function generator2(){
    yield 3;
    yield 4;
}

function generator3(){
    yield 5;
    yield 6;
}

foreach (generator1() as $val){
    echo $val, " ";
}
```

##17.foreach不改变数组指针

```php
$array = [0, 1, 2];

foreach ($array as &$val) {
    var_dump(current($array));
}


PHP5 输出：

int(1)

int(2)

bool(false)

PHP7 输出：

int(0)

int(0)

int(0)
```

##18.foreach迭代时能动态添加元素
在PHP中，foreach时使用的是数组的一份拷贝。

```php
$array = [0];

foreach ($array as &$val) {

var_dump($val);

$array[1] = 1;

}

?>

PHP5 输出：

int(0)

PHP7 输出：

int(0)

int(1)
```

##19.new创建的对象不能以&引用的方式赋值

##20.移除 $HTTP_RAW_POST_DATA变量，使用php://input代替

