from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.models import User

@login_required
def profile(request):
    username = request.user.username
    user = User.objects.get(username=username)
    return render(request, 'common/profile.html',{ 'userLog': user })

@login_required
def saveUserData(request):
    username = request.user.username
    user = User.objects.get(username=username)
    if request.POST['first_name']:
        user.first_name = request.POST['first_name']
    if request.POST['last_name']:
        user.last_name = request.POST['last_name'] 
    if request.POST['email']:
        user.email = request.POST['email']  
    user.save()
    return render(request, 'common/profile.html',{ 'userLog': user, 'successData': "Data de perfil actualizados" })

@login_required
def savePassword(request):
    username = request.user.username
    user = User.objects.get(username=username)
    if request.POST['newpassword'] == request.POST['renewpassword']:
        user.set_password(request.POST['newpassword'])
        user.save()
    else:
        return render(request, 'common/profile.html',{ 'userLog': user, 'errorData': "Las contraseñas no son iguales" })
    return render(request, 'common/profile.html',{ 'userLog': user, 'successData': "Contraseña actualizada" })