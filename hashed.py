import bcrypt

def hash():
    password = 'ernest123'.encode('utf-8')
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    print(hashed.decode('utf-8'))
    
hash()
    