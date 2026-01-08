import firebase_admin
from firebase_admin import credentials, db
import json
import os

# --- 1. INITIALIZE FIREBASE ---
cred = credentials.Certificate("dj-chaka-website-firebase-adminsdk-fbsvc-7bb7cdd281.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://dj-chaka-website-default-rtdb.europe-west1.firebasedatabase.app/'
})

# --- 2. LOAD LOCAL DATA ---
LOCAL_FILE = "chain_5001.json"

if os.path.exists(LOCAL_FILE):
    with open(LOCAL_FILE, 'r') as f:
        local_data = json.load(f)
    
    # --- 3. UPLOAD TO CLOUD ---
    db.reference("/blockchain").set(local_data)
    
    # Update global stats to match your 100 CHAKA height
    db.reference("/").update({
        "total_cycles_verified": len(local_data),
        "overall_status": "CORE_81_PRODUCTION_ACTIVE"
    })
    
    print(f"✅ SUCCESS: Migrated {len(local_data)} blocks to Firebase!")
else:
    print("❌ ERROR: chain_5001.json not found in this folder.")