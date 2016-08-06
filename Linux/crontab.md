# crontab
crontab -l|-r|-e|-i [username]
   -l 显示用户的crontab文件的内容
   -i 删除crontab文件时给出提示
   -r 从crontab目录中删除用户的crontab文件
   -e 编辑用户的crontab文件
  
##格式

```shell
 ~ *　　*　　*　　*　　*　　command
 # 分　 时　 日　 月　 周　 命令
```
>* 第1列表示分钟1～59 每分钟用*或者 */1表示
>* 第2列表示小时1～23(0表示0点)
>* 第3列表示日期1～31
>* 第4列表示月份1～12
>* 第5列标识号星期0～6(0表示星期天)
>* 第6列要运行的命令

```shell
# 例子
30 21 * * * /usr/local/apache/bin/apachectl restart
#上面的例子表示每晚的21:30重启apache。
  
45 4 1,10,22 * * /usr/local/apache/bin/apachectl restart
#上面的例子表示每月1、10、22日的4 : 45重启apache。
  
10 1 * * 6,0 /usr/local/apache/bin/apachectl restart
#上面的例子表示每周六、周日的1 : 10重启apache。
  
0,30 18-23 * * * /usr/local/apache/bin/apachectl restart
#上面的例子表示在每天18 : 00至23 : 00之间每隔30分钟重启apache。
  
0 23 * * 6 /usr/local/apache/bin/apachectl restart
#上面的例子表示每星期六的11 : 00 pm重启apache。
  
* */1 * * * /usr/local/apache/bin/apachectl restart
#每一小时重启apache
  
* 23-7/1 * * * /usr/local/apache/bin/apachectl restart
#晚上11点到早上7点之间，每隔一小时重启apache
  
#每月每天每小时的第 0 分钟执行一次 /bin/ls :
0 * * * * /bin/ls

#在 12 月内, 每天的早上 6 点到 12 点中，每隔 20 分钟执行一次 /usr/bin/backup :
*/20 6-12 * 12 * /usr/bin/backup

#周一到周五每天下午 5:00 寄一封信给 ranger@domain.name :
0 17 * * 1-5 mail -s "hi" ranger@domain.name < /tmp/maildata

#每月每天的午夜 0 点 20 分, 2 点 20 分, 4 点 20 分....执行 echo "haha"
20 0-23/2 * * * echo "haha"

#晚上11点到早上8点之间每两个小时，早上8点
0 23-7/2，8 * * * date
```






