from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from .forms import SyncRFQS
from .services.syncService import syncDataGeneral, syncByCategory
from .services.listRfqService import searchService, setCategories, getCategoryDist
from django.core.exceptions import ObjectDoesNotExist
from .models import RFQModel, UserOwner, Attachments, Modifications, TokensGsa, Category, RFQCategory, HistorySync
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

def home(request):
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
        username = request.user.username
        user = User.objects.get(username=username)
        if request.POST['tokenGSA']:
            syncDataGeneral(request.POST['tokenGSA'],user)
            syncByCategory(request.POST['tokenGSA'])
        else:
            token = TokensGsa.objects.last()
            syncDataGeneral(token.tokenGSA, user)
            syncByCategory(token.tokenGSA)
        return redirect('listRfqs')


@login_required
def rfqList(request):
    categories = list(Category.objects.values()) 
    modelCategories = list(RFQCategory.objects.all().values())

    defaultRfq = [x for x in modelCategories if x['category_id'] == 12]
    ids = [val['rfq_id'] for val in defaultRfq]
    if request.method == 'GET':
        rfqs = list(RFQModel.objects.filter(id__in=ids).all().values())
        listRfqs = setCategories(rfqs,categories,modelCategories)
        paginator = Paginator(listRfqs, 10) 
    else:
        paginator = searchService(request.POST['search'],request.POST['field'],request.POST['wordSerach'],ids,categories,modelCategories)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, 'rfqs/list_rqs.html', {"page_obj": page_obj, "categories": categories })

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
            return render(request, 'common/login.html', { "error": "Username or password is incorrect."})

        login(request, user)
        return redirect('dashboard')
    
@login_required
def signout(request):
    logout(request)
    return redirect('home')

@login_required
def dashboard(request):
    history = HistorySync.objects.select_related('user').order_by('-time').all()[:10]
    catDist = getCategoryDist()
    modelCategories = list(RFQCategory.objects.all().values())
    defaultRfq = [x for x in modelCategories if x['category_id'] == 12]
    ids = [val['rfq_id'] for val in defaultRfq]
    rfqs = list(RFQModel.objects.filter(id__in=ids).all()[:10])
    
    return render(request, 'common/dashboard.html',{ 'history': history, 'catDist': catDist, 'rfqs': rfqs })

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
    return redirect('profile')

@login_required
def savePassword(request):
    username = request.user.username
    user = User.objects.get(username=username)
    if request.POST['newpassword'] == request.POST['renewpassword']:
        user.set_password(request.POST['newpassword'])
        user.save()
    return redirect('profile')