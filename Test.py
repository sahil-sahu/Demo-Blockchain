import random
from Lot import Lot
from ProofOfStake import ProofOfStake
import string

def getrandomString(length):
    letters = string.ascii_lowercase    
    resultString = ''.join(random.choice(letters) for i in range(length))
    return resultString

if __name__ == '__main__':
    pos = ProofOfStake()
    pos.update('bob', 100)
    pos.update('alice', 10)

    bobWins = 0
    aliceWins = 0
    for i in range(100):
        forger = pos.forger(getrandomString(i))
        if forger == 'bob':
            bobWins +=1

        elif forger == 'alice':
            aliceWins +=1   

    print(f"bob won {bobWins} times")         
    print(f"alice won {aliceWins} times")         
