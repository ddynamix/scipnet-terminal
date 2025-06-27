import requests
import json

BASE_URL = "https://raw.githubusercontent.com/scp-data/scp-api/main/docs/data/scp/"
BASE_PATH = "/Users/tylersteptoe/Documents/Projects/scp_data_jun2025/scp-api/docs/data/scp"


class DBConnector:
    def __init__(self, using_local_db: bool):
        self.using_local_db = using_local_db
    
    
    def get_content_series(self, series_num: str) -> dict:
        """
        Get the dictionary of content series.
        
        :param series_num: must be of format "x" or "x.5"
        :return: a dictionary of scp content with scp nums as keys
        """
        content_series = {}
        
        if self.using_local_db:
            try:
                with open(BASE_PATH + f"/items/content_series-{series_num}.json", "r") as f:
                    content_series = json.load(f)
            except:
                raise FileNotFoundError("Content series file not found")
    
        else:
            content_series = requests.get(BASE_URL + f"items/content_series-{series_num}.json").json()
            if content_series.status_code != 200:
                raise Exception("Content series request failed")
        
        return content_series
    
    
    def get_metadata(self) -> dict:
        """
        Get the metadata for all scps.
        
        :return: A dictionary of scp metadata
        """
        metadata = {}
        
        if self.using_local_db:
            try:
                with open(BASE_PATH + "/items/index.json") as f:
                    metadata = json.load(f)
            except:
                raise FileNotFoundError("Metadata file not found")
            
        else:
            metadata = requests.get(BASE_URL + "items/index.json").json()
            if metadata.status_code != 200:
                raise Exception("Metadata request failed")
            
        return metadata
