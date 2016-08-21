# ngx_lua_module配置指令
##环境配置
###lua_use_default_type
* 语法: lua_use_default_type on | off
* 默认: lua_use_default_type on
* 环境: http, server, location, location if

指定响应头中`Content-Type`的默认值，开启的话会使得`default_type`指令指定的MIME类型生效。

###lua_code_cache
* 语法: lua_code_cache on | off
* 默认: lua_code_cache on
* 环境: http, server, location, location if

打开或者关闭 `*_by_lua_file` 指令（类似 set_by_lua_file 和 content_by_lua_file） 中指定的文件，以及Lua模块的Lua代码缓存。
缓存关闭，每个ngx_lua处理的请求会运行在一个单独的Lua虚拟机实例中。
当缓存打开时，如果修改了`*_by_lua_file`指定的文件，缓存并不会更新，只有重新加载配置文件才能使得改动生效。需要重启Nginx或者发送HUP信号。

```shell
kill -HUP pid
nginx -s reload
``` 

###lua_regex_cache_max_entries
* 语法: lua_regex_cache_max_entries <num>
* 默认: lua_regex_cache_max_entries 1024
* 环境: http

在工作进程级别，指定正则表达式编译缓存允许的最大数目。
当使用`ngx.re.match`，`ngx.re.gmatch`，`ngx.re.sub`和 `ngx.re.gsub`等正则匹配方法时，如果使用o选项，匹配结果会被缓存。
当缓存数量超过了限制，新的正则表达式使用o选项时不会被缓存。

###lua_package_path
* 语法: lua_package_path <lua-style-path-str>
* 默认: 当前环境 LUA_PATH 的环境变量或编译指定的默认值
* 环境: http

设置Lua模块的查找路径，包括`set_by_lua`，`content_by_lua`指令中加载的模块。

###lua_package_cpath
* 语法: lua_package_cpath <lua-style-cpath-str>
* 默认: 当前环境 LUA_CPATH 的环境变量或编译指定的默认值
* 环境: http

设置Lua C模块的查找路径，包括`set_by_lua`，`content_by_lua`指令中加载的模块。

###lua_shared_dict
* 语法: lua_shared_dict <name> <size>
* 默认: no
* 环境: http
* 阶段: depends on usage

在共享的内存区域中声明一个变量<name>，用来存储Lua字典 `ngx.shared.<name>`。在当前的Nginx实例中，该变量被所有nginx worker进程共享。

```nginx
http {
    lua_shared_dict dogs 10m;
    ...
}
```

##初始化阶段

###init_by_lua
* 语法: init_by_lua <lua-script-str>
* 环境: http
* 阶段: loading-config

Nginx的master进程在`加载配置文件`时，在全局的Lua虚拟机上运行该命令指定的Lua代码，类似初始化。


###init_by_lua_block
* 语法: init_by_lua_block { lua-script }
* 环境: http
* 阶段: loading-config

作用和`init_by_lua`一样，但是带花括号中嵌入代码，特殊字符需要转义。

```shell
init_by_lua_block {
     print("I need no extra escaping here, for example: \r\nblah")
 }
```
 
###init_by_lua_file
* 语法: init_by_lua_file <path-to-lua-script-file>
* 环境: http
* 阶段: loading-config

作用和`init_by_lua`一样，但给定的参数一个文件路径，如果是相对路径，是相对于nginx启动时指定的-p选项的参数。

###init_worker_by_lua
* 语法: init_worker_by_lua <lua-script-str>
* 环境: http
* 阶段: starting-worker

如果开启master模式，会在`worker进程启动时`执行指定的Lua代码。
如果关闭master模式，会在`init_by_lua* `后直接运行。
通常用来创建单进程反复执行定时器，可以说后端服务健康检查，也可以是其他定时任务。

```lua
init_worker_by_lua '
     local delay = 3  -- in seconds
     local new_timer = ngx.timer.at
     local log = ngx.log
     local ERR = ngx.ERR
     local check

     check = function(premature)
         if not premature then
             -- do the health check or other routine work
             local ok, err = new_timer(delay, check)
             if not ok then
                 log(ERR, "failed to create timer: ", err)
                 return
             end
         end
     end

     local ok, err = new_timer(delay, check)
     if not ok then
         log(ERR, "failed to create timer: ", err)
         return
     end
 ';
```

