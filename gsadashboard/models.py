from django.db import models


class Account(models.Model):
    name = models.CharField(max_length=200,null=True)
    lastName = models.CharField(max_length=200, null= True)
    password = models.CharField(max_length=50,null=True)
    position = models.CharField(max_length=200, null = True)
    codeGSA = models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.name

class UserOwner(models.Model):
    idGSA = models.CharField(max_length=200,null=True)
    name = models.CharField(max_length=200,null=True)
    agency = models.CharField(max_length=200,null=True)
    agencyCode = models.CharField(max_length=200,null=True)
    userEmail = models.CharField(max_length=200,null=True)

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

class Attachments(models.Model):
    docName = models.CharField(max_length=200,null=True)
    docPath = models.CharField(max_length=200,null=True)
    docSeqNum = models.IntegerField(null=True)
    docType = models.IntegerField(null=True)
    docSessionId = models.IntegerField(null=True)
    docSessionDate = models.CharField(max_length=50,null=True)
    seqNum = models.IntegerField(null=True)
    rfq = models.ForeignKey(RFQModel, on_delete = models.PROTECT)


    

class Modifications(models.Model):
    versionNumber = models.IntegerField(null=True)
    note = models.TextField(null=True)
    time = models.CharField(max_length=50,null=True)
    rfq = models.ForeignKey(RFQModel, on_delete = models.PROTECT)

