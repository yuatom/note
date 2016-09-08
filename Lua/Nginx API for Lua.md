# Nginx API for Lua
ngx 和 ndk 为Lua的两个标准模块，这两个模块在ngx_lua默认的全局作用域中。
这两个模块可以用在用户自己封装的Lua模块中：

```lua
 local say = ngx.say

 local _M = {}

 function _M.foo(a)
     say(a)
 end

 return _M
```

用户代码中的网络I/O操作应该使用Nginx API实现，否则Nginx的事件循环可能被阻塞，从而严重影响性能。相对小数据量的磁盘操作可以通过标准的Lua io库来实现，如果是大规模的文件读写可能会严重阻塞Nginx进程。

##服务器环境与变量
###ngx.arg
* 语法: val = ngx.arg[index]
* 环境: set_by_lua\*, body_filter_by_lua*

index为nginx.conf中使用 `set $var $value`的$var。
ngx.arg[index]的变量在 `set_by_lua*` 中是只读的。
在`body_filter_by_lua*`中，ngx.arg[1]为输出的数据，ngx.arg[2]为结束符。可以在`body_filter_by_lua*`的代码中修改这两个变量的值来达到过滤结果的目的。


###ngx.var.VARIABLE
* 语法: ngx.var.VAR_NAME
* 环境: set_by_lua\*, rewrite_by_lua\*, access_by_lua\*, content_by_lua\*, header_filter_by_lua\*, body_filter_by_lua\*, log_by_lua*

读写Nginx变量的值，只有已经定义的Nginx变量才能被写入（ngx_lua预定义的变量或者在nginx.conf中使用set定义的变量）。
部分变量不能被修改，例如`$query_string`，`$arg_PARAMETER`，和 `$http_NAME` 等。

Nginx正则表达式捕获组的 `$1`、`$2`、`$3`等，可以使用ngx.var[1]、ngx.var[2]及ngx.var[3]来获取。

使用这种方式读取变量时，是从基于请求的内存池中分配内存，只有当请求终止时才会释放内存。如果需要反复读取某个Nginx变量，应该用一个local变量来缓存该变量以免在当前请求周期内的临时内存泄漏。

```lua
local val = ngx.var.some_var
--- 在后面反复使用变量 val
```
也可以使用 `ngx.ctx` 来缓存需要反复读取的Nginx变量。

> 未定义的Nginx变量在被获取时其值为nil，如果已经定义了但还未初始化，其值是一个空的Lua字符串。

###core constants
* 环境: init_by_lua\*, set_by_lua\*, rewrite_by_lua\*, access_by_lua\*, content_by_lua\*, header_filter_by_lua\*, body_filter_by_lua, *log_by_lua\*, ngx.timer.\*, balancer_by_lua\*, ssl_certificate_by_lua\*

>* ngx.OK       = 0
>* ngx.ERROR    = -1
>* ngx.AGAIN    = -2
>* ngx.DONE     = -3
>* ngx.DECLINED = -4

以上这些常量中，只有三个可被ngx.exit()方法使用，即NGX_OK， NGX_ERROR，NGX_DECLINED。

>* ngx.null     = NULL，指代C中的null，一般用来表达Lua table中的nil值。

###HTTP method constants
环境: init_by_lua\*, set_by_lua\*, rewrite_by_lua\*, access_by_lua\*, content_by_lua\*, header_filter_by_lua\*, body_filter_by_lua, log_by_lua\*, ngx.timer.\*, balancer_by_lua\*, ssl_certificate_by_lua\*, ssl_session_fetch_by_lua\*, ssl_session_store_by_lua\*

指代HTTP协议中的方法，这些常量一般用在 `ngx.location.capture` 和 `ngx.location.capture_multi`。

>* ngx.HTTP_GET
>* ngx.HTTP_HEAD
>* ngx.HTTP_PUT
>* ngx.HTTP_POST
>* ngx.HTTP_DELETE
>* ngx.HTTP_OPTIONS   (v0.5.0rc24 版本加入)
>* ngx.HTTP_MKCOL     (v0.8.2 版本加入)
>* ngx.HTTP_COPY      (v0.8.2 版本加入)
>* ngx.HTTP_MOVE      (v0.8.2 版本加入)
>* ngx.HTTP_PROPFIND  (v0.8.2 版本加入)
>* ngx.HTTP_PROPPATCH (v0.8.2 版本加入)
>* ngx.HTTP_LOCK      (v0.8.2 版本加入)
>* ngx.HTTP_UNLOCK    (v0.8.2 版本加入)
>* ngx.HTTP_PATCH     (v0.8.2 版本加入)
>* ngx.HTTP_TRACE     (v0.8.2 版本加入)

###HTTP statu constants
* 环境: init_by_lua\*, set_by_lua\*, rewrite_by_lua\*, access_by_lua\*, content_by_lua\*, header_filter_by_lua\*, body_filter_by_lua, log_by_lua\*, ngx.timer.\*, balancer_by_lua\*, ssl_certificate_by_lua\*

>* value = ngx.HTTP_CONTINUE (100) (first added in the v0.9.20 release)
>* value = ngx.HTTP_SWITCHING_PROTOCOLS (101) (first added in the v0.9.20 release)
>* value = ngx.HTTP_OK (200)
>* value = ngx.HTTP_CREATED (201)
>* value = ngx.HTTP_ACCEPTED (202) (first added in the v0.9.20 release)
>* value = ngx.HTTP_NO_CONTENT (204) (first added in the v0.9.20 release)
>* value = ngx.HTTP_PARTIAL_CONTENT (206) (first added in the v0.9.20 release)
>* value = ngx.HTTP_SPECIAL_RESPONSE (300)
>* value = ngx.HTTP_MOVED_PERMANENTLY (301)
>* value = ngx.HTTP_MOVED_TEMPORARILY (302)
>* value = ngx.HTTP_SEE_OTHER (303)
>* value = ngx.HTTP_NOT_MODIFIED (304)
>* value = ngx.HTTP_TEMPORARY_REDIRECT (307) (first added in the v0.9.20 release)
>* value = ngx.HTTP_BAD_REQUEST (400)
>* value = ngx.HTTP_UNAUTHORIZED (401)
>* value = ngx.HTTP_PAYMENT_REQUIRED (402) (first added in the v0.9.20 release)
>* value = ngx.HTTP_FORBIDDEN (403)
>* value = ngx.HTTP_NOT_FOUND (404)
>* value = ngx.HTTP_NOT_ALLOWED (405)
>* value = ngx.HTTP_NOT_ACCEPTABLE (406) (first added in the v0.9.20 release)
>* value = ngx.HTTP_REQUEST_TIMEOUT (408) (first added in the v0.9.20 release)
>* value = ngx.HTTP_CONFLICT (409) (first added in the v0.9.20 release)
>* value = ngx.HTTP_GONE (410)
>* value = ngx.HTTP_UPGRADE_REQUIRED (426) (first added in the v0.9.20 release)
>* value = ngx.HTTP_TOO_MANY_REQUESTS (429) (first added in the v0.9.20 release)
>* value = ngx.HTTP_CLOSE (444) (first added in the v0.9.20 release)
>* value = ngx.HTTP_ILLEGAL (451) (first added in the v0.9.20 release)
>* value = ngx.HTTP_INTERNAL_SERVER_ERROR (500)
>* value = ngx.HTTP_METHOD_NOT_IMPLEMENTED (501)
>* value = ngx.HTTP_BAD_GATEWAY (502) (first added in the v0.9.20 release)
>* value = ngx.HTTP_SERVICE_UNAVAILABLE (503)
>* value = ngx.HTTP_GATEWAY_TIMEOUT (504) (first added in the v0.3.1rc38 release)
>* value = ngx.HTTP_VERSION_NOT_SUPPORTED (505) (first added in the v0.9.20 release)
>* value = ngx.HTTP_INSUFFICIENT_STORAGE (507) (first added in the v0.9.20 release)

###Ngixn log level constants
* 环境: set_by_lua\*, rewrite_by_lua\*, access_by_lua\*, content_by_lua\*, header_filter_by_lua\*, body_filter_by_lua, log_by_lua\*, ngx.timer.\*, balancer_by_lua\*, ssl_certificate_by_lua\*, ssl_session_fetch_by_lua\*, ssl_session_store_by_lua\*

