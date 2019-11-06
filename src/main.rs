extern crate merlin;
use merlin::Transcript;

use bincode::serialize;
use serde::Serialize;

#[derive(Debug, Clone, Serialize)]
struct VASPData {
	vasp_name: String,
	vasp_address_hash: String,
	chain_id: u32,
}

impl VASPData {
	pub fn new(name: &str, address: &str, chain_id: u32) -> VASPData {
		VASPData {
			vasp_name: name.to_string(),
			vasp_address_hash: address.to_string(),
			chain_id: chain_id,
		}
	}
}

fn main() {
	let vasp = VASPData::new("Binance", "1EEq3UrinJ4hkZ42chcgJzMKrexbef8Xw2", 0);

	println!("Vasp is: {:?}", vasp);
	let serialized_vasp = serialize(&vasp).unwrap();
	println!("Serizlied VASP is: {:?}", serialized_vasp);

    let mut real_transcript = Transcript::new(b"test msg");
    let mut test_transcript = Transcript::new(b"test msg");

    real_transcript.append_message(b"VaspData", &serialized_vasp);
    test_transcript.append_message(b"VaspData", &serialized_vasp);

    let mut real_challenge = [0u8; 32];
    let mut test_challenge = [0u8; 32];

    real_transcript.challenge_bytes(b"challenge", &mut real_challenge);
    test_transcript.challenge_bytes(b"challenge", &mut test_challenge);

    println!("{:?}", real_challenge == test_challenge);
}
