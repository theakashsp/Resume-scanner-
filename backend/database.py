import os

try:
    from pymongo import MongoClient
    from pymongo.errors import ConnectionFailure
except ImportError:
    MongoClient = None
    ConnectionFailure = Exception

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = "careermatch_ai_db"
COLLECTION_NAME = "candidates"

client = None
db = None
collection = None

if MongoClient is not None and os.getenv("ENABLE_MONGODB", "").lower() in {"true", "1"}:
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        client.admin.command("ping")
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]
    except Exception:
        pass

# ======================================================
# 💾 DATA STORAGE FUNCTIONS
# ======================================================
def save_candidate(data: dict):
    """
    Saves the analyzed resume profile securely to the database.
    This tracks the filename, skills, predicted role, and ATS score.
    """
    try:
        result = collection.insert_one(data)
        print(f"[DB] Profile saved with ID: {result.inserted_id}")
        return True
    except Exception as e:
        print(f"[DB] Error: {e}")
        return False