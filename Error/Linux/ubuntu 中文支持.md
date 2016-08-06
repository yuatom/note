# ubuntu 中文支持
apt-get install language-pack-zh-hant language-pack-zh-hans-base

vim /etc/environment
在文件中增加语言和编码的设置：
LANG="zh_CN.UTF-8" LANGUAGE="zh_CN:zh:en_US:en"

sudo dpkg-reconfigure locales

