# HTTP响应
##基本响应

```php
Route::get('/', function () {
    return 'Hello World';
});
```
###Response 对象

```php
use Illuminate\Http\Response;

// 新建对象
Route::get('home', function () {
return (new Response($content, $status))
->header('Content-Type', $value);
});

// response辅助函数
Route::get('home', function () {
    return response($content, $status)
        ->header('Content-Type', $value);
});

// 添加响应头
return response($content)
    ->header('Content-Type', $type)
    ->header('X-Header-One', 'Header Value')
    ->header('X-Header-Two', 'Header Value');

// withHeaders方法，数组形式添加响应头
return response($content)
    ->withHeaders([
        'Content-Type' => $type,
        'X-Header-One' => 'Header Value',
        'X-Header-Two' => 'Header Value',
    ]);
 
// 添加cookie响应   
return response($content)->header('Content-Type', $type)
    ->cookie('name', 'value');
// cookie额外参数->cookie($name, $value, $minutes, $path, $domain, $secure, $httpOnly)
```
默认情况下Laravel生成的cookie是经过加密和签名的，可以使用中间件  App\Http\Middleware\EncryptCookies 的 $except 属性来排除这些 Cookie：

```php
/**
 * 不需要被加密的cookies名称
 *
 * @var array
 */
protected $except = [
    'cookie_name',
];
```

视图

```php

return response()->view('hello', $data)->header('Content-Type', $type);
```

json

```php
return response()->json(['name' => 'Abigail', 'state' => 'CA']);

// jsonp回调
return response()->json(['name' => 'Abigail', 'state' => 'CA'])
    ->setCallback($request->input('callback'));
```

文件下载

```php
return response()->download($pathToFile);
return response()->download($pathToFile, $name, $headers);
```

##重定向

```php
Route::get('dashboard', function () {
    return redirect('home/dashboard');
});

// back()返回上一页
Route::post('user/profile', function () {
    // 验证请求...
    return back()->withInput();
});

// 重定向到路由名的链接
return redirect()->route('login');
return redirect()->route('profile', [1]);	// 带参数
return redirect()->route('profile', [$user]);	// 模型绑定

// 重定向到控制器动作
return redirect()->action('HomeController@index');
return redirect()->action('UserController@profile', [1]);	// 带参数

Route::post('user/profile', function () {
    // 更新用户属性...
    return redirect('dashboard')->with('status', 'Profile updated!');
});

// 带一次性session
Route::post('user/profile', function () {
    // 更新用户属性...
    return redirect('dashboard')->with('status', 'Profile updated!');
});
```

##响应宏
定义一个自定义的响应并且在多个路由和控制器中复用，可以使用 Illuminate\Contracts\Routing\ResponseFactory 实现类或者 Response Facade上的  macro 方法:

```php
<?php

namespace App\Providers;

use Response;
use Illuminate\Support\ServiceProvider;

class ResponseMacroServiceProvider extends ServiceProvider
{
    /**
     * Perform post-registration booting of services.
     *
     * @return void
     */
    public function boot()
    {
        Response::macro('caps', function ($value) {
            return Response::make(strtoupper($value));
        });
    }
}
```

macro 方法接收响应名称作为第一个参数，闭包函数作为第二个参数，macro 的闭包在 ResponseFactory 实现类或辅助函数 response 中调用 macro 名称的时候被执行：

```php
// 调用
return response()->caps('foo');
```


