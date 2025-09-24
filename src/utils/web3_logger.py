{\rtf1\ansi\ansicpg1252\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 from web3 import Web3\
import os\
\
class Web3Logger:\
    def __init__(self, rpc_url=None, private_key=None, address=None):\
        self.rpc_url = rpc_url or os.getenv("WEB3_RPC_URL")\
        self.private_key = private_key or os.getenv("WEB3_PRIVATE_KEY")\
        self.address = address or os.getenv("WEB3_ADDRESS")\
        if not self.rpc_url:\
            raise ValueError("WEB3_RPC_URL not provided")\
        self.w3 = Web3(Web3.HTTPProvider(self.rpc_url))\
        if not self.w3.is_connected():\
            raise ConnectionError("Could not connect to Ethereum network")\
\
    def log_hash(self, file_hash):\
        """\
        Log a file hash as a transaction on the Ethereum testnet.\
        Returns transaction hash.\
        """\
        nonce = self.w3.eth.get_transaction_count(self.address)\
        tx = \{\
            'nonce': nonce,\
            'to': self.address,  # self-transfer just to record data\
            'value': 0,\
            'gas': 21000,\
            'gasPrice': self.w3.to_wei('5', 'gwei'),\
            'data': file_hash.encode()\
        \}\
        signed_tx = self.w3.eth.account.sign_transaction(tx, private_key=self.private_key)\
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)\
        return self.w3.to_hex(tx_hash)}