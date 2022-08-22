import time
import copy

class Block():
    def __init__(self, transactions, lasthash, forger, blockcount):
        self.transactions = transactions
        self.lasthash = lasthash
        self.forger = forger
        self.blockcount = blockcount
        self.timestamp = time.time()
        self.signature = ''

    @staticmethod    
    def genesis():
        genesisBlock = Block([],"genesisHash", 'genesis', 0)
        genesisBlock.timestamp = 0
        return genesisBlock

    def toJson(self):
        data = {}
        data['lasthash'] = self.lasthash
        data['forger'] = self.forger
        data['blockcount'] = self.blockcount
        data['timestamp'] = self.timestamp
        data['signature'] = self.signature
        jsonTransaction = []
        for transaction in self.transactions:
            jsonTransaction.append(transaction.toJson())
        data['transactions'] = jsonTransaction
        return data    

    def payload(self):
        json_representation = copy.deepcopy(self.toJson())
        json_representation['signature'] = ''
        return json_representation

    def sign(self, signature):
        self.signature = signature
    

        

