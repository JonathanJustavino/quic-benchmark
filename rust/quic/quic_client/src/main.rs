use std::net;

fn main() -> std::io::Result<()> {
    println!("Hello, Client!");
    let server_name = "quic-rust.org";
    let _old_server_name = "127.0.0.:7766";
    let pem_cert = "../certs/cert.pem";
    let pem_key = "../certs/key.pem";
    let mut config = quiche::Config::new(quiche::PROTOCOL_VERSION).unwrap();
    config.load_cert_chain_from_pem_file(pem_cert).unwrap();
    config.load_priv_key_from_pem_file(pem_key).unwrap();
    let socket = std::net::UdpSocket::bind("127.0.0.1:7755").unwrap();
    let server_socket_address = net::SocketAddr::from(([127, 0, 0, 1], 7766));
    let connection_result = socket.connect(server_socket_address);

    match connection_result {
        Ok(v) => {
            println!("Successful connection: {:?}", v);
        }
        Err(e) => {
            eprintln!("Error: {}", e);
        }
    }

    let scid = [0xba; 16];
    let mut conn = quiche::connect(Some(&server_name), &scid, &mut config).unwrap();
    let mut out = [0; 512];

    loop {
        let write = match conn.send(&mut out) {
            Ok(v) => v,
    
            Err(quiche::Error::Done) => {
                // Done writing.
                break;
            },
    
            Err(e) => {
                // An error occurred, handle it.
                eprintln!("Error: {}", e);
                break;
            },
        };

        let result = socket.send(&out[..write]);
        println!("Writing");
        println!("{:?}", result);
    }

    Ok(())
}
