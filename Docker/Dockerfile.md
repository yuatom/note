# Dockerfile

#Dockerfile
用于Docker build命令来创建镜像的“配置”文件，其中包括了创建镜像时需要的命令。

`docker bulid [OPTION] PATH | URL | - `
从包括命令的Dockerfile文件（用-f选项）和“上下文（context）”中创建镜像，上下文的参数可以是一个路径也可以是一个URL链接。

`docker build .  ` 使用当前的路径作为环境创建一个镜像。
该命令执行的第一步是将路径中上下文（递归的方式）发送给docker守护进程（daemon）。**大多数情况下，将一个空的目录作为上下文，将Dockerfile文件放在这个目录中**。

使用`-f`选项来指出Dockerfile的位置：
`$ doucker build -f /path/dockerfile .`

使用`-t`指出创建的镜像的仓库和标签
`$ docker build -t vieux/apache:2.0 .`
`$ docker build -f dockerfiles/Dockerfile.debug -t myapp_debug .`
`$ docker build -f dockerfiles/Dockerfile.prod  -t myapp_prod .`

使用-创建
`$ docker build - < Dockerfile` 从dockerfile文件中的命令来创建镜像，因为没有标出上下文的路径，因此不会发送任何本地目录给守护进程
`$ docker build - < context.tar.gz` 从一个压缩的上下文文件中创建镜像。

#Dockerfile支持的语法格式：
`#comment` 以#开头作为注释行，#在不是开头的行中会被当做参数。
`INSTRUCTION argument` 对应的命令和参数，命令没有大小写约束但一般用大写来和参数区分开来。


###`FROM`，指出要创建的镜像是基于那个基础镜像
Dockerfile文件中第一个命令必须是`FROM`。
```Dockerfile
FROM <image>
FROM <image>:<tag>
FROM <image>@<digest>
```


###`ENV`，声明环境变量。
参数为一个键值对，声明后的环境变量可以在该文件被其他命令通过`$varialbe_name`或`${varialbe_name}`调用（可使用\对$进行转义）。调用的同时支持bash修饰语法：
 `${variable:-word}`表示如果这个变量已经被定义，则使用变量原来的值，否则使用word；
 `${variable:+word}`表示如果这个变量已经被定义，则使用word作为当前的值，否则使用空字符串作为当前的值。
```Dockerfile
FROM busybox
ENV foo /bar
WORKDIR ${foo}   # WORKDIR /bar
ADD . $foo       # ADD . /bar
COPY \$foo /quux # COPY $foo /quux
```
ENV声明的变量支持的命令`ADD`、`COPY`、`ENV`、`EXPOSE`、`LABEL`、`USER`、`WORKDIR`、`VOLUME`、`STOPSIGNAL`、`ONBUILD`
**可使用`docker run --env <key>=<value>`更改容器中的变量。**


###`.dockerignore`文件
在控制台将上下文目录发送给守护进程之前，会在上下文的根目录中查找.dockerfile文件，上下文目录中能匹配到.dockerignore中规则的文件将不会发送给守护进程，该文件的作用类似于.gitignore。
匹配规则采用的是GO语言的路径匹配规则：
`*/temp*`，根目录下的子目录下temp开头的文件，temp后面可以没有字符
`*/*/temp*`，根目录下的二级子目录下temp开头的文件，temp后面可以没有字符
`temp?`，根目录中temp开头的文件，temp后面不能为空
`!README.md`，所有的README.md文件都不会匹配，
**当！在最后一行时，会覆盖其他的匹配效果**：
`*.md`
`README-secret.md`
`!README*.md`
如果最后一行!没有覆盖其他效果的话，上面的例子中，所有Markdown文件都不会发送（\*.md）,README-secret.md不会发送，但是由于README*.md匹配到README-sdecret.md文件，且该行是最后一行，以!开头，因此，README-secret.md文件会被发送到守护进程中。

###`MAINTAINER`，设置要创建的镜像的作者
```Dockerfile
MAINTAINER <name>
```


###`RUN`，执行命令
```Dockerfile
RUN <command>   //shell形式
RUN ["executable", "param1", "param2"]  //exec形式
```
RUN引导命令会在当前镜像的最高层创建一个可读写的层并执行命令，然后将执行后的结果提交到镜像中，用于Dockerfile文件中的下一步命令。
exec格式可以避免所使用的基础镜像中不包含/bin/sh；
shell格式支持使用\在多行中执行一个RUN：
```Dockerfile
RUN /bin/bash -c 'source $HOME/.bashrc ;\   //更新bashrc文件
echo $HOME'                                 //输出变量
```
相当于
```Dockerfile
RUN /bin/bash -c 'source $HOME/.bashrc ; echo $HOME'
```
要使用其他的shell，可以用exec形式来表达，exec通过JSON数组传递参数，因此要用到，k双引号：
```Dockerfile
RUN ["/bin/bash", "-c", "echo hello"]
```

RUN命令执行过程中产生的缓存，在下次执行时并不会失效，可使用docker build --no-cache选择设置不缓存。


