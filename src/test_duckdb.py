import duckdb

con = duckdb.connect("analytics.duckdb")

print("\nTotal registros en trips:")
print(con.execute("SELECT COUNT(*) FROM trips").fetchall())

print("\nDistancia promedio:")
print(con.execute("SELECT AVG(trip_distance) FROM trips").fetchall())

print("\nTop 5 viajes más largos:")
print(con.execute("SELECT vehicle_id, trip_distance FROM trips ORDER BY trip_distance DESC LIMIT 5").fetchall())
