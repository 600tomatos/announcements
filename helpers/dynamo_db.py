import os

from datetime import datetime
from decimal import Decimal

import boto3


class DynamoClient:
    client = None

    def __init__(self):
        if not self.client:
            self.client = boto3.resource('dynamodb', endpoint_url="http://localhost:8000", region_name='localhost')

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
