# HTTPS certificate

needed for local test web server to use HTTPS

## Generate HTTPS certificate

needed files: `test-https.cert.cnf`

### Step 1: create private key

    openssl genrsa -out test-https.priv.pem 2048

-> creates private key file `test-https.priv.pem` 

### Step 2: create HTTPS certificate

    openssl req -new -x509 -config test-https.cert.cnf -nodes -days 7300 -key test-https.priv.pem -out test-https.cert.pem

-> creates HTTPS certificate file `test-https.cert.pem`
