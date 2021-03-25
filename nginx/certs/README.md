# HTTPS certificate

needed for local test web server to use HTTPS

```
openssl req -x509 -nodes -days 365 -newkey rsa:1024 \
    -keyout nginx-selfsigned.key \
    -out nginx-selfsigned.crt
```
