import json
from datetime import datetime

from django.shortcuts import render, redirect
from django.http import HttpResponse
from api.models import CustomUser, Expenses, ExpenseType, Suggestions, SuggestionType
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpRequest
from django.template import loader
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout

def index(request):
    return HttpResponse("Hello, world. You're at the api index.")

@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get('password')

        user = CustomUser.objects.create_user(username=username, password=password)
        return JsonResponse({"message": "User registered successfully", "user_id": user.id})
    return JsonResponse({"error": "Invalid request method."}, status=405)

@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"message": "Login successful"})
        return JsonResponse({"error": "Username or password not matching"}, status=406)
    return JsonResponse({"error": "Invalid request method."}, status=405)

@csrf_exempt
def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({"message": "Logout successful"})
    return JsonResponse({"error": "Invalid request method."}, status=405)

@csrf_exempt
def check_auth_status(request):
    if request.user.is_authenticated:
        return JsonResponse({"isAuthenticated": True, "username": request.user.username})
    return JsonResponse({"isAuthenticated": False})

@csrf_exempt
def get_user(request:HttpRequest):
    if request.method == 'POST':
        # Get the user data from the request
        username = json.loads(request.body).get('username')

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
        username = json.loads(request.body).get('username')

        try:
            # Find matching user
            user = CustomUser.objects.get(username=username)
            password = json.loads(request.body).get('password')

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
def create_expenses(request: HttpRequest):
    if request.method == 'POST':
        try:
            # Parse request body once
            data = json.loads(request.body)

            # Get the user data from the request
            userID = data.get('userID')
            date_str = data.get('date')
            amount = data.get('amount')
            description = data.get('description')
            type_id = data.get('typeID')

            # Convert date string to datetime object
            date = datetime.strptime(date_str, '%d/%m/%Y').date()

            # Get user and type objects
            user = CustomUser.objects.get(id=userID)
            type = ExpenseType.objects.get(id=type_id)

            # Create expense
            expenses = Expenses.objects.create(user=user, date=date, amount=amount, description=description, type=type)

            return JsonResponse({"Success": f"Created expenses {expenses.id}."}, status=201)
        except CustomUser.DoesNotExist:
            return JsonResponse({"error": "User not found."}, status=404)
        except ExpenseType.DoesNotExist:
            return JsonResponse({"error": "Expense type not found."}, status=404)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            return JsonResponse({"error": "An error occurred: " + str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method."}, status=405)

@csrf_exempt
def create_expense_type(request: HttpRequest):
    if request.method == 'POST':
        try:
            # Parse request body
            data = json.loads(request.body)
            name = data.get('name')

            if not name:
                return JsonResponse({"error": "Name field is required."}, status=400)

            # Create ExpenseType
            expense_type = ExpenseType.objects.create(name=name)

            return JsonResponse({"Success": f"Created expense type {expense_type.id}."}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON."}, status=400)
        except Exception as e:
            return JsonResponse({"error": "An error occurred: " + str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method."}, status=405)


@csrf_exempt
def get_expense_types(request):
    if request.method == 'GET':
        try:
            expense_types = ExpenseType.objects.all()
            expense_types_list = [
                {
                    "id": expense_type.id,
                    "name": expense_type.name
                } for expense_type in expense_types
            ]
            return JsonResponse(expense_types_list, safe=False, status=200)
        except Exception as e:
            return JsonResponse({"error": "An error occurred: " + str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method."}, status=405)


@csrf_exempt
def create_suggestion(request: HttpRequest):
    if request.method == 'POST':
        try:
            # Parse request body
            data = json.loads(request.body)

            # Extract data from request
            userID = data.get('userID')
            description = data.get('description')
            saved_money = data.get('saved_money')
            rating = data.get('rating')
            suggestion_type_id = data.get('typeID')

            # Validate required fields
            if not all([userID, description, saved_money, rating, suggestion_type_id]):
                return JsonResponse({"error": "All fields are required."}, status=400)

            # Fetch related objects
            user = CustomUser.objects.get(id=userID)
            suggestion_type = SuggestionType.objects.get(id=suggestion_type_id)

            # Create suggestion
            suggestion = Suggestions.objects.create(
                user=user,
                saved_money=saved_money,
                description=description,
                suggestion_type=suggestion_type,
                rating=rating
            )

            return JsonResponse({"Success": f"Created suggestion {suggestion.id}."}, status=201)
        except CustomUser.DoesNotExist:
            return JsonResponse({"error": "User not found."}, status=404)
        except SuggestionType.DoesNotExist:
            return JsonResponse({"error": "Suggestion type not found."}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON."}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method."}, status=405)


@csrf_exempt
def get_suggestions_by_user_id(request, user_id):
    if request.method == 'GET':
        try:
            user = CustomUser.objects.get(id=user_id)
            suggestions = Suggestions.objects.filter(user=user)

            if suggestions.exists():
                suggestions_list = [
                    {
                        "user_id": suggestion.user_id,
                        "suggestion_type": suggestion.suggestion_type.name,
                        "saved_money": suggestion.saved_money,
                        "description": suggestion.description,
                        "rating": suggestion.rating
                    } for suggestion in suggestions
                ]
                return JsonResponse(suggestions_list, safe=False, status=200)
            else:
                return JsonResponse({"error": "No suggestions found for the user."}, status=404)

        except CustomUser.DoesNotExist:
            return JsonResponse({"error": "User not found."}, status=404)

    else:
        return JsonResponse({"error": "Invalid request method."}, status=405)


@csrf_exempt
def create_suggestion_type(request: HttpRequest):
    if request.method == 'POST':
        try:
            # Parse request body
            data = json.loads(request.body)
            name = data.get('name')
            price = data.get('price')

            if not name:
                return JsonResponse({"error": "Name field is required."}, status=400)
            if not price:
                price = 0

            # Create SuggestionType
            suggestion_type = SuggestionType.objects.create(name=name, price=price)

            return JsonResponse({"Success": f"Created suggestion type {suggestion_type.id}."}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON."}, status=400)
        except Exception as e:
            return JsonResponse({"error": "An error occurred: " + str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method."}, status=405)
