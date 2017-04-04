# Nginx DNS.md
微服务架构的优点之一就是你能很快速容易地对服务实例进行伸缩。当有多个服务实例时，你需要一个负载均衡以及当可用服务集合发生改变时你能够及时通知它的方式。这就是“服务发现”。Nginx Plus提供两种用于发现服务集成系统的选项：on‑the‑fly reconfiguration API 和 Domain Name System (DNS) re‑resolution。稍后会着重说这部分。

当通过添加或移除虚拟机或容器对服务实例（博客的后端）进行伸缩时，负载均衡的配置文件必然要修改来适应后端集群。对于不同的应用，每天、每小时甚至每分钟都可能要进行多次服务伸缩。应该使得这些高频率的配置改动能够自动执行，其中一种实现方式就是通过DNS来做到服务发现。

在运行应用时，很多平台支持通过DNS来做到服务发现。将在文末提供在大多数平台中集成Nginx Plus及使用DNS的服务发现工具的文章链接。

## DNS关键功能的快速回顾
在解释如何通过DNS去配置服务发现前，先快速看一下DNS协议相关及有用的功能：

### 存活时间
为了避免DNS客户端使用过期的信息，DNS记录包括了TTL字段，来确定这条记录的有效时间。为了遵循DNS标准，当一条记录过了它的TTL时，客户端必须向服务端查询这个时间更新。Nginx Plus 默认以TTL为标准，但提供了更详细的记录声明周期控制，通过这些控制能配置Nginx Plus忽略TTL并且按照特定的频率去更新记录。

### 使用TCP协议的DNS
默认地，DNS客户端和服务端通过UDP协议进行通讯，但如果一个域名解析出一大串后端IP地址，完整的响应，可能不太符合一个限制在512字节内的UDP数据包。使用TCP协议来代替UDP协议能够解决这个问题：当一个完整的记录集合不能放进一个数据报时，服务器会在响应中设置一个阶段标志位，来告诉客户端切换到TCP协议来获取所有的记录。在Nginx1.9.11及之后的版本和Nginx Plus R9及之后的版本中支持DNS使用TCP协议。更多细节：Load Balancing DNS Traffic with NGINX and NGINX Plus 。

### SRV 记录
DNS将主机名解析成IP地址，但端口号呢？在一些情况下，你不能依赖众所周知的端口号的环境（例如负载均衡的Docker容器）中，因为端口号是动态注册的。DNS有一种特殊的记录——SRV 记录，其中包括了端口号和一些其他参数。在R9和之后的版本中，Nginx Plus支持SRV记录。

## 在Nginx和Nginx Plus中使用DNS的服务发现的方法
限制将展示五种在Nginx和Nginx Plus中使用DNS来实现服务发现的方式，前面三种能在Nginx和Nginx Plus使用，后面两种只能在Nginx Plus中使用。

在这份服务发现方法的调查中，我们假定我们有一个能够解析空间example.com的域名服务器，其IP地址是10.0.0.2。有三个后端服务器共同响应backends.example.com这个域名，如下面的nslookup工具输出展示的那样。在我们讨论的第一个方法中，Nginx和Nginx Plus从DNS请求一个标准的A记录；而在最后一个方法中，Nginx Plus请一个SRV记录。

```sh
$ nslookup backends.example.com 10.0.0.2
Server:		10.0.0.2
Address:	10.0.0.2#53

Name:	backends.example.com
Address: 10.0.0.11
Name:	backends.example.com
Address: 10.0.0.10
Name:	backends.example.com
Address: 10.0.0.12
```


### 使用Nginx和DNS来用于服务发现
开始展示三种使用开源软件Nginx去使用DNS的方式（也可以使用Nginx Plus)。

#### 在proxy_pass命令中使用域名
指定一个域名作为proxy_pass的参数是最简单的定义上流服务集群方式。

```nginx
server {
	location / {
		proxy_pass http://backends.example.com:8080;
	}
}
```

当Nginx启动或者重新加载配置文件时，它会查询DNS服务器来解析backens.example.com。DNS服务器会返回上面讨论的三个后端列表，并且Nginx使用默认的轮询算法在这些后端列表中负载均衡请求。Nginx会从系统的配置文件/etc/resolv.conf中选择DNS服务器。
这个方式是最灵活的服务发现方式，但有以下不利之处：
* 如果域名不能被解析出来，Nginx会启动失败或重载失败；
* Nginx会忽略TTL来缓存DNS记录，直到下一次重启或重载；
* 无法指定其他的负载均衡算法，也无法配置配置被动的健康监测或者其他由server指令参数定义的功能，将在下一节讨论这个。


#### 在上流服务器集群中使用域名
为了利用Nginx提供的负载均衡选项，你必须在upstream配置块中定义上流服务器群。但不是通过使用IP地址来判断服务器，而是使用域名来作为server命令的参数。
在第一个方法中，当Nginx启动或者重载配置文件时，backends.example.com被解析成三个后端服务器。但现在我们能定义更加复杂的均衡负载算法——最少连接数，并且使用max_fails参数来开启被动的健康监测，并指定当有三个连续的请求失败时nginx将该服务器标记为宕机。

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

尽管这个方式能选择均衡负载的算法以及配置健康监测，但它仍然有一些不足因为它将重启、重载及TTL作为previous method。

#### 在变量中设置域名
这个方法是第一种方法的变体，但能够控制Nginx重新解析域名的频率。

```nginx
resolver	10.0.0.2 valid=10s;

server {
	location / {
		set $backend_server	backends.example.com;
		proxy_pass	http://$backend_servers:8080;
	}
}
```

