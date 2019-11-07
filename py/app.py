import json
from flask import Flask
from trisa import *
from vasp import VASPServer

#app = Flask(__name__)
pkl_file = 'db.pkl'
vasp_name = 'vasp'
users = {'jake':
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

vasp_server = VASPServer(__name__)

@vasp_server.route('/')
def print_trisanyms():
    return vasp_server.print_trisanyms()

@vasp_server.route('/bit-commit_1')
def bit_commit(user):
    return vasp_server.bit_commit(user)

@vasp_server.route('/bit-commit_2')
def save_hash(user, hash):
    return vasp_server.save_hash(user, hash)

@vasp_server.route('/bit-commit_3')
def reveal_salt(user):
    return vasp_server.reveal_salt(user)

@vasp_server.route('/bit-commit_4')
def confirm(user, cparty_salt):
    return vasp_server.confirm(user, cparty_salt)

if __name__ == '__main__':
    vasp_server.run()
