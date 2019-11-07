from flask import Flask
import trisa
import pickle
import json

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

class VASPServer(Flask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        if 'users' in kwargs.keys():
            self.users = kwargs['users']
        else:
            self.users = users
        self.name = args[0]

    def print_trisanyms(self):
        return json.dumps(list(map(lambda x: x+'@' + vasp_name, self.users.keys())))

    def bit_commit(self, user, rcv=False):
        user = user.split('@')[0]
        if user not in self.users.keys(): raise ValueError('you suck')
        print(self.users[user])
        h, salt = trisa.salted_hash(self.users[user])
        #print("bit commit salt " + salt)
        pickle.dump({'salt':salt,'rcv':rcv}, open(f'{user}_{pkl_file}','wb'))
        return json.dumps({'hash':h})

    def save_hash(self, user, hash):
        if user not in self.users.keys(): raise ValueError('you really suck')
        udict = pickle.load( open(f'{user}_{pkl_file}','rb') )
        udict['cparty_hash'] = hash
        pickle.dump(udict, open(f'{user}_{pkl_file}','wb'))
        return 

    def reveal_salt(self, user):
        if user not in self.users.keys(): raise ValueError('you suck')
        udict = pickle.load( open(f'{user}_{pkl_file}','rb') )
        if 'cparty_hash' not in udict.keys(): 
            raise ValueError('sneaker. im onto you')
        if 'salt' not in udict.keys(): raise ValueError('dont know salt!')
        return json.dumps({'user':user, 'salt':udict.get('salt')})

    def confirm(self, user, cparty_salt):
        if user not in self.users.keys(): raise ValueError('you suck')
        udict = pickle.load( open(f'{user}_{pkl_file}','rb') )
        if 'cparty_hash' not in udict.keys(): 
            raise ValueError('sneaker. im onto you')
        #print("confirm salt ", cparty_salt.encode())
        print(users[user])
        candidate, _ = trisa.salted_hash(self.users[user], cparty_salt.encode())
        #candidate, _ = trisa.salted_hash(users[user], cparty_salt)
        matches = udict['cparty_hash'] == candidate
        deposit_addr = trisa.gen_btc(user) if matches and udict['rcv'] else ''
        return json.dumps({'user':user, 
                           'approved':matches, 
                           'deposit_addr':deposit_addr})