###init_worker_by_lua_block
* 语法: init_worker_by_lua_block { lua-script }
* 环境: http
* 阶段: starting-worker

###init_worker_by_lua_file
* 语法: init_worker_by_lua_file <lua-file-path>
* 环境: http
* 阶段: starting-worker

###lua_need_request_body
* 语法: lua_need_request_body <on|off>
* 默认: off
* 环境: http, server, location, location if
* 阶段: depends on usage

在运行rewrite/access/access_by_lua*之前决定是都强制获取请求体数据。
Nginx内部默认不读取客户端的请求，如果该指令配置为off，需要在Lua代码中调用`ngx.req.read_body`函数来获取请求体数据。

为了读取`$request_body`，`client_body_buffer_size`要和`client_max_body_size`有同样大小，如果内容大小超过`client_body_buffer_size`但是小于`client_max_body_size`时，Nginx会将缓冲内存数据存到磁盘的临时文件，会导致`$request_body`变量是一个空值。

> 推荐使用`ngx.req.read_body`和`ngx.req.discard_body`函数来处理请求数据，可以更好地控制请求体的读取过程。

##处理请求阶段

###set_by_lua
* 语法: set_by_lua $res <lua-script-str> [$arg1 $arg2 ...]
* 环境: server, server if, location, location if
* 阶段: rewrite

通过lua脚本来定义一个nginx变量。
arg是可选参数，可将这些参数传递到lua脚本中，lua脚本执行后将结果返回给要定义的变量。
该指令一次只能定义一个nginx变量。

```lua
location /foo {
     set $diff ''; # we have to predefine the $diff variable here

     set_by_lua $sum '
         local a = 32
         local b = 56

         ngx.var.diff = a - b;  -- write to $diff directly
         return a + b;          -- return the $sum value normally
     ';
 }
 ```
 
该指令中不能使用的API

* 输出 API 函数 (例如 `ngx.say` 和 `ngx.send_headers`)
* 控制 API 函数 (例如 `ngx.exit`)
* 子请求 API 函数 (例如 `ngx.location.capture` 和 `ngx.location.capture_multi`)
* Cosocket API 函数 (例如 `ngx.socket.tcp` 和 `ngx.req.socket`)
* 休眠 API 函数 `ngx.sleep`

可以和其他指令模块混合使用，

* ngx_http_rewrite_module
* set-misc-nginx-module 
* array-var-nginx-module
混合使用后指令的执行顺序，和配置文件中出现的顺序一致。

###set_by_lua_block
* 语法: set_by_lua_block $res { lua-script }
* 环境: server, server if, location, location if
* 阶段: rewrite

作用和set_by_lua类似。

```lua
 set_by_lua_block $res { return 32 + math.cos(32) }
 # $res now has the value "32.834223360507" or alike.
 ```
 
###set_by_lua_file
* 语法: set_by_lua_file $res <path-to-lua-script-file> [$arg1 $arg2 ...]
* 环境: server, server if, location, location if
* 阶段: rewrite

指定lua文件，其他作用和set_by_lua类似。
如果开启了Lua代码缓存，每次修改文件时需要加载配置文件才生效。

###rewrite_by_lua
* 语法: rewrite_by_lua <lua-script-str>
* 环境: http, server, location, location if
* 阶段: rewrite tail

在重写阶段执行指定的Lua代码。代码中可以调用所有的API，并作为一个新的协程，在一个独立的全局环境中执行。
该指令的处理过程总是在标准的`ngx_http_rewrite_module`之后。因此如果location中有rewrite的话，rewrite_by_lua是不会被执行的。

