from trisa import *

users = {'jake':
             {'name':'Jaek Tiernow',
              'address':'??????',
              'account':'J000000000'},
         'alice':
             {"name":"Alice Lastnamersson",
              "address":"1234 Road Rd, City XY 01234",
              "account":"A0123456789"},
         'bob':
             {"name":"Bob McSurname",
              "address":"4321 Shellcorp Ave, Town YZ 54321",
              "account":"B9876543210"},
}
#users['bob']['name'] = "Bob MacSurname"

SERVER_URL = '127.0.0.1:5000'

remote_users = requests.get(f'{SERVER_URL}')
print(f'Users on server: {remote_users}')
print()

for user in ['alice','bob']
print(f'Now requesting ')
requests


