
from django.contrib.auth.decorators import login_required
from ..models import Keyword, RFQKeyword,RFQModel
from ..services.listRfqService import searchByAddress
from django.core.paginator import Paginator
from django.shortcuts import render

# RFQ search by address    
@login_required
def rfqList(request):
    if request.method == 'GET':
        rfqs = list(RFQModel.objects.all().prefetch_related('Addresses').values())
        print(rfqs[0])
        paginator = Paginator(rfqs, 10) 
    else:
        paginator = searchByAddress(request.POST['search'],request.POST['field'])
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, 'address/listAddress.html', {"page_obj": page_obj })