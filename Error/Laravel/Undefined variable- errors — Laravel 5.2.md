# Undefined variable: errors — Laravel 5.2
原因：控制器中没有加载一次性session的error数据

解决：
>* `app/Kernel.php`的`$middleware`属性中加入`\Illuminate\View\Middleware\ShareErrorsFromSession::class`中间件，即全局加入这个中间件
>* 控制器中加入中间件组`web`：

```php
Route::group(['middleware' => 'web'], function() {
    // Place all your web routes here...(Cut all `Route` which are define in `Route file`, paste here) 
});
```

