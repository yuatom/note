# php install

./configure --prefix=/usr/local/php-5.3.17 --enable-fpm --with-mysql=/usr/bin/ --with-config-file-path=、usr/local/php-5.3.17 --with-mysqli=/usr/bin/mysql_config --with-curl



##configure: error: Cannot find libmysqlclient under /usr.
原因：64位的系统吧libmysqlclient默认按照到/usr/lib64/MySQL目录，所以查找不到。
解决：ln -s /usr/lib64/mysql/ /usr/lib/mysql

##configure: error: Cannot find MySQL header files under /usr/bin/.
原因：--with-mysql时没有加上mysql的目录。
解决：安装mysql，--wthi-mysql=mysql可执行二进制文件的目录，--with-mysqli=mysql_config可执行二进制文件目录。
yum安装mysql：yum install -y mysql-server mysql mysql-devel

##configure: error: Please reinstall the libcurl distribution -
    easy.h should be in /include/curl/
原因：缺少curl的依赖包。
解决：yum install curl curl-devel

##configure error xml2-config not found. please check your libxml2 installation
原因：缺少libxml2依赖包。
解决：yum install libxml2 libxml2-devel


#Cannot find autoconf. Please check your autoconf installation and the
yum install autoconf