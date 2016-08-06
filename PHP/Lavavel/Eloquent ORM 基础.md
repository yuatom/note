# Eloquent ORM 基础
在`config/database.php`中配置数据库连接，然后在`app`目录下或其他`composer.json`文件可自动加载的地方创建模型类文件，所有模型类英继承`Illuminate\Database\Eloquent\Model`类。可用以下命令创建：

```shell
php artisan make:model User
# 生成模型的同时生成数据库迁移
php artisan make:model User --migtation
php artisan make:model User -m
```
##定义模型
###表名

```php
<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model{
    //
}
```
默认情况下模型类对应的数据库表名为类名的复数，如上例`Flight`模型对应的数据表名为`flights`。也可以在模型类中定义`$table`属性来指定表名：

```php
	  /**
     * 关联到模型的数据表
     *
     * @var string
     */
    protected $table = 'my_flights';
```

###主键
Eloquent模型默认每张表的主键为`id`，可以在模型定义`$primaryKey`来指定主键。

###时间戳
Eloquent模型默认`created_at`和`updated_at`字段存在于数据表中，可在模型中定义置`$timestamps`属性为`false`来表示数据表中没有这两个字段。同时可以设置`$dateFormat`属性来指定时间戳的格式。

```php
    /**
     * 表明模型是否应该被打上时间戳
     *
     * @var bool
     */
    public $timestamps = false;
    ```
###数据库连接
默认情况下模型使用应用配置中的默认数据库配置，可在模型中定义`$connection`属性来设置数据库连接。

```php
<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model{
    /**
     * The connection name for the model.
     *
     * @var string
     */
    protected $connection = 'connection-name';
}
```

##获取模型
通过`all`方法获取所有记录，每一条记录作为一个模型对象。

```php
$flights = Flight::all(); 
foreach ($flights as $flight) {
    echo $flight->name;
}
```
>Eloquent模型中获取多个结果返回的都是Collection的一个实例，除了使用该类提供处理结果的方法来处理外，还可以像上面的例子那样以数组的方式处理。

每一个Eloquent模型都是一个查询构建器，因此添加查询或其他子句：

```php
$flights = App\Flight::where('active', 1)
               ->orderBy('name', 'desc')
               ->take(10)
               ->get();
```

获取单个模型，`find`或`first`

```php
// 通过主键获取模型...
$flight = App\Flight::find(1);
// 获取匹配查询条件的第一个模型...
$flight = App\Flight::where('active', 1)->first();
```

如果想在查询不到对象的抛出异常，可使用`findOrFail`和`firstOrFail`方法，当查询不到时会抛出`Illuminate\Database\Eloquent\ModelNotFoundException`异常，如果异常没有被捕捉，则会向客户端返回HTTP 404响应。

```php
$model = App\Flight::findOrFail(1);
$model = App\Flight::where('legs', '>', 100)->firstOrFail();
```
聚合

```php
$count = App\Flight::where('active', 1)->count();
$max = App\Flight::where('active', 1)->max('price');
```
##插入/更新
###插入
创建一个的模型实例，设置属性后调用`save`方法保存到数据库。
如果有`created_at`和`updated_at`字段，这两个字段会在save方法调用时自动设置。

```php
/**
     * 创建一个新的航班实例
     *
     * @param  Request  $request
     * @return Response
     */
    public function store(Request $request)
    {
        // Validate the request...

        $flight = new Flight;

        $flight->name = $request->name;

        $flight->save();
    }
```

`create`方法也可以用于创建数据，该方法返回被创建的模型实例。
在使用该方法之前，需要定义`fillable`或`guarded`属性。`fillable`设置的字段名表示该字段可通过create方法赋值，`guarded`则相反。前者相当于白名单，后者相当于黑名单。这两个属性只能同时使用一个。

```php
    /**
     * 可以被批量赋值的属性.
     *
     * @var array
     */
    protected $fillable = ['name'];
    
    // 创建对象
    $flight = App\Flight::create(['name' => 'Flight 10']);
```

