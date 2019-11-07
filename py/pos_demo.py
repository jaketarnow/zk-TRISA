import vasp
import json
import time

print("Example VASP PII Exchange between alice(sender) and bob(receiver)")
input()
print("Initializing VASP A(sending VASP)")
sender = vasp.VASPServer("A")
print("Initializing VASP B(receiving VASP)")
receiver = vasp.VASPServer("B")

input()
print("VASP A sends alice's trisanym to VASP B")
input()

print("VASP B calculates hash of alice's PII and saves it")
rec_result = json.loads(receiver.bit_commit("alice", rcv=True))
input()
rec_hash = rec_result['hash']

print("VASP A receives and saves VASP B's hash of alice's PII")
sender.save_hash("alice", rec_hash)
input()
print("VASP B sends bob's trisanym to VASP B")
input()

print("VASP A calculates hash of bob's PII and saves it")
send_result = json.loads(sender.bit_commit("bob"))
input()
send_hash = send_result['hash']

print("VASP B receives and saves VASP A's hash of bob's PII")
receiver.save_hash("bob", send_hash)
input()

print("Now that hashes have been exchanged, salts can be exchanged")
rec_salt = json.loads(receiver.reveal_salt("alice"))
send_salt = json.loads(sender.reveal_salt("bob"))
input()

print("Confirmation by VASP A of bob's PII")
send_confirm = sender.confirm("bob", send_salt['salt'])
print(send_confirm)
input()
print("Confirmation by VASP B of alice's PII")
rec_confirm = receiver.confirm("alice", rec_salt['salt'])
print(rec_confirm)
input()
