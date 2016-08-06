# Base64

```php
// php中将图片转换成base64
$img_file = file_get_contents("http://www.oschina.net/img/logo_s2.png");
echo base64_encode($img_file);
```

Data URL是在本地直接绘制图片，不是从服务器加载，所以节省了HTTP连接，起到加速网页的作用。
减少了HTTP请求；
某些文件可以避免跨域的问题；
适用于变动较小的图片；
编码后数据量比原图大，适合于小图片，大图片转换后的字符过长会增加页面体重；
加重客户端的CPU和内存负担；