```nginx
# 1.能够按照顺序执行
location /foo {
     set $a 12; # create and initialize $a
     set $b ""; # create and initialize $b
     rewrite_by_lua 'ngx.var.b = tonumber(ngx.var.a) + 1';
     echo "res = $b";
}

# 2.不能够顺序执行，因为if中的代码会在rewrite之前执行
location /foo {
    set $a 12; # create and initialize $a
    set $b ''; # create and initialize $b
    rewrite_by_lua 'ngx.var.b = tonumber(ngx.var.a) + 1';
    if ($b = '13') {
        rewrite ^ /bar redirect;
        break;
    }
    echo "res = $b";
}

# 2.改成以下形式
location /foo {
    set $a 12; # create and initialize $a
    set $b ''; # create and initialize $b
    rewrite_by_lua '
        ngx.var.b = tonumber(ngx.var.a) + 1
        if (ngx.var.b = '13')) 
            return ngx.direct("/bar")
        end
    ';
    echo "res = $b";
}

```

如果在`rewrite_by_lua`中调用`ngx.exit(ngx.OK)`时，并不会结束当前请求，而是继续执行下一阶段的内容处理。
要在`rewrite_by_lua`结束当前请求，需要`ngx.exit()`返回status>=200(`ngx.HTTP_OK`)且status<300(`ngx.HTTP_SPECIAL_RESPONSE`)，失败的请求返回`ngx.HTTP_INTERNAL_SERVER_ERROR`。

> `ngx_eval`模块可以通过`rewrite_by_lua`近似实现

```nginx
# ngx_eval实现
location / {
     eval $res {
         proxy_pass http://foo.com/check-spam;
     }

     if ($res = 'spam') {
         rewrite ^ /terms-of-use.html redirect;
     }

     fastcgi_pass ...;
 }
 
# rewrite_by_lua实现
location = /check-spam {
     internal;
     proxy_pass http://foo.com/check-spam;
 }

 location / {
     rewrite_by_lua '
         local res = ngx.location.capture("/check-spam")
         if res.body == "spam" then
             return ngx.redirect("/terms-of-use.html")
         end
     ';

     fastcgi_pass ...;
 }
```

###rewrite_by_lua_block
* 语法: rewrite_by_lua_block { lua-script }
* 环境: http, server, location, location if
* 阶段: rewrite tail

在重写阶段执行花括号中的Lua代码。

###rewrite_by_lua_file
* 语法: rewrite_by_lua_file <path-to-lua-script-file>
* 环境: http, server, location, location if
* 阶段: rewrite tail

在重写阶段执行指定文件的Lua代码。
注意相对路径及代码缓存情况，支持通过Nginx变量完成动态调度文件路径。

###access_by_lua
* 语法: access_by_lua <lua-script-str>
* 环境: http, server, location, location if
* 阶段: access tail

在access处理阶段，对每个请求执行指定的Lua代码。
该指令的处理总是在标准`ngx_http_access_module`的后面。

```nginx
# 1.能按照预期工作，除了白名单，其他ip都无法到达mysql的请求
location / {
    # start-标准ngx_http_access_module
    deny    192.168.1.1;
    allow   192.168.1.0/24;
    allow   10.1.1.0/16;
    deny    all;
    # end-标准ngx_http_access_module
    
    access_by_lua '
        local res = ngx.location.capture("/mysql", { ... })
       ...
    ';

    # proxy_pass/fastcgi_pass/...
 }
```

如果在`access_by_lua`中调用`ngx.exit(ngx.OK)`时，并不会结束当前请求，而是继续执行下一阶段的内容处理。
要在`access_by_lua`结束当前请求，需要`ngx.exit()`返回status>=200(`ngx.HTTP_OK`)且status<300(`ngx.HTTP_SPECIAL_RESPONSE`)，失败的请求返回`ngx.HTTP_INTERNAL_SERVER_ERROR`。

###access_by_lua_block
* 语法: access_by_lua_block { lua-script }
* 环境: http, server, location, location if
* 阶段: access tail

在access阶段执行{}中指定的Lua代码。

###access_by_lua_file
* 语法: access_by_lua_file <path-to-lua-script-file>
* 环境: http, server, location, location if
* 阶段: access tail

