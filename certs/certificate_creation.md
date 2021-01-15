zertifikate für quic mit: 

openssl genrsa 2024 > server.key
openssl req -new -key server.key -subj "/C=JP" > server.csr
openssl x509 -req -days 3650 -signkey server.key < server.csr > server.crt


zertifikate für tcp-tls:

openssl genrsa -out private-key.pem 2048
openssl req -new -key private-key.pem -out csr.pem
openssl x509 -req -in csr.pem -signkey private-key.pem -out public-cert.pem