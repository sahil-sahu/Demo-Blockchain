import uuid
import time
import copy

class Transaction():
    def __init__(self, senderPublicKey, recieverPublicKey, amount, type):
        self.senderPublicKey = senderPublicKey
        self.recieverPublicKey = recieverPublicKey
        self.amount = amount
        self.type = type
        self.id = uuid.uuid1().hex
        self.timestamp = time.time()
        self.signature = ''

    def toJson(self):
        return self.__dict__

    def sign(self, sign):
        self.signature = sign

    def payload(self):
        json_representation = copy.deepcopy(self.toJson())
        json_representation['signature'] = ''
        return json_representation

    def equals(self, transaction):
        if self.id == transaction.id:
            return True

        else:
            return False    