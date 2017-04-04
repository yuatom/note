# sed

##命令形式

```shell
sed [options] 'command' file(s)
```

## options

* n：silent模式，默认情况下所有STDIN的内容会输出到屏幕上，加上n选项后只有经过sed处理的内容才会显示；
* e：执行多条sed命令；
* f：通过一个文件脚本来执行动作；
* i：直接修改读取的文件内容，而不是输出到终端；
* r：

## command
* 选定范围：
>* 选定一行`n....`：表示第n行；
>* 通过数字定位范围`n,m...`：表示n到m之间；
>* 通过搜索定位返回`/test/...`：表示包括test字符串的行（可以使用正则？）；
>* 通过搜索定位返回`/test/,/check/...`：表示包含test字符串到包含check字符串之间的行（可以使用正则？）；
>* 通过数字的搜索定位范围`5,/test/...`：表示第五行到包含test字符串之间的行；
* a：追加
>* `1a hello world`表示在第一行后面增加hello world
>* `1,3a hello world`在第一行到第三行后面增加字符串hello world；
* c：替换一行或多行
>* `n,mc hello world`n到m之间的行替换为hello world；
* d：删除
>* `2d`删除第二行；
>* `2,$d`删除从第二行到行末；
>* `$d`删除最后一行；
>* `/test/d`删除所有包含test字符的行；
* i：插入
* p：输入
* s：替换一行中的某部分
>* `s/test/hello world/g`把整行中的test替换为mytest，如果没有g则只替换第一个；
>* `s/^test/&hello world/`把以test开头的行替换中testhello world，&表示被查找的字符串；
>* `s/\(te\)st/\1hello world/p`把test替换为tehello world，\1表示第一个\(\)中的内容；
>* `s#test#hello world#`把test替换为hello world，s后的第一个符合会被当做分隔符，这里的#替换了/；
* w：写入
>* `/hello world/w file`将所有包含hello world的行写入到file中；
* n：下一行
>* `/hello word/{ n; s/test/mytest; }`对匹配到的hello world的下一行进行后面的操作；


## example

```shell
# 将所有的xxx.cpp替换为$ngx_objs_dirxxx$ngx_objext
sed "s#^\(.*\.\)cpp\\$#$ngx_objs_dir\1$ngx_objext#g" 
```

http://www.cnblogs.com/emanlee/archive/2013/09/07/3307642.html
http://www.iteye.com/topic/587673