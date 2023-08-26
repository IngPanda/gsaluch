import json
from ..models import CategoryByRFQ, RFQModel, UserOwner, Attachments, Modifications, HistorySync,Keyword,RFQKeyword,RFQHistorySync,Addresses, VendorCategory
from urllib import request, parse
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
def helperDate(date):
    if date:
        ts = int(date)
        return datetime.fromtimestamp(ts/1000).strftime('%Y-%m-%d %H:%M:%S')   
    else:
        return ' ' 
    
def syncModifications(mods,rfq):
    for mod in mods:
        try: 
            modify = Modifications.objects.get(note = mod['modificationNote'] )
            modify.note= mod['modificationNote']
            modify.versionNumber = mod['versionNumber']
            modify.time = helperDate(mod['modificationTime'])
            modify.rfq = rfq
            modify.save()
        except ObjectDoesNotExist:
            modify = Modifications.objects.create(
                note= mod['modificationNote'],
                versionNumber = mod['versionNumber'],
                time = helperDate(mod['modificationTime']),
                rfq = rfq
            )

def syncAttachments(docs,rfq):
    for doc in docs:
        try: 
            att = Attachments.objects.get(seqNum = doc['seqNum'], docName = doc['docName'] )
            att.docName = doc['docName']
            att.docPath = doc['docPath']
            att.docSeqNum = doc['docSeqNum']
            att.docType = doc['docType']
            att.docSessionId = doc['docSessionId']
            att.docSessionDate = helperDate(doc['docSessionDate'])
            att.seqNum = doc['seqNum']
            att.rfq = rfq
            att.save()
        except ObjectDoesNotExist:
            att =  Attachments.objects.create(
                docName = doc['docName'],
                docPath = doc['docPath'],
                docSeqNum = doc['docSeqNum'],
                docType = doc['docType'],
                docSessionId = doc['docSessionId'],
                docSessionDate = helperDate(doc['docSessionDate']),
                seqNum = doc['seqNum'],
                rfq = rfq
            )
def syncVendors(ven,category):
    try:
        vendorModel = VendorCategory.objects.get(contractNum = ven['contractNum'] )
        vendorModel.contractNum = ven['contractNum']
        vendorModel.schedule = ven['schedule']
        vendorModel.sin = ven['sin']
        vendorModel.subCategory = ven['subCategory']
        vendorModel.email = ven['email']
        vendorModel.vendorCategoryKey = ven['vendorCategoryKey']
        vendorModel.companyName = ven['companyName']
        vendorModel.otherCategories = ven['otherCategories']
        vendorModel.arravendor = ven['arravendor']
        vendorModel.save()
    except ObjectDoesNotExist:
        vendorModel = VendorCategory.objects.create(
                contractNum = ven['contractNum'],
                schedule = ven['schedule'],
                sin = ven['sin'],
                subCategory = ven['subCategory'],
                email = ven['email'],
                vendorCategoryKey = ven['vendorCategoryKey'],
                companyName = ven['companyName'],
                otherCategories = ven['otherCategories'],
                arravendor = ven['arravendor'],
                category = category
        )
        
def syncCategory(categories,rfq):
    for cat in categories: 
        try:
            catModel = CategoryByRFQ.objects.get(categoryId = cat['categoryId'])
            catModel.categoryId = cat['categoryId']
            catModel.schedule = cat['schedule']
            catModel.sin = cat['sin']
            catModel.subCategory = cat['subCategory']
            catModel.subCategoryDescription = cat['subCategoryDescription']
            catModel.vendorCount = cat['vendorCount']
            catModel.alreadyExists = cat['alreadyExists']
            catModel.valid = cat['valid']
            catModel.hideInEbuy = cat['hideInEbuy']
            catModel.scheduleTitle = cat['scheduleTitle']
            catModel.sinDescription1 = cat['sinDescription1']
            catModel.sinDescription2 = cat['sinDescription2']
            catModel.scheduleTypeId = cat['scheduleTypeId']
            catModel.save()
        except ObjectDoesNotExist:
             catModel = CategoryByRFQ.objects.create(
                categoryId = cat['categoryId'],
                schedule = cat['schedule'],
                sin = cat['sin'],
                subCategory = cat['subCategory'],
                subCategoryDescription = cat['subCategoryDescription'],
                vendorCount = cat['vendorCount'],
                alreadyExists = cat['alreadyExists'],
                valid = cat['valid'],
                hideInEbuy = cat['hideInEbuy'],
                scheduleTitle = cat['scheduleTitle'],
                sinDescription1 = cat['sinDescription1'],
                sinDescription2 = cat['sinDescription2'],
                scheduleTypeId = cat['scheduleTypeId'],
                rfq = rfq
            )
        
        for ven in cat['rfqVendors']:
            syncVendors(ven,catModel)

