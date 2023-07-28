from django.core.paginator import Paginator
from ..models import RFQModel,RFQCategory,Category,RFQKeyword, Keyword

def getCategoryDist():
    categoriesList = list(Keyword.objects.all().values())
    for cat in categoriesList:
        modelCategories = list(RFQKeyword.objects.filter(keyword_id = cat['id']).values())
        cat['value'] = len(modelCategories)
    return [x for x in categoriesList if x['value'] > 0 and x['name'] != 'Default' ]

def setCategories(rfqs,cat,rfqCat):
    for rfq in rfqs:
        cateRfq = [x for x in rfqCat if x['rfq_id'] == rfq['id']]
        ids = [val['keyword_id'] for val in cateRfq]
        catList = [x for x in cat if x['id'] in ids and x['name'] != 'Default' ]
        rfq['keywords']=catList
    
    return rfqs

def searchService(search, field, wordSerach,ids,cat,rfqCat):
    baseQuery = RFQModel.objects
    cantPage = 10;
    if search:
        if field == 'id':
            baseQuery = baseQuery.filter(idGSA__contains=search)
            cantPage = 100
        elif field == 'title':
            baseQuery = baseQuery.filter(title__contains=search)
            cantPage = 100
        elif field == 'description':
            baseQuery = baseQuery.filter(description__contains=search)
            cantPage = 100
    if wordSerach:
        if wordSerach != '0':
            modelCategories = list(RFQKeyword.objects.filter(keyword_id = wordSerach).values())
            ids = [val['rfq_id'] for val in modelCategories]
            baseQuery = baseQuery.filter(id__in=ids)
            cantPage = 100
    else: 
        baseQuery = baseQuery.filter(id__in=ids)

    data =  list(baseQuery.values())
    listRfqs = setCategories(data,cat,rfqCat)
    paginator = Paginator(data, cantPage) 
    return paginator

