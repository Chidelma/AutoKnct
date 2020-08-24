import handlerDev
import handlerProd
from handlerDev import * 
from handlerProd import * 

s3Client = boto3.resource('s3')
dynamoDb = boto3.resource('dynamodb', 'ca-central-1')
table = dynamoDb.Table('AUTO')

minYear = int(datetime.now().strftime("%Y")) - 25

def hasJoinWords(p2, p1, curr):
    join1 = curr.islower() and p1.isupper() and p2.isupper() and p2 != None and p1 != None
    join2 = curr == 'n' and p1.isdigit() and p2.isupper() and p2 != None and p1 != None

    if join1 or join2:
        return True
    else:
        return False


def addAuction(event, context):

    urllib.urlretrieve('https://auto-arch.s3.ca-central-1.amazonaws.com/auctionnums/Num_Auction.txt', '/tmp/Num_Auction.txt')
    
    auctionNum = open('/tmp/Num_Auction.txt').readline()

    dt = datetime.now()
    td = timedelta(days=7)
    date = (dt + td).strftime("%Y-%m-%d")
    
    while True:
        url = "https://apps.mpi.mb.ca/salvage/auction.asp?salenm=" + str(auctionNum)
        page = requests.get(url)
        doc = lh.fromstring(page.content)
        headline = doc.xpath('//div[@id="mpi_app_headline"]')

        try:
            if(" ".join(headline[0].text_content().split()) == "Online Tender (Sortable List)"):
                break
            auctionNum = int(auctionNum)
            auctionNum += 1
            auctionNum = str(auctionNum)
        except IndexError:
            auctionNum = int(auctionNum)
            auctionNum += 1
            auctionNum = str(auctionNum)

    f = open("/tmp/Num_Auction.txt", "w")
    f.write(auctionNum)
    f.close()

    s3Client.meta.client.upload_file('/tmp/Num_Auction.txt', 'auto-arch', "auctionnums/Num_Auction.txt")

    tr_elements = doc.xpath('//tr')

    col = []

    i = 0

    for t in tr_elements[0]:
        i += 1
        name = t.text_content()
        #print '%d: "%s"' % (i, name)
        col.append((name, []))

    #Since out first row is the header, data is stored on the second row onwards
    for j in range(1, len(tr_elements)):
        #T is our j'th row
        T = tr_elements[j]
        
        #If row is not of size 7, the //tr data is not from our table 
        if len(T) != 8:
            break
        
        #i is the index of our column
        i = 0
        
        #Iterate through each element of the row
        for t in T.iterchildren():
            data = t.text_content() 

            if i > 0:
            #Convert any numerical value to integers
                try:
                    data = int(data)
                except:
                    pass
            #Append the data to the empty list of the i'th column
            col[i][1].append(data)
            #Increment i for the next column
            i += 1

    auctionNum = str(auctionNum)

    for row in range(0, len(col[0][1])):
        if col[1][1][row] > minYear and isinstance(col[1][1][row], int):

            model = " ".join(str(col[2][1][row]).split())

            for c in range(0, len(model)):
                try:
                    if hasJoinWords(model[c], model[c + 1], model[c + 2]):
                        model = model[:c + 1] + ' ' + model[c + 1:]
                        break
                    else:
                        continue
                except:
                    continue

            mileage = " ".join(col[6][1][row].split())
            mileage = mileage[:-13].replace(u"\u00a0", "").replace('a', '')

            cyl = None
            vin = None

            if "MI" in mileage:
                mileage = int(int(mileage.replace('MI', '')) * 1.6)
            else:
                if mileage != '':
                    mileage = int(mileage)
                else:
                    mileage = None

            if col[4][1][row] != "":
                cyl = col[4][1][row]

            if isinstance(col[3][1][row], str):
                vin = " ".join(col[3][1][row].split())
            elif isinstance(col[3][1][row], int):
                vin = " ".join(str(col[3][1]).split())
            else:
                vin = ''

            if vin != None or vin != '':
                n = int(len(vin) / 2)
                vin = [vin[i:i+n] for i in range(0, len(vin), n)]
                print(vin)

                try:
                    vin = vin[0] + " " + vin[1] + vin[2]
                except:
                    vin = vin[0] + " " + vin[1]

            urls = []

            for pic in range(1, 6):
                urllib.urlretrieve("https://apps.mpi.mb.ca/salvage/GetPicAll.asp?picnum=" + str(pic) + "&salenm=" + auctionNum + "&stndNum=" + str(col[0][1][row]), '/tmp/' + vin + "_" + date + "("+str(pic)+").jpg")
                if os.path.getsize('/tmp/' + vin + "_" + date + "(" + str(pic) + ").jpg") > 1208:
                    s3Client.meta.client.upload_file('/tmp/' + vin + "_" + date + "(" + str(pic) + ").jpg", 'auto-arch', "images/" + vin + "_" + date + "(" + str(pic) + ").jpg")
                    os.remove('/tmp/' + vin + "_" + date + "(" + str(pic) + ").jpg")
                    urls.append('https://auto-arch.s3.ca-central-1.amazonaws.com/images/' + vin + "_" + date + "(" + str(pic) + ").jpg")
                else:
                    os.remove('/tmp/' + vin + "_" + date + "(" + str(pic) + ").jpg")

            myquery = { "VIN" : vin, "Price" : None }

            if colMong.find(myquery).count() > 0:
                newvalues = { "$set": { "Date" : date, "Images" : urls } }

                colMong.update_many(myquery, newvalues)

                print("Item Updated")
            else:
                if vin != None or vin != '':
                    autoID = str(uuid.uuid5(uuid.NAMESPACE_DNS, vin + "_" + date))
                else:
                    autoID = str(uuid.uuid5(uuid.NAMESPACE_DNS, model + "_" + date))

                fireObj = {
                    '_id' : autoID,
                    'Year' : col[1][1][row],
                    'Model' : model,
                    'VIN' : None if vin == '' else " ".join(vin.split()),
                    'CYL' : cyl,
                    'Status' : col[5][1][row],
                    'Mileage' : mileage,
                    'Price' : None,
                    'Date' : date,
                    'Images' : urls,
                    'Location' : " ".join(str(col[7][1][row]).split())
                }

                colMong.insert_one(fireObj)

                print("imported " + autoID)