当你在proxy_pass命令中使用一个变量来指定域名，在域名TTL过期时，Nginx会重新解析域名。必须包含resolver命令来明确指出域名服务器（Nginx不会像前面两种那样去引用/etc/resolv.conf）。通过有效的resolver指令参数，能够告诉Nginx忽略TTL以及以特定的频率去重新解析域名。上面的配置中告诉Nginx每10s重新解析域名。

这种方式能排除第一种的方式的两个不足——当域名不能被解析时Nginx无法启动或重载以及我们能够控制Nginx解析域名的频率。然而，由于它不使用upstream服务器群，所以无法制定均衡负载算法或server命令的参数（在第二个方法中能够指定）。

### 使用Nginx Plus和DNS来用于服务发现

#### 在Nginx Plus中使用A记录
使用Nginx Plus可以以任意想要的频率去重新解析DNS，并且没有上述三种法中的不足。要使用这些功能，需要：
* 使用`resolver`指令来指定域名服务器；
* 在`upstream`配置块中使用`zone`指令来分配一块共享内存空间；
* 在`upstream`配置块中添加`server`指令的`resolve`参数。

例如：

```nginx
resolver	10.0.0.2	valid=10s;

upstream backends {
	zone		backends		64k;
	server	backends.example.com:8080		resolve;
}

server {
	location / {
		proxy_pass	http://backedns;
	}
}

```

nginx默认会根据TTL在记录过期时重新解析域名。可以使用`resolver`指令的`valid`来指定重新解析域名的频率。

在上面的配置中，每过10s Nginx Plus会去查询域名服务器10.0.0.2解析backends.example.com的地址。Nginx Plus不会因为无法解析该域名而无法启动、无法重载或者运行失败。这时Nginx Plus向客户端返回标准的502错误页。

#### 在Nginx Plus中使用SRV记录
Nginx Plus在R9及之后的版本中支持DNS SRV记录。这使得Nginx Plus不只能从域名服务器中解析IP地址，还能解析到端口、权重和优先级。这在动态分配端口的微服务环境是很难做到的。

SRV记录由服务名字、通信协议、以及域名来定义。在查询域名服务器的时候，必须同时提供这三者。上文中的10.0.0.2域名服务器有三条由http（服务名称）、TCP协议及域名backends.example.com组成的SRV记录。使用nslookup工具的输出：

```sh
$ nslookup -query=SRV _http._tcp.backends.example.com 10.0.0.2
Server:		10.0.0.2
Address:	10.0.0.2#53

_http._tcp.backends.example.com	service = 0 2 8090 backend-0.example.com.
_http._tcp.backends.example.com	service = 0 1 8091 backend-1.example.com.
_http._tcp.backends.example.com	service = 10 1 8092 backend-2.example.com.
```

对每一条SRV记录查询其主机名时，能获取到IP地址，端口号及权重优先级等：
```sh
$ nslookup backend-0.example.com 10.0.0.2
. . .
Name:	backend-0.example.com
Address: 10.0.0.10

$ nslookup backend-1.example.com 10.0.0.2
. . .
Name:	backend-1.example.com
Address: 10.0.0.11
$ nslookup backend-2.example.com 10.0.0.2
. . .
Name:	backend-2.example.com
Address: 10.0.0.12
```

取其中一条说明：
```sh
_http._tcp.backends.example.com	service = 0 2 8090 backend-0.example.com.
```
* _http._tcp ——SRV 记录的名字和协议。我们将这个值（即服务名）作为`upstream`配置块中指定`server`指令的参数。
* 0 ——优先级，数值越低表示优先级越高。Nginx Plus将优先级最高的服务器作为主要服务器，其他的服务器作为备用服务器。这条记录相比其他记录的优先级最高，因此Nginx Plus会将其对应的后端服务器作为主要服务器。
* 2 ——权重，Nginx Plus将后端的权重值作为上游服务器群的权重。
* 8090 ——端口，Nginx Plus将它设置为上游服务器群的端口。
* backend-0.example.com ——后端服务器的主机名。Nginx Plus解析这个主机名并将相对应的后端机器添加到上游服务器群中。如果这个主机名解析出多条记录，则会添加多个服务器。

由上面SRV记录我们可以主要配置：

```nginx
resolver 10.0.0.2 valid=10s;

upstream backends {
	zone		64k
	server 	backends.example.com	service=_http._tcp resolve;
}

server {
	location / {
		proxy_pass http://backends;
	}
}


```

使用`server`指令的`service`参数，能够指定我们想解析的SRV记录的服务名和协议。在这个例子中使用_http和_tcp。除了`service`参数以及不指定端口号，这个配置看起来和前面的方法一样。

基于上面nslookup指令返回的结果，Nginx Plus将如下所示配置后端的服务器：
* 10.0.0.10，作为主要服务器，使用8090端口，权重为2；
* 10.0.0.11，作为主要服务器，使用8091端口，权重为1；
* 10.0.0.12，作为备份服务器，使用8092端口，权重为1；
当有请求进来时，10.0.0.10将被分发到2/3的请求，10.0.0.11将被分发到1/3。除非另外两台服务器都宕机了，否则10.0.0.12不会被分发到任何请求。

## 注意：
* DNS服务器必须高可用或者有备份机器。如果DNS服务器不可用，Nginx Plus将会忽略TTL停止更新后端配置，除非重启或者重载。
* 可以通过resolver指令指定多个域名服务器，这样其中一台宕机时Nginx Plus会尝试请求其他服务器。





