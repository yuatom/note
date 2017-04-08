# basic.md

## 1. Date Type 数据类型

* 基本类型；
* 枚举类型；
* 引用类型；
* 空类型；

### 1.1 基本数据类型

* int：整型，不可保存小数；
* float：浮点，可保存小数，保留6位小数；
* double：双精度，可保存小数，保留10位小数；


| 类型 | 字节数（16位CPU） | 范围|
|--|--|--|
|char|1|[-2^7-1, 2^7-1]|
|int|2|[-2^15-1, 2^15-1]|
|float|4||
|double|8||
|long double|10||
|long int|4||
|short int|2||
|unsigned short int|2||
|signed short int|2||
|long long int|8||
|signed long int|4||
|unsigned long int|4||
|unsinged long long int|8||
> 可使用sizeof函数来看某一类型所占的字节数。

```c
#include <stdio.h>
#include <limits.h>

int main()
{
    int a;
    char b;
    float c;
    double d;
    printf("Storage size for int data type:%d \n",sizeof(a));
    printf("Storage size for char data type:%d \n",sizeof(b));
    printf("Storage size for float data type:%d \n",sizeof(c));
    printf("Storage size for double data type:%d\n",sizeof(d));
    return 0;
}
```

### 1.2 枚举数据类型

枚举数据类型是由多个整型常量组成的一个列表。默认地，第一个常量的值为0，而后每个常量递增1。
可通过改变第一个常量的值，同样而后每个常量的值也会在此基础上递增1。

```c
enum month {
    Jan,    // 0
    Feb,    // 1
    Mar     // 2
};

// 指定第一个常量的值
enum month {
    Jan = 1,    // 1
    Feb,        // 2
    Mar         // 3
};

// 通过define来定义枚举中常量的值
#define Jan 20;
#define Feb 21;
#define Mar 22;

enum month {
    Jan,    // 20
    Feb,    // 21
    Mar     // 22
};
```

## 2. constant 常量

```c
const data_type var;
const data_type *var;
```
常量的值是一个固定的值，也称作字面量。常量的值一旦定义就不能修改。
常量的类型：
* 整型常量，至少包含一个数字，不能包含小数点，可可正，[-2^15, 2^15-1]
* 浮点数常量，至少包含一个数字，必须包含小数点，可正可负；
* 十六进制/八进制常量；
* 字符常量，使用单引号定义，字母/数字/符号，长度至多为1；
* 字符串常量，使用双引号定义；
* 转义字符；

|转义字符|含义|
|--|--|
|\b|退格 backspace|
|\f|换页 form feed|
|\n|换行 new line|
|\r|回车 carriage return|
|\t|制表符 horizontal tab|
|\\"|双引号 double quote|
|\\'|单引号 single quote|
|\\|斜杠 backslash|
|\v|垂直制表符 vertical tab|
|\a|响铃符，输出该值时会发出声音，alert or bell|
|\\?|问号 question mark|
|\N|八进制常量 octal constant|
|\XN|十六进制常量 hexadecimal constant|


### 例子
#### 通过定义常量

```c
#include <stdio.h>

void main()
{
    const int height = 100;
    const float number = 3.14;
    const char letter = 'A';
    const char letter_sequence[10] = "ABC";
    const char backslash_char = '\?';
    printf("value of height :%d \n", height );
    printf("value of number : %f \n", number );
    printf("value of letter : %c \n", letter );
    printf("value of letter_sequence : %s \n", letter_sequence);
    printf("value of backslash_char : %c \n", backslash_char);
}
```

#### 通过define
```c
#include <stdio.h>
#define height 100
#define number 3.14
#define letter 'A'
#define letter_sequence "ABC"
#define backslash_char '\?'

void main()
{
    printf("value of height : %d \n", height );
    printf("value of number : %f \n", number );
    printf("value of letter : %c \n", letter );
    printf("value of letter_sequence : %s \n",letter_sequence);
    printf("value of backslash_char : %c \n",backslash_char);
}
```

## 3. Variable 变量

```c
data_type var;          // 声明
data_type var = val;    // 初始化
```

* 内存中的一块命名的位置（named location），其值在程序中可变；
* 以字母或下划线开头，可包含字母/数字/下划线，区分大小写；
* 变量在使用前必须声明，在声明时不会为变量分配内存空间，内存空间的分配发生在变量定义的时候；

### 变量类型

* 本地变量：在函数中声明，且仅在函数中可见；
* 全局变量：在main函数外声明，在整个程序中均可见；
* 环境变量：在所有的C程序中都可见，不需要用户去定义，可使用`setent`，`getenv`，`putenv`等函数来存取环境变量


## 4. Operator and Expressions 操作和表达式 

* 数学操作：`+` / `-` / `*` / `/` / `%`；
* 赋值操作：`=` / `+=` / `-=` / `*=` / `/=` / `%=` / `&=` / `^=`；
* 关系操作：`>` / `<` / `>=` / `<=` / `==` / `!=`；
* 逻辑操作：`&&` / `||` / `!`；
* 位操作：`&` / `|` / `~` / `^` / `<<` / `>>`；
* 自增/自减：`i++` / `++i` / `i--` / `--i`；
* 取值/址：`*` / `&`;

## 5. Control Statements 控制语句

* 条件控制：if () {} / if () {} else {} / if () {} else if () {}；
* 循环控制：for / while / do while；
* 分支控制：switch / goto；