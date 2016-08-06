# 加密形式COOKIE记住用户登录

1、将用户信息，比如一个['uid'=&gt;123, 'username'=&gt;'testuser']的数组，序列化后成为字符串，使用可逆加密算法加密该字符串，写到一个Key为userinfo的COOKIE里。

2、由于可逆加密算法容易被解密，一旦加密的规则被别人猜测到以后，就可以轻易篡改这个COOKIE的内容，然后自行根据加密规则加密后伪造，所以，我们另外加入一个infodig的COOKIE，是将以上的userinfo的COOKIE内容，加入salt后使用不可逆加密算法生成散列，至于salt咱们可以自己定，总之要对外保密，不可逆算法例如md5，甚至多次加盐多次md5。

3、以上两个COOKIE，为增强安全性，防止用户被XSS攻击后拿到，可以设置http-only属性。

服务端判断存在以上两个COOKIE后：
1、验证infodig与userinfo是否匹配（将userinfo的内容使用生成infodig的方法计算后，与COOKIE传上来的infodig匹配是否一致）

2、infodig验证通过后，使用解密算法解密userinfo串，得到用户信息，如果用户信息里的uid存在用户表中，则写SESSION，通过SESSION保持本次会话。

https://www.zhihu.com/question/20182967/answer/84386085



