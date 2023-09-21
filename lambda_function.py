import pymysql
import csv
import os
import boto3
import tempfile
import zipfile
import datetime
import base64

 
# RDS database settings
db_host = os.environ['DB_HOST']
db_user = os.environ['DB_USER']
db_name = os.environ['DB_NAME']
db_password = os.environ['DB_PASSWORD']

# S3 bucket settings
s3_bucket = os.environ['S3_BUCKET']
# Use a timestamp in the S3 object key
timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
s3_key = f'backup_{timestamp}.zip'

def lambda_handler(event, context):
    try:
        # Connect to the RDS database
        conn = pymysql.connect(host=db_host, user=db_user, password=db_password, db=db_name)
        
        # Create a cursor
        cursor = conn.cursor()
        
        # Execute SQL queries to fetch data from tables
        table_queries = {
            'employee': 'SELECT * FROM employee',
            'training': 'SELECT * FROM training',
            'training_attendee': 'SELECT * FROM training_attendee',
            'course': 'SELECT * FROM course'
        }
        
        # Create a temporary directory to store CSV files
        temp_dir = tempfile.mkdtemp()
        
        # Fetch and write data to CSV files
        for table_name, query in table_queries.items():
            cursor.execute(query)
            result = cursor.fetchall()
            
            # Create a CSV file for each table
            csv_filename = os.path.join(temp_dir, f'{table_name}.csv')
            with open(csv_filename, 'w', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerows(result)
        
        # Create a zip file containing all CSV files
        zip_filename = os.path.join(temp_dir, 'data.zip')
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for table_name in table_queries.keys():
                csv_filename = os.path.join(temp_dir, f'{table_name}.csv')
                zipf.write(csv_filename, f'{table_name}.csv')
        
        # Upload the zip file to the S3 bucket
        s3_client = boto3.client('s3')
        s3_client.upload_file(zip_filename, s3_bucket, s3_key)
        
        return f"CSV data zipped and uploaded to S3 bucket '{s3_bucket}' as '{s3_key}'"
        
    except Exception as e:
        return f"Error: {str(e)}"
