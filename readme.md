# Prueba técnica - Ingeniero de Datos Senior - Simon Movilidad

## 1. Descripción general

Este proyecto es mi propuesta de solución para la prueba técnica,  diseñé e implementé un **pipeline de datos en streaming simulado** que toma viajes de taxis desde un archivo Parquet y los envía a dos caminos distintos:

Mi solución divide el pipeline en dos rutas complementarias, cada una cumpliendo un propósito específico dentro de un escenario de movilidad. Uso tecnologías ligeras, gratuitas y fáciles de desplegar, pero pensando en una arquitectura que puede crecer hacia entornos de alta escala como Kafka, Data Lakehouse, o APIs en tiempo real.

1. Camino Operacional – Último estado del vehículo (MongoDB Atlas)
Este camino está orientado a la operación en tiempo real.
Por cada evento procesado, guardo únicamente el último estado conocido del vehículo, lo que permite responder preguntas inmediatas como:
-“¿Dónde estuvo el vehículo X por última vez?”
-“¿Cuál es el último viaje procesado del vehículo?”
-“¿Qué vehículo no ha generado eventos recientemente?”

Para esto utilizo MongoDB Atlas, una base documental en la nube ideal para almacenar objetos JSON y actualizar registros rápido mediante upsert.

2. Camino Analítico – Histórico completo para análisis y ML (DuckDB)
Este segundo camino tiene un propósito distinto: almacenar toda la historia de los eventos, sin perder ningún dato, para permitir:
-Consultas analíticas y agregaciones.
-Exploración del comportamiento de viajes.
-Preparación de datos para modelos predictivos.
-Auditoría y trazabilidad del flujo.
Para esto empleo DuckDB, un motor analítico embebido que trabaja con archivos locales y formato columnar,cada evento se guarda en la tabla trips, incluyendo distancia del viaje, pasajeros, montos, tiempos de pickup y dropoff y  el evento completo como JSON (raw_event), dando como resultado una mini base de datos histórica que sirve como “fuente única de verdad” para análisis.

Mi objetivo fue que la solución fuera:

- **Realista** (uso datos reales de taxis de NYC).
- **Simple de desplegar** (todo corre en local + MongoDB Atlas free tier).
- **Crecible a futuro** hacia arquitecturas con Kafka, APIs o dashboards.

3. Quise dar un valor agregado a la prueba y fue Valor y fue implementando un Módulo de Machine Learning integrado al pipeline, este modulo o  componente de IA/ML que potencia la utilidad del pipeline y lo acerca a un caso real de analítica predictiva y se alimenta directamente  del camino analítico (DuckDB), muestra métricas (MAE, R²) y predicciones.

Como opera:
Entreno un Random Forest Regressor capaz de estimar el costo total del viaje (total_amount) a partir de características clave:
-Distancia del viaje (trip_distance)
-Cantidad de pasajeros (passenger_count)
-Hora del día del pickup (pickup_hour)

Obejetivo principal: Es un valor diferencial que muestra dominio no solo de ingeniería de datos, sino también de Data Analytics y ML aplicado.

## 2. Arquitectura y flujo de datos

### 2.1. Diagrama lógico 

