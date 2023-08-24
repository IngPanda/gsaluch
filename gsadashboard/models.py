from django.db import models
from django.contrib.auth.models import User

class UserOwner(models.Model):
    idGSA = models.CharField(max_length=200,null=True)
    name = models.CharField(max_length=200,null=True)
    agency = models.CharField(max_length=200,null=True)
    agencyCode = models.CharField(max_length=200,null=True)
    userEmail = models.CharField(max_length=200,null=True)




class Keyword(models.Model):
    name = models.CharField(max_length=50)
    icon = models.CharField(max_length=35,null=True)
    activeSearch = models.BooleanField(default=False)
    delete = models.BooleanField(default=False)

class RFQModel(models.Model):
    idGSA = models.CharField(max_length=35,null=True)
    title = models.CharField(max_length=200,null=True)
    status = models.CharField(max_length=50,null=True)
    issueTime = models.CharField(max_length=50,null=True)
    closeTime = models.CharField(max_length=50,null=True)
    cancelTime = models.CharField(max_length=50,null=True)
    idOld = models.IntegerField(null=True)
    daysOpen = models.IntegerField(null=True)
    shipInd = models.IntegerField(null=True)
    referenceNum = models.CharField(max_length=50,null=True)
    description = models.TextField(null=True)
    deliveryDays = models.IntegerField(null=True)
    leadTime = models.CharField(max_length=50,null=True)
    password = models.CharField(max_length=50,null=True)
    sourceSought = models.BooleanField()
    extended = models.BooleanField()
    popStartDate = models.CharField(max_length=50,null=True)
    popEndDate = models.CharField(max_length=50,null=True)
    quoteCount = models.IntegerField(null=True)
    overseas = models.BooleanField()
    closedDate = models.CharField(max_length=50,null=True)
    closeHour = models.CharField(max_length=5,null=True)
    closeHourPMAM = models.CharField(max_length=3,null=True)
    valid = models.CharField(max_length=50,null=True)
    awardCount = models.IntegerField(null=True)
    connectRFQ = models.BooleanField()
    connectAwardableRFQ = models.BooleanField()
    closed = models.BooleanField()
    gwac = models.BooleanField()
    submitted = models.BooleanField()
    saved = models.BooleanField()
    openRFC = models.BooleanField()
    userOwner = models.ForeignKey(UserOwner, on_delete = models.PROTECT)

    def __str__(self):
        return self.idGSA +' '+self.title


class RFQKeyword(models.Model):
    rfq = models.ForeignKey(RFQModel, on_delete = models.PROTECT)
    keyword = models.ForeignKey(Keyword, on_delete = models.PROTECT)

class Attachments(models.Model):
    docName = models.CharField(max_length=200,null=True)
    docPath = models.CharField(max_length=200,null=True)
    docSeqNum = models.IntegerField(null=True)
    docType = models.IntegerField(null=True)
    docSessionId = models.IntegerField(null=True)
    docSessionDate = models.CharField(max_length=50,null=True)
    seqNum = models.IntegerField(null=True)
    rfq = models.ForeignKey(RFQModel, on_delete = models.PROTECT)

