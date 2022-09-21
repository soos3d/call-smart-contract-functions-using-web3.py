# Call smart contract functions using web3.py

# Introduction

So you just deployed a smart contract, but now you need a way to interact with it, let's see how to call smart contract functions using web3.py!

This tutorial shows you how you can call smart contract functions using the web3.py library. You will learn how to call view/pure functions, and functions that change the state of the blockchain. 

# Table of contents

- [Requirements](#requirements)
    - [Install Python](#install-python)
    - [Install web3.py](#install-web3py)
    - [Access a node endpoint](#access-a-node-endpoint)
  - [What is Web3.py?](#what-is-web3py)
  - [How to call smart contract functions using web3.py](#how-to-call-smart-contract-functions-using-web3py)
    - [Connect to the network](#connect-to-the-network)
    - [Initialize smart contract and account](#initialize-smart-contract-and-account)
    - [Call functions and transactions](#call-functions-and-transactions)
      - [Call a function that modifies the state](#call-a-function-that-modifies-the-state)
      - [Call a pure or view function](#call-a-pure-or-view-function)
  - [Full scripts](#full-scripts)
    - [Call view and pure functions](#call-view-and-pure-functions)
    - [Functions that change the state of the blockchain](#functions-that-change-the-state-of-the-blockchain)
  - [Conclusion](#conclusion)

# Requirements

To use `web3.py` you need:

- [Python](https://www.python.org/downloads/).
- [web3.py library](https://web3py.readthedocs.io/en/stable/quickstart.html).
- Access to an EVM node endpoint. 

### Install Python

Follow these [instructions to install Python](https://realpython.com/installing-python/) in any Operating system.

### Install web3.py

Install `web3.py` after installing Python with:

```sh
pip install web3
```

> **Note** that on Windows, you will need to install the [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) to make it work.

Then you need access to a node endpoint to connect to a blockchain.

### Access a node endpoint

To access a node endpoint, I recommend using [Chainstack](https://chainstack.com/):

Follow these steps to sign up on Chainstack, deploy a node, and find your endpoint credentials:

  1. [Sign up with Chainstack](https://console.chainstack.com/user/account/create).
  1. [Deploy a node](https://docs.chainstack.com/platform/join-a-public-network).
  1. [View node access and credentials](https://docs.chainstack.com/platform/view-node-access-and-credentials).

## What is Web3.py?

Web3.py is a Python library for interacting with the Ethereum network (Or other networks based on the EVM).

It’s commonly found in decentralized apps (dapps) to help with sending transactions, interacting with smart contracts, reading block data, and a variety of other use cases.

The original API was derived from the Web3.js Javascript API but has since evolved toward the needs and creature comforts of Python developers.

* source: [Web3.py docs](https://web3py.readthedocs.io/en/stable/)

## How to call smart contract functions using web3.py

When you use `web3.py` to interact with smart contracts, you can divide the script into three parts: 

- Connect to the network.
- Initialize the smart contract & account to sign the transactions from.
- Call functions and transactions. 

> The following examples only show the syntax and the logic; go to the [Full scripts](#full-scripts) section to find complete scripts that call real smart contract functions out of the box. 

Find all of the files in the repository as well. 

### Connect to the network

I always use this syntax to connect my scripts to a network, you can also use an environment variable, but I usually keep it simple for test scripts. 

```py
from web3 import Web3

# Initialize endpoint URL
node_url = "CHAINSTACK_NODE_URL"

# Create the node connection
web3 = Web3(Web3.HTTPProvider(node_url))
```

I usually add an if statement to give a message on the console to verify if the connection is successful (non-required but excellent for the user).

```py
# Verify if the connection is successful
if web3.isConnected():
    print("-" * 50)
    print("Connection Successful")
    print("-" * 50)
else:
    print("Connection Failed")
```

### Initialize smart contract and account

To call functions from a smart contract, we need to specify its address and ABI first. 

```py
# Initialize the address calling the functions/signing transactions
caller = "YOUR_ADDRESS"
private_key = "PRIVATE_KEY"  # To sign the transaction

# Initialize address nonce
nonce = web3.eth.getTransactionCount(caller)

# Initialize contract ABI and address
abi = '[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"balanceLeft","type":"uint256"}],"name":"balance","type":"event"},{"inputs":[{"internalType":"address payable","name":"recipient","type":"address"}],"name":"destroy","outputs":[],"stateMutability":"nonpayable","type":"function"}'

contract_address = "CONTRACT_ADDRESS"

# Create smart contract instance
contract = web3.eth.contract(address=contract_address, abi=abi)
```

### Call functions and transactions

Now we can start calling functions; we can do it two ways:

- Build a transaction to call a function that modifies the state of the network.

- `.call` in case the function is only reading from the blockchain (if it's a `view` or `pure` function). 

#### Call a function that modifies the state

For this, we need to build a transaction to send.

The following example calls a function with no parameters named `testFunc()`, but you can put any function in it and add the parameters if needed. 

```py
# initialize the chain id, we need it to build the transaction for replay protection
Chain_id = web3.eth.chain_id

# Call your function
call_function = contract.functions.testFunc().buildTransaction({"chainId": Chain_id, "from": caller, "nonce": nonce})

# Sign transaction
signed_tx = web3.eth.account.sign_transaction(call_function, private_key=private_key)

# Send transaction
send_tx = web3.eth.send_raw_transaction(signed_tx.rawTransaction)

# Wait for transaction receipt
tx_receipt = web3.eth.wait_for_transaction_receipt(send_tx)
# print(tx_receipt) # Optional
```
#### Call a pure or view function

Then if you want to call a function that only reads from the network (`view` or `pure`), you only need to "call" it since it will not make an actual transaction. 

For example the `totalSupply()` function from an ERC20 token contract.

```py
totalSupply = contract.functions.totalSupply().call()  # read the coin total supply - call means we are reading from the blockchain
print(totalSupply) 
```

## Full scripts

### Call view and pure functions

In this section, you will find the complete script example to call the `name` and `symbol` functions of the Uniswap token on the Ethereum mainnet.

```py
from web3 import Web3

# Initialize endpoint URL
node_url = "CHAINSTACK_NODE_URL"

# Create the node connection
web3 = Web3(Web3.HTTPProvider(node_url))

# Verify if the connection is successful
if web3.isConnected():
    print("-" * 50)
    print("Connection Successful")
    print("-" * 50)
else:
    print("Connection Failed")

# Initialize contract ABI and address, an ERC20 token ABI in this case
abi = '[{"inputs":[{"internalType":"address","name":"account","type":"address"},{"internalType":"address","name":"minter_","type":"address"},{"internalType":"uint256","name":"mintingAllowedAfter_","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"delegator","type":"address"},{"indexed":true,"internalType":"address","name":"fromDelegate","type":"address"},{"indexed":true,"internalType":"address","name":"toDelegate","type":"address"}],"name":"DelegateChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"delegate","type":"address"},{"indexed":false,"internalType":"uint256","name":"previousBalance","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"newBalance","type":"uint256"}],"name":"DelegateVotesChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"minter","type":"address"},{"indexed":false,"internalType":"address","name":"newMinter","type":"address"}],"name":"MinterChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Transfer","type":"event"},{"constant":true,"inputs":[],"name":"DELEGATION_TYPEHASH","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"DOMAIN_TYPEHASH","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"PERMIT_TYPEHASH","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"account","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"rawAmount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"uint32","name":"","type":"uint32"}],"name":"checkpoints","outputs":[{"internalType":"uint32","name":"fromBlock","type":"uint32"},{"internalType":"uint96","name":"votes","type":"uint96"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"delegatee","type":"address"}],"name":"delegate","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"delegatee","type":"address"},{"internalType":"uint256","name":"nonce","type":"uint256"},{"internalType":"uint256","name":"expiry","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"delegateBySig","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"delegates","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"getCurrentVotes","outputs":[{"internalType":"uint96","name":"","type":"uint96"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"account","type":"address"},{"internalType":"uint256","name":"blockNumber","type":"uint256"}],"name":"getPriorVotes","outputs":[{"internalType":"uint96","name":"","type":"uint96"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"minimumTimeBetweenMints","outputs":[{"internalType":"uint32","name":"","type":"uint32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"dst","type":"address"},{"internalType":"uint256","name":"rawAmount","type":"uint256"}],"name":"mint","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"mintCap","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"minter","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"mintingAllowedAfter","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"nonces","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"numCheckpoints","outputs":[{"internalType":"uint32","name":"","type":"uint32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"rawAmount","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"permit","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"minter_","type":"address"}],"name":"setMinter","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"dst","type":"address"},{"internalType":"uint256","name":"rawAmount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"src","type":"address"},{"internalType":"address","name":"dst","type":"address"},{"internalType":"uint256","name":"rawAmount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"}]'

contract_address = "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984"   # Uniswap token contract

# Create smart contract instance
contract = web3.eth.contract(address=contract_address, abi=abi)

# Call view or pure functions
token_name = contract.functions.name().call() 
token_symbol = contract.functions.symbol().call()

print('Name:', token_name)
print('Symbol:', token_symbol)
```

In this case we don't need to initialize and address to send a transaction since these functions don't change the state of the network. 

Run the script and see the result

```bash
python call_pure.py
```

Result:

```bash
--------------------------------------------------
Connection Successful
--------------------------------------------------
Name: Uniswap
Symbol: UNI
```

### Functions that change the state of the blockchain

To call a function that changes the state of the network, we'll need to create and send a transaction. The following example calls the function to save a number on the blockchain of a `SimpleStorage` smart contract deployed on the Goerli testnet.

`SimpleStorage` smart contract code:

```sol
// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

contract SimpleStorage {

    uint favoriteNumber;

    function saveNumber(uint _Number) public {
        favoriteNumber = _Number;
    }


    function deleteNumber() public {
        favoriteNumber = 0;
    }


    function getNumber() public view returns(uint) {
        return favoriteNumber;
    }
}
```

Find the smart contract verified and published at this address [0x37b343ddb81d67A18476d01D6e74b25655fF4A0A](https://goerli.etherscan.io/address/0x37b343ddb81d67a18476d01d6e74b25655ff4a0a#code).

```py
from web3 import Web3

# Initialize endpoint URL
node_url = "CHAINSTACK_NODE_URL"    # You will need a Goerli endpoint for this specific contract.

# Create the node connection
web3 = Web3(Web3.HTTPProvider(node_url))

# Verify if the connection is successful
if web3.isConnected():
    print("-" * 50)
    print("Connection Successful")
    print("-" * 50)
else:
    print("Connection Failed")
    
# Initialize the address calling the functions/signing transactions
caller = "YOUR_WALLET_ADDRESS"
private_key = "YOUR_PRIVATE_KEY"  # To sign the transaction

# Initialize address nonce
nonce = web3.eth.getTransactionCount(caller)

# Initialize contract ABI and address
abi = '[{"inputs":[],"name":"deleteNumber","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"getNumber","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_Number","type":"uint256"}],"name":"saveNumber","outputs":[],"stateMutability":"nonpayable","type":"function"}]'

contract_address = "0x37b343ddb81d67A18476d01D6e74b25655fF4A0A"

# Create smart contract instance
contract = web3.eth.contract(address=contract_address, abi=abi)

# initialize the chain id, we need it to build the transaction for replay protection
Chain_id = web3.eth.chain_id

# Call the saveNumber function passing 12 as a parameter
call_function = contract.functions.saveNumber(12).buildTransaction({"chainId": Chain_id, "from": caller, "nonce": nonce})

# Sign transaction
signed_tx = web3.eth.account.sign_transaction(call_function, private_key=private_key)

# Send transaction
print("Saving the number")
send_tx = web3.eth.send_raw_transaction(signed_tx.rawTransaction)

# Wait for transaction receipt
tx_receipt = web3.eth.wait_for_transaction_receipt(send_tx)
#print(tx_receipt) # Optional
print("Transacion successful")

# Verify that the number was saved by calling the getNumber() function
print("Retriving saved number...")

number_saved = contract.functions.getNumber().call() 
print(f'The saved number is: {number_saved}')
```

Now you can save and run the script.

```bash
python call_function.py
```

You'll see this result:

```bash
--------------------------------------------------
Connection Successful
--------------------------------------------------
Saving the number
Transacion successful
Retriving saved number...
The saved number is: 12
```

So, in this case, we call a function named `saveNumber()`, where we change the state of the network, and then we call a view function to see the number we saved. In the first case, we need a transaction since we change the state of the blockchain.

## Conclusion

Congratulations on getting to the end of this tutorial! Today you learned how to interact with smart contracts using the `web3.py` library in Python, and you are a step closer to becoming a blockchain developer.
