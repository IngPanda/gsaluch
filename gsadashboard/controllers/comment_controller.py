from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from ..models import LuchRFQComents
from datetime import datetime

@login_required
def saveComment(request):
    rfqId = request.POST['rfqId']
    comment = request.POST['comment']
    userId = request.POST['userId']
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    LuchRFQComents.objects.create(
        comment = comment,
        rfq_id= rfqId,
        user_id=userId,
        time = time
    )

    return redirect('/rfq_view/'+rfqId)