def syncAdresses(adress,rfq):

    for adres in adress:
        try: 
            adrsModel = Addresses.objects.get(addressName = adres['addressName'])
            adrsModel.addressName = adres['addressName']
            adrsModel.addressType = adres['addressType']
            adrsModel.addressDepartment = adres['addressDepartment']
            adrsModel.homeAddressAcknowledgement = adres['homeAddressAcknowledgement'] == 'true'
            adrsModel.country = adres['country']
            adrsModel.countryName = adres['countryName']
            adrsModel.agencyName = adres['agencyName']
            adrsModel.addressLine1 = adres['addressLine1']
            adrsModel.addressLine2 = adres['addressLine2']
            adrsModel.city = adres['city']
            adrsModel.state = adres['state']
            adrsModel.zipCode = adres['zip']
            adrsModel.defaultAddress = adres['defaultAddress'] == 'true'
            adrsModel.freightAddress = adres['freightAddress']
            adrsModel.crpAddress = adres['crpAddress']
            adrsModel.invoiceAddress = adres['invoiceAddress']
            adrsModel.crpAAC = adres['crpAAC']
            adrsModel.dodAAC = adres['dodAAC']
            adrsModel.markFor = adres['markFor']
            adrsModel.irsDataName = adres['irsData']['name']
            adrsModel.irsDataEmail = adres['irsData']['email']
            adrsModel.irsDataPhone = adres['irsData']['phone']
            adrsModel.nameNotes = adres['nameNotes']
            adrsModel.emailNotes = adres['emailNotes']
            adrsModel.phoneNotes = adres['phoneNotes']
            adrsModel.shippingAacId = adres['shippingAacId']
            adrsModel.exportIndicator = adres['exportIndicator']
            adrsModel.controlProgram = adres['controlProgram']
            adrsModel.valid = adres['valid'] == 'true'
            adrsModel.irsDataExists = adres['irsDataExists']== 'true'
            adrsModel.mandatorySet = adres['mandatorySet']== 'true'
            adrsModel.addressEmpty = adres['addressEmpty']== 'true'
            adrsModel.invidualReceivingInfoValid = adres['invidualReceivingInfoValid']== 'true'
            adrsModel.save()
        except ObjectDoesNotExist:
            Addresses.objects.create(
                addressName = adres['addressName'],
                addressType = adres['addressType'],
                addressDepartment = adres['addressDepartment'],
                homeAddressAcknowledgement = adres['homeAddressAcknowledgement'] == 'true',
                country = adres['country'],
                countryName = adres['countryName'],
                agencyName = adres['agencyName'],
                addressLine1 = adres['addressLine1'],
                addressLine2 = adres['addressLine2'],
                city = adres['city'],
                state = adres['state'],
                zipCode = adres['zip'],
                defaultAddress = adres['defaultAddress'] == 'true',
                freightAddress = adres['freightAddress'],
                crpAddress = adres['crpAddress'],
                invoiceAddress = adres['invoiceAddress'],
                crpAAC = adres['crpAAC'],
                dodAAC = adres['dodAAC'],
                markFor = adres['markFor'],
                irsDataName = adres['irsData']['name'],
                irsDataEmail = adres['irsData']['email'],
                irsDataPhone = adres['irsData']['phone'],
                nameNotes = adres['nameNotes'],
                emailNotes = adres['emailNotes'],
                phoneNotes = adres['phoneNotes'],
                shippingAacId = adres['shippingAacId'],
                exportIndicator = adres['exportIndicator'],
                controlProgram = adres['controlProgram'],
                valid = adres['valid'] == 'true',
                irsDataExists = adres['irsDataExists']== 'true',
                mandatorySet = adres['mandatorySet']== 'true',
                addressEmpty = adres['addressEmpty']== 'true',
                invidualReceivingInfoValid = adres['invidualReceivingInfoValid']== 'true',
                rfq = rfq
            )
