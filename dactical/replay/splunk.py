from .base import Replay
import os
from splunklib import client

class SplunkReplay(Replay):
    """Replay data into Splunk."""
    
    def __init__(self, hostname: str, username: str, password: str):
        """
        Initialize SplunkReplay.
        
        Args:
            hostname: Splunk server hostname
            username: Splunk username
            password: Splunk password
        """
        super(SplunkReplay, self).__init__()
        self.hostname = hostname
        self.username = username
        self.password = password

    def replay_data(self, data: str, source: str) -> bool:
        """
        Replay data into Splunk.
        
        Args:
            data: The data to replay.
            
        Returns:
            The result of replaying the data.
        """
        try:
            service = client.connect(host=self.hostname, port=8089, username=self.username, password=self.password)
        except ConnectionRefusedError as e:
            raise Exception(f"Could not connect to the splunk server {self.hostname}:8089")
        
        try:
            service.indexes.create('staging_data')
        except Exception as e:
            pass
        
        index = service.indexes['staging_data']
        
        if not os.path.exists('./import'):
            os.mkdir('./import')

        try:
            with open('./import/data.raw', 'w') as f:
                f.write(data)
        except Exception as e:
            raise Exception(f"Could not write data to file: {str(e)}")
        
        index.upload("./import/data.raw", sourcetype=source)








