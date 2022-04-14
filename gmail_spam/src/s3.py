import boto3
import argparse
import os
import sys
from dotenv import load_dotenv

load_dotenv()

BUCKET_NAME = os.getenv("BUCKET")

class S3Client:
    """
    Simple wrapper around aws api to read/write to s3 bucket for this project
    """

    def __init__(self):
        self.s3_resource = boto3.resource("s3")
        self.bucket = None

    def get_bucket(self):
        if not self.bucket:
            self.bucket = self.s3_resource.Bucket(BUCKET_NAME)

        return self.bucket

    def list_obj(self):
        for obj in self.bucket.objects.all():
            print(obj.key)

    def put(self, key, file, filetype):
        """
        Parameters
        ----
        filetype : {'obj', 'path'}
            Whether the `file` passed is a path to a file, or a file object (binary) itself.
            Usually, 'obj' is used with tempfile.
        key : str
            Key of the bucket object (like path in s3 - relative to the project bucket)
        file : { bytes, str }
            If `filetype` is obj then this must be bytes-like obj of a file

        Returns
        -------
        True 
            If success.
        
        Raises
        ------
        Exception: 
            from AWS if error

            
        """
        if filetype not in ['obj', 'path']:
            ValueError("filetype must be one of: 'obj', 'path'")
        if filetype=='obj':
            self.bucket.upload_fileobj(Key=key, Fileobj=file)
        else : 
            self.bucket.upload_file(Key=key, Filename=file)
        # wait until the just placed object exists
        object = self.s3_resource.Object(BUCKET_NAME,key)
        try : 
            object.wait_until_exists()
            print(f"{key} exists!")
            return True
        except Exception as e :
            print(e)
        


def main():
    # parser = argparse.ArgumentParser()
    # parser.add_argument("--create", action="store_true")
    # parser.add_argument("--drop", action="store_true")
    # parser.add_argument("--status", action="store_true")
    # args = parser.parse_args()
    # print("args")
    # print(args)

    client = S3Client()
    client.get_bucket()
    print(client.list_obj())
    # if len(sys.argv) != 2: # we want 2 args (the 2nd is the flag)
    #     print('Flags must be exactly ONE OF : --create, --drop, --status')

    # elif args.create and args.drop:
    #     print('both')
    # elif args.create:
    #     dybamo_table = client.create_ddb_table()
    #     print("Table status:", dybamo_table.table_status)
    # elif args.drop:
    #     client.drop_ddb_table()
    #     print("Table status: dropped" )
    # elif args.status:
    #     status = client.check_table_status()
    #     print(status)


if __name__ == "__main__":
    main()
