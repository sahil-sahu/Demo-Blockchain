from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from blockchainutils import BlockchainUtils
from transaction import Transaction
from Block import Block


class Wallet():
    def __init__(self):
        self.keyPair = RSA.generate(2048)

    def fromKey(self, file):
        key = '' 
        with open(file, 'r') as keyfile:
            key = RSA.importKey(keyfile.read())
            # print(key)
        self.keyPair = key 

    def sign(self, data):
        dataHash = BlockchainUtils.hash(data)
        signatureschemeObj = PKCS1_v1_5.new(self.keyPair)
        signature = signatureschemeObj.sign(dataHash)
        return signature.hex()

    @staticmethod
    def signaturevalid(data, signature, publickeystring):
        signature = bytes.fromhex(signature)
        dataHash = BlockchainUtils.hash(data)
        publickey = RSA.importKey(publickeystring)
        signatureschemeObj = PKCS1_v1_5.new(publickey)
        signatureValid = signatureschemeObj.verify(dataHash, signature)
        return signatureValid

    def publicKeyString(self):
        publicKeyString = self.keyPair.publickey().exportKey('PEM').decode('utf-8')
        return publicKeyString

    def createTransaction(self, reciever, amount, type):
        transaction = Transaction(
            self.publicKeyString(), reciever, amount, type)
        signature = self.sign(transaction.payload())
        transaction.sign(signature)
        return transaction

    def createBlock(self, transactions, lastHash, blockCount):
        block = Block(transactions, lastHash,
                      self.publicKeyString(), blockCount)
        signature = self.sign(block.payload())
        block.sign(signature)
        return block
