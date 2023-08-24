from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from ..services.syncService import syncDataGeneral, syncByCategory, syncDetail
from ..forms import SyncRFQS
from ..models import Addresses, CategoryByRFQ, LuchRFQComents, Modifications, RFQHistorySync, TokensGsa, Keyword, RFQKeyword, RFQModel, Attachments
from django.contrib.auth.models import User
from ..services.listRfqService import searchService, setCategories
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist

# Synchronizes all RFQS
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
# RFQ table view controller    
@login_required
def rfqList(request):
    keywords = list(Keyword.objects.values()) 
    modelKeywords = list(RFQKeyword.objects.all().values())
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


# Detail of an RFQ
@login_required
def rfqView(request, id):
    username = request.user.username
    user = User.objects.get(username=username)
    if request.method == 'POST':
        token = TokensGsa.objects.last()
        syncDetail(token.tokenGSA, user,request.POST['idGSA'])
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
        categoryGSA = list(CategoryByRFQ.objects.filter(rfq_id=id))
    except ObjectDoesNotExist:
        mods = list()
    try:
        words = list(RFQKeyword.objects.select_related('keyword').filter(rfq_id=id).exclude(keyword_id=12))
    except ObjectDoesNotExist:
        words = list()
    try:
        history = list(RFQHistorySync.objects.select_related('user').filter(rfq_id=id).order_by('-time').all()[:10])
    except ObjectDoesNotExist:
        history = list()
    try:
        adresses = list(Addresses.objects.filter(rfq_id=id).values())
    except ObjectDoesNotExist:
        adresses = list()
    try:
        comments = list(LuchRFQComents.objects.select_related('user').filter(rfq_id=id).order_by('-time').all())
    except ObjectDoesNotExist:
        comments = list()
    return render(request, 'rfqs/view.html', { 'rfq': rfq, 'atts': atts, 'mods': mods, 'words': words, 'history': history, 'adresses': adresses, 'categories': categoryGSA, 'comments': comments, 'user': user })
