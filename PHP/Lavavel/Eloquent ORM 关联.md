# Eloquent ORM 关联

##定义关联关系
###一对一
`hasOne`
>* 第一个参数是连表的类名
>* 第二个参数是连表中的字段，默认是“主表类名_id”
>* 第三个参数是主表中的字段，默认是“id”

```php
class User extends Model{
    /**
     * 获取关联到用户的手机
     */
    public function phone()
    {
        return $this->hasOne('App\Phone');	// user表中的id与phone表中的user_id
    }
 }
 
 // 使用
 $phone = User::find(1)->phone;   
 
 // 其他定义
 return $this->hasOne('App\Phone', 'foreign_key');	// user表中的id和phone中的foreign_key
 return $this->hasOne('App\Phone', 'foreign_key', 'local_key');	// user表中的local_key和phone中的foreign_key
```
与`hasOne`对应的关联`belongsTo`
当在`user`中定义了与`phone`的`hasOne`关系后可以在`user`中访问`phone`，此时可以在`phone中`定义`belongsTo`关联来访问`user`

```php
class Phone extends Model{
    /**
     * 获取手机对应的用户
     */
    public function user()
    {
        return $this->belongsTo('App\User');	// phone中的user_id对应user中的id
    }
}


return $this->belongsTo('App\User', 'foreign_key');	// phone中的foreign_key对应user的id
return $this->belongsTo('App\User', 'foreign_key', 'other_key');	// phone中的foreign_key对应user中的other_key

```

###一对多
`hasMany`

```php
class Phone extends Model{
    /**
     * 获取手机对应的用户
     */
    public function user()
    {
        return $this->belongsTo('App\User');
    }
}

// 其他定义
return $this->belongsTo('App\User', 'foreign_key');
return $this->belongsTo('App\User', 'foreign_key', 'other_key');

// 调用
// 普通查询
$comments = App\Post::find(1)->comments;
// 定义查询器
$comments = App\Post::find(1)->comments()->where('title', 'foo')->first();
foreach ($comments as $comment) {
    //
}
```
相对应的关系也是`belongsTo`

###多对多
`belongsToMany`，多对多时需要三个表，除了两个常规的数据表外还需要一个关系表
>* 第一个参数，关联的类名
>* 第二个参数，关系表的表名，默认是两个表名按字母顺序通过_连接起来
>* 第三个参数，关系表中对应主表id的字段名
>* 第四个参数，关系表中对应连表id的字段名

```php
<?php
// users、roles和role_user，role_user表按照关联模型名的字母顺序命名，并且包含user_id和role_id两个列
class User extends Model{
    /**
     * 用户角色
     */
    public function roles()
    {
        return $this->belongsToMany('App\Role');	// role_user中的user_id、role_id
    }
}

return $this->belongsToMany('App\Role', 'user_roles');	// user_roles中的user_id、role_id

return $this->belongsToMany('App\Role', 'user_roles', 'user_id', 'role_id');

```

####访问中间表的字段
使用模型中的`pivot`属性来访问

```php
$user = App\User::find(1);

foreach ($user->roles as $role) {
    echo $role->pivot->created_@;
}
```
>注意我们获取到的每一个Role模型都被自动赋上了pivot属性。该属性包含一个代表中间表的模型，并且可以像其它 Eloquent 模型一样使用。
>默认情况下，只有模型键才能用在pivot对象上，如果你的pivot表包含额外的属性，必须在定义关联关系时进行指定：

```php
return $this->belongsToMany('App\Role')->withPivot('column1', 'column2');
//如果你想要你的pivot表自动包含created_at和updated_at时间戳，在关联关系定义时使用withTimestamps方法：
return $this->belongsToMany('App\Role')->withTimestamps();
```

###多个一对多的相连
`hasManyThrough`，A表和B表关联，B表和C表关联，可以通过远层一对多从A获取C的数据。
>* 第一个参数是最终想获取的模型
>* 第二个参数是中间模型
>* 第三个参数是中间模型的字段名
>* 第四个参数是最终模型的字段名
例子：

```
countries
    id - integer
    name - string

users
    id - integer
    country_id - integer
    name - string

posts
    id - integer
    user_id - integer
    title - string
```
从Contries获取Post

```php
<?php
class Country extends Model{
    /**
     * 获取指定国家的所有文章
     */
    public function posts()
    {
        return $this->hasManyThrough('App\Post', 'App\User');
    }
}
```
###多态关联
例如，有一个点赞`likes`的表，存放着对文章`posts`的点赞和对评论`comments`的点赞。可以对likes表定义动态关联，使得能获取针对主体类型获取不同的like数据。

