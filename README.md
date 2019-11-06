# zk-TRISA
ZKP implementation of VASP messaging

## Basis of Implementation
The basis of this project is to allow VASPs to share information between them such VASP name, corresponding address info, as well as any other metadata. To be able to share this information in a secure and private way without the potential risk of an eavesdropper or bad actor VASP using the network to obtain high profile data.

We are using Bulletproofs which is a non-interactive zero-knowledge proof protocol with very short proofs and without the need of a trusted setup. Thus, a zk-STARK. zk-SNARKs require a pre-existing trusted setup. Bulletproofs enable proving that a committed value is in a range using only 2log2(n) + 9 group and field elements, where n is the bit length of the range. 

The main use of range proofs within a bulletproof is to have a prover to convince a verifier that a particular value lies within a valid range, without revealing any additional information about the given value. 

In order to pass in additional information regarding VASPs we use a new tool for arguments of knowledge called Merlin.
Merlin is a STROBE (STROBE is a new framework for cryptographic protocols. It's goals are to make crpytographic protocols much simpler to develop, deploy and analyze.) based transcript construction for zero-knowledge proofs. It automates the Fiat-Shamir transform so that by using Merlin, non-interactive protocols can be implemented as if they were interactive. By using Merlin for transcript messages - it provides a transcript-based random number generator as defense-in-depth against bad-entropy attacks (nonce re-sue or bias over proofs). The RNG provides synthetic randomness derived from the entire public transcript as well as the prover's witness data and auxiliary input from an external RNG. 

The use of the libraries we are using from dalek-cryptography provides us the Ristretto group which is a modification of Mike Hamburg's Decaf scheme to work with cofactor-8 curves such as Curve25519 instead of previous work on secp256k1. 


## Building and Usage
To enable zk-TRISA make sure you are running nightly rust.
You can install nightly Rust with rustup:
```
rustup default nightly
```

Once you have installed Rust and have compiled the source code successfully you can initiate the bulletproof via:
```
cargo run "70000000661051109711099101340000000496969113518511410511074521041079052509910499103741227775114101120981011025688119500000"
```

This will return true if the verifier proof matches the original bulletproof.