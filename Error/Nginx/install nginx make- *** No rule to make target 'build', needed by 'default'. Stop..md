# install nginx make: *** No rule to make target 'build', needed by 'default'. Stop.

need to install PCRE libraries for Nginx to compile

```shell
# apt-get update # apt-get install libpcre3 libpcre3-dev
```

run ./configure to create Makefile and run make


#./configure: error: the HTTP rewrite module requires the PCRE library

apt-get install libpcre3 libpcre3-dev

#./configure: error: the HTTP gzip module requires the zlib library.
apt-get install libssl-dev  


