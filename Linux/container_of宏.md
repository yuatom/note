# containerof宏
```c
// 传入ptr指针，已知该指针是某个类型type的一个member，返回包含ptr指针的type数据
#define container_of(ptr, type, member) ({                  \
    const typeof( ((type *)0)->member ) *__mptr = (ptr);    \
    (type *) ( (char *)__mptr - offsetof(type, member) );   \
})
```
1.`const typeof( ((type *)0)->member ) *__mptr = (ptr)`：定义一个与ptr类型相同的临时指针变量来保存ptr的值：
1.1.`(type *)0`：type类型的数据（运用了0地址）；
1.2.`((type *)0)->member )`：type的member成员；
1.3.`typeof( ((type *)0)->member ) *__mptr`：typeof，由一个变量名来获取其类型，用type的成员member的类型来定义`*__mptr`；
2.`(type *) ( (char *)__mptr - offsetof(type, member) )`：根据`*__mptr`的值和type这个类型中member的指针偏移量，来计算出ptr所属的type结构数据的首地址；
2.1.`offsetof(type, member)`：type结构体中member成员和结构体首地址的偏移量，这里是字节单位；
2.2.`(char *)__mptr`：将*__mptr指针转换为字节单位长度的；
2.3.`( (char *)__mptr - offsetof(type, member) )`：ptr的值减去type结构体中member成员的地址偏移，能得出包含ptr的type结构体的首地址；
2.4.`(type *) ( (char *)__mptr - offsetof(type, member) )`：最后，转换类型。

