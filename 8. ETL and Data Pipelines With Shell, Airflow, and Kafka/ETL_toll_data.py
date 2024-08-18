# library
import csv
import os
import tarfile
import pandas as pd
from airflow import DAG
from datetime import timedelta
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator

# Task 1.1 - Define DAG arguments
default_args = {
    'owner': 'airflow',
    'start_date': days_ago(0),
    'email': ['airflow@example.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def unzip_tolldata(source, destination):
    try:
        with tarfile.open(source, "r:gz") as tgz:
            tgz.extractall(destination)
    except Exception as e:
        print(f"Error extracting {source}: {e}")


def extract_csv_data(infile, outfile):
    try:
        with open(infile, "r") as readfile, open(outfile, "w") as writefile:
            for line in readfile:
                # Split the line by comma and select columns 1 to 4 (0-based index)
                selected_columns = ",".join(line.strip().split(",")[:4])
                writefile.write(selected_columns + "\n")
    except Exception as e:
        print(f"Error processing {infile}: {e}")


def extract_tsv_data(infile, outfile):
    try:
        with open(infile, "r") as readfile, open(outfile, "w") as writefile:
            for line in readfile:
                # hampir sama kayak tadi
                selected_columns = ",".join(line.strip().split("\t")[4:7])
                writefile.write(selected_columns + "\n")
    except Exception as e:
        print(f"Error processing {infile}: {e}")


def extract_fixed_width_data(infile, outfile):
    try:
        with open(infile, "r") as readfile, open(outfile, "w") as writefile:
            for line in readfile:
                cleaned_line = " ".join(line.split())

                selected_columns = cleaned_line.split(" ")[9:11]
                writefile.write(",".join(selected_columns) + "\n")
    except Exception as e:
        print(f"Error processing {infile}: {e}")


def consolidate_data_extracted(infile, outfile):

    try:
        combined_csv = pd.concat([pd.read_csv(f) for f in infile], axis=1)
        combined_csv.to_csv(outfile, index=False)
    except Exception as e:
        print(f"Error processing {infile}: {e}")


def transform_load_data(infile, outfile):

    try:
        with open(infile, "r") as readfile, open(outfile, "w") as writefile:
            reader = csv.reader(readfile)
            writer = csv.writer(writefile)

            for row in reader:
                row[3] = row[3].upper()
                writer.writerow(row)
    except Exception as e:
        print(f"Error processing {infile}: {e}")




# Task 1.2 - Define the DAG
dag = DAG(
    dag_id='ETL_toll_data',
    schedule_interval=timedelta(days=1),
    default_args=default_args,
    description='Apache Airflow Final Assignment',
)

DESTINATION = "/home/project/airflow/dags"
source = os.path.join(DESTINATION, "tolldata.tgz")
vehicle_data = os.path.join(DESTINATION, "vehicle-data.csv")
tollplaza_data = os.path.join(DESTINATION, "tollplaza-data.tsv")
payment_data = os.path.join(DESTINATION, "payment-data.txt")
csv_data = os.path.join(DESTINATION, "csv_data.csv")
tsv_data = os.path.join(DESTINATION, "tsv_data.csv")
fixed_width_data = os.path.join(DESTINATION, "fixed_width_data.csv")
extracted_data = os.path.join(DESTINATION, "extracted_data.csv")
transformed_data = os.path.join(DESTINATION, "staging/transformed_data.csv")

# Task 2.1 - Create a task to unzip data
unzip_data = PythonOperator(
    task_id='unzip_data',
    python_callable=unzip_tolldata,
    op_args=[source, DESTINATION],
    dag=dag
)

# Task 2.2 - Create a task to extract data from csv file
extract_data_from_csv = PythonOperator(
    task_id='extract_data_from_csv',
    python_callable=extract_csv_data,
    op_args=[vehicle_data, csv_data],
    dag=dag
)

# Task 2.3 - Create a task to extract data from tsv file
extract_data_from_tsv = PythonOperator(
    task_id='extract_data_from_tsv',
    python_callable=extract_tsv_data,
    op_args=[tollplaza_data, tsv_data],
    dag=dag
)

# Task 2.4 - Create a task to extract data from fixed width file
extract_data_from_fixed_width = PythonOperator(
    task_id='extract_data_from_fixed_width',
    python_callable=extract_fixed_width_data,
    op_args=[payment_data, fixed_width_data],
    dag=dag
)

# Task 2.5 - Create a task to consolidate data extracted from previous tasks
consolidate_data = PythonOperator(
    task_id='consolidate_data',
    python_callable=consolidate_data_extracted,
    op_args=[[csv_data, tsv_data, fixed_width_data], extracted_data],
    dag=dag
)

# Task 2.6 - Transform and load the data
transform_data = PythonOperator(
    task_id="transform_data",
    python_callable=transform_load_data,
    op_args=[extracted_data, transformed_data],
    dag=dag
)

# Task 2.7 - Define the task pipeline
unzip_data >> [extract_data_from_csv, extract_data_from_tsv, extract_data_from_fixed_width] >> consolidate_data >> transform_data