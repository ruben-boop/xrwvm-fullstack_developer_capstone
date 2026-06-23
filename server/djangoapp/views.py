# Uncomment the required imports before adding the code
import json
import logging
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Third-party or local app imports
from .models import CarMake, CarModel  # noqa: F401
from .populate import initiate  # noqa: F401
from .restapis import (
    analyze_review_sentiments,
    get_request,
    post_review,
)


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create a `login_request` view to handle sign in request
@csrf_exempt
def login_user(request):
    # Get username and password from request.POST dictionary
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    # Try to check if provide credential can be authenticated
    user = authenticate(username=username, password=password)
    response_data = {"userName": username}
    if user is not None:
        # If user is valid, call login method to login current user
        login(request, user)
        response_data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(response_data)


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    if request.method == 'POST':  # Logout via POST for better CSRF protection
        logout(request)
        return JsonResponse(
            {"success": True, "message": "Logged out successfully"}
        )
    return JsonResponse(
        {"success": False, "error": "Invalid request method"}, status=400
    )


# Create a `registration` view to handle sign up request
@csrf_exempt
def registration(request):
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']
    username_exist = False

    try:
        User.objects.get(username=username)
        username_exist = True
    except User.DoesNotExist:
        pass
    
    if not username_exist:
        User.objects.create_user(username=username, password=password, 
                             first_name=first_name, last_name=last_name, email=email)
        return JsonResponse({"userName": username, "status": "Registered"})