class Addresses(models.Model):
    addressType = models.CharField(max_length=50,null=True)
    addressDepartment = models.CharField(max_length=50,null=True)
    homeAddressAcknowledgement = models.BooleanField(default=False)
    country = models.CharField(max_length=50,null=True)
    countryName = models.CharField(max_length=50,null=True)
    addressName = models.CharField(max_length=100,null=True)
    agencyName = models.CharField(max_length=100,null=True)
    addressLine1 = models.CharField(max_length=100,null=True)
    addressLine2 = models.CharField(max_length=100,null=True)
    city = models.CharField(max_length=50,null=True)
    state = models.CharField(max_length=50,null=True)
    zipCode = models.CharField(max_length=50,null=True)
    defaultAddress = models.BooleanField(default=False)
    freightAddress = models.CharField(max_length=100,null=True)
    crpAddress = models.CharField(max_length=100,null=True)
    billingAddress = models.CharField(max_length=100,null=True)
    invoiceAddress = models.CharField(max_length=100,null=True)
    crpAAC = models.CharField(max_length=100,null=True)
    dodAAC = models.CharField(max_length=100,null=True)
    markFor = models.CharField(max_length=100,null=True)
    irsDataName = models.CharField(max_length=50,null=True)
    irsDataEmail = models.CharField(max_length=50,null=True)
    irsDataPhone = models.CharField(max_length=50,null=True)
    nameNotes = models.CharField(max_length=50,null=True)
    emailNotes = models.CharField(max_length=100,null=True)
    phoneNotes = models.CharField(max_length=100,null=True)
    shippingAacId = models.CharField(max_length=100,null=True)
    exportIndicator = models.CharField(max_length=100,null=True)
    controlProgram = models.CharField(max_length=100,null=True)
    valid = models.BooleanField(default=False)
    addressEmpty = models.BooleanField(default=False)
    irsDataExists = models.BooleanField(default=False)
    mandatorySet = models.BooleanField(default=False)
    invidualReceivingInfoValid = models.BooleanField(default=False)
    rfq = models.ForeignKey(RFQModel, on_delete = models.PROTECT)

class Modifications(models.Model):
    versionNumber = models.IntegerField(null=True)
    note = models.TextField(null=True)
    time = models.CharField(max_length=50,null=True)
    rfq = models.ForeignKey(RFQModel, on_delete = models.PROTECT)

class TokensGsa(models.Model): 
    tokenGSA = models.TextField(null=True)

class HistorySync(models.Model): 
    time = models.CharField(max_length=50,null=True)
    number = models.IntegerField(null=True)
    user = models.ForeignKey(User, on_delete = models.PROTECT)
    keyword = models.CharField(max_length=50,null=True)

class RFQHistorySync(models.Model): 
    time = models.CharField(max_length=50,null=True)
    user = models.ForeignKey(User, on_delete = models.PROTECT)
    rfq = models.ForeignKey(RFQModel, on_delete = models.PROTECT)

class LuchRFQComents(models.Model): 
    time = models.CharField(max_length=50,null=True)
    user = models.ForeignKey(User, on_delete = models.PROTECT)
    comment = models.TextField(null=True)
    rfq = models.ForeignKey(RFQModel, on_delete = models.PROTECT)


class CategoryByRFQ(models.Model):
    categoryId = models.CharField(max_length=50)
    schedule = models.CharField(max_length=50)
    sin = models.CharField(max_length=35,null=True)
    subCategory = models.IntegerField(null=True)
    subCategoryDescription = models.TextField(null=True)
    vendorCount = models.IntegerField(null=True)
    alreadyExists = models.BooleanField(default=False,null=True)
    valid = models.BooleanField(default=False,null=True)
    hideInEbuy = models.BooleanField(default=False,null=True)
    scheduleTitle = models.CharField(max_length=50,null=True)
    sinDescription1= models.CharField(max_length=50,null=True)
    sinDescription2= models.CharField(max_length=50,null=True)
    scheduleTypeId = models.IntegerField(null=True)
    rfq = models.ForeignKey(RFQModel, on_delete = models.PROTECT, default=0)

class VendorCategory(models.Model):
     contractNum = models.CharField(max_length=50)
     schedule = models.CharField(max_length=50)
     sin = models.CharField(max_length=35,null=True)
     subCategory = models.IntegerField(null=True)
     email = models.CharField(max_length=100)
     vendorCategoryKey = models.CharField(max_length=100)
     companyName = models.CharField(max_length=100,null=True)
     otherCategories = models.CharField(max_length=100)
     arravendor = models.BooleanField(default=False)
     category = models.ForeignKey(CategoryByRFQ, on_delete = models.PROTECT)