# # Eloquent ORM 修改器&访问器
访问器，获取模型属性时调用。
修改器，设置模型属性时调用。
##定义访问器&修改器
访问器，在模型中定义一个`getFooAttribute`，`Foo`为字段名的驼峰形式。
修改器，在模型中定义一个`setFooAttribute`，`Foo`为字段名的驼峰形式。

```php
/**
* 获取用户的名字
*
* @param  string  $value
* @return string
*/
public function getFirstNameAttribute($value)
{
   return ucfirst($value);
}
    
/**
* 设置用户的名字
*
* @param  string  $value
* @return string
*/
public function setFirstNameAttribute($value)
{
   $this->attributes['first_name'] = strtolower($value);
}

// 返回处理过的值
$user = App\User::find(1);
$firstName = $user->first_name;

// 保存处理过的值
$user = App\User::find(1);
$user->first_name = 'Sally';
```

##属性转换
模型中的`$casts`属性用来对字段数据类型进行转换。
`$casts`属性是一个数组，键是要转换的字段名，值是要转换的类型，目前支持`integer`, `real`, `float`, `double`, `string`, `boolean`, `object`，`array`，`collection`，`date`和`datetime`。

```php
<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

class User extends Model{
    /**
     * 应该被转化为原生类型的属性
     *
     * @var array
     */
    protected $casts = [
        'is_admin' => 'boolean',
    ];
}

// 即使底层存储在数据库中的值是integer，访问时会被转换成boolean
$user = App\User::find(1);
if ($user->is_admin) {
    //
}

```

`array`类型用于处理被存储为序列号JSON的数据

```php
<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

class User extends Model{
    /**
     * 应该被转化为原生类型的属性
     *
     * @var array
     */
    protected $casts = [
        'options' => 'array',
    ];
}

// $options会被序列号存到数据库中
$user = App\User::find(1);
$options = $user->options;
$options['key'] = 'value';
$user->options = $options;
$user->save();
```

##日期修改器
模型中的`$dates`属性，用来定义哪些属性要调整成日期类型。
Eloquent中的日期类型的值为Carbon 实例，该类继承自 PHP 原生的Datetime类，并提供了各种有用的方法。

```php
<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

class User extends Model{
    /**
     * 应该被调整为日期的属性
     *
     * @var array
     */
    protected $dates = ['created_@', 'updated_@', 'disabled_@'];
}

// 保存
$user = App\User::find(1);
$user->disabled_@ = Carbon::now();
$user->save();

// 获取
$user = App\User::find(1);
return $user->disabled_@->getTimestamp();
```
>默认情况下，时间戳的格式是“Y-m-d H:i:s”，如果你需要自定义时间戳格式，在模型中设置$dateFormat属性，该属性决定日期属性存储在数据库以及序列化为数组或 JSON 时的格式


