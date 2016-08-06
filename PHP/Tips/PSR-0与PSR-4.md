# PSR-0与PSR-4
PSR-0规范

[1]命名空间必须与绝对路径一致

[2]类名首字母必须大写

[3]除去入口文件外，其他“.php”必须只有一个类

[4]php类文件必须自动载入，不采用include等

[5]单一入口


1.在composer中定义的NS，psr4必须以\结尾否则会抛出异常，psr0则不要求

2.psr0里面最后一个\之后的类名中，如果有下划线，则会转换成路径分隔符，如Name_Space_Test会转换成Name\Space\Test.php。在psr4中下划线不存在实际意义

3.psr0有更深的目录结构，比如定义了NS为 Foo\Bar=>vendor\foo\bar\src，
use Foo\Bar\Tool\Request调用NS。
如果以psr0方式加载，实际的目录为vendor\foo\bar\src\Foo\Bar\Tool\Request.php
如果以psr4方式加载，实际目录为vendor\foo\bar\src\Tool\Request.php

