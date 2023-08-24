from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def signup(request):
    if request.method == 'GET':
        return render(request, 'common/signup.html')
    if request.method == 'POST':
        if request.POST['password'] == request.POST['confirmPassword']:
            try:
                user = User.objects.create_user(username=request.POST["emailAddress"], password=request.POST["password"], first_name = request.POST["firstName"], last_name= request.POST["lastName"], email= request.POST["emailAddress"])
                user.save()
                login(request, user)
                return render(request, 'common/signup.html',{'success': 'Usuario creado'})
            except:
                return render(request, 'common/signup.html',{'error': 'Usuario ya existe'})
    return render(request, 'common/signup.html',{'error': 'Contrasenas no son iguales'})

def signin(request):
    if request.method == 'GET':
        return render(request, 'common/login.html')
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'common/login.html', { "errorData": "Username o contraseña son incorrectas."})

        login(request, user)
        return redirect('dashboard')
    
@login_required
def signout(request):
    logout(request)
    return redirect('home')