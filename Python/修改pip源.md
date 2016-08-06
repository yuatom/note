# 修改pip源

~/.pip/pip.conf

```shell
[global]
index-url = http://mirrors.aliyun.com/pypi/simple/
[install]
trusted-host=mirrors.aliyun.com
```

http://mirrors.aliyun.com/pypi/simple/ 
http://pypi.douban.com/simple
http://pypi.v2ex.com/simple

> trusted-host选项为添加信任的源，不然新版本会报错误：he repository located @ pypi.v2ex.com is not a trusted or secure host and is being ignored. If this repository is available via HTTPS it is recommended to use HTTPS instead, otherwise you may silence this warning and allow it anyways with '--trusted-host pypi.v2ex.com'.

