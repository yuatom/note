# Docker command.md
##run，创建容器
`-d` 在后台运行，创建守护式容器，加入该选项后启动容器会返回容器完整id
`--name <containner name>` 容器名称
`-p` 指定开放端口
`-v` 挂载目录
`-i` 标准输入数据流，保持输入流开放
`-t` 为要创建的的容器分配一个伪tty终端
`-h` docker主机名0
`--rm` 在容器停止后清除容器中产生的数据，包括挂载的目录
`--link <containner name>:<alias>`，建立Docker内部连接，containner name所在容器作为子容器，子容器在启动（docker run）时无须对外部主机暴露端口，父容器（当前run的容器）可以直接访问子容器开放的端口（Dockerfile中EXPOSE的端口）。当Docker的守护进程启动时加上`--icc=false`时，容器之间的连接功能将被关闭。
`--restart` 重启选项
>* no  不自动重启
>* always   一直重启
>* unless-stopped 除了停止的情况下
>* on-failure[:max-retries] 当容器异常退出（返回非0的退出状态

`--privileged`，启动Docker特权模式，以宿主机具有的所有能力来运行容器，包括一些内核特性和设备访问；
`--volumes-from` 把指定容器的所有卷都加入新创建的容器器，使得新容器能够访问指定容器中的数据

###卷
卷是一个或多个容器中的指定目录，保存在Docker主机中的`/var/lib/docker/volumes`目录中。具有以下特点：
>* 卷可以在容器间共享和重用；
>* 共享卷时不一定要运行相应的容器；
>* 对卷的修改会直接在卷上反映出来；
>* 更新镜像时不会包含对卷的修改；
>* 卷会一直存在，直到没有容器使用该卷，当最后一个使用卷的容器被删除，卷就会被删除。
更新卷中内容时，如果指定镜像没有运行，需要启动指定镜像，docker中的卷数据才能得到更新。

####备份卷
以下命令，在容器运行结束后，将在当前目录下，生成一个目标容器上要备份的路径下的数据压缩文件。
先将当前目录挂载到新容器的`/backup`，再将要保存的目录压缩保存到`/backup`上。

```sh
# 使用--rm选项，在容器停止时自动删除容器
docker run --rm --volumes-from <contaninner name> \
-v $PWD:/backup ubuntu \
tar cvf /backup/<backup name>.tar <target path>
```

###例子
```sh
# 指定卷，从james_blog容器中
docker run -d -P --volumes-from james_blog jamtur01/apache
d58eebeab912af3b23bcf7e551603b5628e8915cfbe1d059bc0dafc56d98bd3c
```

##start，重新启动已经停止的容器

```sh
docker start <id>/<name>
```
docker restart命令也可以用来重新启动一个容器。

##attach，附着到容器上
通过start/restart启动一个容器时，会沿用run命令的选项，有时会在容器内部运行一个可交互回话shell。此外可以使用attach命名进入到容器的会话上（有时在运行该命令需要再按一次回车）。

```sh
# 容器中有运行/bin/bash，attach后会回到/bin/bash上
docker attach f76eaf5dedb0
root@f76eaf5dedb0:/#
root@f76eaf5dedb0:/#

# 启动没有运行/bin/bash的容器，由于没加任何选项，启动后不会有任何输出
docker run nginx

# 容器内部没有运行/bin/bash，因此attach后也不会进入shell控制台
docker attach 86726cd8baed
```

##logs，获取容器的日志
-f，监控Docker的日志，类似tail -f

##top，查看容器中进程

```sh
docker top f56cfb948445
UID                 PID                 PPID                C                   STIME               TTY                 TIME                CMD
root                11902               1028                0                   05:46               ?                   00:00:00            nginx: master process nginx -g daemon off;
104                 11907               11902               0                   05:46               ?                   00:00:00            nginx: worker process
```

##exec，在容器内部执行命令

```sh
docker exec <option> <docker> <command>
```
进入容器并运行命令。

