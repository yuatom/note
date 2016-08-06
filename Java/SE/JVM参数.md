# JVM参数
##JVM 参数分类
###标准参数
可通过`java -help`查看。标准参数的功能和输出都是比较稳定，在以后的JVM版本中不会改变；
###X参数
非标准化的参数，在未来的版本中可能改变。这类参数使用时以`-X`开始，可使用`java -X`来查看，但不保证所有的X都会被列出；
###XX参数
同样不是标准化的参数，目前这类参数的数量最多，使用时以`-XX`开始。X参数的功能相对比较稳定，但XX参数某些还在实验当中。
###XX参数的使用
>* 对于布尔类型的参数，我们有”+”或”-“，然后才设置JVM选项的实际名称。例如，-XX:+<name>用于激活<name>选项，而-XX:-<name>用于注销选项。
>* 对于需要非布尔值的参数，如string或者integer，我们先写参数的名称，后面加上”=”，最后赋值。例如，  -XX:<name>=<value>给<name>赋值<value>。

##-server and -client
作为客户端程序或服务端程序启动

##-version and -showversion
-version，打印虚拟机版本后终止JVM；
-showversion，输出相同的信息，但是-showversion紧接着会处理并执行Java程序。

```shell
$ java -version
java version "1.6.0_24"
Java(TM) SE Runtime Environment (build 1.6.0_24-b07)
Java HotSpot(TM) Client VM (build 19.1-b02, mixed mode, sharing)
```

##-Xint, -Xcomp, 和 -Xmixed
-Xint标记会强制JVM执行所有的字节码，当然这会降低运行速度，通常低10倍或更多；
-Xcomp参数与它（-Xint）正好相反，JVM在第一次使用时会把所有的字节码编译成本地代码，从而带来最大程度的优化。因为这样完全绕开了缓慢的解释器，所以看起来性能不错。但是很多应用使用这个参数会有性能损失（比-Xint损失得少），因为使用该选项时没有让JVM启用JIT编译器的全部功能，其中包括部分优化行为。比如；
混合模式，默认的模式。

```shell
$ java -server -showversion Benchmark
java version "1.6.0_24"
Java(TM) SE Runtime Environment (build 1.6.0_24-b07)
Java HotSpot(TM) Server VM (build 19.1-b02, mixed mode)
 
Average time: 0.856449 seconds
```

```shell
$ java -server -showversion -Xcomp Benchmark
java version "1.6.0_24"
Java(TM) SE Runtime Environment (build 1.6.0_24-b07)
Java HotSpot(TM) Server VM (build 19.1-b02, compiled mode)
 
Average time: 0.950892 seconds
```

```shell
$ java -server -showversion -Xint Benchmark
java version "1.6.0_24"
Java(TM) SE Runtime Environment (build 1.6.0_24-b07)
Java HotSpot(TM) Server VM (build 19.1-b02, interpreted mode)
 
Average time: 7.622285 seconds
```

##-XX:+UnlockExperimentalVMOptions
解锁参数，有些时候当设置一个特定的JVM参数时，JVM会在输出“Unrecognized VM option”后终止。如果输入的参数拼写正确但是没有被识别，需要设置-XX:+UnlockExperimentalVMOptions 来解锁参数。

##-XX:+PrintCompilation和-XX:+CITime
-XX:+PrintCompilation打印字节码转化为本地代码的变异过程，当有一个方法被编译，就会输出一行包含顺序号（唯一的编译任务ID）和已编译方法的名称和大小的信息。

```shell
$ java -server -XX:+PrintCompilation Benchmark
  1       java.lang.String::hashCode (64 bytes)
  2       java.lang.AbstractStringBuilder::stringSizeOfInt (21 bytes)
  3       java.lang.Integer::getChars (131 bytes)
  4       java.lang.Object::<init> (1 bytes)
---   n   java.lang.System::arraycopy (static)
  5       java.util.HashMap::indexFor (6 bytes)
  6       java.lang.Math::min (11 bytes)
  7       java.lang.String::getChars (66 bytes)
  8       java.lang.AbstractStringBuilder::append (60 bytes)
  9       java.lang.String::<init> (72 bytes)
 10       java.util.Arrays::copyOfRange (63 bytes)
 11       java.lang.StringBuilder::append (8 bytes)
 12       java.lang.AbstractStringBuilder::<init> (12 bytes)
 13       java.lang.StringBuilder::toString (17 bytes)
 14       java.lang.StringBuilder::<init> (18 bytes)
 15       java.lang.StringBuilder::append (8 bytes)
[...]
 29       java.util.regex.Matcher::reset (83 bytes)
```
 
-XX:+CITime可以在JVM关闭时得到各种编译的统计信息。

```shell
$ java -server -XX:+CITime Benchmark
[...]
Accumulated compiler times (for compiled methods only)
------------------------------------------------
  Total compilation time   :  0.178 s
    Standard compilation   :  0.129 s, Average : 0.004
    On stack replacement   :  0.049 s, Average : 0.024
[...]
```
对于-server和-client两个参数执行以上两个参数，输出的内容会不一样。因为作为服务端VM和客户端VM分别要执行优化不一样。

