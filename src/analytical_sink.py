import duckdb
import os
import json   # <- asegúrate de tener este import arriba

class AnalyticalSink:
    def __init__(self, db_path="analytics.duckdb"):
        self.db_path = db_path
        # Connecting creates the file if it doesn't exist
        self.conn = duckdb.connect(self.db_path)
        self._create_table()

    def _create_table(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS trips (
                event_id BIGINT,
                vehicle_id VARCHAR,
                tpep_pickup_datetime TIMESTAMP,
                tpep_dropoff_datetime TIMESTAMP,
                passenger_count INTEGER,
                trip_distance DOUBLE,
                fare_amount DOUBLE,
                total_amount DOUBLE,
                raw_event JSON
            );
        """)

    def insert_event(self, event):
        """
        Inserta un evento en la tabla trips.
        Guarda también el evento completo como JSON (raw_event).
        """
        # Convertimos a JSON, convirtiendo automáticamente cualquier tipo raro (Timestamp, etc.) a string
        raw_json = json.dumps(event, default=str)

        self.conn.execute("""
            INSERT INTO trips (
                event_id,
                vehicle_id,
                tpep_pickup_datetime,
                tpep_dropoff_datetime,
                passenger_count,
                trip_distance,
                fare_amount,
                total_amount,
                raw_event
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, [
            event.get("event_id"),
            event.get("vehicle_id"),
            event.get("tpep_pickup_datetime"),
            event.get("tpep_dropoff_datetime"),
            event.get("passenger_count"),
            event.get("trip_distance"),
            event.get("fare_amount"),
            event.get("total_amount"),
            raw_json
        ])
