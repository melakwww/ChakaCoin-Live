import hashlib
import json

def python_mine_block(block_number, transactions, previous_hash, difficulty):
    """
    A pure Python replacement for chaka_miner.dll.
    Mines a block by finding a nonce that satisfies the difficulty.
    """
    nonce = 0
    target = "0" * difficulty
    
    print(f"⛏️ Mining Block {block_number} with difficulty {difficulty}...")

    while True:
        # 1. Create the data string to hash
        block_data = {
            'index': block_number,
            'transactions': transactions,
            'prev_hash': previous_hash,
            'nonce': nonce
        }
        
        # 2. Sort keys to ensure consistent hashing
        block_string = json.dumps(block_data, sort_keys=True)
        
        # 3. Calculate SHA-256 hash
        block_hash = hashlib.sha256(block_string.encode()).hexdigest()
        
        # 4. Check if we won
        if block_hash.startswith(target):
            print(f"✅ Block Mined! Nonce: {nonce}")
            print(f"🔑 Hash: {block_hash}")
            return nonce, block_hash
            
        nonce += 1