这些常量常用于 `ngx.log`方法。

>* ngx.STDERR
>* ngx.EMERG
>* ngx.ALERT
>* ngx.CRIT
>* ngx.ERR
>* ngx.WARN
>* ngx.NOTICE
>* ngx.INFO
>* ngx.DEBUG

###print
* 语法: print(...)
* 环境: init_by_lua\*, init_worker_by_lua\*, set_by_lua*\, rewrite_by_lua\*, access_by_lua\*, content_by_lua\*, header_filter_by_lua\*, body_filter_by_lua, log_by_lua\*, ngx.timer.\*, balancer_by_lua\*, ssl_certificate_by_lua\*, ssl_session_fetch_by_lua\*, ssl_session_store_by_lua\*

将参数以`ngx.NOTICE`日志级别写入nginx的 `error.log`文件中。相当于

```lua
ngx.log(ngx.NOTICE, ...)
```
nil值的参数会被输出为“nil”字符串，布尔值会被输出为“true”或“false”，ngx.null常量输出为“null”字符串。

###ngx.ctx
* 环境: init_worker_by_lua\*, set_by_lua\*, rewrite_by_lua\*, access_by_lua\*, content_by_lua\*, header_filter_by_lua\*, body_filter_by_lua, log_by_lua\*, ngx.timer.\*, balancer_by_lua\*

该变量的类型为Lua table，可以用来存储基于请求的Lua环境数据，生存周期和当前请求相同，跨越一个请求的rewrite，access 和 content处理阶段。

每一个子请求也有自己的ngx.ctx，一个请求和其子请求中的ngx.ctx，类似一个函数内外的同名变量，互不影响。

ngx.ctx中表元素的查找是基于__index元方法，在一个module中使用ngx.ctx中，应该在一个module的方法中直接调用ngx.ctx.xxx。

```lua
 -- mymodule.lua
 local _M = {}

 -- 下面一行的 ngx.ctx 是属于单个请求的，但 `ctx` 变量是在 Lua 模块级别
 -- 并且属于单个 worker 的。
 local ctx = ngx.ctx

 function _M.main()
     ctx.foo = "bar"
 end

 return _M
```
以上代码，如果同一个worker中处理两个请求，第一个请求取到了ngx.ctx，local ctx指向ngx.ctx，并对ngx.ctx.foo赋值。当第二请求到达时，并没有执行`local ctx = ngx.ctx`，main方法中的ctx是module变量，指向和第一个请求中的ctx是同一个，导致两个请求“串数据”。
改成以下形式，ngx.ctx由函数外部传入，或者直接引用ngx.ctx

```lua
 -- mymodule.lua
 local _M = {}

 function _M.main(ctx)
     ctx.foo = "bar"
 end
 
 -- 或
 -- function _M.main()
 --   ngx.ctx.foo = "bar"
 -- end

 return _M
```

###ngx.location.capture
* 语法: res = ngx.location.capture(uri, options?)
* 环境: rewrite_by_lua\*, access_by_lua\*, content_by_lua\*

在Lua代码中发起一个同步非阻塞的Nginx子请求，子请求会继承富请求的所有请求头信息。
子请求的目标location可以是配置文件中其他文件目录，也可以是其他Nginx C模块，包括`ngx_proxy`、`ngx_fastcgi`、`ngx_memc`、`ngx_postgres`、`ngx_drizzle`，甚至 `ngx_lua` 自身等等 。
所发起的子请求只是模拟HTTP接口的形式，并没有产生额外的HTTP/TCP流量，也进程间通信调用。所有工作都是在C语言级别完成。

在发起子请求前，程序会先通过调用 `ngx.req.read_body` 或设置 `lua_need_request_body` 指令为 `on` 来读取完成的HTTP请求体。

该方法会返回一个包含四个元素的Lua表，res.status，res.header，res.body和res.truncated。
>* res.status是响应状态码；
>* res.header是响应头，类型是Lua table，如果某个响应头项有多个值，则该响应头项的类型也会是一个table，并且按照值的顺序；
>* res.body是响应体，有可能被阶段，通过res.truncated来判断。

####option参数
该参数是一个table，有以下选项：

* method，所使用的请求方法，接受HTTP mothod constants；
* body，请求体，仅限字符串值；
* args，请求的参数，可以是字符串或table；
* ctx，指定一个table作为子请求的ngx.ctx；
* vars，指定一个table作为子请求的Nginx变量，即ngx.var；
* copy_all_vars，设置是否将当前请求的所有Nginx变量拷贝到子请求中；
* share_all_vars，是否共享当前请求的所有Nginx变量给子请求，子请求中对Nginx变量的修改，会影响当前请求的，当share_all_vars和copy_all_vars同时设置为true时，share_all_vars优先；
* always_forward_body，如果为true，且没有设置body，则会把父请求的请求头全部转发给子请求。

```lua
res = ngx.location.capture(
     '/foo/bar',
     { method = ngx.HTTP_POST, body = 'hello, world' }
 )
```

###ngx.location.capture_multi
* 语法: res1, res2, ... = ngx.location.capture_multi({ {uri, options?}, {uri, options?}, ... })
* 环境: rewrite_by_lua\*, access_by_lua\*, content_by_lua\*

与 `ngx.location.capture` 类似，并行发起多个子请求，按元顺序返回多个结果。

```lua
res1, res2, res3 = ngx.location.capture_multi{
     { "/foo", { args = "a=3&b=4" } },
     { "/bar" },
     { "/baz", { method = ngx.HTTP_POST, body = "hello" } },
 }

 if res1.status == ngx.HTTP_OK then
     ...
 end

 if res2.body == "BLAH" then
     ...
 end
```
要等到多有子请求都终止后才返回。

###ngx.status
* 环境: set_by_lua\*, rewrite_by_lua\*, access_by_lua\*, content_by_lua\*, header_filter_by_lua\*, body_filter_by_lua, log_by_lua\*

读写当前响应的状态码，需要在发送响应头之前调用，在响应头发送后修改该变量不会生效。

###ngx.header.HEADER
* 语法: ngx.header.HEADER = VALUE
* 语法: value = ngx.header.HEADER
* 环境: rewrite_by_lua\*, access_by_lua\*, content_by_lua\*, header_filter_by_lua\*, body_filter_by_lua, log_by_lua\*

修改、添加、或清除当前请求待发送的 HEADER 响应头信息。
头名称大小写不敏反感，且其中的下划线会被默认替换为连字符，可以通过 `lua_transform_underscores_in_response_headers` 指令关闭这个替换。

将ngx.header.HEADER设置为nil，表示将该项从响应头中移除。

> `ngx.header` 不是一个标准 Lua 表，不能通过 Lua 的 `ipairs` 函数进行迭代查询。
> 读取 请求 头信息，请使用 `ngx.req.get_headers` 函数。


###ngx.resp.get_headers
* 语法: headers = ngx.resp.get_headers(max_headers?, raw?)
* 环境: set_by_lua\*, rewrite_by_lua\*, access_by_lua\*, content_by_lua\*, header_filter_by_lua\*, body_filter_by_lua, log_by_lua\*, balancer_by_lua\*

返回一个 Lua 表，包含当前请求的所有响应头信息。

```lua
 local h = ngx.resp.get_headers()
 for k, v in pairs(h) do
     ...
 end
```

###ngx.is_subrequest
* 语法: value = ngx.is_subrequest
* 环境: set_by_lua\*, rewrite_by_lua\*, access_by_lua\*, content_by_lua\*, header_filter_by_lua\*, body_filter_by_lua\*, log_by_lua\*

如果当前请求是 nginx 子请求返回 true ，否则返回 false 。

##request
###ngx.req.is_internal
* 语法: is_internal = ngx.req.is_internal()
* 环境: set_by_lua\*, rewrite_by_lua\*, access_by_lua\*, content_by_lua\*, header_filter_by_lua\*, body_filter_by_lua\*, log_by_lua\*

返回一个布尔值，说明当前请求是否是一个“内部请求”，既：一个请求的初始化是在当前 nginx 服务端完成初始化，不是在客户端。

子请求都是内部请求，并且都是内部重定向后的请求。


