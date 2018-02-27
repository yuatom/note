#HTTP2.md
## 1 HTTP
### 1.1 延迟
当一个页面中需要加载多个资源时，并不能同时接收处理，因此会延迟问题。

### 1.1 HTTP Pipelining
将多个HTTP请求放到一个TCP连接中发送，后面的请求不需要等待服务器对前一个请求的响应；但是客户端在处理响应时仍然需要按照发送请求的顺序来接收响应。所以仍然不能解决多个请求时的延迟问题。

### 1.2 Sprinting
将页面需要的多张较小的图片合并成一张大图，然后在通过js或CSS去切割显示。这样能减少对图片资源的请求数。

### 1.3 内联Inling
以图片的原始数据来代替CSS文件中的URL选项，如：

```CSS
.icon1 {
    background: url(data:image/png;base64,<data>) no-repeat;
  }
.icon2 {
    background: url(data:image/png;base64,<data>) no-repeat;
  }
```

TODO...