```sh
# 在后台创建一个配置文件，使用-d选项，在shell中不会输出返回
docker exec -d f76eaf5dedb0 touch /etc/new_config_file

# 进入ubuntu容器并运行/bin/bash，使用-i及-t，创建TTY并输出
docker exec -it f76eaf5dedb0 /bin/bash
# 已经进入容器的/bin/bash
root@f76eaf5dedb0:/#
```
可在容器的`/bin/bash`中输入`exit`退出当前容器。一旦退出当前容器，`/bin/bash`命令也就结束，容器也就停止。

##stop，停止守护式容器

```sh
docker stop <id>/<name>
```

##inspect，查看容器更多的信息

```sh
docker inspect <id>/<name>
```
除了该命令，该可以浏览`/var/lib/docker`目录来了解容器信息。

```sh
docker inspect f76eaf5dedb0
[
{
    "Id": "f76eaf5dedb0d6565dcfd294e9eeb174498d765bb0d9f40d1b70e0809566835a",
    "Created": "2016-06-04T01:07:33.710237363Z",
    "Path": "/bin/bash",
    "Args": [],
    "State": {
        "Status": "running",
        "Running": true,
        "Paused": false,
        "Restarting": false,
        "OOMKilled": false,
        "Dead": false,
        "Pid": 13514,
        "ExitCode": 0,
        "Error": "",
        "StartedAt": "2016-06-04T11:52:22.568021889Z",
        "FinishedAt": "2016-06-04T05:35:27.333685578Z"
    },
    "Image": "af88597ec24be1eb2028ec63fadae21be693428196a917fa24632ec41a791754",
    "ResolvConfPath": "/mnt/sda1/var/lib/docker/containers/f76eaf5dedb0d6565dcfd294e9eeb174498d765bb0d9f40d1b70e0809566835a/resolv.conf",
    "HostnamePath": "/mnt/sda1/var/lib/docker/containers/f76eaf5dedb0d6565dcfd294e9eeb174498d765bb0d9f40d1b70e0809566835a/hostname",
    "HostsPath": "/mnt/sda1/var/lib/docker/containers/f76eaf5dedb0d6565dcfd294e9eeb174498d765bb0d9f40d1b70e0809566835a/hosts",
    "LogPath": "/mnt/sda1/var/lib/docker/containers/f76eaf5dedb0d6565dcfd294e9eeb174498d765bb0d9f40d1b70e0809566835a/f76eaf5dedb0d6565dcfd294e9eeb174498d765bb0d9f40d1b70e0809566835a-json.log",
    "Name": "/elegant_borg",
    "RestartCount": 0,
    "Driver": "aufs",
    "ExecDriver": "native-0.2",
    "MountLabel": "",
    "ProcessLabel": "",
    "AppArmorProfile": "",
    "ExecIDs": null,
    "HostConfig": {
        "Binds": null,
        "ContainerIDFile": "",
        "LxcConf": [],
        "Memory": 0,
        "MemoryReservation": 0,
        "MemorySwap": 0,
        "KernelMemory": 0,
        "CpuShares": 0,
        "CpuPeriod": 0,
        "CpusetCpus": "",
        "CpusetMems": "",
        "CpuQuota": 0,
        "BlkioWeight": 0,
        "OomKillDisable": false,
        "MemorySwappiness": -1,
        "Privileged": false,
        "PortBindings": {},
        "Links": null,
        "PublishAllPorts": false,
        "Dns": [],
        "DnsOptions": [],
        "DnsSearch": [],
        "ExtraHosts": null,
        "VolumesFrom": null,
        "Devices": [],
        "NetworkMode": "default",
        "IpcMode": "",
        "PidMode": "",
        "UTSMode": "",
        "CapAdd": null,
        "CapDrop": null,
        "GroupAdd": null,
        "RestartPolicy": {
            "Name": "no",
            "MaximumRetryCount": 0
        },
        "SecurityOpt": null,
        "ReadonlyRootfs": false,
        "Ulimits": null,
        "LogConfig": {
            "Type": "json-file",
            "Config": {}
        },
        "CgroupParent": "",
        "ConsoleSize": [
            0,
            0
        ],
        "VolumeDriver": ""
    },
    "GraphDriver": {
        "Name": "aufs",
        "Data": null
    },
    "Mounts": [],
    "Config": {
        "Hostname": "f76eaf5dedb0",
        "Domainname": "",
        "User": "",
        "AttachStdin": true,
        "AttachStdout": true,
        "AttachStderr": true,
        "Tty": true,
        "OpenStdin": true,
        "StdinOnce": true,
        "Env": null,
        "Cmd": [
            "/bin/bash"
        ],
        "Image": "ubuntu",
        "Volumes": null,
        "WorkingDir": "",
        "Entrypoint": null,
        "OnBuild": null,
        "Labels": {},
        "StopSignal": "SIGTERM"
    },
    "NetworkSettings": {
        "Bridge": "",
        "SandboxID": "491ff4e54c9476f40a4ccc0841c422c8b0686371d97160e06f45f9c36d1a06bb",
        "HairpinMode": false,
        "LinkLocalIPv6Address": "",
        "LinkLocalIPv6PrefixLen": 0,
        "Ports": {},
        "SandboxKey": "/var/run/docker/netns/491ff4e54c94",
        "SecondaryIPAddresses": null,
        "SecondaryIPv6Addresses": null,
        "EndpointID": "d3948292c4c548a83d3f983aabd9b3bb849f25653cbc770407fe1e7cf7b50d34",
        "Gateway": "172.17.0.1",
        "GlobalIPv6Address": "",
        "GlobalIPv6PrefixLen": 0,
        "IPAddress": "172.17.0.2",
        "IPPrefixLen": 16,
        "IPv6Gateway": "",
        "MacAddress": "02:42:ac:11:00:02",
        "Networks": {
            "bridge": {
                "EndpointID": "d3948292c4c548a83d3f983aabd9b3bb849f25653cbc770407fe1e7cf7b50d34",
                "Gateway": "172.17.0.1",
                "IPAddress": "172.17.0.2",
                "IPPrefixLen": 16,
                "IPv6Gateway": "",
                "GlobalIPv6Address": "",
                "GlobalIPv6PrefixLen": 0,
                "MacAddress": "02:42:ac:11:00:02"
            }
        }
    }
}
]
```

