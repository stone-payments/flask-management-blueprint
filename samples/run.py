"""A module with the sole purpose of running the Flask Web API."""
import os

from api import create_api

if __name__ == "__main__":
    API = create_api(__name__)
    API.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
