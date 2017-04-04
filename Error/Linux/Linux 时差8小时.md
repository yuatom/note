# linux 时间差了八小时

```sh
tzselect
```

/etc/timezone 中添加时区
/etc/localtime，从/usr/share/zoneinfo所选时区的文件复制到/etc/localtime。

如果修改后的没效果，可能需要配置时间同步

```sh
yum install -y ntp        #安装时间同步服务（组件）
ntpdate us.pool.ntp.org   #设置同步服务器
date                      #查看当前时间
```
