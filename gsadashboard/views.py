from django.shortcuts import render
from django.shortcuts import  render, redirect
from .services.listRfqService import getCategoryDist
from .models import  RFQModel, TokensGsa, HistorySync,RFQKeyword, VendorCategory
from django.contrib.auth.decorators import login_required

def home(request):
    title = 'Luch Gsa Project'
    return render(request, 'common/index.html', {
        'title': title
    })

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
def saveToken(request):
     if request.method == 'GET':
         return render(request, 'sync/token.html')
     else:
        keyword = TokensGsa.objects.create(
            tokenGSA= request.POST['token'],
        )
        return render(request, 'sync/token.html', { 'successData': "Token guardado" })
     