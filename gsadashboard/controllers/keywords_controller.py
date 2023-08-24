from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from ..models import TokensGsa, Keyword
from django.core.exceptions import ObjectDoesNotExist
from ..services.syncService import syncSingleCategory
from django.contrib.auth.models import User

@login_required
def listKeywords(request):
    keys = list(Keyword.objects.filter(delete= False).values())
    return render(request, 'keywords/keywords.html',{ 'keys': keys })

@login_required
def createKeywords(request):
    if request.method == 'POST':
        try: 
          username = request.user.username
          user = User.objects.get(username=username)
          key = Keyword.objects.get(name= request.POST['name'], delete = False)
          key.name = name= request.POST['name']
          key.activeSearch =  True if request.POST['search'] == 'on' else False
          key.save()
          if request.POST['sync'] == 'on':
              token = TokensGsa.objects.last()
              syncSingleCategory(token.tokenGSA, key.name, key.id, user)
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
            username = request.user.username
            user = User.objects.get(username=username)
            key = Keyword.objects.get(id = request.POST['keywordId'])
            key.name = name= request.POST['name']
            key.activeSearch =  True if request.POST['search'] == 'on' else False
            key.save()
            print(request.POST.get('sync'))
            if request.POST.get('sync') == 'on':
                token = TokensGsa.objects.last()
                syncSingleCategory(token.tokenGSA, key.name, key.id, user)
            return redirect('keywords')
    except ObjectDoesNotExist:
        return redirect('keywords')
    
@login_required
def editKeywordsState(request, id, state):
    try:
        key = Keyword.objects.get(id = id)
        key.activeSearch =  True if state == 'True' else False
        key.save()
        return redirect('keywords')
    except ObjectDoesNotExist:
        return redirect('keywords')
