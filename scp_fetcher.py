import re
import requests

class SCPFetcher:
    BASE_URL = "https://raw.githubusercontent.com/scp-data/scp-api/main/docs/data/scp/items/"
    INDEX_URL = BASE_URL + "index.json"

    def __init__(self):
        print("Loading SCP index...")
        self.index_data = requests.get(self.INDEX_URL).json()
        print(f"Loaded {len(self.index_data)} SCP entries.")

    def normalize_input(self, user_input):
        match = re.match(r'(?i)(?:scp[\s\-]*)?(\d+)', user_input.strip())
        if match:
            return f"scp-{match.group(1).zfill(3)}"
        else:
            raise ValueError("Invalid SCP ID format.")

    def get_metadata(self, user_input):
        key = self.normalize_input(user_input)
        data = self.index_data.get(key)
        if not data:
            raise ValueError(f"No metadata found for {key}")
        return key, data

    def get_article(self, user_input):
        key, metadata = self.get_metadata(user_input)
        content_file = metadata.get("content_file")
        if not content_file:
            raise ValueError(f"No content file listed for {key}")

        content_url = self.BASE_URL + content_file
        print(f"Fetching content from {content_file}...")
        content_data = requests.get(content_url).json()
        article = content_data.get(key)
        if not article:
            raise ValueError(f"No article found in {content_file} for {key}")
        return article

    def fetch(self, user_input):
        article = self.get_article(user_input)
        return {
            "title": article.get("scp"),
            "rating": article.get("rating"),
            "tags": article.get("tags"),
            "raw_html": article.get("raw_content"),
            "raw_source": article.get("raw_source"),
        }
