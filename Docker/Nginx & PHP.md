# Nginx & PHP

```sh
docker run --name nginx-ct -d -p 80:80 -v /local/dir:/usr/share/nginx/html arkulo/nginx:v1
```
-p 80:80 将docker虚拟机的80端口映射到nginx容器的80端口
-v /local/dir:/usr/share/nginx/html 将本地主机的/local/dir映射到nginx容器的/usr/share/nginx/html上

```sh
docker run --name php-fpm-ct -d -p 9000:9000 -v /local/dir:/usr/share/nginx/html arkulo/php-fpm:v1
```

Nginx容器中配置:/etc/nginx/conf.d/default.conf
192.168.99.100是docker虚拟机的ip
\$document_root的值为这个小节中root定义的值（/usr/share/nginx/html），必须挂载到php容器中的目录对应。
如果php启动语句的配置为**/local/dir:/var/www/html**，则root必须定义为**/var/www/html**或**\$document_root\$fastcgi_script_name**改为**/var/www/html/$fastcgi_script_name**

```sh
server {
    listen       80;
    server_name  localhost;

    #charset koi8-r;
    #access_log  /var/log/nginx/log/host.access.log  main;

    location / {
        root   /usr/share/nginx/html;
        index  index.html index.htm;
    }

    #error_page  404              /404.html;

    # redirect server error pages to the static page /50x.html
    #
    error_page   500 502 503 504  /50x.html;
    location = /50x.html {
        root   /usr/share/nginx/html;
    }

    # proxy the PHP scripts to Apache listening on 127.0.0.1:80
    #
    #location ~ \.php$ {
    #    proxy_pass   http://127.0.0.1;
    #}

    # pass the PHP scripts to FastCGI server listening on 127.0.0.1:9000
    #
    location ~ \.php$ {
        root           /usr/share/nginx/html;
        fastcgi_pass   192.168.99.100:9000;
    	fastcgi_index  index.php;
        fastcgi_param  SCRIPT_FILENAME  $document_root$fastcgi_script_name;
    	include        fastcgi_params;
    }

    # deny access to .htaccess files, if Apache's document root
    # concurs with nginx's one
    #
    #location ~ /\.ht {
    #    deny  all;
    #}
}
```





