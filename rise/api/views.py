import json

from django.shortcuts import render, redirect
from django.http import HttpResponse
from api.models import CustomUser, Expenses, ExpenseType, Suggestions, SuggestionType
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpRequest
from django.template import loader
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm



def index(request):
    return HttpResponse("Hello, world. You're at the api index.")

# Auth
@csrf_exempt
def register_user(request:HttpRequest):
    if request.method == 'POST':
        # Get the user data from the request
        username = json.loads(request.body).get("username")
        password = json.loads(request.body).get('password')

        user = CustomUser.objects.create_user(username=username, password=password)

        # Return the user ID in the response
        return JsonResponse({"message": "User registered successfully", "user_id": user.id})
    else:
        # Return an error response for unsupported request method
        return JsonResponse({"error": "Invalid request method."}, status=405)

@csrf_exempt
def login_user(request:HttpRequest):
    if request.method == 'POST':
        # Check if user is not logged in yet
        session_user_id = request.session.get('user_id')
        if session_user_id is not None:
            return JsonResponse({"error": "Cannot log into multiple users"}, status=403)

        # Get the user data from the request
        username = json.loads(request.body).get('username')

        try:
            # Find matching user
            user = CustomUser.objects.get(username=username)
            password = json.loads(request.body).get('password')

            # Login if passwords match
            if user.check_password(password):
                request.session['user_id'] = user.id
                return JsonResponse({"message": "Login successful"})
            else:
                return JsonResponse({"error": "Username or password not matching"}, status=406)
        except CustomUser.DoesNotExist:
            # Return an error response for a user that does not exist
            return JsonResponse({"error": "User does not exist"}, status=404)
    else:
        # Return an error response for unsupported request method
        return JsonResponse({"error": "Invalid request method."}, status=405)

@csrf_exempt
def get_user(request:HttpRequest):
    if request.method == 'POST':
        # Get the user data from the request
        username = request.POST.get('username')

        try:
            # Find matching user
            user = CustomUser.objects.get(username=username)

            # Construct response
            response = {
                "message": "User found successfully",
                "user_id": user.id,
                "username": user.username
            }

            # If the target user is logged in, show additional info
            session_user_id = request.session.get('user_id')
            if (session_user_id is not None) and (user.id == session_user_id):
                response['email'] = user.email

            return JsonResponse(response)
        except CustomUser.DoesNotExist:
            # Return an error response for a user that does not exist
            return JsonResponse({"error": "User does not exist"}, status=404)
    else:
        # Return an error response for unsupported request method
        return JsonResponse({"error": "Invalid request method."}, status=405)

@csrf_exempt
def logout_user(request:HttpRequest):
    if request.method == 'POST':
        session_user_id = request.session.get('user_id')
        if session_user_id is not None:
            # Log out if logged in
            request.session['user_id'] = None
            return JsonResponse({"message": "Logout successful"})
        else:
            # Return an error response for user that is not logged in yet
            return JsonResponse({"error": "User not logged in"}, status=401)
    else:
        # Return an error response for unsupported request method
        return JsonResponse({"error": "Invalid request method."}, status=405)

@csrf_exempt
def delete_user(request:HttpRequest):
    if request.method == 'POST':
        # Get the user data from the request
        username = request.POST.get('username')

        try:
            # Find matching user
            user = CustomUser.objects.get(username=username)
            password = request.POST.get('password')

            # Delete if passwords match
            if user.check_password(password):
                user.delete()
                return JsonResponse({"message": "User deleted successfully"})
            else:
                return JsonResponse({"error": "Username or password not matching"}, status=406)
        except CustomUser.DoesNotExist:
            # Return an error response for a user that does not exist
            return JsonResponse({"error": "User does not exist"}, status=404)
    else:
        # Return an error response for unsupported request method
        return JsonResponse({"error": "Invalid request method."}, status=405)

@csrf_exempt
def create_expenses(request:HttpRequest):
    if request.method == 'POST':
        # Get the user data from the request
        userID = request.POST.get('userID')
        date = request.POST.get('date')
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        type = request.POST.get('typeName')
        try:
            user = CustomUser.objects.get(userID=userID)
            type = ExpenseType.objects.get(name=type)
            expenses = Expenses.objects.create(user=user, date=date, amount=amount, description=description, type=type)
        except:
            return JsonResponse({"error": "ERROR."}, status=405)
    else:
        return JsonResponse({"error": "Invalid request method."}, status=405)

@csrf_exempt
def create_suggestion(request:HttpRequest):
    if request.method == 'POST':
        # Get the user data from the request
        userID = request.POST.get('userID')
        description = request.POST.get('description')
        saved_money = request.POST.get('saved_money')
        suggestion_type = request.POST.get('typeName')
        try:
            user = CustomUser.objects.get(userID=userID)
            suggestion_type = SuggestionType.objects.get(name=suggestion_type)
            suggestions = Suggestions.objects.create(user=user, saved_money=saved_money, description=description, suggestion_type=suggestion_type)
        except:
            return JsonResponse({"error": "ERROR."}, status=405)
    else:
        return JsonResponse({"error": "Invalid request method."}, status=405)