###ngx.req.start_time
* 语法: secs = ngx.req.start_time()
* 环境: set_by_lua\*, rewrite_by_lua\*, access_by_lua\*, content_by_lua\*, header_filter_by_lua\*, body_filter_by_lua\*, log_by_lua\*

返回当前请求创建时的时间戳，格式为浮点数，其中小数部分代表毫秒值。

以下用 Lua 代码模拟计算了 $request_time 变量值 (由 ngx_http_log_module 模块生成)

```lua
 local request_time = ngx.now() - ngx.req.start_time()
```

###ngx.req.http_version
* 语法: num = ngx.req.http_version()
* 环境: set_by_lua\*, rewrite_by_lua\*, access_by_lua\*, content_by_lua\*, header_filter_by_lua\*

返回一个 Lua 数字代表当前请求的 HTTP 版本号。

当前的可能结果值为 2.0, 1.0, 1.1 和 0.9。无法识别时值时返回 nil。

###ngx.req.raw_header
* 语法: str = ngx.req.raw_header(no_request_line?)
* 环境: set_by_lua\*, rewrite_by_lua\*, access_by_lua\*, content_by_lua\*, header_filter_by_lua\*

返回 Nginx 服务器接收到的原始 HTTP 协议头。
no_request_line，是否去除请求行。

```lua
ngx.print(ngx.req.raw_header())
-- 输出结果类似：
--[[
GET /t HTTP/1.1
Host: localhost
Connection: close
Foo: bar
--]]

ngx.print(ngx.req.raw_header(true))
-- 输出结果类似：
--[[
Host: localhost
Connection: close
Foo: bar
--]]
```

###ngx.req.get_method
* 语法: method_name = ngx.req.get_method()
* 环境: set_by_lua\*, rewrite_by_lua\*, access_by_lua\*, content_by_lua\*, header_filter_by_lua\*, balancer_by_lua\*

获取当前请求的 HTTP 请求方法名称。结果为类似 "GET" 和 "POST" 的字符串，而不是 `HTTP method constants` 中定义的数值。

###ngx.req.set_method
* 语法: ngx.req.set_method(method_id)
* 环境: set_by_lua\*, rewrite_by_lua\*, access_by_lua\*, content_by_lua\*, header_filter_by_lua\*

用 method_id 参数的值改写当前请求的 HTTP 请求方法。当前仅支持 HTTP method constants，例如 `ngx.HTTP_POST` 和 `ngx.HTTP_GET`。

###ngx.req.set_uri
* 语法: ngx.req.set_uri(uri, jump?)
* 环境: set_by_lua\*, rewrite_by_lua\*, access_by_lua\*, content_by_lua\*, header_filter_by_lua\*, body_filter_by_lua\*

修改当前请求的uri，在rewrite阶段，将 `jump` 设置为true可以实现重新匹配location，类似与使用rewrite中的last，为false时类似break。

```nginx
rewrite ^ /foo last;
```
相当于

```lua
ngx.req.set_uri("/foo", true)
```

```nginx
rewrite ^ /foo break;
```
相当于

```lua
ngx.req.set_uri("/foo", false)
```

> 不能使用该方法重写URI参数，应该使用 `ngx.req.set_uri_args` 。

```nginx
 rewrite ^ /foo?a=3? last;
```
相当于

```lua
ngx.req.set_uri_args("a=3")
ngx.req.set_uri("/foo", true)
```
或

```lua
 ngx.req.set_uri_args({a = 3})
 ngx.req.set_uri("/foo", true)
```

###ngx.req.set_uri_args
* 语法: ngx.req.set_uri_args(args)
* 环境: set_by_lua\*, rewrite_by_lua\*, access_by_lua\*, content_by_lua\*, header_filter_by_lua\*, body_filter_by_lua\*

重写当前请求的uri参数。
args可以是字符串，可以是一个Lua table，也可以传多个值。

```lua
-- 字符串，a=3&b=hello%20world
ngx.req.set_uri_args("a=3&b=hello%20world")

-- table，a=3&b=hello%20world
ngx.req.set_uri_args({ a = 3, b = "hello world" })

-- 多值，a=3&b=5&b=6
ngx.req.set_uri_args({ a = 3, b = {5, 6} })
```

###ngx.req.get_uri_args
* 语法: args = ngx.req.get_uri_args(max_args?)
* 环境: set_by_lua\*, rewrite_by_lua\*, access_by_lua\*, content_by_lua\*, header_filter_by_lua\*, body_filter_by_lua, log_by_lua\*

获取uri请求参数，返回一个Lua table。

* 当多个值是同一个key时，该key在元素也是一个table；
* 没有key的值会被忽略；
* 没有value的key会被转换成布尔值的true

```nginx
location = /test {
     content_by_lua '
         local args = ngx.req.get_uri_args()
         for key, val in pairs(args) do
             if type(val) == "table" then
                 ngx.say(key, ": ", table.concat(val, ", "))
             else
                 ngx.say(key, ": ", val)
             end
         end
     ';
 }
```

> 该方法默认只解析前100个请求参数（包括同名的），多余100的参数会被忽略，可以通过设置 `max_args`来修改该限制，当该参数为0时，表示不限制（不推荐）。

###ngx.req.get_post_args
* 语法: args, err = ngx.req.get_post_args(max_args?)
* 环境: rewrite_by_lua\*, access_by_lua\*, content_by_lua\*, header_filter_by_lua\*, body_filter_by_lua, log_by_lua\*

获取POST数据（MIME type 是 application/x-www-form-urlencoded），返回的是一个table。

* 没有key的值会被忽略；
* 没有value的key会被转换成布尔值的true

> 使用前需要调用 `ngx.req.read_body` 读取请求体，或者设置 `lua_need_request_body` 的值为on。

```nginx
location = /test {
    content_by_lua '
        ngx.req.read_body()
        local args, err = ngx.req.get_post_args()
        if not args then
            ngx.say("failed to get post args: ", err)
        end
        for key, val in pairs(args) do
            if type(val) == "table" then
                ngx.say(key, ": ", table.concat(val, ", "))
            else
                ngx.say(key, ": ", val)
            end
        end
    ';
}
```

> 同样有参数数量的限制。

###ngx.req.get_headers
* 语法: headers = ngx.req.get_headers(max_headers?, raw?)
* 环境: set_by_lua\*, rewrite_by_lua\*, access_by_lua\*, content_by_lua\*, header_filter_by_lua\*, body_filter_by_lua, log_by_lua\*

获取所有请求头，返回一个Lua table。

```lua
local h = ngx.req.get_headers()
for k, v in pairs(h) do
    ...
end
```

如果请求头中多次出现某个字段，则获取到的会是一个table：

```
#  Foo: foo
#  Foo: bar
#  Foo: baz

# ngx.req.get_headers()["Foo"]的值
# {"foo", "bar", "baz"}
```

该方法获取的table取key的时候，如果取不到，会将key转换成全小写字母，且将下划线变成连字符，再重新搜索。因为默认情况下Lua table的被添加了 `__index`元方法。

```lua 
-- 以下获取的结果都相同。
ngx.say(headers.my_foo_header)
ngx.say(headers["My-Foo-Header"])
ngx.say(headers["my-foo-header"])
```

> 同样有数量的限制。

###ngx.req.set_header
* 语法: ngx.req.set_header(header_name, header_value)
* 环境: set_by_lua\*, rewrite_by_lua\*, access_by_lua\*, content_by_lua\*, header_filter_by_lua\*, body_filter_by_lua\*

添加/修改请求头，其值可以是一个字符串，也可以是一个数组。
> 默认时，之后通过 `ngx.location.capture` 和 `ngx.location.capture_multi` 发起的所有子请求都将继承新的头信息。

###ngx.req.clear_header
* 语法: ngx.req.clear_header(header_name)
* 环境: set_by_lua\*, rewrite_by_lua\*, access_by_lua\*, content_by_lua\*, header_filter_by_lua\*, body_filter_by_lua\*

清除当前请求的名为 header_name 的请求头信息。已经存在的子请求不受影响，此命令之后发起的子请求将默认继承修改后的头信息。

###ngx.req.read_body
* 语法: ngx.req.read_body()
* 环境: rewrite_by_lua\*, access_by_lua\*, content_by_lua\*

