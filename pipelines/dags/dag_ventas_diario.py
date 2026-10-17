"""DAG de Airflow: pipeline diario de ventas de RetailMax.

Orden:  extraer -> validar calidad (quality gate) -> transformar -> entrenar -> publicar
Si la validacion falla, Airflow detiene el DAG: nada de lo que sigue se ejecuta
y produccion conserva la ultima version buena del modelo.
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator


def alertar_fallo(context):
    """Notifica al ingeniero de datos responsable y al data owner (Slack/correo)."""
    tarea = context["task_instance"].task_id
    print(f"ALERTA: fallo la tarea {tarea}. Pipeline detenido; lote en cuarentena.")


def validar_calidad(**_):
    """Quality gate: corre las pruebas de datos; si fallan, la tarea falla."""
    import subprocess 
    subprocess.run(
        ["pytest", "tests/test_data_quality.py", "-q"], check=True
    )


argumentos = {
    "owner": "equipo-datos",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "on_failure_callback": alertar_fallo,
}

with DAG(
    dag_id="ventas_diario",
    description="Extrae, valida, transforma y entrena el modelo de ventas",
    start_date=datetime(2026, 11, 1),
    schedule="0 2 * * *",  # todos los dias a las 2:00 am
    catchup=False,
    default_args=argumentos,
    tags=["retailmax", "ventas"],
) as dag:
    extraer = BashOperator(
        task_id="extraer_ventas",
        bash_command="python -m scripts.create_snapshot data/ventas.db",
    )
    validar = PythonOperator(task_id="validar_calidad", python_callable=validar_calidad)
    entrenar = BashOperator(
        task_id="transformar_y_entrenar",
        bash_command="APP_ENV={{ var.value.app_env }} python -m src.train_ventas",
    )
    publicar = BashOperator(
        task_id="publicar_resultados",
        bash_command="dvc add data/aggregated_sales.csv && dvc push",
    )

    extraer >> validar >> entrenar >> publicar