fn main() -> std::io::Result<()> {
    println!("Hello, Server!");
    let pem_cert = "../certs/cert.pem";
    let pem_key = "../certs/key.pem";
    let mut config = quiche::Config::new(quiche::PROTOCOL_VERSION).unwrap();
    config.load_cert_chain_from_pem_file(pem_cert).unwrap();
    config.load_priv_key_from_pem_file(pem_key).unwrap();

    let socket = std::net::UdpSocket::bind("127.0.0.1:7766").unwrap();
    let scid = [0xba; 16];
    let mut conn = quiche::accept(&scid, None, &mut config).unwrap();
    let mut buf = [0; 512];

    loop {
        let read = socket.recv(&mut buf).unwrap();
        let read = match conn.recv(&mut buf[..read]) {
            Ok(v) => v,

            Err(e) => {
                println!("{}", e);
                break;
            },
        };
        println!("read {} bytes", read);
        println!("{:?}", buf);
        let reason: &[u8] = &[0];
        let close = conn.close(false, 0, reason);

        match close {
            Ok(res) => {
                println!("{:?}", res);
                println!("Closing the connection");
                break;
            }
            Err(e) => {
                eprint!("Error closing the connection: {}", e);
                break;
            }
        }
    }
    Ok(())
}
