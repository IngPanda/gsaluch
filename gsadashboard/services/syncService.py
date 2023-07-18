import json
from ..models import RFQModel, UserOwner, Attachments, Modifications
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

def mapRfqs(data):
    infoRfq = data['rfq']['rfqInfo']
    try:
        user = UserOwner.objects.get(idGSA = data['userId'])
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
        rfq = RFQModel.objects.get(idGSA = data['rfqId'])  
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


def syncData(token):
    req = request.Request('https://www.ebuy.gsa.gov/ebuy/api/services/ebuyservices//seller/activerfqs/47QTCA22D003S')
    req.add_header('Content-Type', 'application/json')
    req.add_header('Authorization', 'Bearer '+token)
    response = request.urlopen(req)

    text = response.read()

    rfqJsons = json.loads(text.decode('utf-8'))['response']['47QTCA22D003S']
    rfqsModel = list(RFQModel.objects.all())

    empty = True if not bool(rfqsModel) else False
    for rfq in rfqJsons:
        mapRfqs(rfq)
