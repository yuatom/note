#rewrite

`rewrite_log`

* 语法：rewrite_log on|off;
* 默认值：rewrite_log off;
* 作用域：http,server,location,if
以notice将rewrite日志记录到error日志文件中，`error_log`日志需要配置`notice`级别才能显示。

##rewrite顺序

* 执行server块中的`rewrite`匹配；
* 执行location匹配；
* 执行location中的`rewrite`匹配；
* 如果在以上的匹配过程中URI被重写，则由`server`处开始重新匹配，直到找到要执行的文件；
* 如果循环匹配的步骤超过10次，则返回500错误。

##flag标志

* `last`：完成当次循环的匹配，将rewrite后的结果从`server`处开始新一次匹配，一般写在`server`和`if`中；
* `break`：停止当前块后面的匹配，不再进行匹配而执行当前块后面的操作，一般写在`location`中；
* `redirect`：返回302重定向，地址栏会显示跳转后的地址；
* `permanent`：返回301永久重定向，地址栏会显示跳转后的地址；


##if指令
`if(condition){...}`判断变量来决定是否执行某些rewrite。

###condition内容

* `=`/`!=`：	比较变量或字符串是否等于；
* `~`/`~*`/`!~`：正则匹配，一次为区分大小写的匹配，不区分大小写的匹配，区分大小写的不匹配；
* `-f`/`!-f`：是否存在该文件；
* `-d`/`!-d`：是否存在该目录；
* `-e`/`!-e`：是否存在目录或文件；
* `-x`/`!-x`：文件是否可执行。

###可用于if条件中的全局变量

* `$args` ： 这个变量等于请求行中的参数，同$query_string
* `$content_length` ： 请求头中的Content-length字段。
* `$content_type` ： 请求头中的Content-Type字段。
* `$document_root` ： 当前请求在root指令中指定的值。
* `$host` ： 请求主机头字段，否则为服务器名称。
* `$http_user_agent` ： 客户端agent信息
* `$http_cookie` ： 客户端cookie信息
* `$limit_rate` ： 这个变量可以限制连接速率。
* `$request_method` ： 客户端请求的动作，通常为GET或POST。
* `$remote_addr` ： 客户端的IP地址。
* `$remote_port` ： 客户端的端口。
* `$remote_user` ： 已经经过Auth Basic Module验证的用户名。
* `$request_filename` ： 当前请求的文件路径，由root或alias指令与URI请求生成。
* `$scheme` ： HTTP方法（如http，https）。
* `$server_protocol` ： 请求使用的协议，通常是HTTP/1.0或HTTP/1.1。
* `$server_addr` ： 服务器地址，在完成一次系统调用后可以确定这个值。
* `$server_name` ： 服务器名称。
* `$server_port` ： 请求到达服务器的端口号。
* `$request_uri` ： 包含请求参数的原始URI，不包含主机名，如：”/foo/bar.php?arg=baz”。
* `$uri` ： 不带请求参数的当前URI，$uri不包含主机名，如”/foo/bar.html”。
* `$document_uri` ： 与$uri相同。

uri中的变量例子：
http://localhost:88/test1/test2/test.php
`$host`：localhost
`$server_port`：88
`$request_uri`：http://localhost:88/test1/test2/test.php
`$document_uri`：/test1/test2/test.php
`$document_root`：/var/www/html
`$request_filename`：/var/www/html/test1/test2/test.php


condition匹配例子

```nginx
if ($http_user_agent ~ MSIE) {
    rewrite ^(.*)$ /msie/$1 break;
} //如果UA包含"MSIE"，rewrite请求到/msid/目录下
if ($http_cookie ~* "id=([^;]+)(?:;|$)") {
    set $id $1;
 } //如果cookie匹配正则，设置变量$id等于正则引用部分
if ($request_method = POST) {
    return 405;
} //如果提交方法为POST，则返回状态405（Method not allowed）。return不能返回301,302
if ($slow) {
    limit_rate 10k;
} //限速，$slow可以通过 set 指令设置
if (!-f $request_filename){
    break;
    proxy_pass  http://127.0.0.1;
} //如果请求的文件名不存在，则反向代理到localhost 。这里的break也是停止rewrite检查
if ($args ~ post=140){
    rewrite ^ http://example.com/ permanent;
} //如果query string中包含"post=140"，永久重定向到example.com
location ~* \.(gif|jpg|png|swf|flv)$ {
    valid_referers none blocked www.jefflei.com www.leizhenfang.com;
    if ($invalid_referer) {
        return 404;
    } //防盗链
}

```