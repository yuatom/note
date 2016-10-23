


jobs [-lrs]
fg jobsnumber
fg -
在命令后加&，可将命令丢到bash的背景执行，之后可以在该bash中执行其他命令，这里的背景仅是指不会影响当前bash其他操作的背景，而不是系统的背景。
如果这个命令启动的不是守护进程，那当退出当前的bash时，该bash背景的任务也会被退出。




nohup [指令与参数] [&]，执行与终端机无关的任务，不支持/bin/bash内置指令，&表示将任务放到后台去执行
该命令可以在bash用exit退出后继续在后台运行
执行程序的标准输出会保存到该文件~/nohup.out
nohup command > myout.file 2>&1 &  修改输出。
