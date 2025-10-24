@echo off
setlocal EnableDelayedExpansion
chcp 65001 >NUL

REM ================================================================
REM SCRIPT DE EXPORTACIÓN DE LOTES A GEOPACKAGE (Windows)
REM ================================================================
REM Descripción: Exporta lotes de Alvarado, Piedras e Ibagué a GPKG
REM Fecha: 2025-10-22
REM Uso: exportar_lotes_mesetas.bat
REM ================================================================

for /f "delims=" %%E in ('echo prompt $E ^| cmd') do set "ESC=%%E"
set "RED=%ESC%[31m"
set "GREEN=%ESC%[32m"
set "YELLOW=%ESC%[33;1m"
set "NC=%ESC%[0m"

set "DB_HOST=192.168.54.18"
set "DB_NAME=sig_fedearroz_fna"
set "DB_USER=%PGUSER%"
if "%DB_USER%"=="" set "DB_USER=sig_editor_a"
set "DB_PORT=%PGPORT%"
if "%DB_PORT%"=="" set "DB_PORT=5432"

if "%PGPASSWORD%"=="" (
    echo %YELLOW%Ingresa la contraseña para el usuario %DB_USER%:%NC%
    set /p "PGPASSWORD=>"
)

set "OUTPUT_DIR=%USERPROFILE%\Documents\SQL_marco_geografico"
set "OUTPUT_FILE=lotes_alvarado_piedras_ibague.gpkg"
if not exist "%OUTPUT_DIR%" mkdir "%OUTPUT_DIR%"

echo %GREEN%================================================================%NC%
echo %GREEN%EXPORTACIÓN DE LOTES - ALVARADO, PIEDRAS E IBAGUE%NC%
echo %GREEN%================================================================%NC%
echo.

where ogr2ogr >NUL 2>&1
if errorlevel 1 (
    echo %RED%Error: ogr2ogr no está instalado o no está en PATH.%NC%
    pause
    exit /b 1
)

where psql >NUL 2>&1
if errorlevel 1 (
    echo %RED%Error: psql no está instalado o no está en PATH.%NC%
    pause
    exit /b 1
)

echo %YELLOW%Probando conexión a la base de datos...%NC%
psql -h "%DB_HOST%" -p "%DB_PORT%" -U "%DB_USER%" -d "%DB_NAME%" -c "SELECT 1;" >NUL 2>&1
if errorlevel 1 (
    echo %RED%Error: No se pudo conectar a la base de datos.%NC%
    echo Verifica host, puerto, usuario y contraseña.
    pause
    exit /b 1
)
echo %GREEN%✓ Conexión exitosa.%NC%
echo.

echo %YELLOW%Consultando estadísticas de los lotes...%NC%
psql -h "%DB_HOST%" -p "%DB_PORT%" -U "%DB_USER%" -d "%DB_NAME%" -c ^
"SELECT
    m.mpio_cnmbr AS municipio,
    m.mpio_cdpmp AS codigo_municipio,
    COUNT(l.lote_id) AS total_lotes,
    ROUND(SUM(l.area_ha)::numeric, 2) AS area_total_ha
 FROM gis.lotes l
 JOIN gis.municipios m ON l.municipio_principal = m.mpio_cdpmp
 WHERE m.mpio_cnmbr IN ('ALVARADO','PIEDRAS','IBAGUE')
   AND m.dpto_cnmbr = 'TOLIMA'
 GROUP BY m.mpio_cnmbr, m.mpio_cdpmp
 ORDER BY total_lotes DESC;"

echo.
echo %YELLOW%Exportando a GeoPackage...%NC%
echo Archivo de salida: %OUTPUT_DIR%\%OUTPUT_FILE%
echo.

ogr2ogr -f GPKG ^
  "%OUTPUT_DIR%\%OUTPUT_FILE%" ^
  "PG:host=%DB_HOST% port=%DB_PORT% dbname=%DB_NAME% user=%DB_USER% password=%PGPASSWORD%" ^
  -sql "SELECT l.lote_id, l.cofinca, l.secuencia_lote, l.lote_codigo, l.area_m2, l.area_ha, l.municipio_principal, m.mpio_cnmbr AS municipio_nombre, m.dpto_cnmbr AS departamento_nombre, l.porcentaje_municipio_principal, l.zona_codigo, l.created_at, l.updated_at, l.updated_by, l.geom FROM gis.lotes l JOIN gis.municipios m ON l.municipio_principal = m.mpio_cdpmp WHERE m.mpio_cnmbr IN ('ALVARADO','PIEDRAS','IBAGUE') AND m.dpto_cnmbr = 'TOLIMA'" ^
  -nln lotes_meseta ^
  -overwrite ^
  -progress

if errorlevel 1 (
    echo %RED%✗ Error durante la exportación.%NC%
    pause
    exit /b 1
)

echo.
echo %GREEN%================================================================%NC%
echo %GREEN%✓ Exportación completada exitosamente%NC%
echo %GREEN%================================================================%NC%
echo Archivo creado: %OUTPUT_DIR%\%OUTPUT_FILE%
echo.
ogrinfo -so "%OUTPUT_DIR%\%OUTPUT_FILE%" lotes_meseta

set "PGPASSWORD="
echo.
echo %GREEN%Proceso finalizado.%NC%
pause
exit /b 0