import hashlib, datetime, ecdsa, json, os
import firebase_admin
from firebase_admin import credentials, db

# --- FIREBASE CLOUD SETUP ---
# On Render, secret files are placed in /etc/secrets/
filename = "dj-chaka-website-firebase-adminsdk-fbsvc-7bb7cdd281.json"
render_path = f"/etc/secrets/{filename}"
local_path = filename # File in current directory for local testing

# Choose the path that exists
if os.path.exists(render_path):
    cert_path = render_path
    print("☁️ SYSTEM: Running on Render (using /etc/secrets/)")
elif os.path.exists(local_path):
    cert_path = local_path
    print("🏠 SYSTEM: Running locally (using local directory)")
else:
    cert_path = None
    print(f"❌ ERROR: Service key NOT found at {render_path} or {local_path}")

try:
    if cert_path:
        cred = credentials.Certificate(cert_path)
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://dj-chaka-website-default-rtdb.europe-west1.firebasedatabase.app/'
        })
        print("✅ Firebase Connected Successfully!")
    else:
        print("⚠️ Firebase initialization skipped: No credentials file found.")
except Exception as e:
    print(f"Firebase Sync Error: {e}")

# (Standard Wallet, Transaction, and Block classes remain the same)
# ... [Rest of your Blockchain class code continues below]
