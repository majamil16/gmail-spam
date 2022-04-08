
import boto3
import argparse
import os
import sys
from dotenv import load_dotenv
load_dotenv()

class Dynamo():
    """
    Simple class to handle creating / dropping dynamodb table as needed
    (for easy dropping data after testing, etc)
    """
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')

    def drop_ddb_table(self):
        # if not dynamodb:
        #     dynamodb = boto3.resource('dynamodb')
        table = self.dynamodb.Table(os.getenv('TABLE'))
        table.delete()

    def check_table_status(self):
        # if not dynamodb:
        #     dynamodb = boto3.resource('dynamodb')
        table = self.dynamodb.Table(os.getenv('TABLE'))
        status = table.table_status
        return status

    def create_ddb_table(self):
        # if not dynamodb:
        #     dynamodb = boto3.resource('dynamodb')
        schema = {
                "AttributeDefinitions": [
                    {"AttributeName": "id", "AttributeType": "S"},
                    {"AttributeName": "sender", "AttributeType": "S"},
                ],
                "KeySchema": [
                    {"AttributeName": "id", "KeyType": "HASH"},
                    {"AttributeName": "sender", "KeyType": "RANGE"},
                ],
                "ProvisionedThroughput": {"ReadCapacityUnits": 1, "WriteCapacityUnits": 1},
            }
        table = self.dynamodb.create_table(
            TableName=os.getenv('TABLE'),
            KeySchema=schema["KeySchema"],
            AttributeDefinitions=schema["AttributeDefinitions"],
            ProvisionedThroughput=schema["ProvisionedThroughput"],
        )
        return table


    


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--create', action='store_true')
    parser.add_argument('--drop', action='store_true')
    parser.add_argument('--status', action='store_true')
    args = parser.parse_args()

    client = Dynamo()
    if len(sys.argv) != 2: # we want 2 args (the 2nd is the flag)
        print('Flags must be exactly ONE OF : --create, --drop, --status')
        
    elif args.create and args.drop:
        print('both')
    elif args.create:
        dybamo_table = client.create_ddb_table()
        print("Table status:", dybamo_table.table_status)
    elif args.drop:
        client.drop_ddb_table()
        print("Table status: dropped" )
    elif args.status:
        status = client.check_table_status()
        print(status)

    