def syncKeywordModel(rfqId,keywordId):
        try: 
            modify = RFQKeyword.objects.get(keyword_id = keywordId, rfq_id = rfqId).value()
        except ObjectDoesNotExist:
            modify = RFQKeyword.objects.create(
                keyword_id= keywordId,
                rfq_id = rfqId,
            )

def mapRfqs(data, keywordId = 12):
    infoRfq = data['rfq']['rfqInfo']
    try:
        user = UserOwner.objects.get(idGSA = data['userId']).value()
        user.idGSA = data['userId']
        user.name = data['userName']
        user.agency = data['userAgency']
        user.agencyCode = data['agencyCode']
        user.userEmail = data['userEmail']
        user.save()
    except ObjectDoesNotExist:
        user = UserOwner.objects.create(
            idGSA = data['userId'],
            name = data['userName'],
            agency = data['userAgency'],
            agencyCode = data['agencyCode'],
            userEmail = data['userEmail']
        )
   
    try:
        rfq = RFQModel.objects.get(idGSA = data['rfqId']).value()  
        #RFQ
        rfq.idGSA = data['rfqId']
        rfq.title = data['title']
        rfq.status = data['rfqStatusText']
        rfq.issueTime = helperDate(data['issueTime'])
        rfq.closeTime = helperDate(data['closeTime'])
        rfq.cancelTime = helperDate(data['cancelTime'])
        rfq.idOld = data['oid']
        rfq.daysOpen = infoRfq['rfqDaysOpen']
        rfq.shipInd = infoRfq['rfqShipInd']
        rfq.referenceNum = infoRfq['referenceNum']
        rfq.description = infoRfq['description']
        rfq.deliveryDays = infoRfq['deliveryDays']
        rfq.leadTime = infoRfq['leadTime']
        rfq.password = infoRfq['rfqPassword']
        rfq.sourceSought = infoRfq['sourceSought'] == 'true'
        rfq.extended = infoRfq['rfqExtended'] == 'true'
        rfq.popStartDate = helperDate(infoRfq['popStartDate'])
        rfq.popEndDate = helperDate(infoRfq['popEndDate'])
        rfq.quoteCount = infoRfq['quoteCount']
        rfq.overseas = infoRfq['overseas'] == 'true'
        rfq.closedDate = helperDate(infoRfq['closeDate'])
        rfq.closeHour = infoRfq['closeHour']
        rfq.closeHourPMAM = infoRfq['closeHourAmPm']
        rfq.connectRFQ = infoRfq['connectRfq']== 'true'
        rfq.connectAwardableRFQ = infoRfq['connectAwardableRfq']== 'true'
        rfq.closed = infoRfq['rfqClosed']== 'true'
        rfq.gwac = infoRfq['gwac']== 'true'
        rfq.submitted = infoRfq['rfqSubmitted']== 'true'
        rfq.saved = infoRfq['rfqSaved']== 'true'
        rfq.openRFC = infoRfq['rfqOpen']== 'true'
        rfq.userOwner = user
        rfq.save()
    except ObjectDoesNotExist:
        rfq = RFQModel.objects.create(
            idGSA = data['rfqId'],
            title = data['title'],
            status = data['rfqStatusText'],
            issueTime = helperDate(data['issueTime']),
            closeTime = helperDate(data['closeTime']),
            cancelTime = helperDate(data['cancelTime']),
            idOld = data['oid'],
            daysOpen = infoRfq['rfqDaysOpen'],
            shipInd = infoRfq['rfqShipInd'],
            referenceNum = infoRfq['referenceNum'],
            description = infoRfq['description'],
            deliveryDays = infoRfq['deliveryDays'],
            leadTime = infoRfq['leadTime'],
            password = infoRfq['rfqPassword'],
            sourceSought = infoRfq['sourceSought'] == 'true',
            extended = infoRfq['rfqExtended'] == 'true',
            popStartDate = helperDate(infoRfq['popStartDate']),
            popEndDate = helperDate(infoRfq['popEndDate']),
            quoteCount = infoRfq['quoteCount'],
            overseas = infoRfq['overseas'] == 'true',
            closedDate = helperDate(infoRfq['closeDate']),
            closeHour = infoRfq['closeHour'],
            closeHourPMAM = infoRfq['closeHourAmPm'],
            connectRFQ = infoRfq['connectRfq']== 'true',
            connectAwardableRFQ = infoRfq['connectAwardableRfq']== 'true',
            closed = infoRfq['rfqClosed']== 'true',
            gwac = infoRfq['gwac']== 'true',
            submitted = infoRfq['rfqSubmitted']== 'true',
            saved = infoRfq['rfqSaved']== 'true',
            openRFC = infoRfq['rfqOpen']== 'true',
            userOwner = user
        )
 
    if data['rfq']['rfqQAAttachments']:
        syncAttachments(data['rfq']['rfqQAAttachments'],rfq)
    if data['rfq']['rfqModifications']:
        syncModifications(data['rfq']['rfqModifications'],rfq)
    
    syncKeywordModel(rfq.id,keywordId)

