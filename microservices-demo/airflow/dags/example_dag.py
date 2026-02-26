from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    "owner": "airflow",
    "start_date": datetime(2023,1,1),
}

with DAG("example", default_args=default_args, schedule_interval="@daily") as dag:
    BashOperator(task_id="echo",
                 bash_command="echo 'Airflow running'")