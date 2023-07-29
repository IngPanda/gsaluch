from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from .forms import SyncRFQS
from .services.syncService import syncDataGeneral, syncByCategory, syncSingleCategory,syncDetail
from .services.listRfqService import searchService, setCategories, getCategoryDist
from django.core.exceptions import ObjectDoesNotExist
from .models import RFQModel, UserOwner, Attachments, Modifications, TokensGsa, Category, RFQCategory, HistorySync, Keyword,RFQKeyword
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
        try:
            username = request.user.username
            user = User.objects.get(username=username)
            if request.POST['tokenGSA']:
                syncDataGeneral(request.POST['tokenGSA'],user)
                syncByCategory(request.POST['tokenGSA'])
            else:
                token = TokensGsa.objects.last()
                syncDataGeneral(token.tokenGSA, user)
                syncByCategory(token.tokenGSA)
            return render(request, 'sync/sync.html', {
                'form': SyncRFQS(),
                'successData': "Informacion sincronizada con exito !!!"
            })
        except:
            return render(request, 'sync/sync.html', {
                'form': SyncRFQS(),
                'errorData': "Error al sincronizar"
            })


@login_required
def rfqList(request):
    keywords = list(Keyword.objects.values()) 
    modelKeywords = list(RFQKeyword.objects.all().values())
    print(request.GET)
    defaultRfq = [x for x in modelKeywords if x['keyword_id'] == 12]
    ids = [val['rfq_id'] for val in defaultRfq]
    if request.method == 'GET':
        try:
            paginator = searchService(None,None,request.GET['keyword'],ids,keywords,modelKeywords)
        except:
            rfqs = list(RFQModel.objects.filter(id__in=ids).all().values())
            listRfqs = setCategories(rfqs,keywords,modelKeywords)
            paginator = Paginator(listRfqs, 10) 
    else:
        paginator = searchService(request.POST['search'],request.POST['field'],request.POST['wordSerach'],ids,keywords,modelKeywords)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, 'rfqs/list_rqs.html', {"page_obj": page_obj, "keywords": keywords })

@login_required
def rfqView(request, id):
    if request.method == 'POST':
        token = TokensGsa.objects.last()
        syncDetail(token.tokenGSA, request.POST['idGSA'])
        return redirect(request.META.get('HTTP_REFERER'))
    rfq = get_object_or_404(RFQModel, id=id)
    try:
        atts = list(Attachments.objects.filter(rfq_id=id))
    except ObjectDoesNotExist:
        att = list()
    try:
        mods = list(Modifications.objects.filter(rfq_id=id))
    except ObjectDoesNotExist:
        mods = list()
    try:
        words = list(RFQKeyword.objects.select_related('keyword').filter(rfq_id=id).exclude(keyword_id=12))
    except ObjectDoesNotExist:
        words = list()
    return render(request, 'rfqs/view.html', { 'rfq': rfq, 'atts': atts, 'mods': mods, 'words': words})


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

@login_required
def dashboard(request):
    history = HistorySync.objects.select_related('user').order_by('-time').all()[:10]
    catDist = getCategoryDist()
    modelCategories = list(RFQKeyword.objects.all().values())
    defaultRfq = [x for x in modelCategories if x['keyword_id'] == 12]
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

@login_required
def listKeywords(request):
    keys = list(Keyword.objects.filter(delete= False).values())
    return render(request, 'keywords/keywords.html',{ 'keys': keys })

@login_required
def createKeywords(request):
    if request.method == 'POST':
        try: 
          key = Keyword.objects.get(name= request.POST['name'], delete = False)
          key.name = name= request.POST['name']
          key.activeSearch =  True if request.POST['search'] == 'on' else False
          key.save()
          if request.POST['sync'] == 'on':
              token = TokensGsa.objects.last()
              syncSingleCategory(token.tokenGSA, key.name, key.id)
          return render(request, 'keywords/create.html',{ 'successData': "Palabra clave Actualizada" })
        except ObjectDoesNotExist:
            keyword = Keyword.objects.create(
                name= request.POST['name'],
                icon = "bx bx-message-square",
                activeSearch = True if request.POST['search'] == 'on' else False 
            )
            return render(request, 'keywords/create.html',{ 'successData': "Palabra clave creada" })
    else:
        return render(request, 'keywords/create.html')
    

@login_required
def deleteKeywords(request, id):
    try: 
        key = Keyword.objects.get(id = id, delete = False)
        key.delete = True
        key.save()
        return redirect('keywords')
    except ObjectDoesNotExist:
        return redirect('keywords')

@login_required
def editKeywords(request, id):
    try:
        if request.method == 'GET': 
            key = Keyword.objects.get(id = id, delete = False)
            checkValueSync =  "checked" if key.activeSearch else " "
            return render(request, 'keywords/edit.html', {'key': key, 'checkValueSync': checkValueSync})
        else:
            key = Keyword.objects.get(id = request.POST['keywordId'])
            key.name = name= request.POST['name']
            key.activeSearch =  True if request.POST['search'] == 'on' else False
            key.save()
            if request.POST['sync'] == 'on':
              token = TokensGsa.objects.last()
              syncSingleCategory(token.tokenGSA, key.name, key.id)
            return redirect('keywords')
    except ObjectDoesNotExist:
        return redirect('keywords')

@login_required
def saveToken(request):
     if request.method == 'GET':
         return render(request, 'sync/token.html')
     else:
        keyword = TokensGsa.objects.create(
            tokenGSA= request.POST['token'],
        )
        return render(request, 'sync/token.html', { 'successData': "Token guardado" })
     