from pymongo import MongoClient
from config import MONGO_URI, MONGO_DB, MONGO_COLLECTION

def main():
    print("URI leída de .env:", MONGO_URI)

    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB]
    coll = db[MONGO_COLLECTION]

    count = coll.count_documents({})
    print(f"Conexión OK. Documentos actuales en '{MONGO_COLLECTION}': {count}")

if __name__ == "__main__":
    main()