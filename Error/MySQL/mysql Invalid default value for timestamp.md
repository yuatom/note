# mysql Invalid default value for timestamp
have NO_ZERO_DATE enabled in your MySQL configuration
严格模式下timestamp类型的数据不允许为0，`SELECT @@global.sql_mode`查出的结果中有`NO_ZERO_DATE`，可在mysql的配置文件中修改。
sql_mode='ONLY_FULL_GROUP_BY,NO_AUTO_VALUE_ON_ZERO,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,
ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION,PIPES_AS_CONCAT,ANSI_QUOTES'

SELECT @@global.sql_mode; 
查看配置

关闭严格模式
sql-mode="STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION"

