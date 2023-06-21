from web3 import Web3, HTTPProvider, middleware
import json
from web3.middleware import geth_poa_middleware
import os
# from web3.gas_strategies.time_based import medium_gas_price_strategy


def create_new_account(start_id, number):
    if os.path.exists('./accounts/' + str(start_id) + '.txt'):
        print("The start_id already exist!")
    else:
        for i in range(0, number):
            new_account = w3.eth.account.create()
            print(w3.toHex(new_account.key))
            file_handle=open('./accounts/' + str(start_id + i) + '.txt',mode='w')
            file_handle.write(w3.toHex(new_account.key))
            file_handle.close() 

def import_account(start_id, number):
        key_set = []
        for i in range(0, number):
            file_handle=open('./accounts/' + str(start_id + i) + '.txt',mode='r')
            key = file_handle.read()
            # print(key)
            pub_key = w3.eth.account.from_key(key)
            check_balance(pub_key.address)
            key_set.append(pub_key.address)
        
        return key_set

def check_balance(key):
    # acct = w3.eth.account.from_key(key)
    print('The current public key is:', key)
    print('The current balance is:')
    print(w3.fromWei(w3.eth.getBalance(key), 'ether'))

if __name__=='__main__':
    w3 = Web3(Web3.HTTPProvider("https://goerli.infura.io/v3/5e8af2ffda3341c2b8c3b262e3bf8add"))
    w3.middleware_onion.inject(geth_poa_middleware, layer = 0)
    if(w3.isConnected() == True):
        print("Connect successful!")
        
    # create_new_account(1,10)

    from_private_key = ""
    public_acc = w3.eth.account.from_key(from_private_key).address

    account_set = []
    account_set = import_account(1, 2)

    gas_price = w3.eth.gasPrice

    # 转账eth
    addresses_to_send = account_set
    balances_to_send = []
    for i in range(0,2):
        balances_to_send.append(w3.toWei(0.01, "ether"))
    print(addresses_to_send)
    addresses_to_send = ["", ""]
    balances_to_send = [w3.toWei(0.01, "ether"), w3.toWei(0.01, "ether")]

    # 构建交易数据
    for i in addresses_to_send:
        nonce = w3.eth.getTransactionCount(public_acc)
        txn ={
            "from": public_acc,
            'to': i,
            'value': w3.toWei(0.01, 'ether'),
            'gas': 21000,
            'maxFeePerGas': w3.toWei(0.001, 'gwei'),
            'maxPriorityFeePerGas': w3.toWei(0.0001, 'gwei'),
            'nonce': nonce,
            'chainId': w3.eth.chain_id 
            }

        # 发送交易
        signed_txn = w3.eth.account.sign_transaction(txn, private_key=from_private_key)
        # 发送到网络打包，如果报错 already known 就是上一笔交易正在打包，需要打包完成才能下一笔
        w3.eth.sendRawTransaction(signed_txn.rawTransaction)

        # 取得转账哈希
        txhash = w3.toHex(w3.sha3(signed_txn.rawTransaction))

        # 打印交易哈希类似 0xe382252b45073788e015d6d7e3e4847cef540ed24fa0e4c3ec43f8adaf4cd210
        print(txhash)

        while(True):
            print(w3.eth.getTransactionReceipt(txhash))
