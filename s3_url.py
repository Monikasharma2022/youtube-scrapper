import boto3
from my_cred import aws_access_key_id, aws_secret_access_key
from logger import App_Logger

class s3:
    def __init__(self):
        self.logger = App_Logger()
        self.file_object = open("Scrapper_logs/s3_logs", 'a+')

    def upload_s3(self, file):
        try:
            self.logger.log(self.file_object, "enter inside upload_s3 method")
            s3 = boto3.resource(
                service_name='s3',
                region_name='us-east-1',
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key)

            self.logger.log(self.file_object, "resource created successfully for s3_bucket")

            s3.Bucket('monikaawsbucket1').upload_file(Filename=file, Key=file)

            self.logger.log(self.file_object, "uploaded to s3_bucket")

            s3_client = boto3.client('s3',
                                     aws_access_key_id=aws_access_key_id,
                                     aws_secret_access_key=aws_secret_access_key)
            s3_link = s3_client.generate_presigned_url('get_object', Params={'Bucket': 'monikaawsbucket1',
                                                                             'Key': file},
                                                       ExpiresIn=600)

            return s3_link

        except Exception as e:
            self.logger.log(self.file_object, "error in upload_s3: %s" %e)

