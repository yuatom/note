# Facades
Facades 提供一个静态接口给在应用程序的**服务容器**中可以取用的类。
Laravel的Facades或自定义的Facades都会继承基类Facade，并且实现getFacadeAccessor方法，在该方法中定义要从容器中解析什么。基类 Facade 利用 __callStatic() 魔术方法来从你的 facade 调用到解析出来的对象。
> 例如：

```php
<?php

namespace App\Http\Controllers;

use Cache;
use App\Http\Controllers\Controller;

class UserController extends Controller{
    /**
     * 为指定用户显示属性
     *
     * @param  int  $id
     * @return Response
     */
    public function showProfile($id)
    {
        $user = Cache::get('user:'.$id);

        return view('profile', ['user' => $user]);
    }
}
```
以上代码引入了Cache Facade，Cache 类继承基类 Facade 并定义一个 getFacadeAccessor() 方法。记住，这个方法的工作是返回服务容器绑定的名称。
当用户在 Cache 的 facade 上参考任何的静态方法，Laravel 会从服务容器解析被绑定的 cache ，并对该对象执行被请求的方法 (在这个例子中， get)。

Illuminate\Support\Facades\Cache中并没有get方法

```php
class Cache extends Facade {

    /**
     * 取得组件的注册名称
     *
     * @return string
     */
    protected static function getFacadeAccessor() { return 'cache'; }

}
```
getFacadeAccessor返回服务器绑定的名称，这个绑定是在服务提供者中的register方法中绑定的，然后在config/app.php中加载服务提供者。

```php
// CacheServiceProvider中绑定
public function register() {
        $this->app->singleton('cache', function ($app) {
            return new CacheManager($app);
        });

        $this->app->singleton('cache.store', function ($app) {
            return $app['cache']->driver();
        });

        $this->app->singleton('memcached.connector', function () {
            return new MemcachedConnector;
        });

        $this->registerCommands();
    }
```

```php
//两种形式等价
$value = Cache::get('key');
$value = $app->make('cache')->get('key');
```
##创建Facade
Facade需要三个东西：
>* 一个服务容器绑定。
>* 一个 facade 类。
>* 一个 facade 别名配置。

实际上处理的类:

```php
namespace PaymentGateway;

class Payment {

    public function process()
    {
        //
    }

}
```

服务器绑定，PaymentServiceProvider的register中包含以下代码：

```php
App::bind('payment', function()
{
    return new \PaymentGateway\Payment;
});
```

Facade类

```php
use Illuminate\Support\Facades\Facade;

class Payment extends Facade {
	// return的payment为PaymentServiceProvider中bind的名称
    protected static function getFacadeAccessor() { return 'payment'; }

}
```

在app.php中配置别名，aliases数组中添加：

```php
   'Payment'   => Illuminate\Support\Facades\Payment::class,
```

使用:

```php
Payment::process();
```

>自动加载别名的附注
在 aliases 数组中的类在某些实例中不能使用，因为 PHP 将不会尝试去自动加载未定义的类型提示类。如果 \ServiceWrapper\ApiTimeoutException 命别名为 ApiTimeoutException，即便有异常被抛出，在 \ServiceWrapper 命名空间外面的 catch(ApiTimeoutException $e) 将永远捕捉不到异常。类似的问题在有类型提示的别名类一样会发生。唯一的替代方案就是放弃别名并用 use 在每一个文件的最上面引入你希望类型提示的类。


| Facade	| Class	| Service Container Binding| 
| ---- | ---- | ---- |
| App	| Illuminate\Foundation\Application	| app| 
| Artisan	| Illuminate\Console\Application	| artisan| 
| Auth	| Illuminate\Auth\AuthManager	| auth| 
| Auth (实例)| 	Illuminate\Auth\Guard| 
| Blade	| Illuminate\View\Compilers\BladeCompiler	| blade.compiler| 
| Bus	| Illuminate\Contracts\Bus\Dispatcher| 
| Cache	| Illuminate\Cache\CacheManager	| cache| 
| Config	| Illuminate\Config\Repository	| config| 
| Cookie	| Illuminate\Cookie\CookieJar	| cookie| 
| Crypt	| Illuminate\Encryption\Encrypter	| encrypter| 
| DB	| Illuminate\Database\DatabaseManager	| db| 
| DB (实例)	| Illuminate\Database\Connection| 
| Event	| Illuminate\Events\Dispatcher	| events| 
| File	| Illuminate\Filesystem\Filesystem	| files| 
| Hash	| Illuminate\Contracts\Hashing\Hasher	| hash| 
| Input	| Illuminate\Http\Request	| request| 
| Lang	| Illuminate\Translation\Translator	| translator| 
| Log	| Illuminate\Log\Writer	| log| 
| Mail	| Illuminate\Mail\Mailer	| mailer| 
| Password	| Illuminate\Auth\Passwords\PasswordBroker	| auth.password| 
| Queue	| Illuminate\Queue\QueueManager	| queue| 
| Queue (实例)	| Illuminate\Queue\QueueInterface| 
| Queue (基础类)	| Illuminate\Queue\Queue| 
| Redirect	| Illuminate\Routing\Redirector	| redirect| 
| Redis	| Illuminate\Redis\Database| 	| redis| 
| Request	| Illuminate\Http\Request	| request| 
| Response	| Illuminate\Contracts\Routing\ResponseFactory
| Route	| Illuminate\Routing\Router	| router| 
| Schema	| Illuminate\Database\Schema\Blueprint| 
| Session	| Illuminate\Session\SessionManager	| session| 
| Session (实例)	| Illuminate\Session\Store
| Storage	| Illuminate\Contracts\Filesystem\Factory	| filesystem| 
| URL	| Illuminate\Routing\UrlGenerator 	| url| 
| Validator	| Illuminate\Validation\Factory	| validator| 
| Validator (实例)	| Illuminate\Validation\Validator| 
| View	| Illuminate\View\Factory	| view| 
| View (实例)	| Illuminate\View\View| 

