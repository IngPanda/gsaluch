from django.contrib.auth.decorators import login_required
from ..models import VendorCategory, CategoryByRFQ
from django.core.paginator import Paginator
from django.shortcuts import render

#Vendor List
@login_required
def vendorList(request,cat):
    data = VendorCategory.objects.filter(category_id = cat)
    category = CategoryByRFQ.objects.select_related('rfq').get(id=cat)
    paginator = Paginator(data, 20) 
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, 'vendors/vendors.html', {"page_obj": page_obj, 'category': category })