import logging
import boto3
from botocore.exceptions import ClientError
import os

sso_region = os.getenv('SSO_REGION')
queue_url = os.getenv('SQS_QUEUE_URL')


def create_bucket(bucket_name, region):
    """Create an S3 bucket in a specified region

    If a region is not specified, the bucket is created in the S3 default
    region (us-east-1).

    :param bucket_name: Bucket to create
    :param region: String region to create bucket in, e.g., 'us-west-2'
    :return: True if bucket created, else False
    """

    # Create bucket
    try:
        if region is None:
            s3_client = boto3.client('s3',
                                     aws_access_key_id='AKIAVI7PUQMWA7CHFW7Q',
                                     aws_secret_access_key='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')
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3',
                                     region_name=region,
                                     aws_access_key_id='AKIAVI7PUQMWA7CHFW7Q',
                                     aws_secret_access_key='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')
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def list_buckets():
    # Retrieve the list of existing buckets
    s3 = boto3.client('s3')
    response = s3.list_buckets()

    # Output the bucket names
    print('Existing buckets:')
    for bucket in response['Buckets']:
        print(f'  {bucket["Name"]}')


def upload_file(file_name, bucket, object_name, region):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # Upload the file
    s3_client = boto3.client('s3',
                             region_name=region,
                             aws_access_key_id='AKIAVI7PUQMWA7CHFW7Q',
                             aws_secret_access_key='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')
    try:
        s3_client.upload_file(file_name, bucket, object_name)
        print('upload_file is good')
    except ClientError as e:
        logging.error(e)
        return False
    return True


def downloading_files(file_name, bucket, object_name, region):
    s3 = boto3.client('s3',
                      region_name=region,
                      aws_access_key_id='AKIAVI7PUQMWA7CHFW7Q',
                      aws_secret_access_key='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')
    try:
        s3.download_file(bucket, object_name, file_name)
        print('downloading_files is good')
    except ClientError as e:
        logging.error(e)
        return False
    return True


def get_object_name(file_name):
    return os.path.basename(file_name)


def remove_file(file_name):
    if os.path.exists(file_name):
        os.remove(file_name)
        print('Archivo removido con exito ', file_name)
    else:
        print('No se pudo remover el archivo')
        return 'No se pudo remover el archivo', 500


def find_object(bucket, region, object_name):
    s3 = boto3.resource('s3',
                        region_name=region,
                        aws_access_key_id='AKIAVI7PUQMWA7CHFW7Q',
                        aws_secret_access_key='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')
    bucket = s3.Bucket(bucket)
    print("in find_object i need to find......... ", object_name)
    a = [x for x in bucket.objects.all() if x.key == object_name]
    if len(a) > 0:
        print("in find_object..... True")
        return True
    else:
        print("in find_object..... False")
        return False


def delete_object(bucket, region, object_name):
    s3 = boto3.resource('s3',
                        region_name=region,
                        aws_access_key_id='AKIAVI7PUQMWA7CHFW7Q',
                        aws_secret_access_key='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')
    try:
        s3.Object(bucket, object_name).delete()
    except Exception as e:
        logging.error(e)
        return False
    return True


def receive_and_delete_messages_queue():
    # Create SQS client
    sqs = boto3.client('sqs', region_name=sso_region)

    # Receive message from SQS queue
    response = sqs.receive_message(
        QueueUrl=queue_url,
        AttributeNames=[
            'SentTimestamp'
        ],
        MaxNumberOfMessages=1,
        MessageAttributeNames=[
            'All'
        ],
        VisibilityTimeout=0,
        WaitTimeSeconds=0
    )

    print("Response...... ", response)

    if hasattr(response, 'Messages'):
        message = response['Messages'][0]
        receipt_handle = message['ReceiptHandle']

        # Delete received message from queue
        sqs.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=receipt_handle
        )
        print('Received and deleted message: %s' % message)
    else:
        print("Don't have messages")