在access阶段执行指定的Lua文件。
注意相对路径及代码缓存情况，支持通过Nginx变量完成动态调度文件路径。

###rewrite_by_lua_no_postpone
* 语法: rewrite_by_lua_no_postpone on|off
* 默认: rewrite_by_lua_no_postpone off
* 环境: http

开启或禁用 `rewrite_by_lua*` 指令在rewrite阶段的延迟执行。
默认是off，即在rewrite阶段Lua代码会被延迟到最后执行。

###access_by_lua_no_postpone
* 语法: access_by_lua_no_postpone on|off
* 默认: access_by_lua_no_postpone off
* 环境: http

开启或禁用 `access_by_lua*` 指令在access阶段的延迟执行。
默认是off，即在access阶段Lua代码会被延迟到最后执行。

##内容生成阶段

###balancer_by_lua_block
* 语法: balancer_by_lua_block { lua-script }
* 环境: upstream
* 阶段: content

在负载均衡阶段执行Lua代码，在upstream中配置。
通过 `lua-resty-core` 库的 `ngx.balancer`能做到完全忽略upstream中的服务列表。 

```nginx
# 1. 例子
upstream foo {
     server 127.0.0.1;
     balancer_by_lua_block {
         -- 使用 Lua 作为一个动态均衡器完成一些有趣的事情
     }
 }

 server {
     location / {
         proxy_pass http://foo;
     }
 }
 
 # 2.做ip hash调度
 upstream backend{
    server 0.0.0.0;
    balancer_by_lua_block {
        local balancer = require "ngx.balancer"
        local host = {"192.168.1.111", "192.168.1.112"}
        local backend = ""
        local port = ngx.var.server_port
        local remote_ip = ngx.var.remote_addr
        local key = remote_ip..port
        local hash = ngx.crc32_long(key);
        hash = (hash % 2) + 1
        backend = host[hash]
        ngx.log(ngx.DEBUG, "ip_hash=", ngx.var.remote_addr, " hash=", hash, " up=", backend, ":", port)
        -- 远程调用
        local ok, err = balancer.set_current_peer(backend, port)
        if not ok then
            ngx.log(ngx.ERR, "failed to set the current peer: ", err)
            return ngx.exit(500)
        end
        ngx.log(ngx.DEBUG, "current peer ", backend, ":", port)
    }
}

server {
	listen 80;
	listen 8080;
	listen 7777;
	server_name *.x.com
	location / {
		proxy_pass http://backend;
	}
}
```

###balancer_by_lua_file
* 语法: balancer_by_lua_file <path-to-lua-script-file>
* 环境: upstream
* 阶段: content

###content_by_lua
* 语法： content_by_lua <lua-script-str>
* 环境： location, location if
* 阶段： content

内容处理程序，为每一个请求执行一次Lua代码。
不可将本指令和其他内容处理程序指令放在同一个location中。例如不可和`proxy_pass`指令放在同一个location。

###content_by_lua_block
* 语法: content_by_lua_block { lua-script }
* 环境: location, location if
* 阶段: content

在花括号中嵌入Lua代码。

###content_by_lua_file
* 语法: content_by_lua_file <path-to-lua-script-file>
* 环境: location, location if
* 阶段: content

通过文件路径来指定代码。
注意相对路径及代码缓存情况，支持通过Nginx变量完成动态调度文件路径。

```lua
# 注意: nginx 变量必须要小心过滤，否则它将带来严重的安全风险！
 location ~ ^/app/([-_a-zA-Z0-9/]+) {
     set $path $1;
     content_by_lua_file /path/to/lua/app/root/$path.lua;
 }
```

> `ngx_auth_request`模块可以使用`access_by_lua`实现

```nginx
# ngx_auth_request模块
location / {
     auth_request /auth;

     # proxy_pass/fastcgi_pass/postgres_pass/...
 }

# access_by_lua实现
location / {
     access_by_lua '
         local res = ngx.location.capture("/auth")

         if res.status == ngx.HTTP_OK then
             return
         end

         if res.status == ngx.HTTP_FORBIDDEN then
             ngx.exit(res.status)
         end

         ngx.exit(ngx.HTTP_INTERNAL_SERVER_ERROR)
     ';

     # proxy_pass/fastcgi_pass/postgres_pass/...
 }

```

