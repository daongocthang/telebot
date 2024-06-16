import json
import os
from dotenv import load_dotenv

load_dotenv()
creds = os.getenv("FIREBASE_CREDENTIALS")
json_str = json.loads(creds)
print(json_str)