###`CMD`，为容器提供了默认的执行命令。
与`$ docker run ` 命令启动容器时指定要运行的命令非常类似。
一个Dockerfile中只有一个CMD生效，如果在一个Dockerfile中存在多个CMD命令，则只有最后一条生效。
如果在Dockerfile中用`CMD`指定了要执行的命令，同时在`$ docker run `启动容器时也指定了命令，那么`CMD`中的命令会失效。
####命令格式
```Dockerfile
CMD ["executable","param1","param2"] (exec form, this is the preferred form)
CMD ["param1","param2"] (as default parameters to ENTRYPOINT)
CMD command param1 param2 (shell form)
```
####`CMD`与`docker run`转换
```shell
$ docker run -i -t <image> /bin/true
```
```Dockerfile
CMD ["/bin/true"]
```
作为`ENTRYPOINT`的默认参数时，需要用JSON数组形式传递。
CMD如果以exec或shell形式，设置的命令将会在镜像运行的时候执行。

`RUN`运行的命令会在build时将结果提交到镜像中，`CMD`的命令在build期间不会执行，但是说明了镜像运行时默认的命令。


###`ENTRYPOINT`，执行命令，不会被run覆盖
功能与`CMD`相似，但不会被docker run覆盖。
也可以接受从`CMD`或`docker run`传入的参数（`CMD`与`docker run`指定命令的功能类似）。
####命令格式
```Dockerfile
ENTRYPOINT ["executable", "param1", "param2"] (exec form, preferred)
ENTRYPOINT command param1 param2 (shell form)
```
执行命令，相当于`$ /usr/sbin/nginx -g daemon off;`：
```Dockerfile
ENTRYPOINT ["/usr/sbin/nginx","-g","daemon off;"]   //exec格式
ENTRYPOINT /usr/sbin/nginx -g -daemon off;          //shell格式
```
执行命令，`docker run`传入参数：
```Dockerfile
ENTRYPOINT ["/usr/sbin/nginx"]
```
```shell
$sudo docker run -t -i <image> -g "daemon off;"
```
执行命令，`CMD`传入参数：
```Dockerfile
ENTRYPOINT ["/usr/sbin/nginx"]
CMD ["`h"]
```
**可以在启动容器时通过`docker run`的`--entrypoint`标志覆盖`ENTRYPOINT`指令。**


###`LABEL`，为镜像添加meta头信息
参数为键值对。
一个镜像可能包括多个LABEL信息，但是每一个LABEL命令都会产生一个新的层，因此如果有多个LABEL信息，可写进一行，以空格分开：
```Dockerfile
LABEL multi.label1="value1" multi.label2="value2" other="value3"
```
在一个LABEL命令中支持用反斜杠换行：
```Dockerfile
LABEL multi.label1="value1" \
      multi.label2="value2" \
      other="value3"
```
新建镜像的LABEL会包括基础镜像的LABEL，可使用`docker inspect`来查看镜像的LABEL。


###`EXPOSE`指定容器启动时监听的端口
```Dockerfile
EXPOSE <port> [<port>...]
EXPOSE 80   //  暴露80端口
```
告诉docker该容器内部的应用程序将会使用容器的指定端口，但这并不意味着可以自动访问任意容器运行中服务的端口。
出于安全原因，Docker并不会自动打开该端口，需要在使用docker run运行容器时用-p 或-P选项来来指定打开哪些端口。


###`ADD`，将路径或URL为src的文件复制到镜像的dest路径中
```Dockerfile
ADD <src>... <dest>
ADD ["<src>",... "<dest>"] (this form is required for paths containing whitespace)
```
>* 可以有多个src，可以使用通配符；
>* dest是一个绝对路径，或者是相对于`WORKDIR`的相对路径；
>* 所有复制出来的文件的UID和GID的值都为0；
>* 如果src是一个远程的URL，那么dest路径将拥有600权限；
>* 如果远程的src的HTTP中有`Last-Modified`头信息，那这个头信息里的时间会被设置为目标文件的`mtime`，但是任何ADD操作产生的文件的mtime都不会影响源文件是否被修改及缓存更新；
>* 如果src是远程连接且dest的路径不是以斜杠结尾，那会先将这个文件下载然后复制到dest，如果以斜杠结尾，那复制后的文件将dest目录下保持源文件名；
>* 如果src是一个目录，那整个目录的内容都会被复制，包括文件系统的meta信息；
>* 如果src是一个本地可识别的压缩类型的文件，那复制后会被解压成一个目录，如果是远程的压缩文件则不会被解压，解压的过程和`tar -x`一致。


###`COPY`，将路径为src的源文件或目录复制到dest中
只复制文件，不会对URL的文件进行提取及对压缩文件件进行解压
```Dockerfile
COPY <src>... <dest>
COPY ["<src>",... "<dest>"] (this form is required for paths containing whitespace)
```
>* 可以有多个src，可以使用通配符；
>* dest是一个绝对路径，或者是相对于`WORKDIR`的相对路径；
>* 所有复制出来的文件的UID和GID的值都为0；

###`WORKDIR`，在创建容器时为容器内部设置一个工作目录


###`VOLUME`，创建一个挂载点
该挂载点可被当前容器使用，也可被其他容器使用。
也可以在docker run -v来挂载，VOLUME指令将容器内的目录挂载到宿主机的一个目录上，但是无法指定宿主机上的目录，docker run -v可以指定宿主机上的位置。

###`ONBUILD`，为镜像添加触发器
当创建的镜像被用于其他Dockerfile的基础镜像时触发
**该指令只会继承一次，也就是说只会在子镜像中执行，不会在孙子镜像中执行。
```Dockerfile
[...]
ONBUILD ADD . /app/src
ONBUILD RUN /usr/local/bin/python-build --dir /app/src
[...]
```


#创建私有Registry


#自动创建镜像

















