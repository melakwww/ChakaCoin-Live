import firebase_admin
from firebase_admin import credentials, db

# --- INITIALIZE FIREBASE ---
cred = credentials.Certificate("dj-chaka-website-firebase-adminsdk-fbsvc-7bb7cdd281.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://dj-chaka-website-default-rtdb.europe-west1.firebasedatabase.app/'
})

# --- DELETE ALL DATA ---
try:
    # FIXED: Use .delete() instead of .set(None)
    db.reference("/").delete()
    print("🗑️ Firebase Database has been successfully emptied!")
except Exception as e:
    print(f"❌ Error emptying database: {e}")