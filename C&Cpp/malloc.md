# malloc
malloc函数的作用就是从内存中申请分配指定字节大小的内存空间

```c
malloc(4);  // 申请4个字节
malloc(sizeof(int));   // 申请int类型字节数

int *p;p=(int *)malloc(sizeof(int));
```
malloc 函数的返回类型是 void * 类型。void * 表示未确定类型的指针。在 C 和 C++中,void * 类型可以强制转换为任何其他类型的指针。