def syncByCategory(token):
    keywords = list(Keyword.objects.exclude(name='default', activeSearch = True, delete= False).values()) 
    for keyword in keywords:
        req = request.Request('https://www.ebuy.gsa.gov/ebuy/api/services/ebuyservices//seller/searchactiverfqs', method="POST")
        req.add_header('Content-Type', 'application/json')
        req.add_header('Authorization', 'Bearer '+token)
        seach = keyword["name"]
        seachId = keyword["id"]
        data={"contractnumber":"47QTCA22D003S","query": seach.replace(" ","").lower(),"matchtype":1,"sortspec":"CloseDate dsc"}
        data = json.dumps(data)
        data = data.encode()
        r = request.urlopen(req, data=data)
        text = r.read()
        rfqJsons = json.loads(text.decode('utf-8'))['response']['47QTCA22D003S']

        if rfqJsons is not None:
            for rfq in rfqJsons:
                mapRfqs(rfq, seachId)
    

def syncDataGeneral(token, user):
    req = request.Request('https://www.ebuy.gsa.gov/ebuy/api/services/ebuyservices//seller/activerfqs/47QTCA22D003S')
    req.add_header('Content-Type', 'application/json')
    req.add_header('Authorization', 'Bearer '+token)
    response = request.urlopen(req)

    text = response.read()

    rfqJsons = json.loads(text.decode('utf-8'))['response']['47QTCA22D003S']

    for rfq in rfqJsons:
        mapRfqs(rfq)

    
    number_of_elements = len(rfqJsons)
    HistorySync.objects.create(
                number = number_of_elements,
                time = datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                user = user
    )

def syncSingleCategory(token, keyword, keywordId, user):
    req = request.Request('https://www.ebuy.gsa.gov/ebuy/api/services/ebuyservices//seller/searchactiverfqs', method="POST")
    req.add_header('Content-Type', 'application/json')
    req.add_header('Authorization', 'Bearer '+token)
    data={"contractnumber":"47QTCA22D003S","query": keyword.replace(" ","").lower(),"matchtype":1,"sortspec":"CloseDate dsc"}
    data = json.dumps(data)
    data = data.encode()
    r = request.urlopen(req, data=data)
    text = r.read()
    rfqJsons = json.loads(text.decode('utf-8'))['response']['47QTCA22D003S']
    if rfqJsons is not None:
            for rfq in rfqJsons:
                mapRfqs(rfq, keywordId)
    number_of_elements = 0 if rfqJsons == None else len(rfqJsons)
    HistorySync.objects.create(
                number = number_of_elements,
                time = datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                keyword = keyword,
                user = user )

def syncDetail(token, user,GSAID):
    req = request.Request('https://www.ebuy.gsa.gov/ebuy/api/services/ebuyservices//seller/rfq/'+GSAID+'/47QTCA22D003S')
    req.add_header('Content-Type', 'application/json')
    req.add_header('Authorization', 'Bearer '+token)
    response = request.urlopen(req)

    text = response.read()

    data = json.loads(text.decode('utf-8'))['response']
    rfq = RFQModel.objects.get(idGSA = data['rfqInfo']['rfqId']) 
    Att_A = data['rfqQAAttachments']
    Att_B = data['rfqAttachments']
    mods = data['rfqModifications']
    gsAdresss = data['rfqAddresses']
    gsaCategories = data['rfqCategories']
    att = Att_A + Att_B
    syncAttachments(att,rfq)
    syncModifications(mods,rfq)
    syncAdresses(gsAdresss,rfq)
    syncCategory(gsaCategories,rfq)
    RFQHistorySync.objects.create(
                time = datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                rfq = rfq,
                user = user )
    rfq.syncLuch = True
    rfq.save()