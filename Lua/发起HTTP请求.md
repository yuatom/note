# 发起HTTP请求

##通过ngx.location.capture + proxy_pass模块
`ngx.location.capture`，通过模拟HTTP接口的形式，发起非阻塞的`内部请求`访问目标location，没有额外的HTTP/TCP流程，没有IPC进程间通信调用，所有工作都在内部的C语言级别完成。
要发起外部请求时，需要先向server内的一个包含 `proxy_pass` 的location发起内部请求，然后在这个location中通过 `proxy_pass` 发起外部请求。

```nginx
http {
    upstream md_server {
        server      127.0.0.1:81;
        keepalive   20;
    }
    
    server {
        listen  80;
        
        location /test {
            content_by_lua_block {
                ngx.req.read_body()
                local arg, err = ngx.req.get_uri_args()
                
                local res = ngx.location.capture('/spe_md5',
                    {
                        method = ngx.HTTP_POST,
                        body = args.data
                    }
                
                if 200 ~= res.status then
                    ngx.exit(res.status)
                end
                
                if args.key = res.body then
                    ngx.say("valid request")
                else
                    ngx.say("invalid request")
                end
            }
        }
    }
    
    location /spe_md5 {
        proxy_pass http://md5_server;
    }
    
    server{
        listen  81;
        
        location /spe_md5 {
            content_by_lua_block {
                ngx.req.read_body()
                local data = ngx.req.get_body_data()
                ngx.print(ngx.md5(data .. "*&^%$#$^&kjtrKUYG")))
            }
        }
    }
}

```

这种方式比较曲折，并且容易踩坑，比如upstream中长连接的细节处理。

##利用cosocket
利用`resty.http`模块，request_uri 函数完成了连接池、HTTP 请求等一系列动作。

```nginx
http {
    server {
        listen  80;
    
        location /test {
            content_by_lua_block {
                ngx.req.read_body()
                local args, err = ngx.req.get_uri_args()
                
                local http = require "resty.http"
                local httpc = http.new()
                local res, err = httpc:request_uri(
                    "http://127.0.0.1:81/spe_md5",
                    {
                        method = "POST",
                        body = args.data,        
                    }
                )
                if 200 ~= res.status then
                    ngx.exit(res.status)
                end
                
                if args.key = res.body then
                    ngx.say("valid request")
                else
                    ngx.say("invalid request")
                end

            }
        }
    }
    server {
        listen    81;

        location /spe_md5 {
            content_by_lua_block {
                ngx.req.read_body()
                local data = ngx.req.get_body_data()
                ngx.print(ngx.md5(data .. "*&^%$#$^&kjtrKUYG"))
            }
        }
    }
}
```


