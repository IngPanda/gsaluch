from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from .forms import SyncRFQS
from .services.syncService import syncData
from django.core.exceptions import ObjectDoesNotExist
from .models import RFQModel, UserOwner, Account, Attachments, Modifications
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

def index(request):
    title = 'Luch Gsa Project'
    return render(request, 'common/index.html', {
        'title': title
    })

@login_required
def sync_rfq(request):
    if request.method == 'GET':
        return render(request, 'sync/sync.html', {
            'form': SyncRFQS()
        })
    else:
        syncData(request.POST['tokenGSA'])
        return redirect('index')

@login_required
def rfqList(request):
    if request.method == 'GET':
        rfqs = list(RFQModel.objects.values())
    else:
        if request.POST['field'] == 'id':
            rfqs = list(RFQModel.objects.filter(idGSA__contains=request.POST['search']).values())
        elif request.POST['field'] == 'title':
            rfqs = list(RFQModel.objects.filter(title__contains=request.POST['search']).values())
        elif request.POST['field'] == 'description':
            rfqs = list(RFQModel.objects.filter(description__contains=request.POST['search']).values())
        else:
            rfqs = list()
    paginator = Paginator(rfqs, 10) 
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    print(request.POST)
    return render(request, 'rfqs/list_rqs.html', {"page_obj": page_obj})

@login_required
def rfqView(request, id):
    rfq = get_object_or_404(RFQModel, id=id)
    try:
        atts = list(Attachments.objects.filter(rfq_id=id))
    except ObjectDoesNotExist:
        att = list()
    try:
        mods = list(Modifications.objects.filter(rfq_id=id))
    except ObjectDoesNotExist:
        mods = list()
    return render(request, 'rfqs/view.html', { 'rfq': rfq, 'atts': atts, 'mods': mods})


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
            return render(request, 'signin.html', { "error": "Username or password is incorrect."})

        login(request, user)
        return redirect('listRfqs')
    
@login_required
def signout(request):
    logout(request)
    return redirect('index')