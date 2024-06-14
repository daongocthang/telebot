import uvicorn
from ptb import api, config

logger = config.get_logger(__name__)

app = api.creat_app()

if __name__ == "__main__":
    try:
        uvicorn.run(
            app, host="127.0.0.1", port=8080, use_colors=False, timeout_keep_alive=60
        )
    except KeyboardInterrupt:
        logger.info("Exit")
