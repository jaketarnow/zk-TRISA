# zk-TRISA
ZKP implementation of VASP messaging

We present a minimal proof of concept, where VASPs __A__ and __B__
exchange proofs of PII knowledge without revealing the PII in
question.  Because PII exchange must occur before a transaction is
approved, this can cut down on phishing attempts by e.g. Scam ICOs
abusing their access to the TRISA network.  It also provides
individuals more privacy options: whom do you trust more, your
counterparty or your counterparty's VASP?

To accomplish this we have the following endpoints

Use | Endpoint
--- | ---
Trisanym "DNS" | `domain/` 
Send Bit Commitment | `domain/bit-commit_1` 
Receive Bit Commitment | `domain/bit-commit_2` 
Send Our Salt | `domain/bit-commit_3` 
Receive Salt and Verify | `domain/bit-commit_4` 

See the file `server.py` for more info.


## Story

### DNS / Trisanyms

Alice and Bob are customers of VASPs __A__ and __B__
respectively. Alice wants to pay Bob in cryptocurrency for a business
service, with legal protections if Bob breaks contract.  Thus, instead
of sending him BTC directly, she will make the payment through their
respective VASPs, with TRISA.

Users can claim strings that proclaim their identities "jake@binance",
"eric@kraken", "bert@bitfinex", or obscure them: "24601@vasp-toulon",
"655321@vasp-ludovico".  You then ask the endpoint belonging to the
VASP after the "@" if that user is a customer.  If so, you can send to
them.  These trisanyms could be socialized on TRISA using a DNS
protocol.

If you submit a user's Trisanym to the appropriate GET endpoint
(presently root `/`), that endpoimnt responds with either

* User exists:
-- Status 202 (Accepted)
-- with a JSON containing the hashed user info for the given trisanym

* User DNE:
-- Status 204 (No Content)
-- with empty JSON

Then we proceed, based on 3 seperate cases:


### Case A. Alice & Bob provide their PII to eachother.

Bob tells Alice his accounts receivable info:
```json
     {"name":"Bob McSurname",
     "address":"4321 Shellcorp Ave, Town YZ 54321",
     "account":"B9876543210"}
```

Alice does the same for her accounts payable:
```json
     {"name":"Alice Lastnamersson",
     "address":"1234 Road Rd, City XY 01234",
     "account":"A0123456789"}
```

These could be provided by the users' to eachother's apps, P2P.  This
might allow more speed as the VASP need only store the bit-commitment
ciphertext under single-key encryption, and can use multiple
signatures to secure the plaintext PII.

Note this account number, like a bitcoin address, can be a one-time
number.  Similarly, he can pay for a business address of record to
avoid getting harassed at home.  Nonetheless, Bob and __B__ are *not*
comfortable leaking such customer information to every exchange, ICO,
or Foreign Government that claims to want to send Bob money using
TRISA.  Yet we want all of those entities to be using TRISA...

To avoid this step, __A__ and __B__ can exchange bit-commitments
(signed salted hashes of the data, with salt reveal delayed), to check
if they know the same information, without revealing the PII to
eachother.

To confirm Alice:

1. __A__ Send `trisanym_user` and `receive=True` to __B__`/bit-commit_1`, receive `Hash_B`.

2. __A__ Sends `H_A = Hash[ PII_A(Alice), salt_A ]` to __B__`/bit-commit_2`

3. __A__ Requests `salt_B` from __B__`/bit-commit_3`, and confirms that 
```H_mine == Hash[ PII_A(Alice), salt_B ]```

4. __A__ Sends `salt_A` to __B__`/bit-commit_4`, and receives a
deposit address if __B__ confirms the hashes match, and we marked the
user as a recipient in step 1.

To cnfirm Bob, repeat above steps with A and B swapped and
`receive=False`.


This hash-based protocol has the advantage of being zero-knowledge
while also being post-quantum (hashes dont rely on the Discrete Log
being hard.)

Zero Knowledge Proofs also to the Rescue!  Bulletproofs are
small-footprint proofs (~1 KB) which can be used to prove
set-membership, without revealing the elements to be tested.  Reasons
we might want to use a ZKP:

1. Proofs can be chained, so that if __A__ wants to send __B__ m
payments for large m, the time required for the combined proof should
scale as O(log m).  (They all fail or succeed together though.)

2. Bulletproofs are still more expensive than hashing. thus *if* there
is a way to cheaply detect wether transmitted bytes are a bulletproof
or not, this could raise the cost of DDoS attacks relative to hashing
and could serve as a proof-of-work deterrant for TRISA-abuse similar
to what hashcash tried to do for spam email.

3. Unlike the bit commitment above, a ZKP can be saved and confirmed
by an auditor who does *not* know the PII. (So maybe instead of
sending the ZKP, you can generate an audit report of ZKPs.)



### Case B. Alice & Bob provide their PII only to their respective
    VASPSs. The VASPS **do** trust each other.

This case proceeds as the normal TRISA.


### Case C. Alice & Bob provide their PII only to their respective
    VASPSs. The VASPS **do not** trust each other.

Here we need a procedure like banks go through before sending ACH
debits to banks they have never done business with.

Even if the first step can proceed via Case B, we can still use Case A
(ZK) for every subsequent transfer between Alice and Bob.  This limits
the data leaked to bad actors on TRISA-Net or someone who compromises
__B__’s TRISA server.


## Future Work

### Integration with TRISA

* Can merge the flask server with the [BIP-75 reference
implementation](https://github.com/netkicorp/addressimo/blob/master/functest/functest_bip75.py)
so the latter works with (zk-)TRISA instead of Adressimo?

* Can adopt ING's
[zkrp repo](https://github.com/ing-bank/zkrp) (which is in Go, same as
TRISA)
