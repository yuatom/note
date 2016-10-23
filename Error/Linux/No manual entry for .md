
注释掉`/etc/yum.conf`中的`tsflags=nodocs`并执行：

```sh
yum reinstall man man-pages -y
```