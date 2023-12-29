from block_chain_demo_using_flask.blockchain.block import Block


class Blockchain:
    """
    Blockchain: a public ledger of transactions.
    Implemented as a list of blocks - data sets of transactions
    """
    def __init__(self):
        self.chain = [Block.genesis()]

    def add_block(self, data):
        self.chain.append(Block.mine_block(self.chain[-1], data))

    def __repr__(self):
        return f'Blockchain: {self.chain}'

    def to_json(self):
        """
        Serialize the blockchain into a list of blocks.
        """
        serialized_blockchain_blocks = list(map(lambda block: block.to_json(), self.chain))
        return serialized_blockchain_blocks


def main():
    b = Blockchain()
    b.add_block(33)
    b.add_block(66)
    print(b.to_json())


if __name__ == '__main__':
    main()
