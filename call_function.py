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

contract_address = "0x37b343ddb81d67A18476d01D6e74b25655fF4A0A"  # SimpleStorage contract deployed and verified on Goerli

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
