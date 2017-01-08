#Tips

##函数

##闭包
一个可以访问外部函数的局部变量的内部函数。

```lua
function counter()          -- 对于要返回内部函数来说，counter是它的外部函数
    local i = 0             -- 外部函数内的局部变量，每次调用counter时的i都是不一样的
    return function ()      -- 返回一个内部函数
        i = i + 1
        return i
    end
end

local c1 = counter()    -- 返回一个闭包函数
print(c1())             -- 1    调用一次返回的闭包函数
print(c1())             -- 2    调用一次返回的闭包函数

local c2 = counter()    -- 返回一个闭包函数
print(c2())             -- 1
print(c1())             -- 3
print(c2())             -- 2
```

> c1，c2是建立在同一个函数，但作用在同一个局部变量的不同实力上的两个不同闭包。



###递归局部函数

```lua
local function fun(num)
    if num == 1 then
        return 1
    else
        return num * fun(num - 1)
    end
end
```
上面的函数内递归调用fun时，此时在函数不知道fun是局部函数，回去查找全局函数。
通过先定义一个局部变量，再将函数赋值给局部变量来实现。

```lua
local fun
fun = function(num)
    if num == 1 then
        return 1
    else
        return num * fun(num - 1)
    end
end
```

###尾调用
尾调用，即在函数内的最后调用另一个函数，调用后不再做其他操作，可以把尾调用理解成是`goto`操作。
在尾调用中，当被调用的函数执行结束时，程序不需要再返回调用者的环境，即不需要在栈中保留关于调用者的信息，需要使用额外的栈。
当被调用者是调用者本身时（即递归），称为`尾递归`。
> 被调用者的参数可以是复杂的表达式，会在调用之前计算出表达式的值。

```lua
-- 尾调用
function f(x)
    return g(x)
end

-- 尾调用，参数是表达式
function f(x)
    return g(x^2+2*x+1)
end

-- 不是尾调用，在调用g后还需要将g(x)的返回值丢弃
function f(x)
    g(x)
    return
end

-- 不是尾调用，调用后还要再做一个加操作
function f(x)
    return g(x) + 1
end

-- 不是尾调用，调用后还要在取一个结果
function f(x)
    return x or g(x)
end

-- 不是尾调用，调用后还要再取一个结果
function f(x)
    return (g(x))
end
```

###迭代器与闭包
支持指针类型的结构，可以用来遍历集合元素。


```lua
-- 简单的table迭代器
function iter(t)
    local i = 0
    local n = table.getn(t)
    return function ()
        i = i + 1
        return i <= n and return t[i] or nil
    end
end

-- 在while中使用迭代器
local t = {1, 2, 3}
local it = iter()
while true do
    local e = it()
    if e == nil then
        break
    end
    print(e)
end

-- 在for范式中使用迭代器
local t = {1, 2, 3}
for e in iter(t) do
    print(e)
end
```

####范式for与迭代器
```lua
for <var-list> in <exp-list> do
    <body>
end
```
var-list是变量名列表，exp-list是表达式，表达式列表通常只有一个。
执行过程：
>* 1、初始化，执行in后的表达式，表达式返回三个值：迭代函数，状态常量，控制变量；
>* 2、将状态常量和控制变量作为参数调用迭代函数；
>* 3、将迭代函数返回的值赋值给变量列表；
>* 4、如果迭代函数返回的第一个值如果为nil时循环结束，否知执行循环体；
>* 5、将表达式返回的状态变量和迭代函数返回的第一个值作为新的控制变量传入调用迭代函数；

```lua
-- 以下两个代码块等价
for v1, ..., vn in explist do
    block
end

do
    local _f, _s, _var = explist
    while true do 
        local var_1, ..., var_n  = _f(_s, _var)
        _var = var_1
        if _var == nil then
            break
        end
        block
    end
end
```

自己实现一个ipairs

```lua
--[[
    i   控制变量
    v   
]]
local function iterator(t, i)
    i = i + 1
    local v = t[i]
    if v then
        return i, v
    end
end

--[[
    iterator    迭代函数    lua库中返回的next
    t           状态变量
    i           控制变量
]]
local function ipairs(t)
    local i = 0
    return iterator, t, i
end


```
