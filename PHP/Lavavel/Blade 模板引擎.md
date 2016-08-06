# Blade 模板引擎
##模板继承
###定义布局
大多数Web应用在不同页面使用同一个布局，可以将这样一个布局定义为一个单独的blade页面，可称为主布局：

```html
<!-- 存放在 resources/views/layouts/master.blade.php -->

<html>
    <head>
        <title>App Name - @yield('title')</title>
    </head>
    <body>
        @section('sidebar')
            This is the master sidebar.
        @show

        <div class="container">
            @yield('content')
        </div>
    </body>
</html>
```
其中的`@section`和`@yield`两个指令，前者是定义一个内容的片段，后者用于显示给定片段的内容。

###扩展布局
`@extends`指令用来继承主布局，继承一个布局，将会使用当前子页面中`@section`指令的内容注入到布局的片段中；
`@parent`指令来追加（而非覆盖）内容到布局中，`@parent`指令在视图渲染时将会被布局中的内容替换。

```html
<!-- 存放在 resources/views/layouts/child.blade.php -->

@extends('layouts.master')

@section('title', 'Page Title')

@section('sidebar')
    @parent

    <p>This is appended to the master sidebar.</p>
@endsection

@section('content')
    <p>This is my body content.</p>
@endsection
```

显示

```php
// 原生 PHP 视图一样，Blade 视图可以通过 view 方法直接从路由中返回：
Route::get('blade', function () {
   return view('child');
});
```

##数据显示

```php
// php中传递数据
Route::get('greeting', function () {
    return view('welcome', ['name' => 'Samantha']);
});

// 页面中显示
Hello, {{ $name }}.
// 也可使用PHP函数
The current UNIX timestamp is {{ time() }}.

// 原样输出，@{{ name }}中@会被移除，{{ name }}会显示在页面中
<h1>Laravel</h1>
Hello, @{{ name }}.

// 默认值
{{ isset($name) ? $name : 'Default' }}  // 三元运算
{{ $name or 'Default' }} // blade语法

// 原生数据，不经过Blade 的避免 XSS 攻击处理，
Hello, {!! $name !!}.
```
>注：Blade 的 {{}} 语句已经经过 PHP 的 `htmlentities` 函数处理以避免 XSS 攻击。

##流程控制

```html
// if
@if (count($records) === 1)
    I have one record!
@elseif (count($records) > 1)
    I have multiple records!
@else
    I don't have any records!
@endif

// unless
@unless (Auth::check())
    You are not signed in.
@endunless

// for
@for ($i = 0; $i < 10; $i++)
    The current value is {{ $i }}
@endfor

// foreach
@foreach ($users as $user)
    <p>This is user {{ $user->id }}</p>
@endforeach

// forelse
@forelse ($users as $user)
    <li>{{ $user->name }}</li>
    @empty
    <p>No users</p>
@endforelse

// while
@while (true)
    <p>I'm looping forever.</p>
@endwhile
```

##包含子视图

```html
<div>
    @include('shared.errors')

    <form>
        <!-- Form Contents -->
    </form>
</div>

 <!-- 包含后再追加数据 -->
@include('view.name', ['some' => 'data'])
```
> 注：不要在 Blade 视图中使用 __DIR__ 和 __FILE__ 常量，因为它们会指向缓存视图的路径。

###为集合渲染视图
你可以使用 Blade 的 `@each` 指令通过一行代码循环引入多个局部视图：

```html
@each('view.name', $jobs, 'job')
```
该指令的第一个参数是数组或集合中每个元素要渲染的局部视图，第二个参数是你希望迭代的数组或集合，第三个参数是要分配给当前视图的变量名。举个例子，如果你要迭代一个 `jobs` 数组，通常你需要在局部视图中访问 `$job` 变量。

你还可以传递第四个参数到 `@each` 指令，该参数用于指定给定数组为空时渲染的视图：

```html
@each('view.name', $jobs, 'job', 'view.empty')
```
###注释
Blade 还允许你在视图中定义注释，然而，不同于 HTML 注释，Blade 注释并不会包含到 HTML 中被返回：

```html
{{-- This comment will not be present in the rendered HTML --}}
```

##服务注入
`@inject` 指令可以用于从服务容器中获取服务，传递给 `@inject` 的第一个参数是服务将要被放置到的变量名，第二个参数是要解析的服务类名或接口名：

```html
@inject('metrics', 'App\Services\MetricsService')

<div>
    Monthly Revenue: {{ $metrics->monthlyRevenue() }}.
</div>
```

##扩展Blade
Blade 甚至还允许你自定义指令，可以使用`directive`方法来注册一个指令。当 Blade 编译器遇到该指令，将会传入参数并调用提供的回调。

下面的例子创建了一个 `@datetime($var)` 指令格式化给定的 `$var`：

```php
<?php

namespace App\Providers;

use Blade;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Perform post-registration booting of services.
     *
     * @return void
     */
    public function boot() {
        Blade::directive('datetime', function($expression) {
            return "<?php echo with{$expression}->format('m/d/Y H:i'); ?>";
        });
    }

    /**
     * 在容器中注册绑定.
     *
     * @return void
     */
    public function register() {
        //
    }
}
```
正如你所看到的，Laravel 的辅助函数`with`被用在该指令中，`with`方法简单返回给定的对象/值，允许方法链。最终该指令生成的 PHP 代码如下：

```php
<?php echo with($var)->format('m/d/Y H:i'); ?>
```


