
import asyncio
import logging
import uvicorn
import sys
from litellm.proxy.proxy_server import app, initialize

logging.basicConfig(filename='proxy.log', level=logging.INFO)

# Check for a config file path from the command line arguments
if len(sys.argv) > 1:
    config_path = sys.argv[1]
else:
    # Default config file path
    config_path = "C:/Users/user/Downloads/litellm/proxy_config.yaml"

# Run the async initialization
logging.info(f"Initializing proxy with config: {config_path}")
print(f"Initializing LiteLLM proxy with config: {config_path}")
asyncio.run(initialize(config=config_path))
logging.info("Proxy initialization complete.")

# Start the server
logging.info("Starting Uvicorn server.")
print("Starting Uvicorn server on http://0.0.0.0:8000")
uvicorn.run(app, host="0.0.0.0", port=8000)
