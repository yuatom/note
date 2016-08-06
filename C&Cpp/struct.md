# struct
##1.定义
```c
// 1.简单定义
struct student{
    char name[20];
    long num;
}

// 2.定义后声明一个变量
struct student{
    char name[20];
    long num;
} Jack;
// 以上相当于
struct student{
    char name[20];
    long num;
};
struct student Jack;// 结构体变量的声明要使用struct关键字，可以使用typedef将结构体定义一种新类型

// 定义类型
typedef struct student{
    char name[20];
    long num;
};
// 声明
student Jack;

// 3.结构体定义后只使用一次，可以使用类似匿名的方式
struct {
    char name[20];
    long num;
} Jack;
```
##2.初始化

```c
struct student{
    char name[20];
    long num;
};

// 传入
struct student Jack = {'Jack', 111};

// 成员变量赋值
struct student Jack;
Jack.num = 111;
// 成员数组会比较麻烦
Jack.name[0] = 'J';
Jack.name[1] = 'a';
```

##3.指针

```c
struct student{
    char name[20];
    long num;
};

// 定义一个指针
struct student *jack;
jack = malloc(sizeof(struct student));  // 为指针分配变量
jack->num = 111;    // 指针变量赋值

```

