from __future__ import annotations

import io
import boto3
import zlib

import torch

from hashlib import sha3_256

from boto3.dynamodb.conditions import Key
from boto3.dynamodb.types import Binary
from torch import tensor
from torch.functional import Tensor

from .mem_cache import CacheBase
from typing import Generic, TypeVar

T = TypeVar("T")


class DynamoDBCache(CacheBase, Generic[T]):

    def __init__(self, table_name, url='http://localhost:8085', 
                                            region='poa-rs-br-al') -> None:
        super().__init__()
        self.hash_dict = {}
        self.table_name = table_name
        self.url = url
        self.region = region
        self.table = self.connect()

    def connect(self):
        dynamodb = boto3.resource('dynamodb', endpoint_url=self.url, 
                                                    region_name=self.region)
        try:
            table = dynamodb.create_table(
                TableName=self.table_name,
                KeySchema=[
                    {
                        'AttributeName': 'key',
                        'KeyType': 'HASH'
                    }                        
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'key',
                        'AttributeType': 'S'
                    }
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 10,
                    'WriteCapacityUnits': 10
                }
            )
        except:
            print(f'Table {self.table_name} already exist!')

        return dynamodb.Table(self.table_name)

    def get(self, key: str) -> T | None:        
        query_resp = self.table.query(
            KeyConditionExpression=Key('key').eq(key)
        )
        
        if len(query_resp['Items']) > 0:
            read_buffer = io.BytesIO(zlib.decompress(bytes(query_resp['Items'][0]['data'])))
            return torch.load(read_buffer)
        else:
            return None
        

    def multi_get(self, *keys: str) -> list[T | None]:        
        return [self.get(k) for k in keys]

    def set(self, key: str, value: Tensor):
        item_buffer = io.BytesIO()
        torch.save(value, item_buffer)    
        item_buffer.seek(0)    
        item_buffer = item_buffer.read()
        item_buffer = zlib.compress(item_buffer)
        self.table.put_item(Item={'key':key,'data':Binary(item_buffer)})

    def __str__(self):
        return str(self.table)

if __name__ == '__main__':
    db = DynamoDBCache('table_tmp')
    print(db)