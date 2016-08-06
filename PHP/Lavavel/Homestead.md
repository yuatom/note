# Homestead
##安装
安装 [VirtualBox](https://www.virtualbox.org/wiki/Downloads)与 [Vagrant](https://www.vagrantup.com/downloads.html)
###增加 Vagrant 封装包

```shell
vagrant box add laravel/homestead
```
或

```shell
vagrant box add laravel/homestead https://atlas.hashicorp.com/laravel/boxes/homestead
```

###安装 Homestead
在Home目录中

```shell
git clone https://github.com/laravel/homestead.git Homestead
```

在Homestead目录中，执行以下命令来初始化，并产生`~/.homestead/Homestead.yaml`配置文件

```shell
bash init.sh
```

###配置Provider
`Homestead.yaml`中的provider配置provider:virtualbox 、 vmware_fusion (Mac OS X)、或者 vmware_workstation (Windows)。

```shell
provider: virtualbox
```

###配置你的 SSH 密钥
```shell
ssh-keygen -t rsa -C "you@homestead"
```

###配置你的共享文件夹
如果要开启 NFS，只需要在 folders 中加入一个标识：

```shell
folders:
    - map: ~/Code
      to: /home/vagrant/Code
      type: "nfs"
```
###配置你的 Nginx 站点
你可以通过配置 hhvm 属性为 true 来让虚拟站点支持 HHVM:

```shell
sites:
    - map: homestead.app
      to: /home/vagrant/Code/Laravel/public
      hhvm: true
```
多个站点可配置多个map。

###多站点
在homestead主机中：

```shell
serve domain.app /home/vagrant/Code/path/to/public/directory 80
```

###单独配置目录
在项目的目录依次执行

```shell
# 安装homestead
composer require laravel/homestead --dev
# 生成Homestead.yaml
php vendor/bin/homestead make
```

##数据库
如果想要从本机上通过 Navicat 或者 Sequel Pro 连接 MySQL 或者 Postgres 数据库，你可以连接 127.0.0.1 的端口 33060 (MySQL) 或 54320 (Postgres)。而帐号密码分别是 homestead / secret

##通过 SSH 连接

要通过 SSH 连接上您的 Homestead 环境，在终端机里进入你的 Homestead 目录并执行 vagrant ssh 命令。

因为你可能会经常需要通过 SSH 进入你的 Homestead 虚拟机，可以考虑在你的主要机器上创建一个"别名" 用来快速 SSH 进入 Homestead 虚拟机:

alias vm="ssh vagrant@127.0.0.1 -p 2222"
你也可以在 Homestead 目录使用 vagrant ssh 命令

##连接端口

以下的端口将会被转发至 Homestead 环境：

SSH: 2222 → Forwards To 22
HTTP: 8000 → Forwards To 80
HTTPS: 44300 → Forwards To 443
MySQL: 33060 → Forwards To 3306
Postgres: 54320 → Forwards To 5432
增加额外端口

你也可以自定义转发额外的端口至 Vagrant box，只需要指定协议：

ports:
    - send: 93000
      to: 9300
    - send: 7777
      to: 777
      protocol: udp


