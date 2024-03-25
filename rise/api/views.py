from django.shortcuts import render, redirect
from django.http import HttpResponse
from api.models import CustomUser
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.template import loader
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

def index(request):
    return HttpResponse("Hello, world. You're at the api index.")

# Auth
class UserLoginForm(AuthenticationForm):
    def __init__(self, request, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.fields['username'].label = "Логин"
        self.fields['password'].label = "Пароль"

class UserRegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Логин"
        self.fields['password1'].label = "Пароль"
        self.fields['password2'].label = "Подтвердите пароль"
    
    class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'password2')

@csrf_exempt
def register_user(request):
    if request.method == 'GET':
        # Render the register template
        template = loader.get_template("registration/register.html")
        context = {
            'form': UserRegisterForm()
        }
        return HttpResponse(template.render(context, request))
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # Create user from form data
            form.save(commit=False)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = CustomUser.objects.create_user(username=username, password=password)
            # Redirect user to login
            return redirect('login_user')
        else:
            # Render the register template with error
            template = loader.get_template("registration/register.html")
            context = {
                'form': form
            }
            return HttpResponse(template.render(context, request))
    # Return an error response for unsupported request method
    return JsonResponse({"error": "Invalid request method."}, status=405)

@csrf_exempt
def user_profile(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            # Render the register template
            template = loader.get_template("user/profile.html")
            context = {
                'user': request.user
            }
            return HttpResponse(template.render(context, request))
        else:
            # Redirect to login
            return redirect('login_user')
    # Return an error response for unsupported request method
    return JsonResponse({"error": "Invalid request method."}, status=405)
