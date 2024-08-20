from airflow                         import DAG
from datetime                        import timedelta
from airflow.operators.utils.dates   import days_ago
from airflow.operators.bash_operator import BashOperator

# Define DAG argumen

default_args = {
    'owner'            : 'roniantoniuss',
    'start_date'       : days_ago(0),
    'email'            : ['antoniusronz89@gmail.com'],
    'email_on_failure' : False,
    'email_on_retry'   : False,
    'retries'          : 1,
    'retry_delay'      : timedelta(minutes=5)
}

# Define DAG untuk ETL Pipeline for several task

dag = DAG(
    'process_web_log',
    default_args      = default_args,
    description       = 'my-process-web-log',
    schedule_interval = timedelta(days=1)
)


# TASK


# Extract: Ekstrak data

extract = BashOperator(
    task_id      = 'extract_data',
    bash_command = 'cut -d" " -f1 /home/project/airflow/dags/capstone/accesslog.txt \
        > /home/project/airflow/dags/capstone/extracted_data.txt',
    dag          = dag
)

# Transform: Transformasi data in the txt file before
transform_data = BashOperator(
    task_id      = 'transform_data',

    # we will delete some specified ip like 198.46.149.143
    bash_command = 'sed "/198.46.149.143/d" /home/project/airflow/dags/capstone/extracted_data.txt \
        > /home/project/airflow/dags/capstone/transformed_data.txt',
    dag          = dag
)

# Load: Load data to the database or to tar format ok
load_data = BashOperator(
    task_id      = 'load_data',
    bash_command = 'tar cvf weblog.tr /home/project/airflow/dags/capstone/transformed_data.txt',
    dag          = dag
)


# DAG Task Dependencies or task pipeline
extract >> transform_data >> load_data