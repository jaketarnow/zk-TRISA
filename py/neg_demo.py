import vasp
import json
import time
a_users = {'jake':
             {'name':'Jake Tarnow',
              'address':'42 Significance Pl, San Jose CA 95050',
              'account':'J1111111111'},
         'alice':
             {"name":"Alice Lastnamersson",
              "address":"1234 Road Rd, City XY 01234",
              "account":"A0123456789"},
         'bob':
             {"name":"Bob McSurname",
              "address":"4321 Shellcorp Ave, Town YZ 54321",
              "account":"B9876543210"},
}

b_users = {'jake':
             {'name':'Jake Tarnow',
              'address':'42 Significance Pl, San Jose CA 95050',
              'account':'J1111111111'},
         'alice':
             {"name":"lice Lastnamersson",
              "address":"234 Road Rd, City XY 01234",
              "account":"0123456789"},
         'bob':
             {"name":"ob McSurname",
              "address":"321 Shellcorp Ave, Town YZ 54321",
              "account":"9876543210"},
}

print("Example VASP PII Exchange between alice(sender) and bob(receiver)")
input()
print("Initializing VASP A as sending VASP")
sender = vasp.VASPServer("A", users=a_users)
print("Initializing VASP B as receiving VASP")
receiver = vasp.VASPServer("B", users=b_users)

input()

print("VASP A bit committing alice's PII on VASP B")
rec_result = json.loads(receiver.bit_commit("alice", rcv=True))
rec_hash = rec_result['hash']
print("Received hash of alice's PII from VASP B " + rec_hash)

print("Saving VASP B's hash of alice's PII on VASP A")
sender.save_hash("alice", rec_hash)
input()

print("VASP B bit committing bob's PII on VASP A")
send_result = json.loads(sender.bit_commit("bob"))
send_hash = send_result['hash']
print("Received hash of bob's PII from VASP A " + send_hash)

print("Saving VASP A's hash of alice's PII on VASP B")
receiver.save_hash("bob", send_hash)
input()

print("Now that hashes have been exchanged, salts can be exchanged")
rec_salt = json.loads(receiver.reveal_salt("alice"))
send_salt = json.loads(sender.reveal_salt("bob"))
input()

print("Confirmation by VASP A of bob's PII")
send_confirm = sender.confirm("bob", send_salt['salt'])
print(send_confirm)
print("Confirmation by VASP B of alice's PII")
rec_confirm = receiver.confirm("alice", rec_salt['salt'])
print(rec_confirm)
