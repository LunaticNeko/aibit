from hashlib import sha256
from datetime import datetime
from abc import ABC, abstractmethod # This imports abstract class system
import copy

# TO START AUTOMATIC DEMO, fire this up using Python console in INTERACTIVE MODE
# using:
#
# python -i aibit.py
#
# and type:
# >>> automatic_demo()
#
# Otherwise, have fun!

# ONE MORE THING: For purpose of demonstration, I have deliberately excluded
# the timestamp from the hash function. This is to ensure that automatic grading
# or whatever works, and that debugging student work is possible, within limits.

# ------------------------------------------------------------------------------

# Set this to True if you want more messages. Set to True by default because
# this is an educational software.
VERBOSE = True

# This is mining difficulty. Higher means harder. Don't set it too high or new
# blocks will be too hard to create!
DIFF = 3

# This governs how many letters are shown in the back of a hash when it is
# abbreviated. IMPORTANT: DIFF + TAIL_DISPLAY must not be greater than 64, for
# it is the length of SHA-256 hash when printed in hexadecimal.
TAIL_DISPLAY = 4

assert DIFF+TAIL_DISPLAY <= 64

class Block(ABC):
    pass

def bchash(block: Block) -> str:
    # For purpose of demonstration, we have excluded the timestamp from hashing.
    s = repr((block.message,
              block.number,
              block.previoushash,
              block.nonce
              ))
    result_hash = sha256(bytes(s, encoding="UTF_8")).hexdigest()
    return result_hash

def format_hash(h: str, head=DIFF, tail=TAIL_DISPLAY) -> str:
    if head < len(h)-tail:
        return "{0:s}...{1:s}".format(h[:head], h[-tail:])
    else:
        return h

class Block:
    nonce = 0

    def mine(self):
        # Mining is simply finding a nonce value that makes the hash valid.
        # A valid hash in our system requires four consecutive zeroes at the
        # front of the SHA-256 hash. We'll run the nonce from 0 to infinity.
        if VERBOSE:
            print("Attempting to Mine Block #{0:d}".format(self.number))
        h = bchash(self)
        while h[:DIFF] != '0'*DIFF:
            self.nonce += 1
            h = bchash(self)
            if VERBOSE:
                print("\rHash of Block #{0:d} with nonce {1:d} is {2:s}".format(self.number, self.nonce, h), end='\r')
        if VERBOSE:
            print()
        return h

    def __str__(self):
        if self.previoushash is None:
            return "| Block No. {0:d}\n| Previous Hash: None (this is Genesis)\n| Nonce: {1:d}\n| Hash: {2:s} \n| Message: {3:s}" \
                    .format(self.number, self.nonce, format_hash(self.hash), self.message)
        else:
            return "| Block No. {0:d}\n| Previous Hash: {1:s}\n| Nonce: {2:d}\n| Hash: {3:s}\n| Message: {4:s}" \
                    .format(self.number, format_hash(self.previoushash), self.nonce, format_hash(self.hash), self.message)

    def __init__(self, message=None, previousblock=None, automine=True, setnonce=None):
        self.timestamp = int(datetime.now().timestamp())
        self.message = str(message) if message is not None else ''
        assert (type(previousblock) is Block) or (previousblock is None)
        if type(previousblock) is Block:
            self.number = previousblock.number + 1
            self.previoushash = previousblock.hash
        elif previousblock is None:
            self.number = 0
            self.previoushash = None
        if setnonce is None:
            self.nonce = 0
        else:
            self.nonce = setnonce
        if automine:
            self.hash = self.mine()

