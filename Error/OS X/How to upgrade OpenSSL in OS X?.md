# How to upgrade OpenSSL in OS X?

brew update
brew install openssl
brew link --force openssl

openssl version -a

If one of the bad versions come up (1.0.1a-f):

which openssl

Replace with a symlink to /usr/local/Cellar/openssl/1.0.1g/bin/openssl

e.g. in my case openssl was located in /usr/bin

mv /usr/bin/openssl /usr/bin/openssl_OLD
ln -s /usr/local/Cellar/openssl/1.0.1g/bin/openssl /usr/bin/openssl

