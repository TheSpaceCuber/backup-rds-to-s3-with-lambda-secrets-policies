import pymysql
import csv
import os
import boto3
import tempfile
 
# RDS database settings
db_host = os.environ['DB_HOST']
db_user = os.environ['DB_USER']
db_password = os.environ['DB_PASSWORD']
db_name = os.environ['DB_NAME']

# S3 bucket settings
s3_bucket = os.environ['S3_BUCKET']
s3_key = 'employee_data.csv'  # The desired CSV file name in the S3 bucket

def lambda_handler(event, context):
    try:
        # Connect to the RDS database
        conn = pymysql.connect(host=db_host, user=db_user, password=db_password, db=db_name)
        
        # Create a cursor
        cursor = conn.cursor()
        
        # Execute a SQL query to fetch data from the 'employee' table
        cursor.execute("SELECT * FROM employee")
        result = cursor.fetchall()

        # Create a CSV file as a string
        csv_data = "\n".join([",".join(map(str, row)) for row in result])
        
        # Upload the CSV data to the S3 bucket
        s3_client = boto3.client('s3')
        s3_client.put_object(Bucket=s3_bucket, Key=s3_key, Body=csv_data)
        
        return f"CSV data uploaded to S3 bucket '{s3_bucket}' as '{s3_key}'"
        
    except Exception as e:
        return f"Error: {str(e)}"