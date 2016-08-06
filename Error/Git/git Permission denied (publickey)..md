# git Permission denied (publickey).
fatal: Could not read from remote repository.

生成密钥
ssh-keygen -t rsa -C “yuatom93@gmail.com”

得到两个文件
id_rsa和id_rsa.pub

添加到ssh密钥列表
ssh-add 文件名

复制密钥到剪切板
pbcopy < ~/.ssh/id_rsa.pub

在github账户添加ssh key处粘贴


ssh -vT git@github.com 测试

