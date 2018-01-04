import configparser

from binascii import hexlify, unhexlify
from getpass import getpass
from simplecrypt import encrypt as _enc, decrypt as _dec, DecryptionException

from .utils import input_bool

def encrypt(password, message):
    cipher = _enc(password, message.encode('utf8'))
    return str(hexlify(cipher), 'ascii')

def decrypt(password, cipher):
    return str(_dec(password, unhexlify(cipher)), 'ascii')

class Config:
    def __init__(self, headless=False):
        ready = self._load()

        if not ready and not headless:
            self.configure()

        elif ready and self.locked() and not headless:
            self.unlock()

    def _load(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        ready = self.loaded()

        self.key = None
        self.secret = None
        if ready and not self.locked():
            self.key = self.config['creds']['key']
            self.secret = self.config['creds']['secret']

        return ready

    def loaded(self):
        return self.config.has_section('creds')

    def ready(self):
        return self.key != None and self.secret != None

    def configure(self, save=None):
        print('-- API Configuration --')

        if save == None:
            save = input_bool('Remember your credentials?', False)

        if save:
            secure = input_bool('Encrypt the API keys?', True)

            if secure:
                check = False
                password = getpass('Enter your password: ')
                while check != password:
                    check = getpass('Re-enter your password: ')
                    if check == password:
                        break

        key = input('API Key: ').strip()
        secret = input('API Secret: ').strip()

        self.key = key
        self.secret = secret

        if save:
            if secure:
                print('Encrypting your credentials...')
                key = encrypt(password, key)
                secret = encrypt(password, secret)

            creds = {'encrypted': secure, 'key': key, 'secret': secret}
            self.config['creds'] = creds
            self.config.write(open('config.ini', 'w'))

    def locked(self):
        return self.config['creds']['encrypted'] == 'True'

    def unlock(self):
        password = getpass('Enter your password: ')
        print('Unlocking encrypted credentials...')

        try:
            self.key = decrypt(password, self.config['creds']['key'])
            self.secret = decrypt(password, self.config['creds']['secret'])
        except DecryptionException:
            print('Incorrect Password!')
            exit(1)
