from datetime import timedelta
import os
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from great_expectations_provider.operators.great_expectations import GreatExpectationsOperator
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
ROOT = os.getcwd()
DATA_DIR = os.environ.get('DATA_DIR')
DBT_DIR = os.environ.get('DBT_PROFILES_DIR')
DBT_DOCS_DIR = os.environ.get('DBT_DOCS')
GE_ROOT_DIR = os.environ.get('GE_DIR')
GE_DOCS_DIR = os.environ.get('GE_DOCS')


with DAG(
    "dAG_Stack_Pipeline",
    default_args=default_args,
    schedule_interval=timedelta(days=1),
) as dag:
    
# This first step validates the source data files and only proceeds with loading
# if they pass validation with Great Expectations
    validate_source_data = GreatExpectationsOperator( # can have more than one expectation suite
    task_id='validate_source_data',
    assets_to_validate = [
        {
            'batch_kwargs': {
                'path': f'{DATA_DIR}/Transactions.csv',
                'datasource': 'data_dir'
            },
            'expectation_suite_name': 'bank_transactions.source'
        },
       
    ],
    data_context_root_dir=GE_ROOT_DIR
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
#     validate_dbt_data = GreatExpectationsOperator( # sample showing dealing with single suite
#     task_id='validate_transform',
#     expectation_suite_name='bank_transactions.analysis',
#     batch_kwargs={
#         'datasource': 'postgres_docker',
#         'table': 'suspectTransactions',
#         'data_asset_name': 'suspectTransactions'
#     },
#     data_context_root_dir=GE_ROOT_DIR
# )
    
#     dbt_docs_generate = BashOperator(
#     task_id='dbt_docs_generate',
#     bash_command=f'cd {DBT_DIR} && dbt docs generate \
#     --profiles-dir {DBT_DIR} \
#     --target {DBT_DOCS_DIR} \
#     --project-dir {DBT_DIR}',
# )
#     # This task re-builds the Great Expectations docs
#     ge_docs_generate = BashOperator(
#     task_id='ge_docs_generate',
#     bash_command=f'great_expectations --v3-api docs build  --directory {GE_ROOT_DIR} --assume-yes'
# )
    
    dbt_cleanup = BashOperator(
        task_id="dbt_cleanup",
        bash_command=f"cd {DBT_DIR} && dbt clean --profiles-dir {DBT_DIR} --project-dir {DBT_DIR}",
    )

   

validate_source_data >> dbt_seed >> dbt_test >> dbt_run >> dbt_cleanup 
    #validate_dbt_data >> [ge_docs_generate >> dbt_docs_generate] >> dbt_cleanup 
