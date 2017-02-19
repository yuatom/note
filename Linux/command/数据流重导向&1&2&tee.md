# 数据流重导向

##数据流
* 标准输入（stdin）：输入原来需要由键盘输入的数据，代码为0，使用<或<<
* 标准输出（stdout）：指令正常执行输出数据，代码为1，使用>或>>
* 标准错误输出（stderr）：指令执行过程出现错误的输出数据，代码为2，使用2>或2>>
* >：以覆盖的方式将输出写到指定的文件中；
* >>：以追加的方式将输出写到指定的文件中；
* `>`/`>>`/`<`/`<<`后面跟的必须是文件


```sh
# 创建test.txt文件并开始输入文件内容，如果test.txt不存在则创建
[root@a11adc88a32c ~]# cat > test.txt
test
test test
# 使用Ctrl+D来退出输入
# 将test.txt文件内容以标准输出输出到屏幕上
[root@a11adc88a32c ~]# cat test.txt
test
test test
# 将test.txt件内容输出覆盖到test2.txt中，即将标准输出重定向到test2.txt中
[root@a11adc88a32c ~]# cat test.txt > test2.txt
# 将test2.txt文件内容以标准输出输出到屏幕上
[root@a11adc88a32c ~]# cat test2.txt
test
test test

# 将test.txt的内容输出追加到test2.txt中
[root@a11adc88a32c ~]# cat test.txt >> test2.txt
[root@a11adc88a32c ~]# cat test2.txt
test
test test
test
test test

# 创建text3.txt从标准输入中读取内容到该文件中，标准输入为一个文件的内容
[root@a11adc88a32c ~]# cat > test3.txt < test2.txt
[root@a11adc88a32c ~]# cat test3.txt
test
test test
test
test test

# 创建text4.txt并开始从标准输入中读取内容，遇到eof时退出输入
[root@a11adc88a32c ~]# cat > text4.txt << "eof"
> text
> text
> text
> eof
[root@a11adc88a32c ~]# cat text4.txt
text
text
text
```

##重定向
* &>/&>>：&表示标准输出和标准错误输出两者；
* 2>&1：将错误输出重定向到标准输出；


###/dev/null
数据黑洞，当把数据重定向到该文件时，即把数据丢掉，不输出到屏幕也不保存到文件。

```sh
# 每天访问一次localhost，将标准输出保存到/dev/null中，并把错误输出重定向到标准输出中
[root@a11adc88a32c ~]# cron 0 0 * * * curl http://localhost > /dev/null 2>&1 &

```

###例子

```sh
[root@a11adc88a32c ~]# find /etc -name passwd &2>&1 |less
# 分解为：
# 1.find /etc -name passwd &   将find命令放到后台
# 2.错误输出重定向到标准输出，并用less分页

# 下面两者效果一样
[root@a11adc88a32c ~]# find /etc -name passwd > t.tst 2>&1
[root@a11adc88a32c ~]# find /etc -name passwd &>t.txt`

# 下面的用法是错的
# 两股数据同时写入一个文件，没有使用特殊语法，会使得两股数据交叉写入，次序混乱
# t.txt会还是会产生，但是顺序不是原屏幕上的
[root@a11adc88a32c ~]# find /etc -name passwd > t.tst  2>t.tst 

```


##tee

```sh
tee [-a] file       将数据分流送到文件和屏幕
```

###选项
* -a ：以累加 （ append） 的方式，将数据加入 file 当中

```sh
#保存last到last.list的同时给cut处理显示在屏幕上
[root@a11adc88a32c ~]# last | tee last.list | cut -d ' ' -f1  
```

EOF