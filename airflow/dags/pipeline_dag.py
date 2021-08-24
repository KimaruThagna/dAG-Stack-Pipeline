from datetime import timedelta
import os
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator

from airflow.utils.dates import days_ago

DBT_DIR = os.environ.get("DBT_PROFILES_DIR")

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": days_ago(1),
    "email": ["thagana44@gmail.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
    "catchup": False,
}


with DAG(
    "dAG Stack Pipeline",
    default_args=default_args,
    schedule_interval=timedelta(days=1),
) as dag:
    
    dbt_packages = BashOperator(
        task_id="dbt_packages", bash_command=f"cd {DBT_DIR} && dbt deps"
    )
    dbt_seed = BashOperator(
        task_id="dbt_seed",
        bash_command=f"cd {DBT_DIR} && dbt seed --profiles-dir {DBT_DIR} --project-dir {DBT_DIR}",
    )
    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=f"cd {DBT_DIR} && dbt test --profiles-dir {DBT_DIR} --project-dir {DBT_DIR}",
    )
    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=f"cd {DBT_DIR} && dbt run --profiles-dir {DBT_DIR} --project-dir {DBT_DIR}",
    )
    dbt_cleanup = BashOperator(
        task_id="dbt_cleanup",
        bash_command=f"cd {DBT_DIR} && dbt clean --profiles-dir {DBT_DIR} --project-dir {DBT_DIR}",
    )

   

    dbt_packages >> dbt_seed >> dbt_test >> dbt_run >> dbt_cleanup 