###header_filter_by_lua
* 语法： header_filter_by_lua <lua-script-str>
* 环境： http, server, location, location if
* 阶段： output-header-filter

响应头过滤阶段执行指定的Lua代码。
在代码中无法使用以下接口函数：

* 输出类函数（例：`ngx.say` 和 `ngx.send_headers`）
* 控制类函数（例：`ngx.redirect` 和 `ngx.exec`）
* 子请求相关函数（例：`ngx.location.capture`和`ngx.location.capture_multi`）
* cosocket 类函数（例：`ngx.socket.tcp` 和 `ngx.req.socket`）

```nginx
# 添加/修改响应头中的变量
location / {
    proxy_pass http://mybackend;
    header_filter_by_lua 'ngx.header.Foo = "blah"';
}
 ```
 
###header_filter_by_lua_block
* 语法: header_filter_by_lua_block { lua-script }
* 环境: http, server, location, location if
* 阶段: output-header-filter

在响应头过滤阶段执行{}中指定的Lua代码。

```nginx
 header_filter_by_lua_block {
     ngx.header["content-length"] = nil
 }
 ```
 
###header_filter_by_lua_file
* 语法: header_filter_by_lua_file <path-to-lua-script-file>
* 环境: http, server, location, location if
* 阶段: output-header-filter

在响应头过滤阶段执行指定的Lua文件。
注意相对路径和文件缓存情况。

###lua_transform_underscores_in_response_headers
* 语法: lua_transform_underscores_in_response_headers on|off
* 默认: lua_transform_underscores_in_response_headers on
* 环境: http, server, location, location-if

是否将响应头中的下划线转换为连接线(-)。

###body_filter_by_lua
* 语法: body_filter_by_lua <lua-script-str>
* 环境: http, server, location, location if
* 阶段: output-body-filter

响应体过滤处理阶段执行指定的Lua代码。
以ngx.arg[1]（Lua的字符串类型）表示原始的返回Body。
ngx.arg[2]（Lua的布尔值形式）表示Body的结束标识，当该变量为true，抛弃后面所有的响应体。
如果要立刻终止数据流输出，可使用以下代码

```Lua
 return ngx.ERROR
```
以上代码会截断响应体，导致结果不完整，导致响应无效。

```nginx
# 1.将响应头转换成大写
location / {
    proxy_pass http://mybackend;
    body_filter_by_lua  'ngx.arg[1] = string.upper(ngx.arg[1])';
}

# 2.只返回hello world
# 每一个echo/响应输出都会调用一个body_filter_by_lua内的代码
location /t {
    echo hello world;
    echo hiya globe;

    body_filter_by_lua '
        local chunk = ngx.arg[1]
        if string.match(chunk, "hello") then
            ngx.arg[2] = true  -- 当出现了hello，设置已经结束
                               --抛弃后面的响应体剩下的部分，即hiya globe
            return
        end

        -- just throw away any remaining chunk data
        ngx.arg[1] = nil
    ';
}
```

该指令不可用的API：

* 输出 API 函数类（例如：`ngx.say` 和 `ngx.send_headers`）
* 控制 API 函数类（例如：`ngx.redirect` 和 `ngx.exec`）
* 子请求函数类（例如：`ngx.location.capture` 和 `ngx.location.capture_multi`）
* cosocket 函数类（例如：`ngx.socket.tcp` 和 `ngx.req.socket`）


###body_filter_by_lua_block
* 语法: body_filter_by_lua_block { lua-script-str }
* 环境: http, server, location, location if
* 阶段: output-body-filter

响应体过滤处理阶段执行{}中指定的Lua代码。


###body_filter_by_lua_file
* 语法: body_filter_by_lua_file <path-to-lua-script-file>
* 环境: http, server, location, location if
* 阶段: output-body-filter

响应体过滤处理阶段执行中指定文件中的Lua代码。
注意相对路径的情况。