同步读取客户端请求体，不阻塞 Nginx 事件循环。

* 如果已经通过打开 lua_need_request_body 选项或其他模块读取请求体，此函数将不会执行，立即返回；
* 如果已经通过 ngx.req.discard_body 函数或其他模块明确丢弃请求体，此函数将不会执行，立即返回。

该方法读取了请求体之后，可以通过 `ngx.req.get_body_data` 获取请求体数据，或者通过 `ngx.req.get_body_file` 将请求体缓存到文件并返回临时文件名（当前请求体大于 `client_body_buffer_size` 或打开 `clinet_body_in_file_only` 选项的情况下会字段保存到临时文件中）。

###ngx.req.discard_body
* 语法: ngx.req.discard_body()
* 环境: rewrite_by_lua\*, access_by_lua\*, content_by_lua\*

明确丢弃请求体，也就是说，读取连接中的数据后立即丢弃（不以任何形式使用请求体）。
这个函数是异步调用，将立即返回。
如果请求体已经被读取，此函数将不会执行，立即返回。


###ngx.req.get_body_data
* 语法: data = ngx.req.get_body_data()
* 环境: rewrite_by_lua\*, access_by_lua\*, content_by_lua\*, log_by_lua\*

获取保存在内存中的请求体数据，返回Lua字符串而不是解析过参数的table。如果要获取table形式的，要使用 `ngx.req.get_post_args` 。

以下情况返回nil：

* 请求体未被读取，需要调用 `ngx.req.read_body`或打开 `lua_need_request_body`；
* 请求体被保存到临时文件上，使用 `ngx.req.get_body_file`方法替代；
* 请求体大小是0

如果要强制将数据保存到内存中，需要保持 `client_body_buffer_size`和`client_max_body_size`一致。

> 调用此函数比使用 `ngx.var.request_body` 或 `ngx.var.echo_request_body` 更有效率，因为本函数能够节省一次内存分配与数据复制。

###ngx.req.get_body_file
* 语法: file_name = ngx.req.get_body_file()
* 环境: rewrite_by_lua\*, access_by_lua\*, content_by_lua\*

获取保存请求体数据的临时文件名，如果请求体已经被保存到内存中，该函数返回nil。
保存数据的文件是只读的，会被Nginx的内存池清理机制清理。不应该手工修改、更名或删除。

###ngx.req.set_body_data
* 语法: ngx.req.set_body_data(data)
* 环境: rewrite_by_lua*, access_by_lua*, content_by_lua*

使用 `data` 参数指定的内存数据设置当前请求的请求体。
如果当前请求的请求体尚未被读取，它将被安全地丢弃。当请求体已经被读进内存或缓存在磁盘文件中时，相应的内存或磁盘文件将被立即清理回收。

###ngx.req.set_body_file
* 语法: ngx.req.set_body_file(file_name, auto_clean?)
* 环境: rewrite_by_lua\*, access_by_lua\*, content_by_lua\*

使用 file_name 参数指定的数据文件设置当前请求的请求体。

auto_clean为 `true` 的情况下，在本次请求完成或者在本次请求内再次调用本函数或`ngx.req.set_body_data`的时候，会将`file_name`删除。该值默认是 `false`。

如果当前请求的请求体尚未被读取，它将被安全地丢弃。当请求体已经被读进内存或缓存在磁盘文件中时，相应的内存或磁盘文件将被立即清理回收。

###ngx.req.init_body
* 语法: ngx.req.init_body(buffer_size?)
* 环境: set_by_lua\*, rewrite_by_lua\*, access_by_lua\*, content_by_lua\*

为当前请求创建一个新的空请求体初始化缓冲区，为后续调用 `ngx.req.append_body`追加请求体做好准备。
如果设置了 `buffer_size`参数，会将该值作为缓冲区大小。如果该参数没有给出，则使用 `client_body_buffer_size`配置的大小作为缓冲区大小。
当请求体数据过大时，数据会被写入到一个临时文件。

> 在所有请求体添加时候，必须调用 `ngx.req.finish_body`方法来结束。

```lua 
-- 典型用法
 ngx.req.init_body(128 * 1024)  -- 缓冲区 128KB
 for chunk in next_data_chunk() do
     ngx.req.append_body(chunk) -- 每块可以是 4KB
 end
 ngx.req.finish_body()
```

###ngx.req.append_body
* 语法: ngx.req.append_body(data_chunk)
* 环境: set_by_lua\*, rewrite_by_lua\*, access_by_lua\*, content_by_lua\*

向已存在的请求体中追加写入 `data_chunk` 参数指定的新数据块。
该方法使用前要先调用 `ngx.req.init_body` 初始化请求体缓冲区。

> 当请求体数据过大时，数据会被写入到一个临时文件。
> 在所有请求体添加时候，必须调用 `ngx.req.finish_body`方法来结束。

###ngx.req.finish_body
* 语法: ngx.req.finish_body()
* 环境: set_by_lua\*, rewrite_by_lua\*, access_by_lua\*, content_by_lua\*

结束新请求体构造过程，该请求体由 ngx.req.init_body 和 ngx.req.append_body 创建。

###ngx.req.socket
* 语法: tcpsock, err = ngx.req.socket()
* 语法: tcpsock, err = ngx.req.socket(raw)
* 环境: rewrite_by_lua, access_by_lua, content_by_lua*

返回一个包含下游连接的只读 cosocket 对象。
通过该方法返回的 socket 对象，通常是用流式格式读取当前请求体。不要开启 `lua_need_request_body` 指令，并且不要混合调用 `ngx.req.read_body` 和 `ngx.req.discard_body`。


>  `ngx.req.init_body`，`ngx.req.append_body`，`ngx.req.finish_body` 和 `ngx.req.socket` 一起，使用纯 Lua 语言实现高效的输入过滤器 (在 `rewrite_by_lua*` 或 `access_by_lua*` 环境中)，与其他 Nginx 内容处理程序或上游模块例如 `ngx_http_proxy_module` 和 `ngx_http_fastcgi_module` 配合使用。

##控制
###ngx.exec
* 语法: ngx.exec(uri, args?)
* 环境: rewrite_by_lua, access_by_lua, content_by_lua*

使用uri, args参数执行一个内部跳转。

```lua
ngx.exec('/some-location')
ngx.exec('/some-location', 'a=3&b=5&c=6')

-- uri后面跟参数
ngx.exec('/some-location?a=3&b=5', 'c=6') 

-- 参数是lua table, table会被格式化，结果跟使用ngx.encode_args一样
ngx.exec('/some-location', {a = 3, b = 5, c = 6})
```

uri参数也可以是一个命名的location，如此一来会忽略第二个参数。

```nginx
location /foo {
    content_by_lua '
        ngx.exec("@bar", "a=goodbye");
    ';
}

location @bar {
    content_by_lua '
        locat args = ngx.req.get_uri_args();
        for key, val in pairs(args) do 
            if key == "a" then
                ngx.say(val)
            end
        end
    ';
}
```
> ngx.exec与ngx.redirect不同，前者只是个内部跳转，并没有引入任何额外的HTTP信号。
> ngx.exec会终止当前请求的处理，必须在 `ngx.send_headers` 或明确有响应体应答之前调用。


###ngx.redirect
* 语法: ngx.redirect(uri, status?)
* 环境: rewrite_by_lua, access_by_lua, content_by_lua*

发出一个HTTP 301 或 302 重定向到uri，status参数指定是301还是302，默认是302(ngx.HTTP_MOVED_TEMPORARILY)。

```lua
-- 内部跳转
return ngx.redirect("/foo")
return ngx.redirect("/foo", ngx.HTTP_MOVED_TEMPORARILY)
return ngx.redirect("/foo", 301)

-- 外部跳转
return ngx.redirect("http://www.google.com")
```
> ngx.redirect会终止当前请求的处理，必须在 `ngx.send_headers` 或明确有响应体应答之前调用。

###ngx.send_headers
* 语法: ok, err = ngx.send_headers()
* 环境: rewrite_by_lua, access_by_lua, content_by_lua*

发送响应头，成功返回1，失败返回nil。
当内容通过 `ngx.say`, `ngx.print` 输出或当 `content_by_lua` 存在时，ngx_lua将自动发送头部内容。

