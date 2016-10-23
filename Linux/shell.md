shell
test
-z
-n
-e
-f
-d
-a
-o
!

[]中括号判断

shift

if []; then elif []; if && || = ==

case  $var in
  "" )
    code
  ;;
  "" )
    code
  ;;
  * )
    code
    ;;
esac 

echo
date
declare 


读取参数的方式
$1 $2 $3...

$# ：代表后接的参数『个数』，以上表为例这里显示为『 4 』；
$@ ：代表『 "$1" "$2" "$3" "$4" 』之意，每个变量是独立的(用双引号括起来)；
$* ：代表『 "$1c$2c$3c$4" 』，其中 c 为分隔字节，默认为空白键， 所以本例中代表『 "$1 $2 $3 $4" 』之意。

read




函数定义
function  fun(){
    # $1 $2...
}

函数调用，传参
func a c

满足时运行
while [ condition ]
do
     code
done

满足时终止
util [condition]
do
   code
done

var在循环中的值依次为con1 con2 con3
for var in con1 con2 con3
do
    code
done

for ((初始值; 限制值; 运行步阶))
do
    code
done

for (( i=1; i<=$nu; i=i+1 ))
do
	s=$(($s+$i))
done

seq   seq 1 100
cut