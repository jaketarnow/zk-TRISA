extern crate rand;
use rand::thread_rng;

extern crate curve25519_dalek;
use curve25519_dalek::ristretto::CompressedRistretto;
use curve25519_dalek::scalar::Scalar;

extern crate merlin;
use merlin::Transcript;

extern crate bulletproofs;
use bulletproofs::{BulletproofGens, PedersenGens, RangeProof};

use serde::Serialize;
use bincode::serialize;
use std::env;

#[derive(Debug, Serialize)]
struct VaspData {
    name: String,
    address_hash: String,
    chain_id: u32,
}

impl VaspData {
    #[warn(dead_code)]
    fn new(vasp_name: &str, vasp_address: &str, chain_id: u32) -> VaspData {
        VaspData {
            name: vasp_name.to_string(),
            address_hash: vasp_address.to_string(),
            chain_id: chain_id,
        }
    }
}

//Building the actual bulletproof with Merlin's Transcript with the serialized VASP data
fn build_bulletproof(
    pedersen_commitment: PedersenGens,
    bulletproof_gens: &BulletproofGens,
    secret_val: u64,
    blinding: Scalar,
    raw_data: &[u8],
) -> (RangeProof, CompressedRistretto) {
    let mut transcript = Transcript::new(b"trisa init");
    transcript.append_message(b"VaspData", raw_data);

    let (proof, committed_value) = RangeProof::prove_single(
        bulletproof_gens,
        &pedersen_commitment,
        &mut transcript,
        secret_val,
        &blinding,
        32,
    )
    .expect("we messed up somewhere :(");

    (proof, committed_value)
}

//Validation of the original bulletproof and new prover's proof. If is_ok, then both match and we have completed validation
fn validate_proof(
    verifier_proof: RangeProof,
    commited_value: CompressedRistretto,
    pedersen_commitment: PedersenGens,
    bulletproof_gens: &BulletproofGens,
    verifier_bytes: &[u8],
) -> bool {
    let mut verifier_transcript = Transcript::new(b"trisa init");
    verifier_transcript.append_message(b"VaspData", verifier_bytes);
    verifier_proof
        .verify_single(
            bulletproof_gens,
            &pedersen_commitment,
            &mut verifier_transcript,
            &commited_value,
            32,
        )
        .is_ok()
}

fn main() {
    //read in bytes from outside source
    let args: Vec<String> = env::args().collect();
    let raw_bytes = &args[1];

    //generators for Pedersen commitment. Set as default for now
    let pedersen_commitment = PedersenGens::default();

    //generators for Bulletproofs, valid for proof up to bitsize 64 and aggregation size of 1
    let bulletproof_gens = BulletproofGens::new(64, 1);

    //sercret val to prove lies in range [0, 2^32]
    let secret_val = 1037578891u64;

    let blinding = Scalar::random(&mut thread_rng());

    let (x, y) = build_bulletproof(
        pedersen_commitment,
        &bulletproof_gens,
        secret_val,
        blinding,
        raw_bytes.as_bytes(),
    );

    let validation = validate_proof(
        x,
        y,
        pedersen_commitment,
        &bulletproof_gens,
        raw_bytes.as_bytes(),
    );
    println!("{:?}", validation);
}

#[test]
fn test_bulletproof() {
    let pedersen_commitment = PedersenGens::default();
    let bulletproof_gens = BulletproofGens::new(64, 1);
    let secret_val = 1037578891u64;
    let blinding = Scalar::random(&mut thread_rng());
    let bullet_test = build_bulletproof(pedersen_commitment, &bulletproof_gens, secret_val, blinding, b"70000000661051109711099101340000000496969113518511410511074521041079052509910499103741227775114101120981011025688119500000");
    println!("{:?}", bullet_test);
}

#[test]
fn test_full_validation() {
    let pedersen_commitment = PedersenGens::default();
    let bulletproof_gens = BulletproofGens::new(64, 1);
    let secret_val = 1037578891u64;
    let blinding = Scalar::random(&mut thread_rng());
    let (bulletproof, ristretto) = build_bulletproof(pedersen_commitment, &bulletproof_gens, secret_val, blinding, b"70000000661051109711099101340000000496969113518511410511074521041079052509910499103741227775114101120981011025688119500000");
    let validation = validate_proof(bulletproof, ristretto, pedersen_commitment, &bulletproof_gens, b"70000000661051109711099101340000000496969113518511410511074521041079052509910499103741227775114101120981011025688119500000");
    assert_eq!(true, validation);
}

#[test]
fn test_with_vasp_data() {
    let pedersen_commitment = PedersenGens::default();
    let bulletproof_gens = BulletproofGens::new(64, 1);
    let secret_val = 1037578891u64;
    let blinding = Scalar::random(&mut thread_rng());

    let vasp = VaspData::new("ExchangeXYZ", "1EEq3UrinJ4hkZ42chcgJzMKrexbef8Xw2", 0);
    println!("VASP: {:?}", vasp);
    let serialized_vasp = serialize(&vasp).unwrap();
    println!("Serialzied VASP: {:?}", serialized_vasp);

    let (bulletproof, ristretto) = build_bulletproof(
        pedersen_commitment,
        &bulletproof_gens,
        secret_val,
        blinding,
        &serialized_vasp,
    );
    let validation = validate_proof(
        bulletproof,
        ristretto,
        pedersen_commitment,
        &bulletproof_gens,
        &serialized_vasp,
    );
    assert_eq!(true, validation);
}