###ngx.headers_sent
* 语法: value = ngx.header_sent
* 环境: set_by_lua\*, rewrite_by_lua\*, access_by_lua\*, content_by_lua\*

如果响应头部已经通过ngx_lua发送成功则返回true，否则返回false。

###ngx.print
* 语法: ok, err = ngx.pring(...)
* 环境: rewrite_by_lua\*, access_by_lua\*, content_by_lua*

将参数合并作为HTTP响应体发送给HTTP客户端，发送成功返回1，失败返回nil。
在发送响应体之前如果还没有发送响应头，则会先发送发送HTTP响应头，在输出响应体。

>* Lua的nil值输出"nil"字符串，布尔值输出“true”或“false"字符串；
>* 如果参数是数组，数组中的所有元素会按顺序输出；
>* key-value的table会抛出Lua异常；
>* ngx.null常量输出为”null“字符串；

本函数为异步调用，会立刻返回到客户端，不会等待所有数据被写入系统发送缓冲区。
在调用 `ngx.print` 之后调用 `ngx.flush(true)`，能够以同步模式运行该函数。

###ngx.say
* 语法: ok, err = ngx.pring(...)
* 环境: rewrite_by_lua\*, access_by_lua\*, content_by_lua*

与 `ngx.print`相同，但是会在每个 `ngx.say` 后面加一个回车符。

###ngx.log
* 语法: ngx.log(log_level, ...)
* 环境: init_by_lua\*, init_worker_by_lua\*, set_by_lua\*, rewrite_by_lua\*, access_by_lua\*, content_by_lua\*, header_filter_by_lua\*, body_filter_by_lua\*, log_by_lua\*, ngx.timer.\*, balancer_by_lua\*, ssl_certificate_by_lua\*, ssl_session_fetch_by_lua\*, ssl_session_store_by_lua\*

将参数拼接起来，以指定的日志级别写入 error.log。
log_level 参数可以使用类似 `ngx.ERR` 和 `ngx.WARN` 的常量。

###ngx.flush
* 语法: ok, err = ngx.flush(wait?)
* 环境: rewrite_by_lua\*, access_by_lua\*, content_by_lua\*

向客户端刷新响应输出。
wait是一个布尔类型的参数，默认是false，表示以异步的形式直接返回，不等待输出数据被写入系统发送缓冲区。当wait是true的时，将以同步的模式执行，不会立即返回，会等待所有的输出数据写入系统输出缓冲区，或者超过了 `send_timeount` 设置的时间。

> 由于使用了Lua的协程机制，该函数即使在同步模式下也不会阻塞Nginx事件循环。

###ngx.exit
* 语法: ngx.exit(status)
* 环境: rewrite_by_lua\*, access_by_lua\*, content_by_lua\*, header_filter_by_lua\*, ngx.timer\*, balancer_by_lua\*, ssl_certificate_by_lua\*, ssl_session_fetch_by_lua\*, ssl_session_store_by_lua\*

`status` 参数可以是 `ngx.OK`, `ngx.ERROR`, `ngx.HTTP_NOT_FOUND`, `ngx.HTTP_MOVED_TEMPORARILY` 或其它 `HTTP status constants`。
当 `status >= 200` (即 `ngx.HTTP_OK` 及以上)时，本函数终端当前请求执行并反返回状态值给Nginx。
当 `status == 0` （即 `ngx.Ok` ）时，本函数退出当前的“处理阶段句柄”，继续执行当前请求的下一个阶段（如果有）。

```lua
-- 定义一个自定义内容的错误页
ngx.status = ngx.HTTP_GONE
ngx.say("This is our own content")
ngx.exit(ngx.HTTP_OK)   -- 退出整个请求
```

```shell
# $ curl -i http://localhost/test
# HTTP/1.1 410 Gone
# Server: nginx/1.0.6
# Date: Thu, 15 Sep 2011 00:51:48 GMT
# Content-Type: text/plain
# Transfer-Encoding: chunked
# Connection: keep-alive

# This is our own content
```
> 由于调用该方法会中断当前请求处理，所以建议和 `return` 一起调用此方法，即 `return ngx.exit(...)`。


###ngx.eof
* 语法: ok, err = ngx.eof()
* 环境: rewrite_by_lua\*, access_by_lua\*, content_by_lua\*

指定响应输出流的末尾，让HTTP客户端主动关闭连接。
在执行该语句之后，客户端关闭了连接，服务端仍然可以做其他后台任务。

但是，如果用户程序创建子请求通过 Nginx 上游模块访问其他 location 时，需要配置上游模块忽略客户端连接中断 (如果不是默认)。例如，默认时，基本模块 `ngx_http_proxy_module` 在客户端关闭连接后，立刻中断主请求和子请求，所以在 `ngx_http_proxy_module` 配置的 location 块中打开 `proxy_ignore_client_abort` 开关非常重要：

```ngixn
 proxy_ignore_client_abort on;
```

###ngx.sleep
* 语法: ngx.sleep(seconds)
* 环境: rewrite_by_lua\*, access_by_lua\*, content_by_lua\*, ngx.timer.\*, ssl_certificate_by_lua\*, ssl_session_fetch_by_lua\*

无阻塞地休眠特定秒。时间可以精确到 0.001 秒 (毫秒)。
在后台，此方法使用 Nginx 的定时器。

##编码
###ngx.escape_uri
* 语法: newstr = ngx.escape_uri(str)
* 环境: init_by_lua\*, init_worker_by_lua\*, set_by_lua\*, rewrite_by_lua\*, access_by_lua\*, content_by_lua\*, header_filter_by_lua\*, body_filter_by_lua\*, log_by_lua\*, ngx.timer.\*, balancer_by_lua\*, sll_certificate_by_lua\*, ssl_session_fetch_by_lua\*, ssl_session_store_by_lua\*

对str进行URI编码。

###ngx.unescape_uri
对str进行URI解码

###ngx.encode_args
* 语法: str = ngx.encode_args(table)
* 环境: set_by_lua\*, rewrite_by_lua\*, access_by_lua\*, content_by_lua\*, header_filter_by_lua\*, body_filter_by_lua\*, log_by_lua\*, ngx.timer.\*, balancer_by_lua\*, ssl_certificate_by_lia\*

将Lua table编码成一个查询参数的字符串。

###ngx.decode_args
将URI编码的字符串转换成Lua table。

>* table表的key必须是Lua字符串；
>* 支持一个key多个值；
>* value为空的话将等同与nil；
>* value为false时等同于nil；

###ngx.encode_base64
* 语法: newstr = ngx.encode_base64(str, no_padding?)
* 环境: set_by_lua\*, rewrite_by_lua\*, access_by_lua\*, content_by_lua\*, header_filter_by_lua\*, body_filter_by_lua\*, log_by_lua\*, ngx.timer.\*, balancer_by_lua\*, ssl_certificate_by_lua\*, ssl_session_fetch_by_lua\*, ssl_session_store_by_lua\*

通过 base64 对 str 字符串编码。

###ngx.decode_base64
* 语法: newstr = ngx.decode_base64(str)
* 环境: set_by_lua\*, rewrite_by_lua\*, access_by_lua\*, content_by_lua\*, header_filter_by_lua\*, body_filter_by_lua\*, log_by_lua\*, ngx.timer.\*, balancer_by_lua\*, ssl_certificate_by_lua\*, ssl_session_fetch_by_lua\*, ssl_session_store_by_lua\*

通过 base64 解码 str 字符串得到未编码过的字符串。如果 str 字符串没有被正常解码将会返回 nil。


###ngx.crc32_short
* 语法: intval = ngx.crc32_short(str)
* 环境: set_by_lua\*, rewrite_by_lua\*, access_by_lua\*, content_by_lua\*, header_filter_by_lua\*, body_filter_by_lua\*, log_by_lua\*, ngx.timer.\*, balancer_by_lua\*, ssl_certificate_by_lua\*, ssl_session_fetch_by_lua\*, ssl_session_store_by_lua\*

通过一个字符串计算循环冗余校验码。
这个方法最好在字符串较少时调用（比如少于30-60字节），他的结果和 ngx.crc32_long 是一样的。

