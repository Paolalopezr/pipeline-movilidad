import duckdb
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

def load_data():
    con = duckdb.connect("analytics.duckdb")

    query = """
        SELECT
            event_id,
            vehicle_id,
            trip_distance,
            passenger_count,
            total_amount,
            EXTRACT(hour FROM tpep_pickup_datetime) AS pickup_hour
        FROM trips
        WHERE trip_distance IS NOT NULL
          AND total_amount IS NOT NULL
          AND passenger_count IS NOT NULL;
    """

    df = con.execute(query).df()
    return df

def prepare_data(df: pd.DataFrame):
    # Features (X) y variable objetivo (y)
    X = df[["trip_distance", "passenger_count", "pickup_hour"]]
    y = df["total_amount"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )
    return X_train, X_test, y_train, y_test

def train_model(X_train, y_train):
    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print("\n=== Evaluación del modelo de ML ===")
    print(f"MAE (error absoluto medio): {mae:.2f}")
    print(f"R2 (coeficiente de determinación): {r2:.3f}")

def predict_example(model):
    # Ejemplo: viaje de 5km, 2 pasajeros, a las 8am
    example = pd.DataFrame(
        {"trip_distance": [5.0], "passenger_count": [2], "pickup_hour": [8]}
    )
    pred = model.predict(example)[0]
    print("\nEjemplo de predicción:")
    print(f"Viaje de 5km, 2 pasajeros, 8am → total_amount estimado: {pred:.2f} USD")

if __name__ == "__main__":
    df = load_data()
    print(f"Registros cargados para ML: {len(df)}")

    if len(df) < 10:
        print("Muy pocos datos para entrenar un modelo robusto, "
              "pero se ejecutará como demostración.")
    X_train, X_test, y_train, y_test = prepare_data(df)
    model = train_model(X_train, y_train)
    evaluate_model(model, X_test, y_test)
    predict_example(model)
