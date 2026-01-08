import hashlib, datetime, ecdsa, json, os
import firebase_admin
from firebase_admin import credentials, db

# --- FIREBASE CLOUD SETUP ---
try:
    cred = credentials.Certificate("dj-chaka-website-firebase-adminsdk-fbsvc-7bb7cdd281.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://dj-chaka-website-default-rtdb.europe-west1.firebasedatabase.app/'
    })
except Exception as e:
    print(f"Firebase Sync Error: {e}")

# (Standard Wallet, Transaction, and Block classes remain the same)

class Blockchain:
    def __init__(self):
        self.ref = db.reference("/")
        self.chain = []
        self.mempool = []
        self.difficulty = 4
        self.load_chain()

    def get_leaderboard(self):
        """Calculates top miners from reward transactions"""
        scores = {}
        for block in self.chain:
            for tx in block.transactions:
                if tx.sender == "SYSTEM": # Identify rewards
                    scores[tx.receiver] = scores.get(tx.receiver, 0) + tx.amount
        # Return top 5 addresses sorted by total mined
        return sorted(scores.items(), key=lambda x: x[1], reverse=True)[:5]

    def get_balance(self, address):
        balance = 0
        for block in self.chain:
            for tx in block.transactions:
                if tx.receiver == address: balance += tx.amount
                if tx.sender == address: balance -= tx.amount
        return balance

    def mine_pending_transactions(self, miner_address=None):
        if not self.chain: self.chain = [Block([], "0")]
        if miner_address: self.mempool.append(Transaction("SYSTEM", miner_address, 50))
        new_block = Block(self.mempool, self.chain[-1].hash)
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        self.mempool = []
        self.save_chain()

    def save_chain(self):
        data = [block.to_dict() for block in self.chain]
        self.ref.child("blockchain").set(data)
        self.ref.update({
            "last_sync": str(datetime.datetime.now().strftime("%H:%M:%S")),
            "total_cycles_verified": len(self.chain)
        })

    def load_chain(self):
        cloud_data = self.ref.child("blockchain").get()
        if cloud_data:
            self.chain = []
            for b in cloud_data:
                txs = [Transaction(t['sender'], t['receiver'], t['amount'], t['signature']) for t in b['transactions']]
                self.chain.append(Block(txs, b['previous_hash'], b['timestamp'], b['nonce'], b['hash']))
        else:
            self.chain = [Block([], "0")]