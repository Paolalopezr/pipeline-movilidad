from pymongo import MongoClient
from config import MONGO_URI, MONGO_DB, MONGO_COLLECTION

class OperationalSink:
    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client[MONGO_DB]
        self.collection = self.db[MONGO_COLLECTION]

    def upsert_vehicle_state(self, event):
        """
        Guarda o actualiza el último estado del vehículo.
        Se usa vehicle_id como clave única.
        """
        vehicle_id = event.get("vehicle_id")

        if not vehicle_id:
            print("Evento sin vehicle_id, ignorado.")
            return

        self.collection.update_one(
            {"vehicle_id": vehicle_id},
            {"$set": event},
            upsert=True
        )

        print(f"Actualizado estado del vehículo {vehicle_id}")
