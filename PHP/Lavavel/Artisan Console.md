# Artisan Console
Laravel自带有一些`命令行`命令，可使用以下命令查看：

```shell
php artisan list
```

##编写命令
自定义的命令类文件默认保存在`app/Console/Commands`目录下，也可以自己保存在`composer.json`文件能自动加载的目录。
创建命令行类文件可用以下命令：

```shell
# 基本创建
php artisan make:console SendEmails
# 分配终端调用的命令
php artisan make:console SendEmails --command=emails:send
```
以上命令会生成`app/Console/Commands/SendEmails.php`这一个类文件。
该文件将由signature和description属性以及handle方法构成。前面两个属性在命令行执行`list`命令时用到，`handle`方法是该命令类文件定义的命令执行时被调用。

```php
<?php

namespace App\Console\Commands;

use App\User;
use App\DripEmailer;
use Illuminate\Console\Command;
use Illuminate\Foundation\Inspiring;

class Inspire extends Command{
    /**
     * 控制台命令名称
     *
     * @var string
     */
    protected $signature = 'email:send {user}';

    /**
     * 控制台命令描述
     *
     * @var string
     */
    protected $description = 'Send drip e-mails to a user';

    /**
     * The drip e-mail service.
     *
     * @var DripEmailer
     */
    protected $drip;

    /**
     * 创建新的命令实例
     *
     * @param  DripEmailer  $drip
     * @return void
     */
    public function __construct(DripEmailer $drip)
    {
        parent::__construct();
        $this->drip = $drip;
    }

    /**
     * 执行控制台命令
     *
     * @return mixed
     */
    public function handle()
    {
        $this->drip->send(User::find($this->argument('user')));
    }
}
```

##命令I/O
###定义期望输入
即命令的参数。`signature`属性用来定义命令的名称、参数以及选项。
以下代码定义在执行命令时需要输入`user`参数：

```php
/**
 * 控制台命令名称
 *
 * @var string
 */
protected $signature = 'email:send {user}';
```

配置可选参数及参数默认值：

```php
// 选项参数...
email:send {user?}
// 带默认值的选项参数...
email:send {user=foo}
```

配置选项，以两个短划线`-`起始。

```php
/**
 * 控制台命令名称
 *
 * @var string
 */
protected $signature = 'email:send {user} {--queue}';
```

执行命令，当`--queue`选择出现时，其值为`true`，否则为`false`：

```shell
php artisan email:send 1 --queue
```

配置需要传入具体指的选项，定义时在选项名后面加上`=`：

```php
/**
 * 控制台命令名称
 *
 * @var string
 */
protected $signature = 'email:send {user} {--queue=}';
```

执行命令

```shell
php artisan email:send 1 --queue=default
```

其他配置选项

```php
// 给选项配置默认值
email:send {user} {--queue=default}
// 给选项配置简写
email:send {user} {--Q|queue}
// 定义参数和选项以便指定输入数组，可以使用字符*
email:send {user*}
email:send {user} {--id=*}

// 输入描述，通过冒号将参数和描述进行分隔的方式
protected $signature = 'email:send
    {user : The ID of the user}
    {--queue= : Whether the job should be queued}';
```

###获取输入
使用`argument`和`option`方法来获取参数和选项的值。

```php
/**
 * 执行控制台命令
 *
 * @return mixed
 */
public function handle(){
    $userId = $this->argument('user');
}

// 以数组形式获取所有参数
$arguments = $this->argument();

// 选项的获取与参数一样
// 获取指定选项...
$queueName = $this->option('queue');
// 获取所有选项...
$options = $this->option();
```

###输入提示
在命令执行期间让用户输入参数，`ask`方法可以输出提示或问题给用户，然后返回用户的输入：

```php
public function handle(){
    $name = $this->ask('What is your name?');
}
```
`secret`方法和`ask`方法类似，但用户输入的内容不会显示在终端，用于密码等敏感信息的输入

```php
$password = $this->secret('What is the password?');
```

`confirm`方法用于让用户确认信息，该方法默认返回`false`，当输入为`y`时返回`true`：

```php
if ($this->confirm('Do you wish to continue? [y|N]')) {
    //
}
```

`anticipate`给出选择供用户参考，但是用户可以自己输入其他内容：

```php
$name = $this->anticipate('What is your name?', ['Taylor', 'Dayle']);
```

`choice`方法让用户必须从给出的选项中选择，用户选择选择的索引，但是在代码中获取到的时选项的具体值。也可以设置默认值。

```php
$name = $this->choice('What is your name?', ['Taylor', 'Dayle'], false);
```

###输出
`line`,`info`, `comment`, `question` 和 `error`等方法可用于在终端输出信息，每个方法输出的ANSI颜色都不同

`table`布局

进度条

##注册命令
在`app/Console/Kernel.php`类文件的`command`属性注册命令：

```php
protected $commands = [
    'App\Console\Commands\SendEmails'
];
```

##在代码中调用命令
使用`Artisan` Facade的`call`方法，第一个参数为命令名称，第二个参数为数组用于获取命令的参数和选项

```php
Route::get('/foo', function () {
    $exitCode = Artisan::call('email:send', [
        'user' => 1, '--queue' => 'default'
    ]);
});
```

`Artisan`上的`queue`方法可以将命令的执行放到队列中让队列工作者处理

```php
Route::get('/foo', function () {
    Artisan::queue('email:send', [
        'user' => 1, '--queue' => 'default'
    ]);
});
```

###在命令类的handle方法中调用其他命令
使用当前类继承的`call`方法：

```php
/**
 * 执行控制台命令
 *
 * @return mixed
 */
public function handle(){
    $this->call('email:send', [
        'user' => 1, '--queue' => 'default'
    ]);
}
```

如果要屏蔽命令的所有输出，调用`callSilent`方法：

```php
$this->callSilent('email:send', [
    'user' => 1, '--queue' => 'default'
]);
```