##日志阶段
###log_by_lua
* 语法: log_by_lua <lua-script-str>
* 环境: http, server, location, location if
* 阶段: log

在log处理阶段执行指定的Lua代码，在access log处理之前执行。

```nginx
# 收集 $upstream_response_time 平均处理
lua_shared_dict log_dict 5M;

server {
    location / {
        proxy_pass http://mybackend;

        log_by_lua '
            local log_dict = ngx.shared.log_dict
            local upstream_time = tonumber(ngx.var.upstream_response_time)

            local sum = log_dict:get("upstream_time-sum") or 0
            sum = sum + upstream_time
            log_dict:set("upstream_time-sum", sum)

            local newval, err = log_dict:incr("upstream_time-nb", 1)
            if not newval and err == "not found" then
                log_dict:add("upstream_time-nb", 0)
                log_dict:incr("upstream_time-nb", 1)
            end
        ';
    }

    location = /status {
        content_by_lua '
            local log_dict = ngx.shared.log_dict
            local sum = log_dict:get("upstream_time-sum")
            local nb = log_dict:get("upstream_time-nb")

            if nb and sum then
                ngx.say("average upstream response time: ", sum / nb,
                       " (", nb, " reqs)")
            else
                ngx.say("no data yet")
            end
        ';
    }
}
```

###log_by_lua_block
* 语法: log_by_lua_block { lua-script }
* 内容: http, server, location, location if
* 阶段: log

###log_by_lua_file
* 语法: log_by_lua_file <path-to-lua-script-file>
* 环境: http, server, location, location if
* 阶段: log

##SSL相关
如果开启了HTTPS，SSL相关的过程发生在 `set_by_lua*` 之前。

###ssl_certificate_by_lua_block
* 语法: ssl_certificate_by_lua_block { lua-script }
* 环境: server
* 阶段: right-before-SSL-handshake

当下游请求是https时，进行https的握手连接时，执行指定的Lua代码。

* 可通过非阻塞IO操作，从远程加载SSL握手配置；
* 可在 `lua-resty-limit-traffic`的辅助下，以非阻塞的方式完成SSL握手信号控制；

同时需要配置 `ssl_certificate` 和 `ssl_certificate_key` 指令

