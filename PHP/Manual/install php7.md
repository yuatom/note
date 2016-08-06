# install php7

```shell
#!/bin/bash
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi
apt-get update
apt-get install -y git-core autoconf bison libxml2-dev libbz2-dev libmcrypt-dev libcurl4-openssl-dev libltdl-dev libpng-dev libpspell-dev libreadline-dev make
mkdir -p /etc/php7/conf.d
mkdir -p /etc/php7/cli/conf.d
mkdir /usr/local/php7
cd /tmp
git clone https://github.com/php/php-src.git --depth=1
cd php-src
./buildconf
./configure --prefix=/usr/local/php7 --enable-bcmath --with-bz2 --enable-calendar --enable-exif --enable-dba --enable-ftp --with-gettext --with-gd --enable-mbstring --with-mcrypt --with-mhash --enable-mysqlnd --with-mysql=mysqlnd --with-mysqli=mysqlnd --with-pdo-mysql=mysqlnd --with-openssl --enable-pcntl --with-pspell --enable-shmop --enable-soap --enable-sockets --enable-sysvmsg --enable-sysvsem --enable-sysvshm --enable-wddx --with-zlib --enable-zip --with-readline --with-curl --with-config-file-path=/etc/php7/cli --with-config-file-scan-dir=/etc/php7/cli/conf.d
make
make test
make install
```

