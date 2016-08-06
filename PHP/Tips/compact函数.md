# compact函数
传入变量名，以变量名为键名，以变量值为键值放到一个数组中

```php
<?php
$city  = "San Francisco";
$state = "CA";
$event = "SIGGRAPH";

$location_vars = array("city", "state");

$result = compact("event", "nothing_here", $location_vars);
print_r($result);
?>
```

```shell
Array
(
    [event] => SIGGRAPH
    [city] => San Francisco
    [state] => CA
)
```

