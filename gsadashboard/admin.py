from django.contrib import admin
from .models import RFQModel, Attachments, Modifications,UserOwner, TokensGsa
# Register your models here.

admin.site.register(RFQModel)
admin.site.register(Attachments)
admin.site.register(Modifications)
admin.site.register(UserOwner)
admin.site.register(TokensGsa)