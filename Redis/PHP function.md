# PHP function
##DB
>* connect(string host, int port);
>* select(int dbIndex);选择数据库
>* move(string key, int destinationDBIndex);将key移动到目标数据库
>* expireAt(string key, int timestamp);
>* expire/setTimeout(string key, int timeToLive);

```php
$redis = new Redis();
$redis->connect('127.0.0.1', 6379);
$redis->set("key1","value1");
$redis->set("key2",2);
var_dump($redis->get("key2"));  //string(1) "2"
var_dump($redis->getMultiple(["key1","key2"])); //array(2) {[0]=> string(6) "value1" [1]=> string(1) "2" }
```


##Key
>* set(string key, value);
>* get(string key);
>* delete(string key);
>* setnx(string key, value);
>* exists(string key);
>* incr(string key);
>* decr(string key);
>* mSet(array("key"=>value...));
>* mGet/getMultiple(array keysArray);
>* rename/renameKey(string oldKey, string newKey);
>* renameNx(string oldKey, string newKey);已存在的话就不替换
>* keys/getKeys(string keyPatterm);
>* migrate(string targetHost, int port, string key, int db, int timeout, boolean copyFlag, boolean replaceFlag);  // 将一个key迁移到其他数据库实例
>* scan(Long iterator, string pattern, int countPerIteration);  // 迭代出库中所有的key，iterator必须是一个变量，初始化为null，每一次迭代都会改变其值

```php
// migrate
$redis->migrate('backup', 6379, 'foo', 0, 3600);
$redis->migrate('backup', 6379, 'foo', 0, 3600, true, true); /* copy and replace */
$redis->migrate('backup', 6379, 'foo', 0, 3600, false, true); /* just REPLACE flag */

$redis->set("key1","value1");
$redis->set("key2",2);
var_dump($redis->get("key2"));  // string(1) "2"
var_dump($redis->delete("key2"));   // int(1)
var_dump($redis->get("key2"));  // bool(false)

// rename
$redis->set("key1","value1");
$redis->set("key2",2);
var_dump($redis->get("key2"));  // string(1) "2"
var_dump($redis->get("key3"));  // bool(false)
var_dump($redis->rename("key2","key3"));// bool(true)
var_dump($redis->get("key2"));  // bool(false)
var_dump($redis->get("key3"));  // string(1) "2"
```

##String 
>* oldValue getSet(string key, value);
>* append(string key, string value);
>* int strlen(string key);
>* setRange(string key, int index, string value); // 将value覆盖到key原来值的index后面的字符串
>* getRange(string key, int start, int end);    // 获取指定范围字符串
>* strLen(string key);  // 返回字符串的长度

