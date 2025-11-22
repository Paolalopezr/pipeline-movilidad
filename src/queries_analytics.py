import duckdb

con = duckdb.connect("analytics.duckdb")

print("\n=== 1. Total de viajes por hora (pickup) ===")
print(con.execute("""
    SELECT 
        EXTRACT(hour FROM tpep_pickup_datetime) AS hour,
        COUNT(*) AS total_trips
    FROM trips
    GROUP BY hour
    ORDER BY hour;
""").fetchall())


print("\n=== 2. Distancia total por vehículo ===")
print(con.execute("""
    SELECT 
        vehicle_id,
        SUM(trip_distance) AS total_distance
    FROM trips
    GROUP BY vehicle_id
    ORDER BY total_distance DESC
    LIMIT 5;
""").fetchall())


print("\n=== 3. Duración promedio del viaje (en minutos) ===")
print(con.execute("""
    SELECT 
        AVG(EXTRACT(epoch FROM (tpep_dropoff_datetime - tpep_pickup_datetime)) / 60) 
        AS avg_duration_minutes
    FROM trips;
""").fetchall())


print("\n=== 4. Ingresos promedio (total_amount) ===")
print(con.execute("""
    SELECT AVG(total_amount) FROM trips;
""").fetchall())


print("\n=== 5. Top 5 zonas de origen más frecuentes (pickup) ===")
print(con.execute("""
    SELECT 
        passenger_count,
        COUNT(*) AS total
    FROM trips
    GROUP BY passenger_count
    ORDER BY total DESC
    LIMIT 5;
""").fetchall())

