import time
import uuid

from wallet.wallet import Wallet


class Transaction:
    """
    Document of an exchange in currency from a sender to one
    or more recipients.
    """
    def __init__(self, sender_wallet=None, recipient=None, amount=None, id=None, output=None, input=None):
        self.id = id or str(uuid.uuid4())[0:8]
        self.output = output or self.create_output(
            sender_wallet,
            recipient,
            amount
        )
        self.input = input or self.create_input(sender_wallet, self.output)

    def update(self, sender_wallet, recipient, amount):
        """
        Update the transaction with an existing or new recipient.
        """
        if amount > self.output[sender_wallet.address]:
            raise Exception('Amount exceeds balance')

        if recipient in self.output:
            # if same recipient amount gets added to same user (same key gets updated)
            # output:{"recipient":20+ 20}
            self.output[recipient] = self.output[recipient] + amount
        else:
            self.output[recipient] = amount   # for different recipient (recipient changes so new key will be added)

        self.output[sender_wallet.address] = self.output[sender_wallet.address] - amount
        # remaining amount of wallet gets updated for output block/dictionary

        self.input = self.create_input(sender_wallet, self.output)
        # with the generated new self.output, the new self.input created

    def to_json(self):
        """
        Serialize the transaction.
        # converts the object into its serialized form, means into its attributes as dictionary data type
        """
        return self.__dict__

    def create_output(self, sender_wallet, recipient, amount):
        """
        Structure the output data for the transaction.
        """
        if amount > sender_wallet.balance:
            raise Exception('Amount exceeds balance')

        output = {}
        # Empty dict
        output[recipient] = amount
        output[sender_wallet.address] = sender_wallet.balance - amount
        return output

    def create_input(self, sender_wallet, output):
        """
        Structure the input data for the transaction.
        Sign the transaction and include the sender's public key and address
        """
        return {
            'timestamp': time.time_ns(),
            'amount': sender_wallet.balance,
            'address': sender_wallet.address,
            'public_key': sender_wallet.public_key,
            'signature': sender_wallet.sign(output)   # sign the output dictionary
        }


def main():
    transaction = Transaction(Wallet(), 'recipient', 15)
    print(f'transaction.__dict__: {transaction.to_json()}')


if __name__ == '__main__':
    main()
