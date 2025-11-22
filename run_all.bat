@echo off
REM ======================================================
REM  Script: run_all.bat
REM  Objetivo: ejecutar toda la prueba de extremo a extremo
REM ======================================================

echo.
echo ==========================================
echo 1) Activando entorno virtual (.venv)
echo ==========================================
call ".venv\Scripts\activate"

if errorlevel 1 (
    echo [ERROR] No se pudo activar el entorno virtual.
    echo Asegurate de que existe la carpeta .venv en esta ruta.
    pause
    exit /b 1
)

echo.
echo ==========================================
echo 2) Probando conexion a MongoDB (test_mongo.py)
echo ==========================================
python src\test_mongo.py
if errorlevel 1 (
    echo [ERROR] Fallo la prueba de MongoDB.
    pause
    exit /b 1
)

echo.
echo ==========================================
echo 3) Probando DuckDB (test_duckdb.py)
echo ==========================================
python src\test_duckdb.py
if errorlevel 1 (
    echo [ERROR] Fallo la prueba de DuckDB.
    pause
    exit /b 1
)

echo.
echo ==========================================
echo 4) Ejecutando pipeline (producer.py)
echo    - Lee Parquet
echo    - Envía eventos a MongoDB y DuckDB
echo ==========================================
python src\producer.py
if errorlevel 1 (
    echo [ERROR] Fallo la ejecucion de producer.py
    pause
    exit /b 1
)

echo.
echo ==========================================
echo 5) Ejecutando consultas analiticas (queries_analytics.py)
echo ==========================================
python src\queries_analytics.py
if errorlevel 1 (
    echo [ERROR] Fallo la ejecucion de queries_analytics.py
    pause
    exit /b 1
)

echo.
echo ==========================================
echo 6) Ejecutando experimento de ML (ml_experiment.py)
echo    - Entrena Random Forest
echo    - Muestra metricas y ejemplos de prediccion
echo ==========================================
python src\ml_experiment.py
if errorlevel 1 (
    echo [ERROR] Fallo la ejecucion de ml_experiment.py
    pause
    exit /b 1
)

echo.
echo ==========================================
echo  ¡Ejecucion completa!
echo  - Conexiones OK
echo  - Pipeline ejecutado
echo  - Consultas analiticas mostradas
echo  - Experimento de ML ejecutado
echo ==========================================
echo.

pause
