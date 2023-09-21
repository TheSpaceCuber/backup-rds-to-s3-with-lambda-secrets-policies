import csv
import boto3
import logging

def lambda_handler(event, context):
    header = ['Name', 'Age', 'Profession']
    data = [('John', '25', 'Engineer'),
            ('Anna', '28', 'Doctor'),
            ('Peter', '30', 'Artist')]

    filename = 'people.csv'

    with open('/tmp/' + filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)
    
    print("CSV CREATED")
    # Upload the file
    s3_client = boto3.client('s3')
    try:
        s3_bucket = "rds-backup-1-test"
        response = s3_client.upload_file('/tmp/' + filename, s3_bucket, filename)
    except Exception as e:
        logging.error(e)
        return False

    print("COMPLETE")