def automatic_demo():
    global VERBOSE
    temp_VERBOSE = VERBOSE
    VERBOSE = True

    bc = [] # We will use this to represent a blockchain.

    print("This is an automatic demo. Press ENTER to continue. [ENTER]")
    input()
    print("By the way, you can leave this demo anytime by pressing Ctrl+C.")
    print("OK. I'll first create a Genesis Block. Here goes.\n")

    genesis_block = Block("GENESIS", None)
    bc.append(genesis_block)

    print(("\nDo you see the funny long number? That's called the hash. It\n"
           "is basically the fingerprint of data blocks. If you change even\n"
           "a bit in the data, the whole hash will change. This will serve as\n"
           "the foundation for the whole blockchain system.\n\n"
           "To ensure that blocks are hard enough to generate, and that some\n"
           "work is put into generating a block, the protocol usually defines\n"
           "some sort of DIFFICULTY level.\n"))
    print("In our case, the DIFFICULTY level is set to {0:d}.".format(DIFF))
    print(("The meaning is that each block's hash must have >= {0:d} zeroes \n"
           "in front of it.".format(DIFF)))

    print("\nHere's the genesis block.\n")
    print(genesis_block)

    print("[ENTER]")
    input()

    print(("I'll talk a bit more precisely about hash functions.\n"
           "Based on Merkle (2001) (I paraphrased a lot), a hash function:\n"
           "1. Must work with data of any length.\n"
           "2. Must always produce output of the same length. In this case,\n"
           "   use SHA-256 (like Bitcoin), so the output is always 256-bit.\n"
           "3. It's simple to find a hash h(x) based on data x.\n"
           "4. Property of COLLISION-PROOF: It's hard to find two sets of\n"
           "   different data x1 and x2 where h(x1) == h(x2). In other words,\n"
           "   different data should always produce different hash!\n"
           "5. Also (Merkle didn't say this), property of IRREVERSIBILITY:\n"
           "   You cannot easily find original data x based on hash h(x).\n"
           "6. Furthermore, a good hash function has some sort of AVALANCHE\n"
           "   This means even smallest changes produce completely different\n"
           "   hashes. Just one bit of change. I'll show you."
           "n.b. The bibliography is in the source code.\n[ENTER]\n"
         ))
    input()

    print(("So, it's time for me to show a bit what AVALANCHE means. I'll\n"
           "make two fake blocks."
         ))

    fake_block_1 = Block("GENES1S", None, automine=False, setnonce=genesis_block.nonce)
    fake_block_2 = Block("GENESIS", None, automine=False, setnonce=99999999)

    fake_block_1.hash = bchash(fake_block_1)
    fake_block_2.hash = bchash(fake_block_2)

    print()
    print("Fake block 1 (altered message, same nonce)")
    print(fake_block_1, end="\n\n")
    print("Full hash: {0:s}".format(bchash(fake_block_1)))

    print()
    print("Fake block 2 (altered nonce, same message)")
    print(fake_block_2, end="\n\n")
    print("Full hash: {0:s}".format(bchash(fake_block_2)))

    print(("\nAs you can see, these two new blocks have altered content. Even\n"
           "though the change is very slight, the hash completely changes.\n"
           "This means the hash can be used to determine if the data is not\n"
           "altered or modified."))

    print("\nLet me know when you're ready to continue. [ENTER]")
    input()

    print("Let's make another block. This time, you type the message.")
    block2_msg = input("Your message: ")
    print()

    block2 = Block(block2_msg, genesis_block)
    bc.append(block2)

    print("\nNow that's a good block! Let's see.\n")
    print(block2)

    print(("\nAs you can see, we refer to the previous block by its hash, and\n"
           "use this reference to maintain the continuity of the block.\n"))
    print("We'll create a few more blocks. I'll do it automatically. [ENTER]")

    input()

    for i in range(4):
        newblock = Block("This is block {0:d}".format(i+3), bc[-1])
        bc.append(newblock)
        print()


    print("And we're done. I'll show you the whole blockchain. [ENTER]")
    input()

    for block in bc:
        print(block)
        print()

    print(("You'll notice that the prevous-hash of block N must equal to the\n"
           "hash of block N-1. This is what helps maintain the integrity of\n"
           "the blockchain.\n"))
    print(("Things can get complicated when there are more users in the\n"
           "system. For those topics, we will discuss later physically, or\n"
           "you can also read more online.\n"))
    print(("Goodbye for now. This is the end of the tutorial. [Exit: ENTER]"))
    input()
    print()

    VERBOSE = temp_VERBOSE



# Bibliography
# R.C. Merkle. 1990. One Way Hash Functions and DES. In: Brassard G. (eds)
#   Advances in Cryptology -- Crypto' 89 Proceedings.
#   doi:10.1007/0-387-34805-0_40
