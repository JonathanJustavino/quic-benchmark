fn main() -> std::io::Result<()> {
    println!("Hello, Client!");
    let old_server_name = "quic-rust.org";
    let server_name = "127.0.0.:7766";
    let pem_cert = "../certs/cert.pem";
    let pem_key = "../certs/key.pem";
    let mut config = quiche::Config::new(quiche::PROTOCOL_VERSION).unwrap();
    config.load_cert_chain_from_pem_file(pem_cert).unwrap();
    config.load_priv_key_from_pem_file(pem_key).unwrap();
    let socket = std::net::UdpSocket::bind("127.0.0.1:7755").unwrap();
    let scid = [0xba; 16];
    let mut conn = quiche::connect(Some(&server_name), &scid, &mut config).unwrap();
    let mut out = [0; 512];

    // println!("{:?}", conn);

    loop {
        let write = match conn.send(&mut out) {
            Ok(v) => v,
    
            Err(quiche::Error::Done) => {
                // Done writing.
                break;
            },
    
            Err(e) => {
                // An error occurred, handle it.
                break;
            },
        };

        let result = socket.send(&out[..write]);
        println!("{:?}", result);
    }

    Ok(())
}