```text
             +---------------------------+
             |     Producer (Python)     |
             |  Lee Parquet y simula un  |
             |          stream           |
             +--------------+------------+
                            |
                            |  Evento (dict Python)
                +-----------+-----------+
                |                       |
        +-------v--------+      +-------v--------+
        | Operational    |      | Analytical     |
        | Sink (MongoDB) |      | Sink (DuckDB)  |
        | Último estado  |      | Histórico      |
        +----------------+      +----------------+

### 2.2. Flujo en orden

1.Lectura del dataset de viajes

-Uso el archivo data/raw/yellow_tripdata_2023-01.parquet (viajes de taxi de NYC).

-Con pandas convierto el Parquet en un DataFrame y de ahí en una lista de eventos (diccionarios).

2. Simulación del stream

-El script producer.py recorre los eventos uno a uno y hace un time.sleep entre ellos para simular un flujo continuo.

3. Camino operacional (MongoDB)

-Por cada evento llamo a OperationalSink.upsert_vehicle_state(event).

-Se identifica el vehículo con el campo vehicle_id y se hace un update_one(..., upsert=True).

-De esta forma, en la colección vehicle_last_trip siempre tengo el último registro conocido de cada vehículo.

4. Camino analítico (DuckDB)

-Por el mismo evento llamo a AnalyticalSink.insert_event(event).

-Inserto el registro en la tabla trips del archivo analytics.duckdb.

-Esta tabla guarda el histórico completo y sirve para consultas analíticas y para entrenar un modelo de ML.

5.0Consultas analíticas

-Con el script queries_analytics.py lanzo queries en DuckDB (viajes por hora, distancias, duración promedio, entre otros.).

6. Componente de Machine Learning

En ml_experiment.py leo datos desde DuckDB, preparo un dataset y entreno un RandomForestRegressor que estima el total_amount de un viaje a partir de trip_distance, passenger_count y la hora de inicio (pickup_hour).


## 3. Tecnologías utilizadas

-Lenguaje: Python 3

-Gestión de dependencias: venv + pip

-Procesamiento de datos: pandas, pyarrow

-Almacén operacional:

MongoDB Atlas (Free Tier)

Cliente Python: pymongo[srv]

-Almacén analítico:

DuckDB (archivo local analytics.duckdb)

Configuración / secretos:

Archivo .env + librería python-dotenv

-Machine Learning:

scikit-learn (RandomForestRegressor)

Entorno de análisis opcional:

Jupyter Notebook (para extender el análisis si es necesario)

## 4. Estructura del proyecto por carpeta y archivo

pipeline_movilidad/
├─ data/
│  └─ raw/
│     └─ yellow_tripdata_2023-01.parquet     # Dataset de viajes (fuente simulada de stream)
├─ src/
│  ├─ config.py                              # Carga de configuración (.env, rutas)
│  ├─ producer.py                            # Productor de eventos (lee Parquet y envía a ambos sinks)
│  ├─ operational_sink.py                    # Conector a MongoDB (último estado del vehículo)
│  ├─ analytical_sink.py                     # Conector a DuckDB (tabla trips, histórico de viajes)
│  ├─ test_mongo.py                          # Prueba de conexión a MongoDB
│  ├─ test_duckdb.py                         # Prueba de conexión y consultas básicas en DuckDB
│  ├─ queries_analytics.py                   # Consultas analíticas de ejemplo
│  └─ ml_experiment.py                       # Experimento sencillo de ML (Random Forest)
├─ .env                                      # Variables de entorno (URI de Mongo, etc.)
├─ requirements.txt                          # Dependencias de Python
└─ README.md                                 # Este documento

## 5. Configuración y ejecución

 5.1. Crear entorno y activar
```bash
python -m venv .venv
.\.venv\Scripts\activate

5.2. Instalar dependencias
pip install -r requirements.txt

5.3. Configurar variables de entorno (.env)
MONGO_URI="mongodb+srv://paolaferlopez25_db_user:PruebaMongo2025@clustersimon.ndtwvgk.mongodb.net/?retryWrites=true&w=majority&appName=Clustersimon"
MONGO_DB=movilidad
MONGO_COLLECTION=vehicle_last_trip

5.4. Colocar el dataset
Descargar:
https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-01.parquet
Guardar en
data/raw/yellow_tripdata_2023-01.parquet

5.5. Probar conexiones
python src/test_mongo.py
python src/test_duckdb.py

5.6. Ejecutar el pipeline (stream simulado)
python src/producer.py

5.7. Consultas analíticas
python src/queries_analytics.py

5.8. Ejecutar experimento de ML
python src/ml_experiment.py

## 6.Posibles extensiones

- Sustituir el productor simulado por un broker de mensajes real como Kafka, RabbitMQ o Azure Event Hubs.
-Exponer una API REST (por ejemplo con FastAPI) para consultar:
-El último estado de un vehículo (desde Mongo).
-Métricas agregadas (desde DuckDB).

Elaborado por :

Paola Fernanda Lopez Recalde
Ing. de sistemas Esp. Ciencia de datos  y analitica
Tarjeta profesional 52255-305430



