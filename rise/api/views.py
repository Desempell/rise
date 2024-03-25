from django.shortcuts import render
from django.http import HttpResponse
from api.models import CustomUser
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

def index(request):
    return HttpResponse("Hello, world. You're at the api index.")

@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        # Get the user data from the request
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Create a new user object
        user = CustomUser.objects.create_user(username=username, password=password)

        # Return the user ID in the response
        return JsonResponse({"message": "User registered successfully", "user_id": user.id})

    else:
        # Return an error response for unsupported request method
        return JsonResponse({"error": "Invalid request method."}, status=405)

