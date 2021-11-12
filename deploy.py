import json
from web3 import Web3
from solcx import compile_standard, install_solc
import os
from dotenv import load_dotenv

load_dotenv()

# print("Installing...")
install_solc("0.8.2")


with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

# Get Solidity source code
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.8.2",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)


# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# establish Ganache Connection
w3 = Web3(
    Web3.HTTPProvider("https://kovan.infura.io/v3/ba470bb436554e50b1f4eb08fc956b61")
)
my_address = "0xB0A7Dd24339e078214f703fAEDB2D71b6066fEFd"
private_key = os.getenv("PRIVATE_KEY")
chain_id = 42

# Get Trasaction Count
nonce = w3.eth.getTransactionCount(my_address)

SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

print("Deploying")
# build Transaction
transaction = SimpleStorage.constructor().buildTransaction(
    {"from": my_address, "chainId": chain_id, "nonce": nonce}
)

# sign Transaction
sign_tx = w3.eth.account.sign_transaction(transaction, private_key)

# send Transaction
hash_tx = w3.eth.send_raw_transaction(sign_tx.rawTransaction)

receipt_tx = w3.eth.wait_for_transaction_receipt(hash_tx)
print(f"Contract is Successfully Deployed to: {receipt_tx.contractAddress}")

# Working With SmartContract
newValue = int(input("Pls Enter a Store Value: "))

ssContract = w3.eth.contract(abi=abi, address=receipt_tx.contractAddress)

print(f"Retrieve function value = {ssContract.functions.retrieve().call()}")


# deploying new Store Value
print("Deploying Contract")
ssContract_tx = ssContract.functions.store(newValue).buildTransaction(
    {"from": my_address, "chainId": chain_id, "nonce": nonce + 1}
)

# sign new Store Value
ssContract_sign_tx = w3.eth.account.sign_transaction(ssContract_tx, private_key)

# send Store Value
ssContract_hash_tx = w3.eth.send_raw_transaction(ssContract_sign_tx.rawTransaction)

# wait for receipt
ssContract_receipt_tx = w3.eth.wait_for_transaction_receipt(ssContract_hash_tx)

print(
    f"Contract is successfully Deployed from:{my_address} to: {receipt_tx.contractAddress}"
)

print(f"Retrieve function Updated value = {ssContract.functions.retrieve().call()}")
