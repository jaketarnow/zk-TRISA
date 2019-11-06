extern crate merlin;
use merlin::Transcript;
use std::env;

fn build_bulletproof(raw_data: &[u8]) {
	let mut real_transcript = Transcript::new(b"trisa init");
    let mut test_transcript = Transcript::new(b"trisa init");

    real_transcript.append_message(b"VaspData", raw_data);
    test_transcript.append_message(b"VaspData", raw_data);

    let mut real_challenge = [0u8; 32];
    let mut test_challenge = [0u8; 32];

    real_transcript.challenge_bytes(b"challenge", &mut real_challenge);
    test_transcript.challenge_bytes(b"challenge", &mut test_challenge);

    println!("{:?}", real_challenge == test_challenge);
}

fn main() {
	let args: Vec<String> = env::args().collect();
    let raw_bytes = &args[1];

    build_bulletproof(raw_bytes.as_bytes());
}
