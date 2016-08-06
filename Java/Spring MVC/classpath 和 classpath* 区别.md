# classpath 和 classpath* 区别
classpath：只会到你指定的class路径中查找找文件;
classpath*：不仅包含class路径，还包括jar文件中(class路径)进行查找.

举个简单的例子，在我的web.xml中是这么定义的：classpath*:META-INF/spring/application-context.xml
那么在META-INF/spring这个文件夹底下的所有application-context.xml都会被加载到上下文中，这些包括META-INF/spring文件夹底下的 application-context.xml，META-INF/spring的子文件夹的application-context.xml以及jar中的application-context.xml。

如果我在web.xml中定义的是：classpath:META-INF/spring/application-context.xml
那么只有META-INF/spring底下的application-context.xml会被加载到上下文中。





