import os
import firebase_admin
from firebase_admin import credentials, db

# --- FIREBASE SECURE PATH SETUP ---
# On Render, secret files are moved to /etc/secrets/
filename = "dj-chaka-website-firebase-adminsdk-fbsvc-7bb7cdd281.json"
render_path = f"/etc/secrets/{filename}"
local_path = filename 

# Tell Python to check Render's secret folder first
if os.path.exists(render_path):
    cert_path = render_path
    print("☁️ SYSTEM: Using Render Secret File")
elif os.path.exists(local_path):
    cert_path = local_path
    print("🏠 SYSTEM: Using Local JSON Key")
else:
    # This helps us see exactly where it's looking in the logs
    print(f"❌ ERROR: Key not found at {render_path} or {local_path}")
    cert_path = None

if cert_path:
    try:
        cred = credentials.Certificate(cert_path)
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://dj-chaka-website-default-rtdb.europe-west1.firebasedatabase.app/'
        })
        print("✅ Firebase Connected Successfully!")
    except Exception as e:
        print(f"Firebase Sync Error: {e}")