例子

```
posts
    id - integer
    title - string
    body - text

comments
    id - integer
    post_id - integer
    body - text

likes
    id - integer
    likeable_id - integer	// 对应comment或post的id
    likeable_type - string	//	类型
```

`like`模型定义`likeable`方法，返回模型的`morphTo`方法，用于在主体模型中定义使用。
主体模型中调用模型的`morphMany`方法定义关联。

```php
<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

class Like extends Model{
    /**
     * 获取所属的likeable模型
     */
    public function likeable()
    {
        return $this->morphTo();
    }
}

class Post extends Model{
    /**
     * 获取该文章的所有点赞
     */
    public function likes()
    {
        return $this->morphMany('App\Like', 'likeable');
    }
}

class Comment extends Model{
    /**
     * 获取该评论的所有点赞
     */
    public function likes()
    {
        return $this->morphMany('App\Like', 'likeable');
    }
}
```

获取关联

```php
// 从post中获取like
$post = App\Post::find(1);
foreach ($post->likes as $like) {
    //
}

// 从like中获取主体模型，通过调用`morphTo`，也就是likeable
$like = App\Like::find(1);
$likeable = $like->likeable;
```

###多对多的动态管理
上面的动态关联的关联类型和关联信息`like`是放在同一张表，如果把动态关联关系取出来放在另外一张表，可以用多对多的动态关联。
post和video都拥有tag，tag的信息单独维护，taggables表用来维护tag与和它相关的数据的关系

```
posts
    id - integer
    name - string

videos
    id - integer
    name - string

tags
    id - integer
    name - string

taggables
    tag_id - integer
    taggable_id - integer	// video或post的id
    taggable_type - string
```

定义post或video的模型，使用morphToMany与tag模型中的方法关联

```php
<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

class Post extends Model{
    /**
     * 获取指定文章所有标签
     */
    public function tags()
    {
        return $this->morphToMany('App\Tag', 'taggable');
    }
}
```

在tag模型中定义关联关系，使用`morphedByMany`返回给主体模型定义。

```php
<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

class Tag extends Model{
    /**
     * 获取所有分配该标签的文章
     */
    public function posts()
    {
        return $this->morphedByMany('App\Post', 'taggable');
    }

    /**
     * 获取分配该标签的所有视频
     */
    public function videos()
    {
        return $this->morphedByMany('App\Video', 'taggable');
    }
}
```

查询

```php
$post = App\Post::find(1);
foreach ($post->tags as $tag) {
    //
}

$tag = App\Tag::find(1);
foreach ($tag->videos as $video) {
    //
}
```

##关联查询
1、调用关联关系方法查询

```php
$user = App\User::find(1);
$user->posts()->where('active', 1)->get();
```
2、动态属性方式获取，动态属性的方式只有在真正需要访问到关联数据时才会加载关联数据，即`懒惰式加载`。当经常需要用到关联数据时，`懒惰式加载`会比`渴求式加载`增加一些SQL查询。

```php
$user = App\User::find(1);
foreach ($user->posts as $post) {
    //
}
```
###查询已存在的关联关系
即查询有关联数据的数据，可用到`has`方法或`whereHas`和`orWhereHas`将`where`条件放到`has`查询上。

```
// 获取所有至少有一条评论的文章...
$posts = App\Post::has('comments')->get();

// 获取所有至少有三条评论的文章...
$posts = Post::has('comments', '>=', 3)->get();

// 用.来嵌套，获取所有至少有一条评论获得投票的文章，文章关联评论，评论关联投票
$posts = Post::has('comments.votes')->get();

// 获取所有至少有一条评论包含foo字样的文章
$posts = Post::whereHas('comments', function ($query) {
    $query->where('content', 'like', 'foo%');
})->get();
```

###渴求式加载
采用动态属性访问关联数据时，即懒惰式加载会涉及到`N+1`查询问题。也就是一次性查出所有主体数据，然后要循环N次获取关联数据。

```
<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

class Book extends Model{
    /**
     * 获取写这本书的作者
     */
    public function author()
    {
        return $this->belongsTo('App\Author');
    }
}

// 一次性获取所有书，但要去查N次书的作者
$books = App\Book::all();
foreach ($books as $book) {
    echo $book->author->name;
}
```

采用`渴求式`，通过调用`with`方法