###ngx.crc32_long
* 语法: intval = ngx.crc32_long(str)
* 环境: set_by_lua\*, rewrite_by_lua\*, access_by_lua\*, content_by_lua\*, header_filter_by_lua\*, body_filter_by_lua\*, log_by_lua\*, ngx.timer.\*, balancer_by_lua\*, ssl_certificate_by_lua\*, ssl_session_fetch_by_lua\*, ssl_session_store_by_lua\*

通过一个字符串计算循环冗余校验码。
这个方法最好在字符串较多时调用（比如大于30-60字节），他的结果和 ngx.crc32_short 是一样的。


###ngx.hmac_sha1
###ngx.md5
* 语法: digest = ngx.md5(str)
* 环境: set_by_lua\*, rewrite_by_lua\*, access_by_lua\*, content_by_lua\*, header_filter_by_lua\*, body_filter_by_lua\*, log_by_lua\*, ngx.timer.\*, balancer_by_lua\*, ssl_certificate_by_lua\*, ssl_session_fetch_by_lua\*, ssl_session_store_by_lua\*

通过 MD5 计算 str 字符串返回十六进制的数据。
###ngx.md5_bin
* 语法: digest = ngx.md5_bin(str)
* 环境: set_by_lua\*, rewrite_by_lua\*, access_by_lua\*, content_by_lua\*, header_filter_by_lua\*, body_filter_by_lua\*, log_by_lua\*, ngx.timer.\*, balancer_by_lua\*, ssl_certificate_by_lua\*, ssl_session_fetch_by_lua\*, ssl_session_store_by_lua\*

通过 MD5 计算 str 字符串返回二进制的数据。

###ngx.sha1_bin
* 语法: digest = ngx.sha1_bin(str)
* 环境: set_by_lua\*, rewrite_by_lua\*, access_by_lua\*, content_by_lua\*, header_filter_by_lua\*, body_filter_by_lua\*, log_by_lua\*, ngx.timer.\*, balancer_by_lua\*, ssl_certificate_by_lua\*, ssl_session_fetch_by_lua\*, ssl_session_store_by_lua\*

通过 SHA-1 计算 str 字符串返回二进制的数据。
在安装 Nginx 时 这个函数需要 SHA-1 的支持。（这通常说明应该在安装 Nginx 时一起安装 OpenSSL 库）。

###ngx.quote_sql_str
* 语法: quoted_value = ngx.quote_sql_str(raw_value)
* 环境: set_by_lua\*, rewrite_by_lua\*, access_by_lua\*, content_by_lua\*, header_filter_by_lua\*, body_filter_by_lua\*, log_by_lua\*, ngx.timer.\*, balancer_by_lua\*, ssl_certificate_by_lua\*, ssl_session_fetch_by_lua\*, ssl_session_store_by_lua\*

根据 MySQL 转义规则返回一个转义后字符串。



##时间
###ngx.today
* 语法: str = ngx.today()
* 环境: init_worker_by_lua\*, set_by_lua\*, rewrite_by_lua\*, access_by_lua\*, content_by_lua\*, header_filter_by_lua\*, body_filter_by_lua\*, log_by_lua\*, ngx.timer.\*, balancer_by_lua\*, ssl_certificate_by_lua\*, ssl_session_fetch_by_lua\*, ssl_session_store_by_lua\*

获取nginx时间缓存的当前日期，格式：yyyy-mm-dd。
不涉及系统调用。

###ngx.time
* 语法: secs = ngx.time()
* 环境: init_worker_by_lua\*, set_by_lua\*, rewrite_by_lua\*, access_by_lua\*, content_by_lua\*, header_filter_by_lua\*, body_filter_by_lua\*, log_by_lua\*, ngx.timer.\*， balancer_by_lua\*, ssl_certificate_by_lua\*, ssl_session_fetch_by_lua\*, ssl_session_store_by_lua\*

返回从新纪元到nginx缓存的时间的时间戳。
不涉及系统调用。

###ngx.now
* 语法: secs = ngx.now()
* 环境: init_worker_by_lua\*, set_by_lua\*, rewrite_by_lua\*, access_by_lua\*, content_by_lua\*, header_filter_by_lua\*, body_filter_by_lua\*, log_by_lua\*, ngx.timer.\*， balancer_by_lua\*, ssl_certificate_by_lua\*, ssl_session_fetch_by_lua\*, ssl_session_store_by_lua\*

返回一个浮点型的数字，从新纪元到nginx缓存的时间的时间戳，单位秒，小数部分为毫秒。
不涉及系统调用。

###ngx.update_time
* 语法: ngx.update_time()
* 环境: init_worker_by_lua\*, set_by_lua\*, rewrite_by_lua\*, access_by_lua\*, content_by_lua\*, header_filter_by_lua\*, body_filter_by_lua\*, log_by_lua\*, ngx.timer.\*， balancer_by_lua\*, ssl_certificate_by_lua\*, ssl_session_fetch_by_lua\*, ssl_session_store_by_lua\*

更新Nginx当前的时间缓存，会涉及到一个系统调用。

###ngx.localtime
* 语法: str = ngx.localtime() 
* 环境: init_worker_by_lua\*, set_by_lua\*, rewrite_by_lua\*, access_by_lua\*, content_by_lua\*, header_filter_by_lua\*, body_filter_by_lua\*, log_by_lua\*, ngx.timer.\*， balancer_by_lua\*, ssl_certificate_by_lua\*, ssl_session_fetch_by_lua\*, ssl_session_store_by_lua\*

返回nginx缓存的时间的字符串，格式：yyyy-mm-dd hh:mm:ss
获取的是本地时间。
不涉及系统调用。

###ngx.utctime
* 语法: str = ngx.utctime() 
* 环境: init_worker_by_lua\*, set_by_lua\*, rewrite_by_lua\*, access_by_lua\*, content_by_lua\*, header_filter_by_lua\*, body_filter_by_lua\*, log_by_lua\*, ngx.timer.\*， balancer_by_lua\*, ssl_certificate_by_lua\*, ssl_session_fetch_by_lua\*, ssl_session_store_by_lua\*

返回nginx缓存的时间的字符串，格式：yyyy-mm-dd hh:mm:ss
获取的是UTC时间。
不涉及系统调用。

###ngx.cookie_time
* 语法: str = ngx.cookie_time(secs) 
* 环境: init_worker_by_lua\*, set_by_lua\*, rewrite_by_lua\*, access_by_lua\*, content_by_lua\*, header_filter_by_lua\*, body_filter_by_lua\*, log_by_lua\*, ngx.timer.\*， balancer_by_lua\*, ssl_certificate_by_lua\*, ssl_session_fetch_by_lua\*, ssl_session_store_by_lua\*

返回时间戳的一个可以用作cookie过期时间的格式化字符串。

```lua
 ngx.say(ngx.cookie_time(1290079655))
     -- yields "Thu, 18-Nov-10 11:27:35 GMT"
```


###ngx.http_time
* 语法: str = ngx.http_time(secs) 
* 环境: init_worker_by_lua\*, set_by_lua\*, rewrite_by_lua\*, access_by_lua\*, content_by_lua\*, header_filter_by_lua\*, body_filter_by_lua\*, log_by_lua\*, ngx.timer.\*， balancer_by_lua\*, ssl_certificate_by_lua\*, ssl_session_fetch_by_lua\*, ssl_session_store_by_lua\*

返回时间戳的一个可以用作 http 头部时间时间的格式化字符串。

```lua
 ngx.say(ngx.http_time(1290079655))
     -- yields "Thu, 18 Nov 2010 11:27:35 GMT"
```

###ngx.parse_http_time
* 语法: secs = ngx.parse_http_time(str) 
* 环境: init_worker_by_lua\*, set_by_lua\*, rewrite_by_lua\*, access_by_lua\*, content_by_lua\*, header_filter_by_lua\*, body_filter_by_lua\*, log_by_lua\*, ngx.timer.\*， balancer_by_lua\*, ssl_certificate_by_lua\*, ssl_session_fetch_by_lua\*, ssl_session_store_by_lua\*

将http时间格式的字符串转换成时间戳。


