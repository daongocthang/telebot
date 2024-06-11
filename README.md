# PTB webhook with FastAPI
## Run in production
Start command:
```shell
gunicorn main:app -k uvicorn.workers.UvicornWorker --timeout 60
```
## Run locally
1. At first, run `ngrok` on local machine to get URL to receive webhook.
2. Add the URL to environment variables with name `WEBHOOK_URL`. Run `python main.py` to start telegram bot.

