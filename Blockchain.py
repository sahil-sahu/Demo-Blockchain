from Block import Block
from ProofOfStake import ProofOfStake
from blockchainutils import BlockchainUtils
from Accountmodel import AccountModel


class Blockchain():
    def __init__(self):
        self.blocks = [Block.genesis()]
        self.accountModel = AccountModel()
        self.pos = ProofOfStake()

    def addBlock(self, block):
        self.executeTransactions(block.transactions)
        self.blocks.append(block)

    def toJson(self):
        data = {}
        jsonblocks = []
        for block in self.blocks:
            jsonblocks.append(block.toJson())
        data['blocks'] = jsonblocks
        return data

    def blockCountValid(self, block):
        if self.blocks[-1].blockcount == block.blockcount - 1:
            return True

        else:
            return False

    def lastBlockHashvalid(self, block):
        latestblockChainHash = BlockchainUtils.hash(
            self.blocks[-1].payload()).hexdigest()

        if latestblockChainHash == block.lasthash:
            return True

        else:
            return False

    def getCoveredTransactionSet(self, transactions):
        coveredTransaction = []
        for transaction in transactions:

            if self.transactionCovered(transaction):
                coveredTransaction.append(transaction)

            else:
                print("Transaction is not covered by sender")

        return coveredTransaction

    def transactionCovered(self, transaction):
        if transaction.type == 'EXCHANGE':
            return True
        senderBalance = self.accountModel.getBalance(
            transaction.senderPublicKey)
        if senderBalance >= transaction.amount:
            return True

        else:
            return False

    def executeTransactions(self, transactions):
        for transaction in transactions:
            self.executeTransaction(transaction)

    def executeTransaction(self, transaction):
        if transaction.type == 'STAKE':
            sender = transaction.senderPublicKey
            reciever = transaction.recieverPublicKey
            if sender == reciever:
                amount = transaction.amount
                self.pos.update(sender, amount)
                self.accountModel.updateBalance(sender, -amount)
        else:        
            sender = transaction.senderPublicKey
            reciever = transaction.recieverPublicKey
            amount = transaction.amount
            self.accountModel.updateBalance(sender, -amount)
            self.accountModel.updateBalance(reciever, amount)

    def nextForger(self):
        lastBlockHash = BlockchainUtils.hash(self.blocks[-1].payload()).hexdigest()
        nextForger = self.pos.forger(lastBlockHash)
        return nextForger

    def createBlock(self, transactionFromPool, forgerWallet):
        coveredTransactions = self.getCoveredTransactionSet(transactionFromPool)    
        self.executeTransactions(coveredTransactions)
        newBlock = forgerWallet.createBlock(coveredTransactions, BlockchainUtils.hash(self.blocks[-1].payload()).hexdigest(), len(self.blocks))
        self.blocks.append(newBlock)
        return newBlock

    def transactionExists(self, transaction):
        for block in self.blocks:
            for blockTransaction in block.transactions:
                if transaction.equals(blockTransaction):
                    return True
        return False    

    def forgerValid(self, block):
        forgerPublicKey = self.pos.forger(block.lasthash)
        proposedBlockForger = block.forger
        if forgerPublicKey == proposedBlockForger:
            return True
        else:
            return False

    def transactionsValid(self, transactions):
        coveredTransactions = self.getCoveredTransactionSet(transactions)
        if len(coveredTransactions) == len(transactions):
            return True
        return False
    