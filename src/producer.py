import time
import pandas as pd
import os
from config import RAW_DATA_DIR
from operational_sink import OperationalSink
from analytical_sink import AnalyticalSink

def read_parquet_sample(file_name: str, limit: int = 100):
    file_path = os.path.join(RAW_DATA_DIR, file_name)
    print(f"Leyendo archivo: {file_path}")

    df = pd.read_parquet(file_path)

    # Normalizamos un vehicle_id artificial si no existe
    df["vehicle_id"] = df.index.astype(str)
    df["event_id"] = df.index

    df = df.head(limit)
    return df.to_dict(orient="records")

def simulate_stream(events, delay: float = 0.2):
    op_sink = OperationalSink()     # Mongo (último estado)
    an_sink = AnalyticalSink()      # DuckDB (histórico)

    for idx, event in enumerate(events, start=1):
        print(f"\n[{idx}] Evento enviado: {event.get('vehicle_id')}")

        # Camino Operacional
        op_sink.upsert_vehicle_state(event)

        # Camino Analítico
        an_sink.insert_event(event)

        print("✓ Guardado en análisis")

        time.sleep(delay)

if __name__ == "__main__":
    events = read_parquet_sample("yellow_tripdata_2023-01.parquet", limit=20)

    print(f"\nTotal eventos a transmitir: {len(events)}")
    simulate_stream(events, delay=0.3)

