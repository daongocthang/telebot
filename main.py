import uvicorn
import logging
from ptb import api

# Enable logging
logging.basicConfig(
    format="[%(asctime)s %(levelname)s] %(name)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

app = api.creat_app()

if __name__ == "__main__":
    try:
        uvicorn.run(app, host="127.0.0.1", port=8080, use_colors=False)
    except KeyboardInterrupt:
        logging.info("Exit")
