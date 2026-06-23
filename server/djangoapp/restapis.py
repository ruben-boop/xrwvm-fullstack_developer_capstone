import requests
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()

backend_url = os.getenv('backend_url', default="http://localhost:3030")
sentiment_analyzer_url = os.getenv('sentiment_analyzer_url', default="http://localhost:5050/")

def get_request(endpoint, **kwargs):
    """
    Performs a GET to backend_url + endpoint.
    kwargs become query parameters.
    """
    request_url = backend_url + endpoint
    params = {}
    if kwargs:
        # ensure values are strings (requests will handle encoding)
        params.update({k: str(v) for k, v in kwargs.items()})

    print(f"GET from {request_url} with params {params}")
    try:
        response = requests.get(request_url, params=params)
        return response.json()
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        print("Network exception occurred")
        return None

def analyze_review_sentiments(text):
    # URL-encode the text so spaces/special chars don't break the path
    encoded = quote_plus(text)
    request_url = sentiment_analyzer_url + "analyze/" + encoded
    try:
        response = requests.get(request_url)
        return response.json()
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        print("Network exception occurred")
        return None

def post_review(data_dict):
    request_url = backend_url + "/insert_review"
    try:
        response = requests.post(request_url, json=data_dict)
        print(response.json())
        return response.json()
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        print("Network exception occurred")
        return None
