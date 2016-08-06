# # 并查集（Union-Find）

##问题
动态连通性

##API

```java
public class UF
    public UF(int N){}
    // 连接两个节点
    public void union(int p, int q){}
    // 判断两个节点是否连通
    boolean connected(){}
}
```

##实现
###Quick-Find算法
用一个数组来存放节点（int），数组下标为节点名，节点对应的值为该节点所属的连通组件（connected component）id，当该值相等的下标即在同一连通组件内。

```java
public class UF{
    private int[] id;
    private int count; // numbers of connected component
    // initialize
    public UF(int N){
        count = N;
        id = new int[N];
        for (int i = 0; i < N; N++){
            id[i] = i;
        }
    }
    
    public int count(){
        return count;
    }
    
    // get connected component id
    private int find(int p){
        return id[p];
    }
    
    public boolean connected(int p, int q){
        return id[p] == id[q];
    }
    
    public void union(int p, int q){
        int pID = id[p];
        int qID = id[q];
        if (qID == pID) return;
        for (int i = 0; i < id.length; i++){
            if (id[i] == pID) {
                id[i] = qID;
            }
        }
        count--;
    }
}
```

####例子
>* 初始化的数组

|0|1|2|3|4|5|6|7|8|9|
|----|----|----|----|----|----|----|----|----|----|----|
|0|1|2|3|4|5|6|7|8|9|

>* 经过一定的连接后

|0|1|2|3|4|5|6|7|8|9|
|----|----|----|----|----|----|----|----|----|----|----|
|0|1|3|3|4|7|6|7|8|7|

>* 连接5和3，union(3, 5)

|0|1|2|3|4|5|6|7|8|9|
|----|----|----|----|----|----|----|----|----|----|----|
|0|1|<font color='red'>7</font>|<font color='red'>7</font>|4|7|6|7|8|7|

####算法效率

|algorithm|initialize|union|find|
|----| :---: | :---: | :---: |
|quick-find|N|N|1|
> 如果要在N个元素中执行N次union操作，需要N^2次数组操作。

###Quick-Union算法
两个节点连接时，将其中一个节点（A）的id指向另一个节点（B）的下标，即将B作为A的根节点，而根节点的id作为该连通组件的id。

```java
public class UF{
    private int[] id;
    private int count; // numbers of connected component
    // initialize
    public UF(int N){
        id = new int[N];
        for (int i = 0; i < N; N++){
            id[i] = i;
        }
    }
    
    public int count(){
        return count;
    }
    
    // get root
    private int root(int p){
        while (p != id[p]){
            p = id[p];
        }
        return p;
    }
    
    public boolean connected(int p, int q){
        return root(p) == root(q);
    }
    
    public void union(int p, int q){
        int pRoot = root(p);
        int qRoot = root(q);
        id[pRoot] = qRoot;  // change the root of p to root of q;
        count--;
    }
}
```
####例子
>* 初始化的数组

|0|1|2|3|4|5|6|7|8|9|
|----|----|----|----|----|----|----|----|----|----|----|
|0|1|2|3|4|5|6|7|8|9|

>* 经过一定的连接后

|0|1|2|3|4|5|6|7|8|9|
|----|----|----|----|----|----|----|----|----|----|----|
|0|1|3|3|4|7|6|9|8|9|

>* 连接5和3，union(3, 5)

|0|1|2|3|4|5|6|7|8|9|
|----|----|----|----|----|----|----|----|----|----|----|
|0|1|3|<font color='red'>9</font>|4|77|6|9|8|9|

####算法效率

|algorithm|initialize|union|find|
|----| :---: | :---: | :---: |
|quick-find|N|N|1|
|quick-union|N|N|N|
> quick-union会导致树太高，导致查找根节点的开销太大。


###Weighted Quick-Union
普通的Quick-Union在union时有可能将大树连接到小树下，导致树越来越高。
加权的Quich-Union在union时做出判断将小树连接到大树，避免树越来越高。

```java
public class UF{
    private int[] id;
    private int count; // numbers of connected component
    private int[] size; // size of connected component
    // initialize
    public UF(int N){
        id = new int[N];
        size = new int[N];
        for (int i = 0; i < N; N++){
            id[i] = i;
            size[i] = 1;
        }
    }
    
    public int count(){
        return count;
    }
    
    // get root
    private int root(int p){
        while (p != id[p]){
            p = id[p];
        }
        return p;
    }
    
    public boolean connected(int p, int q){
        return root(p) == root(q);
    }
    
    public void union(int p, int q){
        int pRoot = root(p);
        int qRoot = root(q);
        if (size[pRoot] > size[qRoot]){
            id[qRoot] = pRoot;
            size[pRoot] += size[qRoot];
        }else{
            id[pRoot] = qRoot;
            size[qRoot] += size[pRoot];
        }
        count--;
    }
}
```
|algorithm|initialize|union|find|
|----| :---: | :---: | :---: |
|Quick-Find|N|N|1|
|Quick-Union|N|N|N|
|Weighted Quick-Union|N|lgN|lgN|

命题：对于N个节点，加权quick-union算法构造的森林中的任意节点的深度最多为lgN。
数学归纳法证明：
设大小为k的树的高度最多为lgk。
当k=1时树的高度为0，成立。
大小为i的树的高度为lgi，i<j。设i+j=k。
当将i和j合并，由于i<j，于是将i合并到j树下，此时i的深度增加1。
于是有：1+lgi=lg(2*i)=lg(i+i)<=lg(i+j)=lgk。

###Weighted Quick-Union with Path Compression
路径压缩，将在查找时节点的父节点指向该节点的爷爷节点，即每次都压缩一级，最后会生成一棵扁平的树。

```java
private int root(int p){
    while (p != id[p]){
        id[p] = id[id[p]];  //
        p = id[p];
    }
    return p;
}
```

|algorithm|initialize|union|find|
|----| :---: | :---: | :---: |
|Quick-Find|N|N|1|
|Quick-Union|N|N|N|
|Weighted QU|N|lgN|lgN|
|Weighted QU With Path Compression|N|Very near to 1 (amortized)|Very near to 1 (amortized)|

