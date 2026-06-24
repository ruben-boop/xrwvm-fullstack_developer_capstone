import requests
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus
from .models import Dealer, Review

load_dotenv()

backend_url = os.getenv('backend_url', default="http://localhost:3030")
sentiment_analyzer_url = os.getenv('sentiment_analyzer_url', default="http://localhost:5050/")

def get_request(endpoint, **kwargs):
    """
    Performs a GET to backend_url + endpoint.
    For local development, this now returns data from Django models
    instead of calling an external microservice.
    kwargs become query parameters.
    """
    print(f"GET from {backend_url + endpoint} with params {kwargs}")
    
    try:
        # Handle dealer endpoints
        if endpoint == "/fetchDealers":
            dealers = Dealer.objects.all().values()
            return list(dealers)
        
        elif endpoint.startswith("/fetchDealers/"):
            state = endpoint.split("/")[-1]
            dealers = Dealer.objects.filter(state=state.upper()).values()
            return list(dealers)
        
        elif endpoint.startswith("/fetchDealer/"):
            dealer_id = int(endpoint.split("/")[-1])
            dealer = Dealer.objects.filter(id=dealer_id).values()
            return list(dealer)[0] if dealer else None
        
        elif endpoint.startswith("/fetchReviews/dealer/"):
            dealer_id = int(endpoint.split("/")[-1])
            reviews = Review.objects.filter(dealership_id=dealer_id).values()
            return list(reviews)
        
        # Fallback to external API if needed
        request_url = backend_url + endpoint
        params = {}
        if kwargs:
            params.update({k: str(v) for k, v in kwargs.items()})
        
        response = requests.get(request_url, params=params)
        return response.json()
    
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        print("Network exception occurred")
        return None

def analyze_review_sentiments(text):
    """
    Analyzes sentiment of review text using external sentiment analyzer.
    Falls back to simple heuristic if external service is unavailable.
    """
    # URL-encode the text so spaces/special chars don't break the path
    encoded = quote_plus(text)
    request_url = sentiment_analyzer_url + "analyze/" + encoded
    try:
        response = requests.get(request_url)
        return response.json()
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        print("Sentiment analyzer unavailable, using fallback")
        # Simple fallback: check for positive/negative keywords
        text_lower = text.lower()
        if any(word in text_lower for word in ['good', 'great', 'excellent', 'amazing', 'love', 'best']):
            return {"sentiment": "positive"}
        elif any(word in text_lower for word in ['bad', 'terrible', 'awful', 'hate', 'worst', 'poor']):
            return {"sentiment": "negative"}
        else:
            return {"sentiment": "neutral"}

def post_review(data_dict):
    """
    Posts a review to the backend.
    Now saves directly to Django model.
    """
    try:
        # Extract review data
        dealer_id = data_dict.get("dealership")
        review_text = data_dict.get("review")
        reviewer_name = data_dict.get("name")
        car_make = data_dict.get("car_make", "")
        car_model = data_dict.get("car_model", "")
        car_year = data_dict.get("car_year", 2024)
        
        # Get sentiment
        sentiment_response = analyze_review_sentiments(review_text)
        sentiment = sentiment_response.get("sentiment", "neutral") if sentiment_response else "neutral"
        
        # Save to database
        from datetime import date
        review = Review.objects.create(
            dealership_id=dealer_id,
            name=reviewer_name,
            review=review_text,
            sentiment=sentiment,
            car_make=car_make,
            car_model=car_model,
            car_year=car_year,
            date=date.today()
        )
        
        return {"status": "success", "message": "Review posted successfully", "id": review.id}
    
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        print("Network exception occurred")
        return {"status": "error", "message": str(err)}
