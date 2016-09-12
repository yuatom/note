# netstat&nslookup&host

## netstat
查看网络连接相关的统计数据

netstat -tulnp  | grep portnumber
查看某个端口的占用情况

###常用参数

* -a：显示所有socket包括正在监听的；
* -c：每个一段时间就重新显示一遍直到用户中断；
* -t：显示TCP协议的连接情况；
* -u：显示UDP协议的连接情况；
* -n：以网络IP地址代替名称显示；
* -p：显示PID；
* -l：列出正在监听的服务；

```shell
# 无参数
[root@6224a0586831 /]# netstat
Active Internet connections (w/o servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State
Active UNIX domain sockets (w/o servers)
Proto RefCnt Flags       Type       State         I-Node   Path
unix  3      [ ]         STREAM     CONNECTED     18081
unix  3      [ ]         STREAM     CONNECTED     18082

# 列出所有端口
[root@6224a0586831 /]# netstat -a
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State
tcp        0      0 0.0.0.0:http            0.0.0.0:*               LISTEN
Active UNIX domain sockets (servers and established)
Proto RefCnt Flags       Type       State         I-Node   Path
unix  3      [ ]         STREAM     CONNECTED     18081
unix  3      [ ]         STREAM     CONNECTED     18082

# 显示监听端口的进程
[root@6224a0586831 /]# netstat -ap
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
tcp        0      0 0.0.0.0:http            0.0.0.0:*               LISTEN      37/nginx: master pr
Active UNIX domain sockets (servers and established)
Proto RefCnt Flags       Type       State         I-Node   PID/Program name     Path
unix  3      [ ]         STREAM     CONNECTED     18081    37/nginx: master pr
unix  3      [ ]         STREAM     CONNECTED     18082    37/nginx: master pr

# 显示监听端口的进程，以IP和端口的形式来显示，而不是以服务名
[root@6224a0586831 /]# netstat -apn
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
tcp        0      0 0.0.0.0:80              0.0.0.0:*               LISTEN      37/nginx: master pr
Active UNIX domain sockets (servers and established)
Proto RefCnt Flags       Type       State         I-Node   PID/Program name     Path
unix  3      [ ]         STREAM     CONNECTED     18081    37/nginx: master pr
unix  3      [ ]         STREAM     CONNECTED     18082    37/nginx: master pr

# 查找端口占用
[root@6224a0586831 /]# netstat -apn | grep 80
tcp        0      0 0.0.0.0:80              0.0.0.0:*               LISTEN      37/nginx: master pr
unix  3      [ ]         STREAM     CONNECTED     18081    37/nginx: master pr
unix  3      [ ]         STREAM     CONNECTED     18082    37/nginx: master pr

# 查找程序监听的端口
[root@6224a0586831 /]# netstat -apn | grep nginx
tcp        0      0 0.0.0.0:80              0.0.0.0:*               LISTEN      37/nginx: master pr
unix  3      [ ]         STREAM     CONNECTED     18081    37/nginx: master pr
unix  3      [ ]         STREAM     CONNECTED     18082    37/nginx: master pr
```

###显示的信息解释

* Active Internet connections 有源TCP连接，其中"Recv-Q"和"Send-Q"指的是接收队列和发送队列
* Active UNIX domain sockets，称为有源Unix域套接口(和网络套接字一样，但是只能用于本机通信，性能可以提高一倍)


##nslookup
查询一台机器的IP地址和其对应的域名

```
[root@6224a0586831 /]# nslookup baidu.com
Server:		180.76.76.76
Address:       	180.76.76.76#53

Non-authoritative answer:
Name:  	baidu.com
Address: 220.181.57.217
Name:  	baidu.com
Address: 180.149.132.47
Name:  	baidu.com
Address: 111.13.101.208
Name:  	baidu.com
Address: 123.125.114.144
```


##host
查询一个域名或IP地址的详细信息

```shell
[root@6224a0586831 /]# host baidu.com
baidu.com has address 220.181.57.217
baidu.com has address 123.125.114.144
baidu.com has address 180.149.132.47
baidu.com has address 111.13.101.208
baidu.com mail is handled by 20 mx50.baidu.com.
baidu.com mail is handled by 20 mx1.baidu.com.
baidu.com mail is handled by 20 jpmx.baidu.com.
baidu.com mail is handled by 10 mx.n.shifen.com.

# 显示域名、IP和主机名相关信息
[root@6224a0586831 /]# host -a baidu.com
Trying "baidu.com"
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 42165
;; flags: qr rd ra; QUERY: 1, ANSWER: 15, AUTHORITY: 0, ADDITIONAL: 3

;; QUESTION SECTION:
;baidu.com.    			IN     	ANY

;; ANSWER SECTION:
baidu.com.     		3850   	IN     	TXT    	"google-site-verification=GHb98-6msqyx_qqjGl5eRatD3QTHyVB6-xQ3gJB5UwM"
baidu.com.     		3850   	IN     	TXT    	"v=spf1 include:spf1.baidu.com include:spf2.baidu.com include:spf3.baidu.com a mx ptr -all"
baidu.com.     		6571   	IN     	MX     	20 mx50.baidu.com.
baidu.com.     		6571   	IN     	MX     	20 jpmx.baidu.com.
baidu.com.     		6571   	IN     	MX     	10 mx.n.shifen.com.
baidu.com.     		6571   	IN     	MX     	20 mx1.baidu.com.
baidu.com.     		417    	IN     	A      	111.13.101.208
baidu.com.     		417    	IN     	A      	220.181.57.217
baidu.com.     		417    	IN     	A      	123.125.114.144
baidu.com.     		417    	IN     	A      	180.149.132.47
baidu.com.     		56868  	IN     	NS     	ns2.baidu.com.
baidu.com.     		56868  	IN     	NS     	ns4.baidu.com.
baidu.com.     		56868  	IN     	NS     	ns7.baidu.com.
baidu.com.     		56868  	IN     	NS     	dns.baidu.com.
baidu.com.     		56868  	IN     	NS     	ns3.baidu.com.

;; ADDITIONAL SECTION:
mx.n.shifen.com.       	22     	IN     	A      	220.181.3.77
mx1.baidu.com. 		22     	IN     	A      	61.135.163.61
jpmx.baidu.com.		5457   	IN     	A      	61.208.132.13

Received 502 bytes from 192.168.65.3#53 in 45 ms
```














































