# 数据流重导向

##数据流
* 标准输入（stdin）：输入原来需要由键盘输入的数据，代码为0，使用<或<<
* 标准输出（stdout）：指令正常执行输出数据，代码为1，使用>或>>
* 标准错误输出（stderr）：指令执行过程出现错误的输出数据，代码为2，使用2>或2>>
* >：以覆盖的方式将输出写到指定的文件中；
* >>：以追加的方式将输出写到指定的文件中；

> >/>>/</<<后面跟的必须是文件


```shell
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

###/dev/null
数据黑洞，当把数据重定向到该文件时，即把数据丢掉，不输出到屏幕也不保存到文件。







cat > >> < <<


type
history
du
df
wc
vim yy 
cat -n              > 
chmod [who] [+|-|=] = [mode]
ps -ef
top <空格> h/? m t c M P q
crontab -l  -e    /var/spool/cron/user       /etc/crontab
vi    :x  :n  :$  :s/text1/text2   :s/text1/text2/g  :m,ns/text1/text2/g   i a o s r         0 $ H L M nG w/W e/E  b/B     x/X dd/D d0 dw   yy  p  u  r
head -n
tail -f -n
netstat
nslookup
余旭东  15:09:07
login shell:
/etc/profile    系统设置
~/.bash_profile  ~/.bash_login  ~/.profile    个人设置
余旭东  15:31:19
Ctrl + C 终止目前的命令
Ctrl + D 输入结束 （ EOF） ，例如邮件结束的时候；
Ctrl + M 就是 Enter 啦！
Ctrl + S 暂停屏幕的输出
Ctrl + Q 恢复屏幕的输出
Ctrl + U 在提示字符下，将整列命令删除
Ctrl + Z “暂停”目前的命令
余旭东  15:47:09
> >>
2> 2>>
余旭东  15:49:43
1> 1>>
2> 2>>
余旭东  15:52:53
/dev/null，所有传递给这个文件的东西都会被丢弃
余旭东  15:57:27
1> 1>>   标准输出
2> 2>>   标准错误
&> &>> 标准输出和错误
2>&1     将错误输出重定向到标准输出

find /etc -name passwd &2>&1 |less
分解为
1:  find /etc -name passwd &   将find命令放到后台
2:  错误输出重定向到标准输出，并用less分页
余旭东  16:04:09
find /etc -name passwd > t.tst 2>&1
=
find /etc -name passwd &>t.txt

find /etc -name passwd > t.tst  2>t.tst   // 错误，两股数据同时写入一个文件，没有使用特殊语法，会使得两股数据交叉写入，次序混乱，t.txt会还是会产生，但是顺序不是原屏幕上的
余旭东  16:15:41
执行多条命令
分号;   分号前的指令执行完后就会立刻接着执行后面的指令了
&&    前面的命令执行正确，则执行后面的
||        前面的命令执行正确，则不执行后面的
余旭东  16:46:34
管线命令  `|`  将前面命令的标准输出，传递给后面的命令处理
cut  对一行数据进行分解    -d 切割分隔符  -f 取出哪些行    -c 以字符单位取固定字符区间的字符
echo ${PATH} | cut -d ':' -f 3,5      以:分割成多行，取第三和第五行
echo ${PATH} | cut c 3-                取第三个字符及之后的所有

grep 从要处理的数据中取出某些行
-a ：将 binary 文件以 text 文件的方式搜寻数据
-c ：计算找到 '搜寻字串' 的次数
-i ：忽略大小写的不同，所以大小写视为相同
-n ：顺便输出行号
-v ：反向选择，亦即显示出没有 '搜寻字串' 内容的那一行
--color=auto ：可以将找到的关键字部分加上颜色的显示

last | grep 'root'      取出包含root的行
last | grep 'root' | cut -d ' ' -f1                取出包含root的行交给cut处理
余旭东  17:26:01
sort [-fbMnrtuk] [file or stdin] 排序
-f ：忽略大小写的差异，例如 A 与 a 视为编码相同；
-b ：忽略最前面的空白字符部分；
-M ：以月份的名字来排序，例如 JAN, DEC 等等的排序方法；
-n ：使用“纯数字”进行排序（ 默认是以文字体态来排序的） ；
-r ：反向排序；
-u ：就是 uniq ，相同的数据中，仅出现一行代表；
-t ：分隔符号，默认是用 [tab] 键来分隔；
-k ：以那个区间 （ field） 来进行排序的意思

 cat /etc/passwd | sort                 根据每行第一个字母排
cat /etc/passwd | sort -t ':' -k 3   每一行中以：分隔成多个段，使用第三段来排序
余旭东  08:16:52
uniq  将重复的只保留一个
-i ：忽略大小写字符的不同；
-c ：进行计数


wc  统计行数，单词数，字符数
-l ：仅列出行；
-w ：仅列出多少字（ 英文单字） ；
-m ：多少字符；
余旭东  08:17:05

 tee [-a] file       将数据分流送到文件和屏幕
-a ：以累加 （ append） 的方式，将数据加入 file 当中
last | tee last.list | cut -d ' ' -f1               保存last到last.list的同时给cut处理显示在屏幕上
余旭东  10:35:19
https://www.gitbook.com/@wizardforcel
余旭东  16:02:49
cp -a -i -d -p -r
余旭东  16:03:28
cp -a -i -d -p -r -l
余旭东  16:06:03
cp
-a ：相当于 -dr --preserve=all 的意思，至于 dr 请参考下列说明；（ 常用）
-d ：若来源文件为链接文件的属性（ link file） ，则复制链接文件属性而非文件本身；
-f ：为强制（ force） 的意思，若目标文件已经存在且无法打开，则移除后再尝试一次；
-i ：若目标文件（ destination） 已经存在时，在覆盖时会先询问动作的进行（ 常用）
-l ：进行硬式链接（ hard link） 的链接文件创建，而非复制文件本身；
-p ：连同文件的属性（ 权限、用户、时间） 一起复制过去，而非使用默认属性（ 备份常用） ；
-r ：递回持续复制，用于目录的复制行为；（ 常用）
-s ：复制成为符号链接文件 （ symbolic link） ，亦即“捷径”文件；
-u ：destination 比 source 旧才更新 destination，或 destination 不存在的情况下才复制。
--preserve=all ：除了 -p 的权限相关参数外，还加入 SELinux 的属性, links, xattr 等也复制了。
最后需要注意的，如果来源文件有两个以上，则最后一个目的文件一定要是“目录”才行
余旭东  16:10:09
cat
tac
nl
more
less
head
tail
od
余旭东  17:45:05
umask 就是指定 “目前使用者在创建文件或目录时候的权限默认值”，umask 的分数指的是“该默认值需要减掉的权限”
查看当前的分数
一种可以直接输入 umask ，就可以看到数字体态的权限设置分数， 第一组是特殊权限用的， 
一种则是加入 -S （ Symbolic） 这个选项，就会以符号类型的方式来显示出权限了
余旭东  17:49:09
chattr   设置文件隐藏属性   只能在Ext2/Ext3/Ext4的 Linux 传统文件系统上面完整生效， 其他的文件系统可能就无法完整的支持这个指令了，例如 xfs 仅支持部份参数而已
+ ：增加某一个特殊参数，其他原本存在参数则不动。
- ：移除某一个特殊参数，其他原本存在参数则不动。
= ：设置一定，且仅有后面接的参数
A ：当设置了 A 这个属性时，若你有存取此文件（ 或目录） 时，他的存取时间 atime 将不会被修改，可避免 I/O 较慢的机器过度的存取磁盘。（ 目前建议使用文件系统挂载参数处理这个项目）
S ：一般文件是非同步写入磁盘的（ 原理请参考[前一章sync](../Text/index.html#sync)的说明） ，如果加上 S 这个属性时，当你进行任何文件的修改，该更动会“同步”写入磁盘中。
a ：当设置 a 之后，这个文件将只能增加数据，而不能删除也不能修改数据，只有root 才能设置这属性
c ：这个属性设置之后，将会自动的将此文件“压缩”，在读取的时候将会自动解压缩，但是在储存的时候，将会先进行压缩后再储存（ 看来对于大文件似乎蛮有用的！）
d ：当 dump 程序被执行的时候，设置 d 属性将可使该文件（ 或目录） 不会被 dump 备份
i ：这个 i 可就很厉害了！他可以让一个文件“不能被删除、改名、设置链接也无法写入或新增数据！”对于系统安全性有相当大的助益！只有 root 能设置此属性
s ：当文件设置了 s 属性时，如果这个文件被删除，他将会被完全的移除出这个硬盘空间，所以如果误删了，完全无法救回来了喔！
u ：与 s 相反的，当使用 u 来设置文件时，如果该文件被删除了，则数据内容其实还存在磁盘中，可以使用来救援该文件喔！
注意1：属性设置常见的是 a 与 i 的设置值，而且很多设置值必须要身为 root 才能设置
注意2：xfs 文件系统仅支持 AadiS 而已
余旭东  17:51:43
lsattr   [-adR] 文件或目录  显示文件隐藏属性
-a ：将隐藏文件的属性也秀出来；
-d ：如果接的是目录，仅列出目录本身的属性而非目录内的文件名；
-R ：连同子目录的数据也一并列出来！
余旭东  21:36:38
cp
-a ：相当于 -dr --preserve=all 的意思，至于 dr 请参考下列说明；（ 常用）
-d ：若来源文件为链接文件的属性（ link file） ，则复制链接文件属性而非文件本身；
-f ：为强制（ force） 的意思，若目标文件已经存在且无法打开，则移除后再尝试一次；
-i ：若目标文件（ destination） 已经存在时，在覆盖时会先询问动作的进行（ 常用）
-l ：进行硬式链接（ hard link） 的链接文件创建，而非复制文件本身；
-p ：连同文件的属性（ 权限、用户、时间） 一起复制过去，而非使用默认属性（ 备份常用） ；
-r ：递回持续复制，用于目录的复制行为；（ 常用）
-s ：复制成为符号链接文件 （ symbolic link） ，亦即“捷径”文件；
-u ：destination 比 source 旧才更新 destination，或 destination 不存在的情况下才复制。
--preserve=all ：除了 -p 的权限相关参数外，还加入 SELinux 的属性, links, xattr 等也复制了。
最后需要注意的，如果来源文件有两个以上，则最后一个目的文件一定要是“目录”才行
余旭东  21:37:03
cat
tac
nl
more
less
head
tail
od
余旭东  21:37:14
umask 就是指定 “目前使用者在创建文件或目录时候的权限默认值”，umask 的分数指的是“该默认值需要减掉的权限”
查看当前的分数
一种可以直接输入 umask ，就可以看到数字体态的权限设置分数， 第一组是特殊权限用的， 
一种则是加入 -S （ Symbolic） 这个选项，就会以符号类型的方式来显示出权限了
余旭东  21:37:26
chattr   设置文件隐藏属性   只能在Ext2/Ext3/Ext4的 Linux 传统文件系统上面完整生效， 其他的文件系统可能就无法完整的支持这个指令了，例如 xfs 仅支持部份参数而已
+ ：增加某一个特殊参数，其他原本存在参数则不动。
- ：移除某一个特殊参数，其他原本存在参数则不动。
= ：设置一定，且仅有后面接的参数
A ：当设置了 A 这个属性时，若你有存取此文件（ 或目录） 时，他的存取时间 atime 将不会被修改，可避免 I/O 较慢的机器过度的存取磁盘。（ 目前建议使用文件系统挂载参数处理这个项目）
S ：一般文件是非同步写入磁盘的（ 原理请参考[前一章sync](../Text/index.html#sync)的说明） ，如果加上 S 这个属性时，当你进行任何文件的修改，该更动会“同步”写入磁盘中。
a ：当设置 a 之后，这个文件将只能增加数据，而不能删除也不能修改数据，只有root 才能设置这属性
c ：这个属性设置之后，将会自动的将此文件“压缩”，在读取的时候将会自动解压缩，但是在储存的时候，将会先进行压缩后再储存（ 看来对于大文件似乎蛮有用的！）
d ：当 dump 程序被执行的时候，设置 d 属性将可使该文件（ 或目录） 不会被 dump 备份
i ：这个 i 可就很厉害了！他可以让一个文件“不能被删除、改名、设置链接也无法写入或新增数据！”对于系统安全性有相当大的助益！只有 root 能设置此属性
s ：当文件设置了 s 属性时，如果这个文件被删除，他将会被完全的移除出这个硬盘空间，所以如果误删了，完全无法救回来了喔！
u ：与 s 相反的，当使用 u 来设置文件时，如果该文件被删除了，则数据内容其实还存在磁盘中，可以使用来救援该文件喔！
注意1：属性设置常见的是 a 与 i 的设置值，而且很多设置值必须要身为 root 才能设置
注意2：xfs 文件系统仅支持 AadiS 而已










特殊权限

当 s 这个标志出现在文件拥有者的 x 权限上时：“-rwsr-xr-x”，此时就被称为 Set UID，简称为 SUID 的特殊权限。基本上SUID有这样的限制与功能：
SUID 权限仅对二进制程序（ binary program） 有效；
执行者对于该程序需要具有 x 的可执行权限；
本权限仅在执行该程序的过程中有效 （ run-time） ；
执行者将具有该程序拥有者 （ owner） 的权限。

当 s 标志在文件拥有者的 x 项目为 SUID，那 s 在群组的 x 时则称为 Set GID, SGID。SGID 可以针对文件或目录来设置！如果是对文件来说， SGID 有如下的功能：
SGID 对二进制程序有用；
程序执行者对于该程序来说，需具备 x 的权限；
执行者在执行的过程中将会获得该程序群组的支持

当一个目录设置了 SGID 的权限后，他将具有如下的功能：
使用者若对于此目录具有 r 与 x 的权限时，该使用者能够进入此目录；
使用者在此目录下的有效群组（ effective group） 将会变成该目录的群组；
用途：若使用者在此目录下具有 w 的权限（ 可以新建文件） ，则使用者所创建的新文
件，该新文件的群组与此目录的群组相同。

当t标志出现在目录的其他人的x项，为Sticky Bit, SBIT 目前只针对目录有效，对于文件已经没有效果了。SBIT 对于目录的作用是：
当使用者对于此目录具有 w, x 权限，亦即具有写入的权限时；
当使用者在该目录下创建文件或目录时，仅有自己与 root 才有权力删除该文件

当甲这个使用者于 A 目录是具有群组或其他人的身份，并且拥有该目录 w 的权限， 这表示“甲使用者对该目录内任何人创建的目录或文件均可进行 "删除/更名/搬移" 等动作。” 不过，如果将 A 目录加上了 SBIT 的权限项目时， 则甲只能够针对自己创建的文件或目录进行删除/更名/移动等动作，而无法删除他人的文件。

余旭东  21:38:15
设置SUID/SGID/SBIT，只需要在原来三位数字的权限前面，加上一个数字，4为SUID，2为SGID，1为SBIT。假设要改成rwsr-xr-x，可以使用chmod 4755 filename
7表示空SUID/SGID/SBIT，在文件/目录的权限列表中会显示成大S和大T，即 -rwSrwSrwT，此时user/group/other都没有可执行权限。这个 S, T 代表的就是“空的”啦！怎么说？ SUID 是表示“该文件在执行的时候，具有文件拥有者的权限”，但是文件 拥有者都无法执行了，哪里来的权限给其他人使用？当然就是空的。
除了用数字，还可以用符号，其中 SUID 为 u+s ，而 SGID 为 g+s ，SBIT 则是 o+t 
余旭东  21:38:31
which  寻找可执行文件，根据“PATH”这个环境变量所规范的路径，去搜寻“可执行文件”的文件名，不显示bash的内置指令
-a ：将所有由 PATH 目录中可以找到的指令均列出，而不止第一个被找到的指令名称
余旭东  21:38:46
whereis [-bmsu] 文件或目录名    只搜索特定目录下文件名， /bin /sbin   /usr/share/man  及其他几个特定目录（用-l看目录列表），速度比find快
-l :可以列出 whereis 会去查询的几个主要目录而已
-b :只找 binary 格式的文件
-m :只找在说明文档 manual 路径下的文件
-s :只找 source 来源文件
-u :搜寻不在上述三个项目当中的其他特殊文件

locate [-ir] keyword    搜索文件的部分名称，不是直接搜索磁盘，而是从创建好的数据库/var/lib/mlocate/中查找，该数据库有系统维护，默认每天更新一次，可使用updatedb手动更新该数据库。updatedb 指令会去读取 /etc/updatedb.conf 这个配置文件的设置，然后再去硬盘里面进行搜寻文件名的动作，最后再去更新整个数据库
-i ：忽略大小写的差异；
-c ：不输出文件名，仅计算找到的文件数量
-l ：仅输出几行的意思，例如输出五行则是 -l 5
-S ：输出 locate 所使用的数据库文件的相关信息，包括该数据库纪录的文件/目录数量等
-r ：后面可接正则表达式的显示方式

find [PATH] [option] [action]

1\. 与时间有关的选项：共有 -atime, -ctime 与 -mtime ，以 -mtime 说明
-mtime n ：n 为数字，意义为在 n 天之前的“一天之内”被更动过内容的文件；
-mtime +n ：列出在 n 天之前（ 不含 n 天本身） 被更动过内容的文件文件名；
-mtime -n ：列出在 n 天之内（ 含 n 天本身） 被更动过内容的文件文件名。
-newer file ：file 为一个存在的文件，列出比 file 还要新的文件文件名

2\. 与使用者或群组名称有关的参数：
-uid n ：n 为数字，这个数字是使用者的帐号 ID，亦即 UID ，这个 UID 是记录在
/etc/passwd 里面与帐号名称对应的数字。这方面我们会在第四篇介绍。
-gid n ：n 为数字，这个数字是群组名称的 ID，亦即 GID，这个 GID 记录在
/etc/group，相关的介绍我们会第四篇说明～
-user name ：name 为使用者帐号名称喔！例如 dmtsai
-group name：name 为群组名称喔，例如 users ；
-nouser ：寻找文件的拥有者不存在 /etc/passwd 的人！
-nogroup ：寻找文件的拥有群组不存在于 /etc/group 的文件！
当你自行安装软件时，很可能该软件的属性当中并没有文件拥有者，
这是可能的！在这个时候，就可以使用 -nouser 与 -nogroup 搜寻。

3\. 与文件权限及名称有关的参数：
-name filename：搜寻文件名称为 filename 的文件；
-size [+-]SIZE：搜寻比 SIZE 还要大（ +） 或小（ -） 的文件。这个 SIZE 的规格有：
c: 代表 Byte， k: 代表 1024Bytes。所以，要找比 50KB
还要大的文件，就是“ -size +50k ”
-type TYPE ：搜寻文件的类型为 TYPE 的，类型主要有：一般正规文件 （ f） , 设备文件 （ b, c） ,
目录 （ d） , 链接文件 （ l） , socket （ s） , 及 FIFO （ p） 等属性。
-perm mode ：搜寻文件权限“刚好等于” mode 的文件，这个 mode 为类似 chmod
的属性值，举例来说， -rwsr-xr-x 的属性为 4755 ！
-perm -mode ：搜寻文件权限“必须要全部囊括 mode 的权限”的文件，举例来说，
我们要搜寻 -rwxr--r-- ，亦即 0744 的文件，使用 -perm -0744，
当一个文件的权限为 -rwsr-xr-x ，亦即 4755 时，也会被列出来，
因为 -rwsr-xr-x 的属性已经囊括了 -rwxr--r-- 的属性了。
-perm /mode ：搜寻文件权限“包含任一 mode 的权限”的文件，举例来说，我们搜寻
-rwxr-xr-x ，亦即 -perm /755 时，但一个文件属性为 -rw-------
也会被列出来，因为他有 -rw.... 的属性存

4\. 额外可进行的动作：
-exec command ：command 为其他指令，-exec 后面可再接额外的指令来处理搜寻到的结果。
-print ：将结果打印到屏幕上，这个动作是默认动作！
余旭东  10:42:12
jobs [-lrs]
fg jobsnumber
fg -
在命令后加&，可将命令丢到bash的背景执行，之后可以在该bash中执行其他命令，这里的背景仅是指不会影响当前bash其他操作的背景，而不是系统的背景。
如果这个命令启动的不是守护进程，那当退出当前的bash时，该bash背景的任务也会被退出。

nohup [指令与参数] [&]，执行与终端机无关的任务，不支持/bin/bash内置指令，&表示将任务放到后台去执行
执行程序的输出会输出到该文件~/nohup.out


ps -l 查看自己的进程
ps -lA 查看自己的进程和系统的进程
ps aux 查看系统运行的所有进程

pstree [-AUup]
-A ：各程序树之间的连接以 ASCII 字符来连接；
-U ：各程序树之间的连接以万国码的字符来连接。在某些终端接口下可能会有错误；
-p ：并同时列出每个 process 的 PID；
-u ：并同时列出每个 process 的所属帐号名称
余旭东  10:48:46
free [-b|k|m|gtsc]    查看内存占用
-b/k/m/g：显示单位，默认以byte
-t：显示物理内存和swap内存总量
-s：可以让系统每隔几秒输出一次
-c ：与 -s 同时处理
余旭东  14:36:07
nohup [指令与参数] [&]，执行与终端机无关的任务，不支持/bin/bash内置指令，&表示将任务放到后台去执行
该命令可以在bash用exit退出后继续在后台运行
执行程序的标准输出会保存到该文件~/nohup.out
余旭东  14:37:08
nohup command > myout.file 2>&1 &  修改输出。






# netstat -[atunlp]
选项与参数：
-a ：将目前系统上所有的连线、监听、Socket 数据都列出来
-t ：列出 tcp 网络封包的数据
-u ：列出 udp 网络封包的数据
-n ：不以程序的服务名称，以埠号 （ port number） 来显示；
-l ：列出目前正在网络监听 （ listen） 的服务；
-p ：列出该网络服务的程序 PID

netstat -tulnp  | grep portnumber
余旭东  15:13:12
vmstat 可以侦测“ CPU / 内存 / 磁盘输入输出状态 ”
vmstat [-a] [延迟 [总计侦测次数]]            CPU/内存等信息
vmstat [-fs]                                          内存相关
vmstat [-S 单位]                                   设置显示数据的单位
vmstat [-d]                                          与磁盘有关
vmstat [-p 分区]                                   与磁盘有关
选项与参数：
-a ：使用 inactive/active（ 活跃与否） 取代 buffer/cache 的内存输出信息；
-f ：开机到目前为止，系统复制 （ fork） 的程序数；
-s ：将一些事件 （ 开机至目前为止） 导致的内存变化情况列表说明；
-S ：后面可以接单位，让显示的数据有单位。例如 K/M 取代 Bytes 的容量；
-d ：列出磁盘的读写总量统计表
-p ：后面列出分区，可显示该分区的读写总量统计表


vmstat 1 3，查看资源信息，每秒刷新1次，总共刷新3次，后面的数字没给出的话，会无限刷新下去
vmstat -d，查看磁盘读写情况，可以使用时间参数来控制刷新频率和次数
余旭东  16:35:47
/proc/*    保存内存中的程序数据
各个程序的PID都是以目录的形态存在于/proc当中。
举例来说，开机所执行的第一支程序 systemd 他的 PID 是 1 ， 这个 PID 的所有相关信息都写入在/proc/1/* 当中。
余旭东  18:40:38
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
余旭东  22:03:33
systemd, systemctl

systemctl [command] [unit]
command 主要有：
start ：立刻启动后面接的 unit
stop ：立刻关闭后面接的 unit
restart ：立刻关闭后启动后面接的 unit，亦即执行 stop 再 start 的意思
reload ：不关闭后面接的 unit 的情况下，重新载入配置文件，让设置生效
enable ：设置下次开机时，后面接的 unit 会被启动
disable ：设置下次开机时，后面接的 unit 不会被启动
status ：目前后面接的这个 unit 的状态，会列出有没有正在执行、开机默认执行否、登录等信息等！
is-active ：目前有没有正在运行中
is-enable ：开机时有没有默认要启用这个 unit

范例一：看看目前 atd 这个服务的状态为何？
[root@study ~]# systemctl status atd.service
atd.service - Job spooling tools
Loaded: loaded （ /usr/lib/systemd/system/atd.service; enabled）
Active: active （ running） since Mon 2015-08-10 19:17:09 CST; 5h 42min ago
Main PID: 1350 （ atd）
CGroup: /system.slice/atd.service
└─
1350 /usr/sbin/atd -f
Aug 10 19:17:09 study.centos.vbird systemd[1]: Started Job spooling tools.
# 重点在第二、三行喔～
# Loaded：这行在说明，开机的时候这个 unit 会不会启动，enabled 为开机启动，disabled 开机不会启动
# Active：现在这个 unit 的状态是正在执行 （ running） 或没有执行 （ dead）
# 后面几行则是说明这个 unit 程序的 PID 状态以及最后一行显示这个服务的登录文件信息！
# 登录文件信息格式为：“时间” “讯息发送主机” “哪一个服务的讯息” “实际讯息内容”
# 所以上面的显示讯息是：这个 atd 默认开机就启动，而且现在正在运行的意思！
范例二：正常关闭这个 atd 服务
[root@study ~]# systemctl stop atd.service
[root@study ~]# systemctl status atd.service
atd.service - Job spooling tools
Loaded: loaded （ /usr/lib/systemd/system/atd.service; enabled）
Active: inactive （ dead） since Tue 2015-08-11 01:04:55 CST; 4s ago
Process: 1350 ExecStart=/usr/sbin/atd -f $OPTS （ code=exited, status=0/SUCCESS）
Main PID: 1350 （ code=exited, status=0/SUCCESS）
Aug 10 19:17:09 study.centos.vbird systemd[1]: Started Job spooling tools.
Aug 11 01:04:55 study.centos.vbird systemd[1]: Stopping Job spooling tools...
Aug 11 01:04:55 study.centos.vbird systemd[1]: Stopped Job spooling tools.
# 目前这个 unit 下次开机还是会启动，但是现在是没在运行的状态中！同时，
# 最后两行为新增加的登录讯息，告诉我们目前的系统状态喔！



unit相关
[root@study ~]# systemctl [command] [--type=TYPE] [--all]
command:
list-units ：依据 unit 列出目前有启动的 unit。若加上 --all 才会列出没启动的。
list-unit-files ：依据 /usr/lib/systemd/system/ 内的文件，将所有文件列表说明。
--type=TYPE：就是之前提到的 unit type，主要有 service, socket, target 等


target相关
[root@study ~]# systemctl [command] [unit.target]
选项与参数：
command:
get-default ：取得目前的 target
set-default ：设置后面接的 target 成为默认的操作模式
isolate ：切换到后面接的模式
show  ：显示默认设置值

systemctl poweroff 系统关机
systemctl reboot 重新开机
systemctl suspend 进入暂停模式
systemctl hibernate 进入休眠模式
systemctl rescue 强制进入救援模式
systemctl emergency 强制进入紧急救援模式



查看服务依赖
systemctl list-dependencies [unit] [--reverse]
选项与参数：
--reverse ：表示谁在依赖这个unit，不带该参数时表示这个unit依赖谁



service类型服务配置相关
/usr/lib/systemd/system/vsftpd.service：官方释出的默认配置文件；
/etc/systemd/system/vsftpd.service.d/custom.conf：在 /etc/systemd/system 下面创建与
配置文件相同文件名的目录，但是要加上 .d 的扩展名。然后在该目录下创建配置文件即
可。另外，配置文件最好附文件名取名为 .conf 较佳！ 在这个目录下的文件会“累加其他
设置”进入 /usr/lib/systemd/system/vsftpd.service 内喔！
/etc/systemd/system/vsftpd.service.wants/*：此目录内的文件为链接文件，设置相依服
务的链接。意思是启动了 vsftpd.service 之后，最好再加上这目录下面建议的服务。
/etc/systemd/system/vsftpd.service.requires/*：此目录内的文件为链接文件，设置相依
服务的链接。意思是在启动 vsftpd.service 之前，需要事先启动哪些服务的意思。

余旭东  22:03:59
运行两个vsftpd

1 创建新的服务
创建/etc/vsftpd/vsftpd2.conf文件，修改监听字段；
创建/usr/lib/systemd/system/vsftpd2.service文件，修改加载的配置文件；
systemctl daemon-reload，重新加载systemd服务，读取刚刚创建的配置文件，读取新的服务；
systemctl restart vsftpd.service vsftpd2.service，重启服务；
systemctl enable vsftpd.service vsftpd2.service，启用服务，开机启动；

2 使用@服务语法
cat /usr/lib/systemd/system/vsftpd@.service，查看配置文件@的读取规则；
ExecStart=/usr/sbin/vsftpd /etc/vsftpd/%i.conf，%i.conf表示配置文件以@后面的字符串+.conf命名；
创建/etc/vsftpd/vsftpd2.conf文件，修改监听字段；
systemctl start vsftpd@vsftpd2.service，启动@服务，回去查找/etc/vsftpd/vsftpd2.conf文件；
systemctl status vsftpd@vsftpd2.service，查看服务状态；
余旭东  22:04:15
shell
test
-z
-n
-e
-f
-d
-a
-o
!

[]中括号判断

shift

if []; then elif []; if && || = ==

case  $var in
  "" )
    code
  ;;
  "" )
    code
  ;;
  * )
    code
    ;;
esac 

echo
date
declare 


读取参数的方式
$1 $2 $3...

$# ：代表后接的参数『个数』，以上表为例这里显示为『 4 』；
$@ ：代表『 "$1" "$2" "$3" "$4" 』之意，每个变量是独立的(用双引号括起来)；
$* ：代表『 "$1c$2c$3c$4" 』，其中 c 为分隔字节，默认为空白键， 所以本例中代表『 "$1 $2 $3 $4" 』之意。

read
















函数定义
function  fun(){
    # $1 $2...
}

函数调用，传参
func a c

满足时运行
while [ condition ]
do
     code
done

满足时终止
util [condition]
do
   code
done

var在循环中的值依次为con1 con2 con3
for var in con1 con2 con3
do
    code
done

for ((初始值; 限制值; 运行步阶))
do
    code
done

for (( i=1; i<=$nu; i=i+1 ))
do
	s=$(($s+$i))
done

seq   seq 1 100
cut
