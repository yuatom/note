# composer.json

全局参数

下列参数可与每一个命令结合使用：

--verbose (-v): 增加反馈信息的详细度。
-v 表示正常输出。
-vv 表示更详细的输出。
-vvv 则是为了 debug。
--help (-h): 显示帮助信息。
--quiet (-q): 禁止输出任何信息。
--no-interaction (-n): 不要询问任何交互问题。
--working-dir (-d): 如果指定的话，使用给定的目录作为工作目录。
--profile: 显示时间和内存使用信息。
--ansi: 强制 ANSI 输出。
--no-ansi: 关闭 ANSI 输出。
--version (-V): 显示当前应用程序的版本信息。

name

version

type
library: 这是默认类型，它会简单的将文件复制到 vendor 目录。
project: 这表示当前包是一个项目，而不是一个库。例：框架应用程序 Symfony standard edition，内容管理系统 SilverStripe installer 或者完全成熟的分布式应用程序。使用 IDE 创建一个新的工作区时，这可以为其提供项目列表的初始化。
metapackage: 当一个空的包，包含依赖并且需要触发依赖的安装，这将不会对系统写入额外的文件。因此这种安装类型并不需要一个 dist 或 source。
composer-plugin: 一个安装类型为 composer-plugin 的包，它有一个自定义安装类型，可以为其它包提供一个 installler。详细请查看 自定义安装类型。

autoload


create-project
创建项目-参数
--repository-url: 提供一个自定义的储存库来搜索包，这将被用来代替 packagist.org。可以是一个指向 composer 资源库的 HTTP URL，或者是指向某个 packages.json 文件的本地路径。
--stability (-s): 资源包的最低稳定版本，默认为 stable。
--prefer-source: 当有可用的包时，从 source 安装。
--prefer-dist: 当有可用的包时，从 dist 安装。
--dev: 安装 require-dev 字段中列出的包。
--no-install: 禁止安装包的依赖。
--no-plugins: 禁用 plugins。
--no-scripts: 禁止在根资源包中定义的脚本执行。
--no-progress: 移除进度信息，这可以避免一些不处理换行的终端或脚本出现混乱的显示。
--keep-vcs: 创建时跳过缺失的 VCS 。如果你在非交互模式下运行创建命令，这将是非常有用的。