##Hash
>* hSet(string key, string field, value);  // 设置Hash的一个域
>* value hGet(string key, string field);   // 获取Hash的一个域
>* int hLen(string key);   // 获取Hash的域的个数
>* hDel(string key, string field); // 删除Hash的一个域
>* hKeys(string key);  // 获取一个Hash的所有域
>* hVals(string key);  // 获取一个Hash的所有值
>* hGetAll(string key);    // 获取一个Hash的所有域和值
>* hExists(string key, string field);  // 判断域在Hash中是否存在
>* hIncrBy(string key, string field, int increment);   // 将Hash中某个域增加increment
>* hMset(string key, array(field=>value...);   // 批量设置Hash的域的值
>* hMGet(string key, array(string field...);   // 批量获取Hash的域的值

```php
// hMset hMget
var_dump($redis->hMset("hashKey",array("name"=>"atom","gender"=>"male")));  // bool(true)
var_dump($redis->hMget("hashKey",array("name","gender")));  // array(2) {["name"]=> string(4) "atom" ["gender"]=> string(4) "male"}

// hIncrBy
$redis->hSet("hashKey","num",2);
$redis->hSet("hashKey","string","test");
var_dump($redis->hGet("hashKey","num"));    // string(1) "2"
var_dump($redis->hIncrBy("hashKey","num",1));   // int(3)
var_dump($redis->hGet("hashKey","num"));    // string(1) "3"
```

##List
>* lPush(string key, value);   // 从头部添加元素，返回list长度
>* rPush(string key, value);   // 从尾部添加元素，返回list长度
>* lPop(string key);   // 取出头部的元素并从list中删除
>* rPop(String key);   // 取出尾部的元素并从list中删除
>* lPushx/rPushx(string key, value);
>* lSzie(string key);  // 返回list长度
>* lGet/lIndex(int index); // 返回list指定某个索引的元素
>* lSet(string key, int index, value); // 设置list的index位为value
>* lRange/lGetRange(string key, int start, int end);   获取指定范围
>* lTrim/listTrim(string key, int start, int end); 裁剪区间内，区间外的元素会被删除
>* lRem/lRemove(string key, value, count); // 删除list中count个value
>* lInsert(string key, Redis::AFTER/BEFORE, pivot, value); // 在pivot之前或之后插入value
>* rpoplpush(string key1, string key2);    // 将key1的尾部元素取出来存到key2的头部

```php
// rPush 返回list长度
var_dump($redis->rPush("list","v1"));   // int(1)
var_dump($redis->rPush("list","v2"));   // int(2)
var_dump($redis->rPush("list","v3"));   // int(3)
var_dump($redis->lRange("list",0,-1));  // array(3) {[0]=>string(2) "v1" [1]=>string(2) "v2" [2]=> string(2) "v3"}
var_dump($redis->lPop("list")); // string(2) "v1"
var_dump($redis->lRange("list",0,-1));
```

##Set
>* sAdd(string key, value);    // 往set中添加value
>* sRem/sRemove(string key, value);    // 删除set中的value
>* sMove(string sourceKey, string destinationKey, value);  // 将value从source移动到destination
>* sIsMember/sContains(string key, value); // set中是否存在value
>* sCard/sSize(string key);    // set中的元素个数
>* sPop(string key);   // 随机返回set中的元素并删除
>* sRandMember(string key);    // 随机返回set中的元素，不删除
>* sInter/sUnion/sDiff(string key1, string key2...);   // 获取其他set和第一个set的交集/并集/差集
>* sInterStore/sUnionStore/sDiffStore(string outputKey, string key1, string key2...);  // 获取其他set和第一个set的交集/并集/差集，并将结果保存到outputKey中
>* sMembers/sGetMembers(string key);   // 获取一个set的所有元素
>* sort(string key,array( string by, array limit,array get,string sort, boolean alpha, string store)); // 对set进行排序，可选排序的字段，分页，获取字段，排序方式，是否按字母排序以及结果保存等

```php
$redis->sadd('s', 5); 
$redis->sadd('s', 4); 
$redis->sadd('s', 2); 
$redis->sadd('s', 1); 
$redis->sadd('s', 3);
var_dump($redis->sort('s')); // 1,2,3,4,5
var_dump($redis->sort('s', array('sort' => 'desc'))); // 5,4,3,2,1
var_dump($redis->sort('s', array('sort' => 'desc', 'store' => 'out'))); // (int)5

$redis = new redis();
$redis->connect('127.0.0.1', 6379);
$redis->flushall(); 

$redis->lpush('id', 1);
$redis->set('name_1', 'tank');
$redis->set('score_1',89);

$redis->lpush('id', 2);
$redis->set('name_2', 'zhang');
$redis->set('score_2', 40);

$redis->lpush('id', 4);
$redis->set('name_4','ying');
$redis->set('score_4', 70);

$redis->lpush('id', 3);
$redis->set('name_3', 'fXXK');
$redis->set('score_3', 90);

/**
 * 按score从大到小排序,取得id
 */
$sort=array('BY'=>'score_*',
            'SORT'=>'DESC'
            );
print_r($redis->sort('id',$sort)); //结果:Array ( [0] => 3 [1] => 1 [2] => 4 [3] => 2 ) 

/**
 * 按score从大到小排序,取得name
 */
$sort=array('BY'=>'score_*',
            'SORT'=>'DESC',
            'GET'=>'name_*'
            );
print_r($redis->sort('id',$sort)); //结果:Array ( [0] => fXXK [1] => tank [2] => ying [3] => zhang )  

/**
 * 按score从小到大排序,取得name，score
 */
$sort=array('BY'=>'score_*',
            'SORT'=>'DESC',
            'GET'=>array('name_*','score_*')
            );
print_r($redis->sort('id',$sort));
/**
 *结果:Array
        (
            [0] => fXXK
            [1] => 90
            [2] => tank
            [3] => 89
            [4] => ying
            [5] => 70
            [6] => zhang
            [7] => 40
        ))
 */

/**
 * 按score从小到大排序,取得id，name，score
 */
$sort=array('BY'=>'score_*',
            'SORT'=>'DESC',
            'GET'=>array('#','name_*','score_*')
            );
print_r($redis->sort('id',$sort));
/**
 *结果:Array
        (
            [0] => 3
            [1] => fXXK
            [2] => 90
            [3] => 1
            [4] => tank
            [5] => 89
            [6] => 4
            [7] => ying
            [8] => 70
            [9] => 2
            [10] => zhang
            [11] => 40
        )
 */
?>
```

##SortedSet
>* zAdd(string key, int score, string value);
>* zRem(string key, string member);
>* zRemRangeByScore(string key, int min, int max);
>* zCard(string key);
>* zCount(string key, int min, int max);
>* zScore(string key, string value);
>* zRank(string key, string value);
>* zRange(string key, int start, int stop, boolean withscores);
>* zRevRange(string key, int start, int stop, boolean withscores);
>* zRangeByScore(string key, int minScore, int maxScore, array( boolean withscores, int limie));

```php
var_dump($redis->zRangeByScore('key',"-inf","+inf",array('withscores'=>true)));
```

>* zInter/zUnion(String outputKeyName, array( string inputKeyName ...), array( int weight ...), string aggregateFunction);

```php
$redis->zInter('output',array('key','key1'),array(5,1),"MIN");
$redis->zRangeByScore("output","-inf","+inf",array('withscores'=>true));
```