其他创建方法：`firstOrCreate`和`firstOrNew`。
`firstOrCreate`方法先尝试通过给定列/值对在数据库中查找记录，如果没有找到的话则通过给定属性创建一个新的记录。
`firstOrNew`方法返回的模型实例并没有持久化到数据库中，你还需要调用`save`方法手动持久化

```php
// 通过属性获取航班, 如果不存在则创建...
$flight = App\Flight::firstOrCreate(['name' => 'Flight 10']);

// 通过属性获取航班, 如果不存在初始化一个新的实例...
$flight = App\Flight::firstOrNew(['name' => 'Flight 10']);
App\Flight::save($flight);
```
###更新

```php
// 查询出数据后更新
$flight = App\Flight::find(1);
$flight->name = 'New Flight Name';
$flight->save();

// 直接针对某个数据库中数据更新
App\Flight::where('active', 1)
          ->where('destination', 'San Diego')
          ->update(['delayed' => 1]);
```
>update方法要求以数组形式传递键值对参数，代表着数据表中应该被更新的列。

##删除

```php
// 查询出数据实例后删除
$flight = App\Flight::find(1);
$flight->delete();

// 根据主键
App\Flight::destroy(1);
App\Flight::destroy([1, 2, 3]);
App\Flight::destroy(1, 2, 3);

// 根据其他条件
$deletedRows = App\Flight::where('active', 0)->delete();
```

###软删除
Eloquent的软删除会在删除后在模型上设置一个`deleted_at`属性并插入到数据库。当一条记录有飞空`deleted_at`值时，说明该记录被软删除。
要启用模型的软删除功能，可以使用模型上的Illuminate\Database\Eloquent\SoftDeletestrait并添加deleted_at列到$dates属性：

```php
<?php

namespace App;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\SoftDeletes;

class Flight extends Model{
    use SoftDeletes;

    /**
     * 应该被调整为日期的属性
     *
     * @var array
     */
    protected $dates = ['deleted_@'];
}
```

此外，还应在迁移中新增这个字段

```php
Schema::table('flights', function ($table) {
    $table->softDeletes();
});
```

以上设置之后，当调用模型的`delete`方法时，`deleted_at`会被设置成当前时间。

要判断一个模型实例是否被软删除：

```php
if ($flight->trashed()) {
    //
}
```

####查询软删除的模型
软删除的模型不会出现在普通的查询结果中，可以使用`withTrashed`或`onlyTrashed`方法使得软删除的数据模型出现在结果中或只查询软删除。

```php
// 包含软删除
$flights = App\Flight::withTrashed()
                ->where('account_id', 1)
                ->get();
// 包含软删除的关联查询
$flight->history()->withTrashed()->get();

// 只查询软删除
$flights = App\Flight::onlyTrashed()
                ->where('airline_id', 1)
                ->get();
```

恢复软删除

```php
// 恢复一个软删除
$flight->restore();

// 通过查询恢复多个软删除
App\Flight::withTrashed()
        ->where('airline_id', 1)
        ->restore();

// 在关联删除中恢复
$flight->history()->restore();
```

###永久删除

```php
// 强制删除单个模型实例...
$flight->forceDelete();
// 强制删除所有关联模型...
$flight->history()->forceDelete();
```

##查询作用域
###全局作用域
全局作用域允许我们为给定模型的所有查询添加条件约束，比如软删除功能就是使用全局作用域使得软删除的数据不出现在结果中。
####编写全局作用域
实现`Illuminate\Database\Eloquent\Scope`接口并实现`apply`方法：

```php
<?php

namespace App\Scopes;

use Illuminate\Database\Eloquent\Scope;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Builder;

class AgeScope implements Scope{
    /**
     * Apply the scope to a given Eloquent query builder.
     *
     * @param  \Illuminate\Database\Eloquent\Builder  $builder
     * @param  \Illuminate\Database\Eloquent\Model  $model
     * @return void
     */
    public function apply(Builder $builder, Model $model)
    {
        return $builder->where('age', '>', 200);
    }
}
```

