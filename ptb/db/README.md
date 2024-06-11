# Usage
## Start
First of all, you need to obtain firebase credentials and the firebase database url.
## Instantaition
### From environment variables (Recommended)
Store the database URL in an environment variable FIREBASE_URL and the config as a json string in an environment variable `FIREBASE_CREDENTIALS`.
```python
from db.firebase import FirebasePersistence
from telegram.ext import Application

firebase_persistence = FirebasePersistence.from_env()
app = Application.builder().token('TELEGRAM_BOT_TOKEN').persistence(firebase_persistence).build()
```
### Direction
You can also just pass the firebase credentials as URL as simple init parameters
```python
from db.firebase import FirebasePersistence
from telegram.ext import Application

firebase_persistence = FirebasePersistence(database_url='FIREBASE_DATABASE_URL', credentials='FIREBASE_CREDENTIALS_DICT')

app = Application.builder().token('TELEGRAM_BOT_TOKEN').persistence(firebase_persistence).build()
```
