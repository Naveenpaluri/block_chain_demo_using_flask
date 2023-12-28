import json
from flask import Flask, request, render_template, jsonify
from blockchain.blockchain import Blockchain
from wallet.wallet import Wallet
from wallet.transaction import Transaction
from wallet.transactionpool import TransactionPool

app = Flask(__name__)
blockchain = Blockchain()           # Blockchain object
wallet = Wallet(blockchain)         # Wallet object, instance and blockchain instance is passed
transaction_pool = TransactionPool()   # Transaction pool object


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/send')     # redirects  the form requests to the wallet_transact method in main.py
def send_crypto():
    return render_template('transaction.html')


@app.route('/mine')    # redirects the form button to the blockchain_mine method in main.py
def mine_the_block():
    return render_template('mine_the_block.html', block=transaction_pool.transaction_data())


@app.route('/chain')
def get_blockchain():
    return render_template('blockchain.html', chain=blockchain.to_json())
    # blockchain object has to_json() blockchain.to_json()
    # return jsonify(blockchain.to_json())


@app.route('/mine/block', methods=['POST'])
def blockchain_mine():
    transaction_data = transaction_pool.transaction_data()
    # gets the data inside the map dictionary
    blockchain.add_block(transaction_data)
    # add transaction to block, means mining into new block
    block = blockchain.chain[-1]
    # Last block is the last element of the blockchain list
    transaction_pool.clear_blockchain_transactions(blockchain)
    # after mining remove the data from dictionary
    return render_template('mineblock.html', block=json.dumps(block.to_json()))
    # html render where the block parameter here passed to template html


@app.route('/transfer', methods=['POST'])
def wallet_transact():
    # transaction_data = request.get_json()  # gets json data from postman
    transaction_data = request.form     # gets the data in json format from form
    transaction = transaction_pool.existing_transaction(wallet.address)
    """
    checks the transaction pool have already has transaction or else add a new transaction
    for after every mine the transaction pool get reset
    """
    if transaction:
        transaction.update(
            wallet,
            transaction_data['recipient'],
            int(transaction_data['amount'])
        )
    else:
        transaction = Transaction(
            wallet,
            transaction_data['recipient'],
            int(transaction_data['amount'])
        )
    transaction_pool.set_transaction(transaction)       # set transaction ( make into dictionary )
    return render_template('send_success.html',
                           transaction=transaction.id,
                           address=transaction_data['recipient'],
                           amount=transaction.output[transaction_data['recipient']],
                           balance=transaction.output[wallet.address])
    # html render where the transaction parameter here passed to template html


@app.route('/balance')
def wallet_info():
    return render_template('wallet_info.html', address=wallet.address,
                           balance=wallet.balance)
    # html render where the address and balance are passed to template html


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