def addResult(event, context):

    urllib.urlretrieve('https://auto-arch.s3.ca-central-1.amazonaws.com/auctionnums/Num_Result.txt', '/tmp/Num_Result.txt')

    auctionNum = open('/tmp/Num_Result.txt', "r").readline() 

    dt = datetime.now()
    td = timedelta(days=2)
    date = (dt - td).strftime("%Y-%m-%d")

    url = "https://apps.mpi.mb.ca/salvage/SaleResults.asp?salenm=" + auctionNum
    page = requests.get(url)
    doc = lh.fromstring(page.content)

    tr_elements = doc.xpath('//tr')

    col = []

    i = 0

    for t in tr_elements[0]:
        i += 1
        name = t.text_content()
        #print '%d: "%s"' % (i, name)
        col.append((name, []))

    #Since out first row is the header, data is stored on the second row onwards
    for j in range(1, len(tr_elements)):
        #T is our j'th row
        T = tr_elements[j]
        
        #If row is not of size 8, the //tr data is not from our table 
        if len(T) != 9:
            break
        
        #i is the index of our column
        i = 0
        
        #Iterate through each element of the row
        for t in T.iterchildren():
            data = t.text_content() 

            if i > 0:
            #Convert any numerical value to integers
                try:
                    data = int(data)
                except:
                    pass
            #Append the data to the empty list of the i'th column
            col[i][1].append(data)
            #Increment i for the next column
            i += 1

    for row in range(0, len(col[0][1])):
        if col[1][1][row] > minYear and isinstance(col[1][1][row], int):

            vin = None

            if isinstance(col[3][1][row], str):
                vin = " ".join(col[3][1][row].split())
            elif isinstance(col[3][1][row], int):
                vin = " ".join(str(col[3][1]).split())
            else:
                vin = ''

            if vin != None or vin != '':
                n = int(len(vin) / 2)
                vin = [vin[i:i+n] for i in range(0, len(vin), n)]
                print(vin)

                try:
                    vin = vin[0] + " " + vin[1] + vin[2]
                except:
                    vin = vin[0] + " " + vin[1]

            price = int(col[8][1][row].replace('$', '').replace(',', '').replace('.00', ''))

            myquery = { "VIN" : " ".join(vin.split()), "Date" : str(date) }

            newvalues = { "$set": { "Price": price } }

            colMong.update_one(myquery, newvalues)

    myquery = { "Date" : str(date) }

    docs = colMong.find(myquery)

    for doc in docs:
        print("Transferring " + doc['_id'])
        db.collection(u'AUTOS').document(doc['_id']).set({
            u'Year' : doc['Year'],
            u'Model' : doc['Model'],
            u'VIN' : doc['VIN'],
            u'CYL' : doc['CYL'],
            u'Status' : doc['Status'],
            u'Mileage' : doc['Mileage'],
            u'Price' : doc['Price'],
            u'Date' : doc['Date'],
            u'Images' : doc['Images']
        })

        try:
            table.put_item(
                Item={
                    'id': doc['_id'],
                    'Model' : doc['Model'],
                    'Mileage' : doc['Mileage'],
                    'Price' : doc['Price'],
                    'Status' : doc['Status'],
                    'VIN' : doc['VIN'],
                    'Year' : doc['Year'],
                    'Images' : doc['Images'],
                    'Date' : doc['Date'],
                    'CYL' : doc['CYL']
                }
            )
        except:
            table.put_item(
                Item={
                    'id': doc['_id'],
                    'Model' : doc['Model'],
                    'Mileage' : doc['Mileage'] if doc['Mileage'] != u'' or doc['Mileage'] != None else None,
                    'Price' : doc['Price'] if doc['Price'] != u'' or doc['Price'] != None else None,
                    'Status' : doc['Status'] if doc['Status'] != u'' or doc['Status'] != None else None,
                    'VIN' : doc['VIN'] if doc['VIN'] != u'' or doc['VIN'] != '' else None,
                    'Year' : doc['Year'] if doc['Year'] != u'' or doc['Year'] != '' else None,
                    'Images' : None,
                    'Date' : doc['Date'],
                    'CYL' : doc['CYL'] if doc['CYL'] != "" or doc['CYL'] != None else None
                }
            )

            
    urllib.urlretrieve('https://auto-arch.s3.ca-central-1.amazonaws.com/auctionnums/Num_Auction.txt', '/tmp/Num_Auction.txt')

    auctionNum1 = open('/tmp/Num_Auction.txt',"r").readline() 
    auctionNum2 = str(int(auctionNum1) + 1)

    f = open('/tmp/Number.txt', "w")
    f.write(auctionNum1)
    f.close()

    s3Client.meta.client.upload_file('/tmp/Number.txt', 'auto-arch', "auctionnums/Num_Result.txt")

    f = open('/tmp/Number.txt', "w")
    f.write(auctionNum2)
    f.close()

    s3Client.meta.client.upload_file('/tmp/Number.txt', 'auto-arch', "auctionnums/Num_Auction.txt")

    os.remove('/tmp/Number.txt')
    os.remove('/tmp/Num_Auction.txt')
    os.remove('/tmp/Num_Result.txt')