更多例子参考文档[ngx.ssl](https://github.com/openresty/lua-resty-core/blob/master/lib/ngx/ssl.md)

###ssl_certificate_by_lua_file
* 语法: ssl_certificate_by_lua_file <path-to-lua-script-file>
* 环境: server
* 阶段: right-before-SSL-handshake

###ssl_session_fetch_by_lua_block
* 语法: ssl_session_fetch_by_lua_block { lua-script }
* 环境: server
* 阶段: right-before-SSL-handshake

该指令执行的代码，根据当前下游的 SSL 握手请求中的会话 ID，查找并加载 SSL 会话（如果有）。
该指令和 `ssl_session_store_by_lua*` 一起使用，可以实现纯Lua的分布式缓存模型（基于 cosocket API）。如果找到一个已缓存的SSL会话，则会将其加载到当前的SSL会话环境中，SSL会话将立即启动恢复，绕过昂贵的完整SSL握手过程。

如果同时配置了 `ssl_certificate_by_lua*`， `ssl_session_fetch_by_lua_block`会在`ssl_certificate_by_lua*`之前运行，当找到并恢复了缓存的SSL会话，则会绕过`ssl_certificate_by_lua*`过程。同时也会绕过 `ssl_session_store_by_lua_block`指令的执行，因为此时不需要保存会话。

###ssl_session_fetch_by_lua_file
* 语法: ssl_session_fetch_by_lua_file <path-to-lua-script-file>
* 环境: server
* 阶段: right-before-SSL-handshake

通过Lua脚本文件，根据下游SSL握手请求中的会话ID，查找并加载SSL会话。

###ssl_session_store_by_lua_block
* 语法: ssl_session_store_by_lua_block { lua-script }
* 环境: server
* 阶段: right-after-SSL-handshake

通过指定的Lua代码，根据下游的SSL握手请求中的会话ID，获取并保存SSL会话。
被保存或缓存的SSL会话数据能被用来以后的SSL连接，到时候恢复SSL会话不再需要经历完整的SSL握手过程。

###ssl_session_store_by_lua_file
* 语法: ssl_session_store_by_lua_file <path-to-lua-script-file>
* 环境: server
* 阶段: right-before-SSL-handshake

通过Lua脚本文件，根据下游的SSL握手请求中的会话ID，获取并保存SSL会话。

###lua_ssl_ciphers
* 语法: lua_ssl_ciphers <ciphers>
* 默认: lua_ssl_ciphers DEFAULT
* 环境: http, server, location

指定 `tcpsock:sslhandshake` 方法请求SSL/TLS服务的加密方式。
其中参数 ciphers 是 OpenSSL 库里面指定的格式。可以使用 “openssl ciphers” 来查看完整的加密方式列表。

###lua_ssl_crl
* 语法: lua_ssl_crl <file>
* 默认: no
* 环境: http, server, location

指定一个 PEM 格式吊销证书文件，在 `tcpsock:sslhandshake` 方法里验证 SSL/TLS 服务的证书。

###lua_ssl_protocols
* 语法: lua_ssl_protocols [SSLv2] [SSLv3] [TLSv1] [TLSv1.1] [TLSv1.2]
* 默认: lua_ssl_protocols SSLv3 TLSv1 TLSv1.1 TLSv1.2
* 环境: http, server, location

在 `tcpsock:sslhandshake` 方法中开启请求 SSL/TLS 服务的传输协议列表。

###lua_ssl_trusted_certificate
* 语法: lua_ssl_trusted_certificate <file>
* 默认: no
* 环境: http, server, location

指定一个 PEM 格式信任 CA 证书文件，在 `tcpsock:sslhandshake` 方法里验证 SSL/TLS 服务的证书。

###lua_ssl_verify_depth
* 语法: lua_ssl_verify_depth <number>
* 默认: lua_ssl_verify_depth 1
* 环境: http, server, location

设置服务端证书链的验证深度。

##socket相关

###lua_socket_connect_timeout
* 语法: lua_socket_connect_timeout <time>
* 默认: lua_socket_connect_timeout 60s
* 环境: http, server, location

该指令控制 TCP/unix-domain socket 对象的 `connect` 方法默认超时时间，这个值可以被 `settimeout` 方法覆盖。

`<time>`参数可以是整数，后面可以跟着像s (秒), ms (毫秒), m (分钟)的单位可选项。 默认的时间单位是s，也就是"秒"。默认值是60s。

###lua_socket_send_timeout
* 语法: lua_socket_send_timeout <time>
* 默认: lua_socket_send_timeout 60s
* 环境: http, server, location

该指令控制 TCP/unix-domain socket 对象的 `send` 方法默认超时时间，这个值可以被 `settimeout` 方法覆盖。

`<time>`参数可以是整数，后面可以跟着像s (秒), ms (毫秒), m (分钟)的单位可选项。 默认的时间单位是s，也就是"秒"。默认值是60s。

###lua_socket_send_lowat
* 语法: lua_socket_send_lowat <size>
* 默认: lua_socket_send_lowat 0
* 环境: http, server, location

控制 `cosocket` 发送缓冲区 `lowat`（低水位）的值。

###lua_socket_read_timeout
* 语法: lua_socket_read_timeout <time>
* 默认: lua_socket_read_timeout 60s
* 环境: http, server, location
* 阶段: 依赖于使用环境

该指令控制 TCP/unix-domain socket 对象的 `receive` 方法、`receiveuntil` 方法返回迭代函数的默认超时时间。这个值可以被 `settimeout` 方法覆盖。

`<time>`参数可以是整数，后面可以跟着像s (秒), ms (毫秒), m (分钟)的单位可选项。 默认的时间单位是s，也就是"秒"。默认值是60s。

###lua_socket_buffer_size
* 语法: lua_socket_buffer_size <size>
* 默认: lua_socket_buffer_size 4k/8k
* 环境: http, server, location

指定使用 cosocket 进行读取操作时的缓冲区大小。
cosocket支持 100% 的非缓存读取和解析，因此不必为了同时满足所有的请求而把该值设置太大。
即使是将该值设置为1KB，cosocket仍然能正常工作，只是效率比较糟糕。

###lua_socket_pool_size
* 语法: lua_socket_pool_size <size>
* 默认: lua_socket_pool_size 30
* 环境: http, server, location

指定每个cosocket通过远程服务关联的连接池的大小限制（使用主机+端口配对或unix socket文件路径作为标识），即每个地址中的连接数。
当连接池中连接数超过限制大小，在连接池中最近最少使用的空闲连接关闭。
这里的限制是针对每个独立的worker进程生效，而不是每个Nginx服务实例。

###lua_socket_keepalive_timeout
* 语法: lua_socket_keepalive_timeout <time>
* 默认: lua_socket_keepalive_timeout 60s
* 环境: http, server, location

每个cosocket连接池中连接的默认最大空闲时间。当超过这个时间时，空闲的连接将被关闭并从连接池中移除。
该指令会被cosocket对象的 `setkeepalive`方法覆盖。

###lua_socket_log_errors
* 语法: lua_socket_log_errors on|off
* 默认: lua_socket_log_errors on
* 环境: http, server, location

当TCP/UDP cosockets 出现失败时，使用该指令来切换错误日志输出。
如果已经有在其他地方处理Lua代码的错误日志，这里应该设置为off，放置将数据刷写到nginx错误日志文件中。


###lua_http10_buffering
* 语法: lua_http10_buffering on|off
* 默认: lua_http10_buffering on
* 环境: http, server, location, location-if

开启或关闭HTTP 1.0 请求的自动应答缓冲区。这个缓冲机制用于响应头包含合适长度的
 `Content-Length` 的HTTP 1.0长连接。
如果Lua代码在发送响应头之前设置了响应头的 `Content-Length` （通过`ngx.send_header` 或隐式首次调用 `ngx.say` 或 `ngx.print`），该缓冲区应该被禁用。
如果是通过流式输出非常大的响应体（通过 `ngx.flush` ），为了占有内存最小，该设置必须为off。

###lua_check_client_abort
* 语法: lua_check_client_abort on|off
* 默认: lua_check_client_abort off
* 环境: http, server, location, location-if

开启或关闭探测客户端过早终止。
在开启的情况下，ngx_lua会在下游连接上监控连接过早关闭的事件。一旦发生，它会调用用户通过 `ngx.on_abort` 注册的回调函数，如果没有注册该回调，则会停止当前请求并清理该请求产生的Lua"轻线程"。

在当前的实现中，如果请求正通过 `ngx.req.socket` 读取请求体，当客户端关闭连接时，并不会调用回调函数或停止请求清理轻线程等操作。此时 `ngx.req.socket` 的读操作第二个参数将直接返回错误信息 “client aborted” 作为返回值（第一个返回值确定是nil）。 

当TCP长连接被禁用时，该实现依靠客户端 socket 关闭的优雅实现（通过发送一个FIN包或类似的东西）。

###lua_max_pending_timers
* 语法: lua_max_pending_timers <count>
* 默认: lua_max_pending_timers 1024
* 环境: http

设置允许使用的`pending timers`最大数量。`pending timers` 指的是还没有过期的 `timers` 。
当超过这个限制， `ngx.timer.at` 调用将立即返回 nil 和 错误信息 “too many pending timers”。
[ngx.timer.at](https://github.com/iresty/nginx-lua-module-zh-wiki/blob/master/README.md#ngxtimerat)

###lua_max_running_timers
* 语法: lua_max_running_timers <count>
* 默认: lua_max_running_timers 256
* 环境: http

控制允许的`running timers`最大数量。
`running timers` 指的是那些正在执行用户回调函数的 timers 。

当超过这个限制，Nginx 将停止执行新近过期的 `timers` 回调，并记录一个错误日志 “N lua_max_running_timers are not enough”，这里的 "N" 是这个指令的当前值。



