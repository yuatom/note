#Real-ip&X-Forwarded-For
* $remote_addr：Nginx中该变量为发出请求的客户端ip，当请求由代理发出时，这个变量为代理服务器的ip；
* $http_x_forwarded_for：代理的IP链，如果没有设置该请求头，Nginx中该变量默认为空，可通过`proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for`命名将请求头中的`X-Forwarded-For`和`$remote_addr`用逗号合并起来，如果请求头中没有`X-Forwarded-For`，该命令会将其值设置为`$remote_addr`；


## Tips
* 为了能够获取到用户的真实ip，一般在第一层代理服务器中`proxy_set_header X-Real-IP $remote_addr`将客户端的ip记录到`X-Real-IP`请求中；
* 为了防止客户端伪造 `X-Forwarded-For`请求头，一般在第一层代理服务器中不使用`proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for`来设置请求头；