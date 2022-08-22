from transaction import Transaction
from wallet import Wallet
from transactionPool import TransactionPool
from Block import Block
from pprint import pprint as prt
from Blockchain import Blockchain
from blockchainutils import BlockchainUtils
from Accountmodel import AccountModel
from node import Node
import sys


if __name__ == '__main__':

    ip = sys.argv[1]
    port = int(sys.argv[2])
    apiPort = int(sys.argv[3])
    keyfile = None
    if len(sys.argv) > 4:
        keyfile = sys.argv[4]
    node = Node(ip, port, keyfile)
    node.startP2P()
    node.startAPI(apiPort)