####应用全局作用域
在用到全局作用域的模型中重写`boot`方法并调用`addGlobalScope`方法：

```php
<?php

namespace App;

use App\Scopes\AgeScope;
use Illuminate\Database\Eloquent\Model;

class User extends Model{
    /**
     * The "booting" method of the model.
     *
     * @return void
     */
    protected static function boot()
    {
        parent::boot();

        static::addGlobalScope(new AgeScope);
    }
}
```

添加作用域后，如果使用 `User::all()` 查询则会生成如下SQL语句：

```php
select * from `users` where `age` > 200
```

####匿名的全局作用域
在addGlobalScope方法中定义闭包回调，这样就不用每次都定义一个作用域类。

```php
<?php

namespace App;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Builder;

class User extends Model{
    /**
     * The "booting" method of the model.
     *
     * @return void
     */
    protected static function boot()
    {
        parent::boot();

        static::addGlobalScope('age', function(Builder $builder) {
            $builder->where('age', '>', 200);
        });
    }
}
```

####移除全局作用域
在某些查询中不想使用全局作用域的条件，使用`withoutGlobalScope`方法

```php
// 移除一个
User::withoutGlobalScope(AgeScope::class)->get();
// 移除所有
User::withoutGlobalScopes()->get();
// 移除部分
User::withoutGlobalScopes([FirstScope::class, SecondScope::class])->get();
```

###本地作用域
定义某些查询，便于复用。
在定义的时候在模型方法前增加`scope`前缀，在该方法中返回构建器：

```php
<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

class User extends Model{
    /**
     * 只包含活跃用户的查询作用域
     *
     * @return \Illuminate\Database\Eloquent\Builder
     */
    public function scopePopular($query)
    {
        return $query->where('votes', '>', 100);
    }

    /**
     * 只包含激活用户的查询作用域
     *
     * @return \Illuminate\Database\Eloquent\Builder
     */
    public function scopeActive($query)
    {
        return $query->where('active', 1);
    }
}
```

使用模型查询时调用作用域方法，但是不需要加上`scope`前缀，可以同时调用多个作用域：

```php
$users = App\User::popular()->active()->orderBy('created_@')->get();
```
####动态作用域
可传入查询条件的参数

```php
<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

class User extends Model{
    /**
     * 只包含给用类型用户的查询作用域
     *
     * @return \Illuminate\Database\Eloquent\Builder
     */
    public function scopeOfType($query, $type)
    {
        return $query->where('type', $type);
    }
}
```
调用查询

```php
$users = App\User::ofType('admin')->get();
```


##事件
Eloquent模型可以触发事件，允许你在模型生命周期中的多个时间点调用如下这些方法：`creating`, `created`, `updating`, `updated`, `saving`, `saved`,`deleting`, `deleted`, `restoring`, `restored`。事件允许你在一个指定模型类每次保存或更新的时候执行代码。
一个新模型被首次保存的时候，`creating`和`created`事件会被触发。如果一个模型已经在数据库中存在并调用`save`方法，`updating`/`updated`事件会被触发，无论是创建还是更新，`saving`/`saved`事件都会被调用。
举个例子，我们在`服务提供者`中定义一个Eloquent事件监听器，在事件监听器中，我们会调用给定模型的`isValid`方法，如果模型无效会返回`false`。如果从Eloquent事件监听器中返回`false`则取消`save`/`update`操作：

```php
<?php

namespace App\Providers;

use App\User;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider{
    /**
     * 启动所有应用服务
     *
     * @return void
     */
    public function boot()
    {
        User::creating(function ($user) {
            if ( ! $user->isValid()) {
                return false;
            }
        });
    }

    /**
     * 注册服务提供者.
     *
     * @return void
     */
    public function register()
    {
        //
    }
}
```


