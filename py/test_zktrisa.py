import vasp
import pytest
import json
import trisa

vasp_server = vasp.VASPServer('server')
'''
def test_salted_hash():
    h, salt = trisa.salted_hash("bob", "mysalt".encode())
    assert(salt == b"mysalt")

def test_salted_hash_none():
    h, salt = trisa.salted_hash("bob")
    assert(salt is not None)

'''
def test_bit_commit_nouser():
    with pytest.raises(ValueError):
        vasp_server.bit_commit("non-existent user")

def test_save_hash_nouser():
    with pytest.raises(ValueError):
        vasp_server.save_hash("non-existent user", "absfddfsdbvdfvbe")

def test_reveal_salt_nouser():
    with pytest.raises(ValueError):
        vasp_server.reveal_salt("non-existent user")

def test_confirm_nouser():
    with pytest.raises(ValueError):
        vasp_server.confirm("non-existent user", "salt")

def test_workflow():
    sender = vasp.VASPServer("A")
    receiver = vasp.VASPServer("B")

    rec_result = json.loads(receiver.bit_commit("alice"))
    rec_hash = rec_result['hash']
    sender.save_hash("alice", rec_hash)

    send_result = json.loads(sender.bit_commit("bob"))
    send_hash = rec_result['hash']
    receiver.save_hash("bob", send_hash)

    rec_salt = receiver.reveal_salt("alice")

    send_salt = sender.reveal_salt("bob")

    sender.confirm("bob", send_salt)
    receiver.confirm("alice", rec_salt)