##-XX:+LogCompilation and -XX:+PrintOptoAssembly
在使用` -XX:+PrintCompilation`不能提供足够详细的情况下，`-XX:+LogCompilation`可把扩展的编译输出到`history.log`文件中。
XX:+PrintOptoAssembly，由编译器线程生成的本地代码被输出并写到“hotspot.log”文件中。

#参数打印相关
##-XX:+PrintFlagsFinal、 -XX:+PrintFlagsInitial、 -XX:+PrintCommandLineFlags
###PrintFlagsFinal
显示XX参数当前的值。第一列表示参数的数据类型，第二列是名称，第四列为值，第五列是参数的类别。第三列”=”表示第四列是参数的默认值，而”:=” 表明了参数被用户或者JVM赋值了。
###PrintFlagsInitial
显示参数的默认值，相当于-XX:+PrintFlagsFinal的结果中显示第三列为“=”的值。
###PrintCommandLineFlags
印出那些已经被用户或者JVM设置过的详细的XX参数的名称和值。相当于列举出 -XX:+PrintFlagsFinal的结果中第三列有":="的参数。

```shell
$ java -client -XX:+PrintFlagsFinal Benchmark
[Global flags]
uintx AdaptivePermSizeWeight               = 20               {product}
uintx AdaptiveSizeDecrementScaleFactor     = 4                {product}
uintx AdaptiveSizeMajorGCDecayTimeScale    = 10               {product}
uintx AdaptiveSizePausePolicy              = 0                {product}[...]
uintx YoungGenerationSizeSupplementDecay   = 8                {product}
uintx YoungPLABSize                        = 4096             {product}
 bool ZeroTLAB                             = false            {product}
 intx hashCode                             = 0                {product}
```

>* 可用-XX:+UnlockExperimentalVMOptions 和-XX:+UnlockDiagnosticVMOptions来解锁任何额外的隐藏参数。
>* 建议 –XX:+PrintCommandLineFlags 这个参数应该总是设置在JVM启动的配置项里。因为你从不知道你什么时候会需要这些信息。

#内存空间配置相关
##-Xms and -Xmx (or: -XX:InitialHeapSize and -XX:MaxHeapSize)
指定JVM内存的初始值（最小值）和最大值，单位默认是byte，可使用K/M/G等其他单位。然而JVM可以在运行时动态调整内存大小，因此有时看到的堆内存的大小会小于设定的初始值。

##-XX:+HeapDumpOnOutOfMemoryError and -XX:HeapDumpPath
当程序出现内存溢出的时候，这个参数可以让JVM在发生内存溢出时自动的生成堆内存快照。默认情况下，堆内存快照会保存在JVM的启动目录下名为java_pid<pid>.hprof 的文件里（在这里<pid>就是JVM进程的进程号）。也可以通过设置-XX:HeapDumpPath=<path>来改变默认的堆内存快照生成路径，<path>可以是相对或者绝对路径。

##XX:OnOutOfMemoryError
在程序出现内存溢出的时候，可以使用该参数指定某些命令，参数可以接受一串指令和它们的参数。

```shell
$ java -XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=/tmp/heapdump.hprof -XX:OnOutOfMemoryError ="sh ~/cleanup.sh" MyApp
```
上面命令在程序出现内存溢出的时候执行当前目录下的脚本`cleanup.sh`。

## -XX:PermSize and -XX:MaxPermSize
设置永久代的初始大小和最大值。
永久代在堆内存中是一块独立的区域，它包含了所有JVM加载的类的对象表示。
**这里的永久代的大小并不会包括在使用`-XX:MaxHeapSize`设置的内存中。**

##-XX:InitialCodeCacheSize and -XX:ReservedCodeCacheSize
代码缓存大小的初始值和最大值。
JVM有一块内存区域用来存储已编译的方法的本地代码。当该块内存被占满时，JVM会抛出警告，并且切换到`interpreted-only`模式：JIT编译器被停用，字节码将不再会被编译成机器码。

##-XX:+UseCodeCacheFlushing
这个参数可以使代码缓存被填满的时候让JVM放弃编译一些代码，可以避免切换到`interpreted-only`模式。

#新生代垃圾回收相关
##-XX:NewSize and -XX:MaxNewSize
新生代初始值和最大值。
新生代只是堆的一部分，新生代设置的越大，老年代区域就会减少。一般不允许新生代比老年代还大，因为如果GC的时候所有对象都晋升到老年代会发生OOM错误。

##-XX:NewRatio
新生代和老年代的相对大小。这个设置可以使新生代的大小随整个堆内存大小动态变化。
-XX:NewRatio=3 =》 老年代/新生代为3/1。
如果同时设置`-XX:NewSize`和`-XX:MaxNewSize`，按照比例设置的情况下新生代会超过MaxNewSize，则MaxNewSize会生效。