def main(event, context):
    if 'localhost' in event['env']:

        if event['type'] != None:
            if event['func'] == 'initRecords':
                response = handlerDev.initRecords(event, context)
            if event['func'] == 'searchQuery':
                response = handlerDev.searchQuery(event, context)
            if event['func'] == 'checkUser':
                response = handlerDev.checkUser(event, context)
            if event['func'] == 'updateUser':
                response = handlerDev.updateUser(event, context)
            if event['func'] == 'deleteUser':
                response = handlerDev.deleteUser(event, context)
            if event['func'] == 'addToGarage':
                response = handlerDev.addToGarage(event, context)
            if event['func'] == 'removeAuto':
                response = handlerDev.removeAuto(event, context)
            if event['func'] == 'getAnalytics':
                response = handlerDev.getAnalytics(event, context)
            if event['func'] == 'postComment':
                response = handlerDev.postComment(event, context)
            if event['func'] == 'filterResult':
                response = handlerDev.filterResults(event, context)
            if event['func'] == 'getAllUsers' and event['type'] == 'AUSERS':
                response = handlerDev.getAllUsers()
            if event['func'] == 'resetEmail' and event['type'] == 'AUSERS':
                response = handlerDev.resetEmailPassword(event, context)
            if event['func'] == 'createUser' and event['type'] == 'AUSERS' and event['user'] == 'admin':
                response = handlerDev.createUser(event, context)
            if event['func'] == 'disableUser' and event['type'] == 'AUSERS':
                response = handlerDev.disableUser(event, context)
            if event['func'] == 'deleteUser' and event['type'] == 'AUSERS':
                response = handlerDev.deleteUser(event, context)
        else:
            if event['func'] == 'initRecords':
                response = handlerDev.initRecords(event, context)
            if event['func'] == 'checkUser':    
                response = handlerDev.checkUser(event, context)   
    else:
        if event['type'] != None:
            if event['func'] == 'initRecords':
                response = handlerProd.initRecords(event, context)
            if event['func'] == 'searchQuery':
                response = handlerProd.searchQuery(event, context)
            if event['func'] == 'checkUser':
                response = handlerProd.checkUser(event, context)
            if event['func'] == 'updateUser':
                response = handlerProd.updateUser(event, context)
            if event['func'] == 'deleteUser':
                response = handlerProd.deleteUser(event, context)
            if event['func'] == 'addToGarage':
                response = handlerProd.addToGarage(event, context)
            if event['func'] == 'removeAuto':
                response = handlerProd.removeAuto(event, context)
            if event['func'] == 'getAnalytics':
                response = handlerProd.getAnalytics(event, context)
            if event['func'] == 'postComment':
                response = handlerProd.postComment(event, context)
            if event['func'] == 'shareVehicle':
                response = handlerProd.shareVehicle(event, context)
            if event['func'] == 'filterResult':
                response = handlerProd.filterResults(event, context)
            if event['func'] == 'getAllUsers' and event['type'] == 'AUSERS':
                response = handlerProd.getAllUsers()
            if event['func'] == 'resetEmail' and event['type'] == 'AUSERS':
                response = handlerProd.resetEmailPassword(event, context)
            if event['func'] == 'createUser' and event['type'] == 'AUSERS' and event['user'] == 'admin':
                response = handlerProd.createUser(event, context)
            if event['func'] == 'disableUser' and event['type'] == 'AUSERS':
                response = handlerProd.disableUser(event, context)
            if event['func'] == 'deleteUser' and event['type'] == 'AUSERS':
                response = handlerProd.deleteUser(event, context)
        else:
            if event['func'] == 'initRecords':
                response = handlerProd.initRecords(event, context)
            if event['func'] == 'checkUser':    
                response = handlerProd.checkUser(event, context)
                
    return response