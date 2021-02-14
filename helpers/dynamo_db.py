import os

from datetime import datetime
from decimal import Decimal

import boto3


class DynamoClient:

    # Keep clients in class fields allow us to reuse client during hot lambda executions
    client = None

    def __init__(self, is_local):
        if not self.client:
            if is_local:
                self.client = boto3.resource('dynamodb', endpoint_url="http://localhost:8000", region_name='localhost')
            else:
                self.client = boto3.resource('dynamodb')

        self.table = self.client.Table(os.getenv('ANNOUNCEMENTS_TABLE', 'Announcements'))

    def save_announcement(self, title, description):
        """Create new annoucement"""

        utcnow = datetime.utcnow()

        response = self.table.put_item(
            Item={
                'timestamp': Decimal(utcnow.timestamp()),
                'title': title,
                'description': description,
                'date': utcnow.isoformat(),
            }
        )
        return response

    def get_all_announcements(self):
        """Return list of all announcements"""

        return self.table.scan()