##正则匹配
###ngx.re.match
* 语法: capture, err = ngx.re.match(subject, regex, options?, ctx?, res_table?)
* 环境: init_worker_by_lua\*, set_by_lua\*, rewrite_by_lua\*, content_by_lua\*, header_filter_by_lua\*, body_filter_by_lua\*, log_by_lua\*, ngx.timer\*, balancer_by_lua\*, ssl_certificate_by_lua\*, ssl_session_fetch_by_lua\*, ssl_session_store_by_lua\*

匹配正则，匹配成功返回一个Lua表 capture。其中capture[0]保存匹配出的完整子字符串，capture[1]保存第一个括号内的子模板匹配结果，capture[2］保存第二个，以此类推。

```lua
local m, err = ngx.re.match("hello, 1234", "[0-9]+")
-- m[0] = 1234

local m, err = ngx.re.match("hello, 1234", "([0-9])[0-9]+")
-- m[0] = 1234
-- m[1] = 1


-- 为子模板起别名
local m, err = ngx.re.match("hello, 1234", "([0-9])(?<remaining>[0-9+])")
-- m[0] = 1234
-- m[1] = 1
-- m[2] = 234
-- m["remaining"] = 234

-- 子模板匹配不到时返回false
local m, err = ngx.re.match("hello, world", "(world)|(hello)|(?<named>howdy)")
-- m[0] == "hello"
-- m[1] == false
-- m[2] == "hello"
-- m[3] == false
-- m["named"] == false
```

####options参数
有以下这些选项，多个选项可以组合使用。
在优化性能时，选项“o”经常用到，该选项会使正则表达式模板仅被编译一次，之后缓存在worker级的缓存中，并被此nginx worker处理的所有请求共享。
“jo”选项最常被用到。

* a             
锚定模式 (仅从目标字符串开始位置匹配)

* d             
启用 DFA 模式(又名最长令牌匹配语义)。
此选项需要 PCRE 6.0 以上版本，否则将抛出 Lua 异常。
此选项最早出现在 ngx_lua v0.3.1rc30 版本中。

* D             
启用重复命名模板支持。子模板命名可以重复，在结果中以数组方式返回。例如：

```lua
local m = ngx.re.match("hello, world",
                   "(?<named>\w+), (?<named>\w+)",
                   "D")
-- m["named"] == {"hello", "world"}
```
此选项最早出现在 v0.7.14 版本中，需要 PCRE 8.12 以上版本支持.

* i             
大小写不敏感模式 (类似 Perl 的 /i 修饰符)

* j             
启用 PCRE JIT 编译，此功能需要 PCRE 8.21 以上版本以 --enable-jit 选项编译。
为达到最佳性能，此选项应与 'o' 选项同时使用。
此选项最早出现在 ngx_lua v0.3.1rc30 版本中。

* J             
启用 PCRE Javascript 兼容模式。
此选项最早出现在 v0.7.14 版本中，需要 PCRE 8.12 以上版本支持.

* m             
多行模式 (类似 Perl 的 /m 修饰符)

* o             
仅编译一次模式 (类似 Perl 的 /o 修饰符)
启用 worker 进程级正则表达式编译缓存。

* s             
单行模式 (类似 Perl 的 /s 修饰符)

* u             
UTF-8 模式。此选项需要 PCRE 以 --enable-utf8 选项编译，否则将抛出 Lua 异常。

* U         
类似 "u" 模式，但禁用了 PCRE 对目标字符串的 UTF-8 合法性检查。
此选项最早出现在 ngx_lua v0.8.1 版本中。

* x             
扩展模式 (类似 Perl 的 /x 修饰符)

####ctx参数
与正则表达式修饰符`a`组合使用，可以建立一个`ngx.re.match`词法分析器。

####res_table参数
指定保存匹配结果的Lua表


###ngx.re.find
* 语法: from, to, err = ngx.re.fing(subject, regex, options?, ctx?, nth?)
* 环境: init_worker_by_lua\*, set_by_lua\*, rewrite_by_lua\*, content_by_lua\*, header_filter_by_lua\*, body_filter_by_lua\*, log_by_lua\*, ngx.timer\*, balancer_by_lua\*, ssl_certificate_by_lua\*, ssl_session_fetch_by_lua\*, ssl_session_store_by_lua\*

正则匹配，返回匹配结果完整子字符串的开始索引和结束索引。返回的索引值基于1。
此函数不需要创建新的Lua字符串或者表，因此速度快于`ngx.re.match`。

```lua
 local s = "hello, 1234"
 local from, to, err = ngx.re.find(s, "([0-9]+)", "jo")
 if from then
     ngx.say("from: ", from)
     ngx.say("to: ", to)
     ngx.say("matched: ", string.sub(s, from, to))
 else
     if err then
         ngx.say("error: ", err)
         return
     end
     ngx.say("not matched!")
 end
 
-- from: 8
-- to: 11
-- matched: 1234
```

####nth参数
只能怪返回第几个子匹配结果，默认是0，返回所有。

```lua
 local str = "hello, 1234"
 local from, to = ngx.re.find(str, "([0-9])([0-9]+)", "jo", nil, 2)
 if from then
     ngx.say("matched 2nd submatch: ", string.sub(str, from, to))  -- yields "234"
 end
```

###ngx.re.gmatch
* 语法: iterator, err = ngx.re.gmatch(subject, regex, options?)
* 环境: init_worker_by_lua\*, set_by_lua\*, rewrite_by_lua\*, access_by_lua\*, content_by_lua\*, header_filter_by_lua\*, body_filter_by_lua\*, log_by_lua\*, ngx.timer.\*, balancer_by_lua\*, ssl_certificate_by_lua\*, ssl_session_fetch_by_lua\*, ssl_session_store_by_lua\*

匹配效果和`ngx.re.match`相同，但返回的是一个迭代器。每次调用这个迭代器的时候返回一个匹配结果。

```lua
local iterator, err = ngx.re.gmatch("hello, world!", "([a-z]+)", "i")
 if not iterator then
     ngx.log(ngx.ERR, "error: ", err)
     return
 end

 local m
 m, err = iterator()    -- m[0] == m[1] == "hello"
 if err then
     ngx.log(ngx.ERR, "error: ", err)
     return
 end

 m, err = iterator()    -- m[0] == m[1] == "world"
 if err then
     ngx.log(ngx.ERR, "error: ", err)
     return
 end

 m, err = iterator()    -- m == nil
 if err then
     ngx.log(ngx.ERR, "error: ", err)
     return
 end
```


###ngx.re.sub
* 语法: newstr, n, err = ngx.re.sub(subject, regex, replace, options?)
* 环境: init_worker_by_lua\*, set_by_lua\*, rewrite_by_lua\*, access_by_lua\*, content_by_lua\*, header_filter_by_lua\*, body_filter_by_lua\*, log_by_lua\*, ngx.timer.\*, balancer_by_lua\*, ssl_certificate_by_lua\*, ssl_session_fetch_by_lua\*, ssl_session_store_by_lua\*

将第一个匹配结果替换为字符串或函数类型参数 `replace`。
当replace是一个字符串时，直接替换。
当replace是一个函数时，将`ngx.re.match`的匹配结果传递给函数，最后取得函数的返回值来替换匹配到的字符串。

```lua
-- 字符串
 local newstr, n, err = ngx.re.sub("hello, 1234", "([0-9])[0-9]", "[$0][$1]")
 if newstr then
     -- newstr == "hello, [12][1]34"
     -- n == 1
 else
     ngx.log(ngx.ERR, "error: ", err)
     return
 end
 
 -- 字符串中可以使用$符号来取得ngx.re.match匹配的结果集
  local newstr, n, err = ngx.re.sub("hello, 1234", "[0-9]", "${0}00")
     -- newstr == "hello, 100234"
     -- n == 1

-- 使用$来转义$
 local newstr, n, err = ngx.re.sub("hello, 1234", "[0-9]", "$$")
     -- newstr == "hello, $234"
     -- n == 1

-- 函数
 local func = function (m)
     return "[" .. m[0] .. "][" .. m[1] .. "]"
 end
 local newstr, n, err = ngx.re.sub("hello, 1234", "( [0-9] ) [0-9]", func, "x")
     -- newstr == "hello, [12][1]34"
     -- n == 1

```




###ngx.re.gsub
* 语法: newstr, n, err = ngx.re.gsub(subject, regex, replace, options?)
* 环境: init_worker_by_lua\*, set_by_lua\*, rewrite_by_lua\*, access_by_lua\*, content_by_lua\*, header_filter_by_lua\*, body_filter_by_lua\*, log_by_lua\*, ngx.timer.\*, balancer_by_lua\*, ssl_certificate_by_lua\*, ssl_session_fetch_by_lua\*, ssl_session_store_by_lua\*

效果和`ngx.re.sub`类似，但执行全局替换。

```lua
 local newstr, n, err = ngx.re.gsub("hello, world", "([a-z])[a-z]+", "[$0,$1]", "i")
 if newstr then
     -- newstr == "[hello,h], [world,w]"
     -- n == 2
 else
     ngx.log(ngx.ERR, "error: ", err)
     return
 end
```

##共享内存中的字典
###ngx.shared.DICT
* 语法: dict = ngx.shared.DICT
* 语法: dict = ngx.shared[name_var]
* 环境: init_worker_by_lua\*, set_by_lua\*, rewrite_by_lua\*, access_by_lua\*, content_by_lua\*, header_filter_by_lua\*, body_filter_by_lua\*, log_by_lua\*, ngx.timer.\*, balancer_by_lua\*, ssl_certificate_by_lua\*, ssl_session_fetch_by_lua\*, ssl_session_store_by_lua\*

获取变量名为DICT的Lua字典对象，该对象是一个共享内存区块，通过`lua_shard_dict`指令定义大小。
所共享的区块被当前nginx实例的所有worker进程共享。
当实例重新加载配置时，共享内存的字典内容不会丢失

```nginx
http {
    lua_shared_dict dogs 10m;
    server {
        location /set {
            content_by_lua '
                local dogs = ngx.shared.dogs
                dogs:get("Jim", 8)
                ngx.say("STORED")
            ';
        }
        
        location /get {
             content_by_lua '
                 local dogs = ngx.shared.dogs
                 ngx.say(dogs:get("Jim"))
             ';
         }

    }
}
```

###ngx.shared.DICT.get
* 语法: value, flags = ngx.shared.DICT:get(key)
* 环境: set_by_lua\*, rewrite_by_lua\*, access_by_lua\*, content_by_lua\*, header_filter_by_lua\*, body_filter_by_lua\*, log_by_lua\*, ngx.timer.\*, balancer_by_lua\*, ssl_certificate_by_lua\*, ssl_session_fetch_by_lua\*, ssl_session_store_by_lua\*

获取共享内存字典中的一个key的值，如果该key不存在或者过期，返回nil。
返回值的类型保持写入字典时的原始数据类型。

```lua
local cats = ngx.shared.cats
local value, flags = cats.get(cats, "Marry")
```
> flag是写入时给予的值，默认是0，如果写入时没有传入该参数，则在这里不会返回。 

###ngx.shared.DICT.get_stale
* 语法: value, flags, stale = ngx.shared.DICT:get_stale(key)
* 环境: set_by_lua\*, rewrite_by_lua\*, access_by_lua\*, content_by_lua\*, header_filter_by_lua\*, body_filter_by_lua\*, log_by_lua\*, ngx.timer.\*, balancer_by_lua\*, ssl_certificate_by_lua\*, ssl_session_fetch_by_lua\*, ssl_session_store_by_lua\*

即使key过期也依然返回该key的值。
返回的stale用来标识该key是否已经过期。
> 已过期的key可能会被删除，所以不一定会返回。

###ngx.shared.DICT.set
* 语法: success, err, forcible = ngx.shared.DICT:set(key, value, exptime?, flags?)
* 环境: init_by_lua\*, set_by_lua\*, rewrite_by_lua\*, access_by_lua\*, content_by_lua\*, header_filter_by_lua\*, body_filter_by_lua\*, log_by_lua\*, ngx.timer.\*, balancer_by_lua\*, ssl_certificate_by_lua\*, ssl_session_fetch_by_lua\*, ssl_session_store_by_lua\*

在ngx.shared.DICT中设置一个key-value键值对。返回success标识是否存储成功；forcible标识是否因为存储空间不足而有其他的可用项被强制删除。
`value`可以是布尔值，数字，字符串或nil；
`exptime`单位是s，可以精确到0.001，默认是0，表示永不过期。
当无法给当前要set的key-value分配内存时，会使用LRU算法删除存储中已有的项，会优先考虑过期时间。如果删除了十项以后空间依旧不足，`success`会返回false，同时 err 将返回 `no memory`
如果执行成功的同时移除了字典中其他尚未过期的项，`forcible`会返回true，否则返回false。

```lua
local cats = ngx.shared.cats
local succ, err, forcible = cats.set(cats, "Marry", "it is a nice cat!")
```

###ngx.shared.DICT.safe_set
* 语法: ok, err = ngx.shared.DICT:safe_set(key, value, exptime?, flags?)
当内存不足，不会通过删除有效的项来完成当前key-value的添加。此时会返回nil和 `no memory` 。

###ngx.shared.DICT.add
* 语法: success, err, forcible = ngx.shared.DICT:add(key, value, exptime?, flags?)
类似setnx，只有内存字典中不存在改key的项（不存在或已过期），才会设置成功。否则返回`exist`错误。

###ngx.shared.DICT.safe_add
* 语法: ok, err = ngx.shared.DICT:safe_add(key, value, exptime?, flags?)
当内存不足时，不会强制执行add操作。

###ngx.shared.DICT.replace
* 语法: success, err, forcible = ngx.shared.DICT:replace(key, value, exptime?, flags?)
类似setx，只有内存字典中存在该key且还未过期，才会设置成功，否则返回`not found`错误。

###ngx.shared.DICT.delete
* 语法: ngx.shared.DICT:delete(key)
删除key

###ngx.shared.DICT.incr
* 语法: newval, err, forcible? = ngx.shared.DICT:incr(key, value, init?)

将内存字典中的key增加value，如果key不存在或已过期，则会拿init参数作为key的原始值。如果key不存在或已经过期且没有传递init或init未nil，则返回`not found`错误。
当内存空间不足时，同样会根据LRU算法覆盖已有的值。
当init没有指定时，forcible返回用于为nil。

###ngx.shared.DICT.flush_all
* 语法: ngx.shared.DICT:flush_all()
清空内存字典内容。实际内存并没有被释放，只是将所有的key标记为已过期。

###ngx.shared.DICT.flush_expired
* 语法: flushed = ngx.shared.DICT:flush_expired(max_count?)
删除已经过期的key，返回删除的个数。max_count默认是0，表示清除所有，返回实际上删除的数量。
该方法会将删除掉的已过期的内容占用的内存释放。

###ngx.shared.DICT.get_keys
* 语法: keys = ngx.shared.DICT:get_keys(max_count?)
获取字典中存储的key列表，默认返回前1024个，当max_count为0时，返回所有。



##socket
###ngx.socket.udp
###udpsock:setpeername
###udpsock:send
###udpsock:receive
###udpsock:close
###udpsock:settimeout
###ngx.socket.stream
###ngx.socket.tcp
###tcpsock:connect
###tcpsock:sslhandshake
###tcpsock:send
###tcpsock:receive
###tcpsock:receiveuntil
###tcpsock:close
###tcpsock:settimeout
###tcpsock:setoption
###tcpsock:setkeepalive
###tcpsock:getreusedtimes
###ngx.socket.connect


##线程
###ngx.get_phase
###ngx.thread.spawn
###ngx.thread.wait
###ngx.thread.kill
###ngx.on_abort
###ngx.timer.at
###ngx.timer.running_count
###ngx.timer.pending_count

##Nginx配置
###ngx.config.subsystem
###ngx.config.debug
###ngx.config.prefix
###ngx.config.nginx_version
###ngx.config.nginx_configure
###ngx.config.ngx_lua_version

##Nginx worker进程
###ngx.worker.exiting
###ngx.worker.pid
###ngx.worker.count
###ngx.worker.id
###ngx.semaphore
###ngx.balancer
###ngx.ssl
###ngx.ocsp
###ndk.set_var.DIRECTIVE
###coroutine.create
###coroutine.resume
###coroutine.yield
###coroutine.wrap
###coroutine.running
###coroutine.status

