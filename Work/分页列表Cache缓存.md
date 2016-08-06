# 分页列表cache缓存
以SortedSet保存具体数据的ID，Score的值为具体排序规则的值，SortedSet的key为`{$prefix}:{$order}:{$condition}:{$value}`。
多个条件筛选时，取相同排序规则下的不同条件的SortedSet的交集。

```php
class ArticleService {
    private $articleInfoCachePrefix = 'article:info:';
    private $articleListCachePrefix = 'article:list:';
    private $this->redis;   // redis instance
    private $this->article; // Dao

    /**
     * 可排序项与db中字段的映射
     * @var array
     */
    private $cacheOrderMap = array(
      'create_time' => 'article_create',
    );

    /**
     * @description 从cache获取列表
     * @param int $page
     * @param int $pageSize
     * @param array $condition
     * @param string $order
     * @param bool $orderDesc
     * @return array|bool
     */
    public function getArticlePageListFromCache($page = 1, $pageSize = 10, $condition = array(), $order = 'create_time', $orderDesc = true)
    {
        $offset = (int)$page < 1 ? 0 : ($page - 1) * $pageSize;
        $end = $offset + $pageSize - 1;
    
        // 获取目标的key，即取交集，如果这个交集不存在则生成
        $idListCacheKey = $this->_getSortedSetInterKeyByOrderAndCondition($this->articleListCachePrefix, $order, $condition);
    
        // get id list
        if ($orderDesc){
            $idList = $this->redis->zRevRange($idListCacheKey, $offset, $end);
        }else{
            $idList = $this->redis->zRange($idListCacheKey, $offset, $end);
        }
    
        if(empty($idList)){
            return false;
        }
    
        // get data list
        $list = array();
        foreach ((array)$idList as $id){
            $info = $this->getArticleInfoById($id);
            if(is_array($info)){
                $list[] = $info;
            }
        }
    
        // get total
        $total = $this->redis->zCard($idListCacheKey);
        return array('list' => $list, 'total' => $total);
    }
    
    /**
     * @description 获取一条数据
     * @param $id
     * @return array|bool|null
     */
    public function getArticleInfoById($id)
    {
        $redisKey = $this->_getArticleInfoCacheKey($id);
        $cache = $this->redis->getUnserialise($redisKey,'preCache');
        if (!$cache){
            // get from db
            $condition = array();
            $condition['article_id'] = $id;
            $content = $this->article->fetchOneInfo($condition);
            if(!$content){
                return false;
            }
            // put in cache
            $this->redis->setSerialise($redisKey, $content,'preCache');
            $data = $content;
        }else{
            $data = $cache;
        }
        return $data;
    }
    
    /**
     * 刷新列表缓存
     */
    public function refreshIdListCache()
    {
        $oldKeys = $this->redis->keys($this->articleListCachePrefix . '*');
        if(!empty($oldKeys)){
            $this->redis->del($oldKeys);
        }
        
        // 从db拿列表
        $data = $this->article->fetchList();
        foreach ((array)$this->cacheOrderMap as $key => $dbColumn){
            foreach ((array)$data['list'] as $item){
                $cacheKey = $this->_getArticleIdListCacheKey($this->articleListCachePrefix, $key);
                $score = strtotime($item[$dbColumn]);
                $id = $item['article_id'];
                // all
                $this->redis->zAdd($cacheKey, $score, $id, 'preCache');
    
                // type
                $typeCondition = array();
                $typeCondition['type'] = $item['article_type_id'];
                $typeCacheKey = $this->_getArticleIdListCacheKey($this->articleListCachePrefix, $key, $typeCondition);
                \Engine\Core::$register->redis->zAdd($typeCacheKey, $score, $id, 'preCache');
            }
        }
    }
    
    /**
     * @description 获取列表的key prefix:order:condition:value:
     * @param $keyPrefix
     * @param $order
     * @param $condition
     * @return string
     */
    public function _getArticleIdListCacheKey($keyPrefix, $order, $condition)
    {
    	if(empty($condition) && empty($order)){
    		return '';
    	}
    	$key = $keyPrefix;
    
    	if(!empty($order)){
    		$key .= 'order:' . $order . ':';
    	}
    	if(!empty($condition) && is_array($condition)){
    		ksort($condition);
    		foreach ($condition as $k => $v){
    			$key .= $k . ':';
    			if(is_array($v)){
    				$key .= implode(':', $v) . ':';
    			}else{
    				$key .= $v . ':';
    			}
    		}
    	}
    	return rtrim($key, ':');
    }
    
    /**
     * @description get redis key by id
     * @param $id
     * @return string
     */
    private function _getArticleInfoCacheKey($id)
    {
        $key = $this->articleInfoCachePrefix . $id;
        return $key;
    }
    
    /**
     * 根据排序和筛选字段，获取交集的key，如果交集不存在，会创建这个交集
     * @param $keyPrefix
     * @param $order
     * @param $condition
     * @return string
     */
    private function _getSortedSetInterKeyByOrderAndCondition($keyPrefix, $order, $condition)
    {
    	$idListCacheKey = $this->getSortedSetKeyByOrderAndCondition($keyPrefix, $order, $condition);
    	$isExists = $this->redis->exists($idListCacheKey);
    	// 不存在时，取交集
    	if(!$isExists){
    		$interSetKey = array();
    		foreach ((array)$condition as $key => $value){
    			$interSetKey[] = $this->getSortedSetKeyByOrderAndCondition($keyPrefix, $order, array($key=>$value));
    		}
    		if(count($interSetKey) > 1){
    			$this->zInterStore($idListCacheKey, count($interSetKey), $interSetKey);
    		}
    	}
    	return $idListCacheKey;
    }
}
```






