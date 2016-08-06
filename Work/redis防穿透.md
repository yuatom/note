# redis防穿透

##解决问题
在高并发的情况下，当Cache崩溃或缓存过期，会有大量的请求回源往DB，导致DB服务器压力剧增。

##解决方式
提前过期，在缓存过期前提前更新缓存，在每次获取cache之前，判断cache是否快过期（有效时间小于某个值），如果是就回DB取数据并更新缓存。但这样也可能会在高并发的情况下，多个请求判断都是快过期并且都回源。此时需要并发锁。

并发锁，同一个时刻只有一个请求回源。通过Redis的`SETNX`和`GETSET`实现，针对每个cache都设置一个锁，只有SETNX成功的连接才能回源。

##Code

```php
class RedisImpl {
    private $keyCreateTimeSet = 'key:create:time:';

    private $keyLockTimePrefix = 'key:lock:';

    private $timeToUpdateCache = 5;

    private $timeToDelLock = 10;
    
    private $redis;
    
    //读名单
    private static $preRAction = array(
        "get",
        "mGet",
        "hGet",
        "getUnserialise",
    );
    
    //写名单
    private static $preWAction = array(
        "set",
        "mSet",
        "hSet",
        "setSerialise",
    );

	/**
	 * 构造方法
	 * @param array $params
	 * @param bool $consident
	 */
	public function __construct($params, $consident = false){
		parent::__construct($params, $consident);
	}

	/**
	 * 魔术方法
	 */
	public function __call($name, $args){
		$status = $this->beforeAction($name, $args);
		if($status){
			return false;
		}
		$result = call_user_func_array(array($this->redis, $name), $arguments);
		$this->afterAction($name, $args);
		return $result;
	}

	/**
	 * beforeAction
	 * @param string $name
	 * @param array $args
	 * @return bool
	 */
	public function beforeAction($name, &$args){
		$end = end($args);
		$key = $args[0];
		if(!is_array($end) && "preCache" == $end){
			if(in_array($name, RedisImpl::$preRAction)){
				//属于读名单
				if($this->checkIsNeedToUpdate($key)){
				    // 需要提前更新
					if($this->setLock($key)){
						// 是否抢锁成功
						return true;
					}else{
						return false;
					}
				}else{
					//不需要前更新
					return false;
				}
			}else if(in_array($name, RedisImpl::$preWAction)){
				//属于写名单
				//$this->setKeyCreateTimestamp($key);
			}
			array_pop($args);
		}
		//不需要前更新
		return false;
	}

	/**
	 * afterAction
	 * @param string $name
	 * @param array $args
	 * @return void
	 */
	public function afterAction($name, $args){
		
	}

    /**
     * 是否需要去db更新
     * @param $key
     * @return bool
     */
    private function checkIsNeedToUpdate($key)
    {
        $t = $this->ttl($key);
        if($t < $this->timeToUpdateCache){
            return true;
        }else{
            return false;
        }
    }

   /**
    * 获取key创建时的时间戳
    * @param $key
    * @return mixed
    */
   private function getKeyCreateTimestamp($key)
   {
       return $this->get($this->keyCreateTimeSet.$key);
   }

    /**
     * 设置key创建时的时间戳
     * @param $key
     */
    private function setKeyCreateTimestamp($key)
    {
        $time = time();
        $this->set($this->keyCreateTimeSet.$key, $time);
    }

    /**
     * 抢锁
     * @param $key
     * @return bool
     */
    private function setLock($key)
    {
        $time = $this->redis->time();
        $nowTimestamp = $time[0];
        $key = $this->keyLockTimePrefix . $key;
        if((bool)$this->redis->setnx($key, $nowTimestamp)){
            $this->redis->expire($key, $this->timeToDelLock);
            return true;
        }else{
            // check expire
            $lockTime = $this->redis->get($key);
            if($nowTimestamp  < ($this->timeToDelLock + $lockTime)){
                // expire
                $lockTime = $this->redis->getSet($key, $nowTimestamp);
                if($nowTimestamp < ($this->timeToDelLock + $lockTime)){
                    // 上一次时间仍然过期，getSet加锁成功
                    return true;
                }else{
                    // 上一次的时间没过期，说明有其他连接抢到锁，本次连接没抢到，虽然getSet把时间改了，但是影响不大
                    return false;
                }
            }else{
                // alive
                return false;
            }
        }	        
    }


    /**
     * 删除锁
     * @param $key
     */
    private function deleteLock($key)
    {
        $key = $this->keyLockTimePrefix . $key;
        $this->del($key);
    }
}
```






