import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Initialize the Firebase Admin SDK
cred = credentials.Certificate('./py-url-shortener-firebase-adminsdk-u8z45-44b6a43557.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://py-url-shortener-default-rtdb.firebaseio.com'
})

urlRef = db.reference('urlPairs')
statsRef = db.reference('stats')

def get_all():
    data = urlRef.get()
    return data

def read_one(key):
    data = urlRef.get()
    return data[key]

def write(key, value):
    urlRef.child(key).set(value)

def check_exists(key):
    data = urlRef.get()
    try:
        return key in data
    except TypeError:
        return False
    
def log_stats(key):
    current_stats = statsRef.get()
    if key in current_stats:
        statsRef.child(key).set(current_stats[key] + 1)
    else:
        statsRef.child(key).set(1)
    
def get_stats(key):
    data = statsRef.get()
    return data[key]