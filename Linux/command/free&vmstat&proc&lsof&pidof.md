# free&vmstat&proc&lsof&pidof
查看内存情况

```sh
free [-b|k|m|g|h] [-t] [-s N -c N]
```

## free
查看内存情况

```sh
free [-b|k|m|g|h] [-t] [-s N -c N]
```

###选项

* -b :直接输入 free 时,显示的单位是 KBytes，可以使用 b(Bytes), m(MBytes)，k(KBytes), 及 g(GBytes)来显示单位喔!也可以直接让系统自己指定单位 (-h)；
* -t :在输出的最终结果,显示实体内存与 swap 的总量；
* -s :多久刷新一次；
* -c :总共显示多少次，与-s配合使用；
 
```sh
[root@6224a0586831 /]# free
              total        used        free      shared  buff/cache   available
Mem:        2048660       54016     1687660      183756      306984     1686820
Swap:        987960           0      987960
[root@6224a0586831 /]# free -m
              total        used        free      shared  buff/cache   available
Mem:           2000          52        1648         179         299        1647
Swap:           964           0         964
[root@6224a0586831 /]# free -s 2
              total        used        free      shared  buff/cache   available
Mem:        2048660       54104     1687520      183756      307036     1686688
Swap:        987960           0      987960

              total        used        free      shared  buff/cache   available
Mem:        2048660       54064     1687536      183756      307060     1686704
Swap:        987960           0      987960

              total        used        free      shared  buff/cache   available
Mem:        2048660       54084     1687536      183756      307040     1686704
Swap:        987960           0      987960
```

###显示的数据

* Mem：物理内存；
* Swap：虚拟内存；
* total：内存总量；
* used：已被使用的内存大小；
* free：可用的内存大小；
* shared：多个进程共享的内存大小；
* buff/cache：磁盘缓存的大小；

buff/cache对于OS来说，是已经被使用的；对于应用程序来说，仍然可用，在内存不足时会释放这些内存；
从应用程序的角度来说，可用内存=free + buffers + cached.

##vmstat
虚拟内存统计，可用来查看虚拟内存、进程、CPU活动。

```sh
vmstat [-a] [延迟 [总计侦测次数]] # CPU/内存等信息
vmstat [-fs] # 内存相关
vmstat [-S 单位] # 设置显示数据的单位
vmstat [-d] #与磁盘有关
vmstat [-p 分区] #与磁盘有关
```

###参数：
-a ：使用 inactive/active（ 活跃与否） 取代 buffer/cache 的内存输出信息；
-f ：开机到目前为止，系统复制 （ fork） 的程序数；
-s ：将一些事件 （ 开机至目前为止） 导致的内存变化情况列表说明；
-S ：后面可以接单位，让显示的数据有单位。例如 K/M 取代 Bytes 的容量；
-d ：列出磁盘的读写总量统计表
-p ：后面列出分区，可显示该分区的读写总量统计表


```sh
# vmstat 1 3，查看资源信息，每秒刷新1次，总共刷新3次，后面的数字没给出的话，会无限刷新下去
[root@6224a0586831 /]# vmstat 1 3
procs -----------memory---------- ---swap-- -----io---- -system-- ------cpu-----
 r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st
 3  0      0 1687892  32284 274592    0    0    26     3   28   47  0  0 100  0  0
 0  0      0 1687844  32284 274652    0    0     0     0  107  201  0  0 100  0  0
 0  0      0 1687844  32284 274652    0    0     0     0  138  265  0  0 100  0  0

# vmstat -d，查看磁盘读写情况，可以使用时间参数来控制刷新频率和次数
[root@6224a0586831 /]# vmstat -d
disk- ------------reads------------ ------------writes----------- -----IO------
       total merged sectors      ms  total merged sectors      ms    cur    sec
loop0      0      0       0       0      0      0       0       0      0      0
loop1      0      0       0       0      0      0       0       0      0      0
loop2      0      0       0       0      0      0       0       0      0      0
loop3      0      0       0       0      0      0       0       0      0      0
loop4      0      0       0       0      0      0       0       0      0      0
loop5      0      0       0       0      0      0       0       0      0      0
loop6      0      0       0       0      0      0       0       0      0      0
loop7      0      0       0       0      0      0       0       0      0      0
vda     8743      0  173164   21130    523   1554   16864    8490      0      2
````

###字段含义

* procs：该字段下面有两列，r表示等待运行中的程序数量；b表示不可唤醒的程序数量，两个项目越多，代表系统越繁忙；
* memory：swpd表示已swapd的虚拟内存大小；free可用的物理内存发小；buff用于缓存的内存大小；cache用于高速缓存的内存大小；
* swap：si表示从磁盘将程序取出的大小；so表示由与内存不足而将程序写入磁盘的大小；si/so的值越大，系统性能越差；
* io：bi表示读磁盘的量；bo表示写磁盘的量；值越高，表示磁盘I/O越忙；
* system：in每秒被中断的程序次数；cs每秒进行的事件切换次数；数值越高，表示设备I/O越大；
* CPU：us表示非核心层的CPU使用状态；sy表示核心层的CPU使用状态；id表示闲置的状态；wa表示等待I/O所耗费的CPU状态；st表示被虚拟机锁盗用的CPU使用状态；







/proc/*    保存内存中的程序数据
各个程序的PID都是以目录的形态存在于/proc当中。
举例来说，开机所执行的第一支程序 systemd 他的 PID 是 1 ， 这个 PID 的所有相关信息都写入在/proc/1/* 当中。



lsof [-aUu] [+d]
选项与参数：
-a ：多项数据需要“同时成立”才显示出结果时！
-U ：仅列出 Unix like 系统的 socket 文件类型；
-u ：后面接 username，列出该使用者相关程序所打开的文件；
+d ：后面接目录，亦即找出某个目录下面已经被打开的文件

pidof [-sx] program_name
选项与参数：
-s ：仅列出一个 PID 而不列出所有的 PID
-x ：同时列出该 program name 可能的 PPID 那个程序的 PID








































