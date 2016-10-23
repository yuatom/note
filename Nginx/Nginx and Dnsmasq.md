#Nginx and Dnsmasq

##NginxDNS解析
Nginx中的DNS解析有自己的机制，有以下三种方式：

###proxy_pass 
会去/etc/resolv.conf中配置的域名服务器解析域名ip。
缺点：
* 如果域名解析不了，在重启或重载时会失败；
* 无法配置上流负载均衡算法；
* 域名ip一旦解析了只有在nginx重启/重载时才会更新；

```nginx
server {
	location / {
		proxy_pass http://backends.example.com:8080;
	}
}
```

###proxy_pass和upstream
特点：
* /etc/resolv.conf中配置的域名服务器解析域名ip；
* 可以配置负载均衡算法。

缺点：
* 如果域名解析不了，在重启或重载时会失败；
* 域名ip一旦解析了只有在nginx重启/重载时才会更新；

```nginx
upstream backends {
	least_conn;
	server backends.example.com:8080 max_fails=3;
}

server {
	location / {
		proxy_pass http://backends;
	}
}
```

###proxy_pass中使用域名变量
需要使用resolver指定域名解析服务器。

特点：
* 可以指定域名解析更新的频率；
* 不会因为域名无法解析而无法启动/重载。

```nginx
resolver	10.0.0.2 valid=10s;

server {
	location / {
		set $backend_server	backends.example.com;
		proxy_pass	http://$backend_servers:8080;
	}
}
```

##ngx_lua中访问外部http请求
ngx_lua中调用外部http请求使用的是Nginx的DNS解析。
需要配置`resolver`指令指定DNS服务器。


##使用本地的hosts文件
如果想要使用本地的hosts文件，需要：

* 本地搭建dns服务器，使用dnsmasq搭建；
* dnsmasq的配置文件/etc/dnsmasq.conf中`listen-address`配置添加127.0.0.1；