
from django.contrib.auth.decorators import login_required
from ..models import Keyword, RFQKeyword,RFQModel
from ..services.listRfqService import searchService, setCategories
from django.core.paginator import Paginator
from django.shortcuts import render

# RFQ search by address    
@login_required
def rfqList(request):
    keywords = list(Keyword.objects.values()) 
    modelKeywords = list(RFQKeyword.objects.all().values())
    defaultRfq = [x for x in modelKeywords if x['keyword_id'] == 12]
    ids = [val['rfq_id'] for val in defaultRfq]
    rfqs = list(RFQModel.objects.filter(id__in=ids).all().values())
    paginator = Paginator(rfqs, 10) 
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, 'address/listAddress.html', {"page_obj": page_obj, 'keywords': keywords})