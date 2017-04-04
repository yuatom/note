# configure执行过程
##执行./auto/options文件，判断执行configure的参数

##执行./auto/init文件，初始化configure命令后续将产生的文件路径，一般在./objs路径

##执行./auto/sources文件，分析Nginx源码，构造Makefile文件

##创建编译过程中所有要生成的文件路径，该路径由--builddir参数指定

##准备创建必要的编译文件，如ngx_auto_headers.h、autoconf.err等

##向objs/gx_auto_headers.h写入命令行带的参数

##判断DEBUG标志

##检查操作系统参数是否支持后续编译

##输出操作系统信息

##执行./auto/cc/conf检查并设置GCC编译器

##执行./auto/headers定义非Windows系统的一些必要头文件

##执行./auto/os/conf定义当前操作系统相关的方法并检查环境是否支持

##执行./auto/unix定义UNIX系统中通用的头文件和系统调用

##执行./auto/modules，读取模块数组，生成ngx_modules.c文件，该文件会被编译进Nginx

### 加载模块目录配置

一个自定义的模块源码会放在某个目录下，并且需要在这个目录中添加config文件。config文件需要包含以下3个变量：
* ngx\_addon_name: configure执行时调用，设置为模块名称。
* HTTP\_MODULES: 保存所有的HTTP模块名称，模块直接用空格隔开。注意不要覆盖原有的HTTP\_MODULES变量，一般为`"$HTTP\_MODULES ngx\_http\_my\_module"
* NGX\_ADDON\_SRC: 指定新增模块的源代码目录，多个目录之间用空格隔开。注意不要覆盖原有的变量，同时该变量的定义中可以使用`$ngx_addon_dir`变量，该值等于configure时的`--add-module=PATH`中的PATH参数。

通过在configure时添加`--add-module=PATH`选项来指定模块的目录。执行./auto/options时会将`--add-module`选项的值添加到`NGX_ADDONS`变量中。执行./auto/modules时根据`NGX_ADDONS`遍历需要编译的模块的目录，并执行这些目录中的config文件。

```sh

if test -n "$NGX_ADDONS"; then

    echo configuring additional modules

    for ngx_addon_dir in $NGX_ADDONS

    do

        echo "adding module in $ngx_addon_dir"

        if test -f $ngx_addon_dir/config; then

            . $ngx_addon_dir/config

            echo " + $ngx_addon_name wad configured"

        else
            echo "$0: error: no $ngx_addon_dir/config was found"

            exit 1

        fi

    done

fi
```

### 生成ngx_module.c文件
首先会将要编译的模块名添加到`modules`变量，随后遍历该变量，将模块添加到module.c中`ngx_module_t *ngx_modules[]`数组，Nginx在初始化时，会根据该数据来确定该用哪一个模块来处理。

```sh
# 定义modules变量
modules="$CORE_MODULES $EVENT_MODULES"

if [ $USE_OPENSLL = YES ]; then
    modules="$modules $OPENSSL_MODULE"
    CORE_DEPS="$CORE_DEPS $OPENSSL_DEPS"
    CORE_SRCS="$CORE_SRCS $OPENSSL_SRCS"
fi

if [ $HTPP = YES ]; then
    modules="$modules $HTTP_MODULES $HTTP_FILRTER_MOUDLE \
                    $HTPP_HEADERS_FILTER_MODULE \
                    $HTTP_AUX_FILTER_MODULE \
                    $HTTP_COPY_FILTER_MODULE \
                    $HTTP_RANGE_BODY_FILTER_MODULE \
                    $HTTP_NOT_MODIFIED_FILTER_MODULE"
    NGX_ADDONS_DEPS="$NGX_ADDONS_DEPS \$(HTTP_DEPS)"
fi
```

开始将变量的值写进ngx_module.c文件

```sh
# 将输入输出到$NGX_MODULE_C变量所指定的路径中，遇到END时结束
cat << END                                              > $NGX_MODULE_C

#include <ngx_config.h>
#include <ngx_core.h>

$NGX_PRAGMA

END

for mod in $modules
do 
    echo "extern ngx_module_t   $mod;"
done

echo                                                    >> $NGX_MODULE_C
echo 'ngx_module_t *ngx_modules[] = { '                 >> $NGX_MODULE_C

for mod in $modules
do
    echo "      &$mod,"                                 >> $NGX_MODULE_C
done

cat << END                                              >> $NGX_MODULE_C
    NULL
};

END

```

##执行./auto/lib/conf检查第三方库

##处理Nginx安装后的路径

##处理Nginx安装后conf文件的路径

##处理Nginx安装后，二进制文件、pid、lock等其他文件的路径

##执行./auto/make创建编译时使用的objs/Makefile文件

```shell
# 转换第三方模块的文件路径以及文件的扩展名，并生成编译的命令写进Makefile中
if test -n "$NGX_ADDON_SRCS"; then

    ngx_cc="\$(CC) $ngx_compile_opt \$(CFLAGS) $ngx_use_pch \$(ALL_INCS)"

    for ngx_src in $NGX_ADDON_SRCS
    do

        ngx_obj="addon/`basename \`dirname $ngx_src\``"
            
        ngx_obj=`echo $ngx_obj/\`basename $ngx_src\` \
            sed -e "s/\//$ngx_regex_dirsep/g"`

        ngx_obj=`echo $ngx_obj \
            | sed -e
            "s#\(.*\.\)cpp\\$#$ngx_objs_dir/1$ngx_objext#g" \
            "s#\(.*\.\)cc\\$#$ngx_objs_dir/1$ngx_objext#g" \
            "s#\(.*\.\)c\\$#$ngx_objs_dir/1$ngx_objext#g" \
            "s#\(.*\.\)S\\$#$ngx_objs_dir/1$ngx_objext#g"`

        ngx_src=`echo $ngx_src | sed -e "s/\\/$ngx_regex_dirsep/g"`

        cat << END                                               >> $NGX_MAKEFILE

$ngx_obj: \$(ADDON_DEPS)$ngx_cont$ngx_src
    $ngx_cc$ngx_tab$ngx_objout$ngx_obj$ngx_tab$ngx_src$NGX_AUX

END
    done
fi
```


```shell
# 将模块的目标文件设置到ngx_obj变量中，并生成Makefile文件中的链接代码

for ngx_src in $NGX_ADDON_SRCS
do
    ngx_obj="addon/`basename \`dirname $ngx_src\``"

    test -d $NGX_OBJS/$ngx_obj || mkdir -p $NGC_OBJS/$ngx_obj

    ngx_obj=`echo $ngx_obj/\`basename $ngx_src\`    \
        | sed -e "s/\//$ngx_regex_dirsep/g"`

    ngx_all_srcs="$ngx_all_srcs $ngx_obj"
done

...

cat << END                                                      >> $NGX_MAKEFILE

$NGX_OBJS${ngx_dirsep}nginx${ngx_binext}:
    $ngx_deps$ngx_spacer \${LINK}
    ${ngx_long_start}${ngx_binout}$NGX_OBJS${ngx_dirsep}nginx$ngx_long_cont$ngx_objs$ngx_libs$ngx_link
    $ngx_rcc
${ngx_long_end}
END
```

ADDON_DEPS = \$(CORE_DEPS) $NGX_ADDON_DEPS

##执行./auto/lib/make，为objs/Makefile加入需要的第三库

##执行./auto/install，为objs/Makefile加入install功能

##执行./auto/stubs

##在ngx_auto_config.h中指定Nginx服务的用户和用户组

##执行./auto/summary


