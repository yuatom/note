# # Eloquent ORM 序列化
转换数组，`toArray`:

```php
// 转换对象
$user = App\User::with('roles')->first();
return $user->toArray();

// 转换集合，Eloquent模型返回多个结果时以集合类型返回
$users = App\User::all();
return $users->toArray();
```

转换JSON，`toJSON`

```php
// 转移单个模型
$user = App\User::find(1);
return $user->toJson();

// 当模型或集合被转换为字符串时，会自动调用toJson方法
$user = App\User::find(1);
return (string) $user;

// 在路由中直接返回，由于这里返回的是String，所以也会被转换为String
Route::get('users',function(){
    return App\User::all();
});
```

##设置在转换成JSON时要隐藏的属性
`$hidden`属性，设置要隐藏的属性，数组，传入字段名。
>隐藏关联时，使用关联关系的方法名，而不是动态属性名。

```php
<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

class User extends Model{
    /**
     * 在数组中隐藏的属性
     *
     * @var array
     */
    protected $hidden = ['password'];
}
```

>`$visible`属性，设置要显示的属性，数组，传入字段名。

```php
<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

class User extends Model{
    /**
     * 在数组中显示的属性
     *
     * @var array
     */
    protected $visible = ['first_name', 'last_name'];
}
```

>`$makeVisible`模型方法，临时显示隐藏的属性

```php
return $user->makeVisible('attribute')->toArray();
```

##添加数据库中没有的字段到数组中
需要先定义一个访问器，然后再模型中定义`$appends`：

```php
<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

class User extends Model{
    /**
     * 为用户获取管理员标识
     *
     * @return bool
     */
    public function getIsAdminAttribute()
    {
        return $this->attributes['admin'] == 'yes';
    }
    
    /**
     * 追加到模型数组表单的访问器
     *
     * @var array
     */
    protected $appends = ['is_admin'];
}
```
>字段被添加到 appends 列表之后，将会被包含到模型数组和 JSON 中，appends 数组中的字段还会遵循模型中配置的 visible 和 hidden 设置。