##rm，删除容器

```sh
docker rm <id>/<name>
```
该命令只能删除已停止运行的容器。目前没有删除所有容器的命令，但可以使用以下小技巧来删除所有容器：

```sh
docker rm `docker ps -a -q`
```

##push，将本地镜像推到远程库
docker push yuatom/php:7-fpm

##commit、将容器提交到镜像
docker commit -m "php 7 fpm with setting nginx docuemnt root" -a "yuatom" d5636c7f4e3c yuatom/php:7-fpm
-m 附加信息
-a 作者
容器id
库/镜像名:tag

##rmi、删除镜像

# 列出当前所有正在运行的container  
$docker ps  
# 列出所有的container  
$docker ps -a  
# 列出最近一次启动的container  
$docker ps -l  
XBD3V@888&


##build
--no-cache  不使用缓存
-t  镜像名称

docker

docker images
docker pull $imagename
docker commit -m $message -a $author $container_id $repo/$imagename:$tag
docker tag $containerid $repo/$imagename:$tag
docker save -o
docker load --input $localimagepath
docker load < $localimagepath
docker rmi 
“docker rmi $(docker images --quiet --filter "dangling=true")” 删除未打标签的中间镜像，因为这些没有打标签（没有意义）的镜像会占用空间


docker run -t -i \$repo/\$imagename:\$tag --name\$containername
-t为容器分配一个伪终端
-i打开容器的标准输入
-t -i 结合，即在容器启动时打开一个终端，并接受run命令后面的shell命令到容器里的终端
-v挂载，-v $hostdir:$destdir:$mode
--volum-from从其它容器挂载
-p指定映射的端口，ip:hostPort:containerPort | ip::containerPort （本机的任意端口都到容器的某个端口）| hostPort:containerPort
-P，随机映射一个主机49000~49900之间的端口到容器端口
--link，容器互联，name:alias，使得容器不需要暴露端口就能通过alias访问name容器，通过env和host两种方式实现


docker stop
docker rm
-v同时删除挂载了该容器的容器
docker ps
docker logs
docker attach
docker export
docker import
docker inspect
docker port