##-XX:SurvivorRatio
新生代内部的Eden和幸存区的大小比例。
XX:SurvivorRatio=10 表示伊甸园区(Eden)是 幸存区To 大小的10倍(也是幸存区From的10倍)。
如果Eden区太小，就会很快耗尽，增加新生代GC的次数；
如果Eden区太大，一次GC后无法全部保存到幸存区中，就会有部分转移到老年代。

##-XX:+PrintTenuringDistribution
打印幸存区中的年龄分布

```shell
Desired survivor size 75497472 bytes, new threshold 15 (max 15)
- age 1: 19321624 bytes, 19321624 total
- age 2: 79376 bytes, 19401000 total
- age 3: 2904256 bytes, 22305256 total
```
第一行表示To Survivor大小为75497472字节及晋升到老年代需要经过GC次数是15次。
上面的输出表示警告一次GC后的大小是19321624，两次后是79376。
每行结尾显示直到本年龄的全部对象大小。
假设下一次的GC输出为

```shell
Desired survivor size 75497472 bytes, new threshold 2 (max 15)
- age 1: 68407384 bytes, 68407384 total
- age 2: 12494576 bytes, 80901960 total
- age 3: 79376 bytes, 80981336 total
- age 4: 2904256 bytes, 83885592 total
```
该次的3和4跟上一次的2和3大小一致，表示上一次的2和3还保存在幸存区中。
该次GC中，幸存区占用总大小为83885592，大于设置的75497472，因此老年代的阀值被JVM下调到2。下次GC时一部分对象会强制离开幸存区，这些对象可能会被回收(如果他们刚好死亡)或移动到老年代。

##？-XX:InitialTenuringThreshold, -XX:MaxTenuringThreshold and -XX:TargetSurvivorRatio
老年代的初始阀值、最大值以及幸存区空间目标使用率（默认50，最大90）。
-XX:TargetSurvivorRatio=90表示幸存区空间目标使用率为90%，超过这个值时会清除幸存区的对象。

##-XX:+NeverTenure and -XX:+AlwaysTenure
新生代对象永远不会晋升到老年代；
所有对象在第一次GC后都转移到老年代。

#吞吐量相关
##-XX:+UseSerialGC
启用串行垃圾收集器。
无论年轻代还是年老代都将只有一个线程执行垃圾收集。 该标志被推荐用于只有单个可用处理器核心的JVM。

##XX:+UseParallelGC
启用多线程并行新生代垃圾收集。

##-XX:+UseParallelOldGC
启用多线程并行新生代和老年代垃圾收集。

##-XX:ParallelGCThreads
指定并行垃圾收集的线程数量。
-XX:ParallelGCThreads=6表示每次并行垃圾收集将有6个线程执行。
默认的情况下，按availableProcessors()方法的返回值N，如果N<=8，使用N个垃圾回收线程，如果N>8个可用处理器，使用3+5N/8。

##-XX:-UseAdaptiveSizePolicy
停用UseAdaptiveSizePolicy。
默认情况下开启UseAdaptiveSizePolicy，能像动态调整堆大小那样动态调整垃圾收集器。

##-XX:GCTimeRatio
-XX:GCTimeRatio=N指定目标应用程序线程的执行时间(与总的程序执行时间)达到N/(N+1)的目标比值。GC线程占其余的1/N。

##-XX:MaxGCPauseMillis
JVM最大暂停时间的目标值(以毫秒为单位)。
如果最大暂停时间和最小吞吐量同时设置了目标值，实现最大暂停时间目标具有更高的优先级。

#CMS回收相关
##-XX：+UseConcMarkSweepGC
启用CMS收集器，默认是使用并行；
##-XX：UseParNewGC
新生代使用多线程并行，默认随UseConcMarkSweepGC开启；
##-XX：+CMSConcurrentMTEnabled
开启多线程，默认是开启的；
##-XX：ConcGCThreads
CMS并发的线程数；
##-XX:CMSInitiatingOccupancyFraction=<value>
触发CMS收集的老年代使用率，当老年代中达到这个值时，CMS收集器会被触发；
##-XX：+UseCMSInitiatingOccupancyOnly
只根据老年代使用率来触发CMS，不基于JVM运行收集的数据，大多数情况下JVM更懂得何时触发，除非测试情况下，不建议使用该选项；
##-XX:+CMSClassUnloadingEnabled
对永久代也进行垃圾回收，CMS收集器默认是不对永久代进行回收；
##-XX:+CMSIncrementalMode
开机CMS收集器的增量模式；
##-XX:+ExplicitGCInvokesConcurrent
无论什么时候调用系统GC，都执行CMS GC，而不是Full GC；
##-XX:+ExplicitGCInvokesConcurrentAndUnloadsClasses
保证当有系统GC调用时，永久代也被包括进CMS垃圾回收的范围内；
##-XX:+DisableExplicitGC
完全忽略系统的GC调用(不管使用的收集器是什么类型)。