```php
$books = App\Book::with('author')->get();
foreach ($books as $book) {
    echo $book->author->name;
}
```
以上操作转换为sql：

```sql
select * from books
select * from authors where id in (1, 2, 3, 4, 5, ...)
```

其他渴求式加载用法

```php
// 获取多个关联
$books = App\Book::with('author', 'publisher')->get();

// 嵌套关联，book关联author，author关联contact
$books = App\Book::with('author.contacts')->get();

// 带条件约束的
// select * from user left join posts on posts.user_id = user.id where posts.title like '%first%';
$users = App\User::with(['posts' => function ($query) {
    $query->where('title', 'like', '%first%');
}])->get();

$users = App\User::with(['posts' => function ($query) {
    $query->orderBy('created_@', 'desc');
}])->get();
```

###懒惰渴求式加载
在获取了主体数据后，要一次性获取所有关联数据。使用`load`。

```php
$books = App\Book::all();
if ($someCondition) {
    $books->load('author', 'publisher');
}

// load的回调中添加查询构造器
$books->load(['author' => function ($query) {
    $query->orderBy('published_date', 'asc');
}]);
```

##插入关联模型
也就是添加新模型到关联关系中
###基本
`save`方法，直接插入到连表中而不用手动去设置关联的字段

```php
// 自动设置comment中的post_id
$comment = new App\Comment(['message' => 'A new comment.']);
$post = App\Post::find(1);
$post->comments()->save($comment);
```
>注意以上没有用动态属性方式访问comments，而是调用comments方法获取关联关系实例。

`saveMany`，保存多个

```php
$post = App\Post::find(1);
$post->comments()->saveMany([
    new App\Comment(['message' => 'A new comment.']),
    new App\Comment(['message' => 'Another comment.']),
]);
```

`save`与多对多，在第二个参数中传递中间关系表的数据

```php
App\User::find(1)->roles()->save($role, ['expires' => $expires]);
```

`create`方法，`save`方法接收的参数是Eloquent模型而`create`接收数组形式的数据。
使用`create`之前确保属性通过`批量赋值保护`。

```php
$post = App\Post::find(1);
$comment = $post->comments()->create([
    'message' => 'A new comment.',
]);
```

更新多对一（属于）关系时，即`belongsTo`，可用`associate`或`dissociate`方法，前者用于增加，后者用于解除

```php
$account = App\Account::find(10);
$user->account()->associate($account);
$user->save();

$user->account()->dissociate();
$user->save();
```

###多对多
假定一个用户可能有多个角色同时一个角色属于多个用户，要通过在连接模型的中间表中插入记录附加角色到用户上，可以使用`attach`方法：

```php
$user = App\User::find(1);
$user->roles()->attach($roleId);

// 第二个参数添加额外数据
$user->roles()->attach($roleId, ['expires' => $expires]);
```

从用户中移除角色，要移除一个多对多关联记录，使用`detach`方法

```php
// 从指定用户中移除角色...
$user->roles()->detach($roleId);
// 从指定用户移除所有角色...
$user->roles()->detach();
```

`attach`和`detach`还接收数组形式的 ID 作为输入：

```php
$user = App\User::find(1);
$user->roles()->detach([1, 2, 3]);
$user->roles()->attach([1 => ['expires' => $expires], 2, 3]);
```

####同步
使用`sync`方法构建多对多关联。
`sync`方法接收数组形式的ID并将其放置到中间表。任何不在该数组中的ID对应记录将会从中间表中移除。因此，该操作完成后，只有在数组中的ID对应记录还存在于中间表。

```php
$user->roles()->sync([1, 2, 3]);

//和ID一起传递额外的中间表值：
$user->roles()->sync([1 => ['expires' => true], 2, 3]);
```

##触发父级时间戳
当一个模型属于另外一个时，例如Comment属于Post，子模型更新时父模型的时间戳也被更新将很有用，例如，当Comment模型被更新时，你可能想要”触发“创建其所属模型Post的updated_at时间戳。Eloquent使得这项操作变得简单，只需要添加包含关联关系名称的touches属性到子模型中即可：

```php
<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

class Comment extends Model{
    /**
     * 要触发的所有关联关系
     *
     * @var array
     */
    protected $touches = ['post'];

    /**
     * 评论所属文章
     */
    public function post()
    {
        return $this->belongsTo('App\Post');
    }
}
```
现在，当你更新Comment时，所属模型Post将也会更新其updated_at值：

```php
$comment = App\Comment::find(1);
$comment->text = 'Edit to this comment!';
$comment->save();
```


