#cut&grep&sort&wc&uniq



wc
chmod [who] [+|-|=] = [mode]




login shell:
/etc/profile    系统设置
~/.bash_profile  ~/.bash_login  ~/.profile    个人设置



执行多条命令
分号;   分号前的指令执行完后就会立刻接着执行后面的指令了
&&    前面的命令执行正确，则执行后面的
||        前面的命令执行正确，则不执行后面的

